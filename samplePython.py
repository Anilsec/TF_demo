from Forensics.EC2_capture import initLogger, options
from pythonjsonlogger import jsonlogger
from unittest.mock import patch, MagicMock
import logging
import pytest
import sys

class TestEC2Capture:

    def test_initLogger_json_output(self):
        """
        Test initLogger when options.output is set to 'json'
        """
        # Mock the options object
        mock_options = MagicMock()
        mock_options.output = 'json'

        # Patch the global options object
        with patch('Forensics.EC2_capture.options', mock_options):
            # Patch the logger
            mock_logger = MagicMock()
            with patch('Forensics.EC2_capture.logger', mock_logger):
                # Call the function
                initLogger()

                # Assertions
                assert mock_logger.level == logging.DEBUG
                mock_logger.addHandler.assert_called_once()
                
                # Check if JsonFormatter is used
                handler = mock_logger.addHandler.call_args[0][0]
                assert isinstance(handler.formatter, jsonlogger.JsonFormatter)

                # Check if StreamHandler is used with sys.stderr
                assert isinstance(handler, logging.StreamHandler)
                assert handler.stream == sys.stderr

class TestEc2Capture:

    @patch('Forensics.EC2_capture.logging')
    @patch('Forensics.EC2_capture.sys')
    def test_initLogger_2(self, mock_sys, mock_logging):
        """
        Test initLogger when output is not 'json'
        """
        # Setup
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger
        options.output = 'text'

        # Execute
        initLogger()

        # Assert
        assert mock_logger.level == logging.DEBUG
        mock_logging.Formatter.assert_called_once_with('%(asctime)s - %(message)s')
        mock_logging.StreamHandler.assert_called_once_with(mock_sys.stderr)
        mock_logger.addHandler.assert_called_once()

        formatter = mock_logging.Formatter.return_value
        assert formatter.formatTime == loggerTimeStamp

        handler = mock_logging.StreamHandler.return_value
        handler.setFormatter.assert_called_once_with(formatter)

    def test_initLogger_exception_handling(self):
        """
        Test initLogger's exception handling when StreamHandler fails.
        """
        def mock_stream_handler(*args, **kwargs):
            raise Exception("Mock StreamHandler exception")

        original_stream_handler = logging.StreamHandler
        logging.StreamHandler = mock_stream_handler

        try:
            with pytest.raises(Exception):
                initLogger()
        finally:
            logging.StreamHandler = original_stream_handler

    def test_initLogger_invalid_output(self):
        """
        Test initLogger with an invalid output option.
        """
        options.output = 'invalid'
        initLogger()
        assert logger.level == logging.DEBUG
        assert isinstance(logger.handlers[0], logging.StreamHandler)
        assert isinstance(logger.handlers[0].formatter, logging.Formatter)

    def test_initLogger_json_output(self):
        """
        Test initLogger with JSON output option.
        """
        options.output = 'json'
        initLogger()
        assert logger.level == logging.DEBUG
        assert isinstance(logger.handlers[0], logging.StreamHandler)
        assert isinstance(logger.handlers[0].formatter, jsonlogger.JsonFormatter)

    def test_initLogger_multiple_calls(self):
        """
        Test initLogger being called multiple times to ensure it doesn't add duplicate handlers.
        """
        initLogger()
        initial_handler_count = len(logger.handlers)
        initLogger()
        assert len(logger.handlers) == initial_handler_count

    def test_initLogger_no_output(self):
        """
        Test initLogger with no output option set.
        """
        options.output = None
        initLogger()
        assert logger.level == logging.DEBUG
        assert isinstance(logger.handlers[0], logging.StreamHandler)
        assert isinstance(logger.handlers[0].formatter, logging.Formatter)

    def test_initLogger_sys_stderr_unavailable(self):
        """
        Test initLogger when sys.stderr is not available.
        """
        original_stderr = sys.stderr
        sys.stderr = None

        try:
            with pytest.raises(AttributeError):
                initLogger()
        finally:
            sys.stderr = original_stderr