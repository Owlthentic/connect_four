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

    # def key_pressed(self) -> bool:
    #     """
    #     Check if a key has been pressed.
    # 
    #     Returns:
    #         bool: True if a key is pressed, False otherwise.
    #     """
    #     

    def read_key(self):
        """
        Read a key from the console and return its corresponding key code.

        Returns:
            Enum: The key code corresponding to the pressed key.
        """
        
        while True:
            input_list = []
            input_list = self.sense.stick.get_events()

            if input_list != [] and input_list[0].action == "pressed":
                direction = input_list[0].direction

                if direction == "middle":
                    return Keys.ENTER
                elif direction == "up":
                    return Keys.UP
                elif direction == "right":
                    return Keys.RIGHT
                elif direction == "down":
                    return Keys.DOWN
                elif direction == "left":
                    return Keys.LEFT


if __name__ == "__main__":
    input = InputSense()
    input.read_key()
