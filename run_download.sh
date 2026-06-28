#!/bin/zsh
# Run from project root:
#   zsh run_download.sh          → full download
#   zsh run_download.sh --test   → test: 1 repo, 2 weeks

export GITHUB_TOKEN=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

cd "$(dirname "$0")"
python3 -u tools/download_public_data.py "$@"
