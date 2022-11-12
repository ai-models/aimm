import typer
from prettytable import PrettyTable

import aimm
from cli import base_funcs as base_funcs

app = aimm.app
@app.command()
def list():
    """
    List all installed models.
    """
    typer.echo("Installed models:")
    # show installed packages' name, version, size and path in a table format
    table = PrettyTable(['Name', 'Version', 'Size', 'Path'])

    for package in aimm.installed["packages"]:
        # add another entry if more than one path
        table.add_row([package["name"], package["version"], package["size"], package["paths"]])
    
    typer.echo(table)
