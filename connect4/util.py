import os
import platform


class Util:
    """
    Class Util with static method isRaspberry(cls) that checks if the current system is a Raspberry Pi by checking the OS name, system platform, and machine architecture.
    Returns True if the system is a Raspberry Pi, otherwise returns False.
    """
    @classmethod
    # @property
    def isRaspberry(cls) -> bool:
        """
        Check if the current system is a Raspberry Pi.

        Args:
            None

        Returns:
            bool: True if the current system is a Raspberry Pi, False otherwise.
        """
        if os.name == "posix":
            if platform.system() == "Linux":
                if platform.machine() == "armv7l" or platform.machine() == "aarch64":
                    return True
        return False


if __name__ == '__main__':
    print(f"Raspberry Pi: {Util.isRaspberry()}")
