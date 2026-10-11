"""Read-only dated primary retrievals; downloaded foreign bytes stay private."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, subprocess, urllib.request
HERE = Path(__file__).resolve().parent
DEST = HERE / 'tmp/root_primary'
ITEMS = [
    ('aim-literal.html', 'http://aimpl.org/finitedynamics/2/'),
    ('aim-workshop.html', 'https://aimath.org/pastworkshops/finitedynamics.html'),
    ('aim-report.pdf', 'https://aimath.org/pastworkshops/finitedynamicsrep.pdf'),
    ('hlushchanka-v2.pdf', 'https://arxiv.org/pdf/1904.04759v2'),
    ('hidalgo-quispe-v4.pdf', 'https://arxiv.org/pdf/1502.05306v4'),
    ('silverman.pdf', 'https://www.numdam.org/item/CM_1995__98_3_269_0.pdf'),
    ('bonifant-buff-milnor.pdf', 'https://arxiv.org/pdf/1512.01850'),
]

def fetch(item):
    name, url = item
    rec = {'name': name, 'requested_url': url, 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            data = response.read()
            rec.update(http_status=response.status, final_url=response.url, content_type=response.headers.get('Content-Type'))
        path = DEST / name; path.write_bytes(data)
        rec.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        if name.endswith('.pdf'):
            assert data.startswith(b'%PDF'), 'Response is not PDF'
            p = subprocess.run(['pdftotext', '-layout', str(path), str(path.with_suffix('.txt'))], capture_output=True)
            rec['text_extraction_returncode'] = p.returncode
            assert p.returncode == 0
            rec['text_sha256'] = hashlib.sha256(path.with_suffix('.txt').read_bytes()).hexdigest()
    except Exception as error:
        rec['failure'] = type(error).__name__ + ': ' + str(error)
    rec['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return rec

def main():
    assert not (HERE / 'ROOT_PRIMARY_RETRIEVAL.json').exists()
    DEST.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(fetch, ITEMS))
    (HERE / 'ROOT_PRIMARY_RETRIEVAL.json').write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps(records, indent=2))

if __name__ == '__main__':
    main()
