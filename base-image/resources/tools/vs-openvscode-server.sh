#!/bin/sh

# Stops script execution if a command has an error
set -e

INSTALL_ONLY=0
# Loop through arguments and process them: https://pretzelhands.com/posts/command-line-flags
for arg in "$@"; do
    case $arg in
        -i|--install) INSTALL_ONLY=1 ; shift ;;
        *) break ;;
    esac
done


if [ ! -f "/usr/local/bin/openvscode-server"  ]; then
    echo "Installing OpenVS Code Server. Please wait..."

    OPENVSCODE_VERSION=1.66.1
    cd /tmp
    mkdir -p ${RESOURCES_PATH}/novnc
    curl -sSL https://github.com/gitpod-io/openvscode-server/releases/download/openvscode-server-v${OPENVSCODE_VERSION}/openvscode-server-v${OPENVSCODE_VERSION}-linux-x64.tar.gz -o /tmp/openvscode-server-linux-x64.tar.gz
    #unzip $CACHE_DIR/novnc-install.tar.gz -d ${RESOURCES_PATH}/novnc
    mkdir -p /tmp/openvscode-server && tar -xzf /tmp/openvscode-server-linux-x64.tar.gz --strip-components=1 -C /tmp/openvscode-server
    mv /tmp/openvscode-server /opt
    ln -sf /opt/openvscode-server/bin/openvscode-server /usr/local/bin/openvscode-server

else
    echo "VS Code Server is already installed"
fi

# Run
if [ $INSTALL_ONLY = 0 ] ; then
    if [ -z "$PORT" ]; then
        read -p "Please provide a port for starting VS Code Server: " PORT
    fi

    echo "Starting VS Code Server on port "$PORT
    # Create tool entry for tooling plugin
    echo '{"id": "vscode-link", "name": "VS Code", "url_path": "/tools/'$PORT'/", "description": "Visual Studio Code webapp"}' > $HOME/.workspace/tools/vscode.json
    /usr/local/bin/openvscode-server --port=$PORT --disable-telemetry --user-data-dir=$HOME/.config/Code/ --extensions-dir=$HOME/.vscode/extensions/ --disable-update-check --auth=none $WORKSPACE_HOME/
    sleep 15
fi