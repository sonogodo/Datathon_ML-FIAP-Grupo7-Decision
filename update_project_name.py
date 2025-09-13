#!/usr/bin/env python3
"""
Script para atualizar referências ao nome do projeto
"""
import os
import re
from pathlib import Path

def update_file_content(file_path, old_name, new_name):
    """Update file content replacing old project name with new one"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace various forms of the old name
        replacements = [
            (f'cd {old_name}', f'cd {new_name}'),
            (f'/{old_name}', f'/{new_name}'),
            (f'{old_name}/', f'{new_name}/'),
            (f'"{old_name}"', f'"{new_name}"'),
            (f"'{old_name}'", f"'{new_name}'"),
        ]
        
        updated = False
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                updated = True
        
        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")

def main():
    """Update project name references"""
    old_name = "decision-ai"
    new_name = "Datathon_ML-FIAP-Grupo7-Decision"
    
    print(f"🔄 Updating project name from '{old_name}' to '{new_name}'")
    print("=" * 60)
    
    # Files to update
    files_to_update = [
        "README.md",
        "GITHUB_SETUP.md", 
        "PROFESSOR_README.md",
        "QUICK_START.md",
        "EVALUATION_CHECKLIST.md",
        "setup.py",
        "run_demo.py"
    ]
    
    for file_name in files_to_update:
        file_path = Path(file_name)
        if file_path.exists():
            update_file_content(file_path, old_name, new_name)
        else:
            print(f"⚠️  File not found: {file_name}")
    
    print("\n🎉 Project name update completed!")
    print(f"New project name: {new_name}")
    print("\n📋 Next steps:")
    print("1. Create GitHub repository with the new name")
    print("2. Push your code")
    print("3. Share the repository URL with your professor")

if __name__ == "__main__":
    main()