#!/usr/bin/env python3
"""Fetch primary sources into memory; retain only metadata, never source bodies.

Run with python3 -B. PDF page selections are one-based physical pages.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parent


def atomic(path, data):
    tmp = path.with_name(path.name + '.tmp-own')
    tmp.write_text(data, encoding='utf-8')
    os.replace(tmp, path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', required=True)
    parser.add_argument('--url', required=True)
    parser.add_argument('--pages', default='')
    parser.add_argument('--find', default='')
    args = parser.parse_args()
    ledger = ROOT / 'SOURCE_FETCH_RECEIPTS.json'
    rows = json.loads(ledger.read_text()) if ledger.exists() else []
    row = {'id': args.id, 'requested_url': args.url,
           'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(args.url, headers={'User-Agent': 'IndependentResearchPriorityAudit/1.0'})
        with urllib.request.urlopen(request, timeout=35) as response:
            body = response.read(20_000_001)
            if len(body) > 20_000_000:
                raise ValueError('source exceeds 20 MB memory cap')
            row.update({'resolved_url': response.url, 'status': response.status,
                        'content_type': response.headers.get('Content-Type'),
                        'last_modified': response.headers.get('Last-Modified'),
                        'body_bytes': len(body), 'body_sha256': hashlib.sha256(body).hexdigest()})
        if body.startswith(b'%PDF'):
            output = subprocess.run(['pdftotext', '-layout', '-', '-'], input=body,
                                    check=True, capture_output=True).stdout
            decoded = output.decode('utf-8')
            pages = decoded.split('\f')
            if pages and not pages[-1].strip():
                pages.pop()
            row['physical_pages'] = len(pages)
            row['extracted_text_sha256'] = hashlib.sha256(output).hexdigest()
            row['requested_page_inspection'] = args.pages
            row['requested_find'] = args.find
            if args.pages:
                indices = set()
                for item in args.pages.split(','):
                    if '-' in item:
                        left, right = map(int, item.split('-'))
                        indices.update(range(left, right + 1))
                    else:
                        indices.add(int(item))
                for index in sorted(indices):
                    print(f'\nPHYSICAL PAGE {index}\n{pages[index - 1]}')
            if args.find:
                for index, page in enumerate(pages, 1):
                    if re.search(args.find, page, re.I):
                        print(f'\nMATCHING PHYSICAL PAGE {index}\n{page}')
        else:
            row['note'] = 'Non-PDF response; body not retained or treated as full paper.'
        row['outcome'] = 'fetched'
    except Exception as exc:
        row.update({'outcome': 'error', 'error_type': type(exc).__name__, 'error': str(exc)})
    rows.append(row)
    atomic(ledger, json.dumps(rows, indent=2) + '\n')
    print('\nFETCH RECEIPT', json.dumps(row, sort_keys=True))


if __name__ == '__main__':
    main()
