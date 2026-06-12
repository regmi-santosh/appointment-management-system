class UserAlreadyExists(Exception):
    """Raised when attempting to create a user with an email that already exists."""


class UserNotFound(Exception):
    """Raised when a user cannot be found by id or other identifier."""


class RepositoryError(Exception):
    """Generic repository error."""
