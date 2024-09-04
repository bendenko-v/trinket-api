from loguru import logger
from starlette.responses import JSONResponse

from src.exceptions import (
    LoginError,
    NavigationError,
    TrinketCreationError,
    TrinketUpdateError,
    TrinketVerificationError,
)


def handle_exception(e: Exception) -> JSONResponse:
    match e:
        case LoginError():
            error_type = "Login error"
        case NavigationError():
            error_type = "Navigation error"
        case TrinketCreationError():
            error_type = "Trinket creation error"
        case TrinketUpdateError():
            error_type = "Trinket update error"
        case TrinketVerificationError():
            error_type = "Trinket verification error"
        case _:
            error_type = "Unexpected error"
            e = "An unexpected error occurred"

    logger.error(f"{error_type}: {e}")
    return JSONResponse(content={"error": str(e)}, status_code=500)
