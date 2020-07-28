#!/bin/bash

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

if ! dpkg-query -l cifs-utils >/dev/null; then
    echo "Please make sure to run the script with: sudo -E bash webdisk-lrz.sh"
    echo "Installing CIFS. Please wait..."
    apt-get update
    apt-get install cifs-utils
else
    echo "CIFS is already installed"
fi

# Run
if [ $INSTALL_ONLY = 0 ] ; then
    echo "Starting CIFS Terminal..."
    echo "CIFS is to be mounted. Make sure to enter the passwored for the login."
    # SMB_USERNAME="ge49gar"
    SMB_USERNAME=${JUPYTERHUB_USER}
    SMB_SERVER="//nas.ads.mwn.de/"
    mkdir -p /media/webdisk
    ln -s -f /media/webdisk /workspace 
    LINE=$(echo "${SMB_SERVER}${SMB_USERNAME} /media/webdisk cifs username=${SMB_USERNAME},domain=ADS,vers=3.0,rw,nounix,file_mode=0777,dir_mode=0777 0 0")
    echo "Username: $SMB_USERNAME"
    echo "Mount following SMB:"

    FILE="/etc/fstab"
    cat $FILE
    grep -qF -- "$LINE" "$FILE" || echo "$LINE" >> "$FILE"
    mount -a

    mkdir -p /media/webdisk/
    #cp -r ~/Downloads /media/webdisk && rm -r ~/Downloads
    ln -s -f /media/webdisk/ $HOME/
    ln -s -f /media/webdisk/Downloads $HOME/ 
    sleep 10
fi