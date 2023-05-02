from fastapi.responses import JSONResponse
from fastapi import status, Request
from collections import defaultdict
from fastapi.exceptions import RequestValidationError
from fastapi_jwt_auth.exceptions import AuthJWTException, MissingTokenError

from main import app


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    why do we require?
    :To Display Error in Proper Format
    From This :
    {
    "detail": [
        {
            "loc": [
                "body",
                "user_name"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": [
                "body",
                "password"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": [
                "body",
                "email"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}

To This:
{
    "user_name": [
        "field required"
    ],
    "password": [
        "field required"
    ],
    "email": [
        "field required"
    ]
}
    """
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)  # nested fields with dot-notation
        reformatted_message[field_string].append(msg)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=reformatted_message)


@app.exception_handler(MissingTokenError)
def authjwt_exception_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
