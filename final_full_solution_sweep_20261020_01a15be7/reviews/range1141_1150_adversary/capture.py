"""Read-only capture of the assigned PRs and their entire immutable comparisons."""
import base64, concurrent.futures, datetime, hashlib, json, pathlib, subprocess

HERE = pathlib.Path(__file__).resolve().parent
PRIVATE = HERE / 'private'
CHECKPOINT = 'b1083ddf4c801487b8d85f6985845843c1f451a7'
REPO = 'AlecKriebel/Math'

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()
def api(endpoint):
    return subprocess.check_output(['gh','api',f'repos/{REPO}/{endpoint}'])
def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {'path':str(path.relative_to(HERE)), 'bytes':len(data), 'sha256':sha(data)}
def capture_pr(n):
    d = PRIVATE / f'pr{n}'
    raw = api(f'pulls/{n}')
    pr = json.loads(raw)
    save(d/'live_initial.json',raw)
    base, head = pr['base']['sha'], pr['head']['sha']
    cmpraw = api(f'compare/{base}...{head}?per_page=100&page=1')
    cmp = json.loads(cmpraw)
    save(d/'comparison.json',cmpraw)
    files = cmp['files']
    # GitHub returns all compare files on page 1, maximum 300. Reject saturation.
    assert len(files) < 300
    livefiles = json.loads(api(f'pulls/{n}/files?per_page=100'))
    save(d/'live_files.json',json.dumps(livefiles,indent=2).encode())
    assert len(livefiles) < 100
    assert sorted(x['filename'] for x in files) == sorted(x['filename'] for x in livefiles)
    receipts=[]
    for f in files:
        if f['status']=='removed': continue
        obj=json.loads(api(f"git/blobs/{f['sha']}"))
        data=base64.b64decode(obj['content'])
        gitsha=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        assert gitsha == f['sha']
        rec=save(d/'head'/f['filename'],data)
        rec.update(git_blob_sha=f['sha'],filename=f['filename'],status=f['status'])
        receipts.append(rec)
    out={'pr':n,'captured':now(),'head':head,'base':base,'body_sha256':sha((pr['body'] or '').encode()),'state':pr['state'],'changed_paths':[f['filename'] for f in files],'queue_paths':[f['filename'] for f in files if 'QUEUE' in f['filename'].upper()],'payloads':receipts}
    save(d/'capture_receipt.json',json.dumps(out,indent=2).encode())
    return {k:v for k,v in out.items() if k!='payloads'}

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(capture_pr,range(1141,1151)))
    save(PRIVATE/'initial_capture_summary.json',json.dumps(results,indent=2).encode())
    print(json.dumps(results,indent=2))
