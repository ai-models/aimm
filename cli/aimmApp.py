import os
import sys
import subprocess
import json
import requests
import typer
import appdirs

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
    print("  add <model_name>:[version]                  Add a model to aimodels.json and installs it.")
    print("  remove <model_name>:[version]               Remove a model from aimodels.json (doesn't uninstall).")
    print("  install                                     Installs all models in aimodels.json to system")
    print("  credentials <user>@<domain>                 Set credentials for a domain.")
    print()
    print("System Wide:")
    print("  list                                        List all installed models.")
    print("  info <model_name>                           Get info about a model (name, version, description, etc).")
    print("  install <model_name>:[version]              Install a model to system.")
    print("  uninstall <model_name>:[version]            Uninstall a model.")
    print("  scan <model_name>:[version]                 Scan model for pickles and potential issues.")
    print()
    print("Search:")
    print("  search <query>                              Search for a model.")
    print("  search <query> --include-adult              Search for a model and include adult results.")
    print("  search <query> --only-adult                 Search for a model and only include adult results.")
    print()
    print("Options:")
    print("  -v, --version                 Show version.")
    print("  --check-update                Check for updates.")
    print("  --licenses                    Show licenses. --verbose for more info.")
    print("  --help                        Show this message and exit.")
    print()
    print(f"Run '{program_name} help [command]' for more information on a command.")
    sys.exit(0)


def check_for_updates(repo, current_version):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            latest_version = r.json()["tag_name"]
            if latest_version != current_version:
                typer.echo(f"Update available: {current_version} → {latest_version}")
                typer.echo(f"  Latest version: https://github.com/{repo}/releases/latest")
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
    # check if running as a python script
    elif __file__:
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # is running as pynsist
    else:
        path = sys.executable
        path = os.path.dirname(path)
    if sys.platform == "win32":
        temp = os.getenv("TEMP")
    elif sys.platform in ("linux", "darwin"):
        temp = "/tmp"
    license_file = os.path.join(temp, "aimm_licenses.txt")
    with open(license_file, "w") as aimm_licenses:
        with open(os.path.join(path, "LICENSE"), "r") as license_file:
            aimm_licenses.write(license_file.read())
        if not verbose:
            command = "pip-licenses -f plain -u --from all"
        else:
            command = "pip-licenses -f plain-vertical -l --no-license-path -u --from all"
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as popen:
            while True:
                retcode = popen.poll() 
                line = popen.stdout.readline()
                aimm_licenses.write(line.decode("utf-8"))
                if retcode is not None:
                    break
    os.system(f"more {aimm_licenses.name}") # show licenses with more