set -a
source .env
set +a

if [ ${ENV} = "DEV" ]; then
    uvicorn app.main:app --reload --host=0.0.0.0 --port=8000
else
    gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind :${PORT}
fi
