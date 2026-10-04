# Quickstart & SDK Guide

## Getting Started

- Prerequisites
- Environment setup
- Authentication configuration

## Python SDK

```bash
pip install enterprise-rag-sdk
```

```python
from enterprise_rag import RAGClient

client = RAGClient(api_key="your-key")
client.search(query="your query")
```

## TypeScript SDK

```bash
npm install enterprise-rag-sdk
```

```typescript
import { RAGClient } from 'enterprise-rag-sdk';

const client = new RAGClient({ apiKey: 'your-key' });
client.search('your query');
```