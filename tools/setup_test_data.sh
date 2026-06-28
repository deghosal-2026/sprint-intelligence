#!/bin/bash
set -e

echo "=== SprintSense Test Data Pipeline ==="

echo ""
echo "Step 1: Download raw data from 10 public repos..."
echo "  Requires GITHUB_TOKEN env var. This takes 15-30 minutes."
python tools/download_public_data.py

echo ""
echo "Step 2: Transform raw data → anonymized + fabricated sprints..."
python tools/transform_test_data.py

echo ""
echo "Step 3: Seed database..."
echo "  Requires DATABASE_URL env var (default: localhost:5432/sprintsense)."
python tools/seed_database.py

echo ""
echo "Step 4: Seed test users..."
python tools/seed_users.py

echo ""
echo "Step 5: Run Phase 2 compute..."
python -m poller --compute 2>/dev/null || echo "  (Poller not implemented yet — skip)"

echo ""
echo "=== Done ==="
echo "Verify with:"
echo "  docker compose exec db psql -U sprintsense -c 'SELECT COUNT(*) FROM issues;'"
echo "  docker compose exec db psql -U sprintsense -c 'SELECT COUNT(*) FROM sprints;'"
