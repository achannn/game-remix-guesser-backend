dev:
	docker-compose -f docker-compose.yml up --build

test:
	 docker-compose -f docker-compose.yml up -d --build
