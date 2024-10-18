# Contains errors for program

import sys

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

# This provides colors for output in terminal
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# General SQL Server Exceptions
class SQLServerError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(f"{color.RED}{color.BOLD}SQLServerError: {message}{color.END}")

# Exceptions related to schema or missing schema files
class SchemaError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(f"{color.RED}{color.BOLD}SchemaError: {message}{color.END}")

# Exceptions regarding locking and unlocking constraints on a table
class ConstraintError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(f"{color.RED}{color.BOLD}ConstraintError: {message}{color.END}")