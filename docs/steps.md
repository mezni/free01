# Steps

## Step 0: Init project

Goal: A reproducible repo skeleton that anyone can clone and run

Problem: No structure, no tooling, hard for others to run

Solution (files): pyproject.toml, .python-version, src/, tests/test_smoke.py, .env.example, .gitignore, README.md stub, .github/workflows/ci.yml, ruff + pytest config

Trade-off: uv vs poetry: uv is faster and simpler, with one lockfile and no packaging ceremony. Code sits directly under src/ with no intermediate package name: pythonpath = ["src"] keeps pytest importing flat modules, and a small hatchling backend (package = true) installs them so `uv run python` imports `parsing`/`cleaning` anywhere. First tried package = false, which left `uv run python` unable to import src; making it installable fixes that at the cost of one build backend.

Example: uv run pytest → 1 passed

## Step 1: Corpus and domain scope

Goal: A small, realistic telecom document set plus a manifest that describes every document

Problem: Without realistic docs, retrieval looks fake in a portfolio. Without metadata (version, plan type, effective dates), you can’t filter stale answers later (step 7).

Solution (files): data/raw/{billing,roaming,plans,network}/*.md, data/manifest.json, data/README.md, tests/test_corpus.py, one-line fix in .gitignore

Trade-off: Synthetic docs (safe, controllable, no licensing) vs real operator docs (realistic, legal risk). Start with 5 short docs instead of 12: enough to test every later step, and you can grow the set. Markdown first (diffable in git). PDFs come in step 2 to exercise a second parser.

Example: make test → 5 passed

## Step 2: Parse and clean

Goal: Turn raw files (Markdown, text, PDF) into clean, structured blocks that keep their lineage (heading level, page)

Problem: Raw parsing leaves page numbers, repeated headers and footers, odd whitespace and ligatures. Without structure, chunking (step 3) can't cut on clause boundaries or cite a source.

Solution (files): src/core/models.py (Block), src/parsing/ (_blocks.py, markdown.py, text.py, pdf.py, registry.py), src/cleaning.py, tests/test_parsing.py, tests/test_cleaning.py, tests/test_pdf.py

Trade-off: Parsers take bytes, not a path, so they stay independent of where files come from (filesystem, API, database later). A new block starts at a heading, a clause number (2.1) or after a line ending in ., so clauses stay separate but a wrapped line that ends in a period will be split early. Cleaning drops any text found on 2 or more pages (headers, footers), which would also drop a genuine sentence repeated on two pages. pypdf is light and has no OCR, so scanned PDFs are out of scope. Heavier parsers like docling can replace it later behind the same registry.

Example: AW-ROA-002_roaming_policy_v2.md → heading(level=1) "AW-ROA-002 Roaming Policy (v2)", heading(level=2) "2. Zones", paragraph "2.1 Zone A covers …"