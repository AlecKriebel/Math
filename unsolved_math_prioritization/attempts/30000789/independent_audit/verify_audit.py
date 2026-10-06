#!/usr/bin/env python3
"""Verify an externally pinned audit manifest, nested freeze, and independent replay."""
import argparse,hashlib,io,json,re,stat,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUTHOR_SHA='899b09e6754a8d8473be07c3b12a20817f90c2ecf777be48e9e2d1f32bbef491'
AUTHOR_MANIFEST='76c2f50b88d9270c9a0c76e3e7774d3f863b29dd9fa6e1eeeeb4a73632f2cbda'
def sha(x):return hashlib.sha256(x).hexdigest()
def demand(x,m):
    if not x:raise ValueError(m)
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);args=p.parse_args()
    demand(re.fullmatch('[0-9a-f]{64}',args.expected_manifest),'Invalid external anchor')
    path=ROOT/'MANIFEST.json';demand(path.is_file() and not path.is_symlink(),'Manifest is not a regular file');raw=path.read_bytes()
    demand(sha(raw)==args.expected_manifest,'External audit manifest mismatch');manifest=json.loads(raw)
    demand(manifest['schema']=='ricci-dimension-independent-audit-v1','Wrong audit schema');items=manifest['files'];names=[x['path'] for x in items]
    demand(names==sorted(set(names)) and all('/' not in x and '\\' not in x and x not in ('','.','..','MANIFEST.json') for x in names),'Unsafe audit member list')
    demand({p.name for p in ROOT.iterdir()}==set(names)|{'MANIFEST.json'},'Wrong audit member set')
    for x in items:
        p=ROOT/x['path'];demand(p.is_file() and not p.is_symlink(),'Non-regular audit member');b=p.read_bytes();demand(len(b)==x['bytes'] and sha(b)==x['sha256'],'Audit payload mismatch: '+x['path'])
    raw=(ROOT/'AUTHOR_FREEZE.zip').read_bytes();demand(len(raw)==26608 and sha(raw)==AUTHOR_SHA,'Original freeze transport mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist();demand(len(names)==len(set(names))==16,'Wrong frozen member count')
        demand(all('/' not in x and '\\' not in x and x not in ('','.','..') for x in names),'Unsafe frozen member')
        for x in z.infolist():demand(not x.is_dir() and not stat.S_ISLNK(x.external_attr>>16),'Non-regular frozen member')
        data=z.read('MANIFEST.json');demand(sha(data)==AUTHOR_MANIFEST,'Author manifest mismatch');f=json.loads(data)['files'];demand(set(names)=={x['path'] for x in f}|{'MANIFEST.json'},'Wrong frozen members')
        for x in f:
            data=z.read(x['path']);demand(len(data)==x['bytes'] and sha(data)==x['sha256'],'Frozen payload mismatch')
    cmd=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+[str(ROOT/'independent_check.py')]
    r=subprocess.run(cmd,cwd=ROOT.parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    demand(r.returncode==0,'Independent replay failed: '+r.stderr.decode());demand(r.stdout==(ROOT/'independent_results.json').read_bytes(),'Independent result mismatch')
    print(json.dumps({'status':'PASS','audit_members':len(items),'frozen_members':16,'independent_results_sha256':sha(r.stdout),'threshold_solved':False},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
