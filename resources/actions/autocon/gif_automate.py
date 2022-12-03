# load overview.json into object
import json
import sys
import shutil
import os


# create a template function for each command
def autocon_build(filename):
  cwd = os.path.dirname(os.path.abspath(__file__))

  with open(cwd + '/src/' + filename) as f:
    commands = json.load(f)

  # rename gif_automate.sh filename.sh
  src = cwd + "/src/gif_automate.sh"
  print('src: '+src)
  print('cwd: '+cwd)

  dst = cwd + "/dist/"
  # make dst directory if it doesn't exist
  if not os.path.exists(dst):
    os.makedirs(dst)
  shutil.copy(src, dst + filename.replace(".json", ".sh"))

  prompt = '\[\e[0;38;5;232;107m\]agi\[\e[0;30;107m\]@\[\e[0;1;30;48;5;159m\]ai\[\e[0;1;38;5;232;48;5;255m\]models\[\e[0;7m\]:\[\e[0m\]~\[\e[0m\]\$\[\e[0m\]'

  output = 'DEFAULT_ECHO=' + prompt
  output += 'SCRIPT_PATH="aimm.py"'
  output += 'sleep .5'

  for ops in commands:
    if 'comment' in ops:
      output += 'echo -n -e "${DEFAULT_ECHO}"\n' \
                'sleep ' + str(ops['wait']) + '\n' \
                'sleep ' + str(ops['comment']) + '\n' \
                'sleep ' + str(ops['wait']) + '\n' \
                'typer ' + ops['command'] + '\n' \
                'echo\n' \
                'python3 $SCRIPT_PATH ' + str(ops['command']) + '\n'
    else:
      output += 'echo -n -e "${DEFAULT_ECHO}"\n' \
                'sleep ' + str(ops['wait']) + '\n' \
                'typer ' + ops['command'] + '\n' \
                'echo\n' \
                'python3 $SCRIPT_PATH ' + str(ops['command']) + '\n'

  output += 'typer "exit"'

  # append output to out.txt file
  with open(dst+ filename.replace(".json", ".sh"), "a") as f:
    f.write(output)

    # make the script executable
    os.chmod(dst+ filename.replace(".json", ".sh"), 0o755)


if __name__ == "__main__":
  cwod = os.path.dirname(os.path.abspath(__file__))

  # iterate through the json files in the src directory
  for file in os.listdir(cwod + '/src'):
    if file.endswith(".json"):
      autocon_build(file)
      continue
    else:
      continue
