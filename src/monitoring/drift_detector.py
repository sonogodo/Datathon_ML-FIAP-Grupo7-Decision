"""
Model drift detection for Decision AI
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class DriftDetector:
    """Detect data and model drift"""
    
    def __init__(self, reference_data: pd.DataFrame = None):
        self.reference_data = reference_data
        self.drift_threshold = 0.1  # 10% change threshold
        self.monitoring_data = []
        
    def set_reference_data(self, data: pd.DataFrame):
        """Set reference data for drift detection"""
        self.reference_data = data.copy()
        logger.info(f"Reference data set with {len(data)} samples")
    
    def detect_feature_drift(self, current_data: pd.DataFrame) -> Dict[str, float]:
        """Detect drift in feature distributions"""
        if self.reference_data is None:
            logger.warning("No reference data set for drift detection")
            return {}
        
        drift_scores = {}
        
        for column in current_data.columns:
            if column in self.reference_data.columns:
                # Calculate statistical distance (simplified KL divergence)
                ref_mean = self.reference_data[column].mean()
                ref_std = self.reference_data[column].std()
                
                curr_mean = current_data[column].mean()
                curr_std = current_data[column].std()
                
                # Normalized difference
                mean_drift = abs(curr_mean - ref_mean) / (ref_std + 1e-8)
                std_drift = abs(curr_std - ref_std) / (ref_std + 1e-8)
                
                drift_scores[column] = (mean_drift + std_drift) / 2
        
        return drift_scores
    
    def detect_prediction_drift(self, predictions: np.ndarray, 
                              reference_predictions: np.ndarray = None) -> float:
        """Detect drift in model predictions"""
        if reference_predictions is None and hasattr(self, 'reference_predictions'):
            reference_predictions = self.reference_predictions
        elif reference_predictions is None:
            logger.warning("No reference predictions for drift detection")
            return 0.0
        
        # Compare prediction distributions
        ref_mean = np.mean(reference_predictions)
        curr_mean = np.mean(predictions)
        
        ref_std = np.std(reference_predictions)
        curr_std = np.std(predictions)
        
        mean_drift = abs(curr_mean - ref_mean) / (ref_std + 1e-8)
        std_drift = abs(curr_std - ref_std) / (ref_std + 1e-8)
        
        return (mean_drift + std_drift) / 2
    
    def log_monitoring_data(self, features: pd.DataFrame, predictions: np.ndarray,
                           actual_outcomes: np.ndarray = None):
        """Log data for monitoring"""
        timestamp = datetime.now().isoformat()
        
        monitoring_entry = {
            'timestamp': timestamp,
            'n_samples': len(features),
            'feature_stats': {
                col: {
                    'mean': float(features[col].mean()),
                    'std': float(features[col].std()),
                    'min': float(features[col].min()),
                    'max': float(features[col].max())
                }
                for col in features.columns
            },
            'prediction_stats': {
                'mean': float(np.mean(predictions)),
                'std': float(np.std(predictions)),
                'min': float(np.min(predictions)),
                'max': float(np.max(predictions))
            }
        }
        
        if actual_outcomes is not None:
            monitoring_entry['outcome_stats'] = {
                'mean': float(np.mean(actual_outcomes)),
                'accuracy': float(np.mean(predictions.round() == actual_outcomes))
            }
        
        # Detect drift
        feature_drift = self.detect_feature_drift(features)
        monitoring_entry['feature_drift'] = feature_drift
        
        # Check for significant drift
        max_drift = max(feature_drift.values()) if feature_drift else 0
        monitoring_entry['drift_alert'] = max_drift > self.drift_threshold
        
        self.monitoring_data.append(monitoring_entry)
        
        if monitoring_entry['drift_alert']:
            logger.warning(f"Drift detected! Max drift score: {max_drift:.3f}")
        
        return monitoring_entry
    
    def save_monitoring_data(self, filepath: str):
        """Save monitoring data to file"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.monitoring_data, f, indent=2)
        
        logger.info(f"Monitoring data saved to {filepath}")
    
    def load_monitoring_data(self, filepath: str):
        """Load monitoring data from file"""
        try:
            with open(filepath, 'r') as f:
                self.monitoring_data = json.load(f)
            logger.info(f"Monitoring data loaded from {filepath}")
        except FileNotFoundError:
            logger.warning(f"Monitoring file not found: {filepath}")
    
    def get_drift_summary(self) -> Dict:
        """Get summary of drift detection results"""
        if not self.monitoring_data:
            return {"message": "No monitoring data available"}
        
        recent_entry = self.monitoring_data[-1]
        
        summary = {
            'last_check': recent_entry['timestamp'],
            'samples_processed': recent_entry['n_samples'],
            'drift_detected': recent_entry['drift_alert'],
            'feature_drift_scores': recent_entry['feature_drift'],
            'max_drift_score': max(recent_entry['feature_drift'].values()) if recent_entry['feature_drift'] else 0,
            'total_monitoring_entries': len(self.monitoring_data)
        }
        
        return summary