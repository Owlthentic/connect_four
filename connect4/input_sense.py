from input_base import InputBase
from input_base import Keys
from sense_hat import SenseHat


class InputSense(InputBase):
    def __init__(self):
        self.sense = SenseHat()
        self._events = {}
    """
    Input handler for console applications using keyboard input.
    """

    def key_pressed(self) -> bool:
        """
        Check if a key has been pressed.

        Returns:
            bool: True if a key is pressed, False otherwise.
        """
        if self.sense.stick.get_events() == self._events:
           return False
        else:
            self._events = self.sense.stick.get_events()
            return True

    def read_key(self):
        """
        Read a key from the console and return its corresponding key code.

        Returns:
            Enum: The key code corresponding to the pressed key.
        """
        
        key = self.sense.stick.get_events()[-1]
        print(key)


if __name__ == "__main__":
    input = InputSense()
    input.read_key()
