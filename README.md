# RubiksCube
Simulator for a Rubik's cube using Pygame + OpenGL.

## Context

A Rubik's cube is a popular mechanical puzzle that involves turning the various faces in order to arrive at a "solved" configuration. While seemingly simple, the puzzle can be deceptively difficult to solve.

There are six different faces on the cube. We will represent these as U, F, R, B, L, D for Up, Front, Right, Back, Left, Down respectively. Each of these faces can either be turned "forward" or "backward" - if we want to turn it backward, we use the ' symbol in the notation. We will also need a notation for rotating the entire cube itself. We can use the letters x, y, and z to represent the three different rotations. While these rotations aren't strictly necessary for solving the cube, some algorithms do utilize them.

For example, an algorithm involving rotating the top face clockwise, then rotating the entire cube along the x-axis (so now the front face is on top) and then rotating the right face downward, would be written as: U x R'

## Logic

This program is composed of three files:
- `RubiksCube.py`: This file handles all internal logic related to the Rubik's cube, including storing the colors on the faces and the algorithms for turning each one.
- `engine.py`: This file actually creates the `pygame` window and handles the logic that allows the simulation to run. To run the simulation, run `python3 engine.py`
- `button.py`: Because the simulation itself is 3-D and can be dragged around, we need a separate class for all the buttons, which are 2-D and need to stay in place the whole time.

Special thanks to [Acash2018](https://github.com/Acash2018) for helping me get the text on the buttons to render properly.

## Demo

Here the program is used to perform an N perm (algorithm: R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R') to complete a partially solved Rubik's cube:

![demo](https://github.com/user-attachments/assets/97cf157e-edbd-4fc1-8266-bbd8d9f69188)
