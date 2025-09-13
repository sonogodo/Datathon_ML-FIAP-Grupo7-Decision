# 📁 Instruções para Upload dos Dados da Decision

## Como fazer upload dos seus dados JSON

### 1. Estrutura esperada dos arquivos

Coloque os seguintes arquivos na pasta `data/`:

```
data/
├── vagas.json         # Dados das vagas (chaveado por código da vaga)
├── prospects.json     # Prospecções por vaga (chaveado por código da vaga)
└── applicants.json    # Dados dos candidatos (chaveado por código do candidato)
```

### 2. Formato esperado dos dados

#### vagas.json

```json
{
  "10976": {
    "codigo_vaga": "10976",
    "titulo": "Desenvolvedor Python Sênior",
    "cliente": "TechCorp",
    "is_sap": false,
    "nivel_profissional": "Senior",
    "nivel_ingles": "Intermediário",
    "nivel_espanhol": "Básico",
    "principais_atividades": "Desenvolvimento de APIs REST...",
    "competencias_tecnicas": ["Python", "Django", "PostgreSQL"],
    "beneficios": ["Vale refeição", "Plano de saúde"],
    "localizacao": "São Paulo - SP",
    "salario_range": "12000-18000"
  }
}
```

#### prospects.json

```json
{
  "10976": [
    {
      "codigo_candidato": "41496",
      "nome_candidato": "Sr. Thales Freitas",
      "comentario": "Candidato com excelente fit técnico",
      "situacao": "Contratado"
    }
  ]
}
```

#### applicants.json

```json
{
  "41496": {
    "codigo_candidato": "41496",
    "nome": "Sr. Thales Freitas",
    "nivel_academico": "Superior Completo",
    "nivel_ingles": "Intermediário",
    "nivel_espanhol": "Básico",
    "conhecimentos_tecnicos": ["Python", "Django", "Flask"],
    "area_atuacao": "Desenvolvimento de Software",
    "anos_experiencia": 6,
    "localizacao": "São Paulo - SP",
    "pretensao_salarial": "15000",
    "cv_resumo": "Desenvolvedor Python com 6 anos..."
  }
}
```

### 3. Após fazer upload dos dados

1. **Validar os dados:**

   ```bash
   python validate_data.py
   ```

2. **Treinar o modelo:**

   ```bash
   python src/train_model.py
   ```

3. **Iniciar a API:**

   ```bash
   python src/api/main.py
   ```

4. **Testar a API:**
   ```bash
   curl http://localhost:8000/health
   ```

### 4. Campos importantes para o modelo

O sistema utiliza os seguintes campos para criar features:

**Jobs:**

- `competencias_tecnicas`: Lista de habilidades técnicas
- `nivel_profissional`: Nível da vaga (Junior, Pleno, Senior)
- `nivel_ingles`, `nivel_espanhol`: Requisitos de idioma
- `is_sap`: Se é vaga SAP
- `salario_range`: Faixa salarial
- `localizacao`: Localização da vaga

**Applicants:**

- `conhecimentos_tecnicos`: Habilidades do candidato
- `anos_experiencia`: Anos de experiência
- `nivel_ingles`, `nivel_espanhol`: Nível de idiomas
- `pretensao_salarial`: Pretensão salarial
- `localizacao`: Localização do candidato

**Prospects:**

- `situacao`: Status da candidatura (Contratado, Rejeitado, etc.)

### 5. Mapeamento de Status

O sistema mapeia os seguintes status para o target:

- ✅ **Positivos (1)**: "Contratado", "Aprovado"
- ❌ **Negativos (0)**: "Rejeitado", "Não aprovado", "Cancelado", "Desistiu"
- ⚠️ **Neutros**: "Em processo" (convertido para 0)

### 6. Troubleshooting

Se encontrar problemas:

1. **Erro de formato JSON**: Verifique se os arquivos são JSON válidos
2. **Campos faltando**: O sistema é tolerante a campos faltantes
3. **Poucos dados**: O modelo precisa de pelo menos 10 amostras para funcionar bem
4. **Performance baixa**: Com dados reais, a performance deve melhorar significativamente

### 7. Exemplo de uso da API

```bash
# Testar com dados existentes
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": "41496",
       "job_id": "10976"
     }'

# Testar com dados novos
curl -X POST "http://localhost:8000/predict_with_data" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate": {
         "id": "new_candidate",
         "skills": ["Python", "Django"],
         "experience_years": 3,
         "location": "São Paulo",
         "salary_expectation": "10000",
         "culture_fit": "innovative"
       },
       "job": {
         "id": "new_job",
         "title": "Python Developer",
         "required_skills": ["Python", "Django"],
         "experience_level": "Mid",
         "location": "São Paulo",
         "salary_range": "8000-12000",
         "company_culture": "innovative"
       }
     }'
```

---

**Precisa de ajuda?** Execute `python demo.py` para ver uma demonstração completa do sistema!
