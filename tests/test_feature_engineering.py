"""
Tests for feature engineering functionality
"""
import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from features.feature_engineering import FeatureEngineer

class TestFeatureEngineer:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.feature_engineer = FeatureEngineer()
    
    def test_calculate_skill_match_perfect(self):
        """Test perfect skill match"""
        candidate_skills = ["Python", "Django", "PostgreSQL"]
        job_skills = ["Python", "Django", "PostgreSQL"]
        
        match = self.feature_engineer.calculate_skill_match(candidate_skills, job_skills)
        assert match == 1.0
    
    def test_calculate_skill_match_partial(self):
        """Test partial skill match"""
        candidate_skills = ["Python", "Django"]
        job_skills = ["Python", "Flask", "MongoDB"]
        
        match = self.feature_engineer.calculate_skill_match(candidate_skills, job_skills)
        assert 0 < match < 1
    
    def test_calculate_skill_match_no_match(self):
        """Test no skill match"""
        candidate_skills = ["Java", "Spring"]
        job_skills = ["Python", "Django"]
        
        match = self.feature_engineer.calculate_skill_match(candidate_skills, job_skills)
        assert 0 <= match < 0.5
    
    def test_calculate_skill_match_string_input(self):
        """Test skill match with string input"""
        candidate_skills = "Python, Django, PostgreSQL"
        job_skills = ["Python", "Django"]
        
        match = self.feature_engineer.calculate_skill_match(candidate_skills, job_skills)
        assert match > 0
    
    def test_calculate_experience_match_perfect(self):
        """Test perfect experience match"""
        match = self.feature_engineer.calculate_experience_match(3, "Pleno")
        assert match == 1.0
    
    def test_calculate_experience_match_senior(self):
        """Test senior level match"""
        match = self.feature_engineer.calculate_experience_match(6, "Senior")
        assert match == 1.0
        
        match = self.feature_engineer.calculate_experience_match(6, "Sênior")
        assert match == 1.0
    
    def test_calculate_experience_match_underqualified(self):
        """Test underqualified candidate"""
        match = self.feature_engineer.calculate_experience_match(1, "Senior")
        assert 0 <= match < 1
    
    def test_calculate_salary_match_perfect(self):
        """Test perfect salary match"""
        match = self.feature_engineer.calculate_salary_match("10000", "8000-12000")
        assert match == 1.0
    
    def test_calculate_salary_match_too_high(self):
        """Test salary expectation too high"""
        match = self.feature_engineer.calculate_salary_match("15000", "8000-12000")
        assert 0 <= match < 1
    
    def test_calculate_salary_match_too_low(self):
        """Test salary expectation too low"""
        match = self.feature_engineer.calculate_salary_match("5000", "8000-12000")
        assert 0 <= match < 1
    
    def test_calculate_language_match_perfect(self):
        """Test perfect language match"""
        match = self.feature_engineer.calculate_language_match("Avançado", "Intermediário")
        assert match == 1.0
    
    def test_calculate_language_match_insufficient(self):
        """Test insufficient language level"""
        match = self.feature_engineer.calculate_language_match("Básico", "Avançado")
        assert 0 <= match < 1
    
    def test_calculate_language_match_not_required(self):
        """Test language not required"""
        match = self.feature_engineer.calculate_language_match("Não possui", "Não requerido")
        assert match == 1.0
    
    def test_calculate_sap_match_sap_job_with_skills(self):
        """Test SAP job with SAP skills"""
        candidate_skills = ["SAP ABAP", "SAP ECC", "Python"]
        match = self.feature_engineer.calculate_sap_match(candidate_skills, True)
        assert match == 1.0
    
    def test_calculate_sap_match_sap_job_no_skills(self):
        """Test SAP job without SAP skills"""
        candidate_skills = ["Python", "Django", "React"]
        match = self.feature_engineer.calculate_sap_match(candidate_skills, True)
        assert match == 0.2
    
    def test_calculate_sap_match_non_sap_job(self):
        """Test non-SAP job"""
        candidate_skills = ["Python", "Django"]
        match = self.feature_engineer.calculate_sap_match(candidate_skills, False)
        assert match == 1.0
    
    def test_create_features_empty_data(self):
        """Test feature creation with empty data"""
        jobs_df = pd.DataFrame()
        applicants_df = pd.DataFrame()
        prospects_df = pd.DataFrame()
        
        features_df = self.feature_engineer.create_features(jobs_df, applicants_df, prospects_df)
        assert features_df.empty
    
    def test_create_target_variable(self):
        """Test target variable creation"""
        features_df = pd.DataFrame({
            'status': ['Contratado', 'Rejeitado', 'Em processo', 'Aprovado']
        })
        
        target = self.feature_engineer.create_target_variable(features_df)
        
        assert len(target) == 4
        assert target.iloc[0] == 1  # Contratado
        assert target.iloc[1] == 0  # Rejeitado
        assert target.iloc[3] == 1  # Aprovado