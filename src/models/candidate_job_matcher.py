"""
Candidate-Job Matching Model
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve
import joblib
import logging
from pathlib import Path
from typing import Dict, Tuple, Any

logger = logging.getLogger(__name__)

class CandidateJobMatcher:
    """Machine Learning model for candidate-job matching"""
    
    def __init__(self, model_params: Dict = None):
        """Initialize the matcher with model parameters"""
        default_params = {
            'n_estimators': 100,
            'max_depth': 10,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': 42,
            'class_weight': 'balanced'
        }
        
        if model_params:
            default_params.update(model_params)
            
        self.model = RandomForestClassifier(**default_params)
        self.feature_names = None
        self.is_trained = False
        
    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Train the matching model"""
        logger.info("Starting model training...")
        
        # Store feature names
        self.feature_names = list(X.columns)
        
        # Split data for validation (adjust for small datasets)
        if len(X) < 10:
            # For very small datasets, use all data for training and testing
            X_train, X_test, y_train, y_test = X, X, y, y
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        # Cross-validation (adjust cv based on sample size and class distribution)
        unique_classes = np.unique(y)
        min_class_count = min([np.sum(y == cls) for cls in unique_classes])
        cv_folds = min(3, min_class_count, len(X))
        
        if cv_folds < 2 or len(X) < 6:
            cv_scores = np.array([test_score])  # Use test score if too few samples
            logger.warning("Dataset too small for cross-validation, using test score")
        else:
            try:
                cv_scores = cross_val_score(self.model, X, y, cv=cv_folds, scoring='roc_auc')
            except ValueError as e:
                logger.warning(f"Cross-validation failed: {e}, using test score")
                cv_scores = np.array([test_score])
        
        # Predictions for detailed metrics
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        metrics = {
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'cv_mean_auc': cv_scores.mean(),
            'cv_std_auc': cv_scores.std(),
            'roc_auc': roc_auc
        }
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        logger.info(f"Model training completed. Test AUC: {roc_auc:.3f}")
        logger.info("Top 3 most important features:")
        for _, row in feature_importance.head(3).iterrows():
            logger.info(f"  {row['feature']}: {row['importance']:.3f}")
        
        # Classification report
        logger.info("Classification Report:")
        logger.info(f"\n{classification_report(y_test, y_pred)}")
        
        self.is_trained = True
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions on new data"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
            
        return self.model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Get prediction probabilities"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
            
        return self.model.predict_proba(X)
    
    def get_match_score(self, X: pd.DataFrame) -> float:
        """Get match score (probability of positive class)"""
        probabilities = self.predict_proba(X)
        return probabilities[0, 1] if len(probabilities) > 0 else 0.0
    
    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance rankings"""
        if not self.is_trained:
            raise ValueError("Model must be trained first")
            
        return pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
            
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        try:
            model_data = joblib.load(filepath)
            self.model = model_data['model']
            self.feature_names = model_data['feature_names']
            self.is_trained = model_data['is_trained']
            logger.info(f"Model loaded from {filepath}")
        except FileNotFoundError:
            logger.error(f"Model file not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def evaluate_model_confidence(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Evaluate model confidence and provide interpretation"""
        if not self.is_trained:
            raise ValueError("Model must be trained first")
            
        probabilities = self.predict_proba(X)
        match_score = probabilities[0, 1]
        
        # Confidence based on how far the probability is from 0.5
        confidence = abs(match_score - 0.5) * 2
        
        # Recommendation based on score and confidence
        if match_score >= 0.7 and confidence >= 0.4:
            recommendation = "high_match"
        elif match_score >= 0.5 and confidence >= 0.2:
            recommendation = "medium_match"
        else:
            recommendation = "low_match"
        
        # Get top contributing features
        feature_importance = self.get_feature_importance()
        key_factors = feature_importance.head(3)['feature'].tolist()
        
        return {
            'match_score': float(match_score),
            'confidence': float(confidence),
            'recommendation': recommendation,
            'key_factors': key_factors
        }