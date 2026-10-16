#!/usr/bin/env python3
"""Generate an additive metadata adaptation from the immutable original gate.

Every replacement is literal and count-checked. Scope, source, body, queue,
all-host disposition, API and whole-tree guards are retained. Extra checks bind
the first refresh and the new normal merge. This never edits the original gate.
"""
import ast
import difflib
import hashlib
import json
import pathlib

HERE = pathlib.Path(__file__).parent
ORIGINAL = HERE.parent / 'controls' / 'final_gate.py'
ORIGINAL_SHA = '2b613efcc4d41616277c7fd259d1357dbcc69e0aeb4d330efb9618167442a2de'
PRIOR_HASHES = {
    'snapshot_manifest.json': '989de56033f3d980c2a1f8f79829ebab74f57580af2e283a73b9462deb244612',
    'repaired_snapshot_manifest.json': '3c10ad4c9cd3f636494a8234edbf0d05d4ffde967bfc4bbaabc6b9583580d8d3',
    'queue_repair_receipt.json': 'b40773493c5ae91047af8e942dc3d5ed47904a59cbc8b380ba6ee94452cdfb55',
    'accepted_pr_body.txt': '662fbbeac83e2709a4374f540da4eebf137f5ef4240f1cb820b23814d1cb6b0f',
    'merge_body.txt': 'd05c7698cd384c8fc7f1431b420e9d871e2e6552277fd2a3066c5f497f7c0771',
}
NEW_HASHES = {
    'snapshot_manifest.json': PRIOR_HASHES['snapshot_manifest.json'],
    'repaired_snapshot_manifest.json': 'e155b73d64556bf991513c4247af3e90d4631ea3085481cfe3d910529ccae42e',
    'queue_repair_receipt.json': '04523b4c9e55c83a5901d29b2a0c4c6b3dba21e8b5970ce06820398d98e3d5ea',
    'accepted_pr_body.txt': '0933d8a02e24cc2c441134fbf077108805537fe7370ce2b49a84e0b3a094a6ed',
    'merge_body.txt': PRIOR_HASHES['merge_body.txt'],
}

def main():
    raw = ORIGINAL.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == ORIGINAL_SHA
    original = raw.decode()
    code = original
    replacements = []
    def replace(old, new, count=1):
        nonlocal code
        assert code.count(old) == count, (old, code.count(old), count)
        code = code.replace(old, new)
        replacements.append({'old': old, 'new': new, 'occurrences': count})
    replace("HEAD='26df33899c95d860403ab311c568e0328bc87eeb'", "HEAD='4afe89d1439e0d0d2a28a55f27709192cd56738e'\nPRIOR_HEAD='26df33899c95d860403ab311c568e0328bc87eeb'\nPRIOR_PARENT='ceada39994b1cd2c4935709143b53e2f7a581a45'\nPRIOR_TREE='7d3b187011047ab8944dc2fdb8bf940c2110ce2c'")
    replace("PARENT='ceada39994b1cd2c4935709143b53e2f7a581a45'\nTREE=", "PARENT='8e04757bff6e5c6c25d2dbf23ce10f736da8c5c8'\nTREE=")
    replace("TREE='7d3b187011047ab8944dc2fdb8bf940c2110ce2c'\nPREFIX=", "TREE='9b4c96e230fc3aecca24760e6804ea671d559ca4'\nPREFIX=")
    replace("PREPARED_SHA='662fbbeac83e2709a4374f540da4eebf137f5ef4240f1cb820b23814d1cb6b0f'", "PREPARED_SHA='0933d8a02e24cc2c441134fbf077108805537fe7370ce2b49a84e0b3a094a6ed'\nPRIOR_INPUT_HASHES=" + repr(PRIOR_HASHES) + "\nNEW_INPUT_HASHES=" + repr(NEW_HASHES))
    replace("parser.add_argument('--source-dir',required=True)", "parser.add_argument('--source-dir',required=True)\n    parser.add_argument('--prior-inputs',required=True)")
    replace("    original_manifest=json.loads", "    prior_inputs=pathlib.Path(args.prior_inputs)\n    for name,digest in PRIOR_INPUT_HASHES.items():assert sha((prior_inputs/name).read_bytes())==digest\n    for name,digest in NEW_INPUT_HASHES.items():assert sha((inputs/name).read_bytes())==digest\n    prior_manifest=json.loads((prior_inputs/'repaired_snapshot_manifest.json').read_bytes())\n    prior_repair=json.loads((prior_inputs/'queue_repair_receipt.json').read_bytes())\n    assert prior_manifest['head']==PRIOR_HEAD and prior_manifest['base']==PRIOR_PARENT\n    assert prior_repair['parents']==[ORIGINAL,PRIOR_PARENT] and prior_repair['tree']==PRIOR_TREE\n    original_manifest=json.loads")
    replace("repair['parents']==[ORIGINAL,PARENT]", "repair['parents']==[PRIOR_HEAD,PARENT]")
    replace("    blob_expectations={}", "    prior_tree=treemap(PRIOR_HEAD,'prior_refreshed_tree')\n    assert canonical_tree_sha(prior_tree)==PRIOR_TREE\n    assert {p for p in prior_tree if p.startswith(PREFIX+'/')}==targetpaths\n    assert set(git('prior_refreshed_changed_paths','diff','--name-only',PRIOR_PARENT,PRIOR_HEAD).decode().splitlines())==set(newrows)\n    prior_rows={f['path']:f for f in prior_manifest['files']}\n    assert len(prior_rows)==46 and set(prior_rows)==set(newrows)\n    # A normal merge must carry the entire current-main parent unchanged outside the reviewed scope.\n    parent_tree=treemap(PARENT,'normal_refresh_parent_complete_tree')\n    normal_expected=dict(parent_tree)\n    for path in targetpaths|{QUEUE}:normal_expected[path]=prior_tree[path]\n    assert normal_expected==refreshed_tree and canonical_tree_sha(normal_expected)==TREE\n    blob_expectations={}")
    replace("        if path in targetpaths:assert frozen==updated", "        prior_frozen=(prior_inputs/'repaired_snapshot'/path).read_bytes();h=prior_rows[path]\n        assert (len(prior_frozen),sha(prior_frozen),blobsha(prior_frozen))==(h['bytes'],h['sha256'],prior_tree[path][1])\n        assert prior_frozen==updated and getblob(PRIOR_HEAD,path)==prior_frozen\n        assert prior_tree[path]==refreshed_tree[path]\n        if path in targetpaths:\n            assert frozen==updated and original_tree[path]==refreshed_tree[path]")
    replace("    queue_refreshed=queue_delta(PARENT,HEAD,'refreshed')", "    queue_prior=queue_delta(PRIOR_PARENT,PRIOR_HEAD,'first_refresh')\n    assert queue_prior['old_row']==prior_repair['old_row'] and queue_prior['new_row']==prior_repair['new_row']\n    queue_refreshed=queue_delta(PARENT,HEAD,'refreshed')")
    replace("    assert HEAD in text and ORIGINAL in text and WIP in text and PARENT in text", "    assert HEAD in text and ORIGINAL in text and WIP in text and PARENT in text\n    assert PRIOR_HEAD in text and PRIOR_PARENT in text and TREE in text\n    prior_body=(prior_inputs/'accepted_pr_body.txt').read_bytes()\n    prior_text=prior_body.decode();assert 'unsolved, 5/5' in prior_text and 'None supplies the missing all-host comparison' in prior_text and 'No novelty certification' in prior_text\n    assert PRIOR_HEAD in prior_text and ORIGINAL in prior_text and WIP in prior_text and PRIOR_PARENT in prior_text")
    replace("check_commit(HEAD,[ORIGINAL,PARENT],TREE),check_commit(PARENT)", "check_commit(PRIOR_HEAD,[ORIGINAL,PRIOR_PARENT],PRIOR_TREE),check_commit(PRIOR_PARENT),check_commit(HEAD,[PRIOR_HEAD,PARENT],TREE),check_commit(PARENT)")
    replace("'original_head':ORIGINAL,'original_base':ORIGINAL_BASE", "'original_head':ORIGINAL,'previous_reviewed_head':PRIOR_HEAD,'previous_refreshed_parent':PRIOR_PARENT,'previous_refreshed_tree':PRIOR_TREE,'normal_refresh_every_other_parent_path_preserved':True,'original_base':ORIGINAL_BASE")
    replace("'queue_original':queue_original,'queue_refreshed':queue_refreshed", "'queue_original':queue_original,'queue_first_refresh':queue_prior,'queue_refreshed':queue_refreshed")
    replace("'commits':commits", "'prior_input_metadata_sha256':{name:sha((prior_inputs/name).read_bytes()) for name in PRIOR_INPUT_HASHES},'immutable_original_gate_sha256':'" + ORIGINAL_SHA + "','commits':commits")
    ast.parse(code)
    output = HERE / 'final_gate_refreshed.py'
    output.write_text(code)
    diff = ''.join(difflib.unified_diff(original.splitlines(keepends=True), code.splitlines(keepends=True),
                                      fromfile='immutable/public/controls/final_gate.py',
                                      tofile='additive/public/live_acceptance/final_gate_refreshed.py'))
    (HERE / 'final_gate_metadata_adaptation.diff').write_text(diff)
    receipt = {'immutable_original_gate_sha256': ORIGINAL_SHA,
               'adapted_gate_sha256': hashlib.sha256(code.encode()).hexdigest(),
               'full_diff_sha256': hashlib.sha256(diff.encode()).hexdigest(),
               'literal_replacements': replacements,
               'prior_inputs_exactly_bound': PRIOR_HASHES, 'new_inputs_exactly_bound': NEW_HASHES,
               'all_previous_scope_source_queue_body_API_merge_checks_retained': True,
               'added_prior_object_packet_body_and_whole_parent_map_checks': True,
               'original_gate_not_modified': True, 'metadata_adaptation_only': True}
    (HERE / 'gate_adaptation_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'adapted_gate_sha256': receipt['adapted_gate_sha256'],
                      'immutable_original_gate_sha256': ORIGINAL_SHA,
                      'replacement_count': len(replacements)}, sort_keys=True))

if __name__ == '__main__':
    main()
