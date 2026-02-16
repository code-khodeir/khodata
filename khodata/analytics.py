"""Real estate analytics for broker operations and marketing optimization."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta


class RealEstateAnalytics:
    """Analytics engine for real estate broker operations.
    
    Provides metrics and insights for:
    - Property valuation and pricing
    - Lead conversion tracking
    - Marketing campaign performance
    - Broker productivity
    """
    
    def __init__(self):
        """Initialize analytics engine."""
        self.data = {}
    
    def load_properties(self, properties_df: pd.DataFrame) -> None:
        """Load property data.
        
        Args:
            properties_df: DataFrame with property listings
        """
        self.data['properties'] = properties_df
    
    def load_clients(self, clients_df: pd.DataFrame) -> None:
        """Load client/lead data.
        
        Args:
            clients_df: DataFrame with client information
        """
        self.data['clients'] = clients_df
    
    def load_transactions(self, transactions_df: pd.DataFrame) -> None:
        """Load transaction data.
        
        Args:
            transactions_df: DataFrame with transaction records
        """
        self.data['transactions'] = transactions_df
    
    def load_campaigns(self, campaigns_df: pd.DataFrame) -> None:
        """Load marketing campaign data.
        
        Args:
            campaigns_df: DataFrame with campaign performance
        """
        self.data['campaigns'] = campaigns_df
    
    def calculate_property_metrics(self) -> Dict[str, Any]:
        """Calculate property-level metrics.
        
        Returns:
            Dictionary with property metrics
        """
        if 'properties' not in self.data:
            return {"error": "No property data loaded"}
        
        props = self.data['properties']
        
        metrics = {
            "total_listings": len(props),
            "average_price": props['price'].mean() if 'price' in props else None,
            "median_price": props['price'].median() if 'price' in props else None,
            "price_per_sqft_avg": (props['price'] / props['square_feet']).mean() 
                if 'price' in props and 'square_feet' in props else None,
        }
        
        # Price by property type
        if 'property_type' in props and 'price' in props:
            metrics['price_by_type'] = props.groupby('property_type')['price'].mean().to_dict()
        
        # Days on market
        if 'days_on_market' in props:
            metrics['avg_days_on_market'] = props['days_on_market'].mean()
            metrics['median_days_on_market'] = props['days_on_market'].median()
        
        return metrics
    
    def calculate_conversion_metrics(self) -> Dict[str, Any]:
        """Calculate lead conversion metrics.
        
        Returns:
            Dictionary with conversion metrics
        """
        if 'clients' not in self.data:
            return {"error": "No client data loaded"}
        
        clients = self.data['clients']
        
        metrics = {
            "total_leads": len(clients)
        }
        
        # Conversion by status
        if 'lead_status' in clients:
            status_counts = clients['lead_status'].value_counts().to_dict()
            metrics['leads_by_status'] = status_counts
            
            # Calculate conversion rate (assuming 'converted' or 'closed' status)
            converted = clients[clients['lead_status'].isin(['converted', 'closed', 'won'])].shape[0]
            metrics['conversion_rate'] = (converted / len(clients)) * 100 if len(clients) > 0 else 0
        
        # Conversion by source
        if 'lead_source' in clients and 'lead_status' in clients:
            source_conversion = clients.groupby('lead_source').apply(
                lambda x: (x['lead_status'].isin(['converted', 'closed', 'won']).sum() / len(x)) * 100
            ).to_dict()
            metrics['conversion_rate_by_source'] = source_conversion
        
        # Lead score distribution
        if 'lead_score' in clients:
            metrics['avg_lead_score'] = clients['lead_score'].mean()
            metrics['high_quality_leads'] = (clients['lead_score'] >= 70).sum()
        
        return metrics
    
    def calculate_marketing_roi(self) -> Dict[str, Any]:
        """Calculate marketing campaign ROI and performance.
        
        Returns:
            Dictionary with marketing metrics
        """
        if 'campaigns' not in self.data:
            return {"error": "No campaign data loaded"}
        
        campaigns = self.data['campaigns']
        
        metrics = {
            "total_campaigns": len(campaigns),
            "total_spend": campaigns['campaign_cost'].sum() if 'campaign_cost' in campaigns else 0
        }
        
        # Performance metrics
        if 'impressions' in campaigns:
            metrics['total_impressions'] = campaigns['impressions'].sum()
        
        if 'clicks' in campaigns:
            metrics['total_clicks'] = campaigns['clicks'].sum()
            
            if 'impressions' in campaigns:
                metrics['avg_ctr'] = (campaigns['clicks'].sum() / campaigns['impressions'].sum()) * 100
        
        if 'conversions' in campaigns:
            metrics['total_conversions'] = campaigns['conversions'].sum()
            
            if 'campaign_cost' in campaigns:
                total_cost = campaigns['campaign_cost'].sum()
                total_conversions = campaigns['conversions'].sum()
                metrics['cost_per_conversion'] = total_cost / total_conversions if total_conversions > 0 else 0
        
        # ROI calculation
        if 'revenue_generated' in campaigns and 'campaign_cost' in campaigns:
            total_revenue = campaigns['revenue_generated'].sum()
            total_cost = campaigns['campaign_cost'].sum()
            metrics['total_revenue'] = total_revenue
            metrics['roi'] = ((total_revenue - total_cost) / total_cost) * 100 if total_cost > 0 else 0
        
        # Best performing campaigns
        if 'roi' in campaigns:
            top_campaigns = campaigns.nlargest(5, 'roi')[['campaign_name', 'roi']].to_dict('records')
            metrics['top_campaigns'] = top_campaigns
        
        return metrics
    
    def calculate_broker_performance(self, broker_id: Optional[str] = None) -> Dict[str, Any]:
        """Calculate broker performance metrics.
        
        Args:
            broker_id: Optional specific broker to analyze
            
        Returns:
            Dictionary with broker performance metrics
        """
        if 'transactions' not in self.data:
            return {"error": "No transaction data loaded"}
        
        transactions = self.data['transactions']
        
        if broker_id:
            transactions = transactions[transactions['broker_id'] == broker_id]
        
        metrics = {
            "total_transactions": len(transactions),
        }
        
        # Revenue metrics
        if 'sale_price' in transactions:
            metrics['total_sales_volume'] = transactions['sale_price'].sum()
            metrics['avg_sale_price'] = transactions['sale_price'].mean()
        
        if 'commission' in transactions:
            metrics['total_commission'] = transactions['commission'].sum()
            metrics['avg_commission'] = transactions['commission'].mean()
        
        # Time-based metrics
        if 'transaction_date' in transactions:
            transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
            
            # Transactions by month
            transactions['month'] = transactions['transaction_date'].dt.to_period('M')
            monthly_counts = transactions.groupby('month').size().to_dict()
            metrics['transactions_by_month'] = {str(k): v for k, v in monthly_counts.items()}
        
        # Broker rankings (if not filtered)
        if not broker_id and 'broker_id' in transactions:
            broker_performance = transactions.groupby('broker_id').agg({
                'sale_price': 'sum',
                'commission': 'sum'
            }).reset_index()
            broker_performance.columns = ['broker_id', 'total_sales', 'total_commission']
            top_brokers = broker_performance.nlargest(10, 'total_sales').to_dict('records')
            metrics['top_brokers'] = top_brokers
        
        return metrics
    
    def get_insights(self) -> List[str]:
        """Generate actionable insights for broker operations.
        
        Returns:
            List of insight strings
        """
        insights = []
        
        # Property insights
        prop_metrics = self.calculate_property_metrics()
        if 'total_listings' in prop_metrics:
            insights.append(f"Portfolio contains {prop_metrics['total_listings']} active listings")
            
            if prop_metrics.get('avg_days_on_market'):
                dom = prop_metrics['avg_days_on_market']
                if dom > 60:
                    insights.append(f"⚠️ Average days on market ({dom:.0f} days) is high - consider pricing review")
                else:
                    insights.append(f"✓ Properties selling efficiently (avg {dom:.0f} days on market)")
        
        # Conversion insights
        conv_metrics = self.calculate_conversion_metrics()
        if 'conversion_rate' in conv_metrics:
            rate = conv_metrics['conversion_rate']
            insights.append(f"Lead conversion rate: {rate:.1f}%")
            
            if rate < 5:
                insights.append("⚠️ Conversion rate is below industry average - review lead qualification")
            elif rate > 15:
                insights.append("✓ Excellent conversion rate - maintain current processes")
        
        # Marketing insights
        marketing_metrics = self.calculate_marketing_roi()
        if 'roi' in marketing_metrics:
            roi = marketing_metrics['roi']
            insights.append(f"Marketing ROI: {roi:.1f}%")
            
            if roi < 100:
                insights.append("⚠️ Marketing ROI is below breakeven - optimize campaigns")
            else:
                insights.append(f"✓ Positive marketing ROI - generating {roi:.1f}% return")
        
        if 'cost_per_conversion' in marketing_metrics:
            cpc = marketing_metrics['cost_per_conversion']
            insights.append(f"Cost per conversion: ${cpc:.2f}")
        
        return insights
