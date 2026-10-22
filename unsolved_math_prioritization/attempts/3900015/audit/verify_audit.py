#!/usr/bin/env python3
"""Verify audit identity under a trusted external pin and replay exact checks."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True

def require(ok,message):
    if not ok:raise ValueError(message)

def normalize(value):return json.loads(json.dumps(value,sort_keys=True))

def load(root,name):
    spec=importlib.util.spec_from_file_location('audit_'+name,root/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def verify():
    root=Path(__file__).resolve().parent
    require(not (root/'MANIFEST.json').is_symlink(),'manifest symlink rejected')
    manifest=json.loads((root/'MANIFEST.json').read_text())
    require(manifest['schema']=='reciprocal-independent-audit-manifest-v1','wrong audit manifest schema')
    entries=list(root.iterdir())
    require(all(p.is_file() and not p.is_symlink() for p in entries),'nonregular audit entry')
    require({p.name for p in entries}==set(manifest['files'])|{'MANIFEST.json'},'audit inventory mismatch')
    for name,meta in manifest['files'].items():
        require(name==Path(name).name,'unsafe audit filename')
        b=(root/name).read_bytes()
        require(len(b)==meta['bytes'] and hashlib.sha256(b).hexdigest()==meta['sha256'],'audit member mismatch: '+name)
    accepted=json.loads((root/'ACCEPTANCE.json').read_text())
    author=load(root,'author_artifact_tests')
    require(accepted['accepted_author_archive']['sha256']==author.AUTHOR_ARCHIVE_SHA256,'acceptance identity mismatch')
    require(accepted['full_problem_resolved'] is False and accepted['correction_required'] is False,'acceptance scope mismatch')
    results=normalize(load(root,'independent_checks').checks())
    require(results==json.loads((root/'EXPECTED_INDEPENDENT_CHECKS.json').read_text()),'independent exact checks changed')
    tests=author.tests(root)
    require(tests==json.loads((root/'EXPECTED_AUTHOR_ARTIFACT_TESTS.json').read_text()),'author artifact tests changed')
    print(json.dumps({'verified':True,'problem_id':'3900015','accepted_author_archive_sha256':author.AUTHOR_ARCHIVE_SHA256,
                      'full_problem_resolved':False,'correction_required':False,'independent_checks':results,
                      'author_subprocess_tests':tests['subprocess_test_count'],
                      'external_coordinated_tamper_checks':tests['external_coordinated_tamper_test_count'],
                      'source_corpus_scope':'Recorded complete-byte audit; optional raw-input replay requires separately supplied files.'},sort_keys=True,indent=2))

if __name__=='__main__':
    try:verify()
    except Exception as exc:
        print('AUDIT VERIFICATION FAILED: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
