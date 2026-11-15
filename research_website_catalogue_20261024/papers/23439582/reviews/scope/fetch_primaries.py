"""Bounded ordinary primary-body GETs after the independent initial seal."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json

P = Path(__file__).resolve().parent / 'primary'
URLS = {
    'DGI2006': 'https://webhomes.maths.ed.ac.uk/~v1ranick/papers/dwgriy.pdf',
    'Ishiguro2007': 'https://msp.org/gtm/2007/10/gtm-2007-10-011p.pdf',
    'OWR2026-9': 'https://ems.press/content/serial-article-files/53607?nt=1',
    'Greenlees2504.03050v3': 'https://arxiv.org/pdf/2504.03050v3',
    'Lomp0307046': 'https://arxiv.org/pdf/math/0307046',
    'BIS2025': 'https://nyjm.albany.edu/j/2025/31-26p.pdf',
}


def one(pair):
    name, url = pair
    receipt = {'started_UTC': datetime.now(timezone.utc).isoformat(), 'requested_URL': url,
               'method': 'ordinary GET', 'custom_request_headers': [], 'retries': 0}
    try:
        response = urlopen(url, timeout=40)
    except HTTPError as error:
        response = error
    with response:
        body = response.read()
        receipt.update(status=response.status, final_URL=response.geturl(),
                       response_headers_in_received_order=list(response.headers.items()))
    actual = body.startswith(b'%PDF-')
    path = P / (name + ('.pdf' if actual else '.response'))
    if path.exists() or (P / (name + '.receipt.json')).exists():
        raise FileExistsError(path)
    path.write_bytes(body)
    receipt.update(completed_UTC=datetime.now(timezone.utc).isoformat(), path=str(path),
                   bytes=len(body), SHA256=hashlib.sha256(body).hexdigest(), actual_PDF=actual)
    (P / (name + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    return {k: receipt[k] for k in ('requested_URL', 'status', 'path', 'bytes', 'SHA256', 'actual_PDF')}


if __name__ == '__main__':
    P.mkdir(exist_ok=False)
    with ThreadPoolExecutor(max_workers=6) as pool:
        for result in pool.map(one, URLS.items()):
            print(json.dumps(result), flush=True)
