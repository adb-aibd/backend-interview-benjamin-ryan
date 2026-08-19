from app.services.exchange_rate_service import SameCurrencyError


def register_error_handlers(flask_app):
    flask_app.register_error_handler(
        SameCurrencyError,
        handle_same_currency_error,
    )


def handle_same_currency_error(error):
    return {
        "code": "SAME_CURRENCY",
        "message": "Base and quote currencies must differ.",
    }, 400
