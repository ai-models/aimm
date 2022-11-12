import os
import sys
import shutil
import json
from typing import Optional
import typer

import aimm
from cli import base_funcs as base_funcs

app = aimm.app
@app.command()
def uninstall(name_version: Optional[str] = typer.Argument(None)):
    """
    Uninstall an installed model.
    """
    name, version = base_funcs.extract_name_version(name_version)
    
    # check installed.json if multiple versions of name are installed, specify else uninstall
    if version is None:
        versions = []
        for package in aimm.installed["packages"]:
            if package["name"].lower() == name.lower():
                versions.append(package["version"])
        if len(versions) > 1:
            typer.echo(f"Multiple versions of {name} installed, please specify a version:")
            list()
            while True:
                version = input("Please enter version: ")
                if version in versions:
                    break
                else:
                    typer.echo("Invalid version")
            uninstall(f"{name}:{version}")
        elif len(versions) == 0:
            typer.echo(f"{name} not installed")
            sys.exit(1)
        else:
            version = versions[0]
            uninstall(f"{name}:{version}")
    else:
        # if installed is empty exit
        if aimm.installed["packages"] == []:
            typer.echo("Error: No packages installed")
            return
        else:
            for package in aimm.installed["packages"]:
                if name in package["name"] or package["version"] == version:
                    typer.echo(f"Uninstalling {name_version}...")
                
                    # update installed.json
                    for entry in aimm.installed["packages"]:
                        if entry["name"] == name and entry["version"] == version:
                            aimm.installed["packages"].remove(entry)
                    
                    with open(aimm.installed_json, "w") as file:
                        json.dump(aimm.installed, file, indent=4)
                    # remove the model
                    model_dir = os.path.join(aimm.main_dir, name)
                    try:
                        shutil.rmtree(model_dir  + "/" + version)
                    except Exception as e:
                        typer.echo(f"Error: {e}")
                        sys.exit(1)
                    typer.echo(f"Uninstalled {name_version}!")
                    deleted = True
        if not deleted:
            typer.echo(f"Error: {name_version} not found")
