import aimmApp
import cli
import sys

WEBSITE = "https://aimodels.org"
API_SERVER = "https://api.aimodels.org"
PROGRAM_NAME = "aimm"

def init():    # if no arguments are passed or if the first argument is "--help", print help
    if len(sys.argv) == 1 or sys.argv[1] == "--help":
        aimmApp.show_help(PROGRAM_NAME)
    else:
        aimmApp.app()

#if this file is run directly
if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--help":
        aimmApp.show_help(PROGRAM_NAME)
    else:
        aimmApp.app()