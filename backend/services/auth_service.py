# services/auth_service.py
# All authentication logic has been moved to core/security.py and routers/auth.py.
# This file is kept for backwards compatibility.
from core.security import (  # noqa: F401
    hash_password,
    verify_password,
    create_access_token,
    create_password_reset_token,
    verify_password_reset_token,
    get_current_user,
)
