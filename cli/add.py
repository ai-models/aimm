import os
import sys
import json
from typing import Optional
import typer

from cli import base_funcs, aimmApp
from cli import install as install

app = aimmApp.app
@app.command()
def add(name_version: Optional[str] = typer.Argument(None), mut_path: bool = typer.Option(False, "--allow-mutable")):
    """
    Add a model to local aimodels.json.
    """
    if name_version is None:
        typer.echo("Usage: aimm add [OPTIONS] NAME\n"
                   "Try 'aimm add --help' for help.\n\n"
                   "Error: Missing argument 'NAME_VERSION'.")
        sys.exit(1)
    # if model not installed, install it
    # adds name as key and version as value to aimodels.json
    name, version = base_funcs.lowercase_name_version(name_version)
    if version is None:
        version = base_funcs.get_last_version(name)
    
    # if aimodels.json doesn't exist exit
    if not os.path.exists("aimodels.json"):
        typer.echo("Error: aimodels.json not found, please run the aimm init")
        sys.exit(1)
    
    if base_funcs.should_install(name, version):
        install.install(name_version,mut_path=mut_path)
        if install.header == True:
            sys.exit(1)
    # add to aimodels-lock.json
    save_path = os.path.join(aimmApp.main_dir, name, version)
    base_funcs.update_ai_models_lock(name, version, save_path, "add")
    
    # parse aimodels.json as a json
    try:
        with open("aimodels.json", "r") as f:
            aimodels = json.load(f)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
        
    # append name and version to aimodels.json if not already there
    add_it = True
    for package_name, package_version in aimodels.items():
        if package_name.lower() == name:
            for v in package_version:
                if v.lower() == version:
                    typer.echo(f"Already in aimodels.json: {name}:{version}")
                    add_it = False
                    return
    if add_it:
        # if the name is already there then add the version to the version list
        if name in aimodels:
            aimodels[name].append(version)
        else:
            aimodels[name] = [version]
        try:
            with open("aimodels.json", "w") as f:
                # prettify json
                json.dump(aimodels, f, indent=4)
        except Exception as e:
            typer.echo(f"Error: {e}")
            sys.exit(1)
        
        typer.echo(f"Added {name}:{version} to aimodels.json")
