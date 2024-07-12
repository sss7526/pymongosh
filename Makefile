venv:
	python -m venv venv

install: venv
	. venv/bin/activate && pip install -r requirements.txt

run:
	. venv/bin/activate && python -m pymongosh

help:
	@echo "Available commands:"
	@echo "  venv      - Create a virtual environment"
	@echo "  install   - Activate the virtual environment and install dependencies"
	@echo "  run       - Run the pymongosh interactive shell"
	@echo "  help      - Display this help message"

.PHONY: venv install run help
