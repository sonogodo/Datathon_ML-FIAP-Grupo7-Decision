"""
Data loading and preprocessing utilities for Decision AI
"""
import pandas as pd
import json
import logging
from typing import Dict, List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class DataLoader:
    """Handles loading and initial processing of Decision data"""
    
    def __init__(self, data_path: str = "data/"):
        self.data_path = Path(data_path)
        
    def load_json_data(self, filename: str) -> List[Dict]:
        """Load JSON data from file"""
        try:
            file_path = self.data_path / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data)} records from {filename}")
            return data
        except FileNotFoundError:
            logger.error(f"File {filename} not found in {self.data_path}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON from {filename}: {e}")
            return []
    
    def load_all_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load all Decision data files"""
        # Load raw data - usando os nomes corretos dos arquivos
        vagas_data = self.load_json_data("vagas.json")
        prospects_data = self.load_json_data("prospects.json") 
        applicants_data = self.load_json_data("applicants.json")
        
        # Convert to DataFrames
        vagas_df = pd.DataFrame(vagas_data) if vagas_data else pd.DataFrame()
        prospects_df = pd.DataFrame(prospects_data) if prospects_data else pd.DataFrame()
        applicants_df = pd.DataFrame(applicants_data) if applicants_data else pd.DataFrame()
        
        logger.info(f"Loaded data shapes: vagas={vagas_df.shape}, prospects={prospects_df.shape}, applicants={applicants_df.shape}")
        
        return vagas_df, prospects_df, applicants_df
    
    def create_sample_data(self):
        """Create sample data for testing when real data is not available"""
        # Sample jobs data - estrutura baseada na Decision
        sample_jobs = {
            "10976": {
                "codigo_vaga": "10976",
                "titulo": "Desenvolvedor Python Sênior",
                "cliente": "TechCorp",
                "is_sap": False,
                "nivel_profissional": "Senior",
                "nivel_ingles": "Intermediário",
                "nivel_espanhol": "Básico",
                "principais_atividades": "Desenvolvimento de APIs REST, integração com bancos de dados, code review",
                "competencias_tecnicas": ["Python", "Django", "PostgreSQL", "Docker", "AWS"],
                "beneficios": ["Vale refeição", "Plano de saúde", "Home office"],
                "localizacao": "São Paulo - SP",
                "salario_range": "12000-18000"
            },
            "10977": {
                "codigo_vaga": "10977", 
                "titulo": "Analista SAP ABAP",
                "cliente": "Enterprise Solutions",
                "is_sap": True,
                "nivel_profissional": "Pleno",
                "nivel_ingles": "Avançado",
                "nivel_espanhol": "Não requerido",
                "principais_atividades": "Desenvolvimento ABAP, customizações SAP, suporte funcional",
                "competencias_tecnicas": ["SAP ABAP", "SAP ECC", "SAP S/4HANA", "SQL"],
                "beneficios": ["Vale refeição", "Plano de saúde", "Participação nos lucros"],
                "localizacao": "Rio de Janeiro - RJ",
                "salario_range": "8000-12000"
            }
        }
        
        # Sample applicants data - estrutura baseada na Decision
        sample_applicants = {
            "41496": {
                "codigo_candidato": "41496",
                "nome": "Sr. Thales Freitas",
                "nivel_academico": "Superior Completo",
                "nivel_ingles": "Intermediário",
                "nivel_espanhol": "Básico",
                "conhecimentos_tecnicos": ["Python", "Django", "Flask", "PostgreSQL", "Docker", "Git"],
                "area_atuacao": "Desenvolvimento de Software",
                "anos_experiencia": 6,
                "localizacao": "São Paulo - SP",
                "pretensao_salarial": "15000",
                "cv_resumo": "Desenvolvedor Python com 6 anos de experiência em desenvolvimento web..."
            },
            "41497": {
                "codigo_candidato": "41497",
                "nome": "Sra. Ana Costa",
                "nivel_academico": "Superior Completo",
                "nivel_ingles": "Avançado", 
                "nivel_espanhol": "Não possui",
                "conhecimentos_tecnicos": ["SAP ABAP", "SAP ECC", "SAP S/4HANA", "SQL Server", "Oracle"],
                "area_atuacao": "Consultoria SAP",
                "anos_experiencia": 4,
                "localizacao": "Rio de Janeiro - RJ",
                "pretensao_salarial": "10000",
                "cv_resumo": "Consultora SAP ABAP com 4 anos de experiência em projetos de implementação..."
            }
        }
        
        # Sample prospects data - estrutura baseada na Decision
        sample_prospects = {
            "10976": [
                {
                    "codigo_candidato": "41496",
                    "nome_candidato": "Sr. Thales Freitas",
                    "comentario": "Candidato com excelente fit técnico, aprovado em todas as etapas",
                    "situacao": "Contratado"
                },
                {
                    "codigo_candidato": "41497",
                    "nome_candidato": "Sra. Ana Costa",
                    "comentario": "Perfil não adequado para Python, mais focada em SAP",
                    "situacao": "Rejeitado"
                }
            ],
            "10977": [
                {
                    "codigo_candidato": "41497",
                    "nome_candidato": "Sra. Ana Costa",
                    "comentario": "Perfil adequado para a vaga SAP, contratada",
                    "situacao": "Contratado"
                },
                {
                    "codigo_candidato": "41496",
                    "nome_candidato": "Sr. Thales Freitas",
                    "comentario": "Não tem experiência em SAP",
                    "situacao": "Rejeitado"
                }
            ]
        }
        
        # Save sample data
        self.data_path.mkdir(exist_ok=True)
        
        with open(self.data_path / "vagas.json", 'w', encoding='utf-8') as f:
            json.dump(sample_jobs, f, indent=2, ensure_ascii=False)
            
        with open(self.data_path / "applicants.json", 'w', encoding='utf-8') as f:
            json.dump(sample_applicants, f, indent=2, ensure_ascii=False)
            
        with open(self.data_path / "prospects.json", 'w', encoding='utf-8') as f:
            json.dump(sample_prospects, f, indent=2, ensure_ascii=False)
            
        logger.info("Sample data created successfully")
    
    def process_decision_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Process Decision data into normalized DataFrames"""
        # Load raw data with correct method
        vagas_data = self.load_json_data("vagas.json")
        prospects_data = self.load_json_data("prospects.json")
        applicants_data = self.load_json_data("applicants.json")
        
        # Process vagas data (dictionary format)
        vagas_list = []
        if isinstance(vagas_data, dict):
            for vaga_code, vaga_info in vagas_data.items():
                vaga_info_copy = vaga_info.copy()
                vaga_info_copy['job_id'] = vaga_code
                vagas_list.append(vaga_info_copy)
        vagas_df = pd.DataFrame(vagas_list)
        
        # Process applicants data (dictionary format)
        applicants_list = []
        if isinstance(applicants_data, dict):
            for candidate_code, candidate_info in applicants_data.items():
                candidate_info_copy = candidate_info.copy()
                candidate_info_copy['candidate_id'] = candidate_code
                applicants_list.append(candidate_info_copy)
        applicants_df = pd.DataFrame(applicants_list)
        
        # Process prospects data (nested dictionary format)
        prospects_list = []
        if isinstance(prospects_data, dict):
            for job_code, candidates_list in prospects_data.items():
                if isinstance(candidates_list, list):
                    for candidate in candidates_list:
                        prospect_row = {
                            'job_id': job_code,
                            'candidate_id': candidate.get('codigo_candidato'),
                            'candidate_name': candidate.get('nome_candidato'),
                            'comment': candidate.get('comentario'),
                            'status': candidate.get('situacao')
                        }
                        prospects_list.append(prospect_row)
        prospects_df = pd.DataFrame(prospects_list)
        
        logger.info(f"Processed Decision data: vagas={len(vagas_df)}, applicants={len(applicants_df)}, prospects={len(prospects_df)}")
        
        return vagas_df, prospects_df, applicants_df
    
    def get_job_candidate_pairs(self) -> List[Dict]:
        """Get all job-candidate pairs for training"""
        vagas_df, prospects_df, applicants_df = self.process_decision_data()
        
        pairs = []
        for _, prospect in prospects_df.iterrows():
            job_id = prospect['job_id']
            candidate_id = prospect['candidate_id']
            
            # Get job and candidate details
            job_info = vagas_df[vagas_df['job_id'] == job_id].iloc[0].to_dict() if not vagas_df[vagas_df['job_id'] == job_id].empty else {}
            candidate_info = applicants_df[applicants_df['candidate_id'] == candidate_id].iloc[0].to_dict() if not applicants_df[applicants_df['candidate_id'] == candidate_id].empty else {}
            
            pair = {
                'job_id': job_id,
                'candidate_id': candidate_id,
                'job_info': job_info,
                'candidate_info': candidate_info,
                'status': prospect['status'],
                'comment': prospect['comment']
            }
            pairs.append(pair)
        
        return pairs