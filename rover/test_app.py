import re
from unittest import mock

from click.testing import CliRunner

from app import main


def test_process_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.txt", "w") as f:
            f.write("Plateau:5 5\n")
            f.write("Rover1 Landing:1 2 N\n")
            f.write("Rover1 Instructions:LMLMLMLMM\n")
            f.write("Rover2 Landing:3 3 E\n")
            f.write("Rover2 Instructions:MMRMMRMRRM")

        results = runner.invoke(main, ["--file=test.txt"])
        assert results.exit_code == 0
        assert results.output == "Rover1: 1 3 N\nRover2: 5 1 E\n"


def test_process_file_negative():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test.txt", "w") as f:
            f.write("Plateau:5 5\n")
            f.write("Rover1 Landing:1 2 N\n")
            f.write("Rover1 Instructions:LRM-ASD\n")

        results = runner.invoke(main, ["--file=test.txt"])
        assert results.exit_code == 0
        assert results.output == ""


def test_interactive():
    runner = CliRunner()
    results = runner.invoke(main, input="\n".join(["5 5", "2 3 N", "LMRM"]))

    regex = r"^(New position: 1 4 N)$"
    matches = re.search(regex, results.output, re.MULTILINE)
    assert matches.group() == "New position: 1 4 N"


def test_invalid_plateasu():
    runner = CliRunner()
    with mock.patch("app._invalid_input", side_effect=KeyboardInterrupt):
        results = runner.invoke(
            main,
            input="\n".join(
                [
                    "ABC XYZ",
                ]
            ),
        )
        regex = r"(ABC XYZ\n\nAborted!)"
        matches = re.search(regex, results.output, re.MULTILINE)
        assert matches is not None


def test_invalid_landing():
    runner = CliRunner()
    with mock.patch("app._invalid_input", side_effect=KeyboardInterrupt):
        results = runner.invoke(
            main,
            input="\n".join(["5 5", "A B C"]),
        )
        regex = r"(A B C\n\nAborted!)"
        matches = re.search(regex, results.output, re.MULTILINE)
        assert matches is not None


def test_invalid_commands():
    runner = CliRunner()
    with mock.patch("app._invalid_input", side_effect=KeyboardInterrupt):
        results = runner.invoke(
            main,
            input="\n".join(["5 5", "1 2 N", "ASD"]),
        )
        regex = r"(ASD\n\nAborted!)"
        matches = re.search(regex, results.output, re.MULTILINE)
        assert matches is not None


def test_invalid_commands_with_retry():
    runner = CliRunner()
    results = runner.invoke(
        main,
        input="\n".join(["A B", "5 5", "A B X", "2 3 N", "QWERTY", "LMRM"]),
    )
    regex = r"^(New position: 1 4 N)$"
    matches = re.search(regex, results.output, re.MULTILINE)
    assert matches.group() == "New position: 1 4 N"
