
from click.testing import CliRunner

from jason_server.cli import cli

NON_EXISTING_FILE = "tests/data/non_existing_file"
BAD_FORMATTED_FILE = "tests/data/bad_formatted_database.json"


def describe_cli():

    def with_no_arguments():
        runner = CliRunner()
        result = runner.invoke(cli)
        assert 0 == result.exit_code


def describe_cli_watch():

    def with_non_existing_file():
        runner = CliRunner()
        result = runner.invoke(cli, ['watch', NON_EXISTING_FILE])
        assert 1 == result.exit_code
        assert NON_EXISTING_FILE in result.output

    def with_bad_formated_json():
        runner = CliRunner()
        result = runner.invoke(cli, ['watch', BAD_FORMATTED_FILE])
        assert 2 == result.exit_code
        assert BAD_FORMATTED_FILE in result.output
