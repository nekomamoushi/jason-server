import click

from jason_server.derulo import run

CONTEXT_SETTINGS = dict(help_option_names=['--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-h", "--host", default='localhost', help="Host adress"
)
@click.option(
    "-p","--port", default=8080, help="Port"
)
@click.version_option(
    version='0.2.0'
)
@click.pass_context
def cli(ctx, host, port):
    ctx.obj = {}
    ctx.obj["host"] = host
    ctx.obj["port"] = port

@cli.command(help="Run your database as REST Api")
@click.argument('database')
@click.pass_context
def watch(ctx, database):
    run(ctx.obj, database=database)
