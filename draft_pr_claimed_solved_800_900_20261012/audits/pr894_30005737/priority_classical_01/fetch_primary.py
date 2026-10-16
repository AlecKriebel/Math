"""Bounded primary-body retrieval; raw bodies stay in excluded private_tmp."""
from pathlib import Path
import datetime, gzip, hashlib, json, subprocess, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parent
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def fetch(item):
    key, url = item
    rec = {"key": key, "url": url, "start_utc": now()}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Independent mathematical literature audit"})
        with urllib.request.urlopen(req, timeout=35) as res:
            body = res.read()
            rec.update(status=res.status, resolved_url=res.url, content_type=res.headers.get("Content-Type"), bytes=len(body), sha256=sha(body))
        # Retain only small extracted text captures. Full response hashes above
        # pin the original PDF, which is processed in memory under disk pressure.
        if body.startswith(b'%PDF'):
            p = subprocess.run(['pdftotext','-layout','-','-'],input=body,capture_output=True)
            rec.update(pdftotext_exit=p.returncode, text_bytes=len(p.stdout), text_sha256=sha(p.stdout), stderr_bytes=len(p.stderr), stderr_sha256=sha(p.stderr))
            if p.returncode == 0: (ROOT/'private_tmp'/f'{key}.txt.gz').write_bytes(gzip.compress(p.stdout))
        rec['outcome'] = 'body_fetched'
    except urllib.error.HTTPError as e:
        body=e.read()
        rec.update(status=e.code, outcome='http_error', error=str(e), bytes=len(body), sha256=sha(body))
    except Exception as e:
        rec.update(outcome='request_failed', error=(type(e).__name__+': '+str(e)).replace(str(ROOT), '<audit>'))
    rec['end_utc']=now()
    return rec

if __name__ == '__main__':
    import sys
    items=json.loads(sys.argv[1])
    rows=list(ThreadPoolExecutor(max_workers=4).map(fetch,items))
    print(json.dumps(rows,indent=2))
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    p=ROOT/f'FETCH_{stamp}.json'
    p.write_text(json.dumps(rows,indent=2)+'\n')
