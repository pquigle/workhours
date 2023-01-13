import os
from typing import Tuple
import click
import subprocess

from datetime import date, datetime


FORMAT = "%Y-%m-%d %H:%M:%S"
FILE = "log.csv"
DIR = click.get_app_dir("Workhours")
FILE_PATH = os.path.join(DIR, FILE)

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
        click.echo("working hours not initiated.")
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
        click.echo(f"You have been working for {int(working_hours)} hours and {int(working_minutes)} minutes.")
    else:
        click.echo(f"Last action not recognized: {last_action}")

@cli.command()
def hi():
    """Start counting work hours."""
    date = get_current_time()
    save_hours(date, "start")
    click.echo(f"Tracking working hours started at {date.strftime(FORMAT)}")

@cli.command()
def bye():
    """Stop counting work hours."""
    date = get_current_time()
    save_hours(date, "stop")
    click.echo(f"Tracking work hours stoped at {date.strftime(FORMAT)}")

if __name__ == "__main__":
    cli()
