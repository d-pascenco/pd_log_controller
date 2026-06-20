#!/bin/bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
streamlit run app/Home.py --server.address=0.0.0.0 --server.port=8501
