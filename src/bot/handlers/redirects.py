import inspect
from functools import wraps
from typing import Callable


class Redirects:
    callback_map: dict[str, Callable] = {}

    def register_redirect(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        self.callback_map[func.__name__] = wrapper

        return wrapper

    async def redirect(self, name: str, **data) -> None:
        callback = self.callback_map[name]

        sig = inspect.signature(callback)
        args = [param.name for param in sig.parameters.values()]

        await callback(**{arg: data[arg] for arg in args})


redirects = Redirects()