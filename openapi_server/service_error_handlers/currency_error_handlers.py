from app.services.currency_service import CurrencyNotFoundError


def register_error_handlers(flask_app):
    flask_app.register_error_handler(
        CurrencyNotFoundError,
        currency_not_found,
    )


def currency_not_found(error):
    return {
        "code": "CURRENCY_NOT_FOUND",
        "message": str(error),
    }, 400
