#!/usr/bin/env bash

typer() {
    for (( i=0; i<${#1}; i++ )); do
        echo -n "${1:$i:1}"
        sleep 0.08
    done
}

USERNAME="user"
HOSTNAME="aimodels"
FOLDER="aimm"
DEFAULT_ECHO="\n[${USERNAME}@${HOSTNAME} ${FOLDER}]$ "

SCRIPT_PATH="aimm.py"

WAIT_INITIAL=0.5
WAIT_COMMANDS=1

FIRST_MODEL="BSRGAN"
SECOND_MODEL="StableDiffusion"

# RECORD START
sleep $WAIT_INITIAL
echo -n -e "${DEFAULT_ECHO}"
sleep $WAIT_COMMANDS
typer "aimm init"
echo
python3 $SCRIPT_PATH init 
echo -n -e "${DEFAULT_ECHO}"
sleep $WAIT_COMMANDS
typer "aimm search $FIRST_MODEL"
echo
python3 $SCRIPT_PATH search $FIRST_MODEL 
echo -n -e "${DEFAULT_ECHO}"
sleep $WAIT_COMMANDS
typer "aimm add $FIRST_MODEL"
echo
python3 $SCRIPT_PATH add $FIRST_MODEL 
echo -n -e "${DEFAULT_ECHO}"
sleep $WAIT_COMMANDS
typer "cat aimodels.json"
echo
cat aimodels.json
echo
echo -n -e "${DEFAULT_ECHO}"
sleep $WAIT_COMMANDS
typer "cat aimodels-lock.json"
echo
cat aimodels-lock.json
echo
echo -n -e "${DEFAULT_ECHO}"
sleep $WAIT_COMMANDS
typer "aimm install $FIRST_MODEL"
echo
python3 $SCRIPT_PATH install $SECOND_MODEL 
echo -n -e "${DEFAULT_ECHO}"
sleep $WAIT_COMMANDS
typer "aimm list"
echo
python3 $SCRIPT_PATH list 
echo -n -e "${DEFAULT_ECHO}"
sleep $WAIT_COMMANDS
typer "exit"