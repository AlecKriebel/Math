#!/usr/bin/env python3
"""Test proposed helpers against isolated captured copies; no release writes."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import sys
import tempfile

HERE = Path(__file__).absolute().parent
A = HERE.parents[1]
P = A / 'publication'
V = runpy.run_path(str(P / 'verify_package.py'))


def captured():
    payload = {n: (P / ('PACKAGE_README.md' if n == 'README.md' else n)).read_bytes()
               for n in V['PUBLICATION_FILES']}
    payload.update({n: (A/n).read_bytes() for n in V['ROOT_FILES']})
    for family, names in V['REVIEW_FILES'].items():
        for n in names:
            name = 'reviews/' + family + '/' + n
            payload[name] = (A/name).read_bytes()
    snapshot = V['json_data']((A/'SCOPE_AND_SNAPSHOT.json').read_bytes())
    for n in V['native_bindings'](snapshot):
        payload['native/'+n] = (A/'native'/n).read_bytes()
    V['inspect_payload'](payload)
    return payload


def manifest_for(payload):
    return {'schema': 1, 'problem_id': '2306086', 'original_head': V['HEAD'],
            'file_count': len(payload), 'raw_third_party_fulltexts_included': False,
            'files': [{'path': name, 'bytes': len(data), 'sha256': V['digest'](data)}
                      for name, data in sorted(payload.items())]}


def stage(root, payload):
    root.mkdir()
    for name, data in payload.items():
        path = root/name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    (root/V['MANIFEST']).write_text(json.dumps(manifest_for(payload), indent=2)+'\n')


def replace_manifest_entry(root, name):
    path = root/V['MANIFEST']; doc = json.loads(path.read_text())
    data = (root/name).read_bytes()
    for record in doc['files']:
        if record['path'] == name:
            record.update(bytes=len(data), sha256=V['digest'](data))
    path.write_text(json.dumps(doc))


def hostile_controls(root):
    cases = ['changed_pdf', 'missing_proof', 'extra_file', 'extra_cache', 'empty_directory',
             'duplicate_entry', 'unsafe_parent_path', 'unsafe_absolute_path',
             'unsafe_backslash_path', 'duplicate_manifest_json_key', 'duplicate_claim_json_key',
             'file_symlink', 'directory_symlink', 'claim_inflation_rehashed',
             'claim_integer_for_boolean_rehashed', 'native_change_rehashed',
             'snapshot_change_rehashed', 'gate_change_rehashed', 'extra_allowlist_member_rehashed',
             'manifest_negative_size', 'manifest_boolean_schema', 'nonfinite_json']
    rejected = []
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='hostile-') as temp:
            target = Path(temp)/'packet'; shutil.copytree(root, target)
            manifest_path = target/V['MANIFEST']
            manifest = json.loads(manifest_path.read_text())
            if case == 'changed_pdf':
                path = target/'real_schlicht_preschwarzian.pdf'; path.write_bytes(path.read_bytes()+b'changed')
            elif case == 'missing_proof':
                (target/'real_schlicht_preschwarzian.tex').unlink()
            elif case == 'extra_file': (target/'extra.txt').write_text('reject')
            elif case == 'extra_cache':
                path = target/'__pycache__'; path.mkdir(); (path/'cache.pyc').write_bytes(b'reject')
            elif case == 'empty_directory': (target/'empty').mkdir()
            elif case == 'duplicate_entry': manifest['files'].append(dict(manifest['files'][0])); manifest['file_count']+=1
            elif case.startswith('unsafe_'):
                manifest['files'][0]['path'] = {'unsafe_parent_path':'../escaped',
                    'unsafe_absolute_path':'/escaped', 'unsafe_backslash_path':'bad\\name'}[case]
            elif case == 'duplicate_manifest_json_key':
                manifest_path.write_text(manifest_path.read_text().replace('{', '{"schema":1,', 1))
            elif case == 'duplicate_claim_json_key':
                path = target/'CLAIM_SCOPE.json'; path.write_text(path.read_text().replace('{', '{"original_pr":662,', 1))
                replace_manifest_entry(target, 'CLAIM_SCOPE.json')
            elif case == 'file_symlink':
                path = target/'real_schlicht_preschwarzian.tex'; path.unlink()
                path.symlink_to(root/'real_schlicht_preschwarzian.tex')
            elif case == 'directory_symlink':
                path = target/'reviews/geometry_01'; shutil.rmtree(path)
                path.symlink_to(root/'reviews/geometry_01', target_is_directory=True)
            elif case.startswith('claim_'):
                path = target/'CLAIM_SCOPE.json'; doc=json.loads(path.read_text())
                if case == 'claim_inflation_rehashed': doc['historical_firstness_claim']=True
                else: doc['unrefereed']=1
                path.write_text(json.dumps(doc)); replace_manifest_entry(target, 'CLAIM_SCOPE.json')
            elif case in ('native_change_rehashed', 'snapshot_change_rehashed', 'gate_change_rehashed'):
                name = {'native_change_rehashed': V['NATIVE']+'/author/PROOF_PARTIALS.md',
                        'snapshot_change_rehashed':'SCOPE_AND_SNAPSHOT.json',
                        'gate_change_rehashed':'PRIORITY_GATE_ACCEPTANCE.json'}[case]
                path=target/name; path.write_bytes(path.read_bytes()+b'\n')
                replace_manifest_entry(target,name)
            elif case == 'extra_allowlist_member_rehashed':
                path=target/'extra.txt'; path.write_text('reject')
                manifest['files'].append({'path':'extra.txt','bytes':6,'sha256':V['digest'](b'reject')})
                manifest['file_count']+=1
            elif case == 'manifest_negative_size': manifest['files'][0]['bytes']=-1
            elif case == 'manifest_boolean_schema': manifest['schema']=True
            elif case == 'nonfinite_json':
                name='ROOT_NUMERICAL_REPRODUCTION.json'; path=target/name
                path.write_text('{"nonfinite":NaN}')
                replace_manifest_entry(target,name)
            manifest_cases = {'duplicate_entry','unsafe_parent_path','unsafe_absolute_path',
                              'unsafe_backslash_path','extra_allowlist_member_rehashed',
                              'manifest_negative_size','manifest_boolean_schema'}
            if case in manifest_cases: manifest_path.write_text(json.dumps(manifest))
            try: V['verify'](target)
            except (ValueError, KeyError, FileNotFoundError, NotADirectoryError): rejected.append(case)
            else: raise RuntimeError('Hostile control accepted: '+case)
    return rejected


def main():
    scratch=HERE/'tmp'; scratch.mkdir(exist_ok=True)
    os.environ['TMPDIR']=str(scratch); tempfile.tempdir=None
    payload=captured()
    result={'utc':datetime.now(timezone.utc).isoformat(), 'python_executable':sys.executable,
            'completion_percent':{'package_helpers':85,'pr662':70},
            'release_files_written':False,
            'source_pins':{n:V['digest']((P/n).read_bytes()) for n in ('build_package.py','verify_package.py')}}
    with tempfile.TemporaryDirectory(prefix='author-tests-') as tmp:
        packet=Path(tmp)/'packet'; stage(packet,payload)
        result['baseline']=V['verify'](packet)
        result['hostile_controls_rejected']=hostile_controls(packet)
        result['exact_replay']=V['replay'](packet,False)
        if '--numerical' in sys.argv:
            result['optional_numerical_replay']=V['replay'](packet,True)
        result['preserved']=V['verify'](packet)==result['baseline']
    (HERE/'TEST_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
