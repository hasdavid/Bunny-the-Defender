# Bunny the Defender

One of my first Python programs, a simple game written in Python 3. The player takes the role of a warrior bunny, who has to defend his castle against a horde of badgers. The goal of the project was to play with and explore Python, it's module PyGame and object-oriented programming.

## Screenshot

![Screenshot](/other/screenshot.png)

## Running the game

Download the repository, start a command line and navigate to the main folder. Launch as a script
`./game.py` or using the Python interpreter `python3 ./game.py`.

## Controls

The bunny moves with keys `w`, `a`, `s`, `d` and turns by following the mouse cursor. After a click he shoots an arrow.

## Possible future updates

The code is not as beautiful as it could be. I am aware that there are some incomplete docstrings and that the three main classes - Player, Arrow and Badger - would deserve a common superclass called for example Entity, since they share some similar or even same methods and attributes.

Also I noticed there is a much better representation of such entity already implemented in PyGame - it is called Sprite. I may refactor the code using this module later.

Another thing would be to remove the dependency on the "point" library. At first I thought that would bring some functionality which PyGame was missing, but it turned out to be more of a nuisance and made the code more unclear.

Please, feel free to share your own remarks. I am still new to object-oriented programming and will welcome any advice.

## Credit

The graphics and music in the game come from [this guy](https://www.raywenderlich.com/2795-beginning-game-programming-for-teens-with-python).

I did not come up with the concept. I just recreated the game using object-oriented paradigm and rewrote the code as I thought would be better. All the credit still goes to the original author.
