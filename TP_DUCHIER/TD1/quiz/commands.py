from .app import app, db

@app.cli.command()
def syncdb():
    """
    create all missing tables
    """
    db.create_all()