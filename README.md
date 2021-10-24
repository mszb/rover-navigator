# MARS Rover Navigation

A command line interface to navigate rover naviation.

A rover's position is represented by a combination of an x and y co-ordinates and a letter representing one of the four cardinal compass points. The plateau is divided up into a grid to simplify navigation. An example position might be 0, 0, N, which means the rover is in the bottom left corner and facing North.

In order to control a rover, NASA sends a simple string of letters. The possible letters are 'L', 'R' and 'M'. 'L' and 'R' makes the rover spin 90 degrees left or right respectively, without moving from its current spot.

'M' means move forward one grid point, and maintain the same heading.

## Installation:

`pip install -r requirements.txt`
(Supports Python 3)

## Usage

CLI support interactive interface and file input.

To run the cli using file input:

`python app.py --file=example.txt`

To run interactive command prompt, run:

`python app.py`

## Testing

Command: `pytest`

With coverage: `coverage run -m pytest && coverage report -m`

```
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
app.py                         57      1    98%   103
rover/__init__.py               0      0   100%
rover/exceptions.py             2      0   100%
rover/rover_navigation.py      84      0   100%
---------------------------------------------------------
TOTAL                         143      1    99%
```
