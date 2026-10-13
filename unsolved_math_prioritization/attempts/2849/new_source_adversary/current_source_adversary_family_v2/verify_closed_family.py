#!/usr/bin/env python3
"""Independent read-only post-child closed family check."""
import argparse, hashlib, json, os, re, stat
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent; R=F.parents[3]
def sha(b): return hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x: raise ValueError(m)
parser=argparse.ArgumentParser(); parser.add_argument('--expected-manifest-sha256',required=True); args=parser.parse_args()
need(__debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'Unoptimized verifier'); p=F/'SELF_MANIFEST.json'; b=p.read_bytes()
need(re.fullmatch('[0-9a-f]{64}',args.expected_manifest_sha256) and sha(b)==args.expected_manifest_sha256,'Actual closed manifest pin')
m=json.loads(b); need(m['schema']=='pr47-source-v2-independent-self-only-closure/v1' and m['self_excluded']==['SELF_MANIFEST.json'] and type(m['files_count']) is int and m['files_count']==len(m['files']),'Manifest schema/self/count')
fs=set(); ds=set()
for p in F.rglob('*'):
 need(not p.is_symlink(),'No symlink'); n=p.relative_to(F).as_posix()
 if stat.S_ISREG(p.stat().st_mode): fs.add(n)
 else: need(stat.S_ISDIR(p.stat().st_mode),'No special members'); ds.add(n)
need(fs=={r['path'] for r in m['files']}|{'SELF_MANIFEST.json'} and ds==set(m['directories']),'Exact full topology')
for r in m['files']:
 p=F/r['path']; need(type(r['bytes']) is int and r['bytes']>=0 and type(r['full_mode']) is int and r['full_mode']==0o444,'Typed declared full mode'); b=p.read_bytes(); need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Payload full bytes/mode')
need(stat.S_IMODE((F/'SELF_MANIFEST.json').stat().st_mode)==0o444,'Self full mode')
inputs=json.loads((F/'INPUT_BINDINGS.json').read_bytes())
for r in inputs['files']:
 p=R/r['path']; need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular unchanged input'); b=p.read_bytes(); need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode'],'Fixed input unchanged')
need(m['closed_clean'] is True and m['future_acceptance_approved'] is False and m['current_freeze_or_merge_approved'] is False,'Clean SOURCE only')
print(json.dumps({'status':'PASS_POST_CHILD_CLOSED_CLEAN_SOURCE_V2_READBACK','files_count':m['files_count'],'relative_directories':len(ds),'manifest_sha256':args.expected_manifest_sha256,'actual_readonly_verifier_pid':os.getpid(),'future_acceptance_approved':False},indent=2))
