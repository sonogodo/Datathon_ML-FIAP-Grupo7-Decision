"""
Teste da API com dados reais da Decision
"""
import requests
import json
import time

def test_api():
    """Test API with real Decision data"""
    base_url = "http://localhost:8000"
    
    print("🚀 TESTANDO API DECISION AI")
    print("=" * 50)
    
    # Test health
    print("1. 🏥 Testando Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data}")
        else:
            print(f"   ❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
        return
    
    print()
    
    # Test model info
    print("2. 📊 Testando Model Info...")
    try:
        response = requests.get(f"{base_url}/model/info")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Modelo: {data['model_type']}")
            print(f"   📈 Features: {len(data['feature_names'])}")
        else:
            print(f"   ❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    
    # Test prediction with existing IDs
    print("3. 🔮 Testando Predição com IDs Existentes...")
    
    test_cases = [
        {
            "name": "Thales → Python (Match Positivo)",
            "candidate_id": "41496",
            "job_id": "10976",
            "expected": "high_match"
        },
        {
            "name": "Ana → SAP (Match Positivo)", 
            "candidate_id": "41497",
            "job_id": "10977",
            "expected": "high_match"
        },
        {
            "name": "Ana → Python (Match Negativo)",
            "candidate_id": "41497", 
            "job_id": "10976",
            "expected": "low_match"
        },
        {
            "name": "Thales → SAP (Match Negativo)",
            "candidate_id": "41496",
            "job_id": "10977", 
            "expected": "low_match"
        }
    ]
    
    for test_case in test_cases:
        print(f"   🧪 {test_case['name']}")
        
        payload = {
            "candidate_id": test_case["candidate_id"],
            "job_id": test_case["job_id"]
        }
        
        try:
            response = requests.post(
                f"{base_url}/predict",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"      🎯 Score: {data['match_score']:.3f}")
                print(f"      🔒 Confiança: {data['confidence']:.3f}")
                print(f"      💡 Recomendação: {data['recommendation']}")
                print(f"      🔑 Fatores: {', '.join(data['key_factors'][:3])}")
                
                # Check if prediction makes sense
                if test_case["expected"] == "high_match" and data['match_score'] > 0.6:
                    print("      ✅ Predição coerente!")
                elif test_case["expected"] == "low_match" and data['match_score'] < 0.4:
                    print("      ✅ Predição coerente!")
                else:
                    print("      ⚠️  Predição inesperada")
                    
            else:
                print(f"      ❌ Erro: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"      ❌ Erro: {e}")
        
        print()
    
    # Test prediction with new data
    print("4. 🆕 Testando Predição com Dados Novos...")
    
    new_candidate = {
        "id": "new_candidate",
        "skills": ["Python", "Django", "React", "AWS"],
        "experience_years": 5,
        "location": "São Paulo - SP",
        "salary_expectation": "14000",
        "culture_fit": "innovative"
    }
    
    new_job = {
        "id": "new_job",
        "title": "Full Stack Developer",
        "required_skills": ["Python", "Django", "React"],
        "experience_level": "Senior",
        "location": "São Paulo - SP", 
        "salary_range": "12000-16000",
        "company_culture": "innovative"
    }
    
    payload = {
        "candidate": new_candidate,
        "job": new_job
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict_with_data",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   🎯 Score: {data['match_score']:.3f}")
            print(f"   🔒 Confiança: {data['confidence']:.3f}")
            print(f"   💡 Recomendação: {data['recommendation']}")
            print(f"   🔑 Fatores: {', '.join(data['key_factors'][:3])}")
        else:
            print(f"   ❌ Erro: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    
    # Test drift monitoring
    print("5. 📈 Testando Monitoramento de Drift...")
    try:
        response = requests.get(f"{base_url}/monitoring/drift")
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Status: {data}")
        else:
            print(f"   ❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    print("🎉 Testes da API concluídos!")

if __name__ == "__main__":
    # Wait for API to be ready
    print("⏳ Aguardando API inicializar...")
    time.sleep(2)
    test_api()