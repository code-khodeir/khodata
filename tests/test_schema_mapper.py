"""Tests for header mapping functionality."""

import unittest
from khodata.schema_mapper import HeaderMapper


class TestHeaderMapper(unittest.TestCase):
    """Test cases for HeaderMapper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mapper = HeaderMapper()
    
    def test_exact_match(self):
        """Test exact header matching."""
        headers = ['price', 'bedrooms', 'address']
        mapping = self.mapper.map_headers(headers)
        
        self.assertEqual(mapping['price'], 'price')
        self.assertEqual(mapping['bedrooms'], 'bedrooms')
        self.assertEqual(mapping['address'], 'address')
    
    def test_case_insensitive_match(self):
        """Test case-insensitive matching."""
        headers = ['PRICE', 'BedRooms', 'ADDress']
        mapping = self.mapper.map_headers(headers)
        
        self.assertEqual(mapping['PRICE'], 'price')
        self.assertEqual(mapping['BedRooms'], 'bedrooms')
        self.assertEqual(mapping['ADDress'], 'address')
    
    def test_variant_match(self):
        """Test matching header variants."""
        headers = ['Sale_Price', 'num_bedrooms', 'street_address']
        mapping = self.mapper.map_headers(headers)
        
        self.assertEqual(mapping['Sale_Price'], 'price')
        self.assertEqual(mapping['num_bedrooms'], 'bedrooms')
        self.assertEqual(mapping['street_address'], 'address')
    
    def test_fuzzy_match(self):
        """Test fuzzy matching for similar headers."""
        headers = ['sqft', 'bed']
        mapping = self.mapper.map_headers(headers)
        
        # Should match to 'square_feet' and 'bedrooms'
        self.assertEqual(mapping['sqft'], 'square_feet')
        self.assertIn(mapping['bed'], ['bedrooms', 'bed'])
    
    def test_unmapped_headers(self):
        """Test handling of unmapped headers."""
        headers = ['custom_field_xyz', 'unknown_column']
        mapping = self.mapper.map_headers(headers)
        
        # Should return normalized version
        self.assertIsNotNone(mapping['custom_field_xyz'])
        self.assertIsNotNone(mapping['unknown_column'])
    
    def test_mapping_report(self):
        """Test mapping report generation."""
        headers = ['price', 'Sale_Price', 'unknown_field']
        report = self.mapper.get_mapping_report(headers)
        
        self.assertIn('mapped', report)
        self.assertIn('unmapped', report)
        self.assertIsInstance(report['mapped'], list)
        self.assertIsInstance(report['unmapped'], list)
    
    def test_caching(self):
        """Test that mappings are cached."""
        header = 'SALE_PRICE'
        first_mapping = self.mapper.map_header(header)
        
        # Should be in cache now
        self.assertIn(header, self.mapper.mapping_cache)
        
        # Second call should use cache
        second_mapping = self.mapper.map_header(header)
        self.assertEqual(first_mapping, second_mapping)


if __name__ == "__main__":
    unittest.main()
