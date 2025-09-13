#!/usr/bin/env python3
"""
Script para verificar se o ambiente está pronto para executar o Decision AI
"""
import sys
import subprocess
import importlib
from pathlib import Path

def check_python_version():
    """Verifica versão do Python"""
    print("🐍 Verificando versão do Python...")
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Requer Python 3.9+")
        return False

def check_pip():
    """Verifica se pip está disponível"""
    print("📦 Verificando pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print("   ✅ pip disponível")
        return True
    except subprocess.CalledProcessError:
        print("   ❌ pip não encontrado")
        return False

def check_dependencies():
    """Verifica dependências principais"""
    print("📚 Verificando dependências...")
    
    required_packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'), 
        ('scikit-learn', 'sklearn'),
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('joblib', 'joblib'),
        ('pydantic', 'pydantic'),
        ('pytest', 'pytest')
    ]
    
    missing = []
    for package_name, import_name in required_packages:
        try:
            importlib.import_module(import_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - não instalado")
            missing.append(package_name)
    
    return len(missing) == 0, missing

def check_project_structure():
    """Verifica estrutura do projeto"""
    print("📁 Verificando estrutura do projeto...")
    
    required_paths = [
        'src/',
        'src/data/',
        'src/features/',
        'src/models/',
        'src/api/',
        'tests/',
        'data/',
        'requirements.txt'
    ]
    
    missing = []
    for path in required_paths:
        if Path(path).exists():
            print(f"   ✅ {path}")
        else:
            print(f"   ❌ {path} - não encontrado")
            missing.append(path)
    
    return len(missing) == 0, missing

def check_data_files():
    """Verifica arquivos de dados"""
    print("📊 Verificando arquivos de dados...")
    
    data_files = ['vagas.json', 'prospects.json', 'applicants.json']
    found_files = []
    
    for file in data_files:
        file_path = Path('data') / file
        if file_path.exists():
            print(f"   ✅ {file}")
            found_files.append(file)
        else:
            print(f"   ⚠️  {file} - não encontrado (será criado automaticamente)")
    
    return len(found_files) > 0 or True  # OK mesmo sem dados reais

def main():
    """Verificação completa do ambiente"""
    print("🔍 VERIFICAÇÃO DO AMBIENTE - DECISION AI")
    print("=" * 50)
    
    checks = []
    
    # Python version
    checks.append(check_python_version())
    print()
    
    # pip
    checks.append(check_pip())
    print()
    
    # Dependencies
    deps_ok, missing_deps = check_dependencies()
    checks.append(deps_ok)
    print()
    
    # Project structure
    struct_ok, missing_paths = check_project_structure()
    checks.append(struct_ok)
    print()
    
    # Data files
    checks.append(check_data_files())
    print()
    
    # Summary
    print("📋 RESUMO DA VERIFICAÇÃO")
    print("=" * 50)
    
    if all(checks):
        print("🎉 AMBIENTE PRONTO!")
        print("   Todos os requisitos foram atendidos.")
        print("   Execute: python run_demo.py")
        return True
    else:
        print("⚠️  AMBIENTE PRECISA DE AJUSTES")
        
        if not deps_ok and missing_deps:
            print(f"   📦 Instale dependências: pip install {' '.join(missing_deps)}")
        
        if not struct_ok and missing_paths:
            print(f"   📁 Arquivos faltando: {', '.join(missing_paths)}")
        
        print("   🔧 Execute: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)