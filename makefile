SHELL := /bin/bash
.ONESHELL:

CYAN = \033[1;36m
GREEN = \033[1;32m
YELLOW = \033[1;33m
RED = \033[1;31m

RESET = \033[0m

.PHONY: .init-frontend .init-backend .init-docker init clean

clean:
	@echo -e "$(YELLOW)Removing make generated directories...$(RESET)"
	@deactivate 2>/dev/null || true
	@rm -rf ./venv ./frontend/node_modules  2>/dev/null || true

init:
	@echo -e "$(GREEN)Setting up the project...$(RESET)"
	@make -s .init-backend
	@make -s .init-frontend
	@make -s .init-docker
	@echo -e "$(GREEN)Setup complete! Run '$(CYAN)source ./venv/bin/activate$(RESET)$(GREEN)' and then $(RESET)'$(CYAN)make run$(RESET)$(GREEN)' to start the backend project.$(RESET)"


.init-frontend:
	@echo -e "$(GREEN)Setting up frontend npm deps...$(RESET)"
	@cd ./frontend && npm install -q
	@echo -e "$(GREEN)Frontend setup complete!$(RESET)"


.init-backend:
	@echo -e "$(GREEN)Setting up venv and installing python backend deps...$(RESET)"
	@deactivate 2>/dev/null || true
	@python3 -m venv --without-pip ./venv
	@source ./venv/bin/activate
	@echo -e "$(GREEN)Installing pip...$(RESET)"
	@curl -sSL https://bootstrap.pypa.io/get-pip.py | python3 - --index-url=https://pypi.org/simple/
	@deactivate 2>/dev/null || true
	@source ./venv/bin/activate
	@echo -e "$(GREEN)Installing backend python dependencies...$(RESET)"
	@python3 -m pip install -q --upgrade wheel setuptools pytest requests pytest-asyncio alembic ruff pre-commit poetry
	@cd ./backend && poetry install
	@pre-commit install
	@echo -e "$(GREEN)Backend setup complete!$(RESET)"

.init-docker:
	@echo -e "$(GREEN)Pulling docker base images...$(RESET)"
	@ecr 2>/dev/null 
	@docker compose pull database backend 2>/dev/null
	@echo -e "$(GREEN)Docker setup complete!$(RESET)"

run:
	@echo -e "$(GREEN)Starting the backend...$(RESET)"
	@docker compose up --build