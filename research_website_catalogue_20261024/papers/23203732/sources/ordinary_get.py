#!/usr/bin/env python3
"""New ordinary Zenodo GET custody. No scientific/project imports or bypasses."""
from pathlib import Path
from urllib.parse import urlsplit, urljoin
from datetime import datetime, timezone
import hashlib
import http.client
import json
import sys

ROOT = Path(__file__).resolve().parent


def utc():
    return datetime.now(timezone.utc).isoformat()


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


class Connection(http.client.HTTPSConnection):
    def send(self, data):
        if isinstance(data, (bytes, bytearray, memoryview)):
            self.actual_sent.extend(bytes(data))
        return super().send(data)


def fetch(url, role, accept="application/json", asset=False):
    require(role and all(c.isalnum() or c in "-_." for c in role), "unsafe role")
    receipts_path = ROOT / "ALL_TRANSPORT_RECEIPTS.json"
    receipts = json.loads(receipts_path.read_bytes()) if receipts_path.exists() else []
    redirects, current = [], url
    for hop in range(6):
        u = urlsplit(current)
        require(u.scheme == "https" and u.hostname == "zenodo.org" and not u.username and not u.password, "ordinary native Zenodo target required")
        target = (u.path or "/") + ("?" + u.query if u.query else "")
        stem = role + ".response.body" + ("" if hop == 0 else ".redirect-%02d" % hop)
        destination = ROOT / stem
        sent_path = ROOT / (stem + ".actual-request.bin")
        require(not destination.exists() and not sent_path.exists(), "never overwrite a transport; preserve failed attempts")
        headers = [["Host", u.netloc], ["User-Agent", "Python-http.client (source-only custody)"], ["Accept", accept]]
        start = utc()
        c = Connection(u.hostname, u.port or 443, timeout=45)
        c.actual_sent = bytearray()
        status, reason, received, chunks, complete, error = None, None, [], [], False, None
        try:
            c.putrequest("GET", target, skip_host=True, skip_accept_encoding=True)
            for k, v in headers:
                c.putheader(k, v)
            c.endheaders()
            response = c.getresponse()
            status, reason, received = response.status, response.reason, list(response.headers.raw_items())
            while True:
                block = response.read1(65536)
                if not block:
                    break
                chunks.append(block)
            lengths = [v for k, v in received if k.lower() == "content-length"]
            if lengths:
                require(len(set(lengths)) == 1 and int(lengths[0]) == sum(map(len, chunks)), "partial native body versus Content-Length")
            complete = True
        except Exception as exc:
            error = exc
        finally:
            c.close()
            body = b"".join(chunks)
            destination.write_bytes(body)
            sent_path.write_bytes(c.actual_sent)
            row = {"started_UTC": start, "completed_UTC": utc(), "logical_role": role, "redirect_hop": hop, "method": "GET", "request_URL": current, "actual_request_headers_in_sent_order": headers, "actual_sent_request_bytes_path": str(sent_path), "actual_sent_request_bytes": len(c.actual_sent), "actual_sent_request_SHA256": hashlib.sha256(c.actual_sent).hexdigest(), "HTTP_status": status, "HTTP_reason": reason, "response_headers_in_received_order": received, "body_path": str(destination), "bytes": len(body), "SHA256": hashlib.sha256(body).hexdigest(), "whole_native_response_body_complete": complete, "all_received_body_bytes_preserved_before_followup": True, "error_type": type(error).__name__ if error else None, "error_message": str(error) if error else None}
            receipts.append(row)
            receipts_path.write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + "\n")
            (ROOT / (stem + ".transport.json")).write_text(json.dumps(row, ensure_ascii=False, indent=2) + "\n")
        if error:
            raise error
        if status in [301, 302, 303, 307, 308]:
            locations = [v for k, v in received if k.lower() == "location"]
            require(len(locations) == 1, "ambiguous actual native redirect")
            redirects.append({"status": status, "actual_Location": locations[0]})
            current = urljoin(current, locations[0])
            continue
        require(status == 200, "non200 complete native body preserved: " + str(status))
        return body, row, redirects
    raise RuntimeError("bounded six-hop redirect limit; all actual bodies retained")


if __name__ == "__main__":
    require(len(sys.argv) == 3, "explicit URL and new role required")
    body, row, redirects = fetch(sys.argv[1], sys.argv[2])
    print(json.dumps({"HTTP_status": row["HTTP_status"], "bytes": len(body), "SHA256": row["SHA256"], "redirects": redirects}))
