set -a
source .env
set +a

if [ ${ENV} = "DEV" ]; then
    echo "Running dev environment"
    export GOOGLE_APPLICATION_CREDENTIALS="game-remix-guesser-a41630194599.json"
    uvicorn app.main:app --reload --host=0.0.0.0 --port=8000
else
    echo "Running prod environment"
    gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind :8080
fi
