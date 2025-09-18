from typing import List
from typing import Optional

from fastapi import Request
from src.db.auth import credentials

class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get(
            "email"
        )  # since outh works on username field we are considering email as username
        self.password = form.get("password")

    async def _is_authenticated(self):
        if self.username == credentials["username"] and self.password == credentials["password"]:
            return True
        else:
            return False

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        is_authenticated = await self._is_authenticated()
        if not self.errors and is_authenticated:
            return True
        return False