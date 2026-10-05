"""Configuration loader for ingestion pipeline.

This module provides utilities to load and validate YAML configuration
files for the Enterprise RAG ingestion pipeline.
"""

import yaml
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, Any, List, Optional


@dataclass
class PipelineConfig:
    """Pipeline configuration section."""
    name: str
    version: str


@dataclass
class IngestionConfig:
    """Ingestion configuration section."""
    knowledge_base_path: str
    supported_extensions: List[str]


@dataclass
class MetadataConfig:
    """Metadata configuration section."""
    required_fields: List[str]
    departments: List[str]
    doc_types: List[str]


@dataclass
class ChunkingConfig:
    """Chunking configuration section."""
    strategy: str
    chunk_size: int
    chunk_overlap: int


@dataclass
class HybridConfig:
    """Hybrid search configuration section."""
    vector_weight: float
    lexical_weight: float


@dataclass
class VectorStoreConfig:
    """Vector store configuration section."""
    backend: str
    persist_directory: str
    hybrid: HybridConfig


@dataclass
class GenerationConfig:
    """Generation configuration section."""
    max_context_chunks: int
    require_citations: bool
    refuse_when_no_context: bool


@dataclass
class EvaluationConfig:
    """Evaluation configuration section."""
    required_answer_fields: List[str]
    min_citation_when_answered: int


@dataclass
class IngestionPipelineConfig:
    """Full ingestion pipeline configuration."""
    pipeline: PipelineConfig
    ingestion: IngestionConfig
    metadata: MetadataConfig
    chunking: ChunkingConfig
    vector_store: VectorStoreConfig
    generation: GenerationConfig
    evaluation: EvaluationConfig

    @classmethod
    def load_from_yaml(cls, config_path: Path) -> 'IngestionPipelineConfig':
        """Load configuration from a YAML file."""
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IngestionPipelineConfig':
        """Create configuration from dictionary."""
        return cls(
            pipeline=PipelineConfig(**data['pipeline']),
            ingestion=IngestionConfig(**data['ingestion']),
            metadata=MetadataConfig(**data['metadata']),
            chunking=ChunkingConfig(**data['chunking']),
            vector_store=VectorStoreConfig(
                backend=data['vector_store']['backend'],
                persist_directory=data['vector_store']['persist_directory'],
                hybrid=HybridConfig(**data['vector_store']['hybrid'])
            ),
            generation=GenerationConfig(**data['generation']),
            evaluation=EvaluationConfig(**data['evaluation'])
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        result = {
            'pipeline': self.pipeline.__dict__,
            'ingestion': self.ingestion.__dict__,
            'metadata': self.metadata.__dict__,
            'chunking': self.chunking.__dict__,
            'vector_store': {
                'backend': self.vector_store.backend,
                'persist_directory': self.vector_store.persist_directory,
                'hybrid': self.vector_store.hybrid.__dict__
            },
            'generation': self.generation.__dict__,
            'evaluation': self.evaluation.__dict__
        }
        return result
