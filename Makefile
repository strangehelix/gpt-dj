init:
	python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
start:
	uvicorn app.main:app --reload