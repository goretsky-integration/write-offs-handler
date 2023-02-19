from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

import exceptions

__all__ = ('include_exception_handlers',)


def on_unit_not_found_exception(request: Request, exc: exceptions.UnitNotFound) -> JSONResponse:
    return JSONResponse(
        content={'detail': 'Unit is not found'},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=exceptions.UnitNotFound,
        handler=on_unit_not_found_exception,
    )
