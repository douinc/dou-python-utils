from ._logger import _Logger
from .cli import app

__version__ = "0.1.3"

__all__ = ["logger", "cli"]

logger = _Logger()

if __name__ == "__main__":
    app()
