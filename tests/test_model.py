"""
Tests for candidate job matcher model
"""
import pytest
import pandas as pd
import numpy as np
import tempfile
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from models.candidate_job_matcher import CandidateJobMatcher

class TestCandidateJobMatcher:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.matcher = CandidateJobMatcher()
        
        # Create sample training data
        np.random.seed(42)
        n_samples = 100
        
        self.X_train = pd.DataFrame({
            'skill_match': np.random.uniform(0, 1, n_samples),
            'experience_match': np.random.uniform(0, 1, n_samples),
            'salary_match': np.random.uniform(0, 1, n_samples),
            'location_match': np.random.uniform(0, 1, n_samples),
            'english_match': np.random.uniform(0, 1, n_samples),
            'spanish_match': np.random.uniform(0, 1, n_samples),
            'sap_match': np.random.uniform(0, 1, n_samples),
            'academic_match': np.random.uniform(0, 1, n_samples)
        })
        
        # Create target based on features (higher scores = more likely to be hired)
        feature_sum = self.X_train.sum(axis=1)
        self.y_train = (feature_sum > feature_sum.median()).astype(int)
    
    def test_model_initialization(self):
        """Test model initialization"""
        assert self.matcher.model is not None
        assert not self.matcher.is_trained
        assert self.matcher.feature_names is None
    
    def test_model_training(self):
        """Test model training"""
        metrics = self.matcher.train(self.X_train, self.y_train)
        
        assert self.matcher.is_trained
        assert self.matcher.feature_names == list(self.X_train.columns)
        assert 'train_accuracy' in metrics
        assert 'test_accuracy' in metrics
        assert 'roc_auc' in metrics
        assert 0 <= metrics['roc_auc'] <= 1
    
    def test_prediction_before_training(self):
        """Test prediction before training raises error"""
        with pytest.raises(ValueError, match="Model must be trained"):
            self.matcher.predict(self.X_train)
    
    def test_prediction_after_training(self):
        """Test prediction after training"""
        self.matcher.train(self.X_train, self.y_train)
        
        predictions = self.matcher.predict(self.X_train[:5])
        assert len(predictions) == 5
        assert all(pred in [0, 1] for pred in predictions)
    
    def test_predict_proba(self):
        """Test probability prediction"""
        self.matcher.train(self.X_train, self.y_train)
        
        probabilities = self.matcher.predict_proba(self.X_train[:5])
        assert probabilities.shape == (5, 2)
        assert np.allclose(probabilities.sum(axis=1), 1.0)
    
    def test_get_match_score(self):
        """Test match score calculation"""
        self.matcher.train(self.X_train, self.y_train)
        
        score = self.matcher.get_match_score(self.X_train[:1])
        assert 0 <= score <= 1
    
    def test_feature_importance(self):
        """Test feature importance"""
        self.matcher.train(self.X_train, self.y_train)
        
        importance_df = self.matcher.get_feature_importance()
        assert len(importance_df) == len(self.X_train.columns)
        assert 'feature' in importance_df.columns
        assert 'importance' in importance_df.columns
        assert importance_df['importance'].sum() > 0
    
    def test_model_confidence_evaluation(self):
        """Test model confidence evaluation"""
        self.matcher.train(self.X_train, self.y_train)
        
        result = self.matcher.evaluate_model_confidence(self.X_train[:1])
        
        assert 'match_score' in result
        assert 'confidence' in result
        assert 'recommendation' in result
        assert 'key_factors' in result
        
        assert 0 <= result['match_score'] <= 1
        assert 0 <= result['confidence'] <= 1
        assert result['recommendation'] in ['high_match', 'medium_match', 'low_match']
        assert isinstance(result['key_factors'], list)
    
    def test_save_and_load_model(self):
        """Test model saving and loading"""
        # Train model
        self.matcher.train(self.X_train, self.y_train)
        original_prediction = self.matcher.predict(self.X_train[:1])
        
        # Save model
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / "test_model.joblib"
            self.matcher.save_model(str(model_path))
            
            # Load model in new instance
            new_matcher = CandidateJobMatcher()
            new_matcher.load_model(str(model_path))
            
            # Test loaded model
            assert new_matcher.is_trained
            assert new_matcher.feature_names == self.matcher.feature_names
            
            new_prediction = new_matcher.predict(self.X_train[:1])
            assert np.array_equal(original_prediction, new_prediction)
    
    def test_save_untrained_model_error(self):
        """Test saving untrained model raises error"""
        with pytest.raises(ValueError, match="Cannot save untrained model"):
            self.matcher.save_model("test.joblib")
    
    def test_load_nonexistent_model(self):
        """Test loading nonexistent model raises error"""
        with pytest.raises(FileNotFoundError):
            self.matcher.load_model("nonexistent_model.joblib")