"""Bounded ordinary primary-body retrieval after paper-first initial seal."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json

P = Path(__file__).resolve().parent / 'primary'
URLS = {
    'FBPP1501.06898v3': 'https://arxiv.org/pdf/1501.06898v3',
    'OWR2016-46': 'https://ems.press/content/serial-article-files/46651',
    'Ishii0612185': 'https://arxiv.org/pdf/math/0612185',
    'survey1805.01418v1': 'https://arxiv.org/pdf/1805.01418v1',
}


def fetch(pair):
    name, url = pair
    r = {'started_UTC': datetime.now(timezone.utc).isoformat(), 'requested_URL': url,
         'method': 'ordinary GET', 'custom_headers': [], 'retries': 0}
    try:
        response = urlopen(url, timeout=40)
    except HTTPError as error:
        response = error
    with response:
        body = response.read()
        r.update(status=response.status, final_URL=response.geturl(),
                 response_headers_in_received_order=list(response.headers.items()))
    actual = body.startswith(b'%PDF-')
    path = P / (name + ('.pdf' if actual else '.response'))
    if path.exists() or (P / (name + '.receipt.json')).exists():
        raise FileExistsError(path)
    path.write_bytes(body)
    r.update(path=str(path), bytes=len(body), SHA256=hashlib.sha256(body).hexdigest(),
             actual_PDF=actual, completed_UTC=datetime.now(timezone.utc).isoformat())
    (P / (name + '.receipt.json')).write_text(json.dumps(r, indent=2) + '\n')
    return {k:r[k] for k in ['status','path','bytes','SHA256','actual_PDF']}


if __name__ == '__main__':
    P.mkdir(exist_ok=False)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for r in pool.map(fetch, URLS.items()):
            print(json.dumps(r), flush=True)
