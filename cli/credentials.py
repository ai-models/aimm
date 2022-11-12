import os
import sys
import json
import typer
import aimm

app = aimm.app
credentials_app = typer.Typer()
app.add_typer(credentials_app, name="credentials", help="Manage credentials in the app.")

credentials_json = os.path.join(aimm.config_dir, "passwords.json")


@credentials_app.command()
def add(username_domain: str):
    """
    Add a credential to the app. The format is user@domain
    """
    
    # example of argument: "user@domain"
    try:
        username, domain = username_domain.split("@")
    except Exception as e:
        typer.echo("The provided argument is not in the correct format. The format is user@domain")
        sys.exit(1)
        
    # if username and domain aren't empty ask for password
    if username and domain:
        typer.echo("Please enter your password (Input is hidden)")
        password = typer.prompt("Password", hide_input=True)
    else:
        typer.echo("The username or domain is not provided.")
        sys.exit(1)
    # check if passwords.json exists in the config directory
    if not os.path.exists(credentials_json):
        # create the file
        try:
            with open(credentials_json, "w") as f:
                f.write(json.dumps({}))
                
        except Exception as e:
            typer.echo(f"Error: {e}")
            sys.exit(1)
        
        typer.echo(f"Created {credentials_json}")
    # parse passwords.json as a json
    try:
        with open(credentials_json, "r") as f:
            passwords_json = json.load(f)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
    # add the credential to the json
    passwords_json.update({domain:{"username":username,"password":password}})
    # write the json to the file
    try:
        with open(credentials_json, "w") as f:
            f.write(json.dumps(passwords_json, indent=4))
        typer.echo(f"Added {domain} to {credentials_json}")
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)


@credentials_app.command()
def remove(username_domain: str):
    """
    Remove a credential from the app. The format is user@domain
    """
    
    # example of argument: "user@domain"
    username = username_domain.split("@")[0]
    domain = username_domain.split("@")[1]
    
    # check if passwords.json exists in the config directory
    if not os.path.exists(credentials_json):
        typer.echo(f"{credentials_json} does not exist.")
        sys.exit(1)
    # parse passwords.json as a json
    try:
        with open(credentials_json, "r") as f:
            passwords_json = json.load(f)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
    # remove the credential from the json
    for domain_ in passwords_json:
        if domain_ == domain:
            if passwords_json[domain_]["username"] == username:
                del passwords_json[domain_]
                break
    # write the json to the file
    try:
        with open(credentials_json, "w") as f:
            f.write(json.dumps(passwords_json, indent=4))
        typer.echo(f"Removed {domain} from {credentials_json}")
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
        

@credentials_app.command()
# argument can be either --show-password or --show-pass
def list(show_pass: bool = typer.Option(False, "--show-password", "--show-pass")):
    """
    List all credentials in the app.
    """

    # check if passwords.json exists in the config directory
    if not os.path.exists(credentials_json):
        typer.echo(f"{credentials_json} does not exist.")
        sys.exit(1)
    # parse passwords.json as a json
    try:
        with open(credentials_json, "r") as f:
            passwords_json = json.load(f)
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)
    # list the credentials
    typer.echo("Credentials:")
    for domain in passwords_json:
        username = passwords_json[domain]["username"]
        if show_pass:
            password = passwords_json[domain]["password"]
            typer.echo(f"  {username}:{password}@{domain}")
        else:
            typer.echo(f"  {username}@{domain}")