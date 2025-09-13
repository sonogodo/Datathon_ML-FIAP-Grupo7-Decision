# 🚀 Quick Start - Decision AI

## Para Professores/Avaliadores

Este projeto foi desenvolvido para o **Datathon da Decision** e implementa um sistema completo de matching candidato-vaga usando Machine Learning.

### ⚡ Execução Rápida (1 comando)

```bash
python run_demo.py
```

Este comando irá:

- ✅ Verificar dependências
- ✅ Instalar bibliotecas necessárias
- ✅ Validar dados
- ✅ Treinar o modelo
- ✅ Executar testes
- ✅ Mostrar demonstração completa

### 📋 Requisitos Mínimos

- **Python 3.9+** (recomendado 3.11)
- **pip** (gerenciador de pacotes Python)
- **10 MB** de espaço livre

### 🔧 Instalação Manual (se preferir)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Validar dados
python validate_data.py

# 3. Treinar modelo
python src/train_model.py

# 4. Executar testes
pytest tests/ -v

# 5. Ver demonstração
python demo.py
```

### 🌐 Testar API

```bash
# Terminal 1: Iniciar API
python src/api/main.py

# Terminal 2: Testar API
python test_api.py
```

### 📊 Estrutura do Projeto

```
Datathon_ML-FIAP-Grupo7-Decision/
├── src/                    # Código fonte modularizado
│   ├── data/              # Carregamento de dados
│   ├── features/          # Feature engineering
│   ├── models/            # Modelos ML
│   └── api/               # API REST
├── tests/                 # Testes unitários (35 testes)
├── data/                  # Dados de exemplo
├── models/                # Modelos treinados
├── README.md              # Documentação completa
├── FINAL_SUMMARY.md       # Resumo executivo
└── run_demo.py           # Demonstração rápida
```

### 🎯 Principais Features

- **12 features** especializadas para matching
- **API REST** com FastAPI
- **Testes unitários** com 100% cobertura
- **Docker** ready para deploy
- **Monitoramento** de drift
- **Documentação** completa

### 📈 Resultados Esperados

Com os dados de exemplo:

- ✅ Modelo treinado e salvo
- ✅ API funcionando na porta 8000
- ✅ 35 testes unitários passando
- ✅ Features calculadas corretamente
- ✅ Predições em tempo real

### 🆘 Problemas Comuns

**Erro de dependências:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Erro de Python:**

- Certifique-se de usar Python 3.9+
- No Windows: `python --version`
- No Linux/Mac: `python3 --version`

**Porta 8000 ocupada:**

```bash
# Matar processo na porta 8000
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -ti:8000 | xargs kill
```

### 📞 Contato

Sistema desenvolvido para demonstrar aplicação prática de ML em RH, focando em:

- Pipeline completa de ML
- Código de produção
- Testes automatizados
- Deploy containerizado
- Monitoramento contínuo

**Tempo estimado de avaliação: 10-15 minutos** ⏱️
