#!/bin/sh
# https://stackoverflow.com/questions/62353890/windows-subsystem-for-linux-wsl-2-and-jupyter-lab-how-to-open-a-jupyter-note

ADDR=$(jupyter notebook list | grep http | awk '{print $1}')

if ! [ "$ADDR" ]; then
    IP=$(ip addr | grep eth0 | grep inet | awk '{print $2}' | cut -d/ -f1)
    # by default job control doesn't work in scripts
    set -m
    jupyter notebook --no-browser --ip $IP --port 8888 &
    sleep 5
    ADDR=$(jupyter notebook list | grep http | awk '{print $1}')
fi

/mnt/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe "$ADDR"

# without fg it is not possible to shutdown the server with Ctrl-C
fg %1 2>/dev/null || exit 0
