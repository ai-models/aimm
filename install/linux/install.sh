echo "=-- [ AIMM Install ] -------------------------------------= "
echo "| This script will install the AI Model Manager on your   |"
echo "| system.                                                 |"
echo "=------------------------------------ [ by VisionInit ] --= "

echo "Install in /usr/local/bin? (y/n)"
read -r ans
while [ "$ans" != "y" ] && [ "$ans" != "n" ]; do
  echo "Invalid response. Please enter 'y' or 'n'."
  read -r ans
done
if [ "$ans" = "y" ]; then
  install_path=/usr/local/bin
else
  echo "Please enter the path to install to:"
  read -r path
  # Check if path exists, offer to create it if not
  if [ ! -d "$path" ]; then
    echo "Path does not exist. Create it? (y/n)"
    read -r ans
    while [ "$ans" != "y" ] && [ "$ans" != "n" ]; do
      echo "Invalid response. Please enter 'y' or 'n'."
      read -r ans
    done
    if [ "$ans" = "y" ]; then
      makepath=true
    else
      echo "Install cancelled."
      exit 1
    fi
  fi
fi

# Create path if necessary
if [ "$makepath" = true ]; then
  mkdir -p "$path"
  if [ $? -ne 0 ]; then
    echo "Failed to create path. Install cancelled."
    exit 1
  fi
fi

# download the latest version of the program
wget https://github.com/visioninit/ai-models-cli/suites/9396117503/artifacts/443295821 -O $install_path/aimm

# make the program executable
chmod +x $install_path/aimm

# check if folder is in $PATH
if [[ ":$PATH:" != *":$install_path:"* ]]; then
  echo "The install path is not in your \$PATH variable. Please add it to your \$PATH variable to use the program."
  echo "You can do this by adding the following line to your ~/.bashrc file:"
  echo "    export PATH=$install_path:\$PATH"
  echo ""
  echo "Note that this will not automatically update your path for the remainder of the session. To do this, you should run:"
  echo "    source ~/.bashrc"
  echo "    or"
  echo "    source ~/.profile"
fi
