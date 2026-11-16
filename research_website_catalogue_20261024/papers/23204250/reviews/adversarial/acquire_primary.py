"""Ordinary public GET with complete raw custody; no mathematical execution.

No auth, cookies, retries, proxy configuration, scripts or browser challenges.
Redirects follow only the actual single Location header, at most five hops.
"""
from pathlib import Path
import datetime
import hashlib
import http.client
import json
import re
import ssl
import sys
import time
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent
LIMIT = 64 * 1024 * 1024


def binding(path):
    b = path.read_bytes()
    return {"path": str(path), "bytes": len(b), "SHA256": hashlib.sha256(b).hexdigest()}


def get(url, label):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", label):
        raise ValueError("Plain unique owned label required")
    folder = ROOT / "primary"
    folder.mkdir(exist_ok=True)
    hops = []
    current = url
    for number in range(5):
        if any(c in current for c in "\r\n"):
            raise ValueError("Invalid URL line break")
        u = urlsplit(current)
        if u.scheme not in ("https", "http") or not u.hostname or u.username or u.password:
            raise ValueError("Ordinary public HTTP(S) URL required")
        stem = folder / (label + "-hop" + str(number))
        if Path(str(stem) + ".transport.json").exists():
            raise RuntimeError("Refuse duplicate GET/overwrite: " + label)
        host = u.hostname
        if u.port and u.port != (443 if u.scheme == "https" else 80):
            host += ":" + str(u.port)
        path = u.path or "/"
        if u.query:
            path += "?" + u.query
        headers = [["Host", host], ["User-Agent", "Python-http.client/3.14"],
                   ["Accept", "*/*"], ["Connection", "close"]]
        request = ("GET " + path + " HTTP/1.1\r\n" +
                   "".join(k + ": " + v + "\r\n" for k, v in headers) + "\r\n").encode("ascii")
        request_file = Path(str(stem) + ".request.bin")
        request_file.write_bytes(request)
        record = {"UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  "URL": current, "method": "GET", "sent_headers_in_exact_order": headers,
                  "actual_prepared_and_sent_request_buffer": binding(request_file),
                  "request_buffer_sent": False, "HTTP_status": None,
                  "reason": None, "response_headers_in_original_order_with_duplicates": [],
                  "body": None, "whole_body_complete": False, "transport_error": None,
                  "auth_cookies_proxy_retry_or_challenge_bypass": False}
        started = time.monotonic()
        conn = None
        try:
            if u.scheme == "https":
                conn = http.client.HTTPSConnection(u.hostname, u.port or 443, timeout=60,
                                                    context=ssl.create_default_context())
            else:
                conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=60)
            conn.connect()
            conn.send(request)
            record["request_buffer_sent"] = True
            response = http.client.HTTPResponse(conn.sock)
            response.begin()
            record["HTTP_status"] = response.status
            record["reason"] = response.reason
            record["HTTP_version"] = response.version
            record["response_headers_in_original_order_with_duplicates"] = [list(x) for x in response.getheaders()]
            try:
                body = response.read(LIMIT + 1)
            except http.client.IncompleteRead as exc:
                body = exc.partial
                record["transport_error"] = {"type": type(exc).__name__, "literal_repr": repr(exc)}
            record["whole_body_complete"] = (len(body) <= LIMIT and
                response.length in (None, 0) and record["transport_error"] is None)
            record["body_limit_bytes"] = LIMIT
            body_file = Path(str(stem) + ".body")
            body_file.write_bytes(body)
            record["body"] = binding(body_file)
            record["body_representation"] = "HTTP entity body after standard transfer decoding; no content transformation"
        except Exception as exc:
            record["transport_error"] = {"type": type(exc).__name__, "literal_repr": repr(exc)}
        finally:
            if conn is not None:
                conn.close()
        record["elapsed_seconds"] = time.monotonic() - started
        transport_file = Path(str(stem) + ".transport.json")
        transport_file.write_text(json.dumps(record, indent=2) + "\n")
        hops.append({"whole_transport": binding(transport_file), "whole_literal_transport": record})
        if record["transport_error"] is not None:
            break
        if record["HTTP_status"] not in (301, 302, 303, 307, 308):
            break
        locations = [v for k, v in record["response_headers_in_original_order_with_duplicates"] if k.lower() == "location"]
        if len(locations) != 1:
            break
        current = urljoin(current, locations[0])
    result = {"label": label, "requested_URL": url, "hops_in_actual_order": hops,
              "raw_custody_only_no_interpretations_notes_or_control_results": True,
              "terminal_HTTP_status": hops[-1]["whole_literal_transport"]["HTTP_status"],
              "whole_terminal_body": hops[-1]["whole_literal_transport"]["body"]}
    print(json.dumps(result, indent=2))
    return 1 if any(h["whole_literal_transport"]["transport_error"] is not None for h in hops) else 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: acquire_primary.py public_URL unique_label")
    raise SystemExit(get(sys.argv[1], sys.argv[2]))
