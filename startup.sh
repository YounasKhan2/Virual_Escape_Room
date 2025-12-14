#!/bin/bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python database.py
gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
