.PHONY: help build up down logs shell migrate collectstatic test clean

# Default target
help:
	@echo "Available commands:"
	@echo "  build        - Build Docker images"
	@echo "  up           - Start all services"
	@echo "  down         - Stop all services"
	@echo "  logs         - Show logs"
	@echo "  shell        - Open Django shell"
	@echo "  migrate      - Run database migrations"
	@echo "  collectstatic - Collect static files"
	@echo "  test         - Run tests"
	@echo "  clean        - Clean up containers and volumes"
	@echo "  dev          - Start development environment"
	@echo "  prod         - Start production environment"

# Development commands
dev:
	docker-compose -f docker-compose.dev.yml up -d

dev-build:
	docker-compose -f docker-compose.dev.yml build

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

dev-shell:
	docker-compose -f docker-compose.dev.yml exec web python manage.py shell

dev-migrate:
	docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

dev-collectstatic:
	docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput

# Production commands
prod:
	docker-compose up -d

prod-build:
	docker-compose build

prod-logs:
	docker-compose logs -f

prod-shell:
	docker-compose exec web python manage.py shell

prod-migrate:
	docker-compose exec web python manage.py migrate

prod-collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

# General commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

test:
	docker-compose exec web python manage.py test

clean:
	docker-compose down -v
	docker system prune -f

# Database commands
db-shell:
	docker-compose exec db psql -U networthtracker -d networthtracker

db-backup:
	docker-compose exec -T db pg_dump -U networthtracker networthtracker > backup_$(shell date +%Y%m%d_%H%M%S).sql

db-restore:
	docker-compose exec -T db psql -U networthtracker -d networthtracker < $(file)

# Utility commands
status:
	docker-compose ps

restart:
	docker-compose restart

restart-web:
	docker-compose restart web

# SSL commands
ssl-renew:
	docker-compose stop nginx
	sudo certbot renew
	docker-compose up -d nginx

# Monitoring
monitor:
	docker stats

health:
	curl -f http://localhost/ || echo "Application is not healthy" 