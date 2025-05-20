import os
import sys

from loguru import logger as loguru_logger


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

        log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()
        serialize_logs = os.getenv("LOG_SERIALIZE", "false").lower() == "true"
        log_sink_str = os.getenv("LOG_SINK", "stderr").lower()

        if log_sink_str == "stdout":
            log_sink = sys.stdout
        elif log_sink_str == "stderr":
            log_sink = sys.stderr
        else:
            log_sink = log_sink_str

        log_format = (
            "{time} {level} {message} {extra}"  # JSON 형식
            if serialize_logs
            else "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> | <yellow>{extra}</yellow>"  # 가독성 좋은 텍스트 형식 (예시)
        )

        loguru_logger.add(
            log_sink,
            level=log_level,  # 로그 레벨
            format=log_format,  # 로그 포맷
            serialize=serialize_logs,  # JSON 직렬화 여부
            enqueue=True,  # 비동기 로깅 활성화 (I/O 블로킹 방지)
            catch=True,
        )

        self.logger = loguru_logger
        self.logger.info(
            f"Logging setup complete. Level: {log_level}, Serialize: {serialize_logs}, Sink: {log_sink_str}"
        )
