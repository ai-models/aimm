import sys
import json
from urllib.request import urlopen
import typer

import aimm
from cli import base_funcs as base_funcs, aimmApp

app = aimmApp.app
@app.command()
def search(name: str, include_adult: bool = typer.Option(False, "--include-adult"), only_adult: bool = typer.Option(False, "--only-adult")):
    """
    Search for a model.
    """
    if not base_funcs.is_valid(name,None):
        typer.echo(f"Error: {name} not valid")
        sys.exit(1)
    url = f"{aimm.API_SERVER}/api/models?pagination[page]=1&pagination[pageSize]=5&populate[0]=version&filters[$or][0][model_name][$containsi]={name}&filters[$or][1][description][$containsi]={name}"
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
    version_list = []
    typer.echo()
    typer.echo("Results:")
    if include_adult:
        for model in data["data"]:
            if count == 5:
                break
            model_name = model["attributes"]["model_name"]
            versions = model["attributes"]["version"]
            latest_ver = versions[-1]["version_number"]
            # only print the last version of every model
            for item in versions:
                version = item['version_number']
                if len(versions) > 1 and version != latest_ver:
                    version_list.append(item['version_number'])
            for item in versions:
                if item['version_number'] == latest_ver:
                    version = item['version_number']
                    if item['adult']:
                        typer.echo(f"  {model_name}:{version} (Adult content)")
                    else:
                        typer.echo(f"  {model_name}:{version}")
                    typer.echo(f"    Size: {item['size']}  License: {item['license']}")
                    typer.echo(f"    {main.WEBSITE}/m/{model_name}")
                    typer.echo(f"    {model['attributes']['description']}")
                    # print other versions in the same line
                    if len(versions) > 1:
                        typer.echo("    Other versions:")
                        typer.echo("      "+", ".join(list(set(version_list))))
                    count += 1
                
    elif only_adult:
        for model in data["data"]:
            if count == 5:
                break
            model_name = model["attributes"]["model_name"]
            versions = model["attributes"]["version"]
            latest_ver = versions[-1]["version_number"]
            all_versions_list = []
            # find the latest adult version
            # only print the last version of every model
            for item in versions:
                version = item['version_number']
                all_versions_list.append(version)
            for version in reversed(all_versions_list):
                for item in versions:
                    if item['version_number'] == version:
                        if item['adult']:
                            latest_adult_ver = item['version_number']
                            break
            for item in versions:
                if len(versions) > 1 and item['version_number'] != latest_adult_ver:
                    version_list.append(item['version_number'])
            for item in versions:
                if item['version_number'] == latest_adult_ver:
                    if item['adult']:
                        typer.echo(f"  {model_name}:{latest_adult_ver} (Adult content)")
                        typer.echo(f"    Size: {item['size']}  License: {item['license']}")
                        typer.echo(f"    {main.WEBSITE}/m/{model_name}")
                        typer.echo(f"    {model['attributes']['description']}")
                        # print other versions in the same line
                        if len(versions) > 1:
                            typer.echo("    Other versions:")
                            typer.echo("      "+", ".join(list(set(version_list))))
                        count += 1
    else:
        for model in data["data"]:
            if count == 5:
                break
            model_name = model["attributes"]["model_name"]
            versions = model["attributes"]["version"]
            latest_ver = versions[-1]["version_number"]
            # only print the last version of every model
            for item in versions:
                version = item['version_number']
                if len(versions) > 1 and version != latest_ver:
                    version_list.append(item['version_number'])
            for item in versions:
                if item['version_number'] == latest_ver:
                    version = item['version_number']
                    if not item['adult']:
                        typer.echo(f"  {model_name}:{version}")
                        typer.echo(f"    Size: {item['size']}  License: {item['license']}")
                        typer.echo(f"    {aimm.WEBSITE}/m/{model_name}")
                        typer.echo(f"    {model['attributes']['description']}")
                        # print other versions in the same line
                        if len(versions) > 1:
                            typer.echo("    Other versions:")
                            typer.echo("      "+", ".join(list(set(version_list))))
                        count += 1
