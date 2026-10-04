#!/usr/bin/env python3
"""Strict complete-layout verification; source files are external, never redistributed."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
FROZEN = 'd51066d53d8cbe9e114b044fa828b9adaad61f08140b4f0bac7cfa90a7cdb9eb'
AUDIT = 'ee72facdd1df82372bf40f6bbb21658a67aecdb78c5ce33fea005d07308cb316'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def check_entries(base, entries):
    names = set()
    for entry in entries:
        rel = Path(entry['path'])
        assert not rel.is_absolute() and '..' not in rel.parts
        assert entry['path'] not in names
        names.add(entry['path'])
        p = base / rel
        assert p.is_file() and not p.is_symlink(), str(rel)
        assert p.stat().st_size == entry['bytes'], str(rel)
        assert digest(p) == entry['sha256'], str(rel)
    return names

def strict(root):
    manifest = root / 'RELEASE_MANIFEST.json'
    assert manifest.is_file(), 'release manifest missing'
    data = json.loads(manifest.read_text())
    names = check_entries(root, data['files'])
    assert all(not p.is_symlink() for p in root.rglob('*')), 'symlink in public release'
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual == names | {'RELEASE_MANIFEST.json'}, 'public file-set mismatch'
    assert digest(root/'FROZEN_MANIFEST.json') == FROZEN
    frozen = json.loads((root/'FROZEN_MANIFEST.json').read_text())
    frozen_names = check_entries(root, frozen['payload_files'])
    assert frozen_names == {p.relative_to(root).as_posix()
                            for p in (root/'submission').iterdir() if p.is_file()}
    internal = root/'submission/MANIFEST.sha256'
    assert internal.is_file(), 'internal manifest missing'
    entries = internal.read_text().splitlines()
    assert len(entries) == 9
    for line in entries:
        sha, name = line.split('  ', 1)
        assert Path(name).name == name
        assert digest(root/'submission'/name) == sha
    assert digest(root/'independent-audit/AUDIT_MANIFEST.json') == AUDIT
    audit = json.loads((root/'independent-audit/AUDIT_MANIFEST.json').read_text())
    checked = check_entries(root/'independent-audit', audit['files'])
    assert checked | {'AUDIT_MANIFEST.json'} == {
        p.relative_to(root/'independent-audit').as_posix()
        for p in (root/'independent-audit').rglob('*') if p.is_file()}
    return {'release_payloads':len(names), 'frozen_payloads':len(frozen_names),
            'internal_entries':len(entries), 'audit_payloads':len(checked)}

def run_json(args):
    return json.loads(subprocess.check_output([sys.executable, *map(str,args)], text=True))

def negative_controls():
    controls = {
        'missing_internal_manifest':('submission/MANIFEST.sha256','remove'),
        'altered_proof':('submission/PROOF.md','alter'),
        'missing_full_audit':('independent-audit/INDEPENDENT_AUDIT.md','remove'),
        'altered_full_audit':('independent-audit/INDEPENDENT_AUDIT.md','alter'),
        'extra_public_file':('unlisted.txt','add')}
    result = {}
    for label,(name,action) in controls.items():
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp)/'release';shutil.copytree(ROOT,copy)
            p = copy/name
            if action == 'remove':p.unlink()
            elif action == 'alter':p.write_bytes(p.read_bytes()+b'\nMUTATION\n')
            else:p.write_text('unlisted negative control\n')
            try:strict(copy)
            except (AssertionError,FileNotFoundError):result[label]='rejected'
            else:raise AssertionError('negative control accepted: '+label)
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--sources',type=Path)
    ap.add_argument('--self-test',action='store_true')
    args=ap.parse_args()
    out={'result':'PASS','bindings':strict(ROOT)}
    producer=run_json([ROOT/'submission/verify.py'])
    assert producer['source_hashes_checked']==0
    assert producer['manifest_payload_files_checked']==9
    assert producer==json.loads((ROOT/'independent-audit/checks/supplied-default.json').read_text())
    out['producer_source_free']=producer
    out['source_pdfs_checked']=0
    if args.sources:
        records=json.loads((ROOT/'submission/SOURCE_PROVENANCE.json').read_text())['source_pdfs']
        for record in records:
            p=args.sources/record['filename']
            assert p.read_bytes().startswith(b'%PDF')
            assert p.stat().st_size==record['bytes'] and digest(p)==record['sha256']
        with tempfile.TemporaryDirectory() as tmp:
            copy=Path(tmp)/'release';shutil.copytree(ROOT,copy)
            target=copy/'independent-audit/private';target.mkdir()
            for record in records:shutil.copy2(args.sources/record['filename'],target/record['filename'])
            produced=run_json([copy/'submission/verify.py','--sources',target])
            audited=run_json([copy/'independent-audit/independent_checks.py'])
        assert produced==json.loads((ROOT/'independent-audit/checks/supplied-with-sources.json').read_text())
        assert audited==json.loads((ROOT/'independent-audit/checks/independent-results.json').read_text())
        historical=json.loads((ROOT/'submission/CHECK_RESULTS.json').read_text())
        assert historical['manifest_payload_files_checked']==0
        difference={k for k in produced if produced[k]!=historical[k]}
        assert difference=={'manifest_payload_files_checked'}
        out.update(source_pdfs_checked=4,producer_with_sources=produced,independent_audit=audited,
                   historical_manifest_count=0,fresh_manifest_count=9)
    if args.self_test:out['strict_negative_controls']=negative_controls()
    out['limits']=['The source-free mode does not rerun source-dependent independent controls.',
                   'Finite controls and hashes do not prove the general imported theorem.']
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
