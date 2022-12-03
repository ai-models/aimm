import os
import sys
import json
from urllib.request import urlopen
import re
import typer
import pretty_downloader

import aimm
from cli import aimmApp


def models_json(name, version):
    url = f"{aimm.API_SERVER}/api/models?filters[$and][0][version][version_number][$eqi]={version}&filters[$and][1][model_name][$eqi]={name}&publicationState=live&populate=deep"
    # parse api as a json
    try:
        with urlopen(url) as response:
            models = json.loads(response.read())
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
    return models

def download_file(url, path, auth_user=None, auth_pass=None):
    if auth_user:
        print(auth_user)
    if auth_pass:
        print(auth_pass)
    try:
        pretty_downloader.download(url, path)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)

def should_install(name,version):
    for package in aimmApp.installed["packages"]:
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
    url = f"{aimm.API_SERVER}/api/models?filters[$and][0][model_name][$eqi]={name}&publicationState=live&populate=deep"
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
    for package in aimmApp.installed["packages"]:
        if package["name"] == name:
            return package["adult"]

def is_path_valid(path):
    os.path.exists(path)
    
def get_user(download_url) -> str:
    # get auth_user from user
    domain = get_domain_from_url(download_url)
    domain = domain[0].upper() + domain[1:]
    auth_user = typer.prompt(f"{domain} username")
    return auth_user

def get_pass(download_url) -> str:
    # get auth_pass from user
    domain = get_domain_from_url(download_url)
    domain = domain[0].upper() + domain[1:]
    auth_pass = typer.prompt(f"{domain} password (Input is hidden)", hide_input=True)
    return auth_pass

def get_domain_from_url(download_url) -> str:
    # get domain from download_url
    if download_url.startswith("https://") or download_url.startswith("http://"):
        domain = download_url.split("/")[2]
    else:
        domain = download_url.split("/")[0]
    return domain

# a function that updates aimodels-lock.json
def update_ai_models_lock(name, version, path):
    # get current working directory
    cwd = os.getcwd()
    aimodels_lock_file = os.path.join(cwd, "aimodels-lock.json")
    # get a list of files in path
    files = os.listdir(path)
    # path should use forward slashes instead of backslashes
    path = path.replace("\\", "/")
    # check if aimodels-lock.json exists
    if not os.path.exists(aimodels_lock_file):
        # create aimodels-lock.json
        aimodels_lock = {
            "packages": {
                f"{name}:{version}": {
                    "path": path,
                    "files": files
                },
            "credentials": {}
            }
        }
        # write aimodels-lock.json
        with open("aimodels-lock.json", "w") as f:
            json.dump(aimodels_lock, f, indent=4)
    else:
        # read aimodels-lock.json
        with open("aimodels-lock.json", "r") as f:
            aimodels_lock = json.load(f)
        # check if name and version already exist if not append
        if f"{name}:{version}" not in aimodels_lock["packages"]:
            try:
                aimodels_lock["packages"][f"{name}:{version}"] = {
                    "path": path,
                    "files": files
                }
            except:
                typer.echo("Error: aimodels-lock.json is corrupted")
                sys.exit(1)
            # write aimodels-lock.json
            try:
                with open("aimodels-lock.json", "w") as f:
                    json.dump(aimodels_lock, f, indent=4)
            except Exception as e:
                typer.echo(f"Error: {e}")
                sys.exit(1)
                
        else:
            try:
                aimodels_lock["packages"][f"{name}:{version}"] = {
                    "path": path,
                    "files": files
                }
            except:
                typer.echo("Error: aimodels-lock.json is corrupted")
                sys.exit(1)
    # add to .gitignore
    gitignore_file = os.path.join(cwd, ".gitignore")
    gitignore_text = "# For local aimodels packages\naimodels-lock.json\n"
    if not os.path.exists(gitignore_file):
        with open(".gitignore", "w") as f:
            f.write(gitignore_text)
    else:
        with open(".gitignore", "r") as f:
            gitignore = f.read()
        if "aimodels-lock.json" not in gitignore:
            # append to end
            with open(".gitignore", "a") as f:
                f.write(gitignore_text)

def check_for_creds(download_url):
    domain = get_domain_from_url(download_url)
    
    # check if domain exists in aimodels-lock.json
    cwd = os.getcwd()
    aimodels_lock_file = os.path.join(cwd, "aimodels-lock.json")
    if not os.path.exists(aimodels_lock_file):
        return False
    else:
        with open("aimodels-lock.json", "r") as f:
            aimodels_lock = json.load(f)
        if domain in aimodels_lock["credentials"]:
            return True
        else:
            return False
        
def get_creds(download_url):
    domain = get_domain_from_url(download_url)
    
    # check if domain exists in aimodels-lock.json
    if check_for_creds(download_url):
        with open("aimodels-lock.json", "r") as f:
            aimodels_lock = json.load(f)
        # return username and password
        return aimodels_lock["credentials"][domain]["username"], aimodels_lock["credentials"][domain]["password"]

def get_model_path(name_version):
    name, version = extract_name_version(name_version)
    for package in aimmApp.installed["packages"]:
        if package["name"].lower() == name.lower() and package["version"] == version:
            return package["paths"]
    else:
        typer.echo(f"Error: {name}:{version} not found")
        return None