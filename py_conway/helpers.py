"""Helper functions and classes."""


class PseudoEnum(set):
    """Create a pseudo-enum based on provided values."""

    def __getattr__(self, name):
        """Create enum based on provided names."""
        if name in self:
            return name
        raise AttributeError
