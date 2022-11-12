import aimm
import cli
import sys

WEBSITE = "https://aimodels.org"
API_SERVER = "https://api.aimodels.org"
PROGRAM_NAME = "aimm"

if __name__ == "__main__":
    # if no arguments are passed or if the first argument is "--help", print help
    if len(sys.argv) == 1 or sys.argv[1] == "--help":
        aimm.show_help(PROGRAM_NAME)
    else:
        aimm.app()