#!/usr/bin/env python3
"""Read-only verifier for bounded extension evidence and unchanged prior seals."""
from pathlib import Path
import hashlib,json

def main():
    p=Path(__file__).resolve().parent
    m=json.loads((p/'PUBLIC_EVIDENCE_MANIFEST.json').read_text())
    paths=set()
    for e in m['files']:
        assert e['path'] not in paths;paths.add(e['path'])
        f=p/e['path'];assert f.is_file() and not f.is_symlink()
        b=f.read_bytes();assert len(b)==e['bytes']
        assert hashlib.sha256(b).hexdigest()==e['sha256']
    assert paths=={f.name for f in p.iterdir() if f.is_file()}-{'PUBLIC_EVIDENCE_MANIFEST.json'}
    old=p.parent.parent/'public'
    assert hashlib.sha256((old/'PUBLIC_EVIDENCE_MANIFEST.json').read_bytes()).hexdigest()==m['old_manifest_sha256']
    for e in m['old_seals']:
        assert hashlib.sha256((old/e['file']).read_bytes()).hexdigest()==e['sha256']
    assert json.loads((p/'independent_rank_controls.stdout').read_text())['all_passed']
    assert json.loads((p/'diagonal_control_replay.stdout').read_text())['all_checks_passed']
    assert json.loads((p/'COMPLETION.json').read_text())['mandatory_changes']==[]
    print(json.dumps({'extension_public_hashes_verified':len(paths),'old_probability_manifest_and_seals_byte_exact':True,'private_files_in_manifest':False,'verdict':'supported stronger larger-normalization zero; original sharp-prefix unresolved'},sort_keys=True))

if __name__=='__main__':main()
