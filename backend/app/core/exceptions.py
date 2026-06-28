from typing import Any, Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: Optional[str] = None,
        details: Optional[Any] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code or self.__class__.__name__
        self.details = details
        super().__init__(message)


class AuthenticationError(AppException):
    def __init__(
        self,
        message: str = "Authentication failed",
        *,
        code: str = "AUTHENTICATION_ERROR",
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=code,
            details=details,
        )


class InvalidCredentialsError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid email or password",
            code="INVALID_CREDENTIALS",
        )


class InactiveUserError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__(
            message="User account is inactive or deleted",
            code="INACTIVE_USER",
        )


class TokenError(AuthenticationError):
    def __init__(self, message: str = "Invalid or expired token") -> None:
        super().__init__(message=message, code="TOKEN_ERROR")


class PermissionDeniedError(AppException):
    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            code="PERMISSION_DENIED",
        )


async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
    payload: dict[str, Any] = {"error": exc.code, "message": exc.message}
    if exc.details is not None:
        payload["details"] = exc.details
    return JSONResponse(status_code=exc.status_code, content=payload)
