import click

from rover.exceptions import CommandError
from rover.rover_navigation import FileCommandInterface, RoverNavigation


def process_file(file):
    """Proces file based commands"""

    ins = FileCommandInterface()
    while True:
        line = file.readline()
        if not line:
            break
        line = str(line.decode("utf-8").strip())
        ins.register(line)
    file.close()
    results = ins.get_output()
    if results:
        for name, value in results.items():
            click.echo(f"{name}: {value}")


def _invalid_input():
    click.echo("Invalid input, try again")


def interactive():
    """
    Interactive command prompt for rover navigation.
    """

    click.secho(
        "This plateau, which is curiously rectangular, must be navigated by the rovers\n"
        + "so that their on board cameras can get a complete view of the surrounding terrain\n"
        + "to send back to Earth.\n",
        fg="green",
    )
    while True:
        try:
            p = click.prompt("Please enter a valid integer. (Example: 5 5)", type=str)
            p = p.split(" ")
            pos_x = int(p[0])
            pos_y = int(p[1])
            break
        except (IndexError, ValueError):
            _invalid_input()

    click.secho(
        "\n\n\n"
        + "A rover's position is represented by a combination of an x and y co-ordinates and a\n"
        + "letter representing one of the four cardinal compass points. The plateau is divided up\n"
        + "into a grid to simplify navigation. An example position might be 0, 0, N, which means\n"
        + "the rover is in the bottom left corner and facing North.\n",
        fg="green",
    )
    while True:
        try:
            start = click.prompt(
                "Enter rover landing position. (Example: 1 2 N)", type=str
            )
            start = start.split(" ")
            start_x = int(start[0])
            start_y = int(start[1])
            start_point = start[2]
            break
        except (IndexError, ValueError):
            _invalid_input()

    click.secho(
        "In order to control a rover, NASA sends a simple string of letters. The possible letters\n"
        + "are 'L', 'R' and 'M'. 'L' and 'R' makes the rover spin 90 degrees left or right respectively,\n"
        + "without moving from its current spot. 'M' means move forward one grid point,and maintain\n"
        + "the same heading.\n",
        fg="green",
    )
    while True:
        try:
            instuctions = click.prompt("Enter instuctions (Example: LMRM)", type=str)
            x = RoverNavigation(start_x, start_y, start_point)
            x.command(instuctions)
            new_position = x.format_position()
            click.echo(f"\nNew position: {new_position}")
            break
        except CommandError:
            _invalid_input()


@click.command()
@click.version_option("1.0.0")
@click.option("--file", type=click.File("rb"), required=False, help="Path of the file.")
def main(file):
    """Rover navigation CLI"""

    if file:
        process_file(file)
    else:
        click.secho("\n---=======Mars Rover Navigation=======---\n\n", fg="blue")
        interactive()


if __name__ == "__main__":
    main()
