import os
from what2do2day import app


if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")),
            debug=bool(os.getenv("DEBUG", True)))
