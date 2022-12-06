import prettytable
import typer
from prettytable import PrettyTable

from cli import base_funcs as base_funcs, aimmApp

app = aimmApp.app
@app.command()
def list():
    """
    List all installed models.
    """
    typer.echo("Installed models:")
    # show installed packages' name, version, size and path in a table format
    table = PrettyTable(['Name', 'Version', 'Size', 'Path'])
    table.set_style(prettytable.SINGLE_BORDER)
    table.align = "l"
    table.align["Version"] = "r"
    table.align["Size"] = "r"
    for package in aimmApp.installed["packages"]:
        # add another entry if more than one path
        table.add_row([package["name"], package["version"], package["size"], package["paths"]])
    
    typer.echo(table)
