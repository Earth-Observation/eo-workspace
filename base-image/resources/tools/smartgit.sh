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

if [ ! -f "/usr/share/smartgit/bin/smartgit.sh" ]; then
    echo "Installing SmartGit. Please wait..."

    DESKTOP_ICON_PATH="/usr/share/applications"
    if [ "$(stat -c '%a' $DESKTOP_ICON_PATH)" == "777" ]
    then
        cd $RESOURCES_PATH
        wget https://www.syntevo.com/downloads/smartgit/smartgit-20_1_3.deb -O ./smartgit.deb
        apt-get update
        apt-get install -y ./smartgit.deb
        rm ./smartgit.deb
    else
        DESKTOP_ICON_PATH=$HOME/Desktop
        cat <<EOF > ${DESKTOP_ICON_PATH}/syntevo-smartgit.desktop
[Desktop Entry]
Version=1.0
Encoding=UTF-8
Name=SmartGit
Keywords=git
Comment=Git-Client
Type=Application
Categories=Development;RevisionControl
Terminal=false
StartupWMClass=SmartGit
Exec="/usr/share/smartgit/bin/smartgit.sh" %u
MimeType=x-scheme-handler/git;x-scheme-handler/smartgit;
Icon=/usr/share/smartgit/bin/smartgit-128.png
EOF
    fi


else
    echo "SmartGit is already installed"
fi

# Run
if [ $INSTALL_ONLY = 0 ] ; then
    echo "Starting SmartGit..."
    echo "SmartGit is a GUI application. Make sure to run this script only within the VNC Desktop."
    /usr/share/smartgit/bin/smartgit.sh --unity-launch $WORKSPACE_HOME
    sleep 10
fi