# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# mypy: ignore-errors
#%%
import os
import stat
import subprocess

import psutil
import errno

from jupyter_core.paths import jupyter_data_dir

c = get_config()  # noqa: F821
c.ServerApp.ip = "0.0.0.0"
c.ServerApp.port = 8090
c.ServerApp.open_browser = False
#%%
# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False
#%%
## The directory to use for notebooks and kernels.
#  Default: ''
c.ServerApp.root_dir = './'
# c.NotebookApp.notebook_dir="./"
## Whether to allow the user to run the server as root.
#  Default: False
c.ServerApp.allow_root = False
# c.NotebookApp.allow_root=True
# https://forums.fast.ai/t/jupyter-notebook-enhancements-tips-and-tricks/17064/22


## (bytes/sec)
#          Maximum rate at which stream output can be sent on iopub before they are
#          limited.
#  Default: 1000000
c.ServerApp.iopub_data_rate_limit = 2147483647
# c.NotebookApp.iopub_data_rate_limit=2147483647

## (msgs/sec)
#          Maximum rate at which messages can be sent on iopub before they are
#          limited.
#  Default: 1000
c.ServerApp.iopub_msg_rate_limit = 100000000
# c.NotebookApp.iopub_msg_rate_limit = 100000000
## The number of additional ports to try if the specified port is not available
#  (env: JUPYTER_PORT_RETRIES).
#  Default: 50
c.ServerApp.port_retries = 0
# c.NotebookApp.port_retries=0

## If True, display controls to shut down the Jupyter server, such as menu items
#  or buttons.
#  Default: True
c.ServerApp.quit_button = False
# c.NotebookApp.quit_button=False
## Allow requests where the Host header doesn't point to a local server
#  
#         By default, requests get a 403 forbidden response if the 'Host' header
#         shows that the browser thinks it's on a non-local domain.
#         Setting this option to True disables this check.
#  
#         This protects against 'DNS rebinding' attacks, where a remote web server
#         serves you a page and then changes its DNS to send later requests to a
#         local IP, bypassing same-origin checks.
#  
#         Local IP addresses (such as 127.0.0.1 and ::1) are allowed as local,
#         along with hostnames configured in local_hostnames.
#  Default: False
c.ServerApp.allow_remote_access = True
# c.NotebookApp.allow_remote_access=True
## Disable cross-site-request-forgery protection
#  
#          Jupyter notebook 4.3.1 introduces protection from cross-site request forgeries,
#          requiring API requests to either:
#  
#          - originate from pages served by this server (validated with XSRF cookie and token), or
#          - authenticate with a token
#  
#          Some anonymous compute resources still desire the ability to run code,
#          completely without authentication.
#          These services can disable all authentication and security checks,
#          with the full knowledge of what that implies.
#  Default: False
c.ServerApp.disable_check_xsrf = True
# c.NotebookApp.disable_check_xsrf=True
## Set the Access-Control-Allow-Origin header
#  
#          Use '*' to allow any origin to access your server.
#  
#          Takes precedence over allow_origin_pat.
#  Default: ''
c.ServerApp.allow_origin = '*'
# c.NotebookApp.allow_origin='*'

## Whether to trust or not X-Scheme/X-Forwarded-Proto and X-Real-Ip/X-Forwarded-
#  For headerssent by the upstream reverse proxy. Necessary if the proxy handles
#  SSL
#  Default: False
c.ServerApp.trust_xheaders = True
# c.NotebookApp.trust_xheaders=True
## Set the log level by value or name.
## Set the log level by value or name.
#  Choices: any of [0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']
#  Default: 30
c.Application.log_level = 'WARN'
# c.NotebookApp.log_level="WARN"

## Answer yes to any prompts.
#  See also: JupyterApp.answer_yes
c.ServerApp.answer_yes = True
# c.JupyterApp.answer_yes = True

# set base url if available
base_url = os.getenv("WORKSPACE_BASE_URL", "/")
if base_url != None and base_url != "/":
    # c.NotebookApp.base_url=base_url
    c.ServerApp.base_url = base_url

# Do not delete files to trash: https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash=False

# Always use inline for matplotlib
c.IPKernelApp.matplotlib = 'inline'


shutdown_inactive_kernels = os.getenv("SHUTDOWN_INACTIVE_KERNELS", "false")
if shutdown_inactive_kernels and shutdown_inactive_kernels.lower().strip() != "false":
    cull_timeout = 172800 # default is 48 hours
    try: 
        # see if env variable is set as timout integer
        cull_timeout = int(shutdown_inactive_kernels)
    except ValueError:
        pass
    
    if cull_timeout > 0:
        print("Activating automatic kernel shutdown after " + str(cull_timeout) + "s of inactivity.")
        # Timeout (in seconds) after which a kernel is considered idle and ready to be shutdown.
        c.MappingKernelManager.cull_idle_timeout = cull_timeout
        # Do not shutdown if kernel is busy (e.g on long-running kernel cells)
        c.MappingKernelManager.cull_busy = False
        # Do not shutdown kernels that are connected via browser, activate?
        c.MappingKernelManager.cull_connected = False

authenticate_via_jupyter = os.getenv("AUTHENTICATE_VIA_JUPYTER", "false")
if authenticate_via_jupyter and authenticate_via_jupyter.lower().strip() != "false":
    # authentication via jupyter is activated

    # Do not allow password change since it currently needs a server restart to accept the new password
    c.ServerApp.allow_password_change = False

    if authenticate_via_jupyter.lower().strip() == "<generated>":
        # dont do anything to let jupyter generate a token in print out on console
        pass
    # if true, do not set any token, authentication will be activate on another way (e.g. via JupyterHub)
    elif authenticate_via_jupyter.lower().strip() != "true":
        # if not true or false, set value as token
        c.ServerApp.token = authenticate_via_jupyter
else:
    # Deactivate token -> no authentication
    c.ServerApp.token=""

# https://github.com/timkpaine/jupyterlab_iframe
try:
    if not base_url.startswith("/"):
        base_url = "/" + base_url
    # iframe plugin currently needs absolut URLS
    c.JupyterLabIFrame.iframes = [base_url + 'tools/ungit', base_url + 'tools/netdata', base_url + 'tools/vnc', base_url + 'tools/glances', base_url + 'tools/vscode']
except:
    pass

# https://github.com/timkpaine/jupyterlab_templates
WORKSPACE_HOME = os.getenv("WORKSPACE_HOME", "/workspace")
try:
    if os.path.exists(WORKSPACE_HOME + '/templates'):
        c.JupyterLabTemplates.template_dirs = [WORKSPACE_HOME + '/templates']
    c.JupyterLabTemplates.include_default = False
except:
    pass

# Set memory limits for resource use display: https://github.com/yuvipanda/nbresuse
try:
    mem_limit = None
    if os.path.isfile("/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as file:
            mem_limit = file.read().replace('\n', '').strip()
    
    total_memory = psutil.virtual_memory().total

    if not mem_limit:
        mem_limit = total_memory
    elif int(mem_limit) > int(total_memory):
        # if mem limit from cgroup bigger than total memory -> use total memory
        mem_limit = total_memory
    
    # Workaround -> round memory limit, otherwise the number is quite long
    # TODO fix in nbresuse
    mem_limit = round(int(mem_limit) / (1024 * 1024)) * (1024 * 1024)
    c.ResourceUseDisplay.mem_limit = int(mem_limit)
    c.ResourceUseDisplay.mem_warning_threshold=0.1
except:
    pass
#%%
# Generate a self-signed certificate
OPENSSL_CONFIG = """\
[req]
distinguished_name = req_distinguished_name
[req_distinguished_name]
"""
if "GEN_CERT" in os.environ:
    dir_name = jupyter_data_dir()
    pem_file = os.path.join(dir_name, "notebook.pem")
    os.makedirs(dir_name, exist_ok=True)

    # Generate an openssl.cnf file to set the distinguished name
    cnf_file = os.path.join(os.getenv("CONDA_DIR", "/usr/lib"), "ssl", "openssl.cnf")
    if not os.path.isfile(cnf_file):
        with open(cnf_file, "w") as fh:
            fh.write(OPENSSL_CONFIG)

    # Generate a certificate if one doesn't exist on disk
    subprocess.check_call(
        [
            "openssl",
            "req",
            "-new",
            "-newkey=rsa:2048",
            "-days=365",
            "-nodes",
            "-x509",
            "-subj=/C=XX/ST=XX/L=XX/O=generated/CN=generated",
            f"-keyout={pem_file}",
            f"-out={pem_file}",
        ]
    )
    # Restrict access to the file
    os.chmod(pem_file, stat.S_IRUSR | stat.S_IWUSR)
    c.ServerApp.certfile = pem_file

# Change default umask for all subprocesses of the notebook server if set in
# the environment
if "NB_UMASK" in os.environ:
    os.umask(int(os.environ["NB_UMASK"], 8))
