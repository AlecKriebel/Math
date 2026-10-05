#!/usr/bin/env python3
"""Strict frozen-payload binding, expected-output replay and integrity mutation controls."""
import hashlib,json,runpy,tempfile,shutil
from pathlib import Path


def check(root):
    m=json.loads((root/'AUTHOR_MANIFEST.json').read_text())
    assert m['schema']=='kourovka-2570-author-v1'
    assert m['problem_id']==2570 and m['turns_used']==5
    assert m['outcome']=='unresolved_scoped_partials'
    records=m['files'];names=[r['path'] for r in records]
    assert len(names)==len(set(names))
    assert set(names)=={'README.md','PROOFS.md','RESEARCH_LOG.md','LIMITATIONS.md','SOURCE_VERIFICATION.json','CHECK_RESULTS.json','verify_math.py','verify_manifest.py'}
    assert {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}==set(names)|{'AUTHOR_MANIFEST.json'}
    assert not any(p.is_symlink() for p in root.rglob('*'))
    for r in records:
        b=(root/r['path']).read_bytes()
        assert len(b)==r['bytes'],r['path']
        assert hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
    return len(records)


def negative_controls(root):
    names=[]
    for name in ['changed_proof','missing_proof','extra_payload','changed_manifest_identity']:
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'payload';shutil.copytree(root,d)
            if name=='changed_proof':(d/'PROOFS.md').write_bytes((d/'PROOFS.md').read_bytes()+b'\nchanged\n')
            elif name=='missing_proof':(d/'PROOFS.md').unlink()
            elif name=='extra_payload':(d/'unexpected.txt').write_text('unexpected')
            else:
                m=json.loads((d/'AUTHOR_MANIFEST.json').read_text());m['problem_id']=20001495;(d/'AUTHOR_MANIFEST.json').write_text(json.dumps(m))
            try:check(d)
            except (AssertionError,FileNotFoundError):names.append(name)
            else:raise AssertionError('Mutation was not rejected: '+name)
    return names


def main():
    root=Path(__file__).resolve().parent
    n=check(root)
    actual=runpy.run_path(str(root/'verify_math.py'))['run']()
    assert actual==json.loads((root/'CHECK_RESULTS.json').read_text())
    print(json.dumps({'passed':True,'bound_files':n,'math_output_matches':True,'rejected_integrity_mutations':negative_controls(root)},indent=2))

if __name__=='__main__':main()
