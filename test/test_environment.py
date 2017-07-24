# -*- coding: utf-8 -*-
"""
Basic environment tests to make sure everything is set up correctly
"""

import sys
import os
import pytest

# Ensure that 'tabfileio' is imported from parent directory.
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(base))

try:
    import tabfileio as tfio
except ImportError:
    tfio = None


def test_absolute_truth():
    """Ensure that the testing library is working."""
    assert True


def test_capture_output(capsys):
    """Test that the capturing of stdout works."""
    print("hello world")
    out, err = capsys.readouterr()
    assert out == "hello world\n"
    assert err == ""


def test_import():
    """Ensure that 'tfio' is imported."""
    assert tfio is not None

