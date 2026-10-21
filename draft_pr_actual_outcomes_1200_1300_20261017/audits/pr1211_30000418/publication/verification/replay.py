#!/usr/bin/env python3
"""Authenticate the primary archive and compare an actual fresh exact run."""
from pathlib import Path, PurePosixPath
import hashlib, json, subprocess, sys
ROOT=Path(__file__).resolve().parent
def require(condition,message):
    if not condition:raise ValueError(message)
def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    seen=set()
    for entry in manifest['files']:
        rel=PurePosixPath(entry['path'])
        require(not rel.is_absolute() and '..' not in rel.parts,'unsafe member path')
        require(str(rel) not in seen,'duplicate manifest member');seen.add(str(rel))
        data=(ROOT/str(rel)).read_bytes()
        require(len(data)==entry['bytes'],'member size '+str(rel))
        require(hashlib.sha256(data).hexdigest()==entry['sha256'],'member digest '+str(rel))
    run=subprocess.run([sys.executable,'-B',str(ROOT/'verify.py')],capture_output=True,text=True)
    require(run.returncode==0,run.stderr)
    actual=json.loads((ROOT/'results.json').read_text());expected=json.loads((ROOT/'expected_results.json').read_text())
    require(actual==expected,'fresh result differs from expected')
    print(json.dumps({'status':'PASS','authenticated_members':len(seen),'fresh_results_match':True,'scope':'Primary global enumerator and archived byte bindings only. Optional independent-family replay is documented for ordinary Python mode; historical priority and formal certification are not established.'},indent=2))
if __name__=='__main__':main()
