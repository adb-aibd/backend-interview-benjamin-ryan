import os


class Config:
    PORT = int(os.getenv("PORT", "8080"))  # TODO: Validate
    DATABASE_URL = os.environ["DATABASE_URL"]
