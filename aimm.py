import aimmApp, cli, sys

PROGRAM_NAME = "aimm"
WEBSITE = "https://aimodels.org"
API_SERVER = "https://api.aimodels.org"


def init():  # if no arguments are passed or if the first argument is "--help", print help
  if len(sys.argv) == 1 or sys.argv[1] == "--help":
    aimmApp.show_help(PROGRAM_NAME)
  else:
    aimmApp.app()


# if this file is run directly, run init()
if __name__ == "__main__": init()
