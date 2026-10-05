#!/usr/bin/env bash
set -euo pipefail

# 1. Remove all files except .gitignore, .git, README.md, and CHANGELOG.md
shopt -s dotglob
for file in *; do
  case "$file" in
    .gitignore|.git|README.md|CHANGELOG.md|scaffold.sh|".") ;;
    *) rm -rf "$file" ;;
  esac
done
shopt -u dotglob


>CHANGELOG.md
>README.md

# Reset CHANGELOG.md
cat << 'EOF' > CHANGELOG.md
# Changelog

All notable changes to `rag-system` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec.php#pec-2.0.0).

## Version History

| Version | Feature Domain | Key Objectives |
|---------|---------------|----------------|
| 0.0.1   | Project          | Scaffold|


## [0.0.1] - 2026-08-16

### Added
- **Project scaffold:** `pyproject.toml`, `.env.example`, `.gitignore`, `README.md`, test directory structure

EOF

# Reset README.md
cat << 'EOF' > README.md
# Project Name

A brief description of my project.
EOF


# 2. Initialize bare uv project
uv init --bare

# 3. Create virtual environment
uv venv


# 4. Create directories
mkdir -p src tests

# 5. Stage and commit changes
git add .
git commit -m "scaffold project"
git push


