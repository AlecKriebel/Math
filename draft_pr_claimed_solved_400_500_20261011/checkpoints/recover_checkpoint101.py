#!/usr/bin/env python3
"""One bounded checkpoint recovery. Every mutation is journaled and never retried."""
import base64, concurrent.futures, datetime, hashlib, json, os, stat, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / 'draft_pr_claimed_solved_400_500_20261011'
CHECKPOINTS = PROGRAM / 'checkpoints'
REPO = 'AlecKriebel/Math'
PRIVATE = PROGRAM / 'audits/pr411_6800014/private_sources/checkpoint101_recovery'

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(path, value):
    data = (json.dumps(value, indent=2) + '\n').encode()
    with path.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
def api(label, endpoint, method='GET', payload=None, missing=False):
    dump(PRIVATE / (label+'_intent.json'), {'utc': now(), 'method': method, 'endpoint': endpoint, 'payload': payload})
    cmd = ['gh','api',f'repos/{REPO}/{endpoint}']
    if method != 'GET': cmd += ['--method',method,'--input','-']
    p = subprocess.run(cmd, input=None if payload is None else json.dumps(payload), text=True, capture_output=True, timeout=55)
    dump(PRIVATE / (label+'_native.json'), {'utc':now(),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode:
        if missing and 'HTTP 404' in p.stderr and json.loads(p.stdout).get('status') == '404': return None
        raise RuntimeError('STOP; reconcile GET-only: '+label+' '+p.stderr.strip())
    return json.loads(p.stdout)
def blob_sha(data): return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def main():
    if (CHECKPOINTS/'checkpoint101_push.json').exists(): raise RuntimeError('Already released')
    PRIVATE.mkdir(parents=True, exist_ok=False)
    paths=json.loads((CHECKPOINTS/'checkpoint101_files.json').read_text())
    if len(paths)!=19 or len(set(paths))!=19: raise ValueError('Not frozen 19-path selection')
    prepared={}; sha256={}
    forbidden={'private_sources','private_cases','mutation_fixtures','.secrets','.zenodo-state','__pycache__','venv'}
    for rel in paths:
        p=ROOT/rel
        if Path(rel).is_absolute() or '..' in Path(rel).parts or not p.is_relative_to(PROGRAM): raise ValueError(rel)
        if forbidden.intersection(Path(rel).parts) or p.suffix=='.pyc': raise ValueError(rel)
        for part in [p,*p.parents]:
            if part==ROOT.parent: break
            if part.is_symlink(): raise ValueError('symlink '+rel)
        if not stat.S_ISREG(p.lstat().st_mode): raise ValueError('not regular '+rel)
        b=p.read_bytes(); prepared[rel]=b; sha256[rel]=hashlib.sha256(b).hexdigest()
    dump(PRIVATE/'FROZEN_SELECTION.json',{'utc':now(),'files_sha256':sha256,'git_blobs':{k:blob_sha(v) for k,v in prepared.items()}})
    def verify(item):
        i,(rel,b)=item; expected=blob_sha(b)
        d=api(f'blob_get_{i:04}',f'git/blobs/{expected}',missing=True)
        if d is None: return (i,rel,b,expected)
        native=base64.b64decode(d['content'])
        if d['sha']!=expected or d['encoding']!='base64' or d['size']!=len(b) or native!=b or blob_sha(native)!=expected: raise ValueError('blob mismatch '+rel)
        return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        missing=list(x for x in pool.map(verify,enumerate(prepared.items())) if x is not None)
    dump(PRIVATE/'BLOB_RECONCILIATION.json',{'utc':now(),'verified_existing_count':len(paths)-len(missing),'absent_blobs':[{'path':r,'sha':s} for _,r,_,s in missing], 'original_attempt':'Original publisher stopped at POST git/blobs before tree/commit/ref construction; no candidate exists; all content-addressed blobs reconciled before absent-only creation'})
    for i,rel,b,expected in missing:
        d=api(f'blob_create_{i:04}','git/blobs','POST',{'content':base64.b64encode(b).decode(),'encoding':'base64'})
        if d['sha']!=expected: raise ValueError('created blob mismatch')
        back=api(f'blob_verify_{i:04}',f'git/blobs/{expected}')
        if base64.b64decode(back['content'])!=b: raise ValueError('created bytes mismatch')
    head=api('main_before','git/ref/heads/main')['object']['sha']
    parent=api('parent_commit',f'git/commits/{head}')
    entries=[{'path':r,'mode':'100644','type':'blob','sha':blob_sha(b)} for r,b in prepared.items()]
    tree=api('tree_create','git/trees','POST',{'base_tree':parent['tree']['sha'],'tree':entries})['sha']
    commit=api('commit_create','git/commits','POST',{'message':'Checkpoint 101: PR411 integration and ready confirmed, zero-intent merge abort retained; case 96%, batch 87%','tree':tree,'parents':[head]})['sha']
    dump(PRIVATE/'REF_UPDATE_PLAN.json',{'utc':now(),'parent':head,'tree':tree,'commit':commit,'force':False})
    dump(CHECKPOINTS/'checkpoint101_push.candidate.json',{'commit_sha':commit,'parent_main_sha':head,'files_sha256':sha256,'next_action':'one nonforce main PATCH'})
    api('main_update','git/refs/heads/main','PATCH',{'sha':commit,'force':False})
    back=api('main_after','git/ref/heads/main')['object']['sha']
    if back!=commit:
        if api('ancestry',f'compare/{commit}...{back}')['status'] not in ('ahead','identical'): raise RuntimeError('Ancestry failed')
    receipt={'published_at_utc':now(),'parent_main_sha':head,'commit_sha':commit,'readback_main_sha':back,'url':f'https://github.com/{REPO}/commit/{commit}','files_sha256':sha256,'branch':'main','method':'Git-data API, verified existing content-addressed blobs; journaled one nonforced update; shared index untouched','existing_blob_count':len(paths)-len(missing),'new_blob_count':len(missing)}
    dump(CHECKPOINTS/'checkpoint101_push.json',receipt)
    print(json.dumps({'commit':commit,'files':len(paths),'reused':len(paths)-len(missing),'created':len(missing)}),flush=True)
if __name__=='__main__': main()
