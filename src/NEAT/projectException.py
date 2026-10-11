# Ce fichier sert à définir nos propres exceptions
class CoucheError(Exception):
    """Base class for exceptions in this module."""
    pass

class CoucheIsoleeError(CoucheError):
    """

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class CoucheVideError(CoucheError):
    """

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class LoggerError(Exception):
    """Exception levée en cas d'erreur avec le Logger."""
    def __init__(self, message):
        self.message = message