"""
Python bindings for the telegraf Rust client library.

This module provides Python bindings for the telegraf Rust client,
allowing you to send metrics to Telegraf agents from Python applications.
"""

from ._telegraf_client import Client, Point, TelegrafBindingError

__version__ = "0.1.2"
__all__ = ["Client", "Point", "TelegrafBindingError"]
