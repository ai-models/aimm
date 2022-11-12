import os
import sys
import json
from urllib.request import urlopen
import re
import typer
import pretty_downloader

import main, aimm

def models_json(name, version):
    url = f"{main.API_SERVER}/api/models?filters[$and][0][version][version_number][$eqi]={version}&filters[$and][1][model_name][$eqi]={name}&publicationState=live&populate=deep"
    # parse api as a json
    try:
        with urlopen(url) as response:
            models = json.loads(response.read())
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
    return models

def download_file(url, path):
    try:
        pretty_downloader.download(url, path)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)

def should_install(name,version):
    for package in aimm.installed["packages"]:
        # make case insensitive
        if package["name"].lower() == name.lower() and package["version"] == version:
            return False
    return True

def is_valid(name, version):
    # check if name is valid with ^[\w-]+$
    # check if version is valid with ^[\w\.-]+$
    if version is None:
        if re.match(r"^[\w-]+$", name):
            return True
    if re.match(r"^[\w-]+$", name) and re.match(r"^[\w\.-]+$", version):
        return True
    else:
        return False

def extract_name_version(name_version):
    name = None
    version = None
    
    try:
        name = name_version.split(":")[0]
    except:
        pass
    try:
        version = name_version.split(":")[1]
    except:
        pass
    if name is not None and version is not None:
        if not is_valid(name, version):
            typer.echo("Invalid name or version")
            sys.exit(1)
    return name, version

def get_last_version(name):
    url = f"{main.API_SERVER}/api/models?filters[$and][0][model_name][$eqi]={name}&publicationState=live&populate=deep"
    # parse api as a json
    try:
        with urlopen(url) as response:
            models = json.loads(response.read())
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
    if len(models) == 0:
        typer.echo("No model found")
        sys.exit(1)
    # get last version
    try:
        version = models["data"][0]["attributes"]["version"][-1]["version_number"]
    except IndexError:
        typer.echo("Model not found in registry")
        sys.exit(1)
    
    return version

def is_adult(name):
    # check installed.json for name
    for package in aimm.installed["packages"]:
        if package["name"] == name:
            return package["adult"]

def is_path_valid(path):
    os.path.exists(path)
    
def hf_get_user() -> str:
    # get auth_user from user
    auth_user = typer.prompt("Huggingface username")
    return auth_user

def hf_get_pass() -> str:
    # get auth_pass from user
    auth_pass = typer.prompt("Huggingface password")
    return auth_pass

def gh_get_user() -> str:
    # get auth_user from user
    auth_user = typer.prompt("Github username")
    return auth_user

def gh_get_pass() -> str:
    # get auth_pass from user
    auth_pass = typer.prompt("Github password")
    return auth_pass