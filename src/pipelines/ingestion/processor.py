"""Processor module for adding metadata to documents.

This module provides utilities to enrich markdown documents with
metadata fields required for the RAG pipeline.
"""

import re
from dataclasses import dataclass, asdict
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Any, Optional


@dataclass
class DocumentMetadata:
    """Metadata structure for processed documents."""
    department: str
    doc_type: str
    version: str
    effective_date: date
    source: str
    file_type: str
    title: str
    owner: str
    privacy_level: str
    audience: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary with ISO date formatting."""
        data = asdict(self)
        if isinstance(data['effective_date'], date):
            data['effective_date'] = data['effective_date'].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentMetadata':
        """Create metadata from dictionary."""
        if isinstance(data.get('effective_date'), str):
            data['effective_date'] = datetime.strptime(data['effective_date'], '%Y-%m-%d').date()
        return cls(**data)


class MetadataProcessor:
    """Processor to add metadata to markdown documents."""

    def __init__(self, metadata: DocumentMetadata):
        self.metadata = metadata

    def process(self, content: str) -> str:
        """Add metadata as YAML frontmatter to markdown content."""
        frontmatter = "---\n"
        meta_dict = self.metadata.to_dict()
        for key, value in meta_dict.items():
            if isinstance(value, str) and '\n' in value:
                # Use literal block for multiline strings
                frontmatter += f"{key}:\n"
                for line in value.split('\n'):
                    frontmatter += f"  {line}\n"
            else:
                frontmatter += f"{key}: {value}\n"
        frontmatter += "---\n\n"

        # If content already has frontmatter, merge or replace
        if content.strip().startswith('---'):
            # Remove existing frontmatter
            match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if match:
                content = content[match.end():]

        return frontmatter + content

    @classmethod
    def create_from_file(cls, file_path: Path) -> 'MetadataProcessor':
        """Create a processor with metadata inferred from a file path."""
        file_name = file_path.name
        file_stem = file_path.stem
        file_ext = file_path.suffix.lower()

        # Infer basic metadata
        metadata = DocumentMetadata(
            department="general",
            doc_type="document",
            version="1.0",
            effective_date=date.today(),
            source=str(file_path),
            file_type=file_ext.lstrip('.'),
            title=file_stem.replace('_', ' ').replace('-', ' ').title(),
            owner="unknown",
            privacy_level="internal",
            audience="internal"
        )
        return cls(metadata)
