"""
Tests for data loading functionality
"""
import pytest
import pandas as pd
import json
import tempfile
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data.data_loader import DataLoader

class TestDataLoader:
    
    def test_load_json_data_success(self):
        """Test successful JSON data loading"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test data
            test_data = [{"id": "1", "name": "test"}]
            test_file = Path(temp_dir) / "test.json"
            
            with open(test_file, 'w') as f:
                json.dump(test_data, f)
            
            # Test loading
            loader = DataLoader(temp_dir)
            result = loader.load_json_data("test.json")
            
            assert result == test_data
    
    def test_load_json_data_file_not_found(self):
        """Test handling of missing files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            loader = DataLoader(temp_dir)
            result = loader.load_json_data("nonexistent.json")
            
            assert result == []
    
    def test_create_sample_data(self):
        """Test sample data creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            loader = DataLoader(temp_dir)
            loader.create_sample_data()
            
            # Check files were created (using correct filenames)
            assert (Path(temp_dir) / "vagas.json").exists()
            assert (Path(temp_dir) / "applicants.json").exists()
            assert (Path(temp_dir) / "prospects.json").exists()
            
            # Load and verify data
            vagas_df, prospects_df, applicants_df = loader.process_decision_data()
            
            assert not vagas_df.empty
            assert not prospects_df.empty
            assert not applicants_df.empty
    
    def test_load_all_data_empty(self):
        """Test loading when no data exists"""
        with tempfile.TemporaryDirectory() as temp_dir:
            loader = DataLoader(temp_dir)
            vagas_df, prospects_df, applicants_df = loader.load_all_data()
            
            assert vagas_df.empty
            assert prospects_df.empty
            assert applicants_df.empty