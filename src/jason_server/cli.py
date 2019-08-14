import click

from jason_server import main
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(
    invoke_without_command=True,
    context_settings=CONTEXT_SETTINGS
)
@click.version_option(
    version='0.1.0'
)
def cli():
    main()
