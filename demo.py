"""
Demonstração completa do sistema Decision AI
"""
import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from data.data_loader import DataLoader
from features.feature_engineering import FeatureEngineer
from models.candidate_job_matcher import CandidateJobMatcher
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def demo_decision_ai():
    """Demonstração completa do sistema"""
    print("=" * 80)
    print("🚀 DECISION AI - SISTEMA DE MATCHING CANDIDATO-VAGA")
    print("=" * 80)
    print()
    
    # 1. Inicialização
    print("📋 1. INICIALIZANDO COMPONENTES...")
    data_loader = DataLoader("data/")
    feature_engineer = FeatureEngineer()
    matcher = CandidateJobMatcher()
    print("✅ Componentes inicializados")
    print()
    
    # 2. Dados
    print("📊 2. PREPARANDO DADOS...")
    data_loader.create_sample_data()
    vagas_df, prospects_df, applicants_df = data_loader.process_decision_data()
    
    print(f"   📁 Vagas carregadas: {len(vagas_df)}")
    print(f"   👥 Candidatos: {len(applicants_df)}")
    print(f"   🔗 Prospecções: {len(prospects_df)}")
    print()
    
    # 3. Feature Engineering
    print("🔧 3. ENGENHARIA DE FEATURES...")
    X, y = feature_engineer.prepare_training_data(vagas_df, applicants_df, prospects_df)
    print(f"   📈 Features criadas: {X.shape}")
    print(f"   🎯 Distribuição target: Positivos={y.sum()}, Negativos={len(y)-y.sum()}")
    print()
    
    # 4. Treinamento
    print("🤖 4. TREINANDO MODELO...")
    metrics = matcher.train(X, y)
    print(f"   📊 AUC Score: {metrics['roc_auc']:.3f}")
    print(f"   🎯 Acurácia: {metrics['test_accuracy']:.3f}")
    print()
    
    # 5. Feature Importance
    print("📈 5. IMPORTÂNCIA DAS FEATURES:")
    importance_df = matcher.get_feature_importance()
    for _, row in importance_df.head(5).iterrows():
        print(f"   • {row['feature']}: {row['importance']:.3f}")
    print()
    
    # 6. Predições de Exemplo
    print("🔮 6. EXEMPLOS DE PREDIÇÃO:")
    print()
    
    # Exemplo 1: Match perfeito
    print("   📋 EXEMPLO 1 - Match Python Developer:")
    sample_data = {
        'skill_match': 0.8,
        'experience_match': 0.9,
        'salary_match': 0.7,
        'location_match': 1.0,
        'english_match': 0.8,
        'spanish_match': 0.5,
        'sap_match': 1.0,
        'academic_match': 1.0,
        'candidate_experience_years': 6,
        'num_candidate_skills': 6,
        'num_job_skills': 5,
        'is_sap_job': 0
    }
    
    import pandas as pd
    sample_X = pd.DataFrame([sample_data])
    sample_X_scaled = pd.DataFrame(
        feature_engineer.scaler.transform(sample_X),
        columns=sample_X.columns
    )
    
    result = matcher.evaluate_model_confidence(sample_X_scaled)
    print(f"   🎯 Match Score: {result['match_score']:.3f}")
    print(f"   🔒 Confiança: {result['confidence']:.3f}")
    print(f"   💡 Recomendação: {result['recommendation']}")
    print(f"   🔑 Fatores chave: {', '.join(result['key_factors'][:3])}")
    print()
    
    # Exemplo 2: Match SAP
    print("   📋 EXEMPLO 2 - Match SAP Analyst:")
    sample_data_sap = sample_data.copy()
    sample_data_sap.update({
        'skill_match': 0.9,
        'sap_match': 1.0,
        'is_sap_job': 1,
        'english_match': 1.0
    })
    
    sample_X_sap = pd.DataFrame([sample_data_sap])
    sample_X_sap_scaled = pd.DataFrame(
        feature_engineer.scaler.transform(sample_X_sap),
        columns=sample_X_sap.columns
    )
    
    result_sap = matcher.evaluate_model_confidence(sample_X_sap_scaled)
    print(f"   🎯 Match Score: {result_sap['match_score']:.3f}")
    print(f"   🔒 Confiança: {result_sap['confidence']:.3f}")
    print(f"   💡 Recomendação: {result_sap['recommendation']}")
    print(f"   🔑 Fatores chave: {', '.join(result_sap['key_factors'][:3])}")
    print()
    
    # 7. Salvamento
    print("💾 7. SALVANDO MODELO...")
    matcher.save_model("models/candidate_job_matcher.joblib")
    import joblib
    joblib.dump(feature_engineer, "models/feature_engineer.joblib")
    print("✅ Modelo salvo com sucesso")
    print()
    
    # 8. Resumo
    print("📋 8. RESUMO DO SISTEMA:")
    print(f"   🎯 Modelo treinado com {len(X)} amostras")
    print(f"   📊 {len(X.columns)} features utilizadas")
    print(f"   🤖 Algoritmo: Random Forest Classifier")
    print(f"   📈 Performance: AUC = {metrics['roc_auc']:.3f}")
    print(f"   💾 Modelo salvo em: models/candidate_job_matcher.joblib")
    print()
    
    print("=" * 80)
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    print()
    print("📚 PRÓXIMOS PASSOS:")
    print("   1. Faça upload dos dados reais da Decision (vagas.json, prospects.json, applicants.json)")
    print("   2. Execute: python validate_data.py")
    print("   3. Retreine o modelo: python src/train_model.py")
    print("   4. Inicie a API: python src/api/main.py")
    print("   5. Teste a API: curl http://localhost:8000/health")
    print()

if __name__ == "__main__":
    demo_decision_ai()