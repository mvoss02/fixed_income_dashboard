.PHONY: run build-docker run-docker stop-docker ingest-data

# Default Python executable
PYTHON=python3

# Streamlit app file
APP_FILE=run.py

# Docker configuration
DOCKER_IMAGE=fixed-income-dashboard
DOCKER_TAG=latest
PORT=8501

# Run Streamlit locally
run:
	uv run streamlit run $(APP_FILE)

# Build Docker image
build-docker:
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

# Build Docker image on VM
build-docker-vm:
	docker buildx build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

# Run Docker container
run-docker: build-docker
	docker run \
		-p $(PORT):$(PORT) $(DOCKER_IMAGE):$(DOCKER_TAG)

# Run Docker container on VM
run-docker-vm: build-docker-vm
	docker run \
		-d \
		-p $(PORT):$(PORT) $(DOCKER_IMAGE):$(DOCKER_TAG)

# Stop all running containers of this image
stop-docker:
	docker ps -q --filter ancestor=$(DOCKER_IMAGE):$(DOCKER_TAG) | xargs -r docker stop

# Ingest data
ingest-data:
	@echo "Fetching all data..."
	python services/data_ingestion/fetch_bond_data.py

# Pytest tests
run-test:
	@echo "Running testing"
	pytest tests/test.py