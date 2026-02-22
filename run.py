from dotenv import load_dotenv
load_dotenv()

from backend import create_app, db

try:
    app = create_app()

    with app.app_context():
        from backend import models
        print("Connecting to database...", flush=True)
        db.create_all()
        print("Database connected and tables verified!", flush=True)
except Exception as e:
    import traceback, sys
    print("\n---------------- CRITICAL BOOT ERROR ----------------\n", flush=True)
    traceback.print_exc(file=sys.stdout)
    print("\n-----------------------------------------------------\n", flush=True)
    sys.stdout.flush()

if __name__ == "__main__":
    app.run(debug=True)