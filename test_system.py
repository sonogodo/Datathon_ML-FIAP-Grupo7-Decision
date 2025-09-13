"""
Script para testar o sistema Decision AI
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from data.data_loader import DataLoader
from features.feature_engineering import FeatureEngineer
from models.candidate_job_matcher import CandidateJobMatcher
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_system():
    """Test the complete system"""
    logger.info("🚀 Testando o sistema Decision AI")
    
    # Initialize components
    data_loader = DataLoader("data/")
    feature_engineer = FeatureEngineer()
    matcher = CandidateJobMatcher()
    
    # Create sample data if needed
    logger.info("📊 Criando dados de exemplo...")
    data_loader.create_sample_data()
    
    # Load and process data
    logger.info("📥 Carregando dados...")
    vagas_df, prospects_df, applicants_df = data_loader.process_decision_data()
    
    logger.info(f"✅ Dados carregados:")
    logger.info(f"   - Vagas: {len(vagas_df)}")
    logger.info(f"   - Prospects: {len(prospects_df)}")
    logger.info(f"   - Applicants: {len(applicants_df)}")
    
    # Prepare training data
    logger.info("🔧 Preparando features...")
    X, y = feature_engineer.prepare_training_data(vagas_df, applicants_df, prospects_df)
    
    if len(X) == 0:
        logger.error("❌ Nenhum dado de treinamento disponível")
        return
    
    logger.info(f"✅ Features preparadas: {X.shape}")
    logger.info(f"   - Features: {list(X.columns)}")
    logger.info(f"   - Target distribution: {y.value_counts().to_dict()}")
    
    # Train model
    logger.info("🤖 Treinando modelo...")
    metrics = matcher.train(X, y)
    
    logger.info("✅ Modelo treinado com sucesso!")
    logger.info(f"   - Métricas: {metrics}")
    
    # Test prediction
    logger.info("🔮 Testando predição...")
    sample_X = X.iloc[:1]  # First sample
    prediction = matcher.evaluate_model_confidence(sample_X)
    
    logger.info(f"✅ Predição de exemplo: {prediction}")
    
    logger.info("🎉 Sistema testado com sucesso!")
    
    return True

if __name__ == "__main__":
    test_system()