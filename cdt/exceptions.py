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
    def __init__(self, message="sos idiota ? ese ya existe"):
        self.message = message
        super().__init__(self.message)


class UserIdRequiredException(Exception):
    """Exception raised when user_id is not provided."""
    status = status.HTTP_400_BAD_REQUEST
    def __init__(self, message="user_id is required"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    """Exception raised when user is not found."""
    status = status.HTTP_404_NOT_FOUND
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)


class PreferenciasNotFoundException(Exception):
    """Exception raised when preferences are not found."""
    status = status.HTTP_404_NOT_FOUND
    def __init__(self, message="Preferences not found"):
        self.message = message
        super().__init__(self.message)


class ValidationException(Exception):
    """Exception raised for validation errors."""
    status = status.HTTP_400_BAD_REQUEST
    def __init__(self, message="Validation error"):
        self.message = message
        super().__init__(self.message) 