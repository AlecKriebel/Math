#!/usr/bin/env python3
"""Bind the preserved original and corrected packet; no writes or network."""
from pathlib import Path
import ast
import difflib
import hashlib
import json
import subprocess
import sys

OLD_MANIFEST = '5ae79fd9ca09fc095a33d7acfa27818377163c1eb2161977ff172cf641420616'
NEW_MANIFEST = '670f3a5365201fdcda372dbd6037aefb062cda2a7dd3537522a19c4a5204fe55'
OLD_PROOF = '76d197a8fc07f7e3796d67a24308531aa315b0aa03a69f3a2122c3bdf7f77b68'
NEW_PROOF = '1ae5a43cbf52ba23c3b39a99a4d5c4c376305edb375a0b343da935e8328210ed'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 VALIDATE_CORRECTION.py ORIGINAL_PACKET_DIRECTORY')
    old = Path(sys.argv[1]).resolve()
    controls = Path(__file__).resolve().parent
    new = controls.parent/'packet'
    binding = json.loads((controls/'CORRECTION_BINDING.json').read_text())
    assert sha(old/'MANIFEST.json') == OLD_MANIFEST
    assert sha(new/'MANIFEST.json') == NEW_MANIFEST
    assert sha(old/'PROOF.md') == OLD_PROOF
    assert sha(new/'PROOF.md') == NEW_PROOF
    expected = {x['path'] for x in binding['files']}
    assert {p.name for p in old.iterdir()} == expected
    assert {p.name for p in new.iterdir()} == expected
    patch = ''
    for entry in sorted(binding['files'],key=lambda x:x['path']):
        name = entry['path']
        for side,root in [('old',old),('new',new)]:
            p = root/name
            assert p.is_file() and not p.is_symlink()
            d = p.read_bytes()
            assert len(d) == entry[side]['bytes']
            assert hashlib.sha256(d).hexdigest() == entry[side]['sha256']
        ob,nb = (old/name).read_bytes(),(new/name).read_bytes()
        assert (ob != nb) == entry['changed']
        patch += ''.join(difflib.unified_diff(ob.decode().splitlines(keepends=True),nb.decode().splitlines(keepends=True),fromfile='original/'+name,tofile='corrected/'+name))
    assert patch.encode() == (controls/'CORRECTION.diff').read_bytes()
    assert hashlib.sha256(patch.encode()).hexdigest() == binding['diff']['sha256']
    a = json.loads((old/'RESULTS.json').read_text())
    b = json.loads((new/'RESULTS.json').read_text())
    a.pop('publication_typo_control')
    b.pop('synthetic_polygon_sign_control')
    assert a == b
    assert a['assertions'] == 79
    mapping = {
        'correct vertex respects second ray':'source vertex respects second ray',
        'published sign typo violates filtration':'synthetic sign flip violates filtration',
        'publication_typo_control':'synthetic_polygon_sign_control',
        '(-1,2) rejected; (-1,-2) satisfies the e1-e2 second-ray bound':'Synthetic (-1,2) rejected; source-consistent (-1,-2) satisfies the e1-e2 second-ray bound',
    }
    class Normalize(ast.NodeTransformer):
        def visit_Constant(self,n):
            if isinstance(n.value,str) and n.value in mapping:
                n.value = mapping[n.value]
            return n
    oa = Normalize().visit(ast.parse((old/'VERIFY.py').read_text()))
    na = ast.parse((new/'VERIFY.py').read_text())
    assert ast.dump(oa) == ast.dump(na)
    assert (old/'CHECK_PACKET.py').read_bytes() == (new/'CHECK_PACKET.py').read_bytes()
    before = {p.name:sha(p) for p in old.iterdir()}
    run = subprocess.run([sys.executable,'-B',str(new/'CHECK_PACKET.py')],check=True,capture_output=True)
    assert not run.stderr
    assert run.stdout == (controls/'REPLAY_OUTPUT.json').read_bytes()
    assert {p.name:sha(p) for p in old.iterdir()} == before
    print(json.dumps({
        'result':'PASS','old_manifest_sha256':OLD_MANIFEST,'new_manifest_sha256':NEW_MANIFEST,
        'old_packet_members_preserved':len(expected),'changed_members':9,'unchanged_members':1,
        'exact_diff_reproduced':True,'math_results_identical':True,'normalized_verifier_AST_identical':True,
        'author_assertions':79,'corrected_packet_replay':'PASS with byte-identical output and three rejected integrity mutations',
        'delta_audit':'pending; this validation does not replace source-description review',
    },indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
