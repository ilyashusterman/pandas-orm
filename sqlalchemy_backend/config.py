import os

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_URL = os.environ.get('DATABASE_URL', f'postgresql://docker:localone@{DB_HOST}:5432/local_database')