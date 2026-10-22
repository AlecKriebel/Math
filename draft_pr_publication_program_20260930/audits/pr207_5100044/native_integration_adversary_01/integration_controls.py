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
import contextlib
import io

HERE = Path(__file__).absolute().parent
FROZEN = HERE / '_private/native207_frozen_v2'
HELPER_NAME = 'native207_v2.py'
HELPER_PIN = {'bytes': 31634, 'sha256': 'e850bb9adcb40db4d9949251c103677e37651f3ec3daad16219227729f7e1efc'}
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
    path = FROZEN / HELPER_NAME
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
        self.activate()
        return self.h.inputs(self.file, self.wanted)

    def activate(self):
        self.h.BASE = self.base
        self.h.C = self.repo
        self.h.P = self.repo / self.h.PROGRAM

    def candidate(self):
        c, m, overlay, pre, pins = self.inputs()
        journal = Path(tempfile.mkdtemp(prefix='candidate-', dir=self.base))
        return self.h.candidate(c, m, overlay, pre, pins, self.db, journal)

    def sync(self, result, alter_acceptance=None):
        self.activate()
        self.db.ref = result['candidate']
        acceptance = dict(schema='pr207-root-native-integration-acceptance-v1', evidence_scope='ACTUAL_ROOT_RECEIPT',
                          PR=207, phase=self.manifest['phase'], accepted=True, full_scope_verified=True,
                          all_selected_native_bodies_verified=True, manifest_pin=self.wanted, helper_pin=HELPER_PIN,
                          facts=self.facts, parent=self.manifest['expected_parent'], original_head=self.h.HEAD,
                          original_head_tree=self.h.HEAD_TREE, candidate=result['candidate'], tree=result['tree'],
                          actual_MAIN_observed=result['candidate'], fixture_only=True, actual_events_created=False,
                          Root_ref_update=dict(expected_sha=self.manifest['expected_parent'], sha=result['candidate'],
                                               force=False, success_confirmed_by_actual_native_readback=True))
        if alter_acceptance:
            alter_acceptance(acceptance)
        path = self.base / 'TEST_ONLY_ACCEPTANCE.json'
        store(path, encode(acceptance))
        c, m, overlay, pre, pins = self.inputs()
        journal = Path(tempfile.mkdtemp(prefix='sync-', dir=self.base))
        original_put = self.h.put
        self.memory_receipts = {}
        def test_only_put(directory, name, value):
            if value.get('evidence_scope') == 'ACTUAL_ROOT_RECEIPT':
                self.memory_receipts[name] = copy.deepcopy(value)
            else:
                original_put(directory, name, value)
        self.h.put = test_only_put
        try:
            return self.h.sync(c, m, overlay, pre, pins, self.db, journal, self.wanted, path, pin(path.read_bytes()))
        finally:
            self.h.put = original_put


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
        for name, mutate in [
            ('preparation_gate_scope', lambda g: g.update(evidence_scope='PREPARATION_ONLY')),
            ('unaccepted_gate', lambda g: g.update(accepted=False)),
            ('missing_tracker_role', lambda g: g['receipts'].pop('tracker')),
            ('wrong_event_body_pin', lambda g: g['receipts']['publication'].update(sha256='f' * 64)),
        ]:
            f = make(name)
            gate = json.loads(f.overlay[f.gate])
            mutate(gate)
            f.overlay[f.gate] = encode(gate)
            f.freeze()
            trial(name, f.inputs)
        for phase in ['merge95', 'completion100']:
            f = make('phase-' + phase, phase)
            def valid_phase(f=f, phase=phase):
                result = f.candidate()
                check(result['parents'] == ([helper.ANCHOR, helper.HEAD] if phase == 'merge95' else [helper.ANCHOR]), 'Exact phase parents')
                check(result['facts'] == f.facts and result['facts']['goal_complete'] is False, 'Exact phase facts')
                actual = f.db.flat(result['tree'])
                before = f.db.flat(result['parent_tree'])
                for path in ['foreign-empty', 'foreign-run', 'foreign-link', 'foreign-module']:
                    check(actual[path] == before[path], 'Foreign native tuple changed')
                check(f.db.blobs[actual[helper.QUEUE][2]] == f.queue_new, 'Exact resulting QUEUE body')
            trial('exact_' + phase + '_parents_facts_foreign_tuples', valid_phase, False)
        missing_completion = make('noqueue-completion', 'completion100', False)
        trial('completion100_omitted_QUEUE', missing_completion.inputs)
        for name, mutate in [
            ('foreign_QUEUE_line', lambda raw: raw.replace(b'foreign exact', b'foreign edited')),
            ('post_status', lambda raw: raw.replace(b'claimed_solved', b'solved')),
            ('post_effort', lambda raw: raw.replace(b'1/5', b'2/5')),
            ('own_rank', lambda raw: raw.replace(b'| 225 |', b'| 226 |')),
            ('duplicate_own_row', lambda raw: raw + b'|'.join(QUEUED.split(b'|'))),
        ]:
            trial('queue_' + name, lambda mutate=mutate: helper.queue_change(full.queue_old, mutate(full.queue_new), 'merge95'))
        trial('queue_changed_preimage_status', lambda: helper.queue_change(full.queue_old.replace(b'queued', b'claimed_solved'), full.queue_new, 'merge95'))
        trial('queue_changed_preimage_whitespace', lambda: helper.queue_change(full.queue_old.replace(b' 225 ', b'  225 '), full.queue_new, 'merge95'))
        trial('completion100_QUEUE_note_change', lambda: helper.queue_change(full.queue_new, full.queue_new.replace(b'fixture reviewed', b'changed reviewed'), 'completion100'))
        trial('valid_queued_original_to_claimed_submission', lambda: helper.queue_change(full.queue_old, full.queue_new, 'merge95'), False)
        for name, mutate in [
            ('fact_bool_integer_alias', lambda f: f.manifest['facts'].update(active_PR=True)),
            ('extra_phase_fact', lambda f: f.manifest['facts'].update(extra=1)),
            ('premature_advance', lambda f: f.manifest['facts'].update(advance_to_next_PR_authorized_now=True)),
            ('goal_complete', lambda f: f.manifest['facts'].update(goal_complete=True)),
            ('published_count', lambda f: f.manifest['facts'].update(published_count=35)),
            ('manifest_total_bool', lambda f: f.manifest.update(total_files=True)),
        ]:
            f = make('mutant-' + name)
            mutate(f)
            store(f.file, encode(f.manifest))
            f.wanted = pin(f.file.read_bytes())
            trial(name, f.inputs)
        f = make('marker-mismatch')
        f.overlay[helper.VIEWS[3]] = helper.marker(helper.phase_facts('completion100')) + b'\n'
        f.freeze()
        trial('Markdown_phase_disagreement', f.inputs)
        f = make('counter-alias')
        view = json.loads(f.overlay[helper.VIEWS[0]])
        view['workflow_percent'] = 100
        f.overlay[helper.VIEWS[0]] = encode(view)
        f.freeze()
        trial('JSON_counter_alias_disagreement', f.inputs)
        f = make('nonfinite')
        raw = f.file.read_bytes().replace(b'"PR": 207,', b'"PR": 207, "extra": 1e999,')
        store(f.file, raw)
        f.wanted = pin(raw)
        trial('JSON_overflow_nonfinite', f.inputs)
        f = make('duplicate-key')
        raw = f.file.read_bytes().replace(b'"PR": 207,', b'"PR": 207, "PR": 207,')
        store(f.file, raw)
        f.wanted = pin(raw)
        trial('JSON_duplicate_key', f.inputs)
        f = make('source-writable')
        (f.base / f.manifest['files'][0]['source']).chmod(0o644)
        trial('mutable_selected_source', f.inputs)
        f = make('source-symlink')
        source = f.base / f.manifest['files'][0]['source']
        saved = source.read_bytes()
        source.unlink()
        store(f.base / 'symlink-target', saved)
        source.symlink_to(f.base / 'symlink-target')
        trial('symlink_selected_source', f.inputs)
        for name, mutate in [
            ('foreign_overlay', lambda row: row.update(path='foreign/escape.txt')),
            ('unsafe_source', lambda row: row.update(source='../escape')),
            ('wrong_blob_identity', lambda row: row.update(git_blob='f' * 40)),
            ('mode_preimage', lambda row: row.update(preimage=dict(mode='100755', type='blob', sha='f' * 40))),
        ]:
            f = make(name)
            mutate(f.manifest['files'][0])
            store(f.file, encode(f.manifest))
            f.wanted = pin(f.file.read_bytes())
            trial(name, f.inputs)
        for boundary, maximum_posts in [(1, 0), (3, 0), (4, 1), (5, 2)]:
            f = make('stale-' + str(boundary))
            observed = [0]
            def stale(method, path, body, f=f, observed=observed, boundary=boundary):
                if method == 'GET' and path == 'git/ref/heads/main':
                    observed[0] += 1
                    if observed[0] == boundary:
                        f.db.ref = 'd' * 40
            f.db.hook = stale
            trial('stale_MAIN_boundary_' + str(boundary), f.candidate)
            check(sum(x['method'] == 'POST' for x in f.db.calls) <= maximum_posts, 'POST after stale lease boundary')
        for name, mutate in [
            ('wrong_original_HEAD_tree', lambda j: j['tree'].update(sha='f' * 40)),
            ('draft_PR', lambda j: j.update(draft=True)),
            ('wrong_PR_HEAD', lambda j: j['head'].update(sha='f' * 40)),
            ('unmerged_completion', lambda j: j.update(merged=False, state='open')),
        ]:
            f = make(name, 'completion100' if name == 'unmerged_completion' else 'merge95')
            endpoint = 'git/commits/' + helper.HEAD if name == 'wrong_original_HEAD_tree' else 'pulls/207'
            def bad_api(method, path, body=None, f=f, mutate=mutate, endpoint=endpoint):
                value = f.db(method, path, body)
                if path == endpoint:
                    mutate(value)
                return value
            c, m, overlay, pre, pins = f.inputs()
            trial(name, lambda c=c, m=m, overlay=overlay, pre=pre, pins=pins, bad_api=bad_api: helper.plan(c, m, overlay, pre, pins, bad_api))
            check(not any(x['method'] == 'POST' for x in f.db.calls), 'Plan wrote objects')
        f = make('binary-dedup')
        for path in [helper.ATTEMPT + 'requirements.txt', helper.ATTEMPT + 'current_execution_receipt.json']:
            f.overlay[path] = b'\x00\xffsame binary fixture'
        f.freeze()
        def binary_dedup():
            f.candidate()
            check(sum(x['path'] == 'git/blobs' and x['method'] == 'POST' for x in f.db.calls) == 1, 'Binary SHA deduplication')
        trial('binary_blob_POST_deduplicated_verified', binary_dedup, False)
        for name, mutate in [
            ('verify_reversed_parent_order', lambda commit, result: commit['parents'].reverse()),
            ('verify_missing_original_HEAD_parent', lambda commit, result: commit.update(parents=commit['parents'][:1])),
            ('verify_wrong_tree', lambda commit, result: commit.update(tree={'sha': result['parent_tree']})),
            ('verify_wrong_message', lambda commit, result: commit.update(message='unreviewed message')),
        ]:
            f = make(name)
            result = f.candidate()
            mutate(f.db.commits[result['candidate']], result)
            c, m, overlay, pre, pins = f.inputs()
            trial(name, lambda c=c, m=m, overlay=overlay, pre=pre, pins=pins, f=f, result=result: helper.verify(c, m, overlay, pre, pins, f.db, m['expected_parent'], result['candidate']))
        f = make('verify-corrupt-native-body')
        result = f.candidate()
        f.db.blobs[native('blob', f.overlay[helper.ATTEMPT + 'requirements.txt'])] = b'forged native readback'
        c, m, overlay, pre, pins = f.inputs()
        trial('verify_corrupt_selected_native_body', lambda: helper.verify(c, m, overlay, pre, pins, f.db, m['expected_parent'], result['candidate']))
        f = make('verify-readonly')
        result = f.candidate()
        c, m, overlay, pre, pins = f.inputs()
        f.db.calls = []
        trial('independent_verify_GET_only', lambda: helper.verify(c, m, overlay, pre, pins, f.db, m['expected_parent'], result['candidate']), False)
        check(all(x['method'] == 'GET' for x in f.db.calls), 'Verify performed native mutation')
        f = make('dry-offline')
        f.activate()
        saved_argv, saved_api, saved_journal = sys.argv, helper.API, helper.journal_new
        def forbidden(*args, **kwargs):
            raise RuntimeError('Offline dry attempted API/journal')
        sys.argv = [str(FROZEN / HELPER_NAME), 'dry', '--manifest', str(f.file), '--manifest-bytes', str(f.wanted['bytes']), '--manifest-sha256', f.wanted['sha256']]
        helper.API = forbidden
        helper.journal_new = forbidden
        try:
            def dry():
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    helper.main()
                check(json.loads(output.getvalue())['status'] == 'OFFLINE_DRY_ONLY', 'Dry result')
            trial('dry_offline_no_API_or_journal', dry, False)
        finally:
            sys.argv, helper.API, helper.journal_new = saved_argv, saved_api, saved_journal
        f = make('api-boundaries')
        original_run = helper.subprocess.run
        dispatches = []
        def fake_run(argv, **kwargs):
            dispatches.append(argv)
            return subprocess.CompletedProcess(argv, 0, b'{"sha":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}', b'')
        helper.subprocess.run = fake_run
        try:
            for name, method, path, mutate in [
                ('PATCH_ref', 'PATCH', 'git/refs/heads/main', True),
                ('POST_ref', 'POST', 'git/refs', True),
                ('POST_service', 'POST', 'issues/207', True),
                ('GET_unbounded_path', 'GET', 'contents/secrets', False),
                ('read_only_POST_blob', 'POST', 'git/blobs', False),
            ]:
                journal = Path(tempfile.mkdtemp(prefix='api-', dir=f.base))
                api = helper.API(journal, mutate)
                trial(name, lambda api=api, method=method, path=path: api(method, path, {} if method != 'GET' else None))
            check(len(dispatches) == 0, 'Forbidden route reached process dispatch')
            def timed_out(argv, **kwargs):
                dispatches.append(argv)
                raise subprocess.TimeoutExpired(argv, 120)
            helper.subprocess.run = timed_out
            journal = Path(tempfile.mkdtemp(prefix='uncertain-', dir=f.base))
            api = helper.API(journal, True)
            trial('uncertain_POST_stops_attempt', lambda: api('POST', 'git/trees', {'tree': []}))
            trial('uncertain_POST_same_API_retry_refused', lambda: api('POST', 'git/trees', {'tree': []}))
            check(len(dispatches) == 1 and (journal / '00001.OBJECT_INTENT.json').exists() and (journal / '00001.STOPPED.json').exists(), 'Uncertainty retry/journal boundary')
        finally:
            helper.subprocess.run = original_run
        for name, alter in [
            ('sync_success', None),
            ('sync_force_true', lambda a: a['Root_ref_update'].update(force=True)),
            ('sync_false_acceptance', lambda a: a.update(accepted=False)),
            ('sync_preparation_acceptance', lambda a: a.update(evidence_scope='PREPARATION_ONLY')),
            ('sync_unconfirmed_CAS', lambda a: a['Root_ref_update'].update(success_confirmed_by_actual_native_readback=False)),
            ('sync_wrong_expected_SHA', lambda a: a['Root_ref_update'].update(expected_sha='e' * 40)),
        ]:
            f = make(name)
            result = f.candidate()
            def sync(f=f, result=result, alter=alter):
                receipt = f.sync(result, alter)
                check(all((f.repo / path).read_bytes() == f.overlay[path] for path in helper.VIEWS), 'Exact five local postimages')
                check('ROOT_ACTUAL_MERGE95_POINTER.json' in f.memory_receipts and receipt['all_five_local_files_match_actual_checkpoint'] is True, 'Pointer follows all-five check')
                check(not (f.base / 'ROOT_ACTUAL_MERGE95_POINTER.json').exists(), 'Actual fixture pointer was written to disk')
            trial(name, sync, alter is not None)
            if alter:
                check(all((f.repo / path).read_bytes() == f.old[path] for path in helper.VIEWS), 'Bad acceptance installed local view')
        f = make('sync-resume-postimage')
        result = f.candidate()
        store(f.repo / helper.VIEWS[0], f.overlay[helper.VIEWS[0]])
        trial('sync_resume_exact_accepted_postimage', lambda: f.sync(result), False)
        check(all((f.repo / path).read_bytes() == f.overlay[path] for path in helper.VIEWS), 'Resumed exact-five postimages')
        f = make('sync-lock-wrong')
        result = f.candidate()
        store(helper.P / 'ROOT_GLOBAL_FIVE_WRITER.lock', b'wrong stable lock bytes\n')
        trial('new_helper_wrong_stable_lock_payload', lambda: f.sync(result))
        check(not f.memory_receipts and all((f.repo / path).read_bytes() == f.old[path] for path in helper.VIEWS), 'Wrong lock allowed local mutation')
        f = make('sync-bad-preimage')
        result = f.candidate()
        store(f.repo / helper.VIEWS[-1], b'unrelated cooperating-writer edit\n')
        trial('sync_changed_preimage', lambda: f.sync(result))
        check(not f.memory_receipts, 'Stale local preimage published actual receipt')
        f = make('sync-stale-ref')
        result = f.candidate()
        refs = [0]
        def stale_at_pointer(method, path, body):
            if path == 'git/ref/heads/main':
                refs[0] += 1
                if refs[0] >= 4:
                    f.db.ref = 'd' * 40
        f.db.hook = stale_at_pointer
        trial('sync_MAIN_changed_before_pointer', lambda: f.sync(result))
        check(not f.memory_receipts, 'Stale ref published actual pointer')
        optimized = subprocess.run(['/opt/homebrew/opt/python@3.14/bin/python3.14', '-E', '-S', '-B', '-P', '-O', str(FROZEN / HELPER_NAME), '--help'], capture_output=True)
        check(optimized.returncode != 0 and b'Ordinary Python' in optimized.stderr, 'Optimized helper CLI accepted')
        outcomes.append(dict(control='optimized_helper_CLI_refused_before_inputs', result='PASS'))
    return dict(schema='pr207-independent-integration-controls-v1', evidence_scope='INDEPENDENT_OWNED_FIXTURES_ONLY', actual_events_created=False,
                helper_pin=HELPER_PIN, controls=outcomes, control_count=len(outcomes))


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
