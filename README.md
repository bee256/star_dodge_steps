# Star Dodge Steps

Star Dodge Steps is used as a step-by-step approach to building a simple 2D game.
The goal of this project is to let students in a class follow the creation of the game step by step.
Along the way, the class learns a lot about Python, the [Pygame 2D library](https://www.pygame.org) and object-oriented
programming principles.

The idea is to let the students make the changes themselves, and a solution can be shown by the difference between
between `main[x].py` and `main[x+1].py*`. IDEs like PyCharm are very useful for this.

Particularly fun is `main11.py`. It introduces a pause mode (by using the space bar), but there is a bug that causes a
huge amount of stars to fall down, as stars are continuously generated and added to an array during the pause. This is
of course fixed in `main12.py`.

The last file, `main14.py`, marks the end of this project and also displays a message that it is not good coding
practice to have everything in one file. This will be completely changed and refactored in the ‘final’
project [Star Dodge](https://github.com/bee256/star_dodge). See that project for more documentation.

## Installation

### Prerequisites

- Python 3.12 and later
- Required libraries listed in `requirements.txt`

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Credits

Thanks to *Tech With Tim* and his YouTube
video [How to Make a Game in Python](https://youtu.be/waY3LfJhQLY?si=OrJKlrRDu99h5lpH).

## Related Projects

[Star Dodge](https://github.com/bee256/star_dodge)
