import os
import sys
import json
import typer

import aimmApp
from cli import base_funcs
from cli import install as install

app = aimmApp.app
@app.command()
def add(name_version: str):
    """
    Add a model to local aimodels.json.
    """
    # if model not installed, install it
    # adds name as key and version as value to aimodels.json
    name, version = base_funcs.extract_name_version(name_version)
    
    # if aimodels.json doesn't exist exit
    if not os.path.exists("aimodels.json"):
        typer.echo("Error: aimodels.json not found, please run the aimm init")
        sys.exit(1)
    
    if base_funcs.should_install(name, version):
        install.install(name_version)
    else:
        typer.echo(f"{name}:{version} already installed.")
    
    # parse aimodels.json as a json
    try:
        with open("aimodels.json", "r") as f:
            aimodels = json.load(f)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
    
    # if version is not specified, get the latest version
    if version is None:
        version = base_funcs.get_last_version(name)
    
    # append name and version to aimodels.json if not already there
    add_it = True
    for package_name, package_version in aimodels.items():
        if package_name.lower() == name.lower() and package_version == version:
            typer.echo(f"{name}:{version} already added.")
            add_it = False
            return
    if add_it:
        aimodels.update({name: version})
        
        try:
            with open("aimodels.json", "w") as f:
                # prettify json
                json.dump(aimodels, f, indent=4)
        except Exception as e:
            typer.echo(f"Error: {e}")
            sys.exit(1)
        
        typer.echo(f"Added {name}:{version} to aimodels.json")
