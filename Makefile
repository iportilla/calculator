IMAGE_NAME=mcp-calculator
CONTAINER_NAME=mcp-calculator-server
PORT=8000

.PHONY: build run stop logs clean help

help:
	@echo "Makefile targets:"
	@echo "  build    Build the Docker image"
	@echo "  run      Run the container in detached mode on port $(PORT)"
	@echo "  stop     Stop and remove the container"
	@echo "  logs     Show container logs"
	@echo "  clean    Remove the image"

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) --rm $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME) || true

logs:
	docker logs -f $(CONTAINER_NAME)

clean:
	docker rmi $(IMAGE_NAME) || true
