"""Machine learning models for real estate predictions and lead scoring."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split


class PropertyValuationModel:
    """ML model for property price prediction.
    
    Uses property features (bedrooms, bathrooms, sqft, location)
    to predict market value.
    """
    
    def __init__(self):
        """Initialize the valuation model."""
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'bedrooms', 'bathrooms', 'square_feet', 
            'lot_size', 'year_built'
        ]
        self.is_trained = False
    
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare features for model.
        
        Args:
            df: DataFrame with property data
            
        Returns:
            Feature array
        """
        # Select and fill missing values
        features = df[self.feature_columns].copy()
        features = features.fillna(features.median())
        
        return features.values
    
    def train(self, properties_df: pd.DataFrame, target_col: str = 'price') -> Dict[str, float]:
        """Train the valuation model.
        
        Args:
            properties_df: DataFrame with property data and prices
            target_col: Name of target price column
            
        Returns:
            Dictionary with training metrics
        """
        # Prepare data
        X = self.prepare_features(properties_df)
        y = properties_df[target_col].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Simple linear regression model (can be replaced with more complex models)
        from sklearn.linear_model import LinearRegression
        self.model = LinearRegression()
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        # Calculate metrics
        y_pred = self.model.predict(X_test_scaled)
        mae = np.mean(np.abs(y_test - y_pred))
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        self.is_trained = True
        
        return {
            'train_r2': train_score,
            'test_r2': test_score,
            'mae': mae,
            'mape': mape
        }
    
    def predict(self, properties_df: pd.DataFrame) -> np.ndarray:
        """Predict property values.
        
        Args:
            properties_df: DataFrame with property features
            
        Returns:
            Array of predicted prices
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        X = self.prepare_features(properties_df)
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance/coefficients.
        
        Returns:
            Dictionary mapping features to importance
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        return dict(zip(self.feature_columns, self.model.coef_))


class LeadScoringModel:
    """ML model for lead scoring and conversion prediction.
    
    Predicts likelihood of lead conversion based on:
    - Demographics
    - Engagement history
    - Property preferences
    - Lead source
    """
    
    def __init__(self):
        """Initialize the lead scoring model."""
        self.model = None
        self.scaler = StandardScaler()
        self.encoders = {}
        self.feature_columns = []
        self.is_trained = False
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, List[str]]:
        """Prepare features for lead scoring.
        
        Args:
            df: DataFrame with lead data
            
        Returns:
            Tuple of (feature array, feature names)
        """
        features_df = df.copy()
        
        # Numeric features
        numeric_features = ['lead_score', 'interaction_count', 'days_since_first_contact']
        for feat in numeric_features:
            if feat not in features_df.columns:
                features_df[feat] = 0
        
        # Categorical features (encode)
        categorical_features = ['lead_source', 'property_type_interest', 'budget_range']
        for feat in categorical_features:
            if feat in features_df.columns:
                if feat not in self.encoders:
                    self.encoders[feat] = LabelEncoder()
                    features_df[f'{feat}_encoded'] = self.encoders[feat].fit_transform(
                        features_df[feat].fillna('unknown')
                    )
                else:
                    # Handle new categories
                    known_classes = set(self.encoders[feat].classes_)
                    features_df[feat] = features_df[feat].fillna('unknown')
                    features_df[feat] = features_df[feat].apply(
                        lambda x: x if x in known_classes else 'unknown'
                    )
                    features_df[f'{feat}_encoded'] = self.encoders[feat].transform(features_df[feat])
        
        # Select final features
        feature_cols = [col for col in features_df.columns if col.endswith('_encoded')] + numeric_features
        feature_cols = [col for col in feature_cols if col in features_df.columns]
        
        return features_df[feature_cols].fillna(0).values, feature_cols
    
    def train(self, leads_df: pd.DataFrame, target_col: str = 'converted') -> Dict[str, float]:
        """Train the lead scoring model.
        
        Args:
            leads_df: DataFrame with lead data
            target_col: Name of conversion target column (binary)
            
        Returns:
            Dictionary with training metrics
        """
        # Prepare data
        X, feature_names = self.prepare_features(leads_df)
        self.feature_columns = feature_names
        
        # Create binary target if needed
        if target_col in leads_df.columns:
            y = leads_df[target_col].values
        else:
            # Assume 'lead_status' contains conversion info
            y = leads_df['lead_status'].isin(['converted', 'closed', 'won']).astype(int).values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Logistic regression model
        from sklearn.linear_model import LogisticRegression
        self.model = LogisticRegression(random_state=42, max_iter=1000)
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        # Predictions for additional metrics
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        y_pred = self.model.predict(X_test_scaled)
        
        # Calculate precision, recall, f1
        from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
        
        self.is_trained = True
        
        return {
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1_score': f1_score(y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 0
        }
    
    def predict_score(self, leads_df: pd.DataFrame) -> np.ndarray:
        """Predict lead scores (conversion probability 0-100).
        
        Args:
            leads_df: DataFrame with lead features
            
        Returns:
            Array of lead scores (0-100)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        X, _ = self.prepare_features(leads_df)
        X_scaled = self.scaler.transform(X)
        
        # Get probability of conversion
        proba = self.model.predict_proba(X_scaled)[:, 1]
        
        # Convert to 0-100 scale
        return proba * 100
    
    def predict_conversion(self, leads_df: pd.DataFrame) -> np.ndarray:
        """Predict binary conversion outcome.
        
        Args:
            leads_df: DataFrame with lead features
            
        Returns:
            Array of binary predictions (0 or 1)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        X, _ = self.prepare_features(leads_df)
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)


class MarketingOptimizer:
    """Optimizer for marketing campaign allocation and targeting."""
    
    @staticmethod
    def calculate_campaign_efficiency(campaigns_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate efficiency metrics for campaigns.
        
        Args:
            campaigns_df: DataFrame with campaign data
            
        Returns:
            DataFrame with efficiency scores
        """
        result = campaigns_df.copy()
        
        # Calculate efficiency metrics
        if 'conversions' in result.columns and 'campaign_cost' in result.columns:
            result['cost_per_conversion'] = result['campaign_cost'] / result['conversions'].replace(0, 1)
            result['efficiency_score'] = 1 / result['cost_per_conversion']
        
        if 'revenue_generated' in result.columns and 'campaign_cost' in result.columns:
            result['roi'] = ((result['revenue_generated'] - result['campaign_cost']) / 
                           result['campaign_cost'].replace(0, 1)) * 100
        
        return result
    
    @staticmethod
    def recommend_budget_allocation(
        campaigns_df: pd.DataFrame,
        total_budget: float
    ) -> Dict[str, float]:
        """Recommend optimal budget allocation across campaigns.
        
        Args:
            campaigns_df: DataFrame with historical campaign performance
            total_budget: Total budget to allocate
            
        Returns:
            Dictionary mapping campaign to recommended budget
        """
        if 'roi' not in campaigns_df.columns:
            campaigns_df = MarketingOptimizer.calculate_campaign_efficiency(campaigns_df)
        
        # Weight by ROI
        campaigns_df['weight'] = campaigns_df['roi'].clip(lower=0)
        total_weight = campaigns_df['weight'].sum()
        
        if total_weight == 0:
            # Equal allocation if no ROI data
            campaigns_df['weight'] = 1
            total_weight = len(campaigns_df)
        
        # Allocate proportionally
        recommendations = {}
        for _, row in campaigns_df.iterrows():
            campaign_id = row['campaign_id'] if 'campaign_id' in row else row['campaign_name']
            allocation = (row['weight'] / total_weight) * total_budget
            recommendations[campaign_id] = round(allocation, 2)
        
        return recommendations
    
    @staticmethod
    def identify_high_value_segments(
        clients_df: pd.DataFrame,
        n_segments: int = 5
    ) -> List[Dict[str, Any]]:
        """Identify high-value client segments for targeted campaigns.
        
        Args:
            clients_df: DataFrame with client data
            n_segments: Number of segments to identify
            
        Returns:
            List of segment definitions
        """
        segments = []
        
        # Segment by budget range and lead score
        if 'budget_range' in clients_df.columns and 'lead_score' in clients_df.columns:
            segment_analysis = clients_df.groupby('budget_range').agg({
                'lead_score': 'mean',
                'client_id': 'count'
            }).reset_index()
            segment_analysis.columns = ['budget_range', 'avg_lead_score', 'count']
            
            top_segments = segment_analysis.nlargest(n_segments, 'avg_lead_score')
            
            for _, row in top_segments.iterrows():
                segments.append({
                    'segment_name': f"High-value: {row['budget_range']}",
                    'budget_range': row['budget_range'],
                    'avg_lead_score': row['avg_lead_score'],
                    'size': row['count']
                })
        
        return segments
