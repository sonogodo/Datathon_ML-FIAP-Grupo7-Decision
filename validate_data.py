"""
Script para validar os dados da Decision após upload
"""
import sys
import json
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from data.data_loader import DataLoader
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_decision_data():
    """Validate Decision data structure and content"""
    logger.info("🔍 Validando dados da Decision...")
    
    data_loader = DataLoader("data/")
    
    # Check if files exist
    required_files = ["vagas.json", "prospects.json", "applicants.json"]
    missing_files = []
    
    for file in required_files:
        if not (Path("data") / file).exists():
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"❌ Arquivos não encontrados: {missing_files}")
        logger.info("💡 Para testar o sistema, execute: python test_system.py")
        return False
    
    # Load raw data
    logger.info("📥 Carregando arquivos JSON...")
    vagas_data = data_loader.load_json_data("vagas.json")
    prospects_data = data_loader.load_json_data("prospects.json")
    applicants_data = data_loader.load_json_data("applicants.json")
    
    # Validate structure
    logger.info("🔍 Validando estrutura dos dados...")
    
    # Vagas validation
    if isinstance(vagas_data, dict):
        logger.info(f"✅ Vagas: {len(vagas_data)} vagas encontradas")
        sample_vaga = next(iter(vagas_data.values()))
        logger.info(f"   - Campos de exemplo: {list(sample_vaga.keys())}")
    else:
        logger.warning("⚠️  Vagas: formato inesperado (esperado: dict)")
    
    # Prospects validation
    if isinstance(prospects_data, dict):
        total_prospects = sum(len(candidates) for candidates in prospects_data.values())
        logger.info(f"✅ Prospects: {total_prospects} prospecções em {len(prospects_data)} vagas")
        
        # Sample prospect
        sample_vaga = next(iter(prospects_data.keys()))
        sample_prospect = prospects_data[sample_vaga][0] if prospects_data[sample_vaga] else {}
        logger.info(f"   - Campos de exemplo: {list(sample_prospect.keys())}")
    else:
        logger.warning("⚠️  Prospects: formato inesperado (esperado: dict)")
    
    # Applicants validation
    if isinstance(applicants_data, dict):
        logger.info(f"✅ Applicants: {len(applicants_data)} candidatos encontrados")
        sample_applicant = next(iter(applicants_data.values()))
        logger.info(f"   - Campos de exemplo: {list(sample_applicant.keys())}")
    else:
        logger.warning("⚠️  Applicants: formato inesperado (esperado: dict)")
    
    # Process data
    logger.info("🔧 Processando dados...")
    try:
        vagas_df, prospects_df, applicants_df = data_loader.process_decision_data()
        
        logger.info(f"✅ Dados processados com sucesso:")
        logger.info(f"   - Vagas DataFrame: {vagas_df.shape}")
        logger.info(f"   - Prospects DataFrame: {prospects_df.shape}")
        logger.info(f"   - Applicants DataFrame: {applicants_df.shape}")
        
        # Show sample data
        if not vagas_df.empty:
            logger.info(f"   - Colunas Vagas: {list(vagas_df.columns)}")
        if not prospects_df.empty:
            logger.info(f"   - Colunas Prospects: {list(prospects_df.columns)}")
        if not applicants_df.empty:
            logger.info(f"   - Colunas Applicants: {list(applicants_df.columns)}")
        
        # Check data relationships
        logger.info("🔗 Verificando relacionamentos...")
        
        # Check if prospect candidates exist in applicants
        prospect_candidates = set(prospects_df['candidate_id'].dropna())
        applicant_ids = set(applicants_df['candidate_id'].dropna())
        missing_candidates = prospect_candidates - applicant_ids
        
        if missing_candidates:
            logger.warning(f"⚠️  {len(missing_candidates)} candidatos em prospects não encontrados em applicants")
        else:
            logger.info("✅ Todos os candidatos em prospects existem em applicants")
        
        # Check if prospect jobs exist in vagas
        prospect_jobs = set(prospects_df['job_id'].dropna())
        vaga_ids = set(vagas_df['job_id'].dropna())
        missing_jobs = prospect_jobs - vaga_ids
        
        if missing_jobs:
            logger.warning(f"⚠️  {len(missing_jobs)} vagas em prospects não encontradas em vagas")
        else:
            logger.info("✅ Todas as vagas em prospects existem em vagas")
        
        logger.info("🎉 Validação concluída com sucesso!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar dados: {e}")
        return False

if __name__ == "__main__":
    validate_decision_data()