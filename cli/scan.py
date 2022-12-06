import os
import hashlib
import json
import typer
from picklescan import scanner

from cli import aimmApp
from cli.base_funcs import extract_name_version, get_last_version

app = aimmApp.app

def hash_file(filename):
    hash_obj = hashlib.sha256()
    with open(filename, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            hash_obj.update(chunk)

    return hash_obj.hexdigest()

def get_model_path(name_version):
    name, version = extract_name_version(name_version)
    if version is None:
        version = get_last_version(name)
    for package in aimmApp.installed["packages"]:
        if package["name"].lower() == name.lower() and package["version"] == version:
            return package["paths"]
    else:
        typer.echo(f"Error: {name}:{version} not found")
        return None

def get_maximum_danger(result_globals) -> str:
    safety = None
    for module in result_globals:
        if safety is None:
            safety = module.safety
        elif safety.value < module.safety.value:
            safety = module.safety
    match safety:
        case scanner.SafetyLevel.Innocuous:
            safety = "innocuous"
        case scanner.SafetyLevel.Suspicious:
            safety = "suspicious"
        case scanner.SafetyLevel.Dangerous:
            safety = "dangerous"
    return safety

@app.command()
def scan(name_version: str, raw: bool = typer.Option(False, "--raw", "-r")):
    """
    Scan a file for malicious code.
    """
    model_path = get_model_path(name_version)
    if model_path:
        for file in os.listdir(model_path):
            path = os.path.join(model_path, file)
            result = scanner.scan_file_path(path)
            if not raw:
                print(f"Scanning {path}...")
                print(f"scanned files: {result.scanned_files}")
                print(f"issues count: {result.issues_count}")
                print(f"infected files: {result.infected_files}")
                print("safety level of modules:")
                for module in result.globals:
                    print(
                        f"  * {module.module}.{module.name} - {(module.safety.value).title()}")
                print(f"Hash: {hash_file(path)}")
            else:
                safety = get_maximum_danger(result.globals)
                print(json.dumps({
                    "hash": hash_file(path),
                    "picklescan": {
                        "scanned_files": result.scanned_files,
                        "issues_count": result.issues_count,
                        "infected_files": result.infected_files,
                        "safety_level": safety
                    }
                },indent=4))