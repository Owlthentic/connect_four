from enum import Enum


class Keys(Enum):
    """
    Enum class representing different key codes for input handling.
    """
    UNKNOWN = -1   # Unknown key code
    UP = -2       # Key code for the up arrow
    DOWN = -3     # Key code for the down arrow
    LEFT = -4     # Key code for the left arrow
    RIGHT = -5    # Key code for the right arrow
    ENTER = 13    # Key code for the Enter key
    ESC = 27      # Key code for the Escape key


class InputBase:
    """
    Base class for handling input operations.

    This class defines the interface for reading key inputs.
    Subclasses must implement the `read_key` method.
    """

    def read_key(self) -> Keys:
        """
        Read a key input and return its corresponding key code.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError()
