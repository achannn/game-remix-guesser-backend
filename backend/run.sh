#!/usr/bin/bash

set -a
source ../.dev.env
set +a

uvicorn app.main:app --reload --port=3000
