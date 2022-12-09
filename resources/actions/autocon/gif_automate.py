import json
import os
import sys

DEFAULT_DIR = "/home/runner/work/aimm/aimm/resources/actions/autocon"


def scan_json(path_to_file, key=None):
  with open(path_to_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
  if key in json_data:
    return json_data[key]


def process_jsons():
  # for every json file run json_typing.py
  for file in os.listdir(f"{DEFAULT_DIR}/src"):
    if file.endswith('.json'):
      name = file.split('.json')[0]
      print('resetting env')
      # reset the terminal environment
      if os.path.exists(f"/home/runner/.local/share/aimm"):
        os.system(f'rm -rf /home/runner/.local/share/aimm')
      if os.path.exists(f"aimodels.json"):
        os.remove(f"aimodels.json")
      if os.path.exists(f"aimodels-lock.json"):
        os.remove(f"aimodels-lock.json")
      # if setup has values iterate through them
      setup = scan_json(f"{DEFAULT_DIR}/src/{file}", 'setup-commands')
      if setup:
        print('running setup commands')
        for command in setup:
          os.system(command)
        print('setup commands complete')
      os.system(f'asciinema rec {DEFAULT_DIR}/src/{name}.asc -c "python3 {DEFAULT_DIR}/json_typing.py {DEFAULT_DIR}/src/{name}.json"')



def create_gifs():
  if not os.path.exists(f"{DEFAULT_DIR}/dist"):
    os.mkdir(f"{DEFAULT_DIR}/dist")
  for file in os.listdir(f"{DEFAULT_DIR}/src"):
    # run pre-setup commands
    if file.endswith('.asc'):
      name = file.split('.asc')[0]
      json_data = scan_json(f"{DEFAULT_DIR}/src/{name}.json", "config")
      os.system(
        f'./agg --rows=' + str(json_data['lines']) + f' {DEFAULT_DIR}/src/{name}.asc {DEFAULT_DIR}/dist/{name}.gif')


if __name__ == '__main__':
  if len(sys.argv) >= 2:
    if sys.argv[1] == "asc":
      process_jsons()
    elif sys.argv[1] == "gif":
      create_gifs()
