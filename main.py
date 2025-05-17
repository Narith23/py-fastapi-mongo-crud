from fastapi import FastAPI, status, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.core.config import APP_NAME, APP_VERSION, APP_DESCRIPTION, APP_ENV, ROUTE_PREFIX
from api.router import router
from api.utils.base_response import BaseResponse

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

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "message": exc.detail,
            "result": None
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = [
        {
            "field": ".".join(str(loc) for loc in err["loc"][1:]),  # skip "body" or "query"
            "message": err["msg"]
        }
        for err in errors
    ]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Validation failed",
            "result": formatted_errors
        }
    )

@app.get("/", tags=["Default"], response_model=BaseResponse[None])
def read_root():
    return dict(
        status_code=status.HTTP_200_OK,
        message=f"{APP_NAME} is running v{APP_VERSION}. Go to {api_docs['docs_url']} for API documentation.",
        result=None
    )
