from time import time
from typing import Union

def add_numbers(x: int, y: Union[int, None] = None) -> int:
    """Add two numbers together.
    args:
        x (integer): The first number
        y (integer, optional): The second number

    Returns:
        integer: The sum of x and y
    """
    return x + y

def get_time():
    """Gets the current time.
    args: None

    Returns:
        string: the time as string
    """
    return str(time)

class ProgramRunningeDuration:

    def __init__(self):
        self._start = time

    def passed_since_start(self):
        """Gets the duration since the program started running.
        args: None

        Returns:
            string: the duration since the program started as string.
        """
        return str(time-self._start)

tool_functions = [
    add_numbers,
    get_time,
    ProgramRunningeDuration.passed_since_start
]