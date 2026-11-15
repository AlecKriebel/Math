#!/usr/bin/env python3
"""Read-only operational proof/custody closure; no network, Git or subprocess."""
from pathlib import Path
import hashlib
import json
import sys

A = Path(__file__).resolve().parent
SHA = 'addcb8c8a8afa895f3a1dc45bdae50ff9c536c14'
LEAF = 'docs/papers/strict-dirichlet-gap/index.html'
FILES = ['tree-root.json', 'tree-docs.json', 'tree-papers.json', 'tree-leaf.json']
CHILDREN = ['docs', 'papers', 'strict-dirichlet-gap', 'index.html']
TERMINAL = {'OWNED_MANIFEST.json', 'FINAL_CLOSURE.json', 'FINAL_SEAL.json'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def data(p):
    return json.loads(Path(p).read_text())


def native(p):
    x = data(p)
    need(x.get('isError') is not True, 'connector error')
    return json.loads(x['structuredContent']['content'])


def pinned(p):
    path = Path(p['path'])
    need(path.is_file() and not path.is_symlink(), 'nonregular pinned path')
    b = path.read_bytes()
    need(len(b) == p['bytes'] and hashlib.sha256(b).hexdigest() == p['SHA256'],
         'pinned bytes changed: ' + str(path))
    return b


def pins(x):
    if isinstance(x, dict):
        if all(k in x for k in ['path', 'bytes', 'SHA256']):
            pinned(x)
        else:
            for v in x.values():
                pins(v)
    elif isinstance(x, list):
        for v in x:
            pins(v)


def git_hash(kind, b):
    return hashlib.sha1(kind.encode() + b' ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def tree_hash(t):
    need(t['truncated'] is False, 'truncated tree')
    entries = t['tree']
    need(len(entries) == len({e['path'] for e in entries}), 'duplicate tree names')
    ordered = sorted(entries, key=lambda e: (e['path'] + ('/' if e['type'] == 'tree' else '')).encode())
    b = b''.join(str(int(e['mode'])).encode() + b' ' + e['path'].encode() + b'\0' +
                 bytes.fromhex(e['sha']) for e in ordered)
    return git_hash('tree', b)


def main():
    manifest = data(A / 'OWNED_MANIFEST.json')
    actual = {str(p) for p in A.rglob('*') if p.is_file() and p.name not in TERMINAL}
    expected = {p['path'] for p in manifest['files']}
    need(actual == expected and len(expected) == len(manifest['files']), 'exact owned membership')
    need(not any(p.is_symlink() for p in A.rglob('*')), 'unexpected symlink')
    pins(manifest['files'])
    pins(data(A / 'INPUT_MANIFEST.json'))
    before = data(A / 'PRESERVATION_BEFORE.json')
    for group in ['frozen_preparation_files', 'shared_local_Git_controls', 'local_legacy_assets']:
        pins(before[group])
    after = data(A / 'PRESERVATION_AFTER.json')
    need(all(after[k] is True for k in ['all_25_preparation_files_unchanged',
        'all_8_shared_local_Git_control_files_and_membership_unchanged',
        'all_10_local_legacy_asset_files_unchanged']), 'preservation record')

    plan = data(A / 'PLAN.json')
    old = [native(A / 'raw' / f) for f in FILES]
    new = [native(A / 'post-tree' / f) for f in FILES]
    for i, (o, n) in enumerate(zip(old, new)):
        need(tree_hash(o) == o['sha'] and tree_hash(n) == n['sha'], 'actual tree hash')
        need(n['sha'] == plan['ancestor_tree_changes'][i]['new_tree_SHA'], 'predicted post tree')
        for t in [o, n]:
            e = next(e for e in t['tree'] if e['path'] == CHILDREN[i])
            if i < 3:
                target = old[i + 1]['sha'] if t is o else new[i + 1]['sha']
            else:
                target = plan['required_old_blob_SHA'] if t is o else plan['candidate_blob_SHA']
            need(e['sha'] == target, 'actual ancestry')
        ot = [(e['path'], e['mode'], e['type'], e['sha']) for e in o['tree'] if e['path'] != CHILDREN[i]]
        nt = [(e['path'], e['mode'], e['type'], e['sha']) for e in n['tree'] if e['path'] != CHILDREN[i]]
        need(ot == nt, 'remote sibling changed')
    cmd = data(A / 'POST_TREE_VERIFICATION_COMMAND.json')
    need(cmd['result']['exit_code'] == 0 and json.loads(cmd['result']['output'])['actual_post_tree_checked'],
         'actual precommit four-tree command')

    commit = native(A / 'ACTUAL_NEW_COMMIT.json')
    need(commit['sha'] == SHA and commit['tree']['sha'] == new[0]['sha'], 'applied commit/root')
    need(len(commit['parents']) == 1 and commit['parents'][0]['sha'] == plan['parent_commit_SHA'], 'direct parent')
    compare = data(A / 'ACTUAL_SINGLE_FILE_COMPARE.json')['structuredContent']
    need(compare['status'] == 'ahead' and compare['ahead_by'] == compare['total_commits'] == 1 and
         compare['behind_by'] == 0 and len(compare['files']) == 1 and
         compare['files'][0]['filename'] == LEAF and compare['files'][0]['status'] == 'modified', 'single-file comparison')
    args = data(A / 'EXACT_MAIN_UPDATE_ARGS.json')
    need(args['sha'] == SHA and args['expected_sha'] == plan['parent_commit_SHA'] and
         args['force'] is False and args['branch_name'] == 'main', 'nonforced expected-parent guard')
    need(data(A / 'ACTUAL_MAIN_UPDATE.json')['structuredContent']['success'] is True, 'actual update result')
    need(native(A / 'MAIN_AFTER_UPDATE.json')['object']['sha'] == SHA, 'actual main readback')

    ledger = data(A / 'GITHUB_TOOL_LEDGER.json')['calls']
    writes = [c for c in ledger if c['mutating']]
    need([x['tool'] for x in writes] == ['mcp__codex_apps__github_create_tree',
         'mcp__codex_apps__github_create_commit', 'mcp__codex_apps__github_update_ref'], 'exact three authorized mutations')
    need(writes[0]['args'] == plan['create_tree_args'] and len(writes[0]['args']['tree_elements']) == 1,
         'actual one-element tree request')
    need(writes[1]['args'] == plan['create_commit_args_after_tree_verified'] and writes[2]['args'] == args,
         'actual commit/ref request arguments')
    gaps = [c for c in ledger if c['result_file'] is None]
    need(len(gaps) == 1 and not gaps[0]['mutating'] and 'persistence_failure' in gaps[0], 'receipt gap must remain explicit')
    for call in ledger:
        if call['result_file'] is not None:
            need(data(call['result_file']).get('isError') is not True, 'actual connector failure')
    for call in ledger:
        if '/post-tree/' in (call['result_file'] or ''):
            need(call['completed_UTC'] < writes[1]['started_UTC'], 'tree readback was not before commit')

    run = native(A / 'ACTUAL_PAGES_RUN.json')
    need(run['id'] == 43687211477 and run['head_sha'] == SHA and
         run['status'] == 'completed' and run['conclusion'] == 'success', 'actual Pages run')
    jobs = native(A / 'ACTUAL_PAGES_JOBS.json')
    need(jobs['total_count'] == len(jobs['jobs']) == 3 and
         all(j['head_sha'] == SHA and j['status'] == 'completed' and j['conclusion'] == 'success'
             for j in jobs['jobs']), 'actual Pages jobs')
    deliveries = data(A / 'http/AFTERBUILD1/ALL_DELIVERIES.json')
    records = deliveries['records']
    need({r['legacy_name'] for r in records} == {e['path'] for e in new[3]['tree']} and
         len(records) == 10, 'complete legacy leaf delivery set')
    final_sha256 = {}
    for record in records:
        for hop in record['hops']:
            b = pinned({'path': hop['body_path'], 'bytes': hop['bytes'], 'SHA256': hop['SHA256']})
            need(isinstance(hop['ordered_response_headers'], list) and git_hash('blob', b) == hop['git_blob_SHA'],
                 'whole HTTP body/headers')
        last = record['hops'][-1]
        expected_blob = next(e['sha'] for e in new[3]['tree'] if e['path'] == record['legacy_name'])
        need(last['HTTP_status'] == 200 and last['git_blob_SHA'] == expected_blob, 'delivered identity')
        final_sha256[record['legacy_name']] = last['SHA256']
    need(final_sha256['index.html'] == 'dedb9326ddf053603601dc22355b00c555ed1ec05a8767b6119bcec03455965c', 'approved live HTML')
    need(final_sha256['paper.pdf'] == 'ff07b62aa5905544ab62b6cb04b5aa6ca528ccc61f18221fb2a0aa8c1e54f7b9', 'native PDF SHA256')
    need(final_sha256['source-and-verification.zip'] == '1f5d4ebdae73a11313e304585379d32a7ab8ba63e53499203d40b75cb3cff337', 'native ZIP SHA256')
    need(final_sha256['SHA256SUMS.txt'] == '95a6fd5f144e308e09c198b05fc4aff4c0419c8f4cc7e82e79ddecf949ef6e7d', 'original checksum SHA256')
    need(data(A / 'HTTP_COMMAND_COMPLETE.json')['exit_code'] == 0, 'HTTP command exit')
    verdict = data(A / 'CUSTOM_VERDICT.json')
    need(verdict['browser_plain_arrival_verified_by_this_lane'] is False and
         verdict['browser_query_fragment_arrival_verified_by_this_lane'] is False and
         verdict['follow_up'] is None, 'browser/follow-up scope')
    if (A / 'FINAL_SEAL.json').exists():
        pins(data(A / 'FINAL_SEAL.json')['bindings'])
    return {'status': 'PASS_WITH_DISCLOSED_NONCRITICAL_RECEIPT_GAP', 'applied_commit': SHA,
            'actual_post_trees_checked': 4, 'exact_changed_paths': [LEAF],
            'authorized_mutations': 3, 'actual_Pages_run_success': 43687211477,
            'actual_successful_Pages_jobs': 3, 'whole_HTTP_200_exact_deliveries': 10,
            'noncritical_first_Pages_listing_body_gap': 1, 'publication_critical_receipt_gaps': 0,
            'shared_local_Git_controls_unchanged': 8, 'frozen_preparation_files_unchanged': 25,
            'owned_payloads_checked': len(manifest['files']), 'root_browser_arrivals_pending': True,
            'network_Git_subprocess_or_writes_performed': False}


if __name__ == '__main__':
    try:
        print(json.dumps(main(), indent=2))
    except (ValueError, KeyError, OSError, StopIteration, TypeError) as e:
        print(json.dumps({'status': 'FAIL', 'error': str(e)}))
        sys.exit(1)
