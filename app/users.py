"""Compatibility shim: re-export router from refactored API module.

This file keeps the `app.users` import path working while the canonical
implementation lives under `app.api.users`.
"""

from .api.users import router

