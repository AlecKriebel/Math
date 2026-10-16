#!/usr/bin/env python3
"""Root custody verification of the frozen administrative V3 component."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat

HERE = Path(__file__).absolute().parent
CASE = HERE.parent
BASE = HERE / 'admin_helper_v3'

def read(path, pin=None):
    path = path.absolute()
    for parent in [path, *path.parents]:
        assert not parent.is_symlink(), str(parent)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        st = os.fstat(stream.fileno())
        assert stat.S_ISREG(st.st_mode), str(path)
        raw = stream.read()
    if pin:
        assert len(raw) == pin['bytes'], str(path)
        assert hashlib.sha256(raw).hexdigest() == pin['sha256'], str(path)
        if 'mode' in pin:
            assert f'{stat.S_IMODE(st.st_mode):04o}' == pin['mode'], str(path)
    return raw

def sha(raw): return hashlib.sha256(raw).hexdigest()

def main():
    sealraw = read(BASE / 'SHA256_SEALS.json')
    assert sha(sealraw) == 'b3dfbb442b324adbd7e0f777fb46104e70aef8f51a57692bd53abf60c158c254'
    seal = json.loads(sealraw)
    for name, pin in seal['positive_public_files'].items():
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        read(BASE / name, pin)
    custody = json.loads(read(CASE / seal['private_custody_map']['path'], seal['private_custody_map']))
    for group in ['positive_private_files', 'positive_original_sources']:
        for name, pin in custody[group].items():
            assert not Path(name).is_absolute() and '..' not in Path(name).parts
            read(CASE / name, pin)
    kit = custody['repository_kit']
    read(Path(kit['path']), kit)
    assert len(custody['positive_private_files']) == seal['private_files_count'] == 4840
    assert len(custody['positive_original_sources']) == seal['original_sources_count'] == 42
    review = json.loads(read(BASE / 'publication_v3_software_adversary2/PUBLIC_SEAL.json'))
    assert review['result'] == 'PASS' and review['tests_passed'] == 28
    tests = json.loads(read(BASE / 'publication_v3_software_adversary2/TEST_SUMMARY.json'))
    assert len(tests['tests']) == 28 and all(t['status'] == 'PASS' for t in tests['tests'])
    assert tests['protected_unchanged'] is True and tests['live_Zenodo_Sheet_requests'] == 0
    assert review['source_sha256'] == seal['helper_sha256'] == tests['source_sha256']
    assert review['adoption_sha256'] == seal['adoption_sha256'] == tests['adoption_sha256']
    protected = {
        'private_sources/publication_admin_helper/PRODUCTION_STATE.json': '0c0359d83619cdecd0104051d516202b164a6e0e1183763650797f029d2a9d77',
        'private_sources/publication_admin_helper_v2/PRODUCTION_STATE.json': '46e1b481e5291520fd1d2fb2ca9403b9e8184e097b8d240a9b1d4cc0ea4db66c',
        'private_sources/publication_admin_helper_v3/PRODUCTION_STATE.json': 'a05775be027940916f152b02cad8c410f8d9db152b270fe757173574510d83f9',
    }
    for name, expected in protected.items(): assert sha(read(CASE / name)) == expected
    whole = read(CASE / 'ROOT_WHOLE_REVIEW_2_ACCEPTANCE.json')
    assert sha(whole) == '01fe1ab553f8f17a78f222863cb6afa173323c7bd63ed32b55879ca3db4299fe'
    result = {
        'schema': 1, 'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'result': 'PASS_PUBLICATION_V3_COMPONENT', 'case': 'pr411_6800014',
        'helper_sha256': seal['helper_sha256'], 'adoption_sha256': seal['adoption_sha256'],
        'whole_acceptance_sha256': sha(whole), 'outer_seal_sha256': sha(sealraw),
        'positive_public_files_verified': len(seal['positive_public_files']),
        'private_files_verified': 4840, 'original_sources_verified': 42,
        'fresh_independent_tests_passed': 28, 'producer_baseline_tests_passed': 8,
        'root_prior_actual_offline_replays': '8 initial and 8 repaired tests; exact final change reviewed as operation-bound custody clearing; final 8-test producer run and fresh independent 28 groups accepted',
        'root_actual_preliminary_recovery': 'Eight protected GETs, before final repaired-code acceptance; actual state a057 preserved; tracker freshly rechecks publication',
        'historical_states_verified_unchanged': protected,
        'scientific_bytes_and_submitted_metadata_unchanged': True,
        'known_publication': {'id': 23331232, 'doi': '10.5281/zenodo.23331232', 'publish_retry_authorized': False},
        'remaining_live_step': 'Never-attempted exact four-cell tracker append after fresh native scope and publication checks',
        'limits': 'Administrative component acceptance; offline controls do not certify future production outcomes. External editors can race non-atomic API checks. No remote requests or mutations in this verification.',
    }
    out = HERE / 'ROOT_PUBLICATION_V3_COMPONENT_ACCEPTANCE.json'
    with out.open('xb') as stream:
        stream.write((json.dumps(result, indent=2, sort_keys=True) + '\n').encode())
        stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({'acceptance_sha256': sha(out.read_bytes()), 'public': len(seal['positive_public_files']), 'private': 4840, 'sources': 42}))

if __name__ == '__main__': main()
