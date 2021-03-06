import os
import getpass
from pathlib import Path

params = {}
params["user"] = getpass.getuser ()

params["installdir"] = Path.cwd ()

# point your browser at hostname:<number> where <number> is the port
# specified below
params["fonoport"] = 8000

# ExecStart=/bin/bash {installdir}/fono.sh

systemd_template = """\
# Systemd service file for the fono spotify and internet radio player
# NvdM
#
# This file is automatically generated by fono/gen_init_file.py
# It is a systemd recipe for having "fono" start at boot.
#
# Instal as /etc/systemd/system/fono.service
# then run sudo systemctl enable fono
#
# After installing, you can used systemctl commands for controlling
# fono. Reasons to do so include changing the stations menu. Systemctl
# commands include the following:
#    sudo systemctl enable fono # to enable systemctl control of this service
#    sudo systemctl disable fono # to disable
#    sudo systemctl start fono # to start the service
#    sudo systemctl stop fono
#    sudo systemctl restart fono
#    sudo systemctl status fono

[Unit]
Description=Fono Service
After=network.target

[Service]
ExecStart={installdir}/venv/bin/gunicorn -w 1 --bind 0.0.0.0:{fonoport} fono:app
WorkingDirectory={installdir}
StandardOutput=journal
StandardError=journal
Restart=always
User={user}

[Install]
WantedBy=multi-user.target""".format (**params)

print (systemd_template)
