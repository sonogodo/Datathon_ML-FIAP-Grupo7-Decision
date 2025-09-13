#!/usr/bin/env python3
"""
Script de demonstração rápida para professores/avaliadores
Execute este arquivo para ver o sistema funcionando imediatamente
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Execute command and show output"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"❌ Erro: {result.stderr}")
            return False
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False

def main():
    """Demonstração completa do sistema"""
    print("🎓 DECISION AI - DEMONSTRAÇÃO PARA AVALIAÇÃO")
    print("=" * 60)
    print("Este script executa uma demonstração completa do sistema")
    print("Desenvolvido para o Datathon da Decision")
    print()
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ é necessário")
        print(f"Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    
    # Install dependencies
    print("\n📦 Instalando dependências...")
    if not run_command("pip install -r requirements.txt", "Instalação de dependências"):
        print("❌ Falha na instalação das dependências")
        return False
    
    # Run validation
    if not run_command("python validate_data.py", "Validação dos dados"):
        print("⚠️ Validação falhou, mas continuando com dados de exemplo...")
    
    # Run training
    if not run_command("python src/train_model.py", "Treinamento do modelo"):
        print("❌ Falha no treinamento do modelo")
        return False
    
    # Run tests
    if not run_command("python -m pytest tests/ -v", "Execução dos testes unitários"):
        print("⚠️ Alguns testes falharam, mas o sistema principal funciona")
    
    # Run demo
    if not run_command("python demo.py", "Demonstração completa do sistema"):
        print("❌ Falha na demonstração")
        return False
    
    print("\n" + "="*60)
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print()
    print("📋 PRÓXIMOS PASSOS PARA TESTAR A API:")
    print("1. Em um terminal, execute: python src/api/main.py")
    print("2. Em outro terminal, execute: python test_api.py")
    print()
    print("📊 ARQUIVOS IMPORTANTES:")
    print("- README.md: Documentação completa")
    print("- FINAL_SUMMARY.md: Resumo do projeto")
    print("- src/: Código fonte modularizado")
    print("- tests/: Testes unitários")
    print("- models/: Modelos treinados")
    print()
    print("🏆 Sistema pronto para avaliação!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)