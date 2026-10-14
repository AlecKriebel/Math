#!/usr/bin/env python3
"""Root verifies final finite ADMIN review custody and unchanged action code."""
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat

CASE = Path(__file__).absolute().parent.parent
BASE = CASE / 'merge_preparation_v3'
PRIVATE = CASE / 'private_sources/merge_preparation_v3'

def sha(raw): return hashlib.sha256(raw).hexdigest()
def read(path, pin=None):
    for parent in [path, *path.parents]: assert not parent.is_symlink(), str(parent)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        st = os.fstat(stream.fileno()); assert stat.S_ISREG(st.st_mode), str(path)
        raw = stream.read()
    if pin:
        assert sha(raw) == pin['sha256'] and len(raw) == pin['bytes'], str(path)
        expected = int(pin.get('mode_octal', '0o644'), 8)
        assert stat.S_IMODE(st.st_mode) == expected, str(path)
    return raw

def main():
    handraw = read(PRIVATE / 'FINAL_HANDOFF.json')
    assert sha(handraw) == 'b2d712dab8359b1eac5144bf03f2aaf9c5f559199def6ca1045fedd0181b09fc'
    hand = json.loads(handraw)
    seal = read(BASE / 'FINAL_SEAL.json'); white = read(BASE / 'PUBLICATION_WHITELIST.json')
    assert sha(seal) == hand['actual_public_seal_sha256'] == '0ace16c00547fc84191231b38735bbfe21ee678e94c0f8fd578743dd76fe52ac'
    assert sha(white) == hand['actual_public_whitelist_sha256']
    entries = json.loads(white)['entries']
    for pin in entries:
        assert not Path(pin['path']).is_absolute() and '..' not in Path(pin['path']).parts
        read(BASE / pin['path'], pin)
    pmapraw = read(CASE / hand['private_positive_map']['path'])
    assert sha(pmapraw) == hand['private_positive_map']['sha256']
    pins = json.loads(pmapraw)['entries']
    for pin in pins:
        assert not Path(pin['path']).is_absolute() and '..' not in Path(pin['path']).parts
        read(CASE / pin['path'], pin)
    assert len(pins) == hand['private_positive_map']['count'] == 210
    for n, s in hand['sources_sha256'].items(): assert sha(read(BASE / n)) == s
    original = read(CASE / 'merge_preparation/pr411_admin.py')
    current = read(BASE / 'pr411_admin.py')
    assert sha(original) == '1a3963efbab49cf96ea75326cc77b9c3c7455a6c87140a382fc294e739afa131'
    before, after = ast.parse(original).body, ast.parse(current).body
    assert len(before) == len(after) == 84
    changed = [getattr(x, 'name', type(x).__name__) for x, y in zip(before, after)
               if ast.dump(x, include_attributes=False) != ast.dump(y, include_attributes=False)]
    assert changed == ['evidence']
    assert read(BASE / 'verify_custody.py') == read(CASE / 'merge_preparation/verify_custody.py')
    assert sha(read(CASE / 'merge_preparation/FINAL_SEAL.json')) == hand['original_accepted_seal_sha256']
    for mode in ['NORMAL', 'OPTIMIZED']:
        result = json.loads(read(PRIVATE / ('final_software_adversary/INDEPENDENT_' + mode + '.json')))
        assert result['pass'] == result['independent_asserted_controls'] == 315 and result['fail'] == 0
        assert result['unchanged_AST_nodes'] == 83 and result['native_calls'] == 0
        assert len(result['results']) == 321
        assert all(r['result'] in ('PASS', 'OBSERVED') for r in result['results'])
    whole = read(CASE / 'ROOT_WHOLE_REVIEW_2_ACCEPTANCE.json')
    assert sha(whole) == '01fe1ab553f8f17a78f222863cb6afa173323c7bd63ed32b55879ca3db4299fe'
    actual_schema = read(CASE / 'private_sources/root_merge_v3_actual_schema_replay/NATIVE.json')
    assert sha(actual_schema) == '8a9420526c87f5c5da79cf482cc2782a8b64378de6c1602480d9fbda94ceaa30'
    out = {'schema': 1, 'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
           'result': 'PASS_MERGE_V3_ADMINISTRATION_COMPONENT', 'case': 'pr411_6800014',
           'helper_sha256': sha(current), 'whole_acceptance_sha256': sha(whole),
           'outer_seal_sha256': sha(seal), 'private_handoff_sha256': sha(handraw),
           'public_files_verified': len(entries) + 2, 'private_objects_verified': len(pins),
           'fresh_independent_controls_per_mode': 315, 'independent_boundary_observations_per_mode': 6,
           'unchanged_top_level_AST_nodes': 83, 'only_changed_AST_node': 'evidence',
           'root_actual_five_metadata_schema_outcomes_capture_sha256': sha(actual_schema),
           'accepted_prior_action_boundaries_unchanged': True,
           'root_read': 'Exact evidence() diff, final independent oracle, reports and relevant full documentation read; original action implementation previously read in full',
           'live_operation_approval': False,
           'limits': 'Finite ADMIN component acceptance only. Separate genuine publication/tracker bindings, fresh GETs, concrete plan approval and authentic mutation receipts are required for every live phase. No scientific bytes changed and no remote request in this custody verification.'}
    path = CASE / 'ROOT_MERGE_V3_COMPONENT_ACCEPTANCE.json'
    with path.open('xb') as stream:
        stream.write((json.dumps(out, sort_keys=True, indent=2) + '\n').encode()); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({'acceptance_sha256': sha(path.read_bytes()), 'public': len(entries)+2, 'private': len(pins)}))

if __name__ == '__main__': main()
