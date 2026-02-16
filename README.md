# khodata
Real Estate Data Intelligence and Analytics Platform

## Overview
Khodata is a comprehensive data intelligence platform designed for real estate brokers and professionals. It provides end-to-end capabilities for:

- **Header Mapping**: Automatically standardize inconsistent column names from various data sources
- **Star Schema Data Warehouse**: Dimensional modeling for analytics with fact and dimension tables
- **Data Lake Architecture**: Multi-zone data management (raw, staging, processed, curated)
- **Real Estate Analytics**: Broker operations metrics, conversion tracking, and market insights
- **Machine Learning**: Property valuation, lead scoring, and conversion prediction
- **Marketing Optimization**: Campaign ROI tracking and budget allocation recommendations

## Features

### 1. Header Mapping & Standardization
Map random/inconsistent header names to a structured schema:
```python
from khodata import HeaderMapper

mapper = HeaderMapper()
mapping = mapper.map_headers(['Sale_Price', 'num_beds', 'SqFt'])
# {'Sale_Price': 'price', 'num_beds': 'bedrooms', 'SqFt': 'square_feet'}
```

### 2. Star Schema & Data Warehouse
Generate DDL for dimensional data warehouse:
```python
from khodata import StarSchemaDDL

# Get complete star schema DDL
ddl = StarSchemaDDL.get_all_ddl()

# Get specific tables
fact_tables = StarSchemaDDL.get_fact_tables()
dim_tables = StarSchemaDDL.get_dimension_tables()
```

### 3. Data Lake Management
Organize data across multiple processing zones:
```python
from khodata import DataLake

lake = DataLake(base_path="./data_lake")

# Ingest raw data
path = lake.ingest_raw_data(data, domain="properties", source="mls")

# Promote through zones
staging_path = lake.promote_to_staging(path, cleaned_data)
processed_path = lake.promote_to_processed(staging_path, transformed_data, "enriched")
```

### 4. Real Estate Analytics
Calculate broker operations metrics:
```python
from khodata import RealEstateAnalytics

analytics = RealEstateAnalytics()
analytics.load_properties(properties_df)
analytics.load_clients(clients_df)
analytics.load_campaigns(campaigns_df)

# Get comprehensive metrics
property_metrics = analytics.calculate_property_metrics()
conversion_metrics = analytics.calculate_conversion_metrics()
marketing_roi = analytics.calculate_marketing_roi()

# Get actionable insights
insights = analytics.get_insights()
```

### 5. Machine Learning Models
Predict property values and score leads:
```python
from khodata import PropertyValuationModel, LeadScoringModel

# Property valuation
valuation_model = PropertyValuationModel()
valuation_model.train(properties_df)
predicted_prices = valuation_model.predict(new_properties)

# Lead scoring
lead_model = LeadScoringModel()
lead_model.train(leads_df)
lead_scores = lead_model.predict_score(new_leads)  # 0-100 score
```

### 6. Marketing Optimization
Optimize campaign budget allocation:
```python
from khodata import MarketingOptimizer

# Calculate campaign efficiency
campaigns = MarketingOptimizer.calculate_campaign_efficiency(campaigns_df)

# Get budget recommendations
recommendations = MarketingOptimizer.recommend_budget_allocation(
    campaigns_df, 
    total_budget=50000
)
```

### 7. Complete ETL Pipeline
End-to-end data processing:
```python
from khodata import RealEstateETL

etl = RealEstateETL(data_lake_path="./data_lake")

# Process property data with automatic header mapping
results = etl.process_property_data(raw_properties, source="mls_system")

# Process client/lead data
results = etl.process_client_data(raw_clients, source="crm_system")

# Process marketing campaigns
results = etl.process_campaign_data(raw_campaigns, source="marketing_platform")

# Run comprehensive analytics
analytics_results = etl.run_full_analytics()
```

## Installation

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

## Quick Start

### Run the Comprehensive Demo

```bash
python examples/real_estate_demo.py
```

This demonstrates:
- Header mapping for inconsistent data
- ETL processing through data lake
- Real estate analytics and insights
- ML predictions (valuation & lead scoring)
- Marketing optimization

### Command Line Interface (Original Pilot Feature)

```bash
python -m khodata.cli --example
python -m khodata.cli --file examples/sample_data.json
```

## Use Cases

### For Real Estate Brokers
- **Portfolio Management**: Track all active listings with standardized metrics
- **Lead Conversion**: Monitor and optimize lead-to-client conversion rates
- **Performance Analytics**: Measure broker productivity and sales volume
- **Market Insights**: Analyze pricing trends and days-on-market statistics

### For Marketing Teams
- **Campaign ROI**: Track return on investment for all marketing campaigns
- **Budget Optimization**: Allocate budget to highest-performing channels
- **Lead Quality**: Score and prioritize leads based on conversion probability
- **Conversion Tracking**: Monitor campaign effectiveness from impression to sale

### For Data Teams
- **Data Standardization**: Automatically map inconsistent data sources
- **Data Lake**: Organize raw, staged, and processed data
- **Data Warehouse**: Star schema for efficient analytics queries
- **ML Pipeline**: Train and deploy property valuation and lead scoring models

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Raw Data Sources                          │
│  (MLS Listings, CRM, Marketing Platforms, Spreadsheets)     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Header Mapper (Standardization)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Lake Zones                            │
│  ┌──────┐    ┌─────────┐    ┌───────────┐    ┌─────────┐  │
│  │ Raw  │ -> │ Staging │ -> │ Processed │ -> │ Curated │  │
│  └──────┘    └─────────┘    └───────────┘    └─────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Star Schema Data Warehouse                      │
│  ┌──────────────┐         ┌──────────────────┐             │
│  │ Fact Tables  │ <────── │ Dimension Tables │             │
│  └──────────────┘         └──────────────────┘             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           Analytics & Machine Learning                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │  Analytics   │  │  Valuation   │  │  Lead Scoring    │ │
│  │   Engine     │  │    Model     │  │     Model        │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         Insights & Recommendations (for Brokers)             │
└─────────────────────────────────────────────────────────────┘
```

## Data Schema

### Standard Property Fields
- Property identifiers (property_id, mls_id)
- Location (address, city, state, zip_code)
- Characteristics (bedrooms, bathrooms, square_feet, lot_size, year_built)
- Pricing (price, list_price, sale_price)
- Property type (house, condo, townhouse, etc.)

### Standard Client/Lead Fields
- Client identifiers (client_id, email, phone)
- Lead information (lead_source, lead_status, lead_score)
- Demographics (age_range, income_range)
- Preferences (property_type_interest, budget_range)

### Standard Transaction Fields
- Transaction identifiers (transaction_id, deal_id)
- Dates (transaction_date, close_date)
- Financial (sale_price, commission)
- Parties (broker_id, client_id, property_id)

### Standard Marketing Fields
- Campaign identifiers (campaign_id, campaign_name)
- Costs (campaign_cost, budget)
- Performance (impressions, clicks, conversions)
- Results (revenue_generated, roi)

## Testing

Run the test suite:
```bash
python -m unittest discover tests -v
```

Current test coverage:
- Header mapping and schema standardization
- Real estate analytics calculations
- Data quality checks
- ETL pipeline components

## Performance Benefits

### For Broker Operations
- **Faster Decision Making**: Real-time insights on portfolio performance
- **Increased Conversions**: ML-powered lead scoring prioritizes high-value prospects
- **Reduced Costs**: Optimize marketing spend based on ROI data
- **Better Pricing**: ML valuation models ensure competitive pricing

### Maximum Conversion from Marketing Campaigns
- Track complete funnel: impressions → clicks → leads → conversions
- Identify highest ROI channels for budget allocation
- Score leads to focus on most likely conversions
- A/B test campaigns with detailed performance metrics

## License

Apache License 2.0

## Version

2.0.0 - Full Real Estate Analytics Platform
