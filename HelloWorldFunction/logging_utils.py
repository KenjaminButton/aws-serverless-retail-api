# HelloWorldFunction/logging_utils.py
import json, logging, os, time
from typing import Callable, Dict, Any

# Configure root logger once (reused across warm Lambdas)
_logger = logging.getLogger()
if not _logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter('%(message)s'))  # we'll emit JSON strings
    _logger.addHandler(h)
_logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

def log_json(**kwargs) -> None:
    """Emit a single JSON object per log line."""
    _logger.info(json.dumps(kwargs, separators=(",", ":")))

def with_request_metrics(handler: Callable[[Dict[str, Any], Any], Dict[str, Any]]):
    """Measure latency and log a summary for every invocation."""
    def _wrap(event: Dict[str, Any], context: Any):
        t0 = time.time()
        resp: Dict[str, Any] = {}
        try:
            resp = handler(event, context) or {}
            return resp
        finally:
            latency_ms = int((time.time() - t0) * 1000)
            rc = event.get("requestContext", {})
            http = rc.get("http", {})
            log_json(
                service=os.getenv("POWERTOOLS_SERVICE_NAME", "cards-api"),
                level="INFO",
                event="request_summary",
                requestId=getattr(context, "aws_request_id", None),
                method=http.get("method"),
                path=http.get("path"),
                statusCode=(resp.get("statusCode", 200) if isinstance(resp, dict) else 200),
                latencyMs=latency_ms
            )
    return _wrap
