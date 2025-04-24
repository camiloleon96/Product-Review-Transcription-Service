[uv docs](https://docs.astral.sh/uv/guides/integration/fastapi/#migrating-an-existing-fastapi-project)

run the fast api locally:

```
uv run fastapi dev
```

Build the Docker image with:

```
docker build -t fastapi-app .
```

Run the Docker container locally with:

```
docker run -p 8000:80 fastapi-app
```

# docker compose commands

```
docker-compose -f docker-compose.yaml build
docker-compose -f docker-compose.yaml up -d
docker-compose -f docker-compose.yaml down
```
