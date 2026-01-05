from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from app.helpers.utils.encrypt import is_encryption_required


def validation_exception_handler(request:Request, exc: RequestValidationError):
    try:
        # print(exc)
        errors = []
        for error in exc.errors():
            error_messages = dict()
            field = error.get("loc")[-1]  # Get the field name
            if is_encryption_required(request.url.path):
                message = "Unauthorized request. Invalid credentials"
            else:
                msg = error.get("msg")
                message =  f"Invalid {field} - {msg}" # Get description

            error_messages["message"] = message
            errors.append(error_messages)

        if len(errors)==1:
            errors = errors[0]

        return JSONResponse(
            status_code=400,
            content={
                "error": True,
                "data": errors
            })
    except Exception as e:
        print(f"Error while handling validation error :: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={
                "error": True,
                "data": {
                    "message": f"Error while handling validation error :: {str(e)}"
                    }
            })
