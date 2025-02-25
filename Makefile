PROJECT_NAME := chatbot_backend
APP_MODULE := app.main
APP_INSTANCE := app
HOST := 0.0.0.0
PORT := 8000
DOCKER_COMPOSE := docker-compose
DOCKER_COMPOSE_FILE := docker-compose.yml

VENV_DIR := env
VENV_BIN := $(VENV_DIR)/bin
PYTHON := $(VENV_BIN)/python3
PIP := $(VENV_BIN)/pip3

.PHONY: setup venv install run run-prod stop test format check lint clean docker-up docker-down

setup: venv install docker-up

venv:
	@test -d "$(VENV_DIR)" || python -m venv "$(VENV_DIR)"

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@if ! test -d $(VENV_DIR)/lib/python3.12/site-packages/de_core_news_sm; then \
	    $(PYTHON) -m spacy download de_core_news_sm; \
	fi
	@if ! test -d ~/.cache/huggingface/hub/models--sentence-transformers--distiluse-base-multilingual-cased-v1; then \
	    $(PYTHON) -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('distiluse-base-multilingual-cased-v1')"; \
	fi

run: install docker-up
	uvicorn $(APP_MODULE):$(APP_INSTANCE) --host $(HOST) --port $(PORT) --reload

run-prod: install docker-up
	uvicorn $(APP_MODULE):$(APP_INSTANCE) --host $(HOST) --port $(PORT)

clean: docker-down
	@find . -name '__pycache__' -type d -exec rm -rf {} +
	@find . -name '*.pyc' -delete
	@rm -rf "$(VENV_DIR)"

docker-up:
	$(DOCKER_COMPOSE) -f "$(DOCKER_COMPOSE_FILE)" up -d

docker-down:
	$(DOCKER_COMPOSE) -f "$(DOCKER_COMPOSE_FILE)" down

ingest:
	$(PYTHON) app/scripts/ingest_data.py

