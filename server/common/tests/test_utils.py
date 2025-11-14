from django.test import TestCase
from unittest.mock import Mock

from common.utils import (
    validate_file_size,
    # add more from utils
)

class ValidateFileSizeTestCase(TestCase):
    """Test cases for validate_file_size function."""

    def test_valid_file_size(self):
        """Test that valid file size passes validation."""
        mock_file = Mock()
        mock_file.size = 5 * 1024 * 1024  # 5MB

        result = validate_file_size(mock_file, max_size_mb=10)
        self.assertTrue(result)

    def test_file_too_large(self):
        """Test that oversized file fails validation."""
        mock_file = Mock()
        mock_file.size = 15 * 1024 * 1024  # 15MB

        result = validate_file_size(mock_file, max_size_mb=10)
        self.assertFalse(result)

    def test_exact_size_limit(self):
        """Test file exactly at size limit passes."""
        mock_file = Mock()
        mock_file.size = 10 * 1024 * 1024  # 10MB

        result = validate_file_size(mock_file, max_size_mb=10)
        self.assertTrue(result)

    def test_none_file(self):
        """Test that None file returns False."""
        result = validate_file_size(None)
        self.assertFalse(result)

    def test_custom_size_limit(self):
        """Test with custom size limit."""
        mock_file = Mock()
        mock_file.size = 3 * 1024 * 1024  # 3MB

        result = validate_file_size(mock_file, max_size_mb=5)
        self.assertTrue(result)
