#!/usr/bin/env python3
"""Check exact package bytes and replay diagnostics without altering the packet."""
import argparse, hashlib, json, pathlib, shutil, subprocess, sys, tempfile
ROOT=pathlib.Path(__file__).resolve().parent
MANIFEST='PACKAGE_MANIFEST.json'

def integrity():
    doc=json.loads((ROOT/MANIFEST).read_text())
    names=set()
    for entry in doc['files']:
        name=entry['path'];p=pathlib.PurePosixPath(name)
        assert str(p)==name and not p.is_absolute() and '..' not in p.parts
        assert '\\' not in name and name!=MANIFEST and name not in names
        names.add(name)
        data=(ROOT/name).read_bytes()
        assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],name
    actual=set()
    for p in ROOT.rglob('*'):
        assert not p.is_symlink(),'symlink prohibited'
        if p.is_file(): actual.add(p.relative_to(ROOT).as_posix())
    assert actual==names|{MANIFEST},('inventory mismatch',actual-names-{MANIFEST},names-actual)
    assert doc['file_count']==len(names)
    return doc

def run_json(script,cwd):
    result=subprocess.run([sys.executable,str(script)],cwd=cwd,check=True,capture_output=True)
    return json.loads(result.stdout)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--integrity-only',action='store_true');args=ap.parse_args()
    doc=integrity();out={'integrity':'PASS','files':doc['file_count']}
    if not args.integrity_only:
        import sympy
        assert sympy.__version__=='1.14.0','install pinned requirements.txt'
        with tempfile.TemporaryDirectory(prefix='low-exponent-replay-') as tmp:
            root=pathlib.Path(tmp)/'packet';shutil.copytree(ROOT,root)
            candidate=root/'candidate'
            original=run_json(candidate/'verify_publication.py',candidate)
            assert original['exact_packet_integrity']=='PASS'
            out['frozen_candidate']='PASS'
            incidence=root/'reviews/incidence_01'
            result=run_json(incidence/'independent_check.py',incidence)
            assert result==json.loads((incidence/'INDEPENDENT_RESULTS.json').read_text())
            result=run_json(incidence/'nonfano_basis_check.py',incidence)
            assert result==json.loads((incidence/'NONFANO_SAITO.json').read_text())
            out['fresh_incidence_and_nonfano']='PASS'
            algebra=root/'reviews/algebra_01'
            expected=(algebra/'ALGEBRA_CHECKS.json').read_bytes()
            run_json(algebra/'verify_algebra.py',algebra)
            assert (algebra/'ALGEBRA_CHECKS.json').read_bytes()==expected
            out['fresh_algebra']='PASS_BYTE_IDENTICAL'
        integrity()
        out['original_packet_unmodified']='PASS'
        out['meaning']='exact finite diagnostics; universal theorem rests on manuscript proof'
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
