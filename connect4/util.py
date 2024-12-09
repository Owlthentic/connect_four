import os
import platform


class Util:

    @classmethod
    # @property
    def isRaspberry(cls) -> bool:
        if os.name == "posix":
            if platform.system() == "Linux":
                if platform.machine() == "armv7l" or platform.machine() == "aarch64":
                    return True
        return False


if __name__ == '__main__':
    print(f"Raspberry Pi: {Util.isRaspberry()}")
