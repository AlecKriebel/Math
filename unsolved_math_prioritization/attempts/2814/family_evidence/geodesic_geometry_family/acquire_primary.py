#!/usr/bin/env python3
"""Family-local primary acquisition; imported PDF/text remain foreign ignored.

No Git, shared writes, submitted-code execution or individual contact.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, subprocess, urllib.request
ROOT = Path(__file__).resolve().parent
SOURCES = {
    'k3': 'https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf',
    'burns_matveev_aim': 'https://aimath.org/pastworkshops/geodesicsproblems.pdf',
    'luo_markovic_v1': 'https://arxiv.org/pdf/2608.29761v1',
    'xia_v1': 'https://arxiv.org/pdf/2110.14376v1',
    'kuhlmann2006_published': 'https://msp.org/agt/2006/6-5/agt-v6-n5-p04-p.pdf',
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', choices=sorted(SOURCES))
    args = parser.parse_args()
    (ROOT / 'primary').mkdir(exist_ok=True)
    (ROOT / 'receipts').mkdir(exist_ok=True)
    receipt = {'started_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'url': SOURCES[args.name], 'source': args.name,
               'scope': 'Official publisher/author primary source retrieval; no individual contacted', 'foreign_import': True}
    try:
        request = urllib.request.Request(SOURCES[args.name], headers={'User-Agent': 'Independent mathematical source verification'})
        with urllib.request.urlopen(request, timeout=40) as response:
            data = response.read()
            receipt.update(http_status=response.status, final_url=response.url, headers=dict(response.headers))
        if not data.startswith(b'%PDF'):
            raise ValueError('Response is not a PDF')
        path = ROOT / 'primary' / (args.name + '.pdf')
        path.write_bytes(data)
        receipt.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        extraction = subprocess.run(['pdftotext', '-layout', str(path), str(path.with_suffix('.txt'))], capture_output=True)
        receipt['extract_exit'] = extraction.returncode
        for channel in ['stdout', 'stderr']:
            (ROOT / 'receipts' / (args.name + '.extract.' + channel)).write_bytes(getattr(extraction, channel))
        if extraction.returncode:
            raise ValueError('Extraction failed; preserve receipt and source')
        text = path.with_suffix('.txt').read_bytes()
        receipt.update(text_bytes=len(text), text_sha256=hashlib.sha256(text).hexdigest())
    except Exception as error:
        receipt['failure'] = repr(error)
    receipt['finished_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (ROOT / 'receipts' / (args.name + '.fetch.json')).write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(receipt, ensure_ascii=False))
    if 'failure' in receipt:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
