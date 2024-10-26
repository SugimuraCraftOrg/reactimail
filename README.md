# Run Local

## Configure Environment Files

```sh
cp .reactimail.template.env .reactimail.env
cp .postgres.template.env .postgres.env
```

## Up Containers

```sh
docker compose up -d
```
- access to http://localhost:18000

# The Containers

- postgres
- redis
- reactimail
