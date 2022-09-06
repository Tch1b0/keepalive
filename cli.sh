#!/bin/sh

EXPECTED_PROJECT_ROOT=/usr/lib/keepalive
EXPECTED_SERVICE_FILE="$EXPECTED_PROJECT_ROOT"/keepalive.service

install () {
    # copy the keepalive.service file in a directory systemd scans
    cp "$EXPECTED_SERVICE_FILE" /etc/systemd/system/keepalive.service
    systemctl daemon-reload
}

start () {
    install
    systemctl start keepalive
}

enable () {
    install
    systemctl enable keepalive
}

# remove systemd references to keepalive
uninstall () {
    systemctl disable keepalive
    systemctl stop keepalive
    rm /etc/systemd/system/keepalive.service
    systemctl daemon-reload
}

upgrade () {
    git -C "$EXPECTED_PROJECT_ROOT" pull
    install
}

help () {
    cat <<EOF
usage: ./cli.sh [COMMAND]
    
keepalive helper cli

commands:
    install   - install keepalive as a unit for systemd
    start     - start the keepalive unit in systemd
    enable    - enable the keepalive unit in systemd for autostart
    uninstall - uninstall the keepalive unit from systemd
    upgrade   - pull and install the newest keepalive version
    help      - display this help
EOF
}

if [ ! -f "$EXPECTED_SERVICE_FILE" ]; then
    echo "Error: $EXPECTED_SERVICE_FILE does not exist. Please move the keepalive project to $EXPECTED_PROJECT_ROOT"
elif [ "$1" = "" ]; then
    help
else
    # evaluate the first argument, which is expected to be one of the commands listed in the help function
    eval $1
fi
