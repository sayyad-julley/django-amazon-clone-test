#!/bin/bash
set -e
cd /workspace
pytest tests/playwright/ -v
