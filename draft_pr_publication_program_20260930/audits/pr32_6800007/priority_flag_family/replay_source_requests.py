"""Reproduce all durable scholarly retrieval URLs in a new ignored directory.

Run with --output-root tmp/source_replay. Original source bytes and sealed receipts
are never overwritten. A successful response is not assumed to be PDF or identical
to the recorded version. No external individual is contacted.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import argparse
import hashlib
import json

TASK_DIR = Path(__file__).resolve().parent

def utc():
    return datetime.now(timezone.utc).isoformat()

def request(item):
    name, url, out = item
    row = {'name': name, 'requested_url': url, 'started_utc': utc()}
    try:
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (independent mathematical source audit)'}), timeout=55) as response:
            data = response.read()
            row.update(status=response.status, final_url=response.url, content_type=response.headers.get('Content-Type'))
    except HTTPError as exc:
        data = exc.read()
        row.update(status=exc.code, final_url=exc.url, content_type=exc.headers.get('Content-Type'), error=str(exc))
    except Exception as exc:
        data = b''
        row['error'] = repr(exc)
    (out / name).write_bytes(data)
    row.update(finished_utc=utc(), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), is_pdf=data.startswith(b'%PDF-'))
    return row

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-root', default='tmp/source_replay')
    args = parser.parse_args()
    out = (TASK_DIR / args.output_root).resolve()
    if TASK_DIR / 'tmp' not in out.parents:
        raise SystemExit('Replay destination must be a new directory inside this family\'s ignored tmp/.')
    out.mkdir(parents=True, exist_ok=False)
    entries = {}
    for path in sorted(TASK_DIR.glob('*RECEIPTS.json')):
        value = json.loads(path.read_text())
        for row in value if isinstance(value, list) else value.get('receipts', []):
            url = row.get('requested_url', row.get('url'))
            if not url:
                continue
            name = row.get('name', 'response')
            if '.' not in name:
                name += '.response'
            entries.setdefault(url, (f'{len(entries):03d}_{name}', url, out))
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(request, entries.values()))
    (out / 'receipts.json').write_text(json.dumps({'generated_utc': utc(), 'receipts': results}, indent=2) + '\n')
    print(json.dumps({'requests': len(results), 'output_directory': str(out), 'pdfs': sum(x['is_pdf'] for x in results)}, indent=2))
