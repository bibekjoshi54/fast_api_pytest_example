from pytest_example.entrypoint.rest_api.app import get_app

app = get_app()


if __name__ == "__main__":
    from hypercorn.config import Config

    config = Config()
    config.bind = ["localhost:8000"]
    config.debug = True
    import asyncio

    from hypercorn.asyncio import serve

    asyncio.run(serve(app, config))
