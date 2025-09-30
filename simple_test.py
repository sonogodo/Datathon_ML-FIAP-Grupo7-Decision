#!/usr/bin/env python3
"""
Simple test without Unicode characters
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_system():
    """Test the complete system"""
    print("DECISION AI - SYSTEM TEST")
    print("=" * 30)
    
    try:
        # Test 1: Data Loading
        print("1. Testing Data Loading...")
        from data.data_loader import DataLoader
        data_loader = DataLoader("data/")
        vagas_df, prospects_df, applicants_df = data_loader.process_decision_data()
        print(f"   SUCCESS: Loaded {len(vagas_df)} vagas, {len(applicants_df)} candidates")
        
        # Test 2: Feature Engineering
        print("2. Testing Feature Engineering...")
        from features.feature_engineering import FeatureEngineer
        feature_engineer = FeatureEngineer()
        features_df = feature_engineer.create_features(vagas_df, applicants_df, prospects_df)
        print(f"   SUCCESS: Created {len(features_df)} feature rows")
        
        # Test 3: Model Training
        print("3. Testing Model...")
        from models.candidate_job_matcher import CandidateJobMatcher
        X, y = feature_engineer.prepare_training_data(vagas_df, applicants_df, prospects_df)
        matcher = CandidateJobMatcher()
        metrics = matcher.train(X, y)
        print(f"   SUCCESS: Model trained - AUC: {metrics['roc_auc']:.3f}")
        
        # Test 4: Prediction
        print("4. Testing Prediction...")
        result = matcher.evaluate_model_confidence(X.iloc[:1])
        print(f"   SUCCESS: Prediction score: {result['match_score']:.3f}")
        
        # Test 5: Skill Match
        print("5. Testing Skill Match...")
        skill_score = feature_engineer.calculate_skill_match(
            ["Python", "Django"], ["Python", "React"]
        )
        print(f"   SUCCESS: Skill match: {skill_score:.3f}")
        
        # Test 6: API Components
        print("6. Testing API Components...")
        import api.main as api_module
        api_module.initialize_models()
        print("   SUCCESS: API components loaded")
        
        print("\nALL TESTS PASSED!")
        print("System is working correctly")
        return True
        
    except Exception as e:
        print(f"TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_system()
    if success:
        print("\nSYSTEM READY FOR DEPLOYMENT!")
    else:
        print("\nSYSTEM HAS ISSUES - CHECK ERRORS ABOVE")
    sys.exit(0 if success else 1)