#!/bin/bash
set -e

echo "Submitting job..."
RESPONSE=$(curl -sf -X POST http://localhost:3000/submit)
echo "Response: $RESPONSE"
JOB_ID=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job ID: $JOB_ID"

echo "Polling for completion..."
for i in $(seq 1 20); do
  STATUS=$(curl -sf http://localhost:3000/status/$JOB_ID | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Attempt $i: $STATUS"
  if [ "$STATUS" = "completed" ]; then
    echo "Integration test PASSED"
    exit 0
  fi
  sleep 3
done

echo "Integration test FAILED - job never completed"
exit 1
