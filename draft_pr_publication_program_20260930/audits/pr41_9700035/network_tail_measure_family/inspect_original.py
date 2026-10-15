#!/usr/bin/env python3
"""Read every frozen original byte and JSON leaf, without importing helpers."""
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SHA = lambda b: hashlib.sha256(b).hexdigest()


def parse(data):
    def pairs(items):
        value = {}
        for key, item in items:
            assert key not in value, 'Duplicate JSON key'
            value[key] = item
        return value
    return json.loads(data, object_pairs_hook=pairs)


manifest_raw = (AUDIT/'snapshot_manifest.json').read_bytes()
assert SHA(manifest_raw) == 'feef9bf6433c165296d3cdea883ceb74440048e17ff87f03ef636a99338cb3e6'
manifest = parse(manifest_raw)
assert manifest['head'] == '292b95ca601f166e6d246e609cf7ed5ca5653e25'
assert len(manifest['files']) == 16 and len(manifest['changed_paths']) == 17
raw_files, json_files, rows = {}, {}, []
for pin in manifest['files']:
    path = AUDIT/'source_snapshot'/pin['path']
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == pin['size'] and SHA(raw) == pin['sha256']
    raw_files[pin['path']] = raw
    row = dict(pin, whole_bytes_read=True, line_count=len(raw.splitlines()))
    if path.suffix == '.json':
        value = parse(raw)
        json_files[pin['path']] = value
        # Retain the entire interpreted JSON, including every diagnostic name
        # and value, rather than a summary selected from its first/last lines.
        row['whole_parsed_JSON'] = value
    rows.append(row)

for name, total in [('verification.json',211),('review/independent_results.json',3809)]:
    result = json_files[name]
    assert type(result['passed']) is int and result['passed'] == total
    assert type(result['failed']) is int and result['failed'] == 0
    assert len(result['checks']) == total
    assert all(type(k) is str and k and type(v) is str and v == 'PASS' for k,v in result['checks'].items())

assert [x['turn'] for x in json_files['turns.json']] == [1,2]
attempt = json_files['attempt.json']
assert type(attempt['substantive_attempts_used']) is int and attempt['substantive_attempts_used'] == 2
assert type(attempt['substantive_attempt_limit']) is int and attempt['substantive_attempt_limit'] == 5
assert attempt['status'] == 'unsolved_partial_conditional' and attempt['full_original_resolution_claimed'] is False
assert attempt['proof_sha256'] == SHA(raw_files['PROOF.md'])
assert json_files['verification.json']['proof_sha256'] == attempt['proof_sha256']
assert json_files['review/review_summary.json']['final_reviewed_artifact_sha256'] == attempt['proof_sha256']

diff = (AUDIT/'pr_input/diff.patch').read_bytes()
blocks = re.split(rb'(?m)(?=^diff --git )', diff)
blocks = [b for b in blocks if b]
assert len(blocks) == 17
diff_rows = []
for block in blocks:
    lines = block.splitlines(keepends=True)
    first = lines[0].decode().strip()
    left, right = first[len('diff --git '):].split(' ')
    assert left[2:] == right[2:]
    name = right[2:]
    assert name in manifest['changed_paths']
    if name.endswith('/QUEUE.md'):
        removed = [x[1:].decode().rstrip('\n') for x in lines if x.startswith(b'-') and not x.startswith(b'---')]
        added = [x[1:].decode().rstrip('\n') for x in lines if x.startswith(b'+') and not x.startswith(b'+++')]
        assert len(removed) == len(added) == 1
        before, after = [x.strip() for x in removed[0].split('|')[1:-1]], [x.strip() for x in added[0].split('|')[1:-1]]
        assert len(before) == len(after) == 12
        assert before[1] == after[1] == '9700035 / AMR-096-0035'
        assert [(i,b,a) for i,(b,a) in enumerate(zip(before,after)) if b!=a] == [(7,'queued','unsolved'),(8,'0/5','2/5'),(10,before[10],after[10])]
        diff_rows.append({'path':name,'whole_diff_block_bytes':len(block),'sha256':SHA(block),'removed_complete_row':removed[0],'added_complete_row':added[0]})
    else:
        local = name[len(manifest['prefix']):]
        assert b'new file mode 100644\n' in lines and b'--- /dev/null\n' in lines
        reconstructed = b''.join(x[1:] for x in lines if x.startswith(b'+') and not x.startswith(b'+++'))
        assert reconstructed == raw_files[local], 'Whole added diff bytes differ'
        hunks = [x for x in lines if x.startswith(b'@@')]
        assert len(hunks) == 1
        assert hunks[0].startswith(('@'+ '@ -0,0 +1,'+str(len(raw_files[local].splitlines()))+' @@').encode())
        diff_rows.append({'path':name,'whole_diff_block_bytes':len(block),'sha256':SHA(block),'whole_added_payload_equal_original':True})

receipt = {'status':'READONLY_ORIGINAL_COMPLETE_STRUCTURAL_INSPECTION','files':rows,'diff':{'bytes':len(diff),'sha256':SHA(diff),'lines':len(diff.splitlines()),'blocks':diff_rows},
           'original_local_budget':'2/5','saved_author_assertions':211,'saved_old_independent_assertions':3809,
           'saved_diagnostics_are_not_actual_replays':True,'reviewed_helpers_imported_or_executed':False,'new_substantive_attempts':0,'audit_turns':0}
(HERE/'ORIGINAL_READ_LEDGER.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in {'files','diff'}},indent=2))
print(json.dumps(receipt['diff'] | {'blocks':len(diff_rows)},indent=2))
