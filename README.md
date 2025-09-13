# Decision AI - Candidate-Job Matching System

> 🎓 **Para Professores/Avaliadores**: Execute `python run_demo.py` para uma demonstração completa em 1 comando!
> 
> 📋 **Quick Start**: Veja [QUICK_START.md](QUICK_START.md) para instruções rápidas

## Visão Geral do Projeto

### Objetivo

Desenvolver um sistema de inteligência artificial para otimizar o processo de recrutamento da Decision, focando no match entre candidatos e vagas através de análise automatizada de perfis e requisitos.

### Solução Proposta

Pipeline completa de machine learning que analisa candidatos e vagas para:

- Calcular score de compatibilidade candidato-vaga
- Identificar os melhores matches automaticamente
- Reduzir tempo de triagem manual
- Padronizar processo de avaliação

### Stack Tecnológica

- **Linguagem**: Python 3.9+
- **Frameworks ML**: scikit-learn, pandas, numpy
- **API**: FastAPI
- **Serialização**: joblib
- **Testes**: pytest
- **Empacotamento**: Docker
- **Deploy**: Local/Cloud ready
- **Monitoramento**: logging + drift detection

## Estrutura do Projeto

```
decision-ai/
├── data/                   # Dados de entrada
├── src/                    # Código fonte
│   ├── data/              # Processamento de dados
│   ├── features/          # Feature engineering
│   ├── models/            # Modelos ML
│   └── api/               # API endpoints
├── models/                # Modelos treinados
├── tests/                 # Testes unitários
├── docker/                # Configuração Docker
├── requirements.txt       # Dependências
└── Dockerfile            # Container config
```

## Instruções de Deploy

### Pré-requisitos

- Python 3.9+
- Docker (opcional)

### 1. Preparação dos Dados

Coloque os arquivos JSON da Decision na pasta `data/`:

- `data/vagas.json` - Dados das vagas
- `data/prospects.json` - Prospecções por vaga
- `data/applicants.json` - Dados dos candidatos

### 2. Validação dos Dados

```bash
# Validar estrutura dos dados
python validate_data.py

# Testar sistema com dados de exemplo
python test_system.py
```

### 3. Instalação Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Treinar modelo
python src/train_model.py

# Iniciar API
python src/api/main.py
```

### 4. Deploy com Docker

```bash
docker build -t decision-ai .
docker run -p 8000:8000 decision-ai
```

### 5. Testes

```bash
# Executar testes unitários
pytest tests/ -v --cov=src --cov-report=html

# Demonstração completa
python demo.py

# Testar API
curl http://localhost:8000/health
```

## Pipeline de Machine Learning

### Etapas do Pipeline

1. **Pré-processamento dos Dados**

   - Carregamento dos arquivos JSON da Decision
   - Normalização da estrutura de dados
   - Limpeza e validação

2. **Engenharia de Features**

   - Match de habilidades técnicas (Jaccard similarity)
   - Compatibilidade de experiência por nível
   - Match salarial com tolerância
   - Compatibilidade geográfica
   - Avaliação de níveis de idioma (inglês/espanhol)
   - Detecção de vagas SAP vs skills SAP
   - Nível acadêmico

3. **Treinamento e Validação**

   - Algoritmo: Random Forest Classifier
   - Validação cruzada com ajuste para datasets pequenos
   - Métricas: AUC-ROC, Accuracy, Precision, Recall
   - Feature importance analysis

4. **Seleção de Modelo**

   - Threshold de AUC >= 0.7 para produção
   - Análise de feature importance
   - Validação de confiança das predições

5. **Pós-processamento**
   - Cálculo de confidence score
   - Classificação em high/medium/low match
   - Identificação de fatores-chave

## Métricas e Monitoramento

### Métricas do Modelo

- **AUC-ROC**: Área sob a curva ROC (target: >= 0.7)
- **Accuracy**: Acurácia geral do modelo
- **Precision/Recall**: Para classes balanceadas
- **Feature Importance**: Ranking das features mais importantes

### Monitoramento de Drift

- Detecção automática de drift nas features
- Monitoramento de distribuição das predições
- Alertas quando drift > 10%
- Dashboard de métricas em tempo real

## Arquitetura Técnica

### Componentes Principais

- **DataLoader**: Carregamento e processamento dos dados JSON
- **FeatureEngineer**: Criação e transformação de features
- **CandidateJobMatcher**: Modelo de ML para matching
- **DriftDetector**: Monitoramento de drift do modelo
- **FastAPI**: API REST para predições

### Features Utilizadas

1. `skill_match`: Similaridade entre skills candidato-vaga
2. `experience_match`: Compatibilidade de experiência
3. `salary_match`: Alinhamento salarial
4. `location_match`: Compatibilidade geográfica
5. `english_match`: Nível de inglês
6. `spanish_match`: Nível de espanhol
7. `sap_match`: Compatibilidade SAP
8. `academic_match`: Nível acadêmico
9. `candidate_experience_years`: Anos de experiência
10. `num_candidate_skills`: Quantidade de skills do candidato
11. `num_job_skills`: Quantidade de skills da vaga
12. `is_sap_job`: Flag se é vaga SAP

## Exemplos de Uso da API

### Endpoint de Predição com IDs existentes

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": "41496",
       "job_id": "10976"
     }'
```

### Endpoint de Predição com dados completos

```bash
curl -X POST "http://localhost:8000/predict_with_data" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate": {
         "id": "candidate_001",
         "skills": ["Python", "Django", "PostgreSQL"],
         "experience_years": 6,
         "location": "São Paulo - SP",
         "salary_expectation": "15000",
         "culture_fit": "innovative"
       },
       "job": {
         "id": "job_001",
         "title": "Desenvolvedor Python Sênior",
         "required_skills": ["Python", "Django", "PostgreSQL"],
         "experience_level": "Senior",
         "location": "São Paulo - SP",
         "salary_range": "12000-18000",
         "company_culture": "innovative"
       }
     }'
```

### Resposta Esperada

```json
{
  "match_score": 0.85,
  "confidence": 0.92,
  "recommendation": "high_match",
  "key_factors": ["skill_match", "experience_match", "location_match"]
}
```

### Outros Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Informações do modelo
curl http://localhost:8000/model/info

# Status de drift
curl http://localhost:8000/monitoring/drift
```
