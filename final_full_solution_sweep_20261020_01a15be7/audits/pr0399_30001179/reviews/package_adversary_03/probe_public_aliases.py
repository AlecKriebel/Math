#!/usr/bin/env python3
"""Read-only public positive control for Zenodo route identities. No credentials."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import json
import re

A = Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179')
R = A / 'reviews/package_adversary_03'
S = A.parents[1] / 'private/pr0399_package03'
PATTERNS = ['https://zenodo.org/record/ID/', 'https://zenodo.org:443/records/ID',
            'https://zenodo.org/records/./ID', 'https://zenodo.org/records/ID/export/json',
            'https://ZENODO.ORG:443/record/ID/?download=1#details',
            'https://zenodo.org:443/records/./ID?download=1#files',
            'https://zenodo.org:443/records/ID/export/json?x=1#metadata',
            'https://zenodo.org/record/ID/#files',
            'https://zenodo.org/records/ID/export/json#metadata']


def read(item):
    n, pattern = item
    url = pattern.replace('ID', '23333353')
    try:
        with urlopen(Request(url, headers={'User-Agent': 'Read-only independent mathematical review'}),
                     timeout=40) as response:
            body, status, destination, kind = response.read(), response.status, response.url, response.headers.get('content-type')
        p = S/'url_bodies'/('combined_'+str(n)+'.body')
        p.parent.mkdir(exist_ok=True)
        p.write_bytes(body)
        text = body.decode(errors='replace')
        if kind and 'json' in kind:
            value = json.loads(text)
            identity = {'body_id': value.get('id'), 'body_title': value.get('metadata', {}).get('title')}
        else:
            identity = {'canonical_link': re.findall(r'<link[^>]+rel="canonical"[^>]+>', text),
                        'contains_exact_record_doi': '10.5281/zenodo.23333353' in text}
        return {'requested_url': url, 'status': status, 'resolved_url': destination,
                'content_type': kind, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
                'private_body': str(p), 'identity_evidence': identity}
    except Exception as exc:
        return {'requested_url': url, 'error': str(exc)}


def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(read, enumerate(PATTERNS)))
    value = {'requests': results, 'read_only_gets': len(results), 'no_provider_mutations': True,
             'scope': 'Observed public route identity on unrelated already-published23333353. Conservative identity leads, not generic URL/DOI equivalence and not proof that synthetic999 exists.'}
    (R/'PUBLIC_COMBINED_URL_EVIDENCE.json').write_text(json.dumps(value, indent=2)+'\n')
    print(json.dumps(value, indent=2))


if __name__ == '__main__':
    main()
