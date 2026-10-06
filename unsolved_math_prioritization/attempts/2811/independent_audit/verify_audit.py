#!/usr/bin/env python3
"""Externally pinned audit-packet verification and reproducible finite replay."""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
ROOT=pathlib.Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise RuntimeError(why)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--manifest-sha256',required=True);args=parser.parse_args()
    need(re.fullmatch('[0-9a-f]{64}',args.manifest_sha256) is not None,'external manifest SHA-256 required')
    mp=ROOT/'MANIFEST.json';need(mp.is_file() and not mp.is_symlink(),'regular manifest required');raw=mp.read_bytes()
    need(sha(raw)==args.manifest_sha256,'external audit manifest pin mismatch');m=json.loads(raw)
    need(set(m)=={'schema','problem_id','files'} and m['schema']=='safe-independent-audit-v1' and m['problem_id']==2811,'manifest schema/identity')
    need(isinstance(m['files'],list) and len(m['files'])>0,'manifest file list')
    names=[]
    for f in m['files']:
        need(isinstance(f,dict) and set(f)=={'path','bytes','sha256'},'entry schema')
        need(isinstance(f['path'],str) and re.fullmatch('[A-Za-z0-9_.-]+',f['path']) and f['path'] not in {'.','..','MANIFEST.json'},'safe payload path')
        need(type(f['bytes']) is int and f['bytes']>=0,'payload size')
        need(isinstance(f['sha256'],str) and re.fullmatch('[0-9a-f]{64}',f['sha256']),'payload hash format');names.append(f['path'])
    need(len(set(names))==len(names),'duplicate payload')
    actual=list(ROOT.iterdir());need(all(p.is_file() and not p.is_symlink() for p in actual),'regular flat packet only')
    need({p.name for p in actual}==set(names)|{'MANIFEST.json'},'unexpected or missing payload')
    for f in m['files']:
        b=(ROOT/f['path']).read_bytes();need(len(b)==f['bytes'] and sha(b)==f['sha256'],'payload integrity '+f['path'])
    binding=json.loads((ROOT/'BINDING.json').read_bytes())
    need(binding['problem_id']==2811 and binding['accepted_without_repair'] is True,'acceptance binding')
    for f in binding['author_files']:
        b=(ROOT/f['name']).read_bytes();need(len(b)==f['bytes'] and sha(b)==f['sha256'],'original author artifact binding')
    ext=json.loads((ROOT/'SURFACE_TRIPLE_POINTS_2811_AUTHOR_EXTERNAL_MANIFEST.json').read_bytes())
    need(ext['internal_manifest_sha256']==binding['author_internal_manifest_sha256'],'author manifest link')
    expected=(ROOT/'INDEPENDENT_RESULTS.json').read_bytes()
    for flags in ([],['-O']):
        proc=subprocess.run([sys.executable,'-B',*flags,str(ROOT/'independent_checks.py')],capture_output=True)
        need(proc.returncode==0 and not proc.stderr and proc.stdout==expected,'independent replay '+str(flags))
    print(json.dumps({'status':'PASS_EXACT_AUDIT_PACKET_AND_REPLAY','problem_id':2811,'payload_files':len(names),
                      'author_archive_sha256':ext['archive']['sha256'],'audit_manifest_sha256':args.manifest_sha256,
                      'normal_and_optimized_results_identical':True,'author_integrity_negative_cases_per_mode':20,
                      'accepted_scope':'Unsolved, 3/5; elementary conditional lemmas only; no author repair.'},sort_keys=True,indent=2))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
