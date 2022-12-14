import sys
import json
import typer

from cli import base_funcs as base_funcs, aimmApp

app = aimmApp.app
# show default args
@app.command(context_settings={"show_default": True})
def info(name: str, fetch : bool = typer.Option(False, "--fetch", help="Fetch the latest info from the model repository")):
    """
    Show information about a model. 
    """
    if name is None:
        typer.echo("Usage: aimm info [OPTIONS] NAME\n"
                   "Try 'aimm info --help' for help.\n\n"
                   "Error: Missing argument 'NAME_VERSION'.")
        sys.exit(1)
    name = name.lower()
    if not base_funcs.is_valid(name,None):
        typer.echo(f"Error: {name} not valid")
        sys.exit(1)
    if fetch is False:
        # get the details from installed.json
        try:
            with open(aimmApp.installed_json, "r") as file:
                installed = json.load(file)
        except Exception as e:
            typer.echo(f"Error: {e}")
            sys.exit(1)
        for package in installed["packages"]:
            if package["name"] == name:
                if base_funcs.is_adult(name):
                    typer.echo(f"{name} [Installed] (Adult content)")
                else:
                    typer.echo(f"{name} [Installed]")
                typer.echo("  "+package["description"])
                typer.echo(f"  Current: {package['version']}")
                typer.echo(f"  Size: {package['size']}  License: {package['license']}")
                # if links is not empty
                if package["links"]:
                    typer.echo("  Links:")
                    for link in package["links"]:
                        # only show if url isn't None
                        if package['links'][link] is not None:
                            typer.echo(f"      {link} : {package['links'][link]}")
                break
        else:
            info(name,True)
        
    else:
        # get the last version
        version = base_funcs.get_last_version(name)
        # get details from api
        url = base_funcs.models_json(name,version)["data"][0]["attributes"]
        adult = False
        if url["version"][-1]["adult"]:
            adult = True
        # check if installed by checking name and version
        is_installed = False
        try:
            with open(aimmApp.installed_json, "r") as file:
                installed = json.load(file)
        except Exception as e:
            typer.echo(f"Error: {e}")
            sys.exit(1)
        for package in installed["packages"]:
            if package["name"] == name and package["version"] == version:
                is_installed = True
                
        if is_installed:
            if adult:
                typer.echo(f"{name} [Installed] (Adult content)")
            else:
                typer.echo(f"{name} [Installed]")
        else:
            if adult:
                typer.echo(f"{name} [Not Installed] (Adult content)")
            else:
                typer.echo(f"{name} [Not Installed]")
        # print the details
        typer.echo(f"  {url['description']}")
        typer.echo(f"  Current: {url['version'][-1]['version_number']}")
        typer.echo(f"  Size: {url['version'][-1]['size']}  License: {url['version'][-1]['license']}")
        # if links is not empty
        if url["links"]:
            typer.echo("  Links:")
            for link in url["links"]:
                if link != "id":
                    if url["links"][link] is not None:
                        typer.echo(f"      {link} : {url['links'][link]}")
