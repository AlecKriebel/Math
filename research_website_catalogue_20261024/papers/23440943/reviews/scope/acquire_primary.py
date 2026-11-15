"""Ordinary bounded GETs, raw response bodies and ordered header receipts only."""
from pathlib import Path
from urllib.parse import urlsplit, urljoin
import http.client, ssl, hashlib, json, datetime

P = Path(__file__).resolve().parent / 'primary'

def acquire(name, url):
    receipt = P / (name + '.transport.json')
    assert not receipt.exists(), 'Do not overwrite or repeat sealed/acquired receipts'
    attempts = []
    current = url
    for i in range(6):
        split = urlsplit(current)
        conn = http.client.HTTPSConnection(split.hostname, split.port or 443, timeout=35, context=ssl.create_default_context())
        path = split.path or '/'
        if split.query:
            path += '?' + split.query
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            conn.request('GET', path, headers={'User-Agent': 'Mozilla/5.0', 'Accept': '*/*'})
            res = conn.getresponse()
            headers = res.getheaders()
            body = res.read()
            outfile = P / (name if res.status == 200 else name + '.response-' + str(i))
            assert not outfile.exists()
            outfile.write_bytes(body)
            row = {'UTC': started, 'url': current, 'status': res.status, 'reason': res.reason, 'headers_ordered': headers, 'body_path': outfile.name, 'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}
            attempts.append(row)
            location = res.getheader('Location')
            if res.status in (301, 302, 303, 307, 308) and location:
                current = urljoin(current, location)
                continue
            break
        except Exception as exc:
            attempts.append({'UTC': started, 'url': current, 'transport_error': repr(exc)})
            break
        finally:
            conn.close()
    receipt.write_text(json.dumps({'ordinary_unmodified_public_GET': True, 'requested_url': url, 'attempts': attempts}, indent=2) + '\n')
    return {'name': name, 'statuses': [x.get('status') for x in attempts], 'last_bytes': attempts[-1].get('bytes')}

if __name__ == '__main__':
    import sys
    print(json.dumps(acquire(sys.argv[1], sys.argv[2])))
