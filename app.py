import os
from app import create_app
from settings import Settings
from init import init_tools


init_tools()


app = create_app(Settings)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8091)
