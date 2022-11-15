import os
import sys
import json
from typing import Optional
import typer

import aimm
from cli import base_funcs as base_funcs

app = aimm.app
@app.command()
# pass the user with argument --auth-user with the default value of none
def install(name_version: Optional[str] = typer.Argument(None),
            auth_user: Optional[str] = typer.Option(None, "--auth-user"),
            auth_pass: Optional[str] = typer.Option(None, "--auth-pass"),
            mut_path: bool = typer.Option(False, "--allow-mutable-paths")):
    """
    Install a model from the model repository.
    """
    
    # if no name_version is provided
    # go through aimodels.json and verify each item is installed and install if not
    if name_version is None:
        with open("aimodels.json", "r") as f:
            aimodels = json.load(f)
        # if doesn't contain any models exit
        if len(aimodels) == 0:
            typer.echo("No models in aimodels.json")
            sys.exit(1)
        for package_name, package_version in aimodels.items():
            name = package_name
            version = package_version
            if base_funcs.should_install(name, version):
                install(f"{name}:{version}", auth_user, auth_pass, mut_path)
            else:
                typer.echo(f"{name}:{version} already installed")
        return
    name, version = base_funcs.extract_name_version(name_version)
    
    if version is None:
        version = base_funcs.get_last_version(name)
        install(f"{name}:{version}", auth_user, auth_pass, mut_path)
        return

    if base_funcs.should_install(name, version):
        typer.echo(f"Installing {name}:{version}...")
        # download the model
        # if data doesn't have entries exit
        if base_funcs.models_json(name,version)["data"] == []:
            typer.echo(f"Error: {name}:{version} not found")
            sys.exit(1)
        url = base_funcs.models_json(name,version)["data"][0]["attributes"]
        name = url["model_name"]
        # if version doesn't match skip
        for item in url["version"]:
            if item['version_number'] != version:
                continue
            # update installed.json
            
            for file in item["files"]:
                # if doesn't exist exit
                if not file["download_url"]:
                    typer.echo(f"Error: Model {name}:{version} not found")
                    return
                # check if md5 exists
                # check if mut_path is passed 
                if not mut_path:
                    if not file["md5"]:
                        typer.echo(f"Error: {name}:{version}")
                        typer.echo("  Remote URL file could be changed and no checksum provided to validate file.")
                        sys.exit(1)
                
                save_path = os.path.join(aimm.main_dir, name, version)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                # if auth_required is set, check for creds
                if file["auth_required"]:
                    if auth_user is None or auth_pass is None:
                        if base_funcs.check_for_creds(file["download_url"]):
                            auth_user, auth_pass = base_funcs.get_creds(file["download_url"])
                            base_funcs.download_file(file["download_url"], save_path)
                        else:
                            typer.echo("No credentials passed or found in lock file.")
                            auth_user = base_funcs.get_user(file["download_url"])
                            auth_pass = base_funcs.get_pass(file["download_url"])
                # download the file
                if file["auth_required"]:
                    base_funcs.download_file(file["download_url"], save_path, auth_user, auth_pass)
                else:
                    base_funcs.download_file(file["download_url"], save_path)
                    
                # add to aimodels-lock.json
                base_funcs.update_ai_models_lock(name, version, save_path)
            # make a list of links
            links = []
            # only execute if there are links
            if url["links"]:
                for link in url["links"]:
                    # if link is not "id" and not None
                    if link != "id" and link is not None:
                        links.append(link)
            # add path to installed
            aimm.installed["packages"].append({"name":name, "version":version, "size":item["size"], "paths":save_path, "description":url["description"], "license":item["license"], "adult":item["adult"], "links":{}})
            # for every link add it to json only if not empty
            for link in links:
                if url["links"][link] is not None:
                    aimm.installed["packages"][-1]["links"][link] = url["links"][link]
            
            with open(aimm.installed_json, "w") as file:
                json.dump(aimm.installed, file, indent=4)
            typer.echo(f"Installed {name}:{version}!")
    else: 
        typer.echo(f"{name}:{version} already installed.")
