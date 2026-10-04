# Enterprise RAG Platform

A comprehensive Retrieval-Augmented Generation system for enterprise document search and question answering.

## Overview

The Enterprise RAG Platform enables organizations to build, deploy, and manage secure, scalable retrieval-augmented generation systems across multiple data sources including SharePoint, Confluence, and S3 storage.

## Features

- **Multi-source Ingestion**: SharePoint, Confluence, and S3 connectors with synchronized sync schedules
- **Advanced Parsing**: Layout-aware PDF parsing and intelligent chunking strategies
- **Vector Search**: FAISS/hnsw-based vector indexing with metadata schema support
- **Security & Governance**: ACL filtering, PII redaction, encryption, and audit logging
- **Evaluation Framework**: Ragas/TruLens triad metrics with golden dataset management
- **Operations**: Terraform/Docker/Kubernetes pipelines with observability and incident response

## Documentation

For complete technical specifications, see the [documentation site](./docs/).

## Quickstart

```bash
# Install dependencies
pip install -r requirements.txt

# Start the documentation site
mkdocs serve -d docs
```