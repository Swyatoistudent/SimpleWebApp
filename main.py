from flaskr import create_app
from flaskr import init_db
import click
app=create_app()

@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    click.echo("Initialized the database.")
if __name__=="__main__":
    app.run()
