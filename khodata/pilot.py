"""Pilot module for data intelligence operations."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


class DataAnalyzer:
    """Core data analyzer for the pilot feature.
    
    This class provides basic data intelligence capabilities including:
    - Data loading and preprocessing
    - Statistical analysis
    - Data quality checks
    """
    
    def __init__(self):
        """Initialize the DataAnalyzer.
        
        Attributes:
            data: pandas DataFrame that holds the loaded data. Initially None.
        """
        self.data = None
        
    def load_data(self, data: Any) -> None:
        """Load data into the analyzer.
        
        Args:
            data: Data to analyze (dict, list, or DataFrame)
        """
        if isinstance(data, pd.DataFrame):
            self.data = data
        elif isinstance(data, dict):
            self.data = pd.DataFrame([data])
        elif isinstance(data, list):
            self.data = pd.DataFrame(data)
        else:
            raise ValueError("Unsupported data type")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get statistical summary of the loaded data.
        
        Returns:
            Dictionary containing summary statistics
        """
        if self.data is None:
            return {"error": "No data loaded"}
        
        summary = {
            "rows": len(self.data),
            "columns": len(self.data.columns),
            "column_names": list(self.data.columns),
            "dtypes": self.data.dtypes.to_dict(),
        }
        
        # Add numeric statistics
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            summary["numeric_summary"] = self.data[numeric_cols].describe().to_dict()
        
        return summary
    
    def check_quality(self) -> Dict[str, Any]:
        """Check data quality metrics.
        
        Returns:
            Dictionary containing quality metrics
        """
        if self.data is None:
            return {"error": "No data loaded"}
        
        quality = {
            "missing_values": self.data.isnull().sum().to_dict(),
            "duplicate_rows": int(self.data.duplicated().sum()),
            "total_cells": int(self.data.size),
        }
        
        # Calculate completeness percentage
        missing_values = self.data.isnull().sum().sum()
        quality["completeness_percentage"] = round(
            ((quality["total_cells"] - missing_values) / quality["total_cells"]) * 100, 2
        )
        
        return quality
    
    def get_insights(self) -> List[str]:
        """Generate basic insights from the data.
        
        Returns:
            List of insight strings
        """
        if self.data is None:
            return ["No data loaded"]
        
        insights = []
        
        # Data size insight
        insights.append(f"Dataset contains {len(self.data)} rows and {len(self.data.columns)} columns")
        
        # Missing data insight
        missing_count = self.data.isnull().sum().sum()
        if missing_count > 0:
            insights.append(f"Found {missing_count} missing values across the dataset")
        else:
            insights.append("No missing values detected")
        
        # Duplicate insight
        dup_count = self.data.duplicated().sum()
        if dup_count > 0:
            insights.append(f"Found {dup_count} duplicate rows")
        
        # Numeric columns insight
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            insights.append(f"Dataset has {len(numeric_cols)} numeric columns")
        
        return insights
