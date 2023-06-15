FROM node:latest AS build-vue

# Install node requirements
COPY web/package.json web/package-lock.json ./
RUN npm install

WORKDIR /build
COPY web /build

# Creates a non-root user with an explicit UID and adds permission to access the /build folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" builduser && chown -R builduser /build
USER builduser

RUN npm run build

#######################################################################
#######################################################################

FROM python:3-slim AS server

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY snakem /app/snakem
COPY --from=build-vue /build/dist /app/web

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

EXPOSE 9000/tcp

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "snakem.web.app:app", "--host", "0.0.0.0", "--port", "9000", "--log-level", "info"]
