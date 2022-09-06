#!/bin/sh

EXPECTED_PROJECT_ROOT=/usr/lib/keepalive
EXPECTED_SERVICE_FILE="$EXPECTED_PROJECT_ROOT"/keepalive.service

# installed: boolean
installed=0

install () {
    # return if already installed
    if [ $installed -eq 1 ]; then
        return
    fi
    pip install -r "$EXPECTED_PROJECT_ROOT"/requirements.txt > /dev/null
    # copy the keepalive.service file in a directory systemd scans
    cp "$EXPECTED_SERVICE_FILE" /etc/systemd/system/keepalive.service
    systemctl daemon-reload
    installed=1
}

start () {
    install
    systemctl start keepalive
}

stop () {
    systemctl stop keepalive
}

enable () {
    install
    systemctl enable keepalive
}

disable () {
    systemctl disable keepalive
}

deploy () {
    install
    start
    enable
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
    # set installed to 0(=false) as the updated version was not installed yet
    installed=0
    install
}

help () {
    cat <<EOF
usage: ./cli.sh [COMMAND]
    
keepalive helper cli

commands:
    install   - install keepalive as a unit for systemd
    start     - start the keepalive systemd unit
    stop      - stop the keepalive systemd unit
    enable    - enable the keepalive systemd unit for autostart
    disable   - disable the keepalive systemd unit for autostart
    deploy    - install, start and enable keepalive
    uninstall - uninstall the keepalive systemd unit
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
