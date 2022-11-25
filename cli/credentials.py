import os
import sys
import json
import typer
from cli import aimmApp

app = aimmApp.app
credentials_app = typer.Typer()
app.add_typer(credentials_app, name="credentials", help="Manage credentials in the app.")

# get current working directory
cwd = os.getcwd()
aimodels_lock_file = os.path.join(cwd, "aimodels-lock.json")

def parse_username_domain(username_domain) -> tuple:
    try:
        # the following works for email addresses too
        domain = username_domain.split("@")[-1]
        # remove domain from the end of string to get username
        username = username_domain[:-len(domain)-1]
    except Exception as e:
        typer.echo("The provided argument is not in the correct format. The format is user@domain")
        sys.exit(1)
    return username, domain

@credentials_app.command()
def add(username_domain: str):
    """
    Add a credential to the app. The format is user@domain
    """
    
    # example of argument: "user@domain"
    username, domain = parse_username_domain(username_domain)
        
    # if username and domain aren't empty ask for password
    if username and domain:
        typer.echo("Please enter your password (Input is hidden)")
        password = typer.prompt("Password", hide_input=True)
    else:
        typer.echo("The username or domain is not provided.")
        sys.exit(1)
    # check if aimodels-lock.json exists in the config directory
    init()
    # parse aimodels-lock.json as a json
    try:
        with open(aimodels_lock_file, "r") as f:
            passwords_json = json.load(f)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
    # add the credential to the json
    passwords_json["credentials"][domain] = {
        "username": username,
        "password": password
    }

    # write the json to the file
    try:
        with open(aimodels_lock_file, "w") as f:
            f.write(json.dumps(passwords_json, indent=4))
        typer.echo(f"Added {domain} to {aimodels_lock_file}")
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)


@credentials_app.command()
def remove(username_domain: str):
    """
    Remove a credential from the app. The format is user@domain
    """
    
    # example of argument: "user@domain"
    username, domain = parse_username_domain(username_domain)

    
    # check if aimodels-lock.json exists in the config directory
    if not os.path.exists(aimodels_lock_file):
        typer.echo(f"{aimodels_lock_file} does not exist.")
        sys.exit(1)
    # parse aimodels-lock.json as a json
    try:
        with open(aimodels_lock_file, "r") as f:
            passwords_json = json.load(f)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
    # remove the credential from the json
    try:
        del passwords_json["credentials"][domain]
    except KeyError:
        typer.echo(f"{domain} does not exist in {aimodels_lock_file}")
        sys.exit(1)
    # write the json to the file
    try:
        with open(aimodels_lock_file, "w") as f:
            f.write(json.dumps(passwords_json, indent=4))
        typer.echo(f"Removed {domain} from {aimodels_lock_file}")
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
        

@credentials_app.command()
# argument can be either --show-password or --show-pass
def list(show_pass: bool = typer.Option(False, "--show-password", "--show-pass")):
    """
    List all credentials in the app.
    """

    # check if aimodels-lock.json exists in the config directory
    if not os.path.exists(aimodels_lock_file):
        typer.echo(f"{aimodels_lock_file} does not exist.")
        sys.exit(1)
    # parse aimodels-lock.json as a json
    try:
        with open(aimodels_lock_file, "r") as f:
            passwords_json = json.load(f)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
    # list the credentials only if there are any
    try:
        if passwords_json["credentials"]:
            typer.echo()
            typer.echo("Credentials:")
            for _domain in passwords_json["credentials"]:
                if show_pass:
                    typer.echo(f"  {_domain}: {passwords_json['credentials'][_domain]['username']}:{passwords_json['credentials'][_domain]['password']}")
                else:
                    typer.echo(f"  {_domain}: {passwords_json['credentials'][_domain]['username']}")
        else:
            typer.echo("No credentials found.")
    except KeyError:
        typer.echo("No credentials found.")
        sys.exit(1)
        
            
def init():
    default_json = {
        "packages": {},
        "credentials": {}
        }
    # check if aimodels-lock.json exists in the current directory
    if not os.path.exists(aimodels_lock_file):
        # create the file
        try:
            with open(aimodels_lock_file, "w") as f:
                f.write(json.dumps(default_json))
                
        except Exception as e:
            typer.echo(f"Error: {e}")
            sys.exit(1)
        
        typer.echo(f"Created {aimodels_lock_file}")