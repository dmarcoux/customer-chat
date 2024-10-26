# https://mcr.microsoft.com/en-us/artifact/mar/devcontainers/python
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Same as in .devcontainer/devcontainer.json
WORKDIR /workspaces

# Install sqlite CLI, see https://packages.debian.org/index for package names
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends sqlite3

# Install Python dependencies
COPY requirements.txt /tmp/pip-tmp/
RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp
