"""Reauthenticate the original closed v1 and first-review evidence without writes there."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True
base = Path(__file__).resolve().parent.parent
audit = base.parent
sys.path.insert(0,str(base/'publicfiles/support'))
from safe_output import write_new, json_bytes

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

before = json.loads((base/'private/BASELINE_AUTHENTICATION_BEFORE.json').read_text())
verified = []
for folder,name,key in [('contingent_credited_note_v1','CLOSED_MANIFEST.json','files'),
                        ('whole_package_round1_20261006','CLOSED_EVIDENCE_MANIFEST.json','own_files')]:
    root = audit/folder
    manifest = root/name
    baseline = next(e for e in before['original_closures_verified']
                    if e['reference'] == folder+'/'+name)
    if sha(manifest) != baseline['manifest_sha256']:
        raise RuntimeError('Original manifest changed')
    data = json.loads(manifest.read_text())
    for e in data[key]:
        p = root/e['path']
        if sha(p) != e['sha256'] or p.stat().st_size != e['bytes']:
            raise RuntimeError('Original evidence changed: '+e['path'])
    symlinks = data.get('controlled_symlinks',[])
    for e in symlinks:
        p = root/e['path']
        if not p.is_symlink() or os.readlink(p) != e['target']:
            raise RuntimeError('Original controlled link changed')
    for group in data.get('hardlink_groups',[]):
        if len({((root/n).stat().st_dev,(root/n).stat().st_ino) for n in group}) != 1:
            raise RuntimeError('Original hardlink witness changed')
    expected = {e['path'] for e in data[key]} | {e['path'] for e in symlinks} | {name}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
              if p.is_file() or p.is_symlink()}
    if expected != actual:
        raise RuntimeError('Original closed file inventory changed')
    verified.append(dict(reference=folder+'/'+name,manifest_sha256=sha(manifest),
                         verified_files=len(data[key]),controlled_symlinks=len(symlinks),
                         hardlink_groups=len(data.get('hardlink_groups',[])),exact_inventory=True))
identity = json.loads((base/'BYTE_IDENTITY.json').read_text())
for e in identity['files']:
    if sha(base/'publicfiles'/e['path']) != e['sha256']:
        raise RuntimeError('Protected v2 copied bytes changed')
    if (base/'publicfiles'/e['path']).read_bytes() != (audit/e['original_reference']).read_bytes():
        raise RuntimeError('Protected v2 bytes differ from v1')
borrowed = json.loads((audit/'contingent_credited_note_v1/CLOSED_MANIFEST.json').read_text())['borrowed_input_bindings']
for e in borrowed:
    p=audit/e['reference']
    if sha(p)!=e['sha256'] or p.stat().st_size!=e['bytes']:
        raise RuntimeError('Original borrowed mathematical/priority binding changed')
for e in before['borrowed_original_and_round1_pins']:
    p=audit/e['reference']
    if sha(p)!=e['sha256'] or p.stat().st_size!=e['bytes']:
        raise RuntimeError('Borrowed original/review pin changed')
result=dict(status='PASS',utc=dt.datetime.now(dt.timezone.utc).isoformat(),
            original_closures_verified=verified,unchanged_v2_static_files=len(identity['files']),
            original_mathematical_priority_bindings=len(borrowed),
            original_round1_selected_pins=len(before['borrowed_original_and_round1_pins']),
            original_round1_counterexamples_and_ENOSPC_records_preserved=True,
            no_writes_outside_v2=True,publication_authorized=False,whole_package_acceptance=False)
write_new(base/'private/BASELINE_AUTHENTICATION_AFTER.json',json_bytes(result))
print(json.dumps(result,indent=2))
