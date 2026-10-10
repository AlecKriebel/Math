#!/usr/bin/env python3
"""Verify all four bound inputs, the exact patch, retained artifacts and replays.
Writes only temporary reconstruction files; never changes bound inputs.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def h(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def check_manifest(root,expected_hash=None):
    mpath=root/'MANIFEST.json'
    if expected_hash is not None:assert h(mpath)['sha256']==expected_hash
    m=json.loads(mpath.read_text())
    assert {p.name for p in root.iterdir()}=={r['path'] for r in m['files']}|{'MANIFEST.json'}
    for r in m['files']:
        p=root/r['path'];assert p.is_file() and not p.is_symlink()
        assert h(p)=={k:r[k] for k in ('bytes','sha256')},str(p)

def main():
    here=Path(__file__).resolve().parent
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=here.parents[1]);args=ap.parse_args()
    root=args.root
    binding=json.loads((here/'DELTA_BINDING.json').read_text())
    roots={'original':root/'release','first_audit':root/'audit_20261005/safe',
           'corrected':root/'corrected_release_20261005','correction_binding':root/'correction_binding_20261005/safe'}
    check_manifest(here)
    for key,p in roots.items():
        b=binding['input_bindings'][key]
        check_manifest(p,b['manifest']['sha256'])
        assert [{'path':x.name,**h(x)} for x in sorted(p.iterdir())]==b['files']
    old=roots['original'];new=roots['corrected'];inventory=[];chunks=[]
    for name in sorted({p.name for p in old.iterdir()}|{p.name for p in new.iterdir()}):
        a=old/name;b=new/name;ah=h(a) if a.exists() else None;bh=h(b) if b.exists() else None
        change='added' if ah is None else 'deleted' if bh is None else 'unchanged' if ah==bh else 'modified'
        inventory.append({'path':name,'change':change,'old':ah,'new':bh})
        if change!='unchanged':
            chunks.extend(difflib.unified_diff(a.read_text().splitlines(True) if a.exists() else [],
                b.read_text().splitlines(True) if b.exists() else [],
                fromfile='a/'+name if a.exists() else '/dev/null',tofile='b/'+name if b.exists() else '/dev/null'))
    recorded=json.loads((roots['correction_binding']/'CHANGE_INVENTORY.json').read_text())['changes']
    assert inventory==[{k:r[k] for k in ('path','change','old','new')} for r in recorded]
    assert inventory==binding['independently_recreated_inventory']
    patch=roots['correction_binding']/'OLD_TO_NEW.diff'
    assert ''.join(chunks).encode()==patch.read_bytes()
    for a,b in [('REPLACEMENT_PROOF.md','NORMALIZATION_RECONSTRUCTION.md'),
                ('independent_controls.py','audit_controls.py'),('INDEPENDENT_CONTROLS.json','AUDIT_CONTROLS.json')]:
        assert (roots['first_audit']/a).read_bytes()==(new/b).read_bytes()
    with tempfile.TemporaryDirectory(prefix='clasp_delta_') as tmp:
        recreated=Path(tmp)/'candidate';shutil.copytree(old,recreated)
        subprocess.run(['patch','--batch','--forward','-p1','-d',str(recreated),'-i',str(patch.resolve())],check=True,capture_output=True,text=True)
        assert {p.name for p in recreated.iterdir()}=={p.name for p in new.iterdir()}
        for p in new.iterdir():assert p.read_bytes()==(recreated/p.name).read_bytes()
        # The reconstructed candidate must run successfully after relocation.
        subprocess.run([sys.executable,'-B',str(recreated/'verify_release.py')],check=True,capture_output=True,text=True)
    for p in [old/'verify_release.py',new/'verify_release.py',roots['first_audit']/'verify_audit.py']:
        subprocess.run([sys.executable,'-B',str(p)],check=True,capture_output=True,text=True)
    terminal=subprocess.run([sys.executable,'-B',str(here/'terminal_step_controls.py')],check=True,capture_output=True,text=True)
    assert json.loads(terminal.stdout)==json.loads((here/'TERMINAL_STEP_CONTROLS.json').read_text())
    # Recheck hashes after execution as well.
    for key,p in roots.items():check_manifest(p,binding['input_bindings'][key]['manifest']['sha256'])
    print(json.dumps({'status':'PASS','delta_verdict':'ACCEPTED_QUALIFIED_PRIOR_FORMULA',
        'exact_input_manifests_verified':4,'inventory_entries':len(inventory),
        'exact_diff_recomputed':True,'patch_reconstruction_byte_identical':True,
        'retained_audit_artifacts_byte_identical':True,'all_replays_match':True,
        'relocated_candidate_replay_passed':True,'terminal_step_checks_passed':True,
        'original_and_first_audit_preserved':True},indent=2,sort_keys=True))

if __name__=='__main__':main()
