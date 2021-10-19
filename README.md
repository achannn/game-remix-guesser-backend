# Game Remix Guesser

## Development


Run backend on docker, and frontend in yarn, separate terminals.

In one terminal, do

```bash
cd backend
make dev
```

In another, do

```bash
cd frontend
yarn run dev
```


### Database Changes

There's no Alembic yet, so any changes that modify database tables (add / remove columns) require a tear-down of the docker volume. From the backend folder, do

```bash
docker volume ls
```

Look for volumes with `mysql` in the name. For each of those volumes, do

```bash
docker volume rm {volume_name}
```
