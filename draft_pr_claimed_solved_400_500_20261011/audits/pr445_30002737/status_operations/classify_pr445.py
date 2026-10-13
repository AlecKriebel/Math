#!/usr/bin/env python3
"""Fixed PR445 QUEUE-only correction; prepare is read-only; apply needs root digest."""
import argparse
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import quote

REPO = 'AlecKriebel/Math'
PR = 445
PROBLEM = '30002737'
HEAD = '3242c84e06db7e99012c7fe581adde5c3f89fc89'
BRANCH = 'research/diffraction-dynamical-30002737'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
RECEIPT_SHA256 = '31ccb9e3e153117812391ca028e2ea458d30eb6ac44699ec575f7a0e07292913'
SCHEMA = 'pr445_queue_classification_gate_v1'
HERE = Path(__file__).absolute().parent
PROGRAM = HERE.parents[2]
CASE = HERE.parent
SOURCE_RECEIPT = CASE / 'SOURCE_RECEIPT.json'
HEX40 = re.compile(r'[0-9a-f]{40}\Z')
HEX64 = re.compile(r'[0-9a-f]{64}\Z')

class Refusal(Exception):
    pass

class APIUncertain(Refusal):
    pass

def need(condition, message):
    if not condition:
        raise Refusal(message)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def blobsha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def pairs_no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result

def parse_json(raw):
    try:
        value = json.loads(raw, object_pairs_hook=pairs_no_duplicates,
                           parse_constant=lambda x: (_ for _ in ()).throw(Refusal('nonfinite JSON number')))
    except (ValueError, UnicodeError) as error:
        raise Refusal('invalid JSON: ' + str(error)) from error
    need(type(value) is dict, 'JSON root must be an object')
    return value

def regular_inside_case(rawpath):
    p = Path(rawpath)
    if not p.is_absolute():
        p = CASE / p
    need('..' not in p.parts, 'path traversal refused')
    need(p.is_relative_to(CASE), 'path outside CASE refused')
    for component in [p, *p.parents]:
        if component == CASE.parent:
            break
        need(not component.is_symlink(), 'symlink refused: ' + str(component))
    need(p.is_file(), 'required regular file absent: ' + str(p))
    return p

def check_gate(path, expected_digest):
    need(type(expected_digest) is str and HEX64.fullmatch(expected_digest),
         'apply requires --expected-gate-sha256 as trusted external expectation')
    raw = regular_inside_case(path).read_bytes()
    need(sha256(raw) == expected_digest, 'root gate digest mismatch')
    gate = parse_json(raw)
    exact = {'schema': SCHEMA, 'repo': REPO, 'problem_id': PROBLEM,
             'source_head': HEAD, 'branch': BRANCH, 'from_status': 'claimed_solved',
             'to_status': 'already_solved', 'source_receipt_sha256': RECEIPT_SHA256}
    for key, value in exact.items():
        need(type(gate.get(key)) is str and gate[key] == value, 'gate binding mismatch: ' + key)
    need(type(gate.get('pr')) is int and gate['pr'] == PR, 'gate PR must be literal integer 445')
    need(gate.get('approved') is True, 'root gate is not approved')
    need(gate.get('genuine_accepted_certificate') is True, 'root has not accepted a genuine certificate')
    bindings = gate.get('review_bindings')
    need(type(bindings) is list and len(bindings) >= 3, 'missing structural review bindings')
    roles = set()
    verified = []
    for binding in bindings:
        need(type(binding) is dict and set(binding) == {'role', 'path', 'sha256'}, 'malformed review binding')
        role, path, digest = binding['role'], binding['path'], binding['sha256']
        need(type(role) is str and role and role not in roles, 'empty or duplicate review role')
        need(type(path) is str and type(digest) is str and HEX64.fullmatch(digest), 'malformed review path/hash')
        data = regular_inside_case(path).read_bytes()
        need(sha256(data) == digest, 'review hash mismatch: ' + role)
        roles.add(role)
        verified.append({'role': role, 'path': path, 'sha256': digest})
    need({'root_disposition', 'priority', 'numeric_certificate_adversary'} <= roles,
         'required review role absent')
    return {'sha256': expected_digest, 'bindings': verified,
            'trust_boundary': 'Caller supplies trusted root digest; replacing both gate and digest replaces that trust.'}

def receipt_files():
    raw = regular_inside_case(SOURCE_RECEIPT).read_bytes()
    need(sha256(raw) == RECEIPT_SHA256, 'frozen source receipt changed')
    receipt = parse_json(raw)
    need(type(receipt.get('pr')) is int and receipt['pr'] == PR and
         receipt.get('problem_id') == PROBLEM and receipt.get('head_sha') == HEAD, 'frozen receipt identity mismatch')
    files = receipt.get('files')
    need(type(files) is list and len(files) == 12, 'receipt must specify exactly 12 originals')
    paths = set()
    prefix = 'unsolved_math_prioritization/attempts/30002737/'
    for entry in files:
        need(type(entry) is dict and set(entry) == {'path', 'bytes', 'sha256'}, 'invalid source entry')
        path = entry['path']
        need(type(path) is str and path.startswith(prefix) and path not in paths and
             '..' not in PurePosixPath(path).parts and not PurePosixPath(path).is_absolute(), 'unsafe source path')
        need(type(entry['bytes']) is int and entry['bytes'] >= 0 and
             type(entry['sha256']) is str and HEX64.fullmatch(entry['sha256']), 'invalid source size/hash')
        paths.add(path)
    return receipt

def queue_change(data, receipt):
    need(sha256(data) == receipt['queue_sha256'], 'immutable QUEUE hash differs')
    lines = data.splitlines(keepends=True)
    headers = [line for line in lines if line.startswith(b'| Rank |')]
    need(len(headers) == 1, 'QUEUE header absent or ambiguous')
    names = [x.strip() for x in headers[0].strip().split(b'|')[1:-1]]
    need(len(names) == len(set(names)), 'duplicate QUEUE headers')
    for column in (b'ID / code', b'Status', b'Turns', b'DOI'):
        need(column in names, 'required QUEUE header absent')
    indices = {column: names.index(column) for column in (b'ID / code', b'Status', b'Turns', b'DOI')}
    selected = []
    for number, line in enumerate(lines):
        if not line.startswith(b'|'):
            continue
        cells = line.rstrip(b'\r\n').split(b'|')[1:-1]
        if len(cells) == len(names) and cells[indices[b'ID / code']].strip().split(b' / ')[0] == PROBLEM.encode():
            selected.append((number, line, cells))
    need(len(selected) == 1, 'selected numeric problem row absent or ambiguous')
    number, line, cells = selected[0]
    need(line.rstrip(b'\r\n').decode() == receipt['selected_queue_row'], 'selected original row differs')
    need(cells[indices[b'Status']].strip() == b'claimed_solved', 'selected status is not claimed_solved')
    need(cells[indices[b'Turns']].strip() == b'1/5', 'selected attempts differ from 1/5')
    need(cells[indices[b'DOI']].strip() == b'', 'selected DOI is nonblank')
    # Byte offsets follow the header-derived column index, preserving every other byte.
    bars = [i for i, value in enumerate(line) if value == 124]
    start, end = bars[indices[b'Status']] + 1, bars[indices[b'Status'] + 1]
    cell = line[start:end]
    need(cell.count(b'claimed_solved') == 1, 'ambiguous status bytes')
    replacement = cell.replace(b'claimed_solved', b'already_solved', 1)
    new_line = line[:start] + replacement + line[end:]
    lines[number] = new_line
    return b''.join(lines), {'before_row': line.rstrip(b'\r\n').decode(),
                            'after_row': new_line.rstrip(b'\r\n').decode(),
                            'status_column': indices[b'Status'], 'turns_preserved': '1/5', 'doi_preserved': ''}

class API:
    def __init__(self, record):
        self.record = record

    def request(self, method, endpoint, body=None):
        argv = ['gh', 'api', '--method', method, 'repos/' + REPO + '/' + endpoint]
        payload = None
        if body is not None:
            argv += ['--input', '-']
            payload = json.dumps(body, sort_keys=True, separators=(',', ':')).encode()
        item = {'method': method, 'endpoint': endpoint}
        if payload is not None:
            item['request_bytes'] = len(payload)
            item['request_sha256'] = sha256(payload)
        self.record['api_calls'].append(item)
        if method != 'GET':
            self.record['mutation_attempts'].append({'method': method, 'endpoint': endpoint})
        try:
            result = subprocess.run(argv, input=payload, capture_output=True, timeout=60)
        except (OSError, subprocess.TimeoutExpired) as error:
            item['error'] = str(error)
            raise APIUncertain('API execution uncertain: ' + method + ' ' + endpoint) from error
        item.update({'returncode': result.returncode, 'response_bytes': len(result.stdout),
                     'response_sha256': sha256(result.stdout), 'stderr': result.stderr.decode(errors='replace')})
        if result.returncode:
            raise APIUncertain('API failed: ' + method + ' ' + endpoint)
        try:
            return parse_json(result.stdout)
        except Refusal as error:
            raise APIUncertain('API response invalid: ' + method + ' ' + endpoint + ': ' + str(error)) from error

    def metadata(self):
        pr = self.request('GET', 'pulls/445')
        need(type(pr.get('number')) is int and pr['number'] == PR and pr.get('state') == 'open' and
             pr.get('draft') is True, 'PR is not exact OPEN/DRAFT 445')
        for field, ref in [('head', BRANCH), ('base', 'main')]:
            info = pr.get(field)
            need(type(info) is dict and info.get('ref') == ref and type(info.get('repo')) is dict and
                 info['repo'].get('full_name') == REPO, 'PR ' + field + ' branch/repository mismatch')
        need(pr['head'].get('sha') == HEAD, 'PR head moved')
        need(self.ref() == HEAD, 'branch head moved')

    def ref(self):
        response = self.request('GET', 'git/ref/heads/' + BRANCH)
        need(response.get('ref') == 'refs/heads/' + BRANCH and type(response.get('object')) is dict and
             response['object'].get('type') == 'commit' and HEX40.fullmatch(str(response['object'].get('sha'))), 'invalid branch ref')
        return response['object']['sha']

    def content(self, path, ref):
        obj = self.request('GET', 'contents/' + quote(path, safe='/') + '?ref=' + ref)
        need(obj.get('type') == 'file' and obj.get('path') == path and obj.get('encoding') == 'base64' and
             type(obj.get('size')) is int and type(obj.get('content')) is str, 'invalid content identity/encoding')
        try:
            data = base64.b64decode(''.join(obj['content'].split()), validate=True)
        except (ValueError, UnicodeError) as error:
            raise Refusal('invalid base64 content') from error
        need(len(data) == obj['size'] and obj.get('sha') == blobsha(data), 'content size/blob hash mismatch')
        return data, obj['sha']

    def commit(self, commit, tree=None, parent=None):
        obj = self.request('GET', 'git/commits/' + commit)
        need(obj.get('sha') == commit and type(obj.get('tree')) is dict and
             HEX40.fullmatch(str(obj['tree'].get('sha'))), 'invalid commit identity/tree')
        if tree is not None:
            need(obj['tree']['sha'] == tree and type(obj.get('parents')) is list and
                 len(obj['parents']) == 1 and obj['parents'][0].get('sha') == parent, 'new commit tree/parent mismatch')
        return obj['tree']['sha']

    def tree(self, sha):
        if not hasattr(self, 'tree_cache'):
            self.tree_cache = {}
        if sha in self.tree_cache:
            return self.tree_cache[sha]
        obj = self.request('GET', 'git/trees/' + sha)
        need(obj.get('sha') == sha and obj.get('truncated') is False and type(obj.get('tree')) is list, 'incomplete or invalid tree')
        result = {}
        for entry in obj['tree']:
            need(type(entry) is dict and type(entry.get('path')) is str and entry['path'] not in result and
                 '/' not in entry['path'] and entry['path'] not in ('', '.', '..') and
                 HEX40.fullmatch(str(entry.get('sha'))) and type(entry.get('mode')) is str and
                 entry.get('type') in ('tree', 'blob', 'commit'), 'invalid tree entry')
            result[entry['path']] = {key: entry[key] for key in ('mode', 'type', 'sha')}
        self.tree_cache[sha] = result
        return result

    def entry_at(self, root, path):
        parts = PurePosixPath(path).parts
        for index, part in enumerate(parts):
            entry = self.tree(root).get(part)
            need(entry is not None, 'required tree path absent: ' + path)
            if index == len(parts) - 1:
                return entry
            need(entry['type'] == 'tree' and entry['mode'] == '040000', 'unsafe tree ancestor: ' + path)
            root = entry['sha']

    def queue_only_tree(self, old_root, new_root, queue_blob):
        parts = PurePosixPath(QUEUE).parts
        for index, part in enumerate(parts):
            old, new = self.tree(old_root), self.tree(new_root)
            need(part in old and part in new and set(old) == set(new), 'tree path set changed')
            need({p: e for p, e in old.items() if p != part} ==
                 {p: e for p, e in new.items() if p != part}, 'created tree changes paths besides QUEUE')
            if index == len(parts) - 1:
                need(old[part]['mode'] == '100644' and old[part]['type'] == 'blob' and
                     new[part] == {'mode': '100644', 'type': 'blob', 'sha': queue_blob}, 'new QUEUE tree entry mismatch')
            else:
                need(old[part]['type'] == new[part]['type'] == 'tree' and
                     old[part]['mode'] == new[part]['mode'] == '040000', 'QUEUE ancestor mode/type changed')
                old_root, new_root = old[part]['sha'], new[part]['sha']

    def diff(self, commit, queue_sha):
        obj = self.request('GET', 'compare/' + HEAD + '...' + commit)
        files = obj.get('files')
        need(type(obj.get('total_commits')) is int and obj['total_commits'] == 1 and
             obj.get('status') == 'ahead' and type(files) is list and len(files) == 1,
             'commit comparison does not show one QUEUE-only commit')
        file = files[0]
        need(file.get('filename') == QUEUE and file.get('status') == 'modified' and
             file.get('sha') == queue_sha and 'previous_filename' not in file, 'actual commit diff is not QUEUE-only')

def execute(args, record):
    receipt = receipt_files()
    if args.mode == 'apply':
        record['root_gate'] = check_gate(args.gate, args.expected_gate_sha256)
    api = API(record)
    api.metadata()
    before, queue_sha = api.content(QUEUE, HEAD)
    after, row = queue_change(before, receipt)
    record['queue_change'] = row
    record['queue_before_sha256'] = sha256(before)
    record['queue_after_sha256'] = sha256(after)
    old_tree_sha = api.commit(HEAD)
    need(api.entry_at(old_tree_sha, QUEUE) == {'mode': '100644', 'type': 'blob', 'sha': queue_sha}, 'QUEUE tree identity/mode mismatch')
    originals = []
    for entry in receipt['files']:
        data, git_sha = api.content(entry['path'], HEAD)
        need(len(data) == entry['bytes'] and sha256(data) == entry['sha256'], 'original source bytes differ: ' + entry['path'])
        need(api.entry_at(old_tree_sha, entry['path']) == {'mode': '100644', 'type': 'blob', 'sha': git_sha}, 'source tree identity/mode mismatch')
        originals.append({**entry, 'git_blob_sha': git_sha})
    record['originals_verified_before_change'] = originals
    record['preflight_complete'] = True
    if args.mode == 'prepare':
        record['outcome'] = 'prepared_read_only'
        return 0
    blob_sha = blobsha(after)
    response = api.request('POST', 'git/blobs', {'content': base64.b64encode(after).decode(), 'encoding': 'base64'})
    need(response.get('sha') == blob_sha, 'created blob SHA mismatch')
    response = api.request('POST', 'git/trees', {'base_tree': old_tree_sha, 'tree': [
        {'path': QUEUE, 'mode': '100644', 'type': 'blob', 'sha': blob_sha}]})
    new_tree_sha = response.get('sha')
    need(type(new_tree_sha) is str and HEX40.fullmatch(new_tree_sha), 'created tree SHA invalid')
    api.queue_only_tree(old_tree_sha, new_tree_sha, blob_sha)
    response = api.request('POST', 'git/commits', {'message': 'Classify problem 30002737 as already solved',
                                                'tree': new_tree_sha, 'parents': [HEAD]})
    new_commit = response.get('sha')
    need(type(new_commit) is str and HEX40.fullmatch(new_commit), 'created commit SHA invalid')
    record['created_commit'] = new_commit
    api.commit(new_commit, tree=new_tree_sha, parent=HEAD)
    api.diff(new_commit, blob_sha)
    record['queue_only_commit_verified_before_change'] = True
    api.metadata()  # Fresh check just before the single nonforce PATCH; this is not compare-and-swap.
    patch_error = None
    try:
        patched = api.request('PATCH', 'git/refs/heads/' + BRANCH, {'sha': new_commit, 'force': False})
        need(patched.get('ref') == 'refs/heads/' + BRANCH and type(patched.get('object')) is dict and
             patched['object'].get('sha') == new_commit, 'PATCH response identity mismatch')
    except Refusal as error:
        patch_error = str(error)
        record['patch_response_error'] = patch_error
    # Once PATCH is attempted, ONLY administrative ref/QUEUE/diff readback is allowed.
    # Do not read source bodies, gate reviews, or perform mathematical processing here.
    observed_ref = api.ref()  # One reconciliation only, including uncertain/lost PATCH responses.
    observed_queue, observed_blob = api.content(QUEUE, observed_ref)
    record['post_patch_ref'] = observed_ref
    record['post_patch_queue_sha256'] = sha256(observed_queue)
    if observed_ref != new_commit or observed_queue != after or observed_blob != blob_sha:
        raise Refusal('PATCH reconciliation did not find the exact intended branch/QUEUE; do not resend')
    api.commit(new_commit, tree=new_tree_sha, parent=HEAD)
    api.diff(new_commit, blob_sha)
    record['original_source_paths_unchanged_by_commit_tree'] = True
    record['outcome'] = 'applied_reconciled_uncertain_patch' if patch_error else 'applied_verified'
    return 3 if patch_error else 0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['prepare', 'apply'])
    parser.add_argument('--gate', help='CASE-contained final root gate JSON, required for apply')
    parser.add_argument('--expected-gate-sha256', help='trusted externally supplied root gate digest, required for apply')
    args = parser.parse_args()
    record = {'schema': 'pr445_status_operation_receipt_v1', 'repo': REPO, 'pr': PR, 'problem_id': PROBLEM,
              'source_head': HEAD, 'branch': BRANCH, 'mode': args.mode, 'api_calls': [], 'mutation_attempts': [],
              'preflight_complete': False, 'outcome': 'refused', 'automatic_retries': 0,
              'nonforce_patch_is_compare_and_swap': False}
    status = 2
    try:
        need(HERE.name == 'status_operations' and HERE.parent.name == 'pr445_30002737' and
             PROGRAM.name == 'draft_pr_claimed_solved_400_500_20261011', 'helper location differs from assigned CASE')
        if args.mode == 'apply':
            need(args.gate is not None, 'apply requires final root --gate')
        status = execute(args, record)
    except (Refusal, OSError, KeyError, TypeError, AttributeError) as error:
        record['error'] = str(error)
        if record['mutation_attempts']:
            record['outcome'] = 'halted_after_mutation_attempt_no_retry'
    finally:
        record['completed_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print(json.dumps(record, indent=2, sort_keys=True))
    return status

if __name__ == '__main__':
    sys.exit(main())
