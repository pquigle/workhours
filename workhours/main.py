import os
import time
import shutil
from tqdm import tqdm
from typing import Tuple
import click
import subprocess

from datetime import date, datetime, timedelta

#-------------------------------global vars-----------------------------------#

FORMAT = "%Y-%m-%d %H:%M:%S"
FILE = "timecard.csv"
DIR = click.get_app_dir("Workhours")
FILE_PATH = os.path.join(DIR, FILE)

#--------------------------------functions------------------------------------#

def get_current_time() -> datetime:
    return datetime.now()

def save_hours(time_of_action: date, action: str) -> None:
    with click.open_file(FILE_PATH, mode="a") as f:
        f.write(f"{time_of_action.strftime(FORMAT)},{action}\n")

def get_last_entry() -> Tuple[str, str]:
    message = subprocess.check_output(["tail", "-n 1", FILE_PATH])
    return tuple(message.decode("utf-8").replace("\n", "").split(","))

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Track working hours."""
    os.makedirs(DIR, exist_ok=True)
    if ctx.invoked_subcommand is None:
        status()

@cli.command()
def status():
    """Show current working status."""
    if not os.path.isfile(FILE_PATH):
        date = get_current_time()
        click.echo("initiated work hours.")
        save_hours(date, "start")
        return

    last_entry = get_last_entry()
    last_date, last_action = last_entry

    if last_action == "stop":
        click.echo("You're currently not working.")
    elif last_action == "start":
        date = get_current_time()
        time_difference = (date - datetime.strptime(last_date, FORMAT)).total_seconds()
        working_hours = time_difference // 3600
        working_minutes = (time_difference - (working_hours * 3600)) // 60
        click.echo(f"You have focused for {int(working_hours)} hours and {int(working_minutes)} minutes.")
    else:
        click.echo(f"Last action not recognized: {last_action}")

@cli.command()
def hi():
    """Start counting work hours."""
    last_entry = get_last_entry()
    last_date, last_action = last_entry
    if last_action == "start":
        click.echo("You're already working.")
    elif last_action == "stop":
        date = get_current_time()
        save_hours(date, "start")
        click.echo(f"Tracking working hours started at {date.strftime(FORMAT)}")
    else:
        click.echo(f"Last action not recognized: {last_action}")

@cli.command()
def bye():
    """Stop counting work hours."""
    last_entry = get_last_entry()
    last_date, last_action = last_entry
    if last_action == "stop":
        click.echo("You already stopped working.")
    elif last_action == "start":
        date = get_current_time()
        save_hours(date, "stop")
        click.echo(f"Tracking work hours stopped at {date.strftime(FORMAT)}")
    else:
        click.echo(f"Last action not recognized: {last_action}")

@cli.command()
def lunch():
    """Take 30 minute break."""
    last_entry = get_last_entry()
    last_date, last_action = last_entry
    if last_action == "stop":
        click.echo("You already stopped working.")
    elif last_action == "start":
        # Stop work and start lunch
        date = get_current_time()
        save_hours(date, "stop")
        click.echo(f"Started lunch at {date.strftime(FORMAT)}")

        # Wait 30 minutes, initialize progress bar
        for i in tqdm(range(30)):
            time.sleep(60)
        
        # Resume work
        date = get_current_time()
        save_hours(date, "start")
        click.echo(f"Ended lunch at {date.strftime(FORMAT)}")
    else:
        click.echo(f"Last action not recognized: {last_action}")

@cli.command()
def log():
    """Show log of work hours (last 10 entries)."""
    #TODO: show last 2 days rather than static 10 entries
    message = subprocess.check_output(["tail", "-n 10", FILE_PATH])
    print(message.decode("utf-8"))


@cli.command()
def friday():
    """Finish work for the week. Move the current time to legacy"""
    
    # Walk back until we reach Monday of this week
    day = datetime.now()
    while day.day != 'Mon':
        day -= timedelta(days=1)

    # If not checked out, say bye
    bye()

    # Move the log to legacy
    legacy_file = os.path.join(DIR, day.strftime('%Y%m%d') + '_timecard.csv')
    with open(legacy_file, 'a+') as legacy:
        with open(FILE_PATH, 'r') as current:
            legacy.write(current.read())

    # Delete current timecard
    os.remove(current)

    click.echo("Have a nice weekend!")

#-----------------------------------main--------------------------------------#

if __name__ == "__main__":
    cli()
