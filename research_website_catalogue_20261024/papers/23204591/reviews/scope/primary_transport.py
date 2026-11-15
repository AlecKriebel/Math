#!/usr/bin/env python3
"""Explicit ordinary public HTTPS GET custody. Default mode does nothing.

No target or project imports, cookies, authentication, proxy, retry, bypass,
login or purchase. Every HTTP status/body and redirect is retained literally.
The explicit --fetch mode writes only the owned primary directory.
"""
from pathlib import Path
from urllib.parse import urlsplit, urljoin
import datetime
import hashlib
import http.client
import json
import sys

ROOT = Path(__file__).resolve().parent
MAX_BYTES = 128 * 1024 * 1024
MAX_HOPS = 8


def require(value, message):
    if not value:
        raise RuntimeError(message)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fetch(url, label):
    require(label and all(c.isascii() and (c.isalnum() or c in '-_.') for c in label),
            'Unsafe fresh request label')
    require((ROOT / 'primary').is_dir() and not (ROOT / 'primary').is_symlink(), 'Owned primary directory required')
    chain = []
    current = url
    started = utc()
    for hop in range(MAX_HOPS):
        require(not any(ord(c) < 32 or ord(c) == 127 for c in current), 'URL control character')
        parsed = urlsplit(current)
        require(parsed.scheme == 'https' and parsed.hostname and parsed.username is None and
                parsed.password is None and parsed.port in (None, 443) and not parsed.fragment,
                'Only public unauthenticated standard HTTPS URLs')
        target = (parsed.path or '/') + ('?' + parsed.query if parsed.query else '')
        target.encode('ascii')
        headers = [['Host', parsed.netloc], ['User-Agent', 'Independent mathematical primary-source custody'],
                   ['Accept', 'application/pdf, application/json, text/plain, text/html, */*'],
                   ['Accept-Encoding', 'identity'], ['Connection', 'close']]
        request = ('GET ' + target + ' HTTP/1.1\r\n' +
                   ''.join(k + ': ' + v + '\r\n' for k, v in headers) + '\r\n').encode('ascii')
        stem = label + '-hop' + str(hop)
        body_path = ROOT / 'primary' / (stem + '.body')
        transport_path = ROOT / 'primary' / (stem + '.transport.json')
        request_path = ROOT / 'primary' / (stem + '.request.bin')
        require(not any(p.exists() for p in (body_path, transport_path, request_path)),
                'Preserve existing attempt; use a new label')
        request_path.write_bytes(request)
        receipt = {'started_UTC': utc(), 'method': 'GET', 'URL': current, 'redirect_hop': hop,
                   'actual_request_headers_in_sent_order': headers,
                   'prepared_request_bytes_path': str(request_path),
                   'prepared_request_bytes': len(request), 'prepared_request_SHA256': sha(request),
                   'request_send_completed': False, 'HTTP_status': None, 'HTTP_reason': None,
                   'response_headers_in_received_order': None, 'body': None, 'bytes': None,
                   'SHA256': None, 'whole_response_body_complete': False,
                   'authentication_cookies_proxy_retry_or_bypass': False,
                   'error_type': None, 'error': None}
        connection = http.client.HTTPSConnection(parsed.hostname, 443, timeout=40)
        try:
            connection.connect()
            connection.send(request)
            receipt['request_send_completed'] = True
            response = http.client.HTTPResponse(connection.sock, method='GET')
            response.begin()
            receipt['HTTP_status'] = response.status
            receipt['HTTP_reason'] = response.reason
            receipt['response_headers_in_received_order'] = [list(pair) for pair in response.getheaders()]
            body = response.read(MAX_BYTES + 1)
            body_path.write_bytes(body)
            receipt['body'] = body_path.relative_to(ROOT).as_posix()
            receipt['bytes'] = len(body)
            receipt['SHA256'] = sha(body)
            receipt['whole_response_body_complete'] = len(body) <= MAX_BYTES
            if len(body) > MAX_BYTES:
                receipt['error_type'] = 'AcquisitionBodyCap'
                receipt['error'] = 'Response exceeds128MiB; preserved prefix is not a complete primary body.'
        except Exception as error:
            receipt['error_type'] = type(error).__name__
            receipt['error'] = str(error)
        finally:
            connection.close()
        receipt['completed_UTC'] = utc()
        transport_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
        chain.append(receipt)
        if receipt['error'] is not None:
            break
        if receipt['HTTP_status'] in (301, 302, 303, 307, 308):
            locations = [v for k, v in receipt['response_headers_in_received_order'] if k.lower() == 'location']
            if len(locations) != 1:
                break
            current = urljoin(current, locations[0])
            continue
        break
    return {'started_UTC': started, 'completed_UTC': utc(), 'label': label, 'initial_URL': url,
            'literal_request_chain': chain, 'terminal_HTTP_status': chain[-1]['HTTP_status'],
            'terminal_body': chain[-1]['body'], 'terminal_bytes': chain[-1]['bytes'],
            'terminal_SHA256': chain[-1]['SHA256'],
            'terminal_body_complete': chain[-1]['whole_response_body_complete'],
            'error': chain[-1]['error'], 'no_retry_or_access_bypass': True,
            'scientific_body_interpreted_by_transport': False}


def main():
    if len(sys.argv) == 1:
        print(json.dumps({'mode': 'pure default; no action', 'network_requests': 0,
                          'filesystem_writes': 0, 'scientific_execution': False}))
        return
    require(len(sys.argv) == 4 and sys.argv[1] == '--fetch',
            'Only explicit --fetch URL fresh-label performs acquisition')
    print(json.dumps(fetch(sys.argv[2], sys.argv[3]), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
