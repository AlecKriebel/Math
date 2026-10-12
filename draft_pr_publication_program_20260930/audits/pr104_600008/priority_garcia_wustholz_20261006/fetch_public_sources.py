"""Ordinary unauthenticated fetch of publicly advertised source URLs; no bypass."""
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime, timezone
import json, hashlib

root = Path(__file__).parent / 'private_sources'
sources = {
    'wustholz2021': 'https://www.research-collection.ethz.ch/bitstreams/607210dc-654c-473a-b4e7-e9c19f8b2a3a/download',
    'huber_wustholz_author_preprint': 'https://home.mathematik.uni-freiburg.de/arithgeom/preprints/huber-einsmotive.pdf',
}
ledger = []
for name, url in sources.items():
    rec = {'name': name, 'url': url, 'utc': datetime.now(timezone.utc).isoformat(), 'request': 'urllib default ordinary GET; no custom headers, credentials, proxy change, or URL manipulation'}
    try:
        with urlopen(url, timeout=30) as response:
            data = response.read()
            rec.update(status=response.status, final_url=response.url, content_type=response.headers.get('Content-Type'), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            if data.startswith(b'%PDF'):
                (root / (name + '.pdf')).write_bytes(data)
                rec['saved'] = name + '.pdf'
            else:
                rec['saved'] = None
    except (HTTPError, URLError) as err:
        rec.update(status=getattr(err, 'code', None), error=str(err), saved=None)
    ledger.append(rec)
print(json.dumps(ledger, indent=2))
(root / 'FETCH_LEDGER.json').write_text(json.dumps(ledger, indent=2)+'\n')
