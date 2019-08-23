
import webbrowser

import click

from jason_server.derulo import run

CONTEXT_SETTINGS = dict(help_option_names=['--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-h", "--host", default='localhost', help="Host adress"
)
@click.option(
    "-p", "--port", default=8080, help="Port"
)
@click.option(
    "-q", "--quiet", is_flag=True
)
@click.version_option(
    version='0.8.1'
)
@click.pass_context
def cli(ctx, host, port, quiet):
    """Set options

    Args:
        host(str): host adress
        port(int): port number
        quiet(bool): disable cli output

    """
    ctx.obj = {}
    ctx.obj["host"] = host
    ctx.obj["port"] = port
    ctx.obj["quiet"] = quiet


@cli.command(help="Run your database as REST Api")
@click.argument('database')
@click.option(
    "-o", "--open", is_flag=True
)
@click.pass_context
def watch(ctx, database, open):
    """Generate the REST api and Run the server

    Args:
        databae(str): path to database
        open(bool): open home url in browser

    """
    if open:
        url = "http://{}:{}".format(ctx.obj["host"], ctx.obj["port"])
        webbrowser.open(url)
    run(ctx.obj, database=database)
