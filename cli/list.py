import os

import prettytable
import typer
from prettytable import PrettyTable

from cli import aimmApp

app = aimmApp.app
@app.command()
def list():
    """
    List all installed models.
    """
    typer.echo("Installed models:")
    # get main_dir value from aimmApp
    main_dir = aimmApp.main_dir.replace(os.path.expanduser("~"), "~")

    # show installed packages' name, version, size and path in a table format
    table = PrettyTable(['Name', 'Version', 'Size', f'Base Path: {main_dir}'])
    table.set_style(prettytable.SINGLE_BORDER)
    table.align = "l"
    table.align["Version"] = "r"
    table.align["Size"] = "r"
    for package in aimmApp.installed["packages"]:
        # edit path to show relative path to main_dir
        paths = package["paths"].replace(aimmApp.main_dir, "")
        table.add_row([package["name"], package["version"], package["size"], paths])

    typer.echo(table)
