import click

@click.group()
def cli():
    """Track working hours."""
    pass

@click.command()
def hi():
    """Start counting work hours."""
    click.echo("work hours tracking started.")

@click.command()
def bye():
    """Stop counting work hours."""
    click.echo("work hours tracking stopped.")

cli.add_command(hi)
cli.add_command(bye)

if __name__ == "__main__":
    cli()
