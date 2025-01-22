class LimsError(Exception):
    """Base exception for LIMS errors."""

    pass


class XMLParsingError(LimsError):
    """Raised when XML parsing fails."""

    pass
