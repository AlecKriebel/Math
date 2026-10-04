"""Read-only Git freeze plus independent primary-source acquisition."""
import concurrent.futures, datetime, hashlib, json, pathlib, subprocess, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
HEAD = "421c6aa90eace49c8659f9a96e83c24fe1b5b901"
SHA = lambda b: hashlib.sha256(b).hexdigest()
STAMP = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    private = HERE / '.private'
    private.mkdir(exist_ok=True)
    manifest = json.loads((HERE.parent / 'snapshot_manifest.json').read_text())
    bindings = []
    for entry in manifest['files']:
        p = entry['path']
        b = subprocess.check_output(['git', 'show', f'{HEAD}:{p}'], cwd=ROOT)
        local = private / 'original' / p
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_bytes(b)
        blob = subprocess.check_output(['git', 'rev-parse', f'{HEAD}:{p}'], cwd=ROOT).decode().strip()
        bindings.append({'path':p,'git_blob':blob,'bytes':len(b),'sha256':SHA(b),'snapshot_match':len(b)==entry['bytes'] and SHA(b)==entry['sha256']})
    (HERE/'INPUT_BINDING.json').write_text(json.dumps({'utc':STAMP(),'head':HEAD,'snapshot_sha256':SHA((HERE.parent/'snapshot_manifest.json').read_bytes()),'files':bindings},indent=2)+'\n')
    source = json.loads((private/'original/unsolved_math_prioritization/attempts/6600013/SOURCE_MANIFEST.json').read_text())
    specs = [dict(s) for s in source['primary_sources']]
    specs[0]['url'] = 'https://arxiv.org/pdf/1604.06280v2'
    specs[1]['url'] = 'https://arxiv.org/pdf/0804.0145v1'
    def download(s):
        req = urllib.request.Request(s['url'], headers={'User-Agent':'Mozilla/5.0','Accept':'application/pdf,*/*'})
        start = STAMP()
        with urllib.request.urlopen(req,timeout=90) as response:
            b = response.read()
            final_url = response.url
            headers = dict(response.headers.items())
        p = private / 'sources' / s['file']
        p.parent.mkdir(exist_ok=True)
        p.write_bytes(b)
        out = subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],capture_output=True)
        return {'file':s['file'],'requested_url':s['url'],'final_url':final_url,'requested_utc':start,'received_utc':STAMP(),'bytes':len(b),'sha256':SHA(b),'frozen_pdf_bytes':s['bytes'],'frozen_pdf_sha256':s['sha256'],'frozen_bytes_match':SHA(b)==s['sha256'] and len(b)==s['bytes'],'headers':headers,'pdftotext_exit':out.returncode,'pdftotext_stderr':out.stderr.decode(errors='replace')}
    def safe_download(s):
        try: return download(s)
        except Exception as e: return {'file':s['file'],'requested_url':s['url'],'utc':STAMP(),'error':repr(e),'frozen_bytes_match':False}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        receipts = list(pool.map(safe_download,specs))
    (HERE/'SOURCE_RECEIPTS.json').write_text(json.dumps({'utc':STAMP(),'independently_retrieved_sources':receipts},indent=2)+'\n')
    print(json.dumps({'inputs':len(bindings),'all_frozen_inputs_match':all(x['snapshot_match'] for x in bindings),'source_exact_matches':sum(x['frozen_bytes_match'] for x in receipts),'sources':[{k:x[k] for k in ['file','bytes','sha256','frozen_bytes_match','error'] if k in x} for x in receipts]},indent=2))

if __name__ == '__main__': main()
