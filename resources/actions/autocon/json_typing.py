import json
import os
import sys
import time

USERNAME="user"
HOSTNAME="aimodels"
DEFAULT_ECHO= f"[{USERNAME}@{HOSTNAME}]$ "

DEFAULT_DIR = "/home/runner/work/aimm/aimm/resources/actions/autocon"

def reset_env(file):
    # reset the terminal environment
    if os.path.exists(f"/home/runner/.local/share/aimm"):
        os.system(f'rm -rf /home/runner/.local/share/aimm')
    if os.path.exists(f"aimodels.json"):
        os.remove(f"aimodels.json")
    if os.path.exists(f"aimodels-lock.json"):
        os.remove(f"aimodels-lock.json")
    print('resetting env')
    # if setup has values iterate through them
    setup = scan_json(f"{DEFAULT_DIR}/src/{file}", 'setup-commands')
    if setup:
        print('running setup commands')
        for command in setup:
            os.system(command)
        print('setup commands complete')


def typing_effect(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.08)

def scan_json(path_to_file,key=None):
    with open(path_to_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    if key in json_data:
        return json_data[key]

def print_data(json_data):
    print('AIMM Demo')
    for entry in json_data:
        if 'comment' in entry:
            # comments should be gray
            typing_effect('# ' + entry['comment'] +'\n')
        else:
            print()
        print(DEFAULT_ECHO, end='')
        typing_effect(entry['command'] + '\n')
        # if command begins with aimm then it is a command
        if entry['command'].startswith('aimm'):
            command = entry['command'].split('aimm')[1]
            os.system(f'python3 aimm.py {command}')
        else:
            os.system(entry['command'])
        print()
        print(DEFAULT_ECHO, end='', flush=True)
        time.sleep(entry['wait'])
    typing_effect('# End of Example\n')
    time.sleep(3)

arguments = sys.argv
if len(arguments) >= 2:
    path = arguments[1]
    reset_env(path)
    data = scan_json(path,'commands')
    print_data(data)

