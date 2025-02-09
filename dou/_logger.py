import os
import sys
from json import dumps
from typing import Any, Dict, Optional, Union

from loguru import logger as loguru_logger
from pydantic import BaseModel, Field


class _Log(BaseModel):
    search_id: Optional[str] = Field(None, description="검색 식별값")
    message: Union[str, Dict[str, Any]] = Field(..., description="내용")


class _Logger:
    def __init__(self):
        loguru_logger.remove()

        if not os.path.exists("logs"):
            os.makedirs("logs")

        loguru_logger.add(
            "logs/{time:YYYY-MM-DD}.log",
            rotation="00:00",
            retention="31 days",
            enqueue=True,
            backtrace=False,
            diagnose=False,
        )

        loguru_logger.add(
            sys.stdout,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>",
        )
        self._logger = loguru_logger

    def _log(
        self,
        level: str,
        message: Any,
        search_id: Optional[str] = None,
    ) -> None:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {level}")

        if isinstance(message, str) and search_id is None:
            formatted_message = message

        elif isinstance(message, (dict, list)):
            log_data = _Log(search_id=search_id, message=message)
            formatted_message = dumps(log_data.model_dump(), ensure_ascii=False, indent=4)

        elif isinstance(message, BaseModel):
            log_data = _Log(search_id=search_id, message=message.model_dump())
            formatted_message = dumps(log_data.model_dump(), ensure_ascii=False, indent=4)

        elif hasattr(message, '__dict__'):
            log_data = _Log(search_id=search_id, message=message.__dict__)
            formatted_message = dumps(log_data.model_dump(), ensure_ascii=False, indent=4)

        else:
            formatted_message = str(message)

        bound_logger = loguru_logger.bind().opt(depth=2)
        if level.upper() == "ERROR":
            bound_logger = bound_logger.opt(exception=True)

        bound_logger.log(level.upper(), formatted_message)

    def info(
        self, message: Any, search_id: Optional[str] = None
    ) -> None:
        self._log("INFO", message, search_id)

    def debug(
        self, message: Any, search_id: Optional[str] = None
    ) -> None:
        self._log("DEBUG", message, search_id)

    def warning(
        self, message: Any, search_id: Optional[str] = None
    ) -> None:
        self._log("WARNING", message, search_id)

    def error(
        self, message: Any, search_id: Optional[str] = None
    ) -> None:
        self._log("ERROR", message, search_id)

