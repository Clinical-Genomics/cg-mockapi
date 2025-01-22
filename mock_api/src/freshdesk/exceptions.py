class FreshdeskError(Exception):
    """Base exception for Freshdesk related errors."""

    pass


class InvalidTicketDataError(FreshdeskError):
    """Raised when ticket data is invalid."""

    pass


class AttachmentError(FreshdeskError):
    """Raised when there's an issue with attachments."""

    pass
