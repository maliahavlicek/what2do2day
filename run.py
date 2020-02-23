import os
from what2do2day import app

if __name__ == '__main__':
    if not os.getenv("GOOGLE_MAP_KEY"):
        raise ValueError('GOOGLE_MAP_KEY environment variable is missing.')
    elif not os.getenv("MONGO_URI_WHAT2DO2DAY"):
        raise ValueError('MONGO_URI_WHAT2DO2DAY environment variable is missing.')
    elif not os.getenv("SECRET_KEY"):
        raise ValueError('SECRET_KEY environment variable is missing.')
    elif not os.getenv("WTF_CSRF_SECRET_KEY"):
        raise ValueError('WTF_CSRF_SECRET_KEY environment variable is missing.')
    else:
        app.run(host=os.getenv("IP", "0.0.0.0"),
                port=int(os.getenv("PORT", "5000")),
                debug=bool(os.getenv("DEBUG", True)))
