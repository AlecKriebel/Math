"""Read-only primary-source retrieval; all body material stays in private/."""
import sys, json, hashlib, pathlib, datetime, urllib.request, urllib.error, subprocess

BASE = pathlib.Path(__file__).resolve().parent
PRIVATE = BASE / 'private'
PRIVATE.mkdir(exist_ok=True)

def retrieve(key, url):
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    out = {'key': key, 'request_url': url, 'retrieved_utc': utc,
           'mode': 'fresh_network', 'method': 'GET', 'contact': 'none'}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Independent mathematical literature audit (read-only)'})
        with urllib.request.urlopen(request, timeout=55) as r:
            body = r.read()
            out.update(status=r.status, final_url=r.url, content_type=r.headers.get('Content-Type'),
                       last_modified=r.headers.get('Last-Modified'), etag=r.headers.get('ETag'))
        suffix = '.pdf' if body.startswith(b'%PDF') else '.html'
        path = PRIVATE / (key + suffix)
        path.write_bytes(body)
        out.update(path=str(path.relative_to(BASE)), bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
        if suffix == '.pdf':
            textpath = PRIVATE / (key + '.txt')
            subprocess.run(['pdftotext', '-layout', str(path), str(textpath)], check=True, capture_output=True)
            data = textpath.read_bytes()
            out.update(extracted_path=str(textpath.relative_to(BASE)), extracted_bytes=len(data),
                       extracted_sha256=hashlib.sha256(data).hexdigest())
    except Exception as e:
        out.update(error=type(e).__name__ + ': ' + str(e))
    with (PRIVATE / 'network_events.jsonl').open('a') as f:
        f.write(json.dumps(out, sort_keys=True) + '\n')
    display = {k: v for k, v in out.items() if k != 'final_url'}
    print(json.dumps(display, sort_keys=True))
    return out

if __name__ == '__main__':
    retrieve(sys.argv[1], sys.argv[2])
