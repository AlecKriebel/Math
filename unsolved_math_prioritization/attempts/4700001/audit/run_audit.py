#!/usr/bin/env python3
"""Portable replay driver; no network or frozen-input mutation.
Requires Python 3, NumPy, SciPy, SymPy. The exact input manifest is embedded in
input-verification.json; --packet may point to a relocated eight-file packet.
"""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path
here=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,default=here.parent/'frozen');p.add_argument('--output',type=Path,default=here/'rerun');a=p.parse_args()
packet=a.packet.resolve();out=a.output.resolve()
assert packet!=out and packet not in out.parents,'Do not write inside the input packet.'
out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((here/'input-verification.json').read_text())
for entry in manifest['files']:
    b=(packet/entry['path']).read_bytes()
    assert len(b)==entry['bytes'],entry['path']
    assert hashlib.sha256(b).hexdigest()==entry['sha256'],entry['path']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def replay(script,name):
    with (out/name).open('w') as f:
        subprocess.run([sys.executable,str(script)],check=True,stdout=f,cwd=out,env=env)
replay(packet/'check_symbolic.py','symbolic-replay.txt')
replay(packet/'check_numeric.py','numerical-replay.json')
subprocess.run([sys.executable,str(here/'independent_checks.py'),'--packet',str(packet),'--output',str(out/'independent-results.json')],check=True,cwd=out,env=env)
orig=json.loads((packet/'numerical-results.json').read_text());new=json.loads((out/'numerical-replay.json').read_text())
ind=json.loads((out/'independent-results.json').read_text())
report={'frozen_input_hashes_match':True,'frozen_manifest_sha256':manifest['frozen_manifest_sha256'],'supplied_scripts_passed':True,'independent_checks':ind['status'],'independent_check_count':ind['check_count'],'numerical_JSON_exact_match':orig==new,'numerical_exact_match_note':'A different platform or dependency version may produce legitimate floating-point differences. The numerical computation is not a validated enclosure.','scan_summary':new['scan_summary'],'target_status':'unsolved','no_global_exclusion':True}
(out/'replay-summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
