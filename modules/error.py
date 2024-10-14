# Contains errors for program

import sys

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

class SQLServerError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)