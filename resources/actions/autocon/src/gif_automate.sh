#!/usr/bin/env bash

typer() {
    for (( i=0; i<${#1}; i++ )); do
        echo -n "${1:$i:1}"
        sleep 0.08
    done
}
