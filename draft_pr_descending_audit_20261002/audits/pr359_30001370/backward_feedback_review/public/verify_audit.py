#!/usr/bin/env python3
"""Read-only checker of the finite public/private closure and raw receipts.

Before sealing, --draft validates available receipt consistency. The final
default checks every public/private file, directory, byte count, SHA256 and
mode, and rejects unexpected root artifacts. It performs no writes/network.
"""
from pathlib import Path
import argparse
import hashlib
import json
import stat

ROOT = Path(__file__).resolve().parents[1]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pairs(rows):
    out = {}
    for key,value in rows:
        if key in out:
            raise ValueError('duplicate JSON key: '+key)
        out[key]=value
    return out

def read_json(path):
    return json.loads(path.read_bytes(),object_pairs_hook=pairs)

def check_streams(directory, record):
    label=record['label']
    assert read_json(directory/(label+'.json')) == record
    for stream in ('stdout','stderr'):
        data=(directory/(label+'.'+stream)).read_bytes()
        assert len(data)==record[stream+'_bytes']
        assert sha(data)==record[stream+'_sha256']
    comparison=record.get('complete_old_byte_comparison')
    if comparison:
        expected=(directory/(label+'.expected')).read_bytes()
        actual=(directory/(label+'.stdout')).read_bytes()
        assert len(expected)==comparison['expected_bytes']
        assert sha(expected)==comparison['expected_sha256']
        assert (expected==actual)==comparison['byte_exact']
        first=next((i for i,(a,b) in enumerate(zip(expected,actual)) if a!=b),None)
        if first is None and len(expected)!=len(actual):
            first=min(len(expected),len(actual))
        assert first==comparison['first_difference_offset']

def check_receipts():
    first=read_json(ROOT/'public'/'SOURCE_FIRST_SEAL.json')
    note=(ROOT/'public'/'SOURCE_FIRST.md').read_bytes()
    assert first['candidate_read_before_seal'] is False
    assert len(note)==first['size'] and sha(note)==first['sha256']
    for path,digest in first['sources'].items():
        assert sha((ROOT/path).read_bytes())==digest
    replays=read_json(ROOT/'public'/'REPLAY_RECEIPTS.json')
    for row in replays['records']:
        check_streams(ROOT/'private'/'replays',row)
    assert replays['candidate_before_after_full_bytes_unchanged'] is True
    outputs={r['label']:r for r in replays['records']}
    for label in ('existing_check_turn_1','existing_check_turn_2','existing_check_turn_3',
                  'existing_review_check_independent'):
        assert outputs[label]['exit_code']==0
        assert outputs[label]['stderr_bytes']==0
        assert outputs[label]['complete_old_byte_comparison']['byte_exact'] is True
    for label in ('existing_verify_packet','existing_verify_packet_with_sources'):
        assert outputs[label]['exit_code']==0 and outputs[label]['stderr_bytes']==0
    source_wrapper=read_json(ROOT/'private'/'replays'/'existing_verify_packet_with_sources.stdout')
    assert source_wrapper['source_hashes']['verified_files']==3
    custody=read_json(ROOT/'public'/'PACKET_CUSTODY.json')
    assert custody['status']=='PASS_READ_ONLY_BINDING'
    assert custody['all_files_count']==38
    assert custody['branch_before']==custody['branch_after']=='main'
    for row in custody['native_commands']:
        check_streams(ROOT/'private'/'bindings',row)
        assert row['exit_code']==0
    assert len(custody['old_author_full_byte_comparisons'])==25
    assert all(r['full_old_bytes_equal_frozen_head'] for r in custody['old_author_full_byte_comparisons'])
    assert all(e['valid'] for m in custody['nested_manifests'] for e in m['entries'])
    independent=(ROOT/'public'/'INDEPENDENT_CHECKS.json').read_bytes()
    assert independent==(ROOT/'private'/'replays'/'independent_backward_feedback.stdout').read_bytes()
    assert json.loads(independent)['status']=='PASS'
    portable=read_json(ROOT/'public'/'PORTABLE_CONTROLS.json')
    output311=(ROOT/'private'/'replays'/'portable_controls_python311.stdout').read_bytes()
    output314=(ROOT/'private'/'replays'/'portable_controls_python314.stdout').read_bytes()
    assert portable['portable_verifier_stdout_byte_exact_311_314'] is True
    assert portable['raw_control_checker_cross_runtime_byte_exact'] is False
    assert output311==output314
    assert len(output311)==portable['stdout_bytes'] and sha(output311)==portable['stdout_sha256']
    for label in ('portable_controls_python311','portable_controls_python314'):
        assert outputs[label]['exit_code']==0 and outputs[label]['stderr_bytes']==0
    source=read_json(ROOT/'public'/'SOURCE_CUSTODY.json')
    assert len(source['manifest_source_entries'])==3
    for row in source['manifest_source_entries']:
        data=(ROOT/'private'/'candidate_source_aliases'/row['name']).read_bytes()
        assert row['verified'] is True
        assert len(data)==row['actual_bytes'] and sha(data)==row['actual_sha256']
    return {'native_program_runs':len(replays['records']),
            'binding_native_commands':len(custody['native_commands']),
            'source_hashes':3,'scope_files':38,
            'manifest_entries':sum(m['entry_count'] for m in custody['nested_manifests'])}

def check_closure():
    seal=read_json(ROOT/'SEAL.json')
    manifest_raw=(ROOT/'MANIFEST.json').read_bytes()
    assert set(seal)=={'schema_version','closed_utc','manifest_path','manifest_bytes','manifest_sha256','manifest_mode','no_writes_after_seal'}
    assert seal['schema_version']==1 and seal['no_writes_after_seal'] is True
    assert seal['manifest_path']=='MANIFEST.json'
    assert len(manifest_raw)==seal['manifest_bytes'] and sha(manifest_raw)==seal['manifest_sha256']
    assert format(stat.S_IMODE((ROOT/'MANIFEST.json').stat().st_mode),'04o')==seal['manifest_mode']
    manifest=json.loads(manifest_raw,object_pairs_hook=pairs)
    assert set(manifest)=={'schema_version','closed_utc','scope','entries'}
    assert manifest['schema_version']==1 and manifest['closed_utc']==seal['closed_utc']
    assert manifest['scope']==['public','private']
    assert set(p.name for p in ROOT.iterdir())=={'public','private','MANIFEST.json','SEAL.json'}
    actual=set()
    for namespace in manifest['scope']:
        actual.add(namespace)
        for p in (ROOT/namespace).rglob('*'):
            assert not p.is_symlink()
            actual.add(str(p.relative_to(ROOT)))
    entries=manifest['entries']
    assert len(entries)==len({r['path'] for r in entries})
    assert actual==set(r['path'] for r in entries)
    for row in entries:
        p=ROOT/row['path']
        assert not p.is_symlink()
        assert format(stat.S_IMODE(p.stat().st_mode),'04o')==row['mode']
        if row['type']=='directory':
            assert set(row)=={'path','type','mode'} and p.is_dir()
        else:
            assert set(row)=={'path','type','mode','bytes','sha256'} and p.is_file()
            data=p.read_bytes()
            assert len(data)==row['bytes'] and sha(data)==row['sha256']
    return {'closed_utc':seal['closed_utc'], 'files':sum(r['type']=='file' for r in entries),
            'directories':sum(r['type']=='directory' for r in entries),
            'manifest_sha256':seal['manifest_sha256']}

parser=argparse.ArgumentParser()
parser.add_argument('--draft',action='store_true',help='Check current raw receipts before final closure, with no writes.')
args=parser.parse_args()
result={'status':'PASS','receipt_consistency':check_receipts()}
if args.draft:
    result['closure']='not yet sealed; no final closure claim'
else:
    result['closure']=check_closure()
print(json.dumps(result,indent=2,sort_keys=True))
