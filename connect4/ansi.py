class Ansi:
    """
    A class to handle ANSI escape codes for terminal text formatting.
    """

    def set_foreground(color: int, intensity: bool) -> None:
        """
        Set the foreground color of the text.

        Parameters:
        - color: The color code (0-7 for standard colors).
        - intensity: Boolean indicating if the color should be bright (True) or normal (False).
        """
        if intensity:
            print(f"\033[{color + 90}m", end='')
        else:
            print(f"\033[{color + 30}m", end='')

    def set_background(color: int, intensity: bool) -> None:
        """
        Set the background color of the text.

        Parameters:
        - color: The color code (0-7 for standard colors).
        - intensity: Boolean indicating if the color should be bright (True) or normal (False).
        """
        if intensity:
            print(f"\033[{color + 100}m", end='')
        else:
            print(f"\033[{color + 40}m", end='')

    def reset() -> None:
        """Reset all text formatting to default settings."""
        print(f"\033[0m", end='')

    def clear_line() -> None:
        """Clear the current line in the terminal."""
        print(f"\033[2K", end='')

    def clear_screen() -> None:
        """Clear the entire screen in the terminal."""
        print(f"\033[2J", end='')

    def gotoXY(x: int, y: int) -> None:
        """
        Move the cursor to a specific position in the terminal.

        Parameters:
        - x: The horizontal position (column).
        - y: The vertical position (row).
        """
        print(f"\033[{y};{x}H", end='')
