import json
import os
import sys

DEFAULT_DIR = "resources/actions/autocon"


def scan_json(path_to_file, key=None):
  with open(path_to_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
  return json_data[key]


def process_jsons():
  # for every json file run json_typing.py
  for file in os.listdir(f"{DEFAULT_DIR}/src"):
    if file.endswith('.json'):
      name = file.split('.json')[0]
      os.system(
        f'asciinema rec {DEFAULT_DIR}/src/{name}.asc -c "python3 {DEFAULT_DIR}/json_typing.py {DEFAULT_DIR}/src/{name}.json"')


def reset_env(path):
  setup = scan_json(path, 'setup-commands')

  # reset the terminal environment
  if os.path.exists("/home/runner/.local/share/aimm"):
    os.system("rm -fr /home/runner/.local/share/aimm")
  if os.path.exists("aimodels.json"):
    os.system("rm aimodels.json")
  if os.path.exists("aimodels-lock.json"):
    os.system("rm aimodels-lock.json")
  # if setup has values iterate through them
  if setup:
    for command in setup:
      os.system(command)
      print('setup command: ' + command)


def create_gifs():
  if not os.path.exists(f"{DEFAULT_DIR}/dist"):
    os.mkdir(f"{DEFAULT_DIR}/dist")
  for file in os.listdir(f"{DEFAULT_DIR}/src"):
    # run pre-setup commands
    if file.endswith('.asc'):
      name = file.split('.asc')[0]
      json_data = scan_json(f"{DEFAULT_DIR}/src/{name}.json", "config")
      reset_env(f'{DEFAULT_DIR}/src/{name}.json')
      os.system(
        f'./agg --rows=' + str(json_data['lines']) + f' {DEFAULT_DIR}/src/{name}.asc {DEFAULT_DIR}/dist/{name}.gif')


if __name__ == '__main__':
  # change working directory to the main directory
  os.chdir(os.path.dirname(os.path.abspath(__file__)))

  if len(sys.argv) >= 2:
    if sys.argv[1] == "asc":
      process_jsons()
    elif sys.argv[1] == "gif":
      create_gifs()
