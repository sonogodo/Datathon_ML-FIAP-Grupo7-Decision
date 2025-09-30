#!/usr/bin/env python3
"""
Test script to verify API functionality without running the server
"""
import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from models.candidate_job_matcher import CandidateJobMatcher
from features.feature_engineering import FeatureEngineer
from data.data_loader import DataLoader

def test_core_functionality():
    """Test the core ML pipeline functionality"""
    print("Testing Decision AI Core Functionality")
    print("=" * 50)
    
    try:
        # 1. Test Data Loading
        print("📊 1. Testing Data Loading...")
        data_loader = DataLoader("data/")
        vagas_df, prospects_df, applicants_df = data_loader.process_decision_data()
        print(f"   ✅ Loaded: {len(vagas_df)} vagas, {len(applicants_df)} candidates, {len(prospects_df)} prospects")
        
        # 2. Test Feature Engineering
        print("🔧 2. Testing Feature Engineering...")
        feature_engineer = FeatureEngineer()
        features_df = feature_engineer.create_features(vagas_df, applicants_df, prospects_df)
        target = feature_engineer.create_target_variable(features_df)
        print(f"   ✅ Created {len(features_df)} feature rows with {features_df.shape[1]} features")
        
        # 3. Test Model Training
        print("🤖 3. Testing Model Training...")
        X, y = feature_engineer.prepare_training_data(vagas_df, applicants_df, prospects_df)
        
        matcher = CandidateJobMatcher()
        metrics = matcher.train(X, y)
        print(f"   ✅ Model trained - AUC: {metrics['roc_auc']:.3f}")
        
        # 4. Test Prediction
        print("🔮 4. Testing Prediction...")
        result = matcher.evaluate_model_confidence(X.iloc[:1])
        print(f"   ✅ Prediction: Score={result['match_score']:.3f}, Confidence={result['confidence']:.3f}")
        
        # 5. Test Skill Match specifically
        print("🎯 5. Testing Skill Match Algorithm...")
        candidate_skills = ["Python", "Django", "PostgreSQL"]
        job_skills = ["Python", "Django", "React"]
        skill_score = feature_engineer.calculate_skill_match(candidate_skills, job_skills)
        print(f"   ✅ Skill Match: {skill_score:.3f} (Jaccard similarity)")
        
        # 6. Test Model Saving/Loading
        print("💾 6. Testing Model Persistence...")
        matcher.save_model("models/test_model.joblib")
        
        new_matcher = CandidateJobMatcher()
        new_matcher.load_model("models/test_model.joblib")
        print("   ✅ Model saved and loaded successfully")
        
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The Decision AI system is working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_models():
    """Test API model definitions"""
    print("\n📋 Testing API Models...")
    
    try:
        # Import API models
        sys.path.append(str(Path(__file__).parent / "src" / "api"))
        from main import CandidateData, JobData, MatchRequest, MatchResponse
        
        # Test model creation
        candidate = CandidateData(
            id="test_001",
            skills=["Python", "Django"],
            experience_years=5,
            location="São Paulo",
            salary_expectation="15000",
            culture_fit="innovative"
        )
        
        job = JobData(
            id="job_001",
            title="Python Developer",
            required_skills=["Python", "Django"],
            experience_level="Senior",
            location="São Paulo",
            salary_range="12000-18000",
            company_culture="innovative"
        )
        
        request = MatchRequest(candidate_id="test_001", job_id="job_001")
        
        print("   ✅ API models created successfully")
        return True
        
    except Exception as e:
        print(f"   ❌ API model test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_core_functionality()
    api_success = test_api_models()
    
    if success and api_success:
        print("\n🚀 System is ready for deployment!")
        print("💡 To start the API server, run: python src/api/main.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)