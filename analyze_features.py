"""
Análise detalhada das features criadas com os dados reais
"""
import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from data.data_loader import DataLoader
from features.feature_engineering import FeatureEngineer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_features():
    """Analyze features created from real data"""
    print("=" * 80)
    print("🔍 ANÁLISE DETALHADA DAS FEATURES - DADOS REAIS DA DECISION")
    print("=" * 80)
    print()
    
    # Load data
    data_loader = DataLoader("data/")
    feature_engineer = FeatureEngineer()
    
    vagas_df, prospects_df, applicants_df = data_loader.process_decision_data()
    
    print("📊 DADOS CARREGADOS:")
    print(f"   Vagas: {len(vagas_df)}")
    print(f"   Candidatos: {len(applicants_df)}")
    print(f"   Prospecções: {len(prospects_df)}")
    print()
    
    # Show raw data
    print("📋 VAGAS DISPONÍVEIS:")
    for _, vaga in vagas_df.iterrows():
        print(f"   🏢 {vaga['job_id']}: {vaga['titulo']}")
        print(f"      Cliente: {vaga['cliente']}")
        print(f"      Nível: {vaga['nivel_profissional']}")
        print(f"      SAP: {'Sim' if vaga['is_sap'] else 'Não'}")
        print(f"      Skills: {vaga['competencias_tecnicas']}")
        print(f"      Localização: {vaga['localizacao']}")
        print(f"      Salário: {vaga['salario_range']}")
        print()
    
    print("👥 CANDIDATOS DISPONÍVEIS:")
    for _, candidate in applicants_df.iterrows():
        print(f"   👤 {candidate['candidate_id']}: {candidate['nome']}")
        print(f"      Experiência: {candidate['anos_experiencia']} anos")
        print(f"      Skills: {candidate['conhecimentos_tecnicos']}")
        print(f"      Localização: {candidate['localizacao']}")
        print(f"      Pretensão: R$ {candidate['pretensao_salarial']}")
        print(f"      Inglês: {candidate['nivel_ingles']}")
        print()
    
    print("🔗 PROSPECÇÕES:")
    for _, prospect in prospects_df.iterrows():
        print(f"   📝 Job {prospect['job_id']} + Candidato {prospect['candidate_id']}")
        print(f"      Status: {prospect['status']}")
        print(f"      Comentário: {prospect['comment']}")
        print()
    
    # Create features
    features_df = feature_engineer.create_features(vagas_df, applicants_df, prospects_df)
    target = feature_engineer.create_target_variable(features_df)
    
    print("🔧 FEATURES CALCULADAS:")
    print()
    
    for i, (_, row) in enumerate(features_df.iterrows()):
        job_id = row['job_id']
        candidate_id = row['candidate_id']
        target_val = target.iloc[i]
        
        print(f"   📊 MATCH {i+1}: Job {job_id} + Candidato {candidate_id}")
        print(f"      🎯 Target: {'✅ Positivo' if target_val == 1 else '❌ Negativo'}")
        print(f"      🔧 Skill Match: {row['skill_match']:.3f}")
        print(f"      📈 Experience Match: {row['experience_match']:.3f}")
        print(f"      💰 Salary Match: {row['salary_match']:.3f}")
        print(f"      📍 Location Match: {row['location_match']:.3f}")
        print(f"      🇺🇸 English Match: {row['english_match']:.3f}")
        print(f"      🇪🇸 Spanish Match: {row['spanish_match']:.3f}")
        print(f"      🏢 SAP Match: {row['sap_match']:.3f}")
        print(f"      🎓 Academic Match: {row['academic_match']:.3f}")
        print(f"      📊 Candidate Experience: {row['candidate_experience_years']} anos")
        print(f"      🔢 Candidate Skills: {row['num_candidate_skills']}")
        print(f"      🔢 Job Skills: {row['num_job_skills']}")
        print(f"      🏢 Is SAP Job: {'Sim' if row['is_sap_job'] == 1 else 'Não'}")
        print()
    
    # Feature correlation with target
    print("📈 CORRELAÇÃO DAS FEATURES COM O TARGET:")
    feature_cols = [col for col in features_df.columns if col not in ['candidate_id', 'job_id', 'status']]
    correlations = []
    
    for col in feature_cols:
        corr = features_df[col].corr(target)
        correlations.append((col, corr))
    
    correlations.sort(key=lambda x: abs(x[1]), reverse=True)
    
    for feature, corr in correlations:
        direction = "📈" if corr > 0 else "📉" if corr < 0 else "➡️"
        print(f"   {direction} {feature}: {corr:.3f}")
    
    print()
    print("=" * 80)
    print("🎯 INSIGHTS DOS DADOS REAIS:")
    print("=" * 80)
    
    # Analyze specific matches
    print("\n🔍 ANÁLISE DOS MATCHES:")
    
    # Perfect matches
    perfect_matches = features_df[target == 1]
    if not perfect_matches.empty:
        print(f"\n✅ MATCHES POSITIVOS ({len(perfect_matches)}):")
        for _, match in perfect_matches.iterrows():
            print(f"   • Job {match['job_id']} + Candidato {match['candidate_id']}")
            print(f"     Skill: {match['skill_match']:.3f}, Exp: {match['experience_match']:.3f}, Sal: {match['salary_match']:.3f}")
    
    # Failed matches
    failed_matches = features_df[target == 0]
    if not failed_matches.empty:
        print(f"\n❌ MATCHES NEGATIVOS ({len(failed_matches)}):")
        for _, match in failed_matches.iterrows():
            print(f"   • Job {match['job_id']} + Candidato {match['candidate_id']}")
            print(f"     Skill: {match['skill_match']:.3f}, Exp: {match['experience_match']:.3f}, Sal: {match['salary_match']:.3f}")
    
    print("\n🎉 Análise concluída!")

if __name__ == "__main__":
    analyze_features()