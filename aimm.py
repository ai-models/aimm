import os
import sys
import json
import typer
import appdirs
# disable arguments from help
app = typer.Typer(no_args_is_help=True, invoke_without_command=True, rich_markup_mode="rich")

config_dir = appdirs.site_config_dir("aimm")

if not os.path.exists(config_dir):
    os.makedirs(config_dir)


main_dir = appdirs.site_data_dir("aimm")

if not os.path.exists(main_dir):
    os.makedirs(main_dir)


installed_json = os.path.join(config_dir, "installed.json")
if not os.path.exists(installed_json):
    data = {"packages":[]}
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
    print("  credentials <user>:<password>@<domain>      Set credentials.")
    print()
    print("Search:")
    print("  search <query>                              Search for a model.")
    print("  search <query> --include-adult              Search for a model and include adult results.")
    print("  search <query> --only-adult                 Search for a model and only include adult results.")
    print()
    print("Options:")
    print("  --install-completion          Install completion for the current shell.")
    print("""  --show-completion             Show completion for the current shell, to copy it or customize
                                the installation.""")
    print("  --help                        Show this message and exit.")
    print()
    print(f"Run '{program_name} help [command]' for more information on a command.")
    sys.exit(0)