#!/usr/bin/env python3
"""Strict flat packet verification and byte-exact mathematical replay."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

REQUIRED={
 'README.md','PROOF.md','APPROACH_LOG.md','STATUS.json','SOURCE_VERIFICATION.json',
 'check_math.py','CHECK_RESULTS.json','verify_packet.py'
}

def require(ok,message):
    if not ok:raise ValueError(message)

def unique_object(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,'Duplicate JSON key')
        out[k]=v
    return out

def parse(data):return json.loads(data,object_pairs_hook=unique_object)
def digest(data):return hashlib.sha256(data).hexdigest()

def verify_bytes(files,manifest_bytes,expected=None):
    if expected is not None:require(digest(manifest_bytes)==expected,'Pinned manifest mismatch')
    m=parse(manifest_bytes)
    require(set(m)=={'format','problem_id','files'},'Manifest schema mismatch')
    require(m['format']==1 and m['problem_id']=='30001658','Manifest identity mismatch')
    entries=m['files'];require(type(entries) is list,'File entries must be a list')
    names=[x.get('path') for x in entries]
    require(len(names)==len(set(names)) and set(names)==REQUIRED,'Manifest inventory mismatch')
    require(set(files)==REQUIRED,'Actual inventory mismatch')
    for e in entries:
        require(set(e)=={'path','bytes','sha256'},'File entry schema mismatch')
        p=e['path'];require('/' not in p and p not in {'','.', '..'},'Unsafe path')
        require(type(e['bytes']) is int and e['bytes']>=0,'Invalid byte count')
        require(type(e['sha256']) is str and len(e['sha256'])==64,'Invalid hash')
        require(len(files[p])==e['bytes'] and digest(files[p])==e['sha256'],'File binding mismatch: '+p)
    status=parse(files['STATUS.json'])
    require(status['problem_id']=='30001658' and status['status']=='unsolved','Status mismatch')
    require(status['approaches_used']==5 and status['approach_limit']==5,'Approach count mismatch')
    require(status['full_resolution'] is False and status['novelty_claim'] is False and status['global_open_status_claim'] is False,'Unsupported status claim')
    require(status['independent_audit']=='pending','Author audit state changed')
    return m

def reject(thunk):
    try:thunk()
    except (ValueError,KeyError,TypeError):return
    raise ValueError('Negative control was accepted')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest-sha256');args=ap.parse_args()
    root=Path(__file__).resolve().parent
    entries=list(root.iterdir())
    require(all(p.is_file() and not p.is_symlink() for p in entries),'Directories and symlinks are forbidden')
    require({p.name for p in entries}==REQUIRED|{'MANIFEST.json'},'Strict filesystem inventory mismatch')
    files={p: (root/p).read_bytes() for p in REQUIRED};raw=(root/'MANIFEST.json').read_bytes()
    verify_bytes(files,raw,args.expected_manifest_sha256)
    cmd=[sys.executable,'-B']
    if sys.flags.optimize:cmd+=['-O']
    result=subprocess.run(cmd+[str(root/'check_math.py')],capture_output=True,check=False)
    require(result.returncode==0 and not result.stderr,'Mathematical checker failed')
    require(result.stdout==files['CHECK_RESULTS.json'],'Frozen mathematical output mismatch')
    results=parse(result.stdout)
    require(results['status']=='PASS_SCOPED_CONTROLS' and results['total_checks']==704115,'Mathematical result identity mismatch')
    # In-memory corruption cases do not alter the frozen packet.
    bad=dict(files);bad['PROOF.md']+=b'changed';reject(lambda:verify_bytes(bad,raw))
    bad2=dict(files);bad2.pop('PROOF.md');reject(lambda:verify_bytes(bad2,raw))
    bad3=dict(files);bad3['extra.txt']=b'x';reject(lambda:verify_bytes(bad3,raw))
    m=parse(raw);m['files'].append(dict(m['files'][0]));reject(lambda:verify_bytes(files,json.dumps(m).encode()))
    m=parse(raw);m['files'][0]['path']='../PROOF.md';reject(lambda:verify_bytes(files,json.dumps(m).encode()))
    m=parse(raw);m['files'][0]['bytes']+=1;reject(lambda:verify_bytes(files,json.dumps(m).encode()))
    reject(lambda:verify_bytes(files,raw,'0'*64))
    bad4=dict(files);s=parse(bad4['STATUS.json']);s['full_resolution']=True
    bad4['STATUS.json']=json.dumps(s).encode();m=parse(raw)
    for e in m['files']:
        if e['path']=='STATUS.json':e.update(bytes=len(bad4['STATUS.json']),sha256=digest(bad4['STATUS.json']))
    reject(lambda:verify_bytes(bad4,json.dumps(m).encode()))
    print(json.dumps({'status':'PASS_SCOPED_AUTHOR_PACKET','manifest_sha256':digest(raw),
       'manifest_pin_supplied':args.expected_manifest_sha256 is not None,
       'bound_files':len(REQUIRED),'mathematical_checks':results['total_checks'],
       'integrity_negative_controls':8,'mathematical_negative_controls':6,
       'frozen_results_replayed':True,'independent_audit':'pending'},sort_keys=True,indent=2))
if __name__=='__main__':main()
