#!/bin/bash
echo Starting server
poetry run uvicorn app.main:app --workers 3 --host 0.0.0.0 --port 80
