#!/usr/bin/env python3.4

import click
import os

from tabulate import tabulate

from Data import EmailDelivery, DataHelper
from HackerRankAPI import API

# HackerRank API instance
api = API(os.environ['HA_TOKEN'])

# Helpers
dh = DataHelper(api)
ed = EmailDelivery(username='andrey@betlabs.ru')


@click.group()
def cli():
    pass


@cli.group()
def db():
    pass


@db.command()
@click.option('--update/--no-update')
def students(update):
    """
    Fetch list of students from default test
    """
    if update:
        click.secho('Updating...', fg='green')
        data = dh.map_students()
        DataHelper.write_data(data, 'students.json')
        click.secho('Finished!', fg='green')


@cli.command()
@click.option('--students', 'what', flag_value='students', help='List of all students.')
@click.option('--student', 'what', flag_value='student', help='Display data for certain student.')
def display(what):
    """
    Display data
    """
    if what == 'students':
        data = DataHelper.read_data('students.json')
        click.secho(tabulate(data, headers="keys", tablefmt="grid"), fg='blue')
    elif what == 'student':
        pass
    else:
        click.secho('Nothing to display', fg='red')


@cli.command()
@click.option('--all/--no-all')
def notify(all):
    """
    Email notifications
    """
    if all:
        click.secho('all', fg='yellow')
    else:
        to = click.prompt('To')
        subject = click.prompt('Subject')
        text = click.prompt('Text')
        password = click.prompt('Enter account password', confirmation_prompt=False, hide_input=True)
        status = ed.send_email_to(password, to, subject, text)
        click.secho(status, fg='yellow')


@cli.command()
def upload():
    """
    Upload new data to website
    """

    # TODO: collect data from all existing test except initial test
    data = dh.collect_data_from_test(103271)
    DataHelper.write_data(data, 'results.json')


if __name__ == "__main__":
    cli()


