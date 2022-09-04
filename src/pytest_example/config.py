from starlette.config import Config


config = Config()

CONFIG_AWS_ENDPOINT = config.get(
    "AWS_ENDPOINT", cast=str, default="http://localhost:20000"
)
