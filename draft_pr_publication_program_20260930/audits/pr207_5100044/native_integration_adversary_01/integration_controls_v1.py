"""Independent bounded native207 tests; owned fake data never actual evidence.

No network or Git command exists here. All imports use owned frozen bytepins;
all output of helper sync is confined to an owned TemporaryDirectory.
"""
import base64
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).absolute().parent
FROZEN = HERE / '_private/native207_frozen_v1'
HELPER_PIN = {'bytes': 31546, 'sha256': '8dcdda540bc8ea083feb5776227d3da971b1d9aca0b39aa84a58d7b0f1c7c910'}
QUEUED = b'| 225 | 5100044 / AMR-050-0044 | Elliptic-billiard invariant k_{804,a} | 0.1905 | 5.0 | 3 | 2021 | queued | 0/5 |  |  |  |\n'


def check(value, message):
    if value is not True:
        raise RuntimeError(message)


def pin(raw):
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def native(kind, raw):
    return hashlib.sha1(kind.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def store(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.chmod(0o644)
    path.write_bytes(raw)
    path.chmod(0o444)


def load():
    path = FROZEN / 'native207.py'
    check(pin(path.read_bytes()) == HELPER_PIN and path.resolve() == path and path.stat().st_mode & 0o777 == 0o444, 'Frozen helper pin')
    spec = importlib.util.spec_from_file_location('independent_native207', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Objects:
    def __init__(self, helper, phase):
        self.helper = helper
        self.phase = phase
        self.trees = {}
        self.blobs = {}
        self.commits = {}
        self.calls = []
        self.ref = helper.ANCHOR
        self.hook = None

    def blob(self, raw):
        sha = native('blob', raw)
        self.blobs[sha] = raw
        return sha

    def tree(self, rows):
        rows = sorted(rows, key=lambda row: row[0].encode() + (b'/' if row[1] == '040000' else b''))
        raw = b''.join((m.lstrip('0') + ' ' + n).encode() + b'\0' + bytes.fromhex(s) for n, m, k, s in rows)
        sha = native('tree', raw)
        self.trees[sha] = [dict(path=n, mode=m, type=k, sha=s) for n, m, k, s in rows]
        return sha

    def from_flat(self, mapping):
        trie = {}
        for path, value in mapping.items():
            parts = path.split('/')
            node = trie
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node[parts[-1]] = value
        def build(node):
            rows = []
            for name, value in node.items():
                if type(value) is dict:
                    rows.append((name, '040000', 'tree', build(value)))
                else:
                    rows.append((name, *value))
            return self.tree(rows)
        return build(trie)

    def flat(self, root, prefix=''):
        result = {}
        for row in self.trees[root]:
            path = prefix + row['path']
            if row['type'] == 'tree' and self.trees[row['sha']]:
                result.update(self.flat(row['sha'], path + '/'))
            else:
                result[path] = (row['mode'], row['type'], row['sha'])
        return result

    def __call__(self, method, path, body=None):
        self.calls.append(dict(method=method, path=path))
        if self.hook:
            self.hook(method, path, body)
        if path == 'git/ref/heads/main' and method == 'GET':
            return {'object': {'sha': self.ref}}
        if path == 'pulls/207' and method == 'GET':
            done = self.phase == 'completion100'
            return dict(number=207, head={'sha': self.helper.HEAD}, base={'ref': 'main'}, draft=False,
                        merged=done, state='closed' if done else 'open', merge_commit_sha='c' * 40 if done else None)
        if method == 'GET' and path.startswith('git/commits/'):
            sha = path.rsplit('/', 1)[1]
            if sha == self.helper.HEAD:
                return {'sha': sha, 'tree': {'sha': self.helper.HEAD_TREE}}
            return copy.deepcopy(self.commits[sha])
        if method == 'GET' and path.startswith('git/trees/'):
            sha = path.rsplit('/', 1)[1]
            return dict(sha=sha, truncated=False, tree=copy.deepcopy(self.trees[sha]))
        if method == 'GET' and path.startswith('git/blobs/'):
            sha = path.rsplit('/', 1)[1]
            raw = self.blobs[sha]
            return dict(sha=sha, size=len(raw), encoding='base64', content=base64.b64encode(raw).decode())
        if method == 'GET' and path.startswith('compare/'):
            return dict(status='ahead', merge_base_commit={'sha': path.split('/')[1].split('...')[0]})
        if method == 'POST' and path == 'git/blobs':
            return {'sha': self.blob(base64.b64decode(body['content'], validate=True))}
        if method == 'POST' and path == 'git/trees':
            flat = self.flat(body['base_tree'])
            for row in body['tree']:
                sha = row.get('sha') or self.blob(row['content'].encode())
                flat[row['path']] = (row['mode'], row['type'], sha)
            return {'sha': self.from_flat(flat)}
        if method == 'POST' and path == 'git/commits':
            sha = native('commit', encode(body))
            self.commits[sha] = dict(sha=sha, tree={'sha': body['tree']}, parents=[{'sha': x} for x in body['parents']], message=body['message'])
            return {'sha': sha}
        raise RuntimeError('Unexpected test endpoint ' + method + ' ' + path)


class Fixture:
    def __init__(self, helper, directory, phase='merge95', queue=True):
        self.h = helper
        self.root = directory
        self.base = directory / 'inputs'
        self.repo = directory / 'repo'
        self.base.mkdir()
        helper.BASE = self.base
        helper.C = self.repo
        helper.P = self.repo / helper.PROGRAM
        for name in ['archive206_verified_reference.py', 'CUSTODY_INVENTORY.json', 'CUSTODY_DELTA.json']:
            store(self.base / name, (FROZEN / name).read_bytes())
        self.db = Objects(helper, phase)
        self.overlay = {}
        self.old = {}
        inventory = json.loads((FROZEN / 'CUSTODY_INVENTORY.json').read_bytes())
        actual_case = HERE.parent
        for name, expected in inventory.items():
            raw = (actual_case / 'submitted_snapshot' / name).read_bytes()
            check(pin(raw) == {k: expected[k] for k in ('bytes', 'sha256')} and native('blob', raw) == expected['git_blob'], 'Independent custody source identity')
            self.overlay[helper.CASE + 'submitted_snapshot/' + name] = raw
            self.overlay[helper.ATTEMPT + name] = raw
        self.overlay[helper.ATTEMPT + 'requirements.txt'] = b'fixture only\n'
        self.overlay[helper.ATTEMPT + 'current_execution_receipt.json'] = b'{"fixture_only":true}\n'
        self.facts = helper.phase_facts(phase)
        view = dict(self.facts)
        view.update(published_PRs=list(range(1, 34)) + [207], fully_completed_eligible_PRs=list(range(1, 50)) + ([207] if phase == 'completion100' else []), dated_eligible_total=99)
        for index, path in enumerate(helper.VIEWS):
            self.overlay[path] = encode(view) if path.endswith('.json') else helper.marker(self.facts) + b'\nTEST FIXTURE ONLY\n'
            self.old[path] = b'owned preimage ' + str(index).encode() + b'\n'
            store(self.repo / path, self.old[path])
        self.gate = helper.CASE + 'TEST_ONLY_PHASE_GATE.json'
        roles = ['scientific', 'whole_package_review', 'publication', 'tracker'] + (['ready_PR_merge'] if phase == 'completion100' else [])
        receipts = {}
        for role in roles:
            path = helper.CASE + 'TEST_ONLY_' + role + '.json'
            self.overlay[path] = b'1'
            receipts[role] = dict(path=path, **pin(b'1'))
        gates = dict(schema='pr207-root-native-phase-gates-v1', evidence_scope='ACTUAL_ROOT_RECEIPT', PR=207,
                     phase=phase, accepted=True, original_head=helper.HEAD, facts=self.facts,
                     scientific_accepted=True, whole_package_accepted=True, actual_publication_verified=True,
                     actual_tracker_verified=True, ready_for_merge=True, receipts=receipts,
                     fixture_only=True, actual_events_created=False)
        self.overlay[self.gate] = encode(gates)
        cells = QUEUED.split(b'|')
        cells[8], cells[9], cells[11], cells[12] = b' claimed_solved ', b' 1/5 ', b' fixture reviewed findings ', b' https://doi.org/10.0000/fixture '
        self.queue_new = b'heading\n| foreign exact | untouched |\n' + b'|'.join(cells) + b'footer\n'
        self.queue_old = b'heading\n| foreign exact | untouched |\n' + QUEUED + b'footer\n' if phase == 'merge95' else self.queue_new
        if queue:
            self.overlay[helper.QUEUE] = self.queue_new
        self.old[helper.QUEUE] = self.queue_old
        self.manifest = dict(schema='pr207-native-integration-inputs-v1', PR=207, phase=phase,
                             anchor=helper.ANCHOR, original_head=helper.HEAD, original_head_tree=helper.HEAD_TREE,
                             expected_parent=helper.ANCHOR, helper_pin=HELPER_PIN, core_pin=helper.CORE_PIN,
                             facts=self.facts, gate_receipt=self.gate, commit_message='TEST FIXTURE ONLY; no actual event')
        self.manifest['local_views'] = [dict(path=path, preimage=pin(self.old[path])) for path in helper.VIEWS]
        self.file = self.base / 'INPUTS.json'
        self.freeze()
        empty = self.db.tree([])
        mapping = {path: ('100644', 'blob', self.db.blob(raw)) for path, raw in self.old.items()}
        mapping.update({'foreign-empty': ('040000', 'tree', empty),
                        'foreign-run': ('100755', 'blob', self.db.blob(b'#!/bin/sh\n')),
                        'foreign-link': ('120000', 'blob', self.db.blob(b'elsewhere')),
                        'foreign-module': ('160000', 'commit', '1' * 40)})
        root = self.db.from_flat(mapping)
        self.db.commits[helper.ANCHOR] = dict(sha=helper.ANCHOR, tree={'sha': root}, parents=[], message='fixture parent')
        lock = helper.P / 'ROOT_GLOBAL_FIVE_WRITER.lock'
        store(lock, helper.LOCK_BYTES)

    def freeze(self):
        rows = []
        for index, (path, raw) in enumerate(sorted(self.overlay.items())):
            source = 'payload/' + str(index)
            store(self.base / source, raw)
            old = self.old.get(path)
            preimage = dict(mode='100644', type='blob', sha=native('blob', old)) if old is not None else None
            rows.append(dict(path=path, source=source, **pin(raw), git_blob=native('blob', raw), preimage=preimage))
        self.manifest.update(files=rows, total_files=len(rows), total_bytes=sum(map(len, self.overlay.values())))
        raw = encode(self.manifest)
        store(self.file, raw)
        self.wanted = pin(raw)

    def inputs(self):
        return self.h.inputs(self.file, self.wanted)

    def candidate(self):
        c, m, overlay, pre, pins = self.inputs()
        journal = self.base / 'candidate'
        journal.mkdir()
        return self.h.candidate(c, m, overlay, pre, pins, self.db, journal)


def run():
    check(sys.flags.ignore_environment == 1 and sys.flags.no_site == 1 and sys.dont_write_bytecode is True and sys.flags.safe_path is True and sys.flags.optimize == 0, 'Ordinary Python -E -S -B -P required')
    helper = load()
    outcomes = []
    def trial(name, action, reject=True):
        try:
            action()
        except (RuntimeError, ValueError, KeyError, TypeError, OSError) as error:
            if not reject:
                raise
            outcomes.append(dict(control=name, result='REJECTED_AS_REQUIRED', exception=type(error).__name__))
        else:
            outcomes.append(dict(control=name, result='UNEXPECTED_ACCEPTANCE' if reject else 'PASS'))
    with tempfile.TemporaryDirectory(prefix='integration-controls-', dir=HERE / '_private') as temporary:
        root = Path(temporary)
        def make(name, phase='merge95', queue=True):
            path = root / name
            path.mkdir()
            return Fixture(helper, path, phase, queue)
        full = make('full')
        trial('merge95_valid_exact_overlay_candidate', full.candidate, False)
        check(all(x['path'] in ('git/trees', 'git/commits') for x in full.db.calls if x['method'] == 'POST'), 'Fixture unexpected POST')
        noqueue = make('noqueue', queue=False)
        def omitted_queue():
            result = noqueue.candidate()
            check(helper.QUEUE not in result['selected_files'], 'QUEUE unexpectedly selected')
            check(noqueue.db.blobs[noqueue.db.flat(result['tree'])[helper.QUEUE][2]] == noqueue.queue_old, 'QUEUE unexpectedly adopted')
        trial('merge95_omitted_QUEUE_leaves_queued_status', omitted_queue)
        alias = make('receipt_bool')
        gates = json.loads(alias.overlay[alias.gate])
        gates['receipts']['scientific']['bytes'] = True
        alias.overlay[alias.gate] = encode(gates)
        alias.freeze()
        trial('receipt_byte_pin_bool_alias', alias.inputs)
    return dict(schema='pr207-independent-integration-controls-v1', evidence_scope='INDEPENDENT_OWNED_FIXTURES_ONLY', actual_events_created=False,
                helper_pin=HELPER_PIN, controls=outcomes, control_count=len(outcomes))


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
