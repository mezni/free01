"""Processor tests for the ingestion pipeline.

Tests for the metadata processor in src.pipelines.ingestion.processor.
"""

from datetime import date
from pathlib import Path
import tempfile

from src.pipelines.ingestion.processor import (
    DocumentMetadata,
    MetadataProcessor,
)


def test_document_metadata_to_dict():
    """Test DocumentMetadata to_dict conversion."""
    meta = DocumentMetadata(
        department="engineering",
        doc_type="specification",
        version="2.1",
        effective_date=date(2026, 10, 4),
        source="/data/spec.md",
        file_type="md",
        title="API Specification",
        owner="alice",
        privacy_level="restricted",
        audience="engineering-team"
    )
    result = meta.to_dict()
    assert result['department'] == "engineering"
    assert result['version'] == "2.1"
    assert result['effective_date'] == "2026-10-04"
    assert result['title'] == "API Specification"


def test_document_metadata_from_dict():
    """Test DocumentMetadata from_dict conversion."""
    data = {
        "department": "sales",
        "doc_type": "playbook",
        "version": "1.0",
        "effective_date": "2026-10-04",
        "source": "/data/playbook.pdf",
        "file_type": "pdf",
        "title": "Sales Playbook",
        "owner": "bob",
        "privacy_level": "internal",
        "audience": "sales-team"
    }
    meta = DocumentMetadata.from_dict(data)
    assert meta.department == "sales"
    assert meta.effective_date == date(2026, 10, 4)
    assert meta.file_type == "pdf"


def test_metadata_processor_adds_frontmatter():
    """Test that processor adds YAML frontmatter."""
    meta = DocumentMetadata(
        department="security",
        doc_type="policy",
        version="1.5",
        effective_date=date(2026, 10, 4),
        source="/data/policy.md",
        file_type="md",
        title="Security Policy",
        owner="carol",
        privacy_level="internal",
        audience="all-staff"
    )
    processor = MetadataProcessor(meta)
    content = "# Security Policy\n\nThis is the security policy content."
    result = processor.process(content)
    assert result.startswith("---\n")
    assert "department: security" in result
    assert "version: 1.5" in result
    assert "title: Security Policy" in result
    assert content in result


def test_metadata_processor_replaces_existing_frontmatter():
    """Test that processor replaces existing frontmatter."""
    meta = DocumentMetadata(
        department="engineering",
        doc_type="guide",
        version="1.0",
        effective_date=date(2026, 10, 4),
        source="/data/guide.md",
        file_type="md",
        title="Guide",
        owner="dana",
        privacy_level="public",
        audience="developers"
    )
    processor = MetadataProcessor(meta)
    content_with_fm = "---\nold: value\n---\n\n# Guide\n\nContent"
    result = processor.process(content_with_fm)
    assert "department: engineering" in result
    assert "old: value" not in result
    assert "# Guide" in result


def test_metadata_processor_create_from_file():
    """Test creating processor from file path."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".pdf", delete=False) as f:
        f.write("content")
        tmp_path = Path(f.name)

    processor = MetadataProcessor.create_from_file(tmp_path)
    assert processor.metadata.file_type == "pdf"
    assert processor.metadata.title is not None
    assert processor.metadata.effective_date == date.today()


def test_metadata_processor_process_preserves_content():
    """Test that content is preserved after processing."""
    meta = DocumentMetadata(
        department="network-ops",
        doc_type="runbook",
        version="2.0",
        effective_date=date(2026, 10, 4),
        source="/data/runbook.md",
        file_type="md",
        title="Runbook",
        owner="eve",
        privacy_level="restricted",
        audience="operators"
    )
    processor = MetadataProcessor(meta)
    content = "# Runbook\n\n## Procedure\n\n1. Step one\n2. Step two\n\n**Important:** Note here."
    result = processor.process(content)
    assert "# Runbook" in result
    assert "## Procedure" in result
    assert "Step one" in result
    assert "**Important:** Note here." in result


def test_metadata_contains_all_fields():
    """Test that all required fields are included."""
    meta = DocumentMetadata(
        department="billing",
        doc_type="policy",
        version="3.0",
        effective_date=date(2026, 10, 4),
        source="/data/billing.pdf",
        file_type="pdf",
        title="Billing Policy",
        owner="frank",
        privacy_level="confidential",
        audience="finance"
    )
    result = meta.to_dict()
    required_fields = [
        "department", "doc_type", "version", "effective_date",
        "source", "file_type", "title", "owner", "privacy_level", "audience"
    ]
    for field in required_fields:
        assert field in result
