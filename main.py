from fastapi import FastAPI, status

from api.core.config import APP_NAME, APP_VERSION, APP_DESCRIPTION, APP_ENV, ROUTE_PREFIX
from api.router import router

# Configure API documentation URLs based on environment
api_docs = {
    "openapi_url": (
        f"/{ROUTE_PREFIX}/openapi.json" if APP_ENV == "development" else None
    ),
    "docs_url": f"/{ROUTE_PREFIX}/docs" if APP_ENV == "development" else None,
    "redoc_url": f"/{ROUTE_PREFIX}/redoc" if APP_ENV == "development" else None,
}

# Initialize FastAPI application
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    **api_docs,
)

app.include_router(router)

@app.get("/", tags=["Default"])
def read_root():
    return dict(
        status_code=status.HTTP_200_OK,
        message=f"{APP_NAME} is running v{APP_VERSION}. Go to {api_docs['docs_url']} for API documentation.",
        result=None
    )
