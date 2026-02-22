from dotenv import load_dotenv
load_dotenv()

from backend import create_app, db

app = create_app()

with app.app_context():
    from backend import models
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)