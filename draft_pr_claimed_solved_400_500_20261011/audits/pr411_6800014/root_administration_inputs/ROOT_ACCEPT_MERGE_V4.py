#!/usr/bin/env python3
"""Root accepts only the exact producer-encoding guard and its frozen custody."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat

CASE = Path(__file__).absolute().parent.parent
BASE = CASE / 'merge_preparation_v4'
PRIVATE = CASE / 'private_sources/merge_preparation_v4'

def sha(raw): return hashlib.sha256(raw).hexdigest()
def read(path, pin=None):
    for parent in [path, *path.parents]: assert not parent.is_symlink(), str(parent)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        st = os.fstat(stream.fileno()); assert stat.S_ISREG(st.st_mode), str(path)
        raw = stream.read()
    if pin:
        assert sha(raw) == pin['sha256'] and len(raw) == pin['bytes'], str(path)
        if 'mode' in pin: assert stat.S_IMODE(st.st_mode) == int(pin['mode'][-3:], 8), str(path)
    return raw

def main():
    handraw = read(PRIVATE / 'FINAL_HANDOFF.json')
    assert sha(handraw) == '15f9d40c1758904bb02bb88637b9c5144834a320e6342ae485dabc685c9587b0'
    hand = json.loads(handraw)
    seal = read(BASE / 'FINAL_SEAL.json'); white = read(BASE / 'PUBLICATION_WHITELIST.json')
    assert sha(seal) == hand['actual_seal_sha256'] == 'a03d98052f442e212635016c20491d242d27f05d4ebb7a50a97dda5f550c65c8'
    assert sha(white) == hand['actual_whitelist_sha256']
    entries = json.loads(white)['entries']
    for pin in entries:
        assert not Path(pin['path']).is_absolute() and '..' not in Path(pin['path']).parts
        read(BASE / pin['path'], pin)
    rawmap = read(CASE / hand['private_positive_pinmap_path'])
    assert sha(rawmap) == hand['private_positive_pinmap_sha256']
    pins = json.loads(rawmap)['entries']
    for pin in pins:
        assert not Path(pin['path']).is_absolute() and '..' not in Path(pin['path']).parts
        read(CASE / pin['path'], pin)
    assert len(pins) == hand['private_positive_objects'] == 1465
    old = read(CASE / 'merge_preparation_v3/pr411_admin.py')
    new = read(BASE / 'pr411_admin.py')
    assert sha(old) == 'ed85c2b6386ffa3750eba56f4450adf304b6040db37476dbce3e08ae997858de'
    assert sha(new) == hand['helper_sha256'] == 'e4c9bd76594127b23cf6439df0b2c7a965f39b8f027d6debdb7cdf8e393aaa14'
    prior = "need(original_append.get('payload') == expected_payload and original_append['intent'].get('payload_sha256') == digest(encoded(expected_payload)),"
    repaired = "need(encoded(original_append.get('payload')) == encoded(expected_payload)\n             and original_append['intent'].get('payload_sha256') == digest((json.dumps(expected_payload, sort_keys=True, indent=2, ensure_ascii=False) + '\\n').encode()),"
    assert new.decode().count(repaired) == 1 and new.decode().replace(repaired, prior).encode() == old
    assert read(BASE / 'verify_custody.py') == read(CASE / 'merge_preparation_v3/verify_custody.py')
    for mode in ['normal', 'optimized']:
        result = json.loads(read(PRIVATE / ('software_adversary/verified_' + mode + '/results.json')))
        assert result['controls'] == 26 and result['counters']['native_requests'] == 0
        assert all(r['actual_accept'] is r['expected_accept'] for r in result['results'])
    whole = read(CASE / 'ROOT_WHOLE_REVIEW_2_ACCEPTANCE.json')
    assert sha(whole) == '01fe1ab553f8f17a78f222863cb6afa173323c7bd63ed32b55879ca3db4299fe'
    own = read(CASE / 'private_sources/root_merge_v4_append_replay/NATIVE.json')
    assert sha(own) == '754732a195996bd963d496d845ccd629e2431ad789782b1d0a581c7cde9dee51'
    proof = json.loads(read(BASE / 'ACTUAL_ENCODER_PROOF.json'))
    assert proof['actual_pretty_newline_sha256'] == proof['original_payload_sha256'] == 'd83aaba20b3f7cdb3438c742b2eaf2119624fb793202b55eca254fe7f07ef03b'
    out = {'schema': 1, 'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
           'result': 'PASS_MERGE_V4_ADMINISTRATION_COMPONENT', 'case': 'pr411_6800014',
           'helper_sha256': sha(new), 'whole_acceptance_sha256': sha(whole),
           'outer_seal_sha256': sha(seal), 'private_handoff_sha256': sha(handraw),
           'public_files_verified': len(entries) + 2, 'private_objects_verified': len(pins),
           'fresh_independent_controls_per_mode': 26, 'root_actual_offline_controls': 32,
           'root_actual_offline_capture_sha256': sha(own), 'exact_source_reconstruction_to_accepted_V3': True,
           'unchanged_other_top_level_nodes': 83, 'only_repair': 'Typed payload equality and exact pretty JSON plus newline producer digest at append guard',
           'root_read': 'Exact whole source diff, independent test oracle, finite reports, actual encoder proof and documentation read; original action source previously read and preserved',
           'native_requests_in_this_verification': 0, 'native_mutations': 0, 'live_phase_approval': False,
           'limits': 'Archived ADMIN originals, virtual asset hashes and archived-window clock support the narrow repair only. Every live phase needs genuine fresh Sheet/publication verification and separate exact plan approval. Paper, 99 science files, native source head and original receipts are unchanged.'}
    path = CASE / 'ROOT_MERGE_V4_COMPONENT_ACCEPTANCE.json'
    with path.open('xb') as stream:
        stream.write((json.dumps(out, indent=2, sort_keys=True) + '\n').encode()); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({'acceptance_sha256': sha(path.read_bytes()), 'public': len(entries)+2, 'private': len(pins)}))

if __name__ == '__main__': main()
