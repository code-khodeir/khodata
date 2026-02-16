"""Schema mapper for standardizing data headers and column names."""

from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher
import re


class HeaderMapper:
    """Maps random/inconsistent header names to standardized schema fields.
    
    Uses fuzzy matching and predefined mapping rules to handle variations
    in column naming conventions (e.g., 'Price', 'price', 'PRICE', 'Sale_Price').
    """
    
    # Standard schema for real estate data
    STANDARD_SCHEMA = {
        # Property fields
        "property_id": ["property_id", "prop_id", "id", "listing_id", "mls_id"],
        "address": ["address", "street_address", "location", "street", "addr"],
        "city": ["city", "town", "municipality"],
        "state": ["state", "province", "region"],
        "zip_code": ["zip", "zipcode", "zip_code", "postal_code", "postcode"],
        "property_type": ["type", "property_type", "prop_type", "home_type"],
        "bedrooms": ["bedrooms", "beds", "bed", "num_bedrooms", "bedroom_count"],
        "bathrooms": ["bathrooms", "baths", "bath", "num_bathrooms", "bathroom_count"],
        "square_feet": ["sqft", "square_feet", "sq_ft", "area", "size", "living_area"],
        "lot_size": ["lot_size", "lot_sqft", "land_area", "lot_area"],
        "year_built": ["year_built", "year", "built_year", "construction_year"],
        "price": ["price", "list_price", "asking_price", "sale_price", "value"],
        
        # Client/Lead fields
        "client_id": ["client_id", "lead_id", "contact_id", "customer_id"],
        "client_name": ["name", "client_name", "contact_name", "customer_name", "full_name"],
        "email": ["email", "email_address", "e_mail", "contact_email"],
        "phone": ["phone", "phone_number", "telephone", "mobile", "contact_phone"],
        "lead_source": ["source", "lead_source", "origin", "channel", "referral_source"],
        "lead_status": ["status", "lead_status", "stage", "pipeline_stage"],
        
        # Transaction fields
        "transaction_id": ["transaction_id", "deal_id", "sale_id"],
        "transaction_date": ["date", "sale_date", "transaction_date", "close_date", "closing_date"],
        "transaction_type": ["transaction_type", "sale_type", "deal_type"],
        "commission": ["commission", "commission_amount", "fee"],
        
        # Broker/Agent fields
        "broker_id": ["broker_id", "agent_id", "realtor_id"],
        "broker_name": ["broker", "agent", "realtor", "broker_name", "agent_name"],
        
        # Marketing fields
        "campaign_id": ["campaign_id", "campaign", "marketing_id"],
        "campaign_name": ["campaign_name", "campaign", "promotion"],
        "campaign_cost": ["cost", "campaign_cost", "spend", "budget"],
        "impressions": ["impressions", "views", "reach"],
        "clicks": ["clicks", "click_count"],
        "conversions": ["conversions", "conversion_count", "leads_generated"],
    }
    
    def __init__(self, fuzzy_threshold: float = 0.7):
        """Initialize the header mapper.
        
        Args:
            fuzzy_threshold: Minimum similarity score (0-1) for fuzzy matching
        """
        self.fuzzy_threshold = fuzzy_threshold
        self.mapping_cache: Dict[str, str] = {}
    
    def _normalize_header(self, header: str) -> str:
        """Normalize a header name for comparison.
        
        Args:
            header: Raw header name
            
        Returns:
            Normalized header (lowercase, underscores)
        """
        # Convert to lowercase and replace special chars with underscores
        normalized = re.sub(r'[^a-zA-Z0-9]+', '_', header.lower())
        # Remove leading/trailing underscores
        normalized = normalized.strip('_')
        return normalized
    
    def _fuzzy_match(self, header: str, candidates: List[str]) -> Optional[str]:
        """Find best fuzzy match from candidates.
        
        Args:
            header: Normalized header to match
            candidates: List of candidate standard names
            
        Returns:
            Best matching candidate or None if no good match
        """
        best_score = 0.0
        best_match = None
        
        for candidate in candidates:
            score = SequenceMatcher(None, header, candidate).ratio()
            if score > best_score and score >= self.fuzzy_threshold:
                best_score = score
                best_match = candidate
        
        return best_match
    
    def map_header(self, header: str) -> str:
        """Map a single header to its standard schema field.
        
        Args:
            header: Raw header name
            
        Returns:
            Standard field name or original header if no mapping found
        """
        if header in self.mapping_cache:
            return self.mapping_cache[header]
        
        normalized = self._normalize_header(header)
        
        # Try exact match first
        for standard_field, variants in self.STANDARD_SCHEMA.items():
            if normalized in variants:
                self.mapping_cache[header] = standard_field
                return standard_field
        
        # Try fuzzy match
        for standard_field, variants in self.STANDARD_SCHEMA.items():
            match = self._fuzzy_match(normalized, variants)
            if match:
                self.mapping_cache[header] = standard_field
                return standard_field
        
        # No match found, return normalized version
        self.mapping_cache[header] = normalized
        return normalized
    
    def map_headers(self, headers: List[str]) -> Dict[str, str]:
        """Map multiple headers at once.
        
        Args:
            headers: List of raw header names
            
        Returns:
            Dictionary mapping original headers to standard fields
        """
        return {header: self.map_header(header) for header in headers}
    
    def get_mapping_report(self, headers: List[str]) -> Dict[str, List[Tuple[str, str]]]:
        """Generate a report of header mappings.
        
        Args:
            headers: List of raw headers
            
        Returns:
            Dictionary with 'mapped' and 'unmapped' lists
        """
        mapped = []
        unmapped = []
        
        mapping = self.map_headers(headers)
        
        for original, standard in mapping.items():
            normalized = self._normalize_header(original)
            if standard in self.STANDARD_SCHEMA:
                mapped.append((original, standard))
            else:
                unmapped.append((original, standard))
        
        return {
            "mapped": mapped,
            "unmapped": unmapped
        }
