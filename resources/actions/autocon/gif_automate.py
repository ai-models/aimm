import os

DEFAULT_COMMAND = "asciinema rec"
DEFAULT_DIR = "resources/actions/autocon"

if __name__ == '__main__':
    # change working directory to the main directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    # for every json file run json_typing.py
    for file in os.listdir(f"{DEFAULT_DIR}/src"):
        if file.endswith('.json'):
            name = file.split('.json')[0]
            os.system(f'{DEFAULT_COMMAND} {DEFAULT_DIR}/src/{name}.asc -c "python3 {DEFAULT_DIR}/json_typing.py {DEFAULT_DIR}/src/{name}.json"')
