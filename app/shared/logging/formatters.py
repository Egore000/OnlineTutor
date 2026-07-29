import logging
from datetime import UTC, datetime
from typing import Any

from pythonjsonlogger.json import JsonFormatter


class CustomJsonFormatter(JsonFormatter):
    def add_fields(
        self, log_data: dict[str, Any], record: logging.LogRecord, message_dict: dict[str, Any]
    ) -> None:
        """Добавление полей в логи"""

        super().add_fields(log_data, record, message_dict)

        if not log_data.get("timestamp"):
            now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_data["timestamp"] = now

        if log_data.get("level"):
            log_data["level"] = log_data["level"].upper()
        else:
            log_data["level"] = record.levelname


formatter = JsonFormatter("%(level)s %(timestamp)s %(name)s %(message)s")
