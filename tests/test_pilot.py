"""Tests for the pilot module."""

import unittest
from khodata.pilot import DataAnalyzer


class TestDataAnalyzer(unittest.TestCase):
    """Test cases for DataAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = DataAnalyzer()
        self.sample_data = [
            {"name": "Alice", "age": 30, "score": 85.5},
            {"name": "Bob", "age": 25, "score": 92.0},
            {"name": "Charlie", "age": 35, "score": 78.5},
        ]
    
    def test_load_data_from_list(self):
        """Test loading data from a list of dictionaries."""
        self.analyzer.load_data(self.sample_data)
        self.assertIsNotNone(self.analyzer.data)
        self.assertEqual(len(self.analyzer.data), 3)
    
    def test_load_data_from_dict(self):
        """Test loading data from a single dictionary."""
        single_record = {"name": "Alice", "age": 30}
        self.analyzer.load_data(single_record)
        self.assertIsNotNone(self.analyzer.data)
        self.assertEqual(len(self.analyzer.data), 1)
    
    def test_get_summary(self):
        """Test getting data summary."""
        self.analyzer.load_data(self.sample_data)
        summary = self.analyzer.get_summary()
        
        self.assertEqual(summary["rows"], 3)
        self.assertEqual(summary["columns"], 3)
        self.assertIn("name", summary["column_names"])
        self.assertIn("age", summary["column_names"])
        self.assertIn("score", summary["column_names"])
    
    def test_get_summary_no_data(self):
        """Test getting summary when no data is loaded."""
        summary = self.analyzer.get_summary()
        self.assertIn("error", summary)
    
    def test_check_quality(self):
        """Test data quality check."""
        self.analyzer.load_data(self.sample_data)
        quality = self.analyzer.check_quality()
        
        self.assertIn("missing_values", quality)
        self.assertIn("duplicate_rows", quality)
        self.assertIn("completeness_percentage", quality)
        self.assertEqual(quality["completeness_percentage"], 100.0)
    
    def test_check_quality_with_missing_values(self):
        """Test quality check with missing values."""
        data_with_missing = [
            {"name": "Alice", "age": 30, "score": 85.5},
            {"name": "Bob", "age": None, "score": 92.0},
            {"name": "Charlie", "age": 35, "score": None},
        ]
        self.analyzer.load_data(data_with_missing)
        quality = self.analyzer.check_quality()
        
        self.assertLess(quality["completeness_percentage"], 100.0)
    
    def test_get_insights(self):
        """Test getting insights."""
        self.analyzer.load_data(self.sample_data)
        insights = self.analyzer.get_insights()
        
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        self.assertTrue(any("3 rows" in insight for insight in insights))
    
    def test_get_insights_no_data(self):
        """Test getting insights when no data is loaded."""
        insights = self.analyzer.get_insights()
        self.assertEqual(insights, ["No data loaded"])


if __name__ == "__main__":
    unittest.main()
