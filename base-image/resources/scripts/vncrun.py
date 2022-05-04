import os
import sys
import secrets
import pathlib
import subprocess

from subprocess import call


# Enable logging
import logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s', 
    level=logging.INFO, 
    stream=sys.stdout)

log = logging.getLogger(__name__)

HOME = os.getenv("HOME", "/root")
NB_USER = os.getenv("NB_USER", "1000")
NB_GID = os.getenv("NB_GID", "100")

VNC_PW = os.getenv("VNC_PW", "vncpassword")

if VNC_PW == None or VNC_PW == 'automated':
    vnc_passwd = secrets.token_urlsafe()[:8]
    vnc_viewonly_passwd = secrets.token_urlsafe()[:8]
    
else:
    vnc_passwd = VNC_PW
    vnc_viewonly_passwd = secrets.token_urlsafe()[:8]

print("✂️"*24)
print("VNC password: {}".format(vnc_passwd))
print("VNC view only password: {}".format(vnc_viewonly_passwd))
print("✂️"*24)

vncpasswd_input = "{0}\\n{1}".format(vnc_passwd, vnc_viewonly_passwd)
vnc_user_dir = pathlib.Path.home().joinpath(".vnc")
vnc_user_dir.mkdir(exist_ok=True)
vnc_user_passwd = vnc_user_dir.joinpath("passwd")

with vnc_user_passwd.open('wb') as f:
    subprocess.run(
        ["/opt/TurboVNC/bin/vncpasswd", "-f"],
        stdout=f,
        input=vncpasswd_input,
        universal_newlines=True,
        check=True)
    
vnc_user_passwd.chmod(0o600)

subprocess.call(
    ["/opt/TurboVNC/bin/vncserver " +
    " -SecurityTypes None " +
    " -xstartup 'dbus-launch startxfce4' " +
    " -fg"],
    shell=True

)

#Disable screensaver because no one would want it.
(pathlib.Path.home() / ".xscreensaver").write_text("mode: off\\n")