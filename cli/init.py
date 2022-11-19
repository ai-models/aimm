import os
import sys
import typer

import aimmApp

app = aimmApp.app
@app.command()
def init():
    """
    Initialize aimodels.json.
    """
    typer.echo("Initializing...")
    # creates aimodels.json file if not existing in current directory
    if not os.path.exists("aimodels.json"):
        with open("aimodels.json", "w") as f:
            f.write('{}')
    else:
        typer.echo("Error: aimodels.json already exists")
        sys.exit(1)
    typer.echo("Made aimodels.json")
