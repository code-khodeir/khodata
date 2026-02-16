"""Data Lake architecture for managing raw and processed real estate data."""

import os
import json
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class DataLake:
    """Manages data lake with multiple zones for different processing stages.
    
    Zones:
    - raw: Original unprocessed data
    - staging: Cleaned and validated data
    - processed: Transformed data ready for analytics
    - curated: Aggregated and business-ready datasets
    """
    
    def __init__(self, base_path: str = "./data_lake"):
        """Initialize data lake structure.
        
        Args:
            base_path: Root directory for data lake
        """
        self.base_path = Path(base_path)
        self.zones = {
            "raw": self.base_path / "raw",
            "staging": self.base_path / "staging",
            "processed": self.base_path / "processed",
            "curated": self.base_path / "curated"
        }
        self._create_structure()
    
    def _create_structure(self) -> None:
        """Create data lake directory structure."""
        for zone_path in self.zones.values():
            zone_path.mkdir(parents=True, exist_ok=True)
            
            # Create domain subdirectories
            for domain in ["properties", "clients", "transactions", "marketing"]:
                (zone_path / domain).mkdir(exist_ok=True)
    
    def ingest_raw_data(
        self,
        data: Any,
        domain: str,
        source: str,
        format: str = "json"
    ) -> str:
        """Ingest data into raw zone.
        
        Args:
            data: Data to ingest (DataFrame, dict, or list)
            domain: Data domain (properties, clients, etc.)
            source: Source system name
            format: Output format (json, csv, parquet)
            
        Returns:
            Path to ingested file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source}_{timestamp}.{format}"
        filepath = self.zones["raw"] / domain / filename
        
        if isinstance(data, pd.DataFrame):
            if format == "csv":
                data.to_csv(filepath, index=False)
            elif format == "parquet":
                data.to_parquet(filepath, index=False)
            else:  # json
                data.to_json(filepath, orient="records", indent=2)
        elif isinstance(data, (dict, list)):
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")
        
        # Create metadata
        self._write_metadata(filepath, domain, source, format)
        
        return str(filepath)
    
    def _write_metadata(
        self,
        filepath: Path,
        domain: str,
        source: str,
        format: str
    ) -> None:
        """Write metadata for ingested file.
        
        Args:
            filepath: Path to data file
            domain: Data domain
            source: Source system
            format: File format
        """
        metadata = {
            "filepath": str(filepath),
            "domain": domain,
            "source": source,
            "format": format,
            "ingestion_timestamp": datetime.now().isoformat(),
            "file_size_bytes": filepath.stat().st_size if filepath.exists() else 0
        }
        
        metadata_path = filepath.with_suffix(filepath.suffix + ".meta")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def promote_to_staging(
        self,
        raw_filepath: str,
        cleaned_data: pd.DataFrame
    ) -> str:
        """Promote cleaned data from raw to staging zone.
        
        Args:
            raw_filepath: Original raw file path
            cleaned_data: Cleaned DataFrame
            
        Returns:
            Path to staging file
        """
        raw_path = Path(raw_filepath)
        relative_path = raw_path.relative_to(self.zones["raw"])
        staging_path = self.zones["staging"] / relative_path
        staging_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to staging
        if raw_path.suffix == ".csv":
            cleaned_data.to_csv(staging_path, index=False)
        elif raw_path.suffix == ".parquet":
            cleaned_data.to_parquet(staging_path, index=False)
        else:
            cleaned_data.to_json(staging_path, orient="records", indent=2)
        
        return str(staging_path)
    
    def promote_to_processed(
        self,
        staging_filepath: str,
        transformed_data: pd.DataFrame,
        transformation_name: str
    ) -> str:
        """Promote transformed data to processed zone.
        
        Args:
            staging_filepath: Staging file path
            transformed_data: Transformed DataFrame
            transformation_name: Name of transformation applied
            
        Returns:
            Path to processed file
        """
        staging_path = Path(staging_filepath)
        relative_path = staging_path.relative_to(self.zones["staging"])
        
        # Add transformation name to filename
        processed_filename = f"{staging_path.stem}_{transformation_name}{staging_path.suffix}"
        processed_path = self.zones["processed"] / relative_path.parent / processed_filename
        processed_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to processed (prefer parquet for efficiency)
        transformed_data.to_parquet(
            processed_path.with_suffix(".parquet"),
            index=False
        )
        
        return str(processed_path.with_suffix(".parquet"))
    
    def get_catalog(self, zone: str = "all") -> List[Dict[str, Any]]:
        """Get catalog of files in data lake.
        
        Args:
            zone: Zone to catalog (raw, staging, processed, curated, or all)
            
        Returns:
            List of file metadata dictionaries
        """
        catalog = []
        
        zones_to_scan = [zone] if zone != "all" else list(self.zones.keys())
        
        for zone_name in zones_to_scan:
            zone_path = self.zones[zone_name]
            
            for filepath in zone_path.rglob("*"):
                if filepath.is_file() and not filepath.suffix == ".meta":
                    metadata_path = filepath.with_suffix(filepath.suffix + ".meta")
                    
                    file_info = {
                        "zone": zone_name,
                        "filepath": str(filepath),
                        "filename": filepath.name,
                        "size_bytes": filepath.stat().st_size,
                        "modified": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
                    }
                    
                    # Add metadata if available
                    if metadata_path.exists():
                        with open(metadata_path, 'r') as f:
                            file_info.update(json.load(f))
                    
                    catalog.append(file_info)
        
        return catalog
    
    def read_data(self, filepath: str) -> pd.DataFrame:
        """Read data from data lake.
        
        Args:
            filepath: Path to file
            
        Returns:
            DataFrame with data
        """
        path = Path(filepath)
        
        if path.suffix == ".csv":
            return pd.read_csv(path)
        elif path.suffix == ".parquet":
            return pd.read_parquet(path)
        elif path.suffix == ".json":
            return pd.read_json(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
