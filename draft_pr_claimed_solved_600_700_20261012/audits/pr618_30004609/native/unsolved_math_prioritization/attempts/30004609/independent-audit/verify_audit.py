#!/usr/bin/env python3
"""Verify audit integrity, frozen inputs, and both exact check suites offline."""
from pathlib import Path, PurePosixPath
import hashlib,json,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent

def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    manifest=json.loads((ROOT/'AUDIT_MANIFEST.json').read_text())
    for entry in manifest['files']:
        data=(ROOT/entry['path']).read_bytes()
        assert len(data)==entry['bytes'],entry['path']
        assert sha(data)==entry['sha256'],entry['path']
    source=(ROOT/'AUDITED_INPUTS.json').read_bytes()
    assert sha(source)==manifest['audited_author_manifest_sha256']
    inputs=json.loads(source)
    archive=(ROOT/'inputs/author.zip').read_bytes()
    assert len(archive)==19956 and sha(archive)==manifest['audited_author_zip_sha256']
    with tempfile.TemporaryDirectory(prefix='low-exponent-audit-') as tmp:
        tmp=Path(tmp)
        with zipfile.ZipFile(ROOT/'inputs/author.zip') as z:
            assert sorted(z.namelist())==sorted(e['path'] for e in inputs['files'])
            for entry in inputs['files']:
                p=PurePosixPath(entry['path'])
                assert not p.is_absolute() and '..' not in p.parts
                data=z.read(entry['path'])
                assert len(data)==entry['bytes'] and sha(data)==entry['sha256']
                dest=tmp.joinpath(*p.parts);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        author=tmp/'unsolved_math_prioritization/attempts/30004609'
        run=subprocess.run([sys.executable,str(author/'check.py')],cwd=author,check=True,capture_output=True)
        assert run.stdout==(author/'RESULTS.json').read_bytes()
        assert run.stdout==(ROOT/'AUTHOR_CHECK_RERUN.json').read_bytes()
        independent=subprocess.run([sys.executable,str(ROOT/'independent_checks.py')],cwd=tmp,check=True,capture_output=True)
        assert independent.stdout==(ROOT/'INDEPENDENT_CHECKS.json').read_bytes()
    print(json.dumps({'audit_integrity':'PASS','frozen_author_files':inputs['file_count'],
      'author_checker':'PASS_BYTE_IDENTICAL','independent_checker':'PASS_BYTE_IDENTICAL',
      'proof_sha256':next(e['sha256'] for e in inputs['files'] if e['path'].endswith('/PROOF.md'))},indent=2))

if __name__=='__main__':main()
