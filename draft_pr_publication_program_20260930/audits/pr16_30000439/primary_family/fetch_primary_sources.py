"""Read-only source acquisition into ignored tmp/raw and SHA-256 ledger.
Uses public primary source URLs; no person is contacted. Re-running may obtain
changed current bytes, so each ledger records retrieval time and final URL.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, urllib.request
ROOT = Path(__file__).resolve().parent
SOURCES = {
    'owr_2006_12.pdf': 'https://ems.press/content/serial-article-files/46044',
    'brehm_sarkaria_1992_52.pdf': 'https://archive.mpim-bonn.mpg.de/id/eprint/1946/1/preprint_1992_52.pdf',
    'newman_v3.pdf': 'https://arxiv.org/pdf/2212.09576v3',
    'newman_abs.html': 'https://arxiv.org/abs/2212.09576',
    'lee_nevo_v3.pdf': 'https://arxiv.org/pdf/2307.14195v3',
    'lee_nevo_abs.html': 'https://arxiv.org/abs/2307.14195',
    'frieze_karonski_book.pdf': 'https://www.math.cmu.edu/~af1p/BOOK.pdf',
    'newman_crossref.json': 'https://api.crossref.org/works/10.1016/j.disc.2026.115331',
    'lee_nevo_crossref.json': 'https://api.crossref.org/works/10.1007/s00454-026-00856-4',
    'lee_nevo_published.pdf': 'https://link.springer.com/content/pdf/10.1007/s00454-026-00856-4.pdf',
    'tverberg_constraints_v2.pdf': 'https://arxiv.org/pdf/1401.0690v2',
    'tverberg_constraints_abs.html': 'https://arxiv.org/abs/1401.0690',
    'newman_elsevier.xml': 'https://api.elsevier.com/content/article/PII:S0012365X26003559?httpAccept=text/xml',
    'goodman_pollack_1986.pdf': 'https://link.springer.com/content/pdf/10.1007/BF02187696.pdf',
    'lee_nevo_journal.html': 'https://link.springer.com/article/10.1007/s00454-026-00856-4',
    'newman_journal.html': 'https://www.sciencedirect.com/science/article/pii/S0012365X26003559',
}

def fetch(pair):
    filename, url = pair
    now = datetime.now(timezone.utc).isoformat()
    record = {'filename': filename, 'requested_url': url, 'retrieved_utc': now}
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Independent mathematical source audit (Python urllib)'})
        with urllib.request.urlopen(req, timeout=25) as response:
            data = response.read()
            record.update(final_url=response.url, content_type=response.headers.get('Content-Type'), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), status='retrieved')
        (ROOT/'tmp/raw'/filename).write_bytes(data)
    except Exception as exc:
        record.update(status='unavailable', error=str(exc))
    return record

if __name__ == '__main__':
    (ROOT/'tmp/raw').mkdir(parents=True, exist_ok=True)
    records = list(ThreadPoolExecutor(max_workers=6).map(fetch,SOURCES.items()))
    payload = {'audit_head':'3aa15b4ab70ddddf556c84cbba7d6528910dfceb', 'source_records':records}
    (ROOT/'source_hash_ledger.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(records,indent=2))
