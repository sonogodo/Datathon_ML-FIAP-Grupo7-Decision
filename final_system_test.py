#!/usr/bin/env python3
"""
Final comprehensive system test for Decision AI
"""
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ {description} - SUCCESS")
            return True
        else:
            print(f"   ❌ {description} - FAILED")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ {description} - ERROR: {e}")
        return False

def main():
    """Run comprehensive system tests"""
    print("🚀 DECISION AI - FINAL SYSTEM TEST")
    print("=" * 50)
    
    tests = [
        ("python validate_data.py", "Data Validation"),
        ("python src/train_model.py", "Model Training"),
        ("pytest tests/ -v --tb=short", "Unit Tests"),
        ("python test_system.py", "System Integration Test"),
        ("python test_api_functionality.py", "Core API Functionality"),
        ("python test_api_endpoints.py", "API Endpoints Test"),
    ]
    
    passed = 0
    total = len(tests)
    
    for command, description in tests:
        if run_command(command, description):
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 FINAL RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Decision AI system is fully functional")
        print("\n🚀 READY FOR PRODUCTION!")
        print("\n📋 Next Steps:")
        print("   1. Start API: python src/api/main.py")
        print("   2. Test API: curl http://localhost:8000/")
        print("   3. Deploy with Docker: docker build -t decision-ai .")
        return True
    else:
        print("⚠️  Some tests failed")
        print("🔧 Please review the errors above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)