import json
import os
import sys


DEFAULT_COMMAND = "asciinema rec"
DEFAULT_DIR = "resources/actions/autocon"

def scan_json(path_to_file,key=None):
    with open(path_to_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data[key]


if __name__ == '__main__':
    # delete directory /home/.runner/local/share/aimm
    # os.system(f"rm -rf /home/.runner/local/share/aimm")
    if len(sys.argv) >= 2:
        # change working directory to the main directory
        os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        # for every json file run json_typing.py
        if sys.argv[1] == "asc":
            for file in os.listdir(f"{DEFAULT_DIR}/src"):
                if file.endswith('.json'):
                    name = file.split('.json')[0]
                    os.system(f'{DEFAULT_COMMAND} {DEFAULT_DIR}/src/{name}.asc -c "python3 {DEFAULT_DIR}/json_typing.py {DEFAULT_DIR}/src/{name}.json"')
        elif sys.argv[1] == "gif":
            # make dist folder
            if not os.path.exists(f"{DEFAULT_DIR}/dist"):
                os.mkdir(f"{DEFAULT_DIR}/dist")
            for file in os.listdir(f"{DEFAULT_DIR}/src"):
                if file.endswith('.asc'):
                    name = file.split('.asc')[0]
                    # read the json file
                    json_data = scan_json(f"{DEFAULT_DIR}/src/{name}.json", "config")
                    os.system(f'./agg --rows='+str(json_data['lines'])+' {DEFAULT_DIR}/src/{name}.asc {DEFAULT_DIR}/dist/{name}.gif')