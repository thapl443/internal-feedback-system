# --- Configuration ---
DB_COMPOSE  = docker-compose.db.yml
APP_COMPOSE = docker-compose.yml

# --- Colors ---
BLUE      := $(shell tput -Txterm setaf 4)
CYAN      := $(shell tput -Txterm setaf 6)
GREEN     := $(shell tput -Txterm setaf 2)
MAGENTA   := $(shell tput -Txterm setaf 5)
YELLOW    := $(shell tput -Txterm setaf 3)
WHITE     := $(shell tput -Txterm setaf 7)
RESET     := $(shell tput -Txterm sgr0)

# --- Emoji/Icons ---
ICON_DB   := 🐘
ICON_APP  := 🚀
ICON_DOWN := 🛑
ICON_LOG  := 📋
ICON_HELP := 💡

.PHONY: help db-up all-up down logs

## help: 💡 Show this fancy help menu
help:
	@echo ""
	@echo "  $(MAGENTA)Nexus Project Management$(RESET)"
	@echo "  $(WHITE)--------------------------$(RESET)"
	@echo "  Usage: $(CYAN)make$(RESET) $(YELLOW)<target>$(RESET)"
	@echo ""
	@echo "  $(WHITE)Available Commands:$(RESET)"
	@grep -E '^## [a-zA-Z_-]+:.*?.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "    $(CYAN)%-12s$(RESET) %s\n", $$1, $$2}'
	@echo ""

## db-up: 🐘 Start Database container only (Local Dev Mode)
db-up:
	@echo "$(BLUE)$(ICON_DB) Starting Database...$(RESET)"
	docker-compose -f $(DB_COMPOSE) up -d
	@echo "$(GREEN)✔ Database is ready!$(RESET)"

## all-up: 🚀 Build and start entire stack (Full Stack Mode)
all-up:
	@echo "$(MAGENTA)$(ICON_APP) Building and starting all services...$(RESET)"
	docker-compose -f $(DB_COMPOSE) -f $(APP_COMPOSE) up --build -d
	@echo "$(GREEN)✔ Full stack is up and running!$(RESET)"

## down: 🛑 Stop and remove all containers
down:
	@echo "$(YELLOW)$(ICON_DOWN) Stopping all services...$(RESET)"
	docker-compose -f $(DB_COMPOSE) -f $(APP_COMPOSE) down
	@echo "$(WHITE)✔ All containers removed.$(RESET)"

## logs: 📋 Stream all service logs
logs:
	@echo "$(CYAN)$(ICON_LOG) Attaching to logs...$(RESET)"
	docker-compose -f $(DB_COMPOSE) -f $(APP_COMPOSE) logs -f