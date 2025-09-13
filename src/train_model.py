"""
Model training pipeline for Decision AI
"""
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from data.data_loader import DataLoader
from features.feature_engineering import FeatureEngineer
from models.candidate_job_matcher import CandidateJobMatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main training pipeline"""
    logger.info("Starting Decision AI model training pipeline")
    
    try:
        # Initialize components
        data_loader = DataLoader("data/")
        feature_engineer = FeatureEngineer()
        matcher = CandidateJobMatcher()
        
        # Load data
        logger.info("Loading data...")
        vagas_df, prospects_df, applicants_df = data_loader.process_decision_data()
        
        # Check if data exists, create sample if not
        if vagas_df.empty or prospects_df.empty or applicants_df.empty:
            logger.warning("No data found, creating sample data for demonstration")
            data_loader.create_sample_data()
            vagas_df, prospects_df, applicants_df = data_loader.process_decision_data()
        
        # Prepare training data
        logger.info("Engineering features...")
        X, y = feature_engineer.prepare_training_data(vagas_df, applicants_df, prospects_df)
        
        if len(X) == 0:
            logger.error("No training data available")
            return
        
        # Train model
        logger.info("Training model...")
        metrics = matcher.train(X, y)
        
        # Log training results
        logger.info("Training completed successfully!")
        logger.info(f"Model metrics: {metrics}")
        
        # Save model and feature engineer
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        
        matcher.save_model("models/candidate_job_matcher.joblib")
        
        # Save feature engineer (for consistent preprocessing)
        import joblib
        joblib.dump(feature_engineer, "models/feature_engineer.joblib")
        
        logger.info("Model and feature engineer saved successfully")
        
        # Model validation check
        if metrics['roc_auc'] >= 0.7:
            logger.info("✅ Model meets production criteria (AUC >= 0.7)")
        else:
            logger.warning("⚠️  Model AUC below recommended threshold for production")
        
    except Exception as e:
        logger.error(f"Training pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()