#!/usr/bin/env python

"""Tests for `eleven_labs_script_reader` package."""


import unittest
from click.testing import CliRunner

from eleven_labs_script_reader import eleven_labs_script_reader
from eleven_labs_script_reader import cli


class TestEleven_labs_script_reader(unittest.TestCase):
    """Tests for `eleven_labs_script_reader` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'eleven_labs_script_reader.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
