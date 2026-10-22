#!/usr/bin/env python3
"""Externally pinned flat payload verifier, followed by exact output replay."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path

def check(ok,message):
    if not ok:raise RuntimeError(message)

def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);args=p.parse_args()
    root=Path(__file__).resolve().parent
    manifest=root/'MANIFEST.json';raw=manifest.read_bytes()
    check(hashlib.sha256(raw).hexdigest()==args.expected_manifest,'external manifest pin mismatch')
    m=json.loads(raw);files=m['files']
    check(set(m)=={'format','files'} and m['format']=='sha256-flat-v1','manifest schema')
    check(all('/' not in x and '\\' not in x and x not in ('.','..','MANIFEST.json') for x in files),'unsafe manifest path')
    actual={x.name for x in root.iterdir()}
    check(actual==set(files)|{'MANIFEST.json'},'file allowlist mismatch')
    for name,spec in files.items():
        f=root/name;check(f.is_file() and not f.is_symlink(),'nonregular file '+name)
        b=f.read_bytes();check(len(b)==spec['bytes'] and hashlib.sha256(b).hexdigest()==spec['sha256'],'file mismatch '+name)
    r=subprocess.run([sys.executable,str(root/'verify_math.py')],capture_output=True,check=True)
    check(r.stdout==(root/'EXPECTED_RESULTS.json').read_bytes(),'exact output mismatch')
    print(json.dumps({'manifest_matches_external_pin':True,'payload_files':len(files),'exact_math_replay_matches':True,'target_solved':False},sort_keys=True,indent=2))
if __name__=='__main__':main()
