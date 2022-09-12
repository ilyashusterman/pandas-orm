#!/bin/bash

####################################
###     Local Setup Database     ###
####################################
set -e
set PGPASSWORD=password
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER docker PASSWORD 'localone';
    ALTER USER docker WITH SUPERUSER;
EOSQL

createdb --username "$POSTGRES_USER" local_database

psql -v ON_ERROR_STOP=1 --username docker --dbname local_database < /mock_db/temp_schema.sql
echo "Migrated schema finished successfully!"
psql -v ON_ERROR_STOP=1 --username docker --dbname local_database < /mock_db/temp_data.sql

echo "Setup local_database finished successfully!"