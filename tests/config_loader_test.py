"""Tests for configuration loader."""

from pathlib import Path
import tempfile

from src.utils.config_loader import (
    IngestionPipelineConfig,
    PipelineConfig,
    IngestionConfig,
    MetadataConfig,
    ChunkingConfig,
    VectorStoreConfig,
    GenerationConfig,
    EvaluationConfig,
    HybridConfig,
)


def test_config_from_dict():
    """Test creating config from dictionary."""
    data = {
        "pipeline": {"name": "test-pipeline", "version": "1.0.0"},
        "ingestion": {"knowledge_base_path": "data", "supported_extensions": [".md", ".pdf"]},
        "metadata": {
            "required_fields": ["title", "department"],
            "departments": ["engineering"],
            "doc_types": ["document"]
        },
        "chunking": {"strategy": "semantic", "chunk_size": 1000, "chunk_overlap": 200},
        "vector_store": {
            "backend": "faiss",
            "persist_directory": "storage",
            "hybrid": {"vector_weight": 0.7, "lexical_weight": 0.3}
        },
        "generation": {
            "max_context_chunks": 5,
            "require_citations": True,
            "refuse_when_no_context": True
        },
        "evaluation": {
            "required_answer_fields": ["answer", "citations"],
            "min_citation_when_answered": 1
        }
    }
    config = IngestionPipelineConfig.from_dict(data)
    assert config.pipeline.name == "test-pipeline"
    assert config.ingestion.knowledge_base_path == "data"
    assert config.chunking.chunk_size == 1000
    assert config.vector_store.hybrid.vector_weight == 0.7


def test_config_to_dict():
    """Test converting config to dictionary."""
    config = IngestionPipelineConfig(
        pipeline=PipelineConfig(name="test", version="1.0.0"),
        ingestion=IngestionConfig(knowledge_base_path="data", supported_extensions=[".md"]),
        metadata=MetadataConfig(required_fields=["title"], departments=["eng"], doc_types=["doc"]),
        chunking=ChunkingConfig(strategy="fixed", chunk_size=500, chunk_overlap=50),
        vector_store=VectorStoreConfig(
            backend="faiss",
            persist_directory="storage",
            hybrid=HybridConfig(vector_weight=0.8, lexical_weight=0.2)
        ),
        generation=GenerationConfig(max_context_chunks=3, require_citations=True, refuse_when_no_context=False),
        evaluation=EvaluationConfig(required_answer_fields=["answer"], min_citation_when_answered=1)
    )
    data = config.to_dict()
    assert data["pipeline"]["name"] == "test"
    assert data["vector_store"]["hybrid"]["vector_weight"] == 0.8


def test_config_load_from_yaml():
    """Test loading config from YAML file."""
    yaml_content = """
pipeline:
  name: test-pipeline
  version: 0.1.0
ingestion:
  knowledge_base_path: test_data
  supported_extensions: [.md]
metadata:
  required_fields: [title, department]
  departments: [engineering]
  doc_types: [document]
chunking:
  strategy: semantic
  chunk_size: 1000
  chunk_overlap: 200
vector_store:
  backend: faiss
  persist_directory: storage
  hybrid:
    vector_weight: 0.7
    lexical_weight: 0.3
generation:
  max_context_chunks: 5
  require_citations: true
  refuse_when_no_context: true
evaluation:
  required_answer_fields: [answer, citations]
  min_citation_when_answered: 1
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        tmp_path = Path(f.name)

    config = IngestionPipelineConfig.load_from_yaml(tmp_path)
    assert config.pipeline.name == "test-pipeline"
    assert config.ingestion.knowledge_base_path == "test_data"
    assert config.generation.require_citations is True
