from rest_framework import status


class InvalidUsernameException(Exception):
    """Exception raised for invalid usernames."""
    status = status.HTTP_400_BAD_REQUEST

    def __init__(self, message="Username cannot be empty"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsException(Exception):
    """Exception raised when a user already exists."""
    status = status.HTTP_303_SEE_OTHER

    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message) 