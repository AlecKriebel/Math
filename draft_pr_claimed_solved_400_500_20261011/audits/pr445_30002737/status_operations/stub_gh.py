#!/usr/bin/env python3
"""Offline fixed GitHub API surrogate. Every executed request is persisted privately."""
import base64
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.parse import unquote

statepath = Path(os.environ['PR445_STUB_STATE'])
state = json.loads(statepath.read_text())
args = sys.argv[1:]
if len(args) not in (4, 6) or args[:2] != ['api', '--method'] or (len(args) == 6 and args[4:] != ['--input', '-']):
    raise SystemExit('unexpected gh argv')
method, full = args[2:4]
prefix = 'repos/AlecKriebel/Math/'
if not full.startswith(prefix):
    raise SystemExit('repository scope escaped')
endpoint = full[len(prefix):]
body = json.loads(sys.stdin.read()) if len(args) == 6 else None
call = {'method': method, 'endpoint': endpoint, 'body': body}
state['calls'].append(call)
scenario = state['scenario']
HEAD = state['head']
BRANCH = 'research/diffraction-dynamical-30002737'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'

def hblob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def save():
    statepath.write_text(json.dumps(state, sort_keys=True))

def finish(obj=None, raw=None, code=0):
    save()
    if raw is not None:
        sys.stdout.write(raw)
    else:
        print(json.dumps(obj))
    if code:
        print('simulated lost response', file=sys.stderr)
    raise SystemExit(code)

def queue_before():
    data = Path(state['queue_fixture']).read_bytes()
    if scenario == 'changed_status':
        data = data.replace(state['original_row'].encode(), state['original_row'].replace('claimed_solved', 'already_solved').encode())
    if scenario == 'nonblank_doi':
        old = state['original_row']
        data = data.replace(old.encode(), (old[:-4] + ' https://doi.org/10.1/test |').encode())
    return data

def build_nodes(leaves, root_sha):
    hierarchy = {}
    for path, entry in leaves.items():
        current = hierarchy
        parts = path.split('/')
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = entry
    nodes = {}
    def visit(directory):
        entries = []
        for name, entry in sorted(directory.items()):
            if 'mode' in entry:
                entries.append({'path': name, **entry})
            else:
                entries.append({'path': name, 'mode': '040000', 'type': 'tree', 'sha': visit(entry)})
        digest = hashlib.sha1(json.dumps(entries, sort_keys=True).encode()).hexdigest()
        nodes[digest] = entries
        return digest
    calculated_root = visit(hierarchy)
    nodes[root_sha] = nodes[calculated_root]
    return nodes

if method == 'GET' and endpoint == 'pulls/445':
    count = sum(c['endpoint'] == endpoint for c in state['calls'])
    if scenario == 'changed_head_before_patch' and count == 2:
        state['ref'] = '9' * 40
    obj = {'number': 445, 'state': 'open', 'draft': True,
           'head': {'ref': BRANCH, 'sha': state['ref'], 'repo': {'full_name': 'AlecKriebel/Math'}},
           'base': {'ref': 'main', 'sha': '7' * 40, 'repo': {'full_name': 'AlecKriebel/Math'}}}
    if scenario == 'changed_head': obj['head']['sha'] = '9' * 40
    if scenario == 'changed_branch': obj['head']['ref'] = 'research/different'
    if scenario == 'closed_pr': obj['state'] = 'closed'
    if scenario == 'nondraft_pr': obj['draft'] = False
    if scenario == 'wrong_base': obj['base']['ref'] = 'elsewhere'
    if scenario == 'wrong_repo': obj['head']['repo']['full_name'] = 'Other/Math'
    if scenario == 'bool_pr_remote': obj['number'] = True
    if scenario == 'duplicate_api_keys': finish(raw='{"number":445,"number":445}')
    finish(obj)
if method == 'GET' and endpoint == 'git/ref/heads/' + BRANCH:
    finish({'ref': 'refs/heads/' + BRANCH, 'object': {'type': 'commit', 'sha': state['ref']}})
if method == 'GET' and endpoint.startswith('contents/'):
    path, ref = endpoint[len('contents/'):].split('?ref=')
    path = unquote(path)
    if path != QUEUE and state.get('patch_attempted'):
        finish(raw='forbidden post-change source body read', code=97)
    if path == QUEUE:
        data = queue_before() if ref != state.get('new_commit') else base64.b64decode(state['new_queue'])
        if state.get('patch_attempted') and scenario == 'post_queue_wrong': data += b'corrupted\n'
    else:
        if ref != HEAD or path not in state['sources']: finish(raw='wrong immutable source scope', code=98)
        data = Path(state['sources'][path]).read_bytes()
        if scenario == 'changed_source' and path.endswith('CLARIFICATIONS.md'): data += b'changed\n'
    obj = {'type': 'file', 'path': path, 'encoding': 'base64', 'size': len(data), 'sha': hblob(data),
           'content': base64.b64encode(data).decode()}
    if scenario == 'wrong_source_size' and path.endswith('CLARIFICATIONS.md'): obj['size'] += 1
    finish(obj)
if method == 'GET' and endpoint.startswith('git/commits/'):
    commit = endpoint[len('git/commits/'):]
    if commit == HEAD:
        finish({'sha': HEAD, 'tree': {'sha': state['old_tree_sha']}, 'parents': [{'sha': '7' * 40}]})
    if commit != state.get('new_commit'): finish(raw='unknown commit', code=99)
    finish({'sha': commit, 'tree': {'sha': state['new_tree_sha']}, 'parents': [{'sha': HEAD}]})
if method == 'GET' and endpoint.startswith('git/trees/'):
    tree = endpoint[len('git/trees/'):]
    if '?' in tree: finish(raw='recursive tree read forbidden by fixed fixture', code=94)
    nodes = build_nodes(state['old_leaves'], state['old_tree_sha'])
    if 'new_leaves' in state: nodes.update(build_nodes(state['new_leaves'], state['new_tree_sha']))
    if tree not in nodes: finish(raw='unknown tree SHA', code=93)
    finish({'sha': tree, 'truncated': scenario == 'truncated_tree', 'tree': nodes[tree]})
if method == 'POST' and endpoint == 'git/blobs':
    if set(body) != {'content', 'encoding'} or body['encoding'] != 'base64': finish(raw='bad blob body', code=96)
    state['new_queue'] = body['content']
    state['new_blob_sha'] = hblob(base64.b64decode(body['content']))
    if scenario == 'malformed_blob_response': finish(raw='{')
    if scenario == 'lost_blob_response': finish(raw='', code=1)
    finish({'sha': state['new_blob_sha']})
if method == 'POST' and endpoint == 'git/trees':
    if body != {'base_tree': state['old_tree_sha'], 'tree': [
            {'path': QUEUE, 'mode': '100644', 'type': 'blob', 'sha': state['new_blob_sha']}]}:
        finish(raw='tree payload escaped QUEUE', code=96)
    state['new_tree_sha'] = '3' * 40
    state['new_leaves'] = dict(state['old_leaves'])
    state['new_leaves'][QUEUE] = {'mode': '100644', 'type': 'blob', 'sha': state['new_blob_sha']}
    if scenario == 'tree_changes_other_path': state['new_leaves']['unrelated.txt'] = {'mode': '100644', 'type': 'blob', 'sha': 'a' * 40}
    if scenario == 'malformed_tree_response': finish(raw='{')
    finish({'sha': state['new_tree_sha']})
if method == 'POST' and endpoint == 'git/commits':
    if body != {'message': 'Classify problem 30002737 as already solved', 'tree': state['new_tree_sha'], 'parents': [HEAD]}:
        finish(raw='commit payload escaped scope', code=96)
    state['new_commit'] = '4' * 40
    if scenario == 'malformed_commit_response': finish(raw='{')
    finish({'sha': state['new_commit']})
if method == 'GET' and endpoint.startswith('compare/'):
    if endpoint != 'compare/' + HEAD + '...' + state.get('new_commit', ''): finish(raw='wrong compare', code=96)
    files = [{'filename': QUEUE, 'status': 'modified', 'sha': state['new_blob_sha']}]
    if scenario == 'diff_changes_other_path' or (scenario == 'post_diff_wrong' and state.get('patch_attempted')):
        files.append({'filename': 'other.txt', 'status': 'modified', 'sha': 'a' * 40})
    finish({'status': 'ahead', 'total_commits': 1, 'files': files})
if method == 'PATCH' and endpoint == 'git/refs/heads/' + BRANCH:
    state['patch_attempted'] = True
    if body != {'sha': state.get('new_commit'), 'force': False}: finish(raw='bad patch body', code=96)
    if scenario != 'lost_patch_not_applied': state['ref'] = state['new_commit']
    if scenario in ('lost_patch_applied', 'lost_patch_not_applied'): finish(raw='', code=1)
    if scenario == 'malformed_patch_applied': finish(raw='{')
    if scenario == 'wrong_patch_response_applied': finish({'ref': 'wrong', 'object': {'sha': state['new_commit']}})
    finish({'ref': 'refs/heads/' + BRANCH, 'object': {'type': 'commit', 'sha': state['new_commit']}})
finish(raw='unexpected endpoint ' + endpoint, code=95)
