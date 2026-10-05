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

All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- Initial project scaffold.
EOF

# Reset README.md
cat << 'EOF' > README.md
# Project Name

A brief description of your project.
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


