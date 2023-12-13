class AppException(Exception):
    """Base class for App Exception"""

    def __init__(self, detail: str):
        self.detail = detail


class UnknownClientException(AppException):
    """Unknown Client requesting service"""
    pass
