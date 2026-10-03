"""Read-only actual-object gate; all writes stay in this audit's ignored tmp/.

Source and proof validity was sealed before this integration gate. This program
binds that reviewed packet to exact objects, bytes, full streams and live API.
It does not assert mathematical universality from the finite programs.
"""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

P = Path(__file__).resolve().parent
B = P.parent
REPO = Path('/Users/alec/Documents/Math')
HEAD = 'a7a6729d544f53b2be20b0e648f4001771bc2f42'
BASE = 'a3cfbf7795fc8687f6029e9d00b3ec0a201934f0'
OLD = '75bea4d3be9904e90c3843892671a440ba4d2c42'
TREE = '53fb00b380e106282d993968596c8ff4959ebc9e'
PRIOR = '4600b719b1a8c58498acb35d82a52267e52285d8'
TARGET = 'unsolved_math_prioritization/attempts/30002200/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
PRIVATE_PY = '/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
EMPTY = hashlib.sha256(b'').hexdigest()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(args, cwd=REPO, stem=None, success=True):
    r = subprocess.run(args, capture_output=True, cwd=cwd)
    if stem:
        (P / (stem + '.stdout')).write_bytes(r.stdout)
        (P / (stem + '.stderr')).write_bytes(r.stderr)
    if success:
        assert r.returncode == 0, (args, r.returncode, r.stderr.decode())
        assert not r.stderr, (args, r.stderr.decode())
    return r


def git(*args):
    return run(['git', *args]).stdout


def verify_entry(data, entry):
    assert len(data) == entry.get('bytes', len(data))
    assert digest(data) == entry['sha256']


assert git('rev-parse', 'main').decode().strip() == BASE
commit = run(['git', 'cat-file', '-p', HEAD], stem='final_git_commit').stdout
header = commit.split(b'\n\n', 1)[0].splitlines()
assert [x[7:].decode() for x in header if x.startswith(b'parent ')] == [OLD, BASE]
assert [x[5:].decode() for x in header if x.startswith(b'tree ')] == [TREE]
assert git('merge-base', '--is-ancestor', PRIOR, BASE) == b''
assert git('merge-base', '--is-ancestor', BASE, HEAD) == b''
assert git('merge-base', '--is-ancestor', OLD, HEAD) == b''

manifest = json.loads((B / 'scope_repaired_snapshot_manifest.json').read_text())
assert (manifest['head'], manifest['base'], manifest['original_frozen_head']) == (HEAD, BASE, OLD)
entries = manifest['files']
assert len(entries) == 26 and len({e['path'] for e in entries}) == 26
diff = run(['git', 'diff', '--name-status', BASE, HEAD], stem='final_git_diff_names').stdout
changed = [line.split(b'\t', 1)[1].decode() for line in diff.splitlines()]
assert set(changed) == {e['path'] for e in entries}
assert all(line.split(b'\t')[0] in (b'A', b'M') for line in diff.splitlines())
copy = P / 'tmp/final_git_packet'
copy.mkdir(parents=True, exist_ok=True)
prep = json.loads((B / 'scope_repair_preparation_receipt.json').read_text())
prep_by_path = {e['path']: e for e in prep['files']}
object_receipts = []
for e in entries:
    data = git('show', HEAD + ':' + e['path'])
    verify_entry(data, e)
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert blob == e['git_blob_sha']
    assert data == (B / 'scope_repaired_snapshot' / e['path']).read_bytes()
    if e['path'].startswith(TARGET):
        relative = e['path'][len(TARGET):]
        verify_entry(data, prep_by_path[relative])
        assert data == (B / 'tmp/scope_repaired_packet' / relative).read_bytes()
        dest = copy / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    else:
        assert e['path'] == QUEUE
    object_receipts.append(dict(e))
tree_files = git('ls-tree', '-r', '--name-only', HEAD, TARGET).decode().splitlines()
assert set(tree_files) == {TARGET + x for x in prep_by_path}
assert len(tree_files) == 25

old_manifest = json.loads((B / 'snapshot_manifest.json').read_text())
assert old_manifest['head'] == OLD and len(old_manifest['files']) == 20
for e in old_manifest['files']:
    data = git('show', OLD + ':' + e['path'])
    verify_entry(data, e)
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == e['git_blob_sha']
    assert data == (B / 'snapshot' / e['path']).read_bytes()
historical = []
modified_old = []
for e in old_manifest['files']:
    if e['path'].startswith(TARGET):
        if git('show', OLD + ':' + e['path']) == git('show', HEAD + ':' + e['path']):
            historical.append(e['path'][len(TARGET):])
        else:
            modified_old.append(e['path'][len(TARGET):])
assert len(historical) == 16
assert sorted(modified_old) == sorted(prep['only_changed_prior_paths'])
assert len(prep['six_new_correction_files']) == 6
assert set(tree_files) - {e['path'] for e in old_manifest['files']} == {TARGET+x for x in prep['six_new_correction_files']}

before = git('show', BASE + ':' + QUEUE)
after = git('show', HEAD + ':' + QUEUE)
before_lines, after_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
assert len(before_lines) == len(after_lines)
altered = [i for i, (x, y) in enumerate(zip(before_lines, after_lines)) if x != y]
assert altered == [415]
old_row, new_row = before_lines[415], after_lines[415]
assert b'30002200' in old_row and b'30002200' in new_row
old_cells, new_cells = old_row.split(b'|'), new_row.split(b'|')
assert len(old_cells) == len(new_cells)
changed_cells = [i for i, (x, y) in enumerate(zip(old_cells, new_cells)) if x != y]
assert changed_cells == [8]
assert old_cells[8].strip() == b'queued' and new_cells[8].strip() == b'already_solved'
assert old_cells[1].strip() == new_cells[1].strip() == b'405'
assert any(x.strip() == b'0/5' for x in old_cells)
replacement = old_cells[8].replace(b'queued', b'already_solved')
assert new_cells[8] == replacement
expected = b''.join(before_lines[:415]) + b'|'.join(old_cells[:8] + [replacement] + old_cells[9:]) + b''.join(before_lines[416:])
assert after == expected
run(['git', 'diff', '--no-ext-diff', '--unified=0', BASE, HEAD, '--', QUEUE], stem='final_queue_diff')

nested = []
for name in ['FINAL_SOURCE_MANIFEST.json', 'review/REVIEW_MANIFEST.json', 'CURRENT_SCOPE_MANIFEST.json', 'PUBLICATION_MANIFEST.json']:
    obj = json.loads((copy / name).read_text())
    for e in obj['files']:
        location = copy / ('review/' if name == 'review/REVIEW_MANIFEST.json' else '') / e['path']
        verify_entry(location.read_bytes(), e)
    if name == 'review/REVIEW_MANIFEST.json':
        assert obj['author_manifest_sha256'] == digest((copy / 'FINAL_SOURCE_MANIFEST.json').read_bytes())
    if name == 'CURRENT_SCOPE_MANIFEST.json':
        for e in obj['superseded_historical_claims']:
            verify_entry((copy / e['path']).read_bytes(), e)
        assert obj['author_turns'] == 0 and obj['status'] == 'already_solved'
    nested.append({'path': name, 'bindings': len(obj['files']), 'sha256': digest((copy / name).read_bytes())})
assert len(json.loads((copy / 'PUBLICATION_MANIFEST.json').read_text())['files']) == 24
sources = json.loads((copy / 'SOURCE_MANIFEST.json').read_text())['sources']
own_sources = json.loads((P / 'private_source_evidence_manifest.json').read_text())['files']
for e in own_sources:
    verify_entry((P / e['private_path']).read_bytes(), e)
source_by_url = {e['source_url']: e for e in own_sources if 'source_url' in e}
for e in sources:
    private = source_by_url[e['url']]
    assert (e['bytes'], e['sha256']) == (private['bytes'], private['sha256'])
    verify_entry((P / private['private_path']).read_bytes(), e)

seal_hashes = {'independent_pre_candidate_seal.json': 'e790d02cdab68fccac8b6cf94095e7ed446fdf28967fdc1d95e43df011fa852b', 'mathematical_verdict_seal.json': '0667f6e1f64c96efbf168ca8af7e4c893d981a75f53afcb08409a11e5de4968c'}
seal_instances = 0
for name, value in seal_hashes.items():
    assert digest((P / name).read_bytes()) == value
    obj = json.loads((P / name).read_text())
    for e in obj['files']:
        verify_entry((P / e['path']).read_bytes(), e)
        seal_instances += 1
erratum = (P / 'OWN_AUDIT_ERRATUM.md').read_bytes()
assert b'2b-2' in erratum and b'coincide for b1' in erratum
assert digest(erratum) == '2a2a1368e00082aaa212e3d24147a6f07bcbfa7ae2c44e607bf648f91019f752'

old_runs = json.loads((P / 'packet_reproduction.json').read_text())['runs']
replays = []
for script, old in [(x['script'], x) for x in old_runs]:
    stem = 'final_' + script.replace('/', '_').removesuffix('.py')
    r = run([PRIVATE_PY, '-B', str(copy / script)], cwd=copy, stem=stem)
    assert len(r.stdout) == old['stdout_bytes'] and digest(r.stdout) == old['stdout_sha256']
    assert not r.stderr
    replays.append({'script': script, 'exit': r.returncode, 'stdout_bytes': len(r.stdout), 'stdout_sha256': digest(r.stdout), 'stderr_bytes': 0, 'stderr_sha256': EMPTY})
wrapper = json.loads((P / 'final_verify_publication.stdout').read_bytes())
assert wrapper['current_ext_free_targets'] == [0, 3] and wrapper['current_ext_target_minus_quotient'] == [-9, -6]
assert wrapper['scope_correction_globally_bound'] and wrapper['old_assertions_historical_only']
assert wrapper['source_pdfs_reverified'] is False

prior_api = run(['gh', 'pr', 'view', '378', '--json', 'number,url,state,mergeCommit,mergedAt,headRefOid,baseRefName'], stem='final_prior378_api')
prior = json.loads(prior_api.stdout)
assert prior['state'] == 'MERGED' and prior['mergeCommit']['oid'] == PRIOR
api_run = run(['gh', 'pr', 'view', '377', '--json', 'number,url,state,isDraft,title,body,headRefName,headRefOid,baseRefName,baseRefOid,files,updatedAt'], stem='final_api_current')
api = json.loads(api_run.stdout)
assert api['headRefOid'] == HEAD and api['baseRefOid'] == BASE and api['baseRefName'] == 'main'
assert api['state'] == 'OPEN' and api['isDraft']
assert api['number'] == 377 and api['url'] == 'https://github.com/AlecKriebel/Math/pull/377'
assert {x['path'] for x in api['files']} == set(changed)
api_commit_run = run(['gh', 'api', 'repos/AlecKriebel/Math/git/commits/' + HEAD], stem='final_api_git_commit')
api_commit = json.loads(api_commit_run.stdout)
assert api_commit['sha'] == HEAD and api_commit['tree']['sha'] == TREE
assert [x['sha'] for x in api_commit['parents']] == [OLD, BASE]
remote_run = run(['git', 'ls-remote', '--refs', 'origin', 'refs/heads/main', 'refs/heads/' + api['headRefName']], stem='final_remote_refs')
remote_refs = dict((x.split()[1].decode(), x.split()[0].decode()) for x in remote_run.stdout.splitlines())
assert remote_refs == {'refs/heads/main': BASE, 'refs/heads/' + api['headRefName']: HEAD}
body = api['body']
stale_parent = 'preserves WIP 5ba83eccde1e5a5655d199fc3abb47a277f82b31 as its second parent' in body
current_disclosure = all(x in body for x in ['CURRENT_SCOPE_CORRECTION', 'Ext', 'AI', '0/5'])
metadata_gaps = []
if stale_parent:
    metadata_gaps.append('PR body falsely describes WIP 5ba83 as actual second parent')
if 'three additive wrappers' in body:
    metadata_gaps.append('PR body still describes superseded wrapper scope')
if not current_disclosure:
    metadata_gaps.append('PR body needs explicit current Ext correction and AI/0-of-5 disclosures')
assert git('rev-parse', 'main').decode().strip() == BASE

receipt = {'started_utc': started, 'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'head': HEAD, 'base': BASE, 'tree': TREE, 'parents': [OLD, BASE], 'prior378_merge': PRIOR, 'main_held_fixed': True, 'object_files': object_receipts, 'all26_actual_blob_bindings_verified': True, 'all25_reviewed_packet_bytes_exact': True, 'all20_original_git_objects_unchanged': True, 'historical16_unchanged': historical, 'three_modified_prior_paths': modified_old, 'six_additive_correction_paths': prep['six_new_correction_files'], 'diff_exact26_paths': True, 'queue': {'physical_line': 416, 'rank': 405, 'changed_cell_index': 8, 'before': old_row.decode().rstrip('\n'), 'after': new_row.decode().rstrip('\n'), 'base_sha256': digest(before), 'head_sha256': digest(after), 'only_status_token_changed': True, 'author_turns': '0/5'}, 'nested_manifests': nested, 'actual_primary_pdf_bindings': len(sources), 'owned_private_source_bindings': len(own_sources), 'original_seal_binding_instances': seal_instances, 'original_seals': seal_hashes, 'authoritative_own_erratum_sha256': digest(erratum), 'replays': replays, 'api_exact_head_base_files_verified': True, 'prior378_merged_api_verified': True, 'api_body_sha256': digest(body.encode()), 'metadata_gaps': metadata_gaps, 'status': 'PASS_FINAL_ACTUAL_HEAD_GATE' if not metadata_gaps else 'OBJECT_QUEUE_RUNTIME_PASS_METADATA_REPAIR_REQUIRED', 'completion_percent': 100 if not metadata_gaps else 97, 'no_candidate_git_index_remote_service_writes': True}
receipt['api_exact_commit_tree_parents_verified'] = True
receipt['live_remote_refs'] = remote_refs
(P / 'final_actual_head_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
