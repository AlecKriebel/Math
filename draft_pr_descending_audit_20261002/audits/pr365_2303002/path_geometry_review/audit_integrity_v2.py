#!/usr/bin/env python3
"""Read-only verification of all 19 frozen scope objects and whole outputs."""
import difflib, gzip, hashlib, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
A = ROOT.parent
S = A / 'snapshot'
TARGET = S / 'unsolved_math_prioritization' / 'attempts' / '2303002'
manifest = json.loads((A / 'snapshot_manifest.json').read_text())

def sha(data):
    return hashlib.sha256(data).hexdigest()

def stream(label, which='stdout'):
    return gzip.decompress((ROOT / 'captures' / (label + '.' + which + '.gz')).read_bytes())

def receipt(label):
    return json.loads((ROOT / 'captures' / (label + '.receipt.json')).read_text())

checks = []
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

check('frozen_head', manifest['head'] == '4245f1af53840a07f43c05c928c4783bc6c3a467')
check('frozen_base', manifest['base'] == 'efd29c05204703acca9a0860812f54b94fae54b1')
check('scope_count_19', len(manifest['files']) == 19)
tree = {}
for entry in stream('git_scoped_tree').split(b'\0'):
    if entry:
        mode_type_blob, path = entry.split(b'\t')
        mode, typ, blob = mode_type_blob.decode().split()
        tree[path.decode()] = {'mode': mode, 'type': typ, 'blob': blob}
check('tree_scope_exact', set(tree) == {f['path'] for f in manifest['files']})
scope = []
for item in manifest['files']:
    data = (S / item['path']).read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    check('bytes:' + item['path'], len(data) == item['bytes'])
    check('sha256:' + item['path'], sha(data) == item['sha256'])
    check('blob:' + item['path'], blob == item['git_blob_sha'] == tree[item['path']]['blob'])
    check('mode:' + item['path'], tree[item['path']]['mode'] == '100644' and tree[item['path']]['type'] == 'blob')
    scope.append(dict(item, git_mode=tree[item['path']]['mode']))

for name, count in [('FINAL_FROZEN_MANIFEST.json', 9), ('PUBLICATION_MANIFEST.json', 17)]:
    nested = json.loads((TARGET / name).read_text())
    check(name + ':count', len(nested['files']) == count)
    check(name + ':unique', len({f['path'] for f in nested['files']}) == count)
    for item in nested['files']:
        data = (TARGET / item['path']).read_bytes()
        check(name + ':bytes:' + item['path'], len(data) == item['bytes'])
        check(name + ':sha256:' + item['path'], sha(data) == item['sha256'])
review = json.loads((TARGET / 'final_review' / 'REVIEW_MANIFEST.json').read_text())
check('review_manifest_count', len(review) == 3)
for name, digest in review.items():
    check('review_hash:' + name, sha((TARGET / 'final_review' / name).read_bytes()) == digest)
publication = json.loads((TARGET / 'PUBLICATION_MANIFEST.json').read_text())
check('publication_author_binding', publication['author_manifest_sha256'] == sha((TARGET / 'FINAL_FROZEN_MANIFEST.json').read_bytes()))
check('publication_review_binding', publication['review_manifest_sha256'] == sha((TARGET / 'final_review' / 'REVIEW_MANIFEST.json').read_bytes()))
check('publication_covers_all18', {f['path'] for f in publication['files']} | {'PUBLICATION_MANIFEST.json'} == {str(p.relative_to(TARGET)) for p in TARGET.rglob('*') if p.is_file()})

for label in ['author_replay', 'portable_math_only', 'portable_full_sources', 'git_branch', 'git_scoped_tree', 'git_scoped_diff', 'git_target_history', 'git_target_all_local_history', 'git_base_queue', 'git_full_raw_diff', 'git_author_wip_tree', 'git_head_raw']:
    r = receipt(label)
    check('success:' + label, r['exit_code'] == 0 and not r['timed_out'])
    check('empty_stderr:' + label, stream(label, 'stderr') == b'')
check('whole_author_output', stream('author_replay') == (TARGET / 'SOURCE_CHECKS.json').read_bytes())
check('whole_full_source_output', stream('portable_full_sources') == (TARGET / 'final_review' / 'INDEPENDENT_CHECKS.json').read_bytes())
check('whole_math_only_output', stream('portable_math_only') == (TARGET / 'final_review' / 'INDEPENDENT_CHECKS.json').read_bytes().replace(b'1667', b'1665'))
check('main_branch', stream('git_branch') == b'main\n')
check('historical_verbatim_expected_fail', receipt('historical_verbatim')['exit_code'] == 1 and stream('historical_verbatim') == b'' and b"/workspace/shared/research_harmonicpath_2303002/checkpoint/FINAL_FROZEN_MANIFEST.json" in stream('historical_verbatim', 'stderr'))
for label in ['mutation_radial_sign', 'mutation_compact_cutoff', 'mutation_proof_binding', 'mutation_source_binding']:
    check('mutation_rejected:' + label, receipt(label)['exit_code'] == 1 and stream(label) == b'' and b'AssertionError' in stream(label, 'stderr'))

raw_lines = stream('git_full_raw_diff').decode().splitlines()
raw = {}
for line in raw_lines:
    fields, path = line.split('\t')
    old_mode, new_mode, old_sha, new_sha, status = fields[1:].split()
    raw[path] = {'old_mode': old_mode, 'new_mode': new_mode, 'old_blob': old_sha, 'new_blob': new_sha, 'status': status}
check('actual_diff_scope_exact19', set(raw) == set(tree))
for path, obj in raw.items():
    check('actual_diff_blob_mode:' + path, obj['new_mode'] == '100644' and obj['new_blob'] == tree[path]['blob'])
    check('actual_diff_status:' + path, obj['status'] == ('M' if path.endswith('/QUEUE.md') else 'A'))

queue_path = 'unsolved_math_prioritization/QUEUE.md'
before = stream('git_base_queue').decode().splitlines(keepends=True)
after = (S / queue_path).read_text().splitlines(keepends=True)
diff = list(difflib.unified_diff(before, after, fromfile='base/QUEUE.md', tofile='head/QUEUE.md'))
changes = [s for s in diff if s[:1] in ['+', '-'] and not s.startswith(('+++', '---'))]
check('queue_only_one_row', len(changes) == 2)
check('queue_target_2303002', all('| 2303002 / AMR-022-3002 |' in s for s in changes))
check('queue_zero_turns_preserved', all('| 0/5 |' in s for s in changes))
check('queue_only_status_cell', changes[1][1:] == changes[0][1:].replace('| queued |', '| already_solved |'))

author_tree = {}
for entry in stream('git_author_wip_tree').split(b'\0'):
    if entry:
        fields, path = entry.split(b'\t')
        author_tree[path.decode()] = fields.decode().split()
check('author_wip_count10', len(author_tree) == 10)
for path, fields in author_tree.items():
    check('author_wip_preserved:' + path, fields[0] == tree[path]['mode'] and fields[2] == tree[path]['blob'])
head_raw = stream('git_head_raw').decode()
check('base_parent_preserved', 'parent ' + manifest['base'] in head_raw)
check('author_wip_parent_preserved', 'parent a3ac55761d2301fbfe30e07a266da4a039cbfaba' in head_raw)

out = {'status': 'PASS', 'checks': checks, 'scope19': scope, 'actual_diff19': raw,
       'queue_complete_diff': ''.join(diff), 'author_wip_files_preserved': len(author_tree),
       'output_comparisons': 'complete bytes, including all stdout and stderr; counts alone were not used',
       'history_limit': 'explicit frozen head sees author WIP plus merge; --all current local refs returns no target-path history and is not a certification of inaccessible refs or deleted objects'}
print(json.dumps(out, indent=2, sort_keys=True))
