.PHONY: dev migrate_db seeds runserver format lint

# Start the development environment
dev:
	devcontainer up --workspace-folder . && devcontainer exec --workspace-folder . bash

# Migrate the database
migrate_db:
	python manage.py migrate

# Load database seeds
#
# This creates 3 users, all with the same password `supereasy`:
# - `admin` (Superuser for Django's admin)
# - `customer123` (Customer / `is_staff` set to `False`)
# - `agent123` (Customer Agent / `is_staff` set to `True`)
#
# In addition to users, a few support cases and messages are also created.
seeds:
	python manage.py loaddata seeds.json

# Run the development server on 0.0.0.0 to make it available outside the Docker container
#
# Accessible at http://localhost:8000, admin interface at http://localhost:8000/admin.
#
# Log in as one of the users listed above in the `seeds` target.
runserver:
	python manage.py runserver 0.0.0.0:8000

# Format the Python code
format:
	ruff format

# Lint the Python code
lint:
	ruff check --show-fixes --fix

# Run tests
tests:
	python manage.py test
