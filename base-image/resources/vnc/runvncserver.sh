#!/bin/bash
user_name="jovyan"
group_name="users"
LOG=/tmp/container-init.log
export DBUS_SESSION_BUS_ADDRESS="autolaunch:"
export DISPLAY=":1"
export VNC_RESOLUTION="1920x1080" 
export LANG="en_US.UTF-8"
export LANGUAGE="en_US.UTF-8"
# Execute the command it not already running

# Execute the command it not already running
startInBackgroundIfNotRunning()
{
	log "Starting $1."
	echo -e "\n** $(date) **" | sudoIf tee -a /tmp/$1.log > /dev/null
	if ! pidof $1 > /dev/null; then
		keepRunningInBackground "$@"
		while ! pidof $1 > /dev/null; do
			sleep 1
		done
		log "$1 started."
	else
		echo "$1 is already running." | sudoIf tee -a /tmp/$1.log > /dev/null
		log "$1 is already running."
	fi
}

# Keep command running in background
keepRunningInBackground()
{
	($2 sh -c "while :; do echo [\$(date)] Process started.; $3; echo [\$(date)] Process exited!; sleep 5; done 2>&1" | sudoIf tee -a /tmp/$1.log > /dev/null & echo "$!" | sudoIf tee /tmp/$1.pid > /dev/null)
}

# Use sudo to run as root when required
sudoIf()
{
    if [ "$(id -u)" -ne 0 ]; then
        sudo "$@"
    else
        "$@"
    fi
}

# Use sudo to run as non-root user if not already running
sudoUserIf()
{
    if [ "$(id -u)" -eq 0 ]; then
        sudo -u ${user_name} "$@"
    else
        "$@"
    fi
}

# Log messages
log()
{
    echo -e "[$(date)] $@" | sudoIf tee -a $LOG > /dev/null
}

log "** SCRIPT START **"

# Start dbus.
log 'Running "/etc/init.d/dbus start".'
if [ -f "/var/run/dbus/pid" ] && ! pidof dbus-daemon  > /dev/null; then
    sudoIf rm -f /var/run/dbus/pid
fi
sudoIf /etc/init.d/dbus start 2>&1 | sudoIf tee -a /tmp/dbus-daemon-system.log > /dev/null
while ! pidof dbus-daemon > /dev/null; do
    sleep 1
done

# Startup tigervnc server and fluxbox
sudo rm -rf /tmp/.X11-unix /tmp/.X*-lock
mkdir -p /tmp/.X11-unix
sudoIf chmod 1777 /tmp/.X11-unix
sudoIf chown root:${group_name} /tmp/.X11-unix
if [ "$(echo "${VNC_RESOLUTION}" | tr -cd 'x' | wc -c)" = "1" ]; then VNC_RESOLUTION=${VNC_RESOLUTION}x16; fi
screen_geometry="${VNC_RESOLUTION%*x*}"
screen_depth="${VNC_RESOLUTION##*x}"



# startInBackgroundIfNotRunning "TurboVNC" sudoUserIf "/opt/TurboVNC/bin/vncserver ${DISPLAY} -geometry ${screen_geometry} -depth ${screen_depth}  "
command="/opt/TurboVNC/bin/vncserver "${DISPLAY}" \
 -SecurityTypes None \
 -alwaysshared \
 -depth "${screen_depth}" \
 -geometry "${screen_geometry}" \
 -xstartup "$VNC_XSTARTUP""

startInBackgroundIfNotRunning "TurboVNC" sudoUserIf "${command}"

#startInBackgroundIfNotRunning "TurboVNC" sudoIf "/opt/TurboVNC/bin/vncserver ${DISPLAY} -geometry ${screen_geometry} -depth ${screen_depth} -rfbport  -dpi ${VNC_DPI:-96} -localhost -desktop fluxbox -fg"

# Start fluxbox as a light weight window manager.
# startInBackgroundIfNotRunning "xfce4-session" sudoUserIf "dbus-launch startxfce4"

#startInBackgroundIfNotRunning "x11vnc" sudoIf "x11vnc -display ${DISPLAY:-:1} -rfbport ${VNC_PORT:-5901} -localhost -no6 -xkb -shared -forever -passwdfile $HOME/.vnc/passwd"

#startInBackgroundIfNotRunning "TurboVNC" sudoUserIf "/opt/TurboVNC/bin/vncserver ${DISPLAY} -geometry ${screen_geometry} -depth ${screen_depth} -rfbport  -dpi ${VNC_DPI:-96} -localhost -desktop fluxbox -fg -passwd /usr/local/etc/vscode-dev-containers/vnc-passwd"


# startInBackgroundIfNotRunning "TurboVNC" sudoUserIf "/opt/TurboVNC/bin/vncserver ${DISPLAY} -geometry ${screen_geometry} -depth ${screen_depth}  "
