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
                
                # check if download_url is huggingface.co
                if file["download_url"].startswith("https://huggingface.co/"):
                    # check if auth_user and auth_pass are strings
                    if not isinstance(auth_user, str) or not isinstance(auth_pass, str):
                    # if auth_user is None or auth_pass is None:
                        # check password.json for auth_user and auth_pass in config_dir
                        if os.path.exists(os.path.join(aimm.config_dir, "password.json")):
                            with open(os.path.join(aimm.config_dir, "password.json"), "r") as f:
                                password = json.load(f)
                            # if there's a huggingface entry get the creds
                            if password["huggingface.co"]:
                                if password["huggingface"]["username"] is None or password["huggingface"]["password"] is None:
                                    typer.echo("Error: Huggingface username or password is not properly set")
                                    return
                            else:
                                auth_user = base_funcs.hf_get_user()
                                auth_pass = base_funcs.hf_get_pass()
                        else:
                            auth_user = base_funcs.hf_get_user()
                            auth_pass = base_funcs.hf_get_pass()
                # check if download_url is github.com
                if file["download_url"].startswith("https://github.com/"):
                    # check if auth_user and auth_pass are provided
                    if auth_user is None or auth_pass is None:
                        # check password.json for auth_user and auth_pass in config_dir
                        if os.path.exists(os.path.join(aimm.config_dir, "password.json")):
                            with open(os.path.join(aimm.config_dir, "password.json"), "r") as f:
                                password = json.load(f)
                            # if there's a github entry get the creds
                            if password["github.com"]:
                                if password["github"]["username"] is None or password["github"]["password"] is None:
                                    typer.echo("Error: Github username or password is not properly set")
                                    return
                            else:
                                auth_user = base_funcs.gh_get_user()
                                auth_pass = base_funcs.gh_get_pass()
                        else:
                            auth_user = base_funcs.gh_get_user()
                            auth_pass = base_funcs.gh_get_pass()
                
                save_path = os.path.join(aimm.main_dir, name, version)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                base_funcs.download_file(file["download_url"], save_path)
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
