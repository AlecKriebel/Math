#!/usr/bin/env python3
import datetime, hashlib, json, os, pathlib, subprocess, urllib.request

D = pathlib.Path(__file__).resolve().parent
sources = [
    ('laclair_published_2025.pdf', 'https://link.springer.com/content/pdf/10.1007/s10801-025-01439-x.pdf'),
    ('laclair_2304.13299v1.pdf', 'https://arxiv.org/pdf/2304.13299v1'),
    ('blanco_encinas_1405.3942v5.pdf', 'https://arxiv.org/pdf/1405.3942v5'),
    ('blanco_encinas_uva2018.pdf', 'https://uvadoc.uva.es/bitstream/handle/10324/35936/Computing-log-canonical-threshold.pdf?sequence=1&isAllowed=y'),
]
receipt = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'actual_PID': os.getpid(), 'records': []}
for filename, url in sources:
    path = D / 'private_sources' / filename
    rec = {'url': url, 'filename': filename}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60) as response:
            body = response.read()
            rec.update(final_url=response.url, http_status=response.status, content_type=response.headers.get('Content-Type'))
        if not body.startswith(b'%PDF-'):
            raise ValueError('Primary response is not a PDF')
        if path.exists() and path.read_bytes() != body:
            raise ValueError('Refusing to overwrite different previously retrieved bytes')
        path.write_bytes(body)
        proc = subprocess.run(['/opt/homebrew/bin/pdftotext', '-layout', str(path), str(path.with_suffix('.txt'))], capture_output=True, check=False)
        if proc.returncode != 0:
            raise ValueError('pdftotext failed: ' + proc.stderr.decode('utf-8', 'replace'))
        rec.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), status='retrieved', extraction_actual_returncode=proc.returncode)
    except Exception as e:
        rec.update(status='unavailable', exception_type=type(e).__name__, exception=str(e))
    receipt['records'].append(rec)
    (D / 'RETRIEVAL_RECEIPT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
print(json.dumps(receipt, indent=2, sort_keys=True))
