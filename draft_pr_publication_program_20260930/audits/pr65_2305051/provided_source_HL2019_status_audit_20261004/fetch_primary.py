import datetime, hashlib, json, os, pathlib, urllib.request
D = pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004/status_family_20261004')
sources = {
 'aan1999_fresh.pdf':'https://mat.uab.cat/~artur/data/innerfunctions,blochspacesand.pdf',
 'hayman2018v2_fresh.pdf':'https://arxiv.org/pdf/1809.07200v2',
 'nicolau_contractive2026_fresh.pdf':'https://mat.uab.cat/~artur/data/perlaweb.pdf',
 'ivrii_nicolau2025_fresh.pdf':'https://mat.uab.cat/~artur/data/2507.15200v1.pdf',
 'bampouras_nicolau2026_fresh.pdf':'https://mat.uab.cat/~artur/data/versiowebmeva.pdf.pdf',
}
results = []
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='microseconds')
for n,u in sources.items():
    r = {'file':n, 'requested_url':u, 'started_utc':utc(), 'pid':os.getpid()}
    try:
        with urllib.request.urlopen(u, timeout=25) as resp:
            body=resp.read()
            r.update({'status':resp.status, 'final_url':resp.url, 'response_headers':dict(resp.headers)})
        (D/n).write_bytes(body)
        r.update({'bytes':len(body), 'sha256':hashlib.sha256(body).hexdigest(), 'pdf_magic':body[:5].decode('ascii',errors='replace')})
    except Exception as exc:
        r['error'] = repr(exc)
    r['ended_utc'] = utc()
    results.append(r)
(D/'fresh_primary_retrievals.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
