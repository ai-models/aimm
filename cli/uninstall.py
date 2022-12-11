import os
import sys
import shutil
import json
from typing import Optional
import typer

from cli import base_funcs as base_funcs, aimmApp

app = aimmApp.app
@app.command()
def uninstall(name_version: Optional[str] = typer.Argument(None)):
    """
    Uninstall an installed model.
    """
    if name_version is None:
        typer.echo("Usage: aimm uninstall [OPTIONS] NAME\n"
                   "Try 'aimm uninstall --help' for help.\n\n"
                   "Error: Missing argument 'NAME_VERSION'.")
        sys.exit(1)
    name, version = base_funcs.lowercase_name_version(name_version)
    
    # check installed.json if multiple versions of name are installed, specify else uninstall
    if version is None:
        versions = []
        for package in aimmApp.installed["packages"]:
            if package["name"].lower() == name:
                versions.append(package["version"])
        if len(versions) > 1:
            typer.echo(f"Multiple versions of {name} installed, please specify a version.")
            while True:
                typer.echo(f"Available versions: {versions}")
                input_version = input("Please enter version: ")
                if input_version in versions:
                    break
                typer.echo("Invalid version")
            uninstall(f"{name}:{input_version}")
        elif len(versions) == 0:
            typer.echo("Model package not installed")
            sys.exit(1)
        else:
            version = versions[0]
            uninstall(f"{name}:{version}")
    else:
        # if installed is empty exit
        if aimmApp.installed["packages"] == []:
            typer.echo("Error: No packages installed")
            return
        for package in aimmApp.installed["packages"]:
            if name in package["name"].lower() and package["version"] == version:
                model_dir = package["paths"]
                typer.echo(f'Uninstalling {package["name"]}:{package["version"]}')
                typer.echo(f'from {model_dir}...')
                try:
                    shutil.rmtree(model_dir)
                except Exception as e:
                    typer.echo(f"Error: {e}")
                    sys.exit(1)
                # update installed.json
                try:
                    aimmApp.installed["packages"].remove(package)
                except Exception as e:
                    typer.echo(f"Error: {e}")
                with open(aimmApp.installed_json, "w") as file:
                    json.dump(aimmApp.installed, file, indent=4)
                typer.echo(f"Uninstalled {package['name']}:{package['version']}!")
                
                deleted = True
        if not deleted:
            typer.echo(f"Error: Model not found")
