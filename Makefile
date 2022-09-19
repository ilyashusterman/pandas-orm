################################################################################
# Makefile for Pandas DB Repository : docker setup, commands, docker_build
################################################################################

# Prefer bash shell
export SHELL=/bin/bash
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
## Define repositories dependencies paths

## Make sure of current python path
export PYTHONPATH=$(pwd)

self := $(abspath $(lastword $(MAKEFILE_LIST)))
parent := $(dir $(self))

ifneq (,$(VERBOSE))
    override VERBOSE:=
else
    override VERBOSE:=@
endif

DATABASE_URL:="postgresql://docker:localone@localhost:5432/local_database"
DATABASE_DOCKER_URL:="postgresql://docker:localone@postgres_db_local:5432/local_database"
# functions
define save_db_file
    $(VERBOSE) docker-compose exec postgres_db_local bash -c 'pg_dump $(DATABASE_URL) --data-only --file=./docker_services/postgres/mock_db/temp_data.sql'
    $(VERBOSE) docker-compose exec postgres_db_local bash -c 'pg_dump $(DATABASE_URL) --schema-only --file=./docker_services/postgres/mock_db/temp_schema.sql'
endef

# docker build and params define
CWD := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
tag_version:="latest"


.PHONY: install
install:
	$(VERBOSE) pip install -r requirements.txt
.PHONY: initial_migrate
initial_migrate:
	$(VERBOSE) python database/migrations/main_manage.py db_version postgresql://docker:localone@localhost:5432/local_database database/migrations
.PHONY: connect_db
connect_db:
	$(VERBOSE) docker-compose run postgres_db_local bash -c 'psql $(DATABASE_DOCKER_URL)'
.PHONY: save_db
save_db:
	$(VERBOSE) $(call save_db_file)
.PHONY: start_db
start_db:
	$(VERBOSE) chmod +x docker_services/postgres/scripts/init-postgres.sh
	$(VERBOSE) docker-compose up postgres_db_local
.PHONY: install_mac_psycopg2
install_mac_psycopg2:
	$(VERBOSE) pip install psycopg2-binary
.PHONY: save_db_old
save_db_old:
	$(VERBOSE) pg_dump postgresql://docker:localone@localhost:5432/local_database --file=./docker_services/postgres/mock_db/temp.dump
.PHONY: save_db_data
save_db_data:
	$(VERBOSE) pg_dump postgresql://docker:localone@localhost:5432/local_database --data-only --file=./docker_services/postgres/mock_db/temp.dump
.PHONY: migrations
migrations:
	$(VERBOSE) python django_backend/manage.py makemigrations --name $(name)
.PHONY: migrate
migrate:
	$(VERBOSE) python manage.py migrate $(version)
	$(VERBOSE) $(call save_db_file)
.PHONY: migrate_version
migrate_version:
	$(VERBOSE) python manage.py migrate api $(version)
	$(VERBOSE) $(call save_db_file)
.PHONY: shutdown
shutdown:
	$(VERBOSE) docker-compose down
.PHONY: build_pkg
build_pkg:
	$(VERBOSE) python3 -m build
	$(VERBOSE) python3 -m twine upload --repository pypi dist/*
.PHONY: build_docs
build_docs:
	$(VERBOSE) export PYTHONPATH=$(pwd)/src && sphinx-build -b html source_docs/ docs/


