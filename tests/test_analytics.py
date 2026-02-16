"""Tests for real estate analytics functionality."""

import unittest
import pandas as pd
import numpy as np
from khodata.analytics import RealEstateAnalytics


class TestRealEstateAnalytics(unittest.TestCase):
    """Test cases for RealEstateAnalytics class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analytics = RealEstateAnalytics()
        
        # Sample property data
        self.properties = pd.DataFrame([
            {'property_id': 1, 'price': 250000, 'square_feet': 1500, 'property_type': 'house', 'days_on_market': 30},
            {'property_id': 2, 'price': 350000, 'square_feet': 2000, 'property_type': 'house', 'days_on_market': 45},
            {'property_id': 3, 'price': 150000, 'square_feet': 1000, 'property_type': 'condo', 'days_on_market': 20},
        ])
        
        # Sample client data
        self.clients = pd.DataFrame([
            {'client_id': 1, 'lead_status': 'converted', 'lead_source': 'website', 'lead_score': 85},
            {'client_id': 2, 'lead_status': 'active', 'lead_source': 'referral', 'lead_score': 70},
            {'client_id': 3, 'lead_status': 'converted', 'lead_source': 'website', 'lead_score': 90},
            {'client_id': 4, 'lead_status': 'lost', 'lead_source': 'email', 'lead_score': 45},
        ])
        
        # Sample campaign data
        self.campaigns = pd.DataFrame([
            {'campaign_id': 1, 'campaign_name': 'Summer Sale', 'campaign_cost': 5000, 
             'impressions': 100000, 'clicks': 5000, 'conversions': 50, 'revenue_generated': 25000},
            {'campaign_id': 2, 'campaign_name': 'Fall Promo', 'campaign_cost': 3000,
             'impressions': 50000, 'clicks': 2500, 'conversions': 30, 'revenue_generated': 18000},
        ])
    
    def test_property_metrics_calculation(self):
        """Test property metrics calculation."""
        self.analytics.load_properties(self.properties)
        metrics = self.analytics.calculate_property_metrics()
        
        self.assertEqual(metrics['total_listings'], 3)
        self.assertAlmostEqual(metrics['average_price'], 250000, delta=1000)
        self.assertIn('price_by_type', metrics)
        self.assertIn('avg_days_on_market', metrics)
    
    def test_conversion_metrics_calculation(self):
        """Test conversion metrics calculation."""
        self.analytics.load_clients(self.clients)
        metrics = self.analytics.calculate_conversion_metrics()
        
        self.assertEqual(metrics['total_leads'], 4)
        self.assertAlmostEqual(metrics['conversion_rate'], 50.0, delta=1)
        self.assertIn('conversion_rate_by_source', metrics)
    
    def test_marketing_roi_calculation(self):
        """Test marketing ROI calculation."""
        self.analytics.load_campaigns(self.campaigns)
        metrics = self.analytics.calculate_marketing_roi()
        
        self.assertEqual(metrics['total_campaigns'], 2)
        self.assertEqual(metrics['total_spend'], 8000)
        self.assertEqual(metrics['total_conversions'], 80)
        self.assertIn('roi', metrics)
        self.assertGreater(metrics['roi'], 0)
    
    def test_insights_generation(self):
        """Test insights generation."""
        self.analytics.load_properties(self.properties)
        self.analytics.load_clients(self.clients)
        self.analytics.load_campaigns(self.campaigns)
        
        insights = self.analytics.get_insights()
        
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        # Check that insights contain relevant information
        insights_text = ' '.join(insights)
        self.assertTrue(any(word in insights_text.lower() for word in ['listing', 'conversion', 'roi']))
    
    def test_empty_data_handling(self):
        """Test handling of empty datasets."""
        metrics = self.analytics.calculate_property_metrics()
        self.assertIn('error', metrics)
        
        metrics = self.analytics.calculate_conversion_metrics()
        self.assertIn('error', metrics)


if __name__ == "__main__":
    unittest.main()
