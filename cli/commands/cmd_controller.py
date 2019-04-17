import os
import subprocess

import click

from db.my_db import controllers

@click.group()
def cli():
    """Manage SDN Controller"""
    pass


@click.command()
def ls():
	"""
	Lists the connected SDN controllers
	"""

	for sdn_con in controllers:
		click.echo('{0} controller @ {1}'.format(sdn_con['type'], sdn_con['ip']))
	

cli.add_command(ls)