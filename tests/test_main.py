from unittest.mock import patch, MagicMock

from click.testing import CliRunner

from maked.main import cli


runner = CliRunner()


def test_no_content():
    result = runner.invoke(cli, input="")
    assert result.exit_code == 1
    assert "No content received." in result.output


def test_no_front_matter():
    result = runner.invoke(cli, input="# Just a markdown file\n")
    assert result.exit_code == 1
    assert "No YAML front matter found." in result.output


def test_missing_maked_key():
    result = runner.invoke(cli, input="---\ntitle: hello\n---\n")
    assert result.exit_code == 1
    assert "No 'maked' field found" in result.output


def test_invalid_yaml():
    result = runner.invoke(cli, input="---\n: bad: yaml:\n---\n")
    assert result.exit_code == 1
    assert "Error parsing YAML front matter." in result.output


def test_executes_command():
    mock_result = MagicMock(returncode=0)
    with patch("maked.main.subprocess.run", return_value=mock_result) as mock_run:
        result = runner.invoke(cli, input="---\nmaked: 'echo hello'\n---\n")
        assert result.exit_code == 0
        mock_run.assert_called_once_with("echo hello", shell=True)


def test_propagates_command_exit_code():
    mock_result = MagicMock(returncode=42)
    with patch("maked.main.subprocess.run", return_value=mock_result):
        result = runner.invoke(cli, input="---\nmaked: 'exit 42'\n---\n")
        assert result.exit_code == 42


def test_dry_run():
    with patch("maked.main.subprocess.run") as mock_run:
        result = runner.invoke(cli, ["--dry-run"], input="---\nmaked: 'echo hello'\n---\n")
        assert result.exit_code == 0
        assert "Command: echo hello" in result.output
        mock_run.assert_not_called()


def test_closing_delimiter_without_trailing_newline():
    mock_result = MagicMock(returncode=0)
    with patch("maked.main.subprocess.run", return_value=mock_result):
        result = runner.invoke(cli, input="---\nmaked: 'echo hello'\n---")
        assert result.exit_code == 0


def test_version():
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output
