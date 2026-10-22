#!/usr/bin/env python3
"""Offline read-only integrity and independent-diagnostic checker.

This checks an audit snapshot. It performs no network access, author-program
execution, file writes, source-proof certification, or provider action.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from finite_controls import controls

ROOT = Path(__file__).resolve().parent
CRITICAL = {
    'ANALYTIC_INPUT_REPAIR.md':'79f263395ce93f11c9b80902bc3c718463af92b6440416631b0f6e8e54f013ac',
    'PR1049_JENSEN_STEP_REPAIR.md':'6f3e0dbc1b2f01533f08ea8fe1d6af5bfa8fc5992e0a74cba70e654ce78978c6',
    'prior_SEALED_MANIFEST.json':'f661ea18e22af3c081f6cce90a35471039616efe1688d11d29dfaaa81c4f00bd'
}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def validate(data):
    errors=[]
    for item in data.get('files',[]):
        p=ROOT/item['path']
        if not p.is_file() or p.stat().st_size != item['bytes'] or sha(p) != item['sha256']:
            errors.append('local integrity: '+item['path'])
        if item['path'].startswith('private_sources/') and item.get('private_source') is not True:
            errors.append('missing private flag: '+item['path'])
    for item in data.get('external_inputs',[]):
        p=Path(item['path'])
        if not p.is_file() or p.stat().st_size != item['bytes'] or sha(p) != item['sha256']:
            errors.append('external input integrity: '+item['name'])
        if not isinstance(item.get('private_source'),bool):
            errors.append('missing explicit input privacy: '+item['name'])
    mapped={i['name']:i['sha256'] for i in data.get('external_inputs',[])}
    for name,expected in CRITICAL.items():
        if mapped.get(name) != expected: errors.append('critical input pin: '+name)
    return errors

def main():
    manifest_path=ROOT/'SEALED_MANIFEST.json'
    data=json.loads(manifest_path.read_text())
    seal=json.loads((ROOT/'AUDIT_SEAL.json').read_text())
    assert sha(manifest_path)==seal['manifest_sha256'], 'manifest seal mismatch'
    errors=validate(data)
    assert not errors, errors
    # In-memory corruption controls do not modify even temporary files.
    bad=copy.deepcopy(data);bad['files'][0]['bytes']+=1
    assert validate(bad), 'size corruption not caught'
    bad=copy.deepcopy(data);bad['external_inputs'][0]['sha256']='0'*64
    assert validate(bad), 'source corruption not caught'
    bad=copy.deepcopy(data)
    for item in bad['files']:
        if item['path'].startswith('private_sources/'):
            item['private_source']=False;break
    assert validate(bad), 'private flag corruption not caught'
    bad=copy.deepcopy(data)
    bad['external_inputs']=[i for i in bad['external_inputs'] if i['name']!='ANALYTIC_INPUT_REPAIR.md']
    assert validate(bad), 'critical input omission not caught'

    fresh=json.loads((ROOT/'FRESH_LEDGER_CHECK.json').read_text())
    raw=json.loads((ROOT/fresh['raw_private_path']).read_text())
    assert fresh['numeric_gid']==1254632077 and fresh['grid_columns']==43
    assert raw['range'].startswith("'Math Puzzles'!A1:AQ")
    assert len(raw['values'])==fresh['returned_rows']
    assert all(len(row)<=43 for row in raw['values'])
    assert not any(fresh['target_alias_hits'].values())
    # Dynamic size: 191 is not a hard-coded concurrency/append lock.
    assert fresh['returned_rows']>=2 and fresh['append_or_update_performed'] is False
    live=json.loads((ROOT/'LIVE_PR_CHECK.json').read_text())
    assert live['head']=='810d5bced8059fb0324c3d7d43b8e1d5f29449fa'
    assert len(live['comparisons'])==8 and all(i['equal'] for i in live['comparisons'])
    assert live['body_matches_pinned_utf8'] is True
    independent=controls()
    assert independent==json.loads((ROOT/'FINITE_CONTROL_RESULTS.json').read_text())
    disposition=json.loads((ROOT/'DISPOSITION.json').read_text())
    assert disposition['combined_mathematical_disposition']=='PASS_NO_REMAINING_MATERIAL_OBJECTION'
    assert disposition['analytic_input_assumed'] is False
    assert disposition['journal_pdf_compared'] is False
    assert disposition['provider_writes_performed'] is False
    assert disposition['overall_research_goal_completion_percent']==79
    print(json.dumps({'pass':True,'manifest_sha256':seal['manifest_sha256'],
        'local_files_verified':len(data['files']),
        'external_inputs_verified':len(data['external_inputs']),
        'independent_finite_controls_pass':True,
        'in_memory_corruption_controls_pass':True,
        'ledger_snapshot_rows':fresh['returned_rows'],
        'not_a_live_ledger_lock':True,'mathematical_proof_certification':False,
        'network_access':False,'author_program_executed':False,
        'writes_performed':False},indent=2,sort_keys=True))

if __name__=='__main__': main()
