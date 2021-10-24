import re
from typing import Tuple, Union

from .exceptions import CommandError


class RoverNavigation:
    _POINTS = {"E": 0, "N": 90, "W": 180, "S": 270}
    _POINTS_REVERS = {str(v): k for k, v in _POINTS.items()}

    _L = 90
    _R = -90

    def __init__(self, x: int, y: int, pos: str) -> None:
        self.x = x
        self.y = y
        self.pos = self._POINTS[pos]

    def L(self) -> None:
        self.pos += self._L

    def R(self) -> None:
        self.pos += self._R

    def M(self) -> None:
        self.pos = self.pos % 360
        if self.pos == self._POINTS["E"]:
            self.x += 1
        elif self.pos == self._POINTS["W"]:
            self.x -= 1
        elif self.pos == self._POINTS["N"]:
            self.y += 1
        elif self.pos == self._POINTS["S"]:
            self.y -= 1

    def command(self, instructions: str) -> None:
        validate = bool(re.match(r"^[LRM]*$", instructions))
        if not validate:
            raise CommandError("Invalid instructions. %s" % instructions)
        for a in instructions:
            getattr(self, a)()

    def get_position(self) -> Tuple[int, int, str]:
        return self.x, self.y, self._POINTS_REVERS[str(self.pos % 360)]

    def format_position(self) -> str:
        x, y, pos = self.get_position()
        return f"{x} {y} {pos}"


class FileCommandInterface:
    def __init__(self):
        self._rovers = {}
        self._rovers_output = {}

    @staticmethod
    def check_plateasu(command: str) -> Union[Tuple[int, int], bool]:
        r = r"^(Plateau:)(\d+) (\d+)$"
        match = re.findall(r, command)
        if match:
            return int(match[0][1]), int(match[0][2])
        return False

    @staticmethod
    def check_landing(command: str) -> Union[bool, Tuple[str, int, int, str]]:
        r = r"^(\S+) (Landing:)(\d+) (\d+) (E|W|N|S)$"
        match = re.findall(r, command)
        if match:
            name, x, y, p = (
                match[0][0],
                int(match[0][2]),
                int(match[0][3]),
                match[0][4],
            )
            return name, x, y, p
        return False

    @staticmethod
    def check_instructions(command: str) -> Union[bool, Tuple[str, str]]:
        r = r"^(\S+) (Instructions:)(\S+[LRM])$"
        match = re.findall(r, command)
        if match:
            name, ins = match[0][0], match[0][2]
            return name, ins
        return False

    def register(self, command: str):
        r = self.check_plateasu(command)
        if r:
            self.p_x = r[0]
            self.p_y = r[1]
            return

        r = self.check_landing(command)
        if r:
            name, x, y, p = r
            self._rovers[name] = RoverNavigation(x, y, p)
            return

        r = self.check_instructions(command)
        if r:
            name, ins = r
            x = self._rovers.get(name)
            x.command(ins)
            self._rovers_output[name] = x.format_position()
            return

    def get_output(self) -> dict:
        return self._rovers_output
