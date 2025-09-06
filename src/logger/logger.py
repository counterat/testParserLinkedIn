import json
import logging

from config import FILE_FOR_LOGS

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "event": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_record, ensure_ascii=False)

def setup_json_logger(name="scraper", log_file=FILE_FOR_LOGS, level=logging.INFO):
    FILE_FOR_LOGS.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


logger = setup_json_logger()