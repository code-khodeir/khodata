"""Star schema DDL definitions for real estate data warehouse."""

from typing import Dict, List
from datetime import datetime


class StarSchemaDDL:
    """Generates DDL statements for a star schema data warehouse.
    
    Implements dimensional modeling with fact and dimension tables
    for real estate broker operations and analytics.
    """
    
    @staticmethod
    def get_fact_tables() -> Dict[str, str]:
        """Get DDL for fact tables.
        
        Returns:
            Dictionary of table_name -> DDL statement
        """
        return {
            "fact_property_listing": """
                CREATE TABLE IF NOT EXISTS fact_property_listing (
                    listing_key BIGINT PRIMARY KEY AUTO_INCREMENT,
                    property_key BIGINT NOT NULL,
                    broker_key BIGINT NOT NULL,
                    date_key INT NOT NULL,
                    location_key BIGINT NOT NULL,
                    
                    -- Measures
                    list_price DECIMAL(15, 2),
                    sale_price DECIMAL(15, 2),
                    days_on_market INT,
                    price_per_sqft DECIMAL(10, 2),
                    commission_amount DECIMAL(12, 2),
                    commission_rate DECIMAL(5, 4),
                    
                    -- Degenerate dimensions
                    listing_id VARCHAR(50) UNIQUE,
                    listing_status VARCHAR(20),
                    transaction_type VARCHAR(20),
                    
                    -- Audit fields
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (property_key) REFERENCES dim_property(property_key),
                    FOREIGN KEY (broker_key) REFERENCES dim_broker(broker_key),
                    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
                    FOREIGN KEY (location_key) REFERENCES dim_location(location_key),
                    INDEX idx_date_key (date_key),
                    INDEX idx_broker_key (broker_key),
                    INDEX idx_location_key (location_key)
                );
            """,
            
            "fact_marketing_campaign": """
                CREATE TABLE IF NOT EXISTS fact_marketing_campaign (
                    campaign_key BIGINT PRIMARY KEY AUTO_INCREMENT,
                    campaign_id VARCHAR(50) UNIQUE NOT NULL,
                    broker_key BIGINT NOT NULL,
                    date_key INT NOT NULL,
                    
                    -- Measures
                    campaign_cost DECIMAL(12, 2),
                    impressions INT,
                    clicks INT,
                    leads_generated INT,
                    conversions INT,
                    revenue_generated DECIMAL(15, 2),
                    
                    -- Calculated metrics (can be computed)
                    cost_per_lead DECIMAL(10, 2),
                    cost_per_conversion DECIMAL(10, 2),
                    conversion_rate DECIMAL(5, 4),
                    roi DECIMAL(10, 4),
                    
                    -- Campaign details
                    campaign_name VARCHAR(200),
                    campaign_type VARCHAR(50),
                    channel VARCHAR(50),
                    
                    -- Audit fields
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (broker_key) REFERENCES dim_broker(broker_key),
                    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
                    INDEX idx_date_key (date_key),
                    INDEX idx_broker_key (broker_key)
                );
            """,
            
            "fact_client_interaction": """
                CREATE TABLE IF NOT EXISTS fact_client_interaction (
                    interaction_key BIGINT PRIMARY KEY AUTO_INCREMENT,
                    client_key BIGINT NOT NULL,
                    broker_key BIGINT NOT NULL,
                    date_key INT NOT NULL,
                    property_key BIGINT,
                    
                    -- Measures
                    interaction_duration_minutes INT,
                    follow_up_count INT,
                    
                    -- Degenerate dimensions
                    interaction_id VARCHAR(50) UNIQUE,
                    interaction_type VARCHAR(50),
                    outcome VARCHAR(50),
                    notes TEXT,
                    
                    -- Audit fields
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (client_key) REFERENCES dim_client(client_key),
                    FOREIGN KEY (broker_key) REFERENCES dim_broker(broker_key),
                    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
                    FOREIGN KEY (property_key) REFERENCES dim_property(property_key),
                    INDEX idx_client_key (client_key),
                    INDEX idx_broker_key (broker_key),
                    INDEX idx_date_key (date_key)
                );
            """
        }
    
    @staticmethod
    def get_dimension_tables() -> Dict[str, str]:
        """Get DDL for dimension tables.
        
        Returns:
            Dictionary of table_name -> DDL statement
        """
        return {
            "dim_property": """
                CREATE TABLE IF NOT EXISTS dim_property (
                    property_key BIGINT PRIMARY KEY AUTO_INCREMENT,
                    property_id VARCHAR(50) UNIQUE,
                    
                    -- Property attributes
                    property_type VARCHAR(50),
                    bedrooms INT,
                    bathrooms DECIMAL(3, 1),
                    square_feet INT,
                    lot_size INT,
                    year_built INT,
                    stories INT,
                    garage_spaces INT,
                    
                    -- Features
                    has_pool BOOLEAN DEFAULT FALSE,
                    has_fireplace BOOLEAN DEFAULT FALSE,
                    has_basement BOOLEAN DEFAULT FALSE,
                    
                    -- Property condition
                    condition_rating VARCHAR(20),
                    last_renovation_year INT,
                    
                    -- SCD Type 2 fields
                    effective_date DATE,
                    expiration_date DATE,
                    is_current BOOLEAN DEFAULT TRUE,
                    
                    -- Audit fields
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    INDEX idx_property_id (property_id),
                    INDEX idx_is_current (is_current)
                );
            """,
            
            "dim_location": """
                CREATE TABLE IF NOT EXISTS dim_location (
                    location_key BIGINT PRIMARY KEY AUTO_INCREMENT,
                    
                    -- Address hierarchy
                    address VARCHAR(200),
                    city VARCHAR(100),
                    state VARCHAR(50),
                    zip_code VARCHAR(10),
                    county VARCHAR(100),
                    
                    -- Geographic attributes
                    latitude DECIMAL(10, 8),
                    longitude DECIMAL(11, 8),
                    
                    -- Market attributes
                    market_segment VARCHAR(50),
                    school_district VARCHAR(100),
                    neighborhood VARCHAR(100),
                    walkability_score INT,
                    
                    -- Audit fields
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    INDEX idx_zip_code (zip_code),
                    INDEX idx_city_state (city, state)
                );
            """,
            
            "dim_broker": """
                CREATE TABLE IF NOT EXISTS dim_broker (
                    broker_key BIGINT PRIMARY KEY AUTO_INCREMENT,
                    broker_id VARCHAR(50) UNIQUE,
                    
                    -- Broker details
                    broker_name VARCHAR(200),
                    email VARCHAR(200),
                    phone VARCHAR(20),
                    license_number VARCHAR(50),
                    
                    -- Organization
                    brokerage_name VARCHAR(200),
                    team_name VARCHAR(100),
                    
                    -- Performance tier
                    performance_tier VARCHAR(20),
                    specialization VARCHAR(100),
                    
                    -- Status
                    is_active BOOLEAN DEFAULT TRUE,
                    
                    -- Audit fields
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    INDEX idx_broker_id (broker_id),
                    INDEX idx_is_active (is_active)
                );
            """,
            
            "dim_client": """
                CREATE TABLE IF NOT EXISTS dim_client (
                    client_key BIGINT PRIMARY KEY AUTO_INCREMENT,
                    client_id VARCHAR(50) UNIQUE,
                    
                    -- Client details
                    client_name VARCHAR(200),
                    email VARCHAR(200),
                    phone VARCHAR(20),
                    
                    -- Demographics
                    client_type VARCHAR(50), -- buyer, seller, investor, etc.
                    age_range VARCHAR(20),
                    income_range VARCHAR(30),
                    
                    -- Lead information
                    lead_source VARCHAR(100),
                    lead_score INT,
                    lead_status VARCHAR(50),
                    
                    -- Preferences
                    preferred_contact_method VARCHAR(20),
                    property_type_interest VARCHAR(50),
                    budget_range VARCHAR(30),
                    
                    -- SCD Type 2 fields
                    effective_date DATE,
                    expiration_date DATE,
                    is_current BOOLEAN DEFAULT TRUE,
                    
                    -- Audit fields
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    INDEX idx_client_id (client_id),
                    INDEX idx_lead_status (lead_status),
                    INDEX idx_is_current (is_current)
                );
            """,
            
            "dim_date": """
                CREATE TABLE IF NOT EXISTS dim_date (
                    date_key INT PRIMARY KEY,
                    date_value DATE UNIQUE NOT NULL,
                    
                    -- Date components
                    year INT,
                    quarter INT,
                    month INT,
                    month_name VARCHAR(20),
                    week INT,
                    day_of_month INT,
                    day_of_week INT,
                    day_name VARCHAR(20),
                    
                    -- Flags
                    is_weekend BOOLEAN,
                    is_holiday BOOLEAN,
                    holiday_name VARCHAR(100),
                    
                    -- Business attributes
                    fiscal_year INT,
                    fiscal_quarter INT,
                    is_business_day BOOLEAN,
                    
                    INDEX idx_date_value (date_value),
                    INDEX idx_year_month (year, month)
                );
            """
        }
    
    @staticmethod
    def get_all_ddl() -> str:
        """Get complete DDL for star schema.
        
        Returns:
            Complete DDL as a single string
        """
        ddl_parts = []
        
        # Add dimension tables first (due to foreign keys)
        dimensions = StarSchemaDDL.get_dimension_tables()
        ddl_parts.append("-- Dimension Tables")
        for table_name, ddl in dimensions.items():
            ddl_parts.append(f"\n-- {table_name}")
            ddl_parts.append(ddl.strip())
        
        # Add fact tables
        facts = StarSchemaDDL.get_fact_tables()
        ddl_parts.append("\n\n-- Fact Tables")
        for table_name, ddl in facts.items():
            ddl_parts.append(f"\n-- {table_name}")
            ddl_parts.append(ddl.strip())
        
        return "\n".join(ddl_parts)
    
    @staticmethod
    def generate_date_dimension(start_year: int = 2020, end_year: int = 2030) -> List[Dict]:
        """Generate date dimension data.
        
        Args:
            start_year: Start year for date dimension
            end_year: End year for date dimension
            
        Returns:
            List of date dimension records
        """
        from datetime import date, timedelta
        
        dates = []
        current_date = date(start_year, 1, 1)
        end_date = date(end_year, 12, 31)
        
        while current_date <= end_date:
            date_key = int(current_date.strftime('%Y%m%d'))
            
            dates.append({
                'date_key': date_key,
                'date_value': current_date,
                'year': current_date.year,
                'quarter': (current_date.month - 1) // 3 + 1,
                'month': current_date.month,
                'month_name': current_date.strftime('%B'),
                'week': current_date.isocalendar()[1],
                'day_of_month': current_date.day,
                'day_of_week': current_date.isoweekday(),
                'day_name': current_date.strftime('%A'),
                'is_weekend': current_date.isoweekday() in [6, 7],
                'is_business_day': current_date.isoweekday() not in [6, 7],
                'fiscal_year': current_date.year if current_date.month <= 6 else current_date.year + 1,
                'fiscal_quarter': ((current_date.month + 6) % 12) // 3 + 1,
            })
            
            current_date += timedelta(days=1)
        
        return dates
