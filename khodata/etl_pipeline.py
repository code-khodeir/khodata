"""ETL Pipeline for real estate data processing."""

import pandas as pd
from typing import Dict, List, Optional, Any
from khodata.schema_mapper import HeaderMapper
from khodata.data_lake import DataLake
from khodata.analytics import RealEstateAnalytics
from khodata.ml_models import PropertyValuationModel, LeadScoringModel


class RealEstateETL:
    """ETL pipeline for processing real estate data.
    
    Orchestrates the flow from raw data ingestion through
    schema mapping, data lake storage, analytics, and ML predictions.
    """
    
    def __init__(self, data_lake_path: str = "./data_lake"):
        """Initialize ETL pipeline.
        
        Args:
            data_lake_path: Path to data lake root directory
        """
        self.mapper = HeaderMapper()
        self.data_lake = DataLake(data_lake_path)
        self.analytics = RealEstateAnalytics()
        self.property_model = PropertyValuationModel()
        self.lead_model = LeadScoringModel()
    
    def ingest_raw_data(
        self,
        data: Any,
        domain: str,
        source: str,
        format: str = "json"
    ) -> str:
        """Ingest raw data into data lake.
        
        Args:
            data: Raw data to ingest
            domain: Data domain (properties, clients, transactions, marketing)
            source: Source system name
            format: File format
            
        Returns:
            Path to ingested file
        """
        return self.data_lake.ingest_raw_data(data, domain, source, format)
    
    def process_property_data(
        self,
        raw_data: pd.DataFrame,
        source: str
    ) -> Dict[str, Any]:
        """Process property listing data through the pipeline.
        
        Args:
            raw_data: Raw property DataFrame with inconsistent headers
            source: Source system name
            
        Returns:
            Dictionary with processing results and file paths
        """
        results = {}
        
        # Step 1: Ingest raw data
        raw_path = self.data_lake.ingest_raw_data(
            raw_data,
            domain="properties",
            source=source,
            format="csv"
        )
        results['raw_path'] = raw_path
        
        # Step 2: Map headers to standard schema
        header_mapping = self.mapper.map_headers(raw_data.columns.tolist())
        mapped_data = raw_data.rename(columns=header_mapping)
        results['header_mapping'] = header_mapping
        
        # Step 3: Clean and validate
        cleaned_data = self._clean_property_data(mapped_data)
        
        # Step 4: Promote to staging
        staging_path = self.data_lake.promote_to_staging(raw_path, cleaned_data)
        results['staging_path'] = staging_path
        
        # Step 5: Calculate derived metrics
        transformed_data = self._transform_property_data(cleaned_data)
        
        # Step 6: Promote to processed
        processed_path = self.data_lake.promote_to_processed(
            staging_path,
            transformed_data,
            "enriched"
        )
        results['processed_path'] = processed_path
        
        # Step 7: Run analytics
        self.analytics.load_properties(transformed_data)
        results['metrics'] = self.analytics.calculate_property_metrics()
        
        return results
    
    def process_client_data(
        self,
        raw_data: pd.DataFrame,
        source: str
    ) -> Dict[str, Any]:
        """Process client/lead data through the pipeline.
        
        Args:
            raw_data: Raw client DataFrame
            source: Source system name
            
        Returns:
            Dictionary with processing results
        """
        results = {}
        
        # Ingest and map
        raw_path = self.data_lake.ingest_raw_data(
            raw_data,
            domain="clients",
            source=source,
            format="csv"
        )
        results['raw_path'] = raw_path
        
        header_mapping = self.mapper.map_headers(raw_data.columns.tolist())
        mapped_data = raw_data.rename(columns=header_mapping)
        results['header_mapping'] = header_mapping
        
        # Clean
        cleaned_data = self._clean_client_data(mapped_data)
        
        # Promote through zones
        staging_path = self.data_lake.promote_to_staging(raw_path, cleaned_data)
        results['staging_path'] = staging_path
        
        # Load into analytics
        self.analytics.load_clients(cleaned_data)
        results['metrics'] = self.analytics.calculate_conversion_metrics()
        
        return results
    
    def process_campaign_data(
        self,
        raw_data: pd.DataFrame,
        source: str
    ) -> Dict[str, Any]:
        """Process marketing campaign data.
        
        Args:
            raw_data: Raw campaign DataFrame
            source: Source system name
            
        Returns:
            Dictionary with processing results and ROI metrics
        """
        results = {}
        
        # Ingest and map
        raw_path = self.data_lake.ingest_raw_data(
            raw_data,
            domain="marketing",
            source=source,
            format="csv"
        )
        results['raw_path'] = raw_path
        
        header_mapping = self.mapper.map_headers(raw_data.columns.tolist())
        mapped_data = raw_data.rename(columns=header_mapping)
        
        # Clean and calculate ROI metrics
        cleaned_data = self._clean_campaign_data(mapped_data)
        
        # Promote
        staging_path = self.data_lake.promote_to_staging(raw_path, cleaned_data)
        results['staging_path'] = staging_path
        
        # Analytics
        self.analytics.load_campaigns(cleaned_data)
        results['roi_metrics'] = self.analytics.calculate_marketing_roi()
        results['insights'] = self.analytics.get_insights()
        
        return results
    
    def _clean_property_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean property data.
        
        Args:
            df: Property DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        cleaned = df.copy()
        
        # Remove duplicates
        if 'property_id' in cleaned.columns:
            cleaned = cleaned.drop_duplicates(subset=['property_id'])
        
        # Handle missing values
        numeric_cols = ['bedrooms', 'bathrooms', 'square_feet', 'price']
        for col in numeric_cols:
            if col in cleaned.columns:
                cleaned[col] = pd.to_numeric(cleaned[col], errors='coerce')
        
        # Remove invalid prices
        if 'price' in cleaned.columns:
            cleaned = cleaned[cleaned['price'] > 0]
        
        return cleaned
    
    def _transform_property_data(self, df: pd.DataFrame, reference_year: Optional[int] = None) -> pd.DataFrame:
        """Add calculated fields to property data.
        
        Args:
            df: Cleaned property DataFrame
            reference_year: Reference year for age calculation (defaults to current year)
            
        Returns:
            Transformed DataFrame
        """
        transformed = df.copy()
        
        # Calculate price per square foot
        if 'price' in transformed.columns and 'square_feet' in transformed.columns:
            transformed['price_per_sqft'] = transformed['price'] / transformed['square_feet']
        
        # Property age
        if 'year_built' in transformed.columns:
            from datetime import datetime
            if reference_year is None:
                reference_year = datetime.now().year
            transformed['property_age'] = reference_year - transformed['year_built']
        
        return transformed
    
    def _clean_client_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean client data.
        
        Args:
            df: Client DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        cleaned = df.copy()
        
        # Remove duplicates
        if 'client_id' in cleaned.columns:
            cleaned = cleaned.drop_duplicates(subset=['client_id'])
        elif 'email' in cleaned.columns:
            cleaned = cleaned.drop_duplicates(subset=['email'])
        
        # Standardize lead status
        if 'lead_status' in cleaned.columns:
            cleaned['lead_status'] = cleaned['lead_status'].str.lower().str.strip()
        
        return cleaned
    
    def _clean_campaign_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and enrich campaign data.
        
        Args:
            df: Campaign DataFrame
            
        Returns:
            Cleaned and enriched DataFrame
        """
        cleaned = df.copy()
        
        # Calculate derived metrics
        if 'clicks' in cleaned.columns and 'impressions' in cleaned.columns:
            cleaned['ctr'] = (cleaned['clicks'] / cleaned['impressions'].replace(0, 1)) * 100
        
        if 'conversions' in cleaned.columns and 'clicks' in cleaned.columns:
            cleaned['conversion_rate'] = (cleaned['conversions'] / cleaned['clicks'].replace(0, 1)) * 100
        
        if 'conversions' in cleaned.columns and 'campaign_cost' in cleaned.columns:
            cleaned['cost_per_conversion'] = cleaned['campaign_cost'] / cleaned['conversions'].replace(0, 1)
        
        if 'revenue_generated' in cleaned.columns and 'campaign_cost' in cleaned.columns:
            cleaned['roi'] = ((cleaned['revenue_generated'] - cleaned['campaign_cost']) / 
                             cleaned['campaign_cost'].replace(0, 1)) * 100
        
        return cleaned
    
    def run_full_analytics(self) -> Dict[str, Any]:
        """Run complete analytics across all loaded data.
        
        Returns:
            Dictionary with comprehensive analytics results
        """
        results = {
            'property_metrics': self.analytics.calculate_property_metrics(),
            'conversion_metrics': self.analytics.calculate_conversion_metrics(),
            'marketing_roi': self.analytics.calculate_marketing_roi(),
            'insights': self.analytics.get_insights()
        }
        
        return results
    
    def get_data_catalog(self) -> List[Dict[str, Any]]:
        """Get catalog of all data in the data lake.
        
        Returns:
            List of file metadata
        """
        return self.data_lake.get_catalog()
