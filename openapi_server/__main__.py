#!/usr/bin/env python3

import connexion

from app.db import init_db
from openapi_server.service_error_handlers import register_error_handlers
from openapi_server import encoder


def main():
    init_db()

    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Money Changer Web API'},
                pythonic_params=True)

    register_error_handlers(app.app)

    app.run(port=8080)


if __name__ == '__main__':
    main()
