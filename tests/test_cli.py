import pytest

from click.testing import CliRunner

from jason_server.cli import cli

def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert 0 == result.exit_code
    assert "Using jason-server" in result.output
