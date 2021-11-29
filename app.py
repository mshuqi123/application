import os
from app import create_app
from settings import Settings
from init import init_tools


init_tools()


app = create_app(Settings)


if __name__ == "__main__":
<<<<<<< HEAD
    app.run(host="0.0.0.0", port=8889)
=======
    app.run(host="0.0.0.0", port=8091)
>>>>>>> 831f755291aaeb7a161d9a6e31f35b1ed20a66c8
