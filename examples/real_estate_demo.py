"""
Comprehensive demo of real estate data analytics platform.

This example demonstrates the complete pipeline:
1. Header mapping for inconsistent data
2. ETL processing through data lake zones
3. Real estate analytics
4. Machine learning predictions
5. Marketing optimization
"""

import pandas as pd
import numpy as np
from khodata import (
    HeaderMapper,
    RealEstateETL,
    RealEstateAnalytics,
    PropertyValuationModel,
    LeadScoringModel,
    MarketingOptimizer
)


def demo_header_mapping():
    """Demonstrate automatic header mapping."""
    print("=" * 70)
    print("1. HEADER MAPPING - Standardizing Inconsistent Column Names")
    print("=" * 70)
    
    # Simulate data from different sources with inconsistent headers
    raw_headers = [
        'PROPERTY_ID', 'Sale Price', 'num_beds', 'BathRooms', 
        'sq_ft', 'Zip Code', 'listing_status'
    ]
    
    mapper = HeaderMapper()
    mapping = mapper.map_headers(raw_headers)
    
    print("\nOriginal Headers → Standard Schema:")
    print("-" * 70)
    for original, standard in mapping.items():
        print(f"  {original:20} → {standard}")
    
    # Get mapping report
    report = mapper.get_mapping_report(raw_headers)
    print(f"\n✓ Successfully mapped {len(report['mapped'])} headers")
    print(f"⚠ {len(report['unmapped'])} headers unmapped")


def demo_etl_pipeline():
    """Demonstrate ETL pipeline with data lake."""
    print("\n" + "=" * 70)
    print("2. ETL PIPELINE - Processing Real Estate Data")
    print("=" * 70)
    
    # Create sample property data with inconsistent headers
    raw_properties = pd.DataFrame([
        {'PropID': 'P001', 'Sale_Price': 285000, 'num_beds': 3, 'baths': 2.5, 
         'SqFt': 1850, 'Year': 2015, 'ZIP': '94102'},
        {'PropID': 'P002', 'Sale_Price': 425000, 'num_beds': 4, 'baths': 3.0,
         'SqFt': 2400, 'Year': 2018, 'ZIP': '94103'},
        {'PropID': 'P003', 'Sale_Price': 195000, 'num_beds': 2, 'baths': 2.0,
         'SqFt': 1200, 'Year': 2010, 'ZIP': '94102'},
    ])
    
    print("\nProcessing property data through pipeline...")
    etl = RealEstateETL(data_lake_path="/tmp/khodata_demo_lake")
    
    results = etl.process_property_data(raw_properties, source="demo_mls")
    
    print(f"\n✓ Raw data ingested: {results['raw_path']}")
    print(f"✓ Data cleaned and staged: {results['staging_path']}")
    print(f"✓ Data transformed and processed: {results['processed_path']}")
    
    print("\nProperty Metrics:")
    print("-" * 70)
    metrics = results['metrics']
    print(f"  Total Listings: {metrics['total_listings']}")
    print(f"  Average Price: ${metrics['average_price']:,.2f}")
    print(f"  Median Price: ${metrics['median_price']:,.2f}")


def demo_real_estate_analytics():
    """Demonstrate real estate analytics."""
    print("\n" + "=" * 70)
    print("3. REAL ESTATE ANALYTICS - Broker Operations Insights")
    print("=" * 70)
    
    analytics = RealEstateAnalytics()
    
    # Sample property data
    properties = pd.DataFrame([
        {'property_id': 1, 'price': 285000, 'square_feet': 1850, 'bedrooms': 3,
         'property_type': 'house', 'days_on_market': 28},
        {'property_id': 2, 'price': 425000, 'square_feet': 2400, 'bedrooms': 4,
         'property_type': 'house', 'days_on_market': 45},
        {'property_id': 3, 'price': 195000, 'square_feet': 1200, 'bedrooms': 2,
         'property_type': 'condo', 'days_on_market': 15},
    ])
    
    # Sample client/lead data
    clients = pd.DataFrame([
        {'client_id': 1, 'lead_status': 'converted', 'lead_source': 'website', 'lead_score': 88},
        {'client_id': 2, 'lead_status': 'active', 'lead_source': 'referral', 'lead_score': 72},
        {'client_id': 3, 'lead_status': 'converted', 'lead_source': 'website', 'lead_score': 92},
        {'client_id': 4, 'lead_status': 'lost', 'lead_source': 'email', 'lead_score': 45},
        {'client_id': 5, 'lead_status': 'active', 'lead_source': 'referral', 'lead_score': 68},
    ])
    
    # Sample campaign data
    campaigns = pd.DataFrame([
        {'campaign_id': 1, 'campaign_name': 'Spring Open House', 'campaign_cost': 5000,
         'impressions': 120000, 'clicks': 6000, 'conversions': 60, 'revenue_generated': 30000},
        {'campaign_id': 2, 'campaign_name': 'Social Media Ads', 'campaign_cost': 3500,
         'impressions': 80000, 'clicks': 4000, 'conversions': 40, 'revenue_generated': 22000},
    ])
    
    analytics.load_properties(properties)
    analytics.load_clients(clients)
    analytics.load_campaigns(campaigns)
    
    # Get insights
    insights = analytics.get_insights()
    print("\nKey Insights:")
    print("-" * 70)
    for i, insight in enumerate(insights, 1):
        print(f"  {i}. {insight}")
    
    # Conversion metrics
    conv_metrics = analytics.calculate_conversion_metrics()
    print(f"\nConversion Rate: {conv_metrics['conversion_rate']:.1f}%")
    
    # Marketing ROI
    roi_metrics = analytics.calculate_marketing_roi()
    print(f"Marketing ROI: {roi_metrics['roi']:.1f}%")
    print(f"Cost per Conversion: ${roi_metrics['cost_per_conversion']:.2f}")


def demo_ml_predictions():
    """Demonstrate machine learning models."""
    print("\n" + "=" * 70)
    print("4. MACHINE LEARNING - Predictive Analytics")
    print("=" * 70)
    
    # Property valuation model
    print("\n4a. Property Valuation Model")
    print("-" * 70)
    
    # Generate sample training data
    np.random.seed(42)
    n_samples = 100
    
    properties = pd.DataFrame({
        'bedrooms': np.random.randint(2, 6, n_samples),
        'bathrooms': np.random.choice([1.5, 2.0, 2.5, 3.0, 3.5], n_samples),
        'square_feet': np.random.randint(1000, 3500, n_samples),
        'lot_size': np.random.randint(3000, 10000, n_samples),
        'year_built': np.random.randint(1990, 2023, n_samples),
    })
    
    # Generate synthetic prices based on features
    properties['price'] = (
        properties['square_feet'] * 150 +
        properties['bedrooms'] * 25000 +
        properties['bathrooms'] * 15000 +
        np.random.normal(0, 20000, n_samples)
    )
    
    valuation_model = PropertyValuationModel()
    metrics = valuation_model.train(properties)
    
    print(f"  Model Training R²: {metrics['train_r2']:.3f}")
    print(f"  Model Test R²: {metrics['test_r2']:.3f}")
    print(f"  Mean Absolute Error: ${metrics['mae']:,.2f}")
    print(f"  Mean Absolute % Error: {metrics['mape']:.2f}%")
    
    # Make prediction on new property
    new_property = pd.DataFrame([{
        'bedrooms': 3, 'bathrooms': 2.5, 'square_feet': 2000,
        'lot_size': 5000, 'year_built': 2020
    }])
    
    predicted_price = valuation_model.predict(new_property)[0]
    print(f"\n  Predicted value for 3bd/2.5ba, 2000 sqft home: ${predicted_price:,.2f}")
    
    # Lead scoring model
    print("\n4b. Lead Scoring Model")
    print("-" * 70)
    
    # Generate sample lead data
    leads = pd.DataFrame({
        'lead_score': np.random.randint(30, 100, n_samples),
        'interaction_count': np.random.randint(1, 15, n_samples),
        'days_since_first_contact': np.random.randint(1, 90, n_samples),
        'lead_source': np.random.choice(['website', 'referral', 'email'], n_samples),
        'property_type_interest': np.random.choice(['house', 'condo', 'townhouse'], n_samples),
        'budget_range': np.random.choice(['200-300k', '300-400k', '400-500k'], n_samples),
        'lead_status': np.random.choice(['converted', 'active', 'lost'], n_samples, p=[0.15, 0.55, 0.3])
    })
    
    lead_model = LeadScoringModel()
    metrics = lead_model.train(leads)
    
    print(f"  Model Accuracy: {metrics['test_accuracy']:.3f}")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall: {metrics['recall']:.3f}")
    print(f"  F1 Score: {metrics['f1_score']:.3f}")
    
    # Score new leads
    new_leads = pd.DataFrame([
        {'lead_score': 85, 'interaction_count': 8, 'days_since_first_contact': 14,
         'lead_source': 'website', 'property_type_interest': 'house', 'budget_range': '300-400k'},
        {'lead_score': 45, 'interaction_count': 2, 'days_since_first_contact': 45,
         'lead_source': 'email', 'property_type_interest': 'condo', 'budget_range': '200-300k'},
    ])
    
    scores = lead_model.predict_score(new_leads)
    print(f"\n  High-quality lead conversion probability: {scores[0]:.1f}%")
    print(f"  Low-quality lead conversion probability: {scores[1]:.1f}%")


def demo_marketing_optimization():
    """Demonstrate marketing optimization."""
    print("\n" + "=" * 70)
    print("5. MARKETING OPTIMIZATION - Campaign Budget Allocation")
    print("=" * 70)
    
    # Historical campaign performance
    campaigns = pd.DataFrame([
        {'campaign_id': 'C1', 'campaign_name': 'Facebook Ads', 'campaign_cost': 5000,
         'conversions': 50, 'revenue_generated': 28000},
        {'campaign_id': 'C2', 'campaign_name': 'Google Ads', 'campaign_cost': 7000,
         'conversions': 80, 'revenue_generated': 45000},
        {'campaign_id': 'C3', 'campaign_name': 'Email Marketing', 'campaign_cost': 2000,
         'conversions': 30, 'revenue_generated': 18000},
        {'campaign_id': 'C4', 'campaign_name': 'Direct Mail', 'campaign_cost': 4000,
         'conversions': 20, 'revenue_generated': 12000},
    ])
    
    # Calculate efficiency
    campaigns_with_metrics = MarketingOptimizer.calculate_campaign_efficiency(campaigns)
    
    print("\nCampaign Performance:")
    print("-" * 70)
    for _, row in campaigns_with_metrics.iterrows():
        print(f"  {row['campaign_name']:20} | ROI: {row['roi']:6.1f}% | "
              f"Cost/Conv: ${row['cost_per_conversion']:6.2f}")
    
    # Recommend budget allocation
    total_budget = 20000
    recommendations = MarketingOptimizer.recommend_budget_allocation(campaigns, total_budget)
    
    print(f"\nRecommended Budget Allocation (Total: ${total_budget:,}):")
    print("-" * 70)
    for campaign, budget in recommendations.items():
        print(f"  {campaign:20} ${budget:8,.2f}")


def main():
    """Run complete demonstration."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "KHODATA REAL ESTATE ANALYTICS PLATFORM" + " " * 20 + "║")
    print("║" + " " * 13 + "Comprehensive Demonstration" + " " * 28 + "║")
    print("╚" + "=" * 68 + "╝")
    
    try:
        demo_header_mapping()
        demo_etl_pipeline()
        demo_real_estate_analytics()
        demo_ml_predictions()
        demo_marketing_optimization()
        
        print("\n" + "=" * 70)
        print("DEMONSTRATION COMPLETE")
        print("=" * 70)
        print("\n✓ All features demonstrated successfully!")
        print("\nKey Capabilities:")
        print("  • Automatic header mapping and standardization")
        print("  • Data lake architecture with ETL pipeline")
        print("  • Real estate analytics and insights")
        print("  • ML models for valuation and lead scoring")
        print("  • Marketing optimization and ROI tracking")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
