# High-Level Design (HLD) - Enterprise RAG Platform

## 1. System Context Diagram (C4 Level 1)

This diagram shows how actors (End Users and System Administrators) interact with the Enterprise RAG System and its boundary integration with external enterprise systems (Identity Providers, Data Sources, and LLM Providers).

```mermaid
C4Context
    title System Context Diagram - Enterprise RAG Platform

    Person(user, "Enterprise User", "Queries internal knowledge base via Web UI or Slack/Teams bot.")
    Person(admin, "Knowledge Admin", "Uploads documents, manages access rights, and monitors system health.")

    System(ragSystem, "Enterprise RAG Platform", "Retrieves context, enforces security ACLs, and synthesizes grounded answers using LLMs.")

    System_Ext(idp, "Identity Provider", "Okta / Azure AD / OAuth2.0\nHandles authentication & enterprise user roles.")
    System_Ext(dataSources, "Enterprise Data Sources", "SharePoint, Confluence, S3, SQL, Notion\nStores enterprise documents.")
    System_Ext(llmProvider, "LLM & Embedding API", "OpenAI / Anthropic / AWS Bedrock / Azure AI\nGenerates embeddings & LLM responses.")

    Rel(user, ragSystem, "Sends queries & receives answers w/ citations", "HTTPS / WSS")
    Rel(admin, ragSystem, "Configures connectors, views analytics", "HTTPS")
    
    Rel(ragSystem, idp, "Validates JWT tokens & fetches user group permissions", "OIDC / REST")
    Rel(ragSystem, dataSources, "Syncs document corpus & permissions metadata", "REST / Webhooks")
    Rel(ragSystem, llmProvider, "Sends prompt context & receives text generations", "HTTPS / TLS 1.3")
```

## 2. Container Diagram (C4 Level 2)

This diagram breaks down the system boundary into microservices, data stores, vector indexes, and asynchronous processing workers.

```mermaid
C4Container
    title Container Diagram - Enterprise RAG Platform Architecture

    Person(user, "Enterprise User", "Queries platform")

    Container_Boundary(ragBoundary, "Enterprise RAG System Boundary") {
        Container(webUi, "Web UI / Client", "React / Next.js", "User query interface with streaming response rendering and inline citations.")
        Container(apiGateway, "API Gateway / Auth Middleware", "FastAPI / Traefik", "Handles rate limiting, TLS termination, and IDP JWT validation.")
        Container(queryEngine, "Query Orchestrator", "Python / LangChain / LlamaIndex", "Performs query expansion, hybrid search, reranking, and prompt synthesis.")
        Container(ingestionEngine, "Ingestion Pipeline Worker", "Python / Celery / Ray", "Extracts, parses, cleans, and chunks enterprise documents asynchronously.")
        Container(guardrails, "Guardrails & Safety Engine", "NeMo / Guardrails AI", "Inspects inputs/outputs for prompt injection, PII leakage, and off-topic queries.")
        
        ContainerDb(vectorDb, "Vector & Hybrid DB", "Qdrant / Milvus / Azure AI Search", "Stores dense embeddings, sparse BM25 index, and metadata payload filters (ACLs).")
        ContainerDb(relationalDb, "Application DB", "PostgreSQL", "Stores user feedback, chat sessions, document lineage, and pipeline metadata.")
        ContainerDb(cacheDb, "Cache & Broker", "Redis", "Semantic cache for frequent queries, rate-limit state, and Celery task queue.")
    }

    System_Ext(idp, "Identity Provider", "Okta / Azure AD")
    System_Ext(dataSources, "Data Sources", "SharePoint / S3 / Confluence")
    System_Ext(llm, "LLM Service", "OpenAI / Anthropic / vLLM")

    Rel(user, webUi, "Uses", "HTTPS")
    Rel(webUi, apiGateway, "API Requests", "HTTPS / SSE")
    Rel(apiGateway, idp, "Validates JWT", "REST")
    
    Rel(apiGateway, queryEngine, "Routes authenticated queries", "gRPC / HTTP")
    Rel(queryEngine, guardrails, "Validates input/output", "In-Process / HTTP")
    Rel(queryEngine, vectorDb, "Performs Hybrid Search w/ ACL filters", "gRPC")
    Rel(queryEngine, llm, "Sends context prompt for generation", "HTTPS")
    Rel(queryEngine, relationalDb, "Logs telemetry & sessions", "SQL")
    Rel(queryEngine, cacheDb, "Checks semantic cache", "RESP")

    Rel(dataSources, ingestionEngine, "Pulls raw documents", "CDC / Webhooks")
    Rel(ingestionEngine, cacheDb, "Pushes tasks to queue", "RESP")
    Rel(ingestionEngine, llm, "Generates document embeddings", "HTTPS")
    Rel(ingestionEngine, vectorDb, "Writes vectors + metadata ACLs", "gRPC")
```

## 3. Data Flow & Execution Sequences

### 3.1 Ingestion & Indexing Data Flow

```mermaid
sequenceDiagram
    autonumber
    participant DS as Data Source (SharePoint/S3)
    participant Worker as Ingestion Pipeline
    participant Parser as Layout Parser (LlamaParse/Unstructured)
    participant Redactor as PII Masking Engine
    participant Embedder as Embedding Model
    participant VectorDB as Vector Store (Qdrant/Milvus)

    DS->>Worker: Trigger Sync (Webhook / CDC Event)
    Worker->>Parser: Send Raw Document (PDF/Docx/HTML)
    Parser-->>Worker: Return Structured Markdown & Tables
    Worker->>Redactor: Scan & Redact Sensitive PII Data
    Redactor-->>Worker: Return Cleaned Text Chunks
    Worker->>Worker: Apply Parent-Child Chunking Strategy
    Worker->>Embedder: Batch Embed Chunks (e.g., text-embedding-3-large)
    Embedder-->>Worker: Return Vector Embeddings
    Worker->>VectorDB: Upsert Vectors + Metadata Payload (Doc ID, User ACLs, Timestamp)
    VectorDB-->>Worker: Acknowledge Indexing Complete
```

### 3.2 Query Processing & RAG Retrieval Sequence

```mermaid
sequenceDiagram
    autonumber
    participant User as User / Web Client
    participant GW as API Gateway & Auth
    participant QE as Query Engine
    participant Cache as Redis Semantic Cache
    participant VDB as Vector DB (Hybrid)
    participant Rerank as Re-Ranker (Cohere/BGE)
    participant LLM as LLM Provider

    User->>GW: POST /v1/query (Query + Bearer Token)
    GW->>GW: Validate JWT Token & Extract User Roles/Groups
    GW->>QE: Forward Query + User ACL Context
    QE->>Cache: Check Semantic Query Cache
    
    alt Cache Hit
        Cache-->>QE: Return Cached Answer & Citations
    else Cache Miss
        QE->>QE: Rewrite Query & Decompose Sub-Queries
        QE->>VDB: Execute Hybrid Search (Vector + BM25) + Filter (ACL IN UserGroups)
        VDB-->>QE: Return Top 50 Candidate Chunks
        QE->>Rerank: Re-rank Candidates against Original Query
        Rerank-->>QE: Return Top 5 Relevant Chunks
        QE->>LLM: Send System Prompt + Retrieved Context + Query
        LLM-->>QE: Stream Generated Answer + Citations
        QE->>Cache: Store Query-Answer Pair in Cache
    end
    
    QE-->>User: Stream Response (SSE) with Source Citations
```
