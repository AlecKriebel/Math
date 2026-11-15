#!/usr/bin/env python3
"""One bounded ordinary GET per legacy leaf; preserve complete bodies and hops."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
import hashlib
import json
import sys

A = Path(__file__).resolve().parent
D = A.parent / 'strict-gap-redirect-sol-20261115'
LABEL = sys.argv[1]
if not LABEL.isalnum():
    raise ValueError('simple new attempt label required')
OUT = A / 'http' / LABEL
if OUT.exists():
    raise FileExistsError(OUT)
OUT.mkdir()


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git_blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


leaf = json.loads((A / 'raw/tree-leaf.json').read_text())
entries = json.loads(leaf['structuredContent']['content'])['tree']
opener = build_opener(NoRedirect())
records = []
for entry in entries:
    name = entry['path']
    url = 'https://aleckriebel.github.io/Math/papers/strict-dirichlet-gap/'
    if name != 'index.html':
        url += name
    initial = url
    hops = []
    for hop in range(6):
        record = {'UTC_started': datetime.now(timezone.utc).isoformat(),
                  'method': 'GET', 'URL': url, 'custom_headers': [],
                  'network_retry': False}
        try:
            response = opener.open(Request(url, method='GET'), timeout=45)
        except HTTPError as error:
            response = error
        except (URLError, TimeoutError, OSError) as error:
            record.update({'transport_exception': repr(error),
                           'UTC_completed': datetime.now(timezone.utc).isoformat()})
            hops.append(record)
            break
        with response:
            body = response.read()
            headers = list(response.headers.raw_items())
            status = response.code
            location = response.headers.get('Location')
        bodypath = OUT / (name + f'.hop{hop:02d}.body')
        bodypath.write_bytes(body)
        record.update({'HTTP_status': status, 'ordered_response_headers': headers,
                       'body_path': str(bodypath), 'bytes': len(body), 'SHA256': sha(body),
                       'git_blob_SHA': git_blob(body), 'whole_body': True,
                       'UTC_completed': datetime.now(timezone.utc).isoformat()})
        hops.append(record)
        if status in (301, 302, 303, 307, 308) and location:
            next_url = urljoin(url, location)
            if not next_url.startswith('https://'):
                record['redirect_stopped'] = 'non-HTTPS'
                break
            url = next_url
            continue
        break
    final = hops[-1]
    expected = '7b7411fefe1638f4721bc2180486574497f69ab0' if name == 'index.html' else entry['sha']
    item = {'legacy_name': name, 'original_URL': initial, 'hops': hops,
            'expected_git_blob_SHA': expected,
            'HTTP_200_whole_exact_expected_bytes': final.get('HTTP_status') == 200 and
                final.get('git_blob_SHA') == expected}
    if name == 'index.html' and final.get('HTTP_status') == 200:
        item['exact_approved_candidate_bytes'] = Path(final['body_path']).read_bytes() == (D / 'index.html').read_bytes()
    records.append(item)
    (OUT / (name + '.receipt.json')).write_text(json.dumps(item, indent=2) + '\n')

result = {'UTC': datetime.now(timezone.utc).isoformat(), 'attempt_label': LABEL,
          'ordinary_GET_only': True, 'custom_headers_proxy_auth_or_bypass': False,
          'records': records, 'all_ten_deliveries_HTTP_200_exact': all(
              r['HTTP_200_whole_exact_expected_bytes'] for r in records),
          'fresh_PDF_text_or_ZIP_extraction': False,
          'browser_execution_or_arrival_checked': False}
(OUT / 'ALL_DELIVERIES.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'report': str(OUT / 'ALL_DELIVERIES.json'),
                  'all_ten_deliveries_HTTP_200_exact': result['all_ten_deliveries_HTTP_200_exact'],
                  'results': [{'name': r['legacy_name'], 'exact': r['HTTP_200_whole_exact_expected_bytes'],
                               'status': r['hops'][-1].get('HTTP_status'),
                               'bytes': r['hops'][-1].get('bytes')} for r in records]}, indent=2))
