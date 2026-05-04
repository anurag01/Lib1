#!/bin/sh
set -e

echo "Applying database migrations..."

attempt=1
max_attempts=20

while [ "$attempt" -le "$max_attempts" ]; do
  if alembic upgrade head; then
    echo "Migrations applied successfully."
    break
  fi

  echo "Migration attempt $attempt failed. Retrying in 3s..."
  attempt=$((attempt + 1))
  sleep 3
done

if [ "$attempt" -gt "$max_attempts" ]; then
  echo "Migration failed after $max_attempts attempts. Exiting."
  exit 1
fi

echo "Starting API server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
