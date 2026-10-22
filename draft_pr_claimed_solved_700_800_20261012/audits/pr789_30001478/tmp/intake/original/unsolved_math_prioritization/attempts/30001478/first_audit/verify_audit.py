#!/usr/bin/env python3
"""Fail-closed integrity and complete replay of the independent audit package."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

AUTHOR_FILES = {'README.md','certificate.json','manifest.json','proof.md','provenance.json',
                'public_sources.json','test_suite.py','verification_results.json','verify.py'}
ROOT_FILES = {'README.md','mathematical_audit.md','scope_addendum.md','independent_check.py',
              'independent_results.json','author_replay_results.json','source_verification.json',
              'corpus_verification.json','author_freeze_verification.json','verify_audit.py',
              'test_audit.py','audit_test_results.json','manifest.json'}
EXPECTED = ROOT_FILES | {'author/'+name for name in AUTHOR_FILES}


def require(ok,message):
    if not ok:
        raise ValueError(message)


def integrity(root):
    found = set()
    for entry in root.rglob('*'):
        name=entry.relative_to(root).as_posix()
        mode=entry.lstat().st_mode
        if stat.S_ISDIR(mode):
            require(name == 'author','Unexpected directory: '+name)
        else:
            require(stat.S_ISREG(mode),'Nonregular entry: '+name)
            found.add(name)
    require(found == EXPECTED,'Exact inventory mismatch')
    manifest=json.loads((root/'manifest.json').read_text())
    require(set(manifest)=={'schema','files'} and manifest['schema']==1,'Manifest schema')
    require(set(manifest['files']) == EXPECTED-{'manifest.json'},'Manifest file set')
    for name,value in manifest['files'].items():
        require(set(value)=={'bytes','sha256'},'Manifest entry schema')
        data=(root/name).read_bytes()
        require(len(data)==value['bytes'] and hashlib.sha256(data).hexdigest()==value['sha256'],
                'Hash mismatch: '+name)


def execute(root,relative,optimized=False):
    command=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(root/relative)]
    run=subprocess.run(command,cwd=root.parent,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),
                       text=True,capture_output=True,timeout=120)
    require(run.returncode == 0,'Replay failed: '+relative+'\n'+run.stderr)
    return json.loads(run.stdout)


def main():
    require(len(sys.argv)==1,'No arguments accepted')
    root=Path(__file__).resolve().parent
    integrity(root)
    normal=execute(root,'author/verify.py')
    optimized=execute(root,'author/verify.py',True)
    require(normal==optimized,'Author optimized replay differs')
    author_suite=execute(root,'author/test_suite.py')
    require(author_suite == json.loads((root/'author_replay_results.json').read_text()),'Author suite saved result mismatch')
    independent=execute(root,'independent_check.py')
    independent_o=execute(root,'independent_check.py',True)
    require(independent==independent_o,'Independent optimized replay differs')
    require(independent==json.loads((root/'independent_results.json').read_text()),'Independent saved result mismatch')
    print(json.dumps({'status':'PASS','exact_regular_file_count':len(EXPECTED),
                      'author_named_controls':author_suite['test_count'],
                      'independent_symbolic_checks':'PASS',
                      'finite_field_degree_cases':sum(len(x['degrees']) for x in independent['finite_field_checks']),
                      'optimized_outputs_match':True},sort_keys=True,indent=2))


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
