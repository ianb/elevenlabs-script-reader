"""Console script for eleven_labs_script_reader."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for eleven_labs_script_reader."""
    click.echo("Replace this message by putting your code into "
               "eleven_labs_script_reader.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
