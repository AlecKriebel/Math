#!/usr/bin/env python3
"""Authenticate the complete public-only corrected derivative and exact queue."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess

ACCEPTED = {'ACCEPTANCE.md': {'bytes': 3269, 'sha256': '6c501d431db841050112caf131139f4bf134b85a96f6197926c25df51780cd61'}, 'ACCEPTANCE_AUDIT.json': {'bytes': 2227, 'sha256': '7f0971617f6fc2895607bfbb1219f1ed071e91eaf0432766aa1b3851c50b290d'}, 'AUDIT.md': {'bytes': 18728, 'sha256': 'a24bb72222a2b2cdeeb367d2292bd33de30a10533e4626142fa2a227987b947d'}, 'CERTIFICATE.json': {'bytes': 1217, 'sha256': 'b16cbf62c09d6644d58995b9fd685a765a8ad9e38ca797ee25851030532b6206'}, 'CORRECTION_CONTEXT.md': {'bytes': 3169, 'sha256': '8d6b7abbf6e380c55550716aa61fa79af5652812304fb9a1df49ca5bae6fdd1b'}, 'MATH_REPLAY_REFERENCE.json': {'bytes': 67645, 'sha256': '121a39c1c0b3ea51c16388c39c28eac4d0b6b18c93aefbcbf4c4cca23f0dacdd'}, 'MATH_REPLAY_REFERENCE.stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'PROVENANCE.json': {'bytes': 2151, 'sha256': 'd37de4c3cbf2dac17b9a4e642c0f24a3e4f17c3aec4a40b016fc47ece878bdd2'}, 'PUBLIC_SCOPE.json': {'bytes': 1342, 'sha256': 'f887ef9d417153e32fb3a4f231db92c93c5797d5c48c3b1f8e7ec3176c6f28e9'}, 'README.md': {'bytes': 3032, 'sha256': '0df37fabb455bff42bebd4e62801b5227731769eab59f00af3279dfe6bce0fa9'}, 'REPORT_CORRECTED.md': {'bytes': 22019, 'sha256': '1f278eef3907c8940fbc1b2fcecf4c267e8e3cceef04894a65fc30fe6d05f6aa'}, 'REPORT_CORRECTION.patch': {'bytes': 4959, 'sha256': 'b81e01825cf0df8496ef2524d49b52041b78f0c7f6604ed1ae8742fad7be0400'}, 'SOURCE_METADATA.json': {'bytes': 4983, 'sha256': '338aad37989a88a20946dd941f146b1d2175d62243dba189a06450dab5d4ee40'}, 'SOURCE_REHASH_HISTORICAL.json': {'bytes': 2050, 'sha256': '9b766fbe91dfe251b791add2f798cdea9b126cd946c8722ba7d1b59a5b123e6e'}, 'STATUS.json': {'bytes': 1036, 'sha256': 'bfa56f8e1014647b9b47ee669a34944a27256adbaaad6fbf315c080bf5f2d2c7'}, 'independent_verify.py': {'bytes': 6031, 'sha256': '909070e45916683a7dc7c9493226c3ac74613bd37ecd16adacd89751a69eac5f'}, 'math_controls.py': {'bytes': 7564, 'sha256': '1ae358929f63219904b04eeee97b0ea1a66ebb38c43e28546b24b73276467688'}, 'mutation_tests.py': {'bytes': 14638, 'sha256': '061abe1dfd63fcf845dd15260e223667050012a62a4c4cad07f3271c42d11241'}, 'verify.py': {'bytes': 5216, 'sha256': '201d97bd5ce09175c8eacfe914951b165a0ea74aef90714519f843c25dfb7ae3'}}
QUEUE = {'path': 'unsolved_math_prioritization/QUEUE.md', 'bytes': 397661, 'sha256': 'e68ab3a139dfe94d6dc212dcf7a8bf4a26cbfebda048e79e40dc05d4c5b52242'}
PAYLOAD = set(ACCEPTED) | {'verify_publication.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json','BOOTSTRAP.py'}

def need(ok,label):
    if not ok:raise ValueError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def same(a,b):
    if type(a) is not type(b):return False
    if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
    if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def unique(pairs):
    r={}
    for k,v in pairs:need(k not in r,'duplicate JSON key');r[k]=v
    return r
def nonfinite(x):raise ValueError('nonfinite JSON')
def finite(x):
    y=float(x);need(math.isfinite(y),'overflow JSON');return y
def parse(b):return json.loads(b,object_pairs_hook=unique,parse_constant=nonfinite,parse_float=finite)
def keys(o,n):need(type(o) is dict and set(o)==set(n),'object schema')
def exact_int(x,v=None):need(type(x) is int and x>=0 and (v is None or x==v),'exact nonnegative integer')
def digest(x):need(type(x) is str and re.fullmatch('[0-9a-f]{64}',x) is not None,'SHA256 format')
def ordinary(path):
    for d in path.parents:need(stat.S_ISDIR(d.lstat().st_mode),'linked ancestor')
    st=path.lstat();need(stat.S_ISREG(st.st_mode) and st.st_size<=2000000,'regular bounded file')
    with os.fdopen(os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)),'rb') as f:
        fs=os.fstat(f.fileno());need((st.st_dev,st.st_ino)==(fs.st_dev,fs.st_ino),'file replacement');raw=f.read(2000001)
    need(len(raw)==st.st_size,'size changed');return raw
def inventory(root):
    for d in (root,*root.parents):need(stat.S_ISDIR(d.lstat().st_mode),'linked root/ancestor')
    entries=list(os.scandir(root));need({e.name for e in entries}==FILES,'exact flat inventory')
    need(all(stat.S_ISREG(e.stat(follow_symlinks=False).st_mode) for e in entries),'linked/special/directory member')
def manifest(x,snapshot):
    keys(x,['schema','problem_id','files','queue']);exact_int(x['schema'],1);exact_int(x['problem_id'],9500007)
    need(same(x['queue'],QUEUE),'exact queue binding')
    rows=x['files'];need(type(rows) is list and len(rows)==len(PAYLOAD),'manifest inventory type/length');seen=set()
    for r in rows:
        keys(r,['path','bytes','sha256']);n=r['path'];need(type(n) is str and n in PAYLOAD and n not in seen,'manifest path');seen.add(n)
        exact_int(r['bytes']);digest(r['sha256']);need(same(r,dict(path=n,bytes=len(snapshot[n]),sha256=sha(snapshot[n]))),'manifest byte binding')
    need(seen==PAYLOAD,'complete inventory')
def semantic(parsed):
    s=parsed['STATUS.json'];need(same(s['problem_id'],9500007) and s['status']=='exhausted' and s['turns']=='5/5' and s['outcome']=='unresolved','status')
    need(s['complete_candidate'] is False and s['novelty_claim'] is False and s['new_approach_added'] is False,'status scope')
    a=parsed['ACCEPTANCE_AUDIT.json'];need(a['verdict']=='accept_restricted_partials_after_contextual_correction' and same(a['substantive_approach_count'],5) and a['new_approach_added'] is False and a['complete_candidate'] is False,'audit scope')
    scope=parsed['PUBLIC_SCOPE.json']
    for n in ['original_complete_bundle_replay','original_audit_driver_replay','original_patch_reconstruction','fresh_source_retrieval','fresh_source_inspection','fresh_pdf_byte_bindings','fresh_dataset_byte_bindings']:
        need(scope[n]=='NOT_RUN','honest omitted-input replay scope')
    r=parsed['MATH_REPLAY_REFERENCE.json'];need(r['status']=='PASS' and same(r['positive_acceptances'],6) and same(r['negative_rejections'],174),'full reference result')
def integrity(root,queue,manifest_pin,bootstrap_pin):
    digest(manifest_pin);digest(bootstrap_pin);inventory(root)
    snapshot={n:ordinary(root/n) for n in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json'])==manifest_pin,'external manifest pin');need(sha(snapshot['BOOTSTRAP.py'])==bootstrap_pin,'external bootstrap pin')
    manifest(parse(snapshot['PUBLICATION_MANIFEST.json']),snapshot)
    for n,r in ACCEPTED.items():need(same(r,dict(bytes=len(snapshot[n]),sha256=sha(snapshot[n]))),'accepted byte pin')
    raw=ordinary(queue);need(len(raw)==QUEUE['bytes'] and sha(raw)==QUEUE['sha256'],'exact external queue')
    parsed={n:parse(b) for n,b in snapshot.items() if n.endswith('.json')};semantic(parsed)
    for n in FILES:
        if n.endswith('.py'):need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(snapshot[n]))),'assertion-free public Python')
    return snapshot

def physical_probe(root,queue):
    rows=[]
    for p,n,d in [(root,'.',True)]+[(root/n,n,False) for n in sorted(FILES)]+[(queue,'external QUEUE.md',False)]:
        need((p.stat().st_mode&0o777)==(0o555 if d else 0o444) and not os.access(p,os.W_OK),'permission-readonly delivery')
        try:fd=os.open(p/'FORBIDDEN_CREATE' if d else p,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if d else 0),0o600)
        except PermissionError as e:
            need(e.errno==13,'physical denial errno');rows.append(dict(path=n,operation='create' if d else 'write_open',errno=e.errno,denied=True))
        else:os.close(fd);raise ValueError('physical write unexpectedly succeeded')
    return rows

def main():
    need(len(sys.argv)==5,'manifest, bootstrap, packet and queue arguments')
    mp,bp,rs,qs=sys.argv[1:];root=Path(os.path.abspath(rs));queue=Path(os.path.abspath(qs))
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required')
    snap=integrity(root,queue,mp,bp);probes=physical_probe(root,queue)
    env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C')
    mode=[] if sys.flags.optimize==0 else ['-'+('O'*sys.flags.optimize)]
    q=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'math_controls.py'),str(root)],cwd=root,env=env,capture_output=True,timeout=180)
    need(q.returncode==0 and q.stdout==snap['MATH_REPLAY_REFERENCE.json'] and q.stderr==snap['MATH_REPLAY_REFERENCE.stderr'],'complete fresh stdout/stderr byte comparison')
    need(same(parse(q.stdout),parse(snap['MATH_REPLAY_REFERENCE.json'])),'recursive exact-type reference equality')
    need(integrity(root,queue,mp,bp)==snap,'complete delivery changed')
    r=dict(schema=1,problem_id=9500007,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,queue=QUEUE,physical_write_probes=probes,math_replay=dict(exit_code=q.returncode,stdout=q.stdout.decode(),stderr=q.stderr.decode(),stdout_bytes=len(q.stdout),stdout_sha256=sha(q.stdout),stderr_bytes=len(q.stderr),stderr_sha256=sha(q.stderr)),full_output_byte_comparison=True,recursive_typed_comparison=True,original_complete_bundle_replay='NOT_RUN',original_patch_reconstruction='NOT_RUN',fresh_pdf_byte_bindings='NOT_RUN',fresh_dataset_byte_bindings='NOT_RUN',delivery_unchanged=True)
    print(json.dumps(r,sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: public delivery validation failed',file=sys.stderr);sys.exit(1)
