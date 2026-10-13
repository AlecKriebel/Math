#!/usr/bin/env python3
"""Read-only primary-source fetcher; all returned bodies and headers stay private."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request

def main():
    if len(sys.argv) != 4:
        raise SystemExit('usage: fetch_primary.py ROOT NAME URL')
    root, name, url = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]
    if not name or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789_' for c in name):
        raise SystemExit('invalid source name')
    folder = root / 'private'
    folder.mkdir(exist_ok=True)
    entry = {'id': name, 'requested_url': url,
             'utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Independent mathematical research audit'})
        with urllib.request.urlopen(req, timeout=45) as response:
            body = response.read()
            entry.update(status=response.status, final_url=response.url)
            headers = dict(response.headers.items())
        suffix = '.pdf' if body.startswith(b'%PDF') else '.body'
        target = folder / (name + suffix)
        if target.exists():
            raise RuntimeError('refusing to overwrite retained source')
        target.write_bytes(body)
        (folder / (name + '.headers.json')).write_text(json.dumps(headers, indent=2) + '\n')
        entry.update(size=len(body), sha256=hashlib.sha256(body).hexdigest(),
                     retained_path=str(target.relative_to(root)), result='downloaded')
        if suffix == '.pdf':
            subprocess.run(['pdftotext', '-layout', str(target), str(folder / (name + '.txt'))], check=True)
            entry['extraction'] = 'complete PDF text extracted; reading limits recorded separately'
    except Exception as error:
        entry.update(result='FAILED', error=str(error))
        if isinstance(error, urllib.error.HTTPError):
            failure_body = error.read()
            target = folder / (name + '.failure_body')
            if target.exists():
                raise SystemExit('refusing to overwrite retained failure body')
            target.write_bytes(failure_body)
            entry.update(status=error.code, size=len(failure_body), sha256=hashlib.sha256(failure_body).hexdigest(),
                         retained_path=str(target.relative_to(root)))
            (folder / (name + '.failure_headers.json')).write_text(json.dumps(dict(error.headers.items()), indent=2) + '\n')
    receipt = folder / ('access_' + name + '.json')
    if receipt.exists():
        raise SystemExit('refusing to overwrite access receipt')
    receipt.write_text(json.dumps(entry, indent=2) + '\n')
    print(json.dumps(entry, indent=2))

if __name__ == '__main__':
    main()
