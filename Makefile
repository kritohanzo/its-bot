TAIL=100


define set-default-container
	ifndef c
	c = bot
	else ifeq (${c},all)
	override c=
	endif
endef


set-container:
	$(eval $(call set-default-container))


build:
	docker compose -f docker-compose.dev.yml build


compile-reqs: set-container
	docker compose -f docker-compose.dev.yml run --rm $(c) bash -c 'pip install pip-tools && uv pip compile pyproject.toml --no-emit-index-url -o requirements.txt'


up:
	docker compose -f docker-compose.dev.yml up --remove-orphans  -d $(c)
down:
	docker compose -f docker-compose.dev.yml down
logs: set-container
	docker compose -f docker-compose.dev.yml logs --tail=$(TAIL) -f $(c)
restart: set-container
	docker compose -f docker-compose.dev.yml restart $(c)


migrate: set-container
	docker compose -f docker-compose.dev.yml run --rm $(c) bash -c 'alembic upgrade head'
migrations: set-container
	docker compose -f docker-compose.dev.yml run --rm $(c) bash -c 'alembic revision --autogenerate'


pre-commit: set-container
	docker compose -f docker-compose.dev.yml run --rm $(c) bash -c 'PRE_COMMIT_HOME=.precomcache pre-commit run --all-files'
