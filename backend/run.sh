set -a
source .env
set +a

if [ ${ENV} = "DEV" ]; then
    echo "Running dev environment"
    uvicorn app.main:static_app --reload --host=0.0.0.0 --port=8000
else
    echo "Running prod environment"
    uvicorn app.main:static_app --host=0.0.0.0 --port=80
fi
