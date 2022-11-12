import sys
import json
from urllib.request import urlopen
import typer

import main, aimm
from cli import base_funcs as base_funcs

app = aimm.app
@app.command()
def search(name: str, include_adult: bool = typer.Option(False, "--include-adult"), only_adult: bool = typer.Option(False, "--only-adult")):
    """
    Search for a model.
    """
    if not base_funcs.is_valid(name,None):
        typer.echo(f"Error: {name} not valid")
        sys.exit(1)
    url = f"{main.API_SERVER}/api/models?pagination[page]=1&pagination[pageSize]=5&populate[0]=version&filters[$or][0][model_name][$containsi]={name}&filters[$or][1][description][$containsi]={name}"
    # parse as json
    try:
        with urlopen(url) as response:
            data = json.loads(response.read())
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
    # if empty exit
    if len(data["data"]) == 0:
        typer.echo("No results found")
        sys.exit(1)
    # print the first 5 results
    count = 0
    typer.echo("Results:")
    if include_adult:
        for model in data["data"]:
            if count == 5:
                break
            model_name = model["attributes"]["model_name"]
            versions = model["attributes"]["version"]
            for item in versions:
                version = item['version_number']
                if item['adult']:
                    typer.echo(f"  {model_name}:{version} (Adult content)")
                else:
                    typer.echo(f"  {model_name}:{version}")
                typer.echo(f"    Size: {item['size']}  License: {item['license']}")
                typer.echo(f"    {main.WEBSITE}/models/{model['id']}")
                typer.echo(f"    {model['attributes']['description']}")
                typer.echo()
                count += 1
                
    elif only_adult:
        for model in data["data"]:
            if count == 5:
                break
            model_name = model["attributes"]["model_name"]
            versions = model["attributes"]["version"]
            for item in versions:
                version = item['version_number']
                if item['adult']:
                    typer.echo(f"  {model_name}:{version} (Adult content)")
                    typer.echo(f"    Size: {item['size']}  License: {item['license']}")
                    typer.echo(f"    {main.WEBSITE}/models/{model['id']}")
                    typer.echo(f"    {model['attributes']['description']}")
                    typer.echo()
                    count += 1
    else:
        for model in data["data"]:
            if count == 5:
                break
            model_name = model["attributes"]["model_name"]
            versions = model["attributes"]["version"]
            for item in versions:
                version = item['version_number']
                if not item['adult']:
                    typer.echo(f"  {model_name}:{version}")
                    typer.echo(f"    Size: {item['size']}  License: {item['license']}")
                    typer.echo(f"    {main.WEBSITE}/models/{model['id']}")
                    typer.echo(f"    {model['attributes']['description']}")
                    typer.echo()
                    count += 1
