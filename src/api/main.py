"""
FastAPI application for Decision AI candidate-job matching
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import logging
from pathlib import Path
import sys
from typing import Dict, List, Optional

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from models.candidate_job_matcher import CandidateJobMatcher
from features.feature_engineering import FeatureEngineer
from data.data_loader import DataLoader
from monitoring.drift_detector import DriftDetector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Decision AI - Candidate Job Matching API",
    description="AI-powered candidate-job matching system for Decision HR",
    version="1.0.0"
)

# Global variables for loaded models
matcher: Optional[CandidateJobMatcher] = None
feature_engineer: Optional[FeatureEngineer] = None
data_loader: Optional[DataLoader] = None
drift_detector: Optional[DriftDetector] = None

# Pydantic models for API
class CandidateData(BaseModel):
    id: str
    skills: List[str]
    experience_years: int
    location: str
    salary_expectation: str
    culture_fit: str

class JobData(BaseModel):
    id: str
    title: str
    required_skills: List[str]
    experience_level: str
    location: str
    salary_range: str
    company_culture: str

class MatchRequest(BaseModel):
    candidate_id: str
    job_id: str

class MatchRequestWithData(BaseModel):
    candidate: CandidateData
    job: JobData

class MatchResponse(BaseModel):
    match_score: float
    confidence: float
    recommendation: str
    key_factors: List[str]

@app.on_event("startup")
async def load_models():
    """Load trained models on startup"""
    global matcher, feature_engineer, data_loader, drift_detector
    
    try:
        # Load models
        matcher = CandidateJobMatcher()
        matcher.load_model("models/candidate_job_matcher.joblib")
        
        feature_engineer = joblib.load("models/feature_engineer.joblib")
        data_loader = DataLoader("data/")
        drift_detector = DriftDetector()
        
        # Load monitoring data if exists
        drift_detector.load_monitoring_data("models/monitoring_data.json")
        
        logger.info("Models loaded successfully")
        
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        # Initialize with defaults for development
        matcher = CandidateJobMatcher()
        feature_engineer = FeatureEngineer()
        data_loader = DataLoader("data/")
        drift_detector = DriftDetector()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Decision AI - Candidate Job Matching API",
        "status": "healthy",
        "model_loaded": matcher is not None and matcher.is_trained
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "api_status": "healthy",
        "model_loaded": matcher is not None and matcher.is_trained,
        "feature_engineer_loaded": feature_engineer is not None,
        "data_loader_ready": data_loader is not None
    }

@app.post("/predict", response_model=MatchResponse)
async def predict_match(request: MatchRequest):
    """Predict candidate-job match using existing data"""
    if not matcher or not matcher.is_trained:
        raise HTTPException(status_code=503, detail="Model not loaded or trained")
    
    try:
        # Load existing data
        vagas_df, prospects_df, applicants_df = data_loader.process_decision_data()
        
        # Find candidate and job
        candidate_data = applicants_df[applicants_df['candidate_id'] == request.candidate_id]
        vaga_data = vagas_df[vagas_df['job_id'] == request.job_id]
        
        if candidate_data.empty:
            raise HTTPException(status_code=404, detail=f"Candidate {request.candidate_id} not found")
        if vaga_data.empty:
            raise HTTPException(status_code=404, detail=f"Job {request.job_id} not found")
        
        # Create temporary prospect for feature engineering
        temp_prospect = pd.DataFrame([{
            'candidate_id': request.candidate_id,
            'job_id': request.job_id,
            'status': 'applied'
        }])
        
        # Generate features
        features_df = feature_engineer.create_features(vagas_df, applicants_df, temp_prospect)
        
        # Select feature columns (updated for Decision data)
        feature_columns = [
            'skill_match', 'experience_match', 'salary_match', 
            'location_match', 'english_match', 'spanish_match',
            'sap_match', 'academic_match', 'candidate_experience_years',
            'num_candidate_skills', 'num_job_skills', 'is_sap_job'
        ]
        
        X = features_df[feature_columns]
        X_scaled = pd.DataFrame(
            feature_engineer.scaler.transform(X),
            columns=X.columns
        )
        
        # Get prediction
        result = matcher.evaluate_model_confidence(X_scaled)
        
        return MatchResponse(**result)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict_with_data", response_model=MatchResponse)
async def predict_match_with_data(request: MatchRequestWithData):
    """Predict candidate-job match with provided data"""
    if not matcher or not matcher.is_trained:
        raise HTTPException(status_code=503, detail="Model not loaded or trained")
    
    try:
        # Convert request data to DataFrames with proper column mapping
        candidate_data = request.candidate.model_dump()
        job_data = request.job.model_dump()
        
        # Map API fields to internal fields
        candidate_mapped = {
            'candidate_id': candidate_data['id'],
            'nome': candidate_data.get('name', 'Unknown'),
            'conhecimentos_tecnicos': candidate_data.get('skills', []),
            'anos_experiencia': candidate_data.get('experience_years', 0),
            'localizacao': candidate_data.get('location', ''),
            'pretensao_salarial': str(candidate_data.get('salary_expectation', '0')),
            'nivel_ingles': candidate_data.get('english_level', 'Intermediário'),
            'nivel_espanhol': candidate_data.get('spanish_level', 'Básico'),
            'nivel_academico': candidate_data.get('academic_level', 'Superior Completo')
        }
        
        job_mapped = {
            'job_id': job_data['id'],
            'titulo': job_data.get('title', 'Unknown'),
            'competencias_tecnicas': job_data.get('required_skills', []),
            'nivel_profissional': job_data.get('experience_level', 'Pleno'),
            'localizacao': job_data.get('location', ''),
            'salario_range': job_data.get('salary_range', '0-0'),
            'nivel_ingles': job_data.get('english_requirement', 'Intermediário'),
            'nivel_espanhol': job_data.get('spanish_requirement', 'Não requerido'),
            'is_sap': job_data.get('is_sap', False)
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
        features_df = feature_engineer.create_features(vaga_df, candidate_df, temp_prospect)
        
        # Select feature columns (updated for Decision data)
        feature_columns = [
            'skill_match', 'experience_match', 'salary_match', 
            'location_match', 'english_match', 'spanish_match',
            'sap_match', 'academic_match', 'candidate_experience_years',
            'num_candidate_skills', 'num_job_skills', 'is_sap_job'
        ]
        
        X = features_df[feature_columns]
        X_scaled = pd.DataFrame(
            feature_engineer.scaler.transform(X),
            columns=X.columns
        )
        
        # Get prediction
        result = matcher.evaluate_model_confidence(X_scaled)
        
        return MatchResponse(**result)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/model/info")
async def get_model_info():
    """Get model information and feature importance"""
    if not matcher or not matcher.is_trained:
        raise HTTPException(status_code=503, detail="Model not loaded or trained")
    
    try:
        feature_importance = matcher.get_feature_importance()
        
        return {
            "model_type": "RandomForestClassifier",
            "is_trained": matcher.is_trained,
            "feature_names": matcher.feature_names,
            "feature_importance": feature_importance.to_dict('records')
        }
        
    except Exception as e:
        logger.error(f"Model info error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")

@app.get("/monitoring/drift")
async def get_drift_status():
    """Get model drift monitoring status"""
    if not drift_detector:
        raise HTTPException(status_code=503, detail="Drift detector not initialized")
    
    try:
        drift_summary = drift_detector.get_drift_summary()
        return drift_summary
        
    except Exception as e:
        logger.error(f"Drift monitoring error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get drift status: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)