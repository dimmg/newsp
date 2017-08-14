.PHONY: start

start:
	@docker-compose stop;
	@docker-compose build;
	@docker-compose up -d;


help:
	@echo 'start:'
	@echo '	Build and start containers'