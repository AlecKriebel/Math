#!/usr/bin/env python3
"""Finite ordinary raw-primary GETs with complete per-hop transport custody.

No source/scientific import or execution; writes only the new own primary/extra.
"""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit, urljoin
import hashlib
import http.client
import json
import ssl

OWN = Path(__file__).resolve().parent
OUT = OWN / 'primary/extra-v3'
REQUESTS = [
    ('gaboriau-2000-author', 'https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/Cout/Cout.pdf'),
    ('psv-v1-pdf', 'https://arxiv.org/pdf/1811.06929v1'),
    ('lueck-v1-pdf', 'https://arxiv.org/pdf/math/0310489v1'),
    ('openai-surgery-figure', 'https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-group-without-fixed-price-October-5-2026/build/surgery-figure.tex'),
]

class CapturingConnection(http.client.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actual_sent = []

    def send(self, data):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError('Only ordinary finite GET headers are expected')
        self.actual_sent.append(bytes(data))
        return super().send(data)

class CapturingHTTPConnection(http.client.HTTPConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actual_sent = []

    def send(self, data):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError('Only ordinary finite GET headers are expected')
        self.actual_sent.append(bytes(data))
        return super().send(data)

def now():
    return datetime.now(timezone.utc).isoformat()

def bind(path, body):
    with path.open('xb') as f:
        f.write(body)
    return {'path': str(path), 'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}

def main():
    if OUT.exists():
        raise ValueError('New raw-primary namespace must be absent')
    OUT.mkdir()
    all_receipts = []
    receipt_log = (OUT / 'TRANSPORT_HOPS.jsonl').open('x')
    for role, initial_url in REQUESTS:
        current = initial_url
        for hop in range(6):
            row = {'role': role, 'redirect_hop': hop, 'UTC_started': now(), 'method': 'GET', 'request_URL': current}
            parsed = urlsplit(current)
            if parsed.scheme not in ['https', 'http'] or parsed.username or parsed.password:
                raise ValueError('Ordinary HTTP(S) URL required')
            target = parsed.path or '/'
            if parsed.query:
                target += '?' + parsed.query
            headers = [('Host', parsed.netloc), ('User-Agent', 'Python-http.client (raw-primary-custody)'), ('Accept', '*/*')]
            row['request_headers_in_sent_order'] = [list(x) for x in headers]
            connection = (CapturingConnection(parsed.hostname, port=parsed.port, timeout=30, context=ssl.create_default_context()) if parsed.scheme == 'https' else CapturingHTTPConnection(parsed.hostname, port=parsed.port, timeout=30))
            body = bytearray()
            location = None
            try:
                connection.putrequest('GET', target, skip_host=True, skip_accept_encoding=True)
                for name, value in headers:
                    connection.putheader(name, value)
                connection.endheaders()
                response = connection.getresponse()
                row['HTTP_status'] = response.status
                row['HTTP_reason'] = response.reason
                row['response_headers_in_received_order'] = [list(x) for x in response.getheaders()]
                location = response.getheader('Location')
                while True:
                    part = response.read(65536)
                    if not part:
                        break
                    body.extend(part)
                row['response_body_complete'] = True
            except Exception as error:
                if isinstance(error, http.client.IncompleteRead):
                    body.extend(error.partial)
                row['error_type'] = type(error).__name__
                row['error_message'] = str(error)
                row['response_body_complete'] = False
            finally:
                row['actual_sent_request'] = bind(OUT / f'{role}.hop{hop}.request.bin', b''.join(connection.actual_sent))
                row['response_body'] = bind(OUT / f'{role}.hop{hop}.body', bytes(body))
                row['UTC_completed'] = now()
                connection.close()
            all_receipts.append(row)
            receipt_log.write(json.dumps(row) + '\n')
            receipt_log.flush()
            if row.get('HTTP_status') in [301, 302, 303, 307, 308] and location and row['response_body_complete']:
                row['followed_actual_Location'] = location
                current = urljoin(current, location)
                continue
            break
    receipt_log.close()
    with (OUT / 'TRANSPORT_RECEIPTS.json').open('x') as f:
        json.dump(all_receipts, f, indent=2)
        f.write('\n')
    print(json.dumps([{'role': r['role'], 'hop': r['redirect_hop'], 'status': r.get('HTTP_status'), 'bytes': r['response_body']['bytes'], 'error': r.get('error_type')} for r in all_receipts], indent=2))

if __name__ == '__main__':
    main()
