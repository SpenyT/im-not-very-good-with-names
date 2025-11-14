# this is solely created to show default implementation of test cases
# change in future probably

import logging

logger = logging.getLogger(__name__)


def validate_file_size(file, max_size_mb: int = 10) -> bool:
    """
    Validate uploaded file size.

    Args:
        file: Uploaded file object (Django UploadedFile)
        max_size_mb: Maximum allowed size in MB

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_file_size(uploaded_file, max_size_mb=5)
        True
    """
    if not file:
        return False

    max_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
    return file.size <= max_size


# more util functions here
