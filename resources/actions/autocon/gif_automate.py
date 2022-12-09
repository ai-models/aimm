import json
import os
import subprocess
import sys

DEFAULT_DIR = "/home/runner/work/aimm/aimm/resources/actions/autocon"


def scan_json(path_to_file, key=None):
  with open(path_to_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
  if key in json_data:
    return json_data[key]


def reset_env(path):
  print('resetting env')
  # reset the terminal environment
  # if exist
  if os.path.exists(f"/home/runner/.local/share/aimm"):
    subprocess.run(["rm", "-fr", "/home/runner/.local/share/aimm"])
  # if exist aimodels.json
  if os.path.exists(f"aimodels.json"):
    subprocess.run(["rm", "aimodels.json"])
  if os.path.exists(f"aimodels-lock.json"):
    subprocess.run(["rm", "aimodels-lock.json"])
  # if setup has values iterate through them
  setup = scan_json(path, 'setup-commands')
  if setup:
    print('running setup commands')
    for command in setup:
      os.system(command)
    print('setup commands complete')

def process_jsons():
  # for every json file run json_typing.py
  for file in os.listdir(f"{DEFAULT_DIR}/src"):
    if file.endswith('.json'):
      name = file.split('.json')[0]
      reset_env(f'{DEFAULT_DIR}/src/{name}.json')
      print('recording..')
      subprocess.run(["asciinema", "rec", "{DEFAULT_DIR}/src/{name}.asc", "-c", "python3 json_typing.py", f"{DEFAULT_DIR}/src/{name}.json"])



def create_gifs():
  if not os.path.exists(f"{DEFAULT_DIR}/dist"):
    os.mkdir(f"{DEFAULT_DIR}/dist")
  for file in os.listdir(f"{DEFAULT_DIR}/src"):
    # run pre-setup commands
    if file.endswith('.asc'):
      name = file.split('.asc')[0]
      json_data = scan_json(f"{DEFAULT_DIR}/src/{name}.json", "config")
      subprocess.run("./agg", f"--rows={json_data['lines']}", f"{DEFAULT_DIR}/src/{name}.asc", f"{DEFAULT_DIR}/dist/{name}.gif")

if __name__ == '__main__':
  if len(sys.argv) >= 2:
    if sys.argv[1] == "asc":
      process_jsons()
    elif sys.argv[1] == "gif":
      create_gifs()
