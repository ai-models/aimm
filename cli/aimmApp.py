import os
import sys
import json
import requests
import typer
import appdirs
import piplicenses
# disable arguments from help
app = typer.Typer(no_args_is_help=True,
                  invoke_without_command=True, rich_markup_mode="rich")

config_dir = appdirs.user_config_dir(appauthor="visioninit", appname="aimm")

if not os.path.exists(config_dir):
    os.makedirs(config_dir)


main_dir = appdirs.user_data_dir(appauthor="visioninit", appname="aimm")

if not os.path.exists(main_dir):
    os.makedirs(main_dir)


installed_json = os.path.join(config_dir, "installed.json")
if not os.path.exists(installed_json):
    data = {"packages": []}
    try:
        with open(installed_json, "w") as f:
            f.write(json.dumps(data))
    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)

# parse installed_json as a json
try:
    with open(installed_json, "r") as f:
        installed = json.load(f)
except Exception as e:
    typer.echo(f"Error: {e}")
    sys.exit(1)


def show_help(program_name):
    print(f"Usage: {program_name} [command] [options]")
    print()
    print("Current Dir:")
    print("  init                                        Initialize aimodels.json.")
    print("  add <model_name>:[version]                  Add a model to aimodels.json.")
    print("  remove <model_name>:[version]               Remove a model from aimodels.json.")
    print()
    print("System Wide:")
    print("  list                                        List all models.")
    print("  info <model_name>:[version]                 Get info about a model.")
    print("  install <model_name>:[version]              Install a model.")
    print("  uninstall <model_name>:[version]            Uninstall a model.")
    print("  credentials <user>@<domain>                 Set credentials.")
    print()
    print("Search:")
    print("  search <query>                              Search for a model.")
    print("  search <query> --include-adult              Search for a model and include adult results.")
    print("  search <query> --only-adult                 Search for a model and only include adult results.")
    print()
    print("Options:")
    print("  -v, --version                 Show version.")
    print("  --check-update                Check for updates.")
    print("  --licenses                    Show licenses.")
    print("  --install-completion          Install completion for the current shell.")
    print("""  --show-completion             Show completion for the current shell, to copy it or customize
                                the installation.""")
    print("  --help                        Show this message and exit.")
    print()
    print(f"Run '{program_name} help [command]' for more information on a command.")
    sys.exit(0)


def check_for_updates(repo, current_version):
    # url = f"https://api.github.com/repos/{repo}/releases/latest"
    url = f"https://api.github.com/repos/{repo}/releases"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            latest_version = r.json()[0]["tag_name"]
            if latest_version != current_version:
                typer.echo(f"Update available: {current_version} → {latest_version}")
                typer.echo("  Latest version: https://github.com/visioninit/aimm/releases/latest")
            else:
                typer.echo("No updates available.")
        else:
            typer.echo(f"Error: {r.status_code}")
    except Exception as e:
        typer.echo(f"Error: {e}")


def show_licenses(verbose: bool = False):
    # check if running as a pyinstaller executable
    if getattr(sys, 'frozen', False):
        path = sys._MEIPASS
    else:
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    with open(os.path.join(path, "LICENSE"), "r") as f:
        print(f.read())
    if not verbose:
        os.system("pip-licenses -f plain -u --from all")
    else:
        os.system("pip-licenses -f plain-vertical -l --no-license-path -u --from all")
