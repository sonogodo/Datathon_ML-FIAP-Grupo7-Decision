"""
Feature engineering for candidate-job matching
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, LabelEncoder
import logging

logger = logging.getLogger(__name__)

class FeatureEngineer:
    """Creates features for candidate-job matching model"""
    
    def __init__(self):
        self.skill_vectorizer = TfidfVectorizer(max_features=100)
        self.scaler = StandardScaler()
        self.location_encoder = LabelEncoder()
        self.culture_encoder = LabelEncoder()
        self.fitted = False
        
    def calculate_skill_match(self, candidate_skills, job_skills) -> float:
        """Calculate skill match percentage between candidate and job"""
        # Handle different input formats
        if isinstance(candidate_skills, str):
            candidate_skills = [skill.strip() for skill in candidate_skills.split(',')]
        if isinstance(job_skills, str):
            job_skills = [skill.strip() for skill in job_skills.split(',')]
        
        if not candidate_skills or not job_skills:
            return 0.0
            
        candidate_set = set([skill.lower().strip() for skill in candidate_skills if skill])
        job_set = set([skill.lower().strip() for skill in job_skills if skill])
        
        if not candidate_set or not job_set:
            return 0.0
        
        intersection = candidate_set.intersection(job_set)
        union = candidate_set.union(job_set)
        
        return len(intersection) / len(union) if union else 0.0
    
    def calculate_experience_match(self, candidate_exp, job_level: str) -> float:
        """Calculate experience level match"""
        # Convert candidate experience to int if needed
        try:
            candidate_exp = int(candidate_exp) if candidate_exp else 0
        except (ValueError, TypeError):
            candidate_exp = 0
            
        level_mapping = {
            'junior': (0, 2),
            'pleno': (2, 5),
            'mid': (2, 5), 
            'senior': (5, 10),
            'sênior': (5, 10),
            'lead': (8, 15),
            'especialista': (6, 12)
        }
        
        job_level_clean = job_level.lower().strip() if job_level else 'pleno'
        if job_level_clean not in level_mapping:
            return 0.5  # neutral score for unknown levels
            
        min_exp, max_exp = level_mapping[job_level_clean]
        
        if min_exp <= candidate_exp <= max_exp:
            return 1.0
        elif candidate_exp < min_exp:
            return max(0.0, 1.0 - (min_exp - candidate_exp) / min_exp)
        else:
            return max(0.0, 1.0 - (candidate_exp - max_exp) / max_exp)
    
    def calculate_salary_match(self, candidate_expectation, job_range: str) -> float:
        """Calculate salary expectation match"""
        try:
            # Convert candidate expectation to float
            if isinstance(candidate_expectation, str):
                candidate_expectation = float(candidate_expectation.replace(',', '').replace('R$', '').strip())
            elif candidate_expectation is None:
                return 0.5
            else:
                candidate_expectation = float(candidate_expectation)
            
            # Parse job salary range (e.g., "8000-12000")
            if not job_range:
                return 0.5
                
            job_range = str(job_range).replace('R$', '').replace(',', '').strip()
            if '-' in job_range:
                min_sal, max_sal = map(float, job_range.split('-'))
            else:
                min_sal = max_sal = float(job_range)
                
            if min_sal <= candidate_expectation <= max_sal:
                return 1.0
            elif candidate_expectation < min_sal:
                return max(0.0, 1.0 - (min_sal - candidate_expectation) / min_sal)
            else:
                return max(0.0, 1.0 - (candidate_expectation - max_sal) / max_sal)
                
        except (ValueError, AttributeError, TypeError):
            return 0.5  # neutral score for parsing errors
    
    def calculate_location_match(self, candidate_location: str, job_location: str) -> float:
        """Calculate location compatibility"""
        if not candidate_location or not job_location:
            return 0.5
            
        candidate_clean = candidate_location.lower().strip()
        job_clean = job_location.lower().strip()
        
        if candidate_clean == job_clean:
            return 1.0
        elif any(city in candidate_clean for city in ['são paulo', 'sp']) and \
             any(city in job_clean for city in ['são paulo', 'sp']):
            return 1.0
        elif any(city in candidate_clean for city in ['rio de janeiro', 'rj']) and \
             any(city in job_clean for city in ['rio de janeiro', 'rj']):
            return 1.0
        else:
            return 0.3  # different locations but still possible (remote, etc.)
    
    def calculate_culture_match(self, candidate_culture: str, job_culture: str) -> float:
        """Calculate culture fit match"""
        if not candidate_culture or not job_culture:
            return 0.5
            
        candidate_clean = candidate_culture.lower().strip()
        job_clean = job_culture.lower().strip()
        
        return 1.0 if candidate_clean == job_clean else 0.3
    
    def calculate_language_match(self, candidate_level: str, required_level: str, language: str = "inglês") -> float:
        """Calculate language proficiency match"""
        if not candidate_level or not required_level:
            return 0.5
            
        # Normalize language levels
        level_mapping = {
            'não possui': 0,
            'básico': 1,
            'intermediário': 2,
            'avançado': 3,
            'fluente': 4,
            'nativo': 5,
            'não requerido': -1  # Special case for not required
        }
        
        candidate_score = level_mapping.get(candidate_level.lower().strip(), 0)
        required_score = level_mapping.get(required_level.lower().strip(), 0)
        
        # If not required, return perfect match
        if required_score == -1:
            return 1.0
            
        # If candidate meets or exceeds requirement
        if candidate_score >= required_score:
            return 1.0
        elif candidate_score == 0 and required_score > 0:
            return 0.0  # No knowledge when required
        else:
            # Partial match based on how close they are
            return max(0.0, candidate_score / required_score)
    
    def calculate_sap_match(self, candidate_skills, job_is_sap: bool) -> float:
        """Calculate SAP-specific match"""
        if not job_is_sap:
            return 1.0  # Not SAP job, so SAP skills don't matter
            
        # Check if candidate has SAP skills
        if isinstance(candidate_skills, str):
            candidate_skills = [skill.strip() for skill in candidate_skills.split(',')]
        
        sap_keywords = ['sap', 'abap', 'hana', 's/4hana', 'ecc', 'fico', 'mm', 'sd', 'pp', 'hr']
        candidate_skills_lower = [skill.lower() for skill in candidate_skills if skill]
        
        has_sap_skills = any(any(keyword in skill for keyword in sap_keywords) for skill in candidate_skills_lower)
        
        return 1.0 if has_sap_skills else 0.2  # Low score if SAP job but no SAP skills
    
    def create_features(self, vagas_df: pd.DataFrame, applicants_df: pd.DataFrame, 
                       prospects_df: pd.DataFrame) -> pd.DataFrame:
        """Create feature matrix for training with Decision data structure"""
        features = []
        
        for _, prospect in prospects_df.iterrows():
            candidate_id = prospect['candidate_id']
            job_id = prospect['job_id']
            
            # Get candidate and job data
            candidate_mask = applicants_df['candidate_id'] == candidate_id
            vaga_mask = vagas_df['job_id'] == job_id
            
            if not candidate_mask.any() or not vaga_mask.any():
                continue
                
            candidate = applicants_df[candidate_mask].iloc[0]
            vaga = vagas_df[vaga_mask].iloc[0]
            
            # Calculate feature scores
            skill_match = self.calculate_skill_match(
                candidate.get('conhecimentos_tecnicos', []), 
                vaga.get('competencias_tecnicas', [])
            )
            
            experience_match = self.calculate_experience_match(
                candidate.get('anos_experiencia', 0),
                vaga.get('nivel_profissional', 'Pleno')
            )
            
            salary_match = self.calculate_salary_match(
                candidate.get('pretensao_salarial', 0),
                vaga.get('salario_range', '0-0')
            )
            
            location_match = self.calculate_location_match(
                candidate.get('localizacao', ''),
                vaga.get('localizacao', '')
            )
            
            # Language matches
            english_match = self.calculate_language_match(
                candidate.get('nivel_ingles', ''),
                vaga.get('nivel_ingles', ''),
                'inglês'
            )
            
            spanish_match = self.calculate_language_match(
                candidate.get('nivel_espanhol', ''),
                vaga.get('nivel_espanhol', ''),
                'espanhol'
            )
            
            # SAP match
            sap_match = self.calculate_sap_match(
                candidate.get('conhecimentos_tecnicos', []),
                vaga.get('is_sap', False)
            )
            
            # Academic level match (simplified)
            academic_match = 1.0 if candidate.get('nivel_academico') else 0.5
            
            # Create feature vector
            feature_row = {
                'candidate_id': candidate_id,
                'job_id': job_id,
                'skill_match': skill_match,
                'experience_match': experience_match,
                'salary_match': salary_match,
                'location_match': location_match,
                'english_match': english_match,
                'spanish_match': spanish_match,
                'sap_match': sap_match,
                'academic_match': academic_match,
                'candidate_experience_years': candidate.get('anos_experiencia', 0),
                'num_candidate_skills': len(candidate.get('conhecimentos_tecnicos', [])) if isinstance(candidate.get('conhecimentos_tecnicos'), list) else 0,
                'num_job_skills': len(vaga.get('competencias_tecnicas', [])) if isinstance(vaga.get('competencias_tecnicas'), list) else 0,
                'is_sap_job': 1 if vaga.get('is_sap', False) else 0,
                'status': prospect.get('status', 'applied')
            }
            
            features.append(feature_row)
        
        features_df = pd.DataFrame(features)
        logger.info(f"Created {len(features_df)} feature rows")
        
        return features_df
    
    def create_target_variable(self, features_df: pd.DataFrame) -> pd.Series:
        """Create target variable based on application status"""
        # Map status to binary target (1 = successful match, 0 = unsuccessful)
        # Baseado nos status da Decision
        status_mapping = {
            'contratado': 1,
            'aprovado': 1,
            'em processo': 0.5,  # Neutral - ainda em avaliação
            'rejeitado': 0,
            'desistiu': 0,
            'não aprovado': 0,
            'cancelado': 0
        }
        
        # Normalize status strings and map
        normalized_status = features_df['status'].str.lower().str.strip()
        target = normalized_status.map(status_mapping).fillna(0)
        
        # Convert 0.5 to binary (can be adjusted based on business logic)
        target = (target >= 0.5).astype(int)
        
        logger.info(f"Created target variable with {target.sum()} positive samples out of {len(target)}")
        
        return target
    
    def prepare_training_data(self, vagas_df: pd.DataFrame, applicants_df: pd.DataFrame,
                            prospects_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare complete training dataset"""
        # Create features
        features_df = self.create_features(vagas_df, applicants_df, prospects_df)
        
        if features_df.empty:
            logger.warning("No features created - returning empty datasets")
            return pd.DataFrame(), pd.Series(dtype=int)
        
        # Create target
        target = self.create_target_variable(features_df)
        
        # Select feature columns for training (updated for Decision data)
        feature_columns = [
            'skill_match', 'experience_match', 'salary_match', 
            'location_match', 'english_match', 'spanish_match',
            'sap_match', 'academic_match', 'candidate_experience_years',
            'num_candidate_skills', 'num_job_skills', 'is_sap_job'
        ]
        
        # Ensure all feature columns exist
        available_columns = [col for col in feature_columns if col in features_df.columns]
        if len(available_columns) != len(feature_columns):
            missing = set(feature_columns) - set(available_columns)
            logger.warning(f"Missing feature columns: {missing}")
        
        X = features_df[available_columns]
        y = target
        
        # Scale features
        if not self.fitted:
            X_scaled = pd.DataFrame(
                self.scaler.fit_transform(X),
                columns=X.columns,
                index=X.index
            )
            self.fitted = True
        else:
            X_scaled = pd.DataFrame(
                self.scaler.transform(X),
                columns=X.columns,
                index=X.index
            )
        
        logger.info(f"Prepared training data: X shape {X_scaled.shape}, y shape {y.shape}")
        
        return X_scaled, y