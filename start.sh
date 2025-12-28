#!/bin/sh
echo "PORT is set to: '$PORT'"
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
