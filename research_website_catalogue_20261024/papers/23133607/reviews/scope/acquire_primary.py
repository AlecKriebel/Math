#!/usr/bin/env python3
"""Explicit ordinary public primary GET; no default network or write action.

Adapted only after full reading of 23205305/reviews/scope/fetch_primary.py.
No project/native imports, authentication, cookies, proxies, retry or bypass.
"""
from pathlib import Path
import datetime
import hashlib
import http.client
import json
import ssl
import sys
from urllib.parse import urlsplit, urljoin

BASE = Path(__file__).resolve().parent

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(body):
    return hashlib.sha256(body).hexdigest()

def main():
    if len(sys.argv) != 4 or sys.argv[1] != '--acquire':
        print('Inert default. Explicit --acquire fresh-label cited-URL required.')
        return
    label, url = sys.argv[2:]
    if not label.replace('-', '').replace('_', '').isalnum():
        raise ValueError('fresh safe label required')
    dest = BASE / 'primary'
    dest.mkdir(exist_ok=True)
    for hop in range(6):
        prefix = dest / (label + '-hop' + str(hop))
        bodypath = prefix.with_suffix('.body')
        requestpath = prefix.with_suffix('.request.bin')
        receiptpath = prefix.with_suffix('.transport.json')
        if any(p.exists() for p in [bodypath, requestpath, receiptpath]):
            raise ValueError('refuse any overwrite')
        parsed = urlsplit(url)
        if parsed.scheme not in ('https', 'http') or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('public ordinary HTTP(S) URL required')
        target = parsed.path or '/'
        if parsed.query:
            target += '?' + parsed.query
        headers = [['Host', parsed.netloc], ['User-Agent', 'Python-http.client/3 primary-source-reading'], ['Accept', '*/*']]
        receipt = {'started_UTC': utc(), 'method': 'GET', 'URL': url,
                   'actual_request_headers_in_sent_order': headers,
                   'redirect_hop': hop, 'authentication_cookies_proxy_retry_or_bypass': False,
                   'HTTP_status': None, 'HTTP_reason': None, 'HTTP_version': None,
                   'response_headers_in_received_order': None, 'response_obtained': False,
                   'body_complete': False, 'error': None}
        conn = None
        sent = []
        chunks = []
        location = None
        try:
            if parsed.scheme == 'https':
                conn = http.client.HTTPSConnection(parsed.hostname, parsed.port or 443, timeout=30, context=ssl.create_default_context())
            else:
                conn = http.client.HTTPConnection(parsed.hostname, parsed.port or 80, timeout=30)
            original_send = conn.send
            def capture_send(data):
                if not isinstance(data, bytes):
                    raise TypeError('unexpected non-byte HTTP request buffer')
                sent.append(data)
                return original_send(data)
            conn.send = capture_send
            conn.putrequest('GET', target, skip_host=True, skip_accept_encoding=True)
            for key, value in headers:
                conn.putheader(key, value)
            conn.endheaders()
            response = conn.getresponse()
            receipt.update({'HTTP_status': response.status, 'HTTP_reason': response.reason,
                            'HTTP_version': response.version,
                            'response_headers_in_received_order': [list(pair) for pair in response.getheaders()],
                            'response_obtained': True})
            location = response.getheader('Location')
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                chunks.append(chunk)
            receipt['body_complete'] = True
        except Exception as error:
            if isinstance(error, http.client.IncompleteRead) and error.partial:
                chunks.append(error.partial)
            receipt['error'] = {'type': type(error).__name__, 'message': str(error)}
        finally:
            if conn:
                conn.close()
        body = b''.join(chunks)
        request = b''.join(sent)
        # Persist the entire received body, including HTTP error/redirect bodies,
        # before any following request. Empty pre-response body is explicitly so.
        bodypath.write_bytes(body)
        requestpath.write_bytes(request)
        receipt.update({'body': str(bodypath.relative_to(BASE)), 'bytes': len(body), 'SHA256': sha(body),
                        'request': str(requestpath.relative_to(BASE)), 'request_bytes': len(request),
                        'request_SHA256': sha(request), 'completed_UTC': utc()})
        receiptpath.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'transport': str(receiptpath.relative_to(BASE)), **receipt}, ensure_ascii=False))
        if receipt['body_complete'] and receipt['HTTP_status'] in (301, 302, 303, 307, 308) and location:
            url = urljoin(url, location)
            continue
        return
    raise RuntimeError('finite six-hop redirect bound reached; all actual bodies retained')

if __name__ == '__main__':
    main()
