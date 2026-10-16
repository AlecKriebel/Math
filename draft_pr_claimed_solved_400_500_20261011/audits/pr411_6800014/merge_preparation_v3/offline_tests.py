#!/usr/bin/env python3
"""Synthetic offline API model only; no native success is certified.

Generated receipts, data and journals stay in a caller-supplied private folder.
Isolated CLI subprocesses intercept gh and HTTP at transport boundaries.
"""
import argparse
import base64
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch
import urllib.parse

sys.dont_write_bytecode = True
HELPER = Path(__file__).with_name('pr411_admin.py')
spec = importlib.util.spec_from_file_location('admin_under_test', HELPER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class World:
    def __init__(self, root):
        self.root = root
        root.mkdir(parents=True, exist_ok=False)
        self.blobs, self.trees, self.commits, self.calls = {}, {}, {}, []
        self.loss = self.drift = None
        self.draft, self.merged, self.merge_sha = True, False, None
        self.ready_ref = None
        self.selected_reads = 0
        self.assets = {'paper.pdf': b'SYNTHETIC PDF TEST BYTES', 'proof.zip': b'SYNTHETIC ZIP A', 'checks.zip': b'SYNTHETIC ZIP B'}
        self.payloads = {m.PREFIX + 'PUBLICATION.md': b'Synthetic publication\n', m.PREFIX + 'README.md': b'Synthetic README\n'}
        self.payloads.update({m.PREFIX + 'paper/' + n: data for n, data in self.assets.items()})
        self.qbase = b'| Rank | ID / code | Problem | Status | Turns | Findings | DOI |\r\n| --- | --- | --- | --- | --- | --- | --- |\n| 1 | 12 / OTHER | Other | queued | 0/5 |  |  |\n| 444 | 6800014 / AMR-067-0014 | Synthetic target | queued | 0/5 |  |  |\r\n'
        self.qscience = self.qbase.replace(b'Synthetic target | queued | 0/5', b'Synthetic target | claimed_solved | 2/5')
        self.base = self.add_commit(self.make_tree({m.QUEUE: (self.qbase, '100644'), 'untouched.txt': (b'old\n', '100755')}), [])
        self.main = self.add_commit(self.make_tree({m.QUEUE: (self.qbase, '100644'), 'untouched.txt': (b'fresh main\n', '100755')}), [self.base])
        source = {m.QUEUE: (self.qscience, '100644'), 'untouched.txt': (b'old\n', '100755')}
        source.update({path: (data, '100644') for path, data in self.payloads.items()})
        self.science = self.head = self.add_commit(self.make_tree(source), [self.base])
        entries = [{'path': path, 'mode': '100644', 'bytes': len(data), 'sha256': m.digest(data), 'git_blob_sha1': m.git_sha('blob', data)} for path, data in self.payloads.items()]
        self.approved = {'format': 'pr411-approved-science-map-v1', 'scientific_head': self.science,
                         'selected_tree_sha': m.Merkle(self).at(self.commits[self.head]['tree']['sha'], m.PREFIX.rstrip('/'))['sha'],
                         'entries': entries, 'findings_path': m.PREFIX + 'PUBLICATION.md',
                         'assets': [{'name': n, 'path': m.PREFIX + 'paper/' + n, 'bytes': len(data), 'sha256': m.digest(data)} for n, data in self.assets.items()]}
        self.record_id = 999999999
        self.doi = '10.5281/zenodo.' + str(self.record_id)
        self.concept_id = str(self.record_id - 1)
        self.legacy_metadata = {'access_right': 'open', 'creators': [{'name': 'Synthetic'}], 'description': 'Not scientific evidence',
            'keywords': ['synthetic control'], 'language': 'eng', 'notes': 'Synthetic notes', 'publication_date': '2026-10-13',
            'title': 'Synthetic admin control', 'version': '0.1', 'license': 'cc-by-4.0', 'upload_type': 'publication',
            'publication_type': 'preprint', 'imprint_publisher': 'Zenodo', 'doi': self.doi,
            'prereserve_doi': {'doi': self.doi, 'recid': self.record_id}}
        same = {'access_right', 'creators', 'description', 'keywords', 'language', 'notes', 'publication_date', 'title', 'version'}
        public_metadata = {key: self.legacy_metadata[key] for key in same}
        public_metadata.update(doi=self.doi, license={'id': 'cc-by-4.0'},
            resource_type={'type': 'publication', 'subtype': 'preprint', 'title': 'Preprint'},
            relations={'version': [{'index': 0, 'is_last': True, 'parent': {'pid_type': 'recid', 'pid_value': self.concept_id}}]})
        self.public = {'id': self.record_id, 'doi': self.doi, 'metadata': public_metadata,
            'files': [{'key': n, 'size': len(data), 'checksum': 'md5:' + hashlib.md5(data).hexdigest()} for n, data in self.assets.items()]}
        parent = {'access': {'grants': [], 'links': [], 'owned_by': {'user': 1}, 'settings': {'allow_member_requests': False}},
            'communities': {'entries': [], 'default': None}, 'id': self.concept_id,
            'pids': {'doi': {'client': 'datacite', 'provider': 'datacite', 'identifier': '10.5281/zenodo.' + self.concept_id}}}
        self.auth_native = {'id': str(self.record_id), 'metadata': {'title': 'Synthetic actual native snapshot', 'publisher': 'Zenodo'},
            'access': {'record': 'public', 'files': 'public', 'embargo': {'active': False}}, 'custom_fields': {},
            'pids': {'doi': {'client': 'datacite', 'provider': 'datacite', 'identifier': self.doi},
                     'oai': {'identifier': 'oai:zenodo.org:' + str(self.record_id), 'provider': 'oai'}},
            'parent': parent, 'versions': {'index': 1, 'is_latest': True, 'is_latest_draft': True},
            'is_published': True, 'is_draft': False}
        self.native = copy.deepcopy(self.auth_native)
        self.native['versions'] = {'index': 1, 'is_latest': True}
        self.native['parent']['access'] = copy.deepcopy({key: value for key, value in parent['access'].items() if key not in ('grants', 'links')})
        self.binding = self.make_binding()
        self.map_ref = self.save('map.json', self.approved)
        self.evidence_ref = self.save('binding.json', self.binding)
        self.journal_root = root / 'journals'
        self.journal_root.mkdir()
        self.calls.clear()
        self.selected_reads = 0

    def save(self, name, obj):
        raw = m.encoded(obj)
        (self.root / name).write_bytes(raw)
        return {'path': name, 'sha256': m.digest(raw)}

    def make_binding(self):
        def intent(service, operation, params=None):
            return {'intent': {'service': service, 'operation': operation, 'params': params, 'evidence_kind': 'native_production_api', 'utc': m.utc()}, 'payload': None}
        def public_raw(obj, native=False):
            return {'url': 'https://zenodo.org/api/records/' + str(self.record_id), 'accept': 'application/vnd.inveniordm.v1+json' if native else 'application/json',
                    'status': 200, 'body_base64': base64.b64encode(m.encoded(obj)).decode()}
        def gws(method, params, response):
            return {'service': 'gws', 'method': method, 'params': params, 'returncode': 0,
                    'stdout_base64': base64.b64encode(m.encoded(response)).decode(), 'stderr_base64': ''}
        pub = {'submitted_intent': self.save('submitted_intent.json', intent('zenodo', 'GET /api/deposit/depositions/' + str(self.record_id))),
               'submitted_response': self.save('submitted_response.json', {'id': self.record_id, 'doi': self.doi, 'submitted': True, 'metadata': self.legacy_metadata}),
               'legacy_public_response': self.save('public_response.json', self.public),
               'legacy_public_native': self.save('public_raw.json', public_raw(self.public)),
               'authenticated_native_response': self.save('auth_native.json', self.auth_native),
               'public_native_response': self.save('native_response.json', self.native),
               'public_native_native': self.save('native_raw.json', public_raw(self.native, True)),
               'approved_native_snapshot': self.save('snapshot.json', {k: self.auth_native[k] for k in ('metadata', 'access', 'custom_fields')}),
               'result': self.save('publication_result.json', {'evidence_kind': 'native_production_api', 'status': 'tracker_already_exact', 'tracker_range': "'Math Puzzles'!A42:D42", 'id': self.record_id, 'doi': self.doi,
                      'asset_hashes': [{'name': n, 'sha256': m.digest(data), 'size': len(data)} for n, data in self.assets.items()]})}
        rr = "'Math Puzzles'!A42:D42"
        row = ['https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf#page=12', 'https://github.com/AlecKriebel/Math/pull/411', 'https://doi.org/' + self.doi, 'Synthetic test row']
        meta_params = {'spreadsheetId': m.SHEET, 'fields': 'spreadsheetId,sheets.properties'}
        meta = {'spreadsheetId': m.SHEET, 'sheets': [{'properties': {'sheetId': m.GID, 'title': m.TITLE}}]}
        batch_params = {'spreadsheetId': m.SHEET, 'ranges': ["'Math Puzzles'!A1:D1", rr], 'majorDimension': 'ROWS', 'valueRenderOption': 'UNFORMATTED_VALUE'}
        batch = {'spreadsheetId': m.SHEET, 'valueRanges': [{'range': "'Math Puzzles'!A1:D1", 'majorDimension': 'ROWS', 'values': [m.HEADERS]},
                    {'range': rr, 'majorDimension': 'ROWS', 'values': [row]}]}
        sheet = {'metadata_intent': self.save('meta_intent.json', intent('sheet', 'get', meta_params)),
                 'metadata_native': self.save('meta_native.json', gws('get', meta_params, meta)), 'metadata_response': self.save('meta_response.json', meta),
                 'batch_intent': self.save('batch_intent.json', intent('sheet', 'batchGet', batch_params)),
                 'batch_native': self.save('batch_native.json', gws('batchGet', batch_params, batch)), 'batch_response': self.save('batch_response.json', batch),
                 'row_range': rr, 'expected_row': row, 'append_intent': None, 'append_native': None, 'append_response': None}
        return {'format': 'pr411-native-administration-bindings-v1', 'doi': self.doi, 'publication': pub, 'sheet': sheet}

    def make_tree(self, files):
        root = {}
        for path, (data, mode) in files.items():
            sha = m.git_sha('blob', data)
            self.blobs[sha] = data
            parts = path.split('/')
            node = root
            for part in parts[:-1]: node = node.setdefault(part, {})
            node[parts[-1]] = {'mode': mode, 'type': 'blob', 'sha': sha}
        def build(node):
            entries = {name: item if 'sha' in item else {'mode': '040000', 'type': 'tree', 'sha': build(item)} for name, item in node.items()}
            sha = m.node_identity(entries)
            self.trees[sha] = entries
            return sha
        return build(root)

    def add_commit(self, tree, parents, specification=None):
        value = specification or {'tree': tree, 'parents': parents, 'message': 'Synthetic historical commit', 'author': {}, 'committer': {}}
        sha = m.git_sha('commit', m.encoded(value)) if specification is None else m.commit_spec(tree, parents[0], parents[1],
                  {k: specification['author'][k] for k in ('name', 'email')}, specification['author']['date'])[0]
        self.commits[sha] = {'sha': sha, 'tree': {'sha': tree}, 'parents': [{'sha': p} for p in parents],
                             **{k: value[k] for k in ('message', 'author', 'committer')}}
        return sha

    def reachable(self, ancestor, head):
        pending, seen = [head], set()
        while pending:
            item = pending.pop()
            if item == ancestor: return True
            if item in seen: continue
            seen.add(item)
            pending.extend(p['sha'] for p in self.commits.get(item, {}).get('parents', []))
        return False

    def call(self, method, route, body=None):
        self.calls.append((method, route, copy.deepcopy(body)))
        if method == 'GET':
            if route == 'pulls/411': return {'number': 411, 'state': 'closed' if self.merged else 'open', 'draft': self.draft, 'merged': self.merged,
                'node_id': 'SYNTHETIC_PR_NODE', 'mergeable': True, 'mergeable_state': 'clean', 'merge_commit_sha': self.merge_sha,
                'head': {'sha': self.head, 'ref': m.BRANCH, 'repo': {'full_name': m.REPO}}, 'base': {'ref': 'main', 'repo': {'full_name': m.REPO}}}
            if route.startswith('git/ref/heads/'): return {'object': {'sha': self.main if route.endswith('/main') else self.head}}
            if route.startswith('git/commits/'): return copy.deepcopy(self.commits[route.rsplit('/', 1)[1]])
            if route.startswith('git/trees/'):
                sha = route.rsplit('/', 1)[1]
                return {'sha': sha, 'truncated': False, 'tree': [{'path': name, **item} for name, item in self.trees[sha].items()]}
            if route.startswith('git/blobs/'):
                sha = route.rsplit('/', 1)[1]
                self.selected_reads += int(any(m.git_sha('blob', data) == sha for data in self.payloads.values()))
                return {'sha': sha, 'encoding': 'base64', 'content': base64.b64encode(self.blobs[sha]).decode()}
            if route.startswith('contents/'):
                head = route.split('?ref=', 1)[1]
                entry = m.Merkle(self).at(self.commits[head]['tree']['sha'], m.QUEUE)
                return {'type': 'file', 'sha': entry['sha'], 'encoding': 'base64', 'content': base64.b64encode(self.blobs[entry['sha']]).decode()}
            if route.startswith('compare/'):
                before, after = route[len('compare/'):].split('...')
                status = 'identical' if before == after else ('ahead' if self.reachable(before, after) else 'diverged')
                return {'status': status, 'merge_base_commit': {'sha': before if status in ('ahead', 'identical') else self.base}}
            raise AssertionError('unmodeled GET ' + route)
        if route == 'git/blobs':
            data = base64.b64decode(body['content']); sha = m.git_sha('blob', data); self.blobs[sha] = data; answer = {'sha': sha}
        elif route == 'git/trees':
            entries = {e['path']: {k: e[k] for k in ('mode', 'type', 'sha')} for e in body['tree']}
            sha = m.node_identity(entries); self.trees[sha] = entries; answer = {'sha': sha}
        elif route == 'git/commits':
            answer = {'sha': self.add_commit(body['tree'], body['parents'], body)}
        elif route == 'git/refs/heads/' + m.BRANCH:
            if self.drift == 'ref': self.head = self.main
            if not self.reachable(self.head, body['sha']): raise m.Uncertain('modeled nonforce ref rejected')
            m.need(body['force'] is False, "synthetic offline invariant")
            self.head = body['sha']; answer = {'object': {'sha': self.head}}
        elif route == 'graphql':
            self.draft = False
            answer = {'data': {'markPullRequestReadyForReview': {'pullRequest': {'id': 'SYNTHETIC_PR_NODE', 'isDraft': False, 'headRefOid': self.head}}}}
        elif route == 'pulls/411/merge':
            m.need(body['sha'] == self.head and body['merge_method'] == 'merge', "synthetic offline invariant")
            source_view = m.Merkle(self)
            source_tree = self.commits[self.head]['tree']['sha']
            replacements = {m.PREFIX.rstrip('/'): source_view.at(source_tree, m.PREFIX.rstrip('/')),
                            m.QUEUE: source_view.at(source_tree, m.QUEUE)}
            merged_tree, nodes = source_view.overlay(self.commits[self.main]['tree']['sha'], replacements)
            for node in nodes: self.trees[node['sha']] = node['entries']
            self.merge_sha = self.add_commit(merged_tree, [self.main, self.head])
            self.main, self.merged = self.merge_sha, True; answer = {'merged': True, 'sha': self.merge_sha}
        else: raise AssertionError('unmodeled write ' + route)
        if self.loss == route: raise m.Uncertain('modeled response loss after side effect')
        return answer

    def production_record(self, record_id, native=False):
        m.need(record_id == self.record_id, "synthetic offline invariant")
        return copy.deepcopy(self.native if native else self.public)

    def production_asset(self, record_id, name, size):
        m.need(record_id == self.record_id, "synthetic offline invariant")
        return self.assets[name]

    def advance_main(self, label):
        root = self.commits[self.main]['tree']['sha']
        entries = copy.deepcopy(self.trees[root])
        data = ('Unrelated descendant ' + label).encode()
        blob_sha = m.git_sha('blob', data)
        self.blobs[blob_sha] = data
        entries['unrelated_' + label + '.txt'] = {'mode': '100755', 'type': 'blob', 'sha': blob_sha}
        sha = m.node_identity(entries)
        self.trees[sha] = entries
        self.main = self.add_commit(sha, [self.main])
        return self.main

    def prepare(self, phase='integrate', receipt=None):
        return m.prepare(self, self.root, phase, self.head, self.main, self.map_ref, self.evidence_ref,
                         {'name': 'Synthetic Test', 'email': 'test@example.invalid'}, '2026-10-13T00:00:00Z', receipt,
                         self.ready_ref if phase == 'merge' else None)

    def apply(self, plan, approved):
        approval = {'format': 'pr411-explicit-administration-approval-v1', 'phase': plan['phase'], 'plan_sha256': m.digest(m.encoded(m.canonical_plan(plan))),
                    'expected_head': plan['expected_head'], 'expected_main': plan['main_head'], 'authorize_one_phase': True}
        journal = m.Journal(self.journal_root, plan['phase'], plan['phase'], plan['expected_head'], m.digest(m.encoded(m.canonical_plan(plan))))
        try:
            result = m.execute(self, plan, approved, journal, approval)
            if plan['phase'] == 'ready': self.ready_ref = self.save('ready_receipt.json', result)
            return result
        finally: journal.close()


def lagged_call(world, trigger, attempts):
    original = world.call
    pending = {'remaining': 0}
    def call(method, route, body=None):
        answer = original(method, route, body)
        if method != 'GET' and route == trigger:
            pending['remaining'] = attempts
        if method == 'GET' and route == 'pulls/411' and pending['remaining']:
            pending['remaining'] -= 1
            if trigger.startswith('git/refs/'):
                answer['head']['sha'] = world.science
            elif trigger == 'graphql':
                answer['draft'] = True
            else:
                answer.update(state='open', merged=False, merge_commit_sha=None)
        return answer
    return original, call


def original_recovery_refs(world, plan):
    directory = world.journal_root / plan['phase']
    def ref(name):
        path = directory / name
        return {'path': path.relative_to(world.root).as_posix(), 'sha256': m.digest(path.read_bytes())}
    return ref('receipt.json'), ref('journal.jsonl')


def cli_child(root, phase, operation):
    w = World(root)
    receipt = None
    if phase != 'integrate':
        plan, approved = w.prepare()
        receipt = w.save('integration.json', w.apply(plan, approved))
        if phase == 'merge':
            ready, approved = w.prepare('ready', receipt)
            w.apply(ready, approved)
    plan, approved = w.prepare(phase, receipt)
    plan_ref = w.save('plan.json', plan)
    approval = {'format': 'pr411-explicit-administration-approval-v1', 'phase': phase, 'plan_sha256': m.digest(m.encoded(m.canonical_plan(plan))),
                'expected_head': plan['expected_head'], 'expected_main': plan['main_head'], 'authorize_one_phase': True}
    approval_ref = w.save('approval.json', approval)
    if operation == 'reconcile': w.apply(plan, approved)
    if operation == 'recover':
        trigger = 'git/refs/heads/' + m.BRANCH if phase == 'integrate' else ('graphql' if phase == 'ready' else 'pulls/411/merge')
        original, w.call = lagged_call(w, trigger, 5)
        try:
            w.apply(plan, approved)
            raise AssertionError('expected stale readback STOP absent')
        except m.Stop:
            pass
        finally:
            w.call = original
        stop_ref, journal_ref = original_recovery_refs(w, plan)
    def ref(value): return value['path'] + ':' + value['sha256']
    argv = [str(HELPER), operation, '--phase', phase, '--case', str(root), '--head', w.head, '--main', w.main,
            '--map', ref(w.map_ref), '--evidence', ref(w.evidence_ref), '--person-name', 'Synthetic Test',
            '--person-email', 'test@example.invalid', '--commit-date', '2026-10-13T00:00:00Z']
    if receipt: argv.extend(['--integration', ref(receipt)])
    if phase == 'merge': argv.extend(['--ready', ref(w.ready_ref)])
    if operation == 'apply': argv.extend(['--plan', ref(plan_ref), '--approval', ref(approval_ref), '--journal-root', str(root / 'cli_journal'), '--run-id', 'actual_cli'])
    if operation == 'reconcile': argv.extend(['--plan', ref(plan_ref)])
    if operation == 'recover': argv.extend(['--plan', ref(plan_ref), '--stop-receipt', ref(stop_ref), '--intent-journal', ref(journal_ref)])
    (root / 'cli_journal').mkdir()
    class Response:
        def __init__(self, url, data): self.url, self.data = url, data
        def geturl(self): return self.url
        def read(self, size=-1): return self.data if size == -1 else self.data[:size]
        def __enter__(self): return self
        def __exit__(self, *a): return None
    class Opener:
        def open(self, request, timeout=None):
            url = request if isinstance(request, str) else request.full_url
            if '/files/' in url:
                name = urllib.parse.unquote(url.split('/files/', 1)[1].split('/content', 1)[0]); data = w.assets[name]
            else: data = m.encoded(w.production_record(w.record_id, not isinstance(request, str) and request.get_header('Accept') == 'application/vnd.inveniordm.v1+json'))
            return Response(url, data)
    def transport(command, input=None, **kwargs):
        m.need(command[0:2] == ['gh', 'api'], "synthetic offline invariant")
        method = command[command.index('--method') + 1]
        route = next(c for c in command if c == 'graphql' or c.startswith('repos/'))
        route = route.removeprefix('repos/' + m.REPO + '/')
        data = w.call(method, route, None if input is None else json.loads(input))
        return subprocess.CompletedProcess(command, 0, m.encoded(data), b'')
    out = io.StringIO()
    with patch.object(sys, 'argv', argv), patch('subprocess.run', transport), patch('urllib.request.build_opener', return_value=Opener()), contextlib.redirect_stdout(out):
        runpy.run_path(str(HELPER), run_name='__main__')
    result = json.loads(out.getvalue())
    expected = result.get('native_write') is False if operation == 'plan' else result['result'] == ('OBSERVED_EXACT_OUTCOME' if operation == 'reconcile' else ('CONFIRMED_RESPONSE_LATER_READBACK' if operation == 'recover' else 'CONFIRMED'))
    m.need(expected, 'actual isolated CLI result differs')
    print(json.dumps({'result': 'PASS', 'phase': phase, 'operation': operation, 'synthetic_only': True}))


def suite(root):
    root.mkdir(parents=True, exist_ok=False)
    results = []
    def test(name, fn):
        fn()
        results.append({'name': name, 'result': 'PASS'})
    def rejects(name, fn):
        try: fn()
        except (m.Stop, KeyError, OSError, ValueError): return
        raise AssertionError(name + ' was accepted')
    def fixture(name): return World(root / name)
    w = fixture('baseline')
    plan, approved = w.prepare()
    test('stable_canonical_plan_after_fresh_GET', lambda: m.need(m.canonical_plan(w.prepare()[0]) == m.canonical_plan(plan), 'plan timestamp drift'))
    receipt = w.save('integration.json', w.apply(plan, approved))
    ready, approved = w.prepare('ready', receipt); w.apply(ready, approved)
    merge, approved = w.prepare('merge', receipt); outcome = w.apply(merge, approved)
    test('modeled_full_three_phase_flow_and_first_parent_preservation', lambda: m.need(outcome['result'] == 'CONFIRMED' and w.merged, 'flow failed'))
    test('one_nonforce_PATCH_one_ready_one_expectedSHA_merge', lambda: m.need(sum(c[0] == 'PATCH' for c in w.calls) == 1 and sum(c[1] == 'graphql' for c in w.calls) == 1 and sum(c[0] == 'PUT' for c in w.calls) == 1, 'write count'))
    v = fixture('main_descendants')
    p,a = v.prepare(); anchor = p['main_head']; old_digest = m.digest(m.encoded(m.canonical_plan(p)))
    n1 = v.advance_main('before_integration')
    p2,a = m.prepare(v,v.root,'integrate',v.head,v.main,v.map_ref,v.evidence_ref,
                     {'name':'Synthetic Test','email':'test@example.invalid'},'2026-10-13T00:00:00Z',anchor_override=anchor)
    test('descendant_main_changes_only_observations', lambda: m.need(m.digest(m.encoded(m.canonical_plan(p2))) == old_digest
         and p2['native_observations']['descendant_main']['observed_main'] == n1 and p2['main_head'] == anchor, 'descendant approval/observation mismatch'))
    receipt = v.save('integration.json',v.apply(p2,a)); v.advance_main('before_ready')
    r,a = v.prepare('ready',receipt); test('ready_accepts_exact_selected_descendant',lambda: m.need(r['main_head']==anchor,'anchor changed'))
    v.apply(r,a); actual_parent = v.advance_main('before_merge')
    g,a = v.prepare('merge',receipt); out = v.apply(g,a)
    test('merge_preserves_unrelated_actual_descendant_first_parent',lambda: m.need(out['readback']['actual_first_parent']==actual_parent
         and out['readback']['unrelated_first_parent_tree_preserved'] is True,'actual parent preservation failed'))
    for findings in ('PUBLICATION.md', 'README.md'):
        v = fixture('findings_' + findings); v.approved['findings_path'] = m.PREFIX + findings
        test('accepted_positive_' + findings, lambda v=v: m.accepted_map(v.approved, v.science))
    for path in ('/absolute', '../escape', 'a//b', 'a/../b', 'a\\b', 'a\0b'):
        test('path_rejection_' + repr(path), lambda path=path: rejects('path', lambda: m.path_name(path)))
    for status in ('already_solved', 'queued', 'partial', 'unknown'):
        v = fixture('status_' + status)
        v.qscience = v.qscience.replace(b'claimed_solved', status.encode())
        sha = m.Merkle(v).at(v.commits[v.head]['tree']['sha'], m.QUEUE)['sha']; v.blobs[sha] = v.qscience
        test('head_status_' + status + '_before_local_read', lambda v=v: rejects('nonclaimed', lambda: m.prepare(v, v.root, 'integrate', v.head, v.main,
                 {'path': 'ABSENT', 'sha256': '0' * 64}, v.evidence_ref, {}, None)))
        m.need(v.selected_reads == 0, "synthetic offline invariant")
    for bad in ('already_solved', 'badDOI', 'badTurns', 'badFindings'):
        data = w.qbase
        if bad == 'already_solved': data = data.replace(b'Synthetic target | queued', b'Synthetic target | already_solved')
        if bad == 'badTurns': data = data.replace(b'Synthetic target | queued | 0/5', b'Synthetic target | queued | 1/5')
        if bad == 'badDOI': data = data.replace(b'Synthetic target | queued | 0/5 |  |  |', b'Synthetic target | queued | 0/5 |  | OTHER |')
        if bad == 'badFindings': data = data.replace(b'Synthetic target | queued | 0/5 |  |  |', b'Synthetic target | queued | 0/5 | OTHER |  |')
        test('main_queue_' + bad, lambda data=data: rejects(bad, lambda: m.queue_overlay(data, w.doi, plan['proposal']['findings'])))
    for field, value in (('path', m.PREFIX + '../escape'), ('path', m.PREFIX + 'private_sources/key'), ('mode', '120000'), ('mode', '160000'), ('sha256', '0' * 64)):
        v = fixture('map_' + field + '_' + str(len(results))); v.approved['entries'][0][field] = value
        test('selected_source_boundary_' + field + '_' + str(value), lambda v=v: rejects('bad approved entry', lambda: m.verify_selected(v, v.commits[v.head]['tree']['sha'], v.approved)))
    for kind in ('asset_sha', 'metadata', 'public_extra_file', 'native_access'):
        v = fixture(kind)
        if kind == 'asset_sha': v.assets['paper.pdf'] += b'corrupt'
        if kind == 'metadata': v.public['metadata']['title'] = 'changed'
        if kind == 'public_extra_file': v.public['files'].append({'key': 'extra'})
        if kind == 'native_access': v.native['access']['files'] = 'restricted'
        test('publication_' + kind, lambda v=v: rejects(kind, lambda: v.prepare()))
    def changed_response(v, kind, transform):
        group = v.binding['sheet']
        key = kind + '_response'
        response = json.loads((v.root / group[key]['path']).read_text())
        transform(response)
        group[key] = v.save(kind + '_response.json', response)
        native_key = kind + '_native'
        native = json.loads((v.root / group[native_key]['path']).read_text())
        native['stdout_base64'] = base64.b64encode(m.encoded(response)).decode()
        group[native_key] = v.save(kind + '_native.json', native)
        v.evidence_ref = v.save('binding.json', v.binding)
    mutations = {
        'wrong_spreadsheet': ('metadata', lambda o: o.update(spreadsheetId='WRONG')),
        'wrong_gid': ('metadata', lambda o: o['sheets'][0]['properties'].update(sheetId=1)),
        'wrong_title': ('metadata', lambda o: o['sheets'][0]['properties'].update(title='Other')),
        'wrong_batch_id': ('batch', lambda o: o.update(spreadsheetId='WRONG')),
        'wrong_header': ('batch', lambda o: o['valueRanges'][0]['values'][0].__setitem__(0, 'Problem ID')),
        'wrong_PR': ('batch', lambda o: o['valueRanges'][1]['values'][0].__setitem__(1, 'https://github.com/AlecKriebel/Math/pull/421')),
        'wrong_DOI': ('batch', lambda o: o['valueRanges'][1]['values'][0].__setitem__(2, 'https://doi.org/10.5281/zenodo.1')),
        'wrong_row_range': ('batch', lambda o: o['valueRanges'][1].update(range="'Math Puzzles'!A43:D43")),
        'wrong_dimension': ('batch', lambda o: o['valueRanges'][1].update(majorDimension='COLUMNS')),
        'duplicate_row': ('batch', lambda o: o['valueRanges'][1]['values'].append(o['valueRanges'][1]['values'][0])),
    }
    for name, (kind, transform) in mutations.items():
        v = fixture('sheet_' + name); changed_response(v, kind, transform)
        test('native_Sheet_' + name, lambda v=v: rejects('Sheet drift', lambda: v.prepare()))
    v = fixture('sheet_stale')
    ref = v.binding['sheet']['batch_intent']; intent = json.loads((v.root / ref['path']).read_text())
    intent['intent']['utc'] = '2000-01-01T00:00:00Z'; v.binding['sheet']['batch_intent'] = v.save('batch_intent.json', intent)
    v.evidence_ref = v.save('binding.json', v.binding)
    test('native_Sheet_stale_intent', lambda: rejects('stale', lambda: v.prepare()))
    for name, replacement in (('head_drift', 'f' * 40), ('main_drift', 'e' * 40)):
        v = fixture(name)
        expected_head, expected_main = v.head, v.main
        if name == 'head_drift': v.head = replacement
        else: v.main = replacement
        test(name + '_before_local_science_read', lambda v=v,h=expected_head,b=expected_main: rejects('native drift', lambda: m.prepare(v,v.root,'integrate',h,b,v.map_ref,v.evidence_ref,{},None)))
        m.need(v.selected_reads == 0, "synthetic offline invariant")
    for defect in ('truncated', 'bad_immediate_SHA', 'duplicate_tree_name', 'bad_blob_SHA'):
        v = fixture('merkle_' + defect); original = v.call
        def corrupted(method, route, body=None, original=original, defect=defect):
            answer = original(method, route, body)
            if method == 'GET' and route.startswith('git/trees/'):
                if defect == 'truncated': answer['truncated'] = True
                if defect == 'bad_immediate_SHA': answer['sha'] = '0' * 40
                if defect == 'duplicate_tree_name': answer['tree'].append(copy.deepcopy(answer['tree'][0]))
            if method == 'GET' and route.startswith('git/blobs/') and defect == 'bad_blob_SHA': answer['content'] = base64.b64encode(b'CORRUPT').decode()
            return answer
        v.call = corrupted
        test('immediate_Merkle_' + defect, lambda v=v: rejects(defect, lambda: v.prepare()))
    # Native API CAS limitations are not modeled as stronger guarantees.
    # A ref changed to another ancestor of the requested commit can still
    # satisfy force=false; this is an explicit API limitation, not a PASS
    # certificate that the old ref was atomically compared.
    v = fixture('approval_drift'); p,a = v.prepare(); p['proposal']['expected_tree'] = '0' * 40
    test('wrong_plan_separate_approval_rejected', lambda v=v,p=p,a=a: rejects('plan approval', lambda: m.execute(v,p,a,None,{})))
    v = fixture('journal_symlink')
    (v.root / 'journal_link').symlink_to(v.journal_root, target_is_directory=True)
    test('journal_symlink_ancestor_rejected', lambda: rejects('journal symlink', lambda: m.Journal(v.root / 'journal_link','bad','integrate',v.head,'0' * 64)))
    for route in ('git/blobs', 'git/trees', 'git/commits', 'git/refs/heads/' + m.BRANCH, 'graphql', 'pulls/411/merge'):
        v = fixture('loss_' + str(len(results)))
        p, a = v.prepare(); receipt = None
        if route in ('graphql', 'pulls/411/merge'):
            receipt = v.save('integration.json', v.apply(p, a)); p, a = v.prepare('ready', receipt)
        if route == 'pulls/411/merge': v.apply(p, a); p, a = v.prepare('merge', receipt)
        v.loss = route
        prior = len(v.calls)
        test('unknown_write_STOP_' + route, lambda v=v,p=p,a=a: rejects('response loss', lambda: v.apply(p,a)))
        writes = [c for c in v.calls[prior:] if c[0] != 'GET']
        m.need(writes and writes[-1][1] == route and (sum((c[1] == route for c in writes)) == 1), "synthetic offline invariant")
        journal = v.journal_root / p['phase'] / 'journal.jsonl'
        events = [json.loads(line) for line in journal.read_text().splitlines()]
        intent = next(e for e in reversed(events) if e['event'] == 'intent')
        prior = len(v.calls)
        test('GET_only_reconcile_' + route, lambda v=v,p=p,a=a,intent=intent: m.reconcile(v,p,a,intent))
        m.need(all((c[0] == 'GET' for c in v.calls[prior:])), "synthetic offline invariant")
        test('exclusive_no_blind_retry_' + route, lambda v=v,p=p: rejects('repeat intent', lambda: m.Journal(v.journal_root,'retry',p['phase'],p['expected_head'],m.digest(m.encoded(m.canonical_plan(p))))))
    v = fixture('unknown_ready_no_merge'); p,a = v.prepare(); receipt = v.save('integration.json',v.apply(p,a))
    p,a = v.prepare('ready',receipt); v.loss = 'graphql'
    rejects('unknown ready',lambda: v.apply(p,a))
    test('unknown_ready_cannot_advance_to_merge', lambda: rejects('unknownready advancement',lambda: v.prepare('merge',receipt)))
    # Known native ACKs and stale metadata are separate from unknown writes.
    for phase in ('integrate', 'ready', 'merge'):
        v = fixture('known_ack_' + phase)
        integration = None
        if phase != 'integrate':
            p,a = v.prepare(); integration = v.save('integration.json',v.apply(p,a))
            if phase == 'merge':
                p,a = v.prepare('ready',integration); v.apply(p,a)
        p,a = v.prepare(phase,integration)
        trigger = 'git/refs/heads/' + m.BRANCH if phase == 'integrate' else ('graphql' if phase == 'ready' else 'pulls/411/merge')
        original, v.call = lagged_call(v,trigger,5)
        test('known_ACK_stale_' + phase + '_STOP',lambda v=v,p=p,a=a: rejects('lag STOP',lambda:v.apply(p,a)))
        v.call = original
        stop_ref,journal_ref = original_recovery_refs(v,p)
        before = len(v.calls)
        recovered = m.known_response_recovery(v,v.root,p,a,stop_ref,journal_ref)
        test('known_ACK_' + phase + '_GET_only_recovery',lambda recovered=recovered,before=before,v=v: m.need(
             recovered['result']=='CONFIRMED_RESPONSE_LATER_READBACK' and all(c[0]=='GET' for c in v.calls[before:]),'recovery wrote'))
        test('original_' + phase + '_STOP_preserved',lambda v=v,stop_ref=stop_ref: m.need(m.document(v.root,stop_ref)['result']=='STOP_UNCONFIRMED_OR_DRIFT','STOP relabeled'))
        test('recovered_' + phase + '_complete_custody_receiver',lambda v=v,recovered=recovered:m.validate_recovery_receiver(v,v.root,recovered))
        relabeled = {k:recovered[k] for k in ('format','phase','result','plan','readback')}
        test('relabel_observation_' + phase + '_receiver_rejected',lambda v=v,relabeled=relabeled:rejects('relabel',lambda:m.validate_recovery_receiver(v,v.root,relabeled)))
        corrupt = copy.deepcopy(recovered); corrupt['original_native_journal']['sha256']='0'*64
        test('recovered_' + phase + '_journal_hash_drift',lambda v=v,corrupt=corrupt:rejects('journal pin',lambda:m.validate_recovery_receiver(v,v.root,corrupt)))
        if phase == 'integrate':
            integration = v.save('recovered_integration.json',recovered)
            ready,a = v.prepare('ready',integration); v.apply(ready,a)
            test('recovered_integration_receiver_after_ready',lambda:v.prepare('merge',integration))
        if phase == 'ready':
            v.ready_ref=v.save('recovered_ready.json',recovered)
            test('recovered_ready_receiver_advances_separate_merge_plan',lambda:v.prepare('merge',integration))
    v = fixture('bounded_lag_positive'); p,a=v.prepare()
    original,v.call=lagged_call(v,'git/refs/heads/'+m.BRANCH,2)
    result=v.apply(p,a)
    test('bounded_metadata_GET_lag_settles_no_write_retry',lambda:m.need(result['readback']['metadata_GET_attempts']==3 and sum(c[0]=='PATCH' for c in v.calls)==1,'lag/readback/count'))
    v=fixture('unknown_ACK_recovery_rejected');p,a=v.prepare();v.loss='git/refs/heads/'+m.BRANCH
    rejects('unknown ACK',lambda:v.apply(p,a));stop_ref,journal_ref=original_recovery_refs(v,p)
    test('unknown_ACK_no_known_response_recovery',lambda:rejects('unknown recovery',lambda:m.known_response_recovery(v,v.root,p,a,stop_ref,journal_ref)))
    v=fixture('freshness_deadline');p,a=v.prepare()
    test('verification_cost_is_observation_only',lambda:m.need('verification_cost' in p['native_observations'] and 'native_observations' not in m.canonical_plan(p),'metrics canonical'))
    p['native_evidence']['sheet_freshness_deadline_utc']='2000-01-01T00:00:00Z';before=len(v.calls)
    test('expired_Sheet_before_any_mutation',lambda:rejects('expired',lambda:v.apply(p,a)))
    m.need(all(c[0]=='GET' for c in v.calls[before:]),'expired evidence wrote')
    v=fixture('exact_automatic_publisher');v.legacy_metadata['imprint_publisher']='Zenodo'
    v.binding=v.make_binding();v.evidence_ref=v.save('binding_publisher.json',v.binding)
    test('exact_generated_publisher_is_editable_join',lambda:v.prepare())
    raw_faults = ('native_index_bool','native_setting_numeric','native_owner_bool','legacy_index_bool','legacy_is_last_numeric')
    for defect in raw_faults:
        v=fixture('raw_join_' + defect)
        key='legacy_public_native' if defect.startswith('legacy_') else 'public_native_native'
        raw=m.document(v.root,v.binding['publication'][key]);body=json.loads(base64.b64decode(raw['body_base64']))
        if defect=='native_index_bool':body['versions']['index']=True
        elif defect=='native_setting_numeric':body['parent']['access']['settings']['allow_member_requests']=0
        elif defect=='native_owner_bool':body['parent']['access']['owned_by']['user']=True
        elif defect=='legacy_index_bool':body['metadata']['relations']['version'][0]['index']=False
        elif defect=='legacy_is_last_numeric':body['metadata']['relations']['version'][0]['is_last']=1
        raw['body_base64']=base64.b64encode(m.encoded(body)).decode()
        v.binding['publication'][key]=v.save('corrupt_raw.json',raw);v.evidence_ref=v.save('corrupt_raw_binding.json',v.binding)
        test('typed_raw_parsed_' + defect + '_rejected',lambda v=v:rejects('rawtypedjoin',lambda:v.prepare()))
    # Full observed Zenodo legacy/native projection, independently re-pinned
    # malformed fixtures so rejection is semantic rather than a local hash miss.
    same = ('access_right','creators','description','keywords','language','notes','publication_date','title','version')
    for key in same:
        v=fixture('mapping_shared_' + key);v.public['metadata'][key]='DIFFERENT'
        v.binding=v.make_binding();v.evidence_ref=v.save('mapping_binding.json',v.binding)
        test('mapping_shared_field_' + key + '_rejected',lambda v=v:rejects('shared mapping',lambda:v.prepare()))
    defects = ('auth_extra','auth_missing','public_extra','public_missing','license_string','license_extra',
        'license_case','resource_title','resource_subtype','resource_extra','default_publisher','native_publisher',
        'reservation_recid','reservation_string_recid','reservation_bool_recid','reservation_doi','metadata_doi','relation_extra','relation_index','relation_bool_index',
        'relation_numeric_boolean','relation_parent','concept_pid','concept_id','auth_grants_nonempty','auth_links_missing',
        'public_grants_present','public_parent_owner','public_parent_bool_owner','native_version_index','native_version_bool_index',
        'native_version_numeric_boolean','public_private_version_flag','native_OAI','native_draft')
    for defect in defects:
        v=fixture('mapping_' + defect)
        if defect=='auth_extra':v.legacy_metadata['unobserved']='extra'
        elif defect=='auth_missing':v.legacy_metadata.pop('notes')
        elif defect=='public_extra':v.public['metadata']['imprint_publisher']='Zenodo'
        elif defect=='public_missing':v.public['metadata'].pop('notes')
        elif defect=='license_string':v.public['metadata']['license']='cc-by-4.0'
        elif defect=='license_extra':v.public['metadata']['license']['title']='CCBY'
        elif defect=='license_case':v.legacy_metadata['license']='CC-BY-4.0';v.public['metadata']['license']={'id':'CC-BY-4.0'}
        elif defect=='resource_title':v.public['metadata']['resource_type']['title']='preprint'
        elif defect=='resource_subtype':v.public['metadata']['resource_type']['subtype']='article'
        elif defect=='resource_extra':v.public['metadata']['resource_type']['id']='publication-preprint'
        elif defect=='default_publisher':v.legacy_metadata['imprint_publisher']='Different'
        elif defect=='native_publisher':v.auth_native['metadata'].pop('publisher');v.native['metadata'].pop('publisher')
        elif defect=='reservation_recid':v.legacy_metadata['prereserve_doi']['recid']=str(v.record_id-1)
        elif defect=='reservation_string_recid':v.legacy_metadata['prereserve_doi']['recid']=str(v.record_id)
        elif defect=='reservation_bool_recid':v.legacy_metadata['prereserve_doi']['recid']=True
        elif defect=='reservation_doi':v.legacy_metadata['prereserve_doi']['doi']='10.5281/zenodo.1'
        elif defect=='metadata_doi':v.public['metadata']['doi']='10.5281/zenodo.1'
        elif defect=='relation_extra':v.public['metadata']['relations']['other']=[]
        elif defect=='relation_index':v.public['metadata']['relations']['version'][0]['index']=1
        elif defect=='relation_bool_index':v.public['metadata']['relations']['version'][0]['index']=False
        elif defect=='relation_numeric_boolean':v.public['metadata']['relations']['version'][0]['is_last']=1
        elif defect=='relation_parent':v.public['metadata']['relations']['version'][0]['parent']['pid_value']='1'
        elif defect=='concept_pid':v.auth_native['parent']['pids']['doi']['identifier']='10.5281/zenodo.1'
        elif defect=='concept_id':v.auth_native['parent']['id']=int(v.concept_id)
        elif defect=='auth_grants_nonempty':v.auth_native['parent']['access']['grants']=[{'permission':'edit'}]
        elif defect=='auth_links_missing':v.auth_native['parent']['access'].pop('links')
        elif defect=='public_grants_present':v.native['parent']['access']['grants']=[]
        elif defect=='public_parent_owner':v.native['parent']['access']['owned_by']['user']=2
        elif defect=='public_parent_bool_owner':v.native['parent']['access']['owned_by']['user']=True
        elif defect=='native_version_index':v.auth_native['versions']['index']=2;v.native['versions']['index']=2
        elif defect=='native_version_bool_index':v.auth_native['versions']['index']=True;v.native['versions']['index']=True
        elif defect=='native_version_numeric_boolean':v.auth_native['versions']['is_latest']=1;v.native['versions']['is_latest']=1
        elif defect=='public_private_version_flag':v.native['versions']['is_latest_draft']=True
        elif defect=='native_OAI':v.auth_native['pids']['oai']['identifier']='oai:zenodo.org:1';v.native['pids']['oai']['identifier']='oai:zenodo.org:1'
        elif defect=='native_draft':v.auth_native['is_draft']=True;v.native['is_draft']=True
        v.binding=v.make_binding();v.evidence_ref=v.save('mapping_binding.json',v.binding)
        test('exact_projection_' + defect + '_rejected',lambda v=v:rejects('exact projection',lambda:v.prepare()))
    v=fixture('concept_derivation_positive');concept='1234567'
    for record in (v.auth_native,v.native):
        record['parent']['id']=concept;record['parent']['pids']['doi']['identifier']='10.5281/zenodo.'+concept
    v.public['metadata']['relations']['version'][0]['parent']['pid_value']=concept
    v.binding=v.make_binding();v.evidence_ref=v.save('concept_binding.json',v.binding)
    test('concept_derived_from_native_PID_not_record_arithmetic',lambda:v.prepare())
    for phase in ('integrate', 'ready', 'merge'):
        for operation in ('plan', 'apply', 'reconcile', 'recover'):
            target = root / ('cli_' + phase + '_' + operation)
            p = subprocess.run([sys.executable, '-B', str(Path(__file__).resolve()), '--cli-child', phase, operation, '--private-dir', str(target)], capture_output=True, text=True)
            (root / ('cli_' + phase + '_' + operation + '_NATIVE.json')).write_text(json.dumps({'command': p.args, 'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}, indent=2))
            test('isolated_actual_CLI_' + phase + '_' + operation, lambda p=p: m.need(p.returncode == 0 and json.loads(p.stdout)['result'] == 'PASS', 'isolated CLI failed: ' + p.stderr))
    return {'result': 'PASS_OFFLINE_MODEL', 'native_write': False, 'scientific_contents_inspected': False, 'test_count': len(results),
            'tests': results, 'boundary': 'Synthetic model fixtures and intercepted transports only. This is not native publication, Sheet, integration, readiness or merge evidence.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private-dir', type=Path, required=True)
    parser.add_argument('--cli-child', nargs=2, metavar=('PHASE', 'OPERATION'))
    args = parser.parse_args()
    if args.cli_child: cli_child(args.private_dir, *args.cli_child)
    else: print(json.dumps(suite(args.private_dir), indent=2))
