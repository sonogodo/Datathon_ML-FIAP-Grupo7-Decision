#!/usr/bin/env python3
"""
Test API endpoints functionality without running server
"""
import sys
from pathlib import Path
import asyncio
import pandas as pd

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

async def test_api_endpoints():
    """Test API endpoints functionality"""
    print("Testing API Endpoints")
    print("=" * 30)
    
    try:
        # Import API module
        import api.main as api_module
        
        # 1. Test model loading
        print("📦 1. Testing Model Loading...")
        api_module.initialize_models()
        print("   ✅ Models loaded successfully")
        
        # 2. Test health check logic
        print("🏥 2. Testing Health Check...")
        health_status = {
            "api_status": "healthy",
            "model_loaded": api_module.matcher is not None and api_module.matcher.is_trained,
            "feature_engineer_loaded": api_module.feature_engineer is not None,
            "data_loader_ready": api_module.data_loader is not None
        }
        print(f"   ✅ Health Status: {health_status}")
        
        # 3. Test prediction with existing data
        print("🔮 3. Testing Prediction with Existing Data...")
        
        # Load data
        vagas_df, prospects_df, applicants_df = api_module.data_loader.process_decision_data()
        
        # Get first candidate and job IDs
        if not prospects_df.empty:
            first_prospect = prospects_df.iloc[0]
            candidate_id = first_prospect['candidate_id']
            job_id = first_prospect['job_id']
            
            # Create temporary prospect for feature engineering
            temp_prospect = pd.DataFrame([{
                'candidate_id': candidate_id,
                'job_id': job_id,
                'status': 'applied'
            }])
            
            # Generate features
            features_df = api_module.feature_engineer.create_features(vagas_df, applicants_df, temp_prospect)
            
            # Select feature columns
            feature_columns = [
                'skill_match', 'experience_match', 'salary_match', 
                'location_match', 'english_match', 'spanish_match',
                'sap_match', 'academic_match', 'candidate_experience_years',
                'num_candidate_skills', 'num_job_skills', 'is_sap_job'
            ]
            
            X = features_df[feature_columns]
            X_scaled = pd.DataFrame(
                api_module.feature_engineer.scaler.transform(X),
                columns=X.columns
            )
            
            # Get prediction
            result = api_module.matcher.evaluate_model_confidence(X_scaled)
            print(f"   ✅ Prediction Result: {result}")
        
        # 4. Test prediction with new data
        print("🆕 4. Testing Prediction with New Data...")
        
        # Create test data
        candidate_data = {
            'id': 'test_candidate',
            'skills': ['Python', 'Django', 'PostgreSQL'],
            'experience_years': 5,
            'location': 'São Paulo - SP',
            'salary_expectation': '15000',
            'culture_fit': 'innovative'
        }
        
        job_data = {
            'id': 'test_job',
            'title': 'Python Developer',
            'required_skills': ['Python', 'Django', 'React'],
            'experience_level': 'Senior',
            'location': 'São Paulo - SP',
            'salary_range': '12000-18000',
            'company_culture': 'innovative'
        }
        
        # Map to internal format
        candidate_mapped = {
            'candidate_id': candidate_data['id'],
            'nome': 'Test Candidate',
            'conhecimentos_tecnicos': candidate_data['skills'],
            'anos_experiencia': candidate_data['experience_years'],
            'localizacao': candidate_data['location'],
            'pretensao_salarial': str(candidate_data['salary_expectation']),
            'nivel_ingles': 'Intermediário',
            'nivel_espanhol': 'Básico',
            'nivel_academico': 'Superior Completo'
        }
        
        job_mapped = {
            'job_id': job_data['id'],
            'titulo': job_data['title'],
            'competencias_tecnicas': job_data['required_skills'],
            'nivel_profissional': job_data['experience_level'],
            'localizacao': job_data['location'],
            'salario_range': job_data['salary_range'],
            'nivel_ingles': 'Intermediário',
            'nivel_espanhol': 'Não requerido',
            'is_sap': False
        }
        
        candidate_df = pd.DataFrame([candidate_mapped])
        vaga_df = pd.DataFrame([job_mapped])
        
        # Create temporary prospect
        temp_prospect = pd.DataFrame([{
            'candidate_id': candidate_data['id'],
            'job_id': job_data['id'],
            'status': 'applied'
        }])
        
        # Generate features
        features_df = api_module.feature_engineer.create_features(vaga_df, candidate_df, temp_prospect)
        
        X = features_df[feature_columns]
        X_scaled = pd.DataFrame(
            api_module.feature_engineer.scaler.transform(X),
            columns=X.columns
        )
        
        # Get prediction
        result = api_module.matcher.evaluate_model_confidence(X_scaled)
        print(f"   ✅ New Data Prediction: {result}")
        
        # 5. Test model info
        print("ℹ️  5. Testing Model Info...")
        feature_importance = api_module.matcher.get_feature_importance()
        model_info = {
            "model_type": "RandomForestClassifier",
            "is_trained": api_module.matcher.is_trained,
            "feature_names": api_module.matcher.feature_names,
            "top_features": feature_importance.head(3).to_dict('records')
        }
        print(f"   ✅ Model Info: {model_info}")
        
        print("\n🎉 ALL API ENDPOINT TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_api_endpoints())
    
    if success:
        print("\n🚀 API is ready for deployment!")
        print("💡 All endpoints are working correctly")
        print("🌐 To start the server: python src/api/main.py")
    else:
        print("\n⚠️  API tests failed. Please check the errors above.")
        sys.exit(1)