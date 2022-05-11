import uvicorn

from app.database import init_db
from app.setup import create_app

app = create_app()


init_db(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
