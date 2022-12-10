import os
import sys
import json
from typing import Optional
import typer

from cli import base_funcs as base_funcs, aimmApp, security
unsafe,header=[False]*2

app = aimmApp.app
@app.command()
# pass the user with argument --auth-user with the default value of none
def install(name_version: Optional[str] = typer.Argument(None),
            auth_user: Optional[str] = typer.Option(None, "--auth-user"),
            auth_pass: Optional[str] = typer.Option(None, "--auth-pass"),
            mut_path: bool = typer.Option(False, "--unsafe-url")):
    """
    Install a model from the model repository.
    """
    global header,unsafe
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
                installed=True
            else:
                typer.echo(f"{name}:{version} already installed")
        if unsafe:
            typer.echo("   To allow mutable files, run command again with argument:\n"+
            "\t --allow-mutable-paths")
        return
    name, version = base_funcs.extract_name_version(name_version)
    
    if version is None:
        version = base_funcs.get_last_version(name)
        install(f"{name}:{version}", auth_user, auth_pass, mut_path)
        return

    if base_funcs.should_install(name, version):
        if not header:
            typer.echo(f"Install Pre-Check: {name}:{version}...")
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
            # check if download_urls are safe
            if not mut_path:
                unsafe_urls = []
                for file in item["files"]:
                    if not security.is_url_safe(file["download_url"]):
                        unsafe_urls.append(file["download_url"])
                        unsafe=True
                if unsafe_urls:
                    if not header:
                        typer.echo("Error: Unverifiable download path in request")
                        typer.echo("  * Remote file is mutable\n" +
                                    "    Immutable download paths always point to the same file. In cases\n" +
                                    "    where the file is mutable, the file could be changed.\n\n" +
                                    "    Example of immutable paths:\n" +
                                    "    - github.com/{user}/{repo_name}/tree/{commit_hash}\n" +
                                    "    - huggingface.co/spaces/{space_name}/{repo_name}/tree/{commit_hash}\n\n" +
                                    "    Mutable paths in your request:")
                        
                        header=True
                    typer.echo(f"    - {name}:{version}")
                    for url in unsafe_urls:
                        typer.echo(f"      {url}")
                    typer.echo()
                    continue
            if not unsafe:
                for file in item["files"]:
                    # if doesn't exist exit
                    if not file["download_url"]:
                        typer.echo(f"Error: Model {name}:{version} not found")
                        return
                    
                    save_path = os.path.join(aimmApp.main_dir, name.lower(), version.lower())
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
                aimmApp.installed["packages"].append({"name":name, "version":version, "size":item["size"], "paths":save_path, "description":url["description"], "license":item["license"], "adult":item["adult"], "links":{}})
                # for every link add it to json only if not empty
                for link in links:
                    if url["links"][link] is not None:
                        aimmApp.installed["packages"][-1]["links"][link] = url["links"][link]
                
                with open(aimmApp.installed_json, "w") as file:
                    json.dump(aimmApp.installed, file, indent=4)
                typer.echo(f"Installed {name}:{version}!")
    else: 
        save_path = os.path.join(aimmApp.main_dir, name.lower(), version.lower())
        base_funcs.update_ai_models_lock(name, version, save_path)
        typer.echo(f"Found Local: {name}:{version}")
