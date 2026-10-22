#!/usr/bin/env python3
"""Verify the closed audit payload and replay both finite arithmetic suites."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
def require(test,message):
    if not test:raise AssertionError(message)

def main():
    manifest=json.loads((ROOT/'AUDIT_MANIFEST.json').read_text())
    expected={entry['path']:entry for entry in manifest['files']}
    require(len(expected)==len(manifest['files']),'Duplicate manifest paths')
    actual={}
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'Symlink is not part of this payload')
        if p.is_file() and p.name!='AUDIT_MANIFEST.json':
            rel=p.relative_to(ROOT).as_posix()
            require(p.suffix in {'.md','.json','.py'},'Disallowed payload type: '+rel)
            require('/' not in rel or rel.startswith('author_freeze/') and rel.count('/')==1,'Unexpected directory: '+rel)
            actual[rel]=p
    require(set(actual)==set(expected),'Closed payload file-set mismatch')
    for name,p in actual.items():
        blob=p.read_bytes(); e=expected[name]
        require(len(blob)==e['bytes'] and hashlib.sha256(blob).hexdigest()==e['sha256'],'Hash/size mismatch: '+name)
    binding=json.loads((ROOT/'AUDIT_BINDING.json').read_text())
    frozen=ROOT/'author_freeze'
    require(set(p.name for p in frozen.iterdir())==set(e['path'] for e in binding['frozen_members']),'Frozen member set mismatch')
    for e in binding['frozen_members']:
        b=(frozen/e['path']).read_bytes()
        require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'Frozen member changed: '+e['path'])
    outputs={}
    for label,path in [('author_manifest',frozen/'verify_manifest.py'),('author_arithmetic',frozen/'verify.py'),('independent_arithmetic',ROOT/'audit_checks.py')]:
        proc=subprocess.run([sys.executable,'-B',str(path)],cwd=path.parent,text=True,capture_output=True)
        require(proc.returncode==0,label+' failed: '+proc.stderr)
        outputs[label]=json.loads(proc.stdout)
        require(outputs[label]['status']=='PASS',label+' did not report PASS')
    require(outputs['author_arithmetic']['total_assertions']==21193,'Author assertion count mismatch')
    require(outputs['independent_arithmetic']['total_assertions']==20371,'Independent assertion count mismatch')
    summary={
        'status':'PASS','audit_verdict':binding['audit_verdict'],
        'payload_files_checked':len(actual),'frozen_members_checked':len(binding['frozen_members']),
        'author_assertions':21193,'independent_assertions':20371,
        'omitted_sources_reverified':False,
        'scope':'Included bytes and finite controls only; the accompanying written audit carries the infinite mathematics and applicability review.'
    }
    print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=='__main__':main()
