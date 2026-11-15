"""Bounded whole primary-body acquisition; no retries or custom headers."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
import json, sys

HERE = Path(__file__).resolve().parent


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def acquire(name, url):
    root = HERE / 'private-primary'
    root.mkdir(exist_ok=True)
    opener = build_opener(NoRedirect())
    receipts = []
    for hop in range(5):
        target = root / (name if hop == 0 else name + '.hop-%02d' % hop)
        receipt_path = Path(str(target) + '.transport.json')
        if target.exists() or receipt_path.exists():
            raise FileExistsError(target)
        request = Request(url, method='GET')
        rec = {'requested_url': url, 'method': 'GET', 'started_UTC': datetime.now(timezone.utc).isoformat(),
               'body_path': str(target), 'custom_headers': [], 'retry': False}
        try:
            try:
                response = opener.open(request, timeout=45)
            except HTTPError as error:
                response = error
            with response:
                rec.update(HTTP_status=response.status, final_url=response.geturl(),
                           ordered_response_headers=list(response.headers.raw_items()))
                body = response.read()
            with target.open('xb') as out:
                out.write(body)
            rec.update(bytes=len(body), SHA256=sha256(body).hexdigest(), whole_response_body=True,
                       is_PDF=body.startswith(b'%PDF-'))
        except Exception as error:
            rec.update(exception_type=type(error).__name__, exception=repr(error))
        rec.update(completed_UTC=datetime.now(timezone.utc).isoformat(),
                   observed_request_headers=list(request.header_items()))
        with receipt_path.open('x') as out:
            out.write(json.dumps(rec, indent=2) + '\n')
        receipts.append(rec)
        if rec.get('HTTP_status') in (301, 302, 303, 307, 308):
            location = next((v for k, v in rec['ordered_response_headers'] if k.lower() == 'location'), None)
            url = urljoin(url, location) if location else ''
            if urlparse(url).scheme == 'https':
                continue
        break
    with (root / (name + '.chain.json')).open('x') as out:
        out.write(json.dumps(receipts, indent=2) + '\n')
    return {'name': name, 'chain': receipts}


if __name__ == '__main__':
    result = acquire(sys.argv[1], sys.argv[2])
    print(json.dumps({'name': result['name'], 'responses':
                     [{k: x.get(k) for k in ['HTTP_status', 'body_path', 'bytes', 'SHA256', 'is_PDF', 'exception']}
                      for x in result['chain']]}, indent=2))
