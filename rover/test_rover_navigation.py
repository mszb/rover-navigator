import pytest

from .rover_navigation import RoverNavigation
from .exceptions import CommandError


def test_rover_position():
    rover = RoverNavigation(1, 2, "N")
    rover.L()
    possible = rover.format_position()
    assert possible == "1 2 W"

    rover.R()
    possible = rover.format_position()
    assert possible == "1 2 N"

    rover2 = RoverNavigation(1, 2, "S")
    rover2.L()
    possible = rover2.format_position()
    assert possible == "1 2 E"

    rover2.R()
    possible = rover2.format_position()
    assert possible == "1 2 S"


def test_rover_movement():
    rover = RoverNavigation(3, 1, "N")
    rover.M()
    rover.M()
    rover.M()
    possible = rover.format_position()
    assert possible == "3 4 N"
    rover.L()
    rover.M()
    rover.M()
    possible = rover.format_position()
    assert possible == "1 4 W"


def test_command():
    rover = RoverNavigation(1, 1, "N")
    rover.command("LMR")
    results = rover.format_position()
    assert "0 1 N" == results


def test_invalid_command():
    rover = RoverNavigation(1, 1, "N")
    with pytest.raises(CommandError):
        rover.command("LMRQWERTY")
