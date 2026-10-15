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
        self.legacy_metadata = {'title': 'Synthetic admin control', 'creators': [{'name': 'Synthetic'}], 'description': 'Not scientific evidence', 'doi': self.doi}
        self.public = {'id': self.record_id, 'doi': self.doi, 'metadata': self.legacy_metadata,
                       'files': [{'key': n, 'size': len(data), 'checksum': 'md5:' + hashlib.md5(data).hexdigest()} for n, data in self.assets.items()]}
        self.native = {'id': str(self.record_id), 'metadata': {'title': 'Synthetic actual native snapshot'},
                       'access': {'record': 'public', 'files': 'public', 'embargo': {'active': False}}, 'custom_fields': {},
                       'pids': {'doi': {'identifier': self.doi}}, 'is_published': True}
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
               'authenticated_native_response': self.save('auth_native.json', self.native),
               'public_native_response': self.save('native_response.json', self.native),
               'public_native_native': self.save('native_raw.json', public_raw(self.native, True)),
               'approved_native_snapshot': self.save('snapshot.json', {k: self.native[k] for k in ('metadata', 'access', 'custom_fields')}),
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
            self.merge_sha = self.add_commit(self.commits[self.head]['tree']['sha'], [self.main, self.head])
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

    def prepare(self, phase='integrate', receipt=None):
        return m.prepare(self, self.root, phase, self.head, self.main, self.map_ref, self.evidence_ref,
                         {'name': 'Synthetic Test', 'email': 'test@example.invalid'}, '2026-10-13T00:00:00Z', receipt,
                         self.ready_ref if phase == 'merge' else None)

    def apply(self, plan, approved):
        approval = {'format': 'pr411-explicit-administration-approval-v1', 'phase': plan['phase'], 'plan_sha256': m.digest(m.encoded(plan)),
                    'expected_head': plan['expected_head'], 'expected_main': plan['main_head'], 'authorize_one_phase': True}
        journal = m.Journal(self.journal_root, plan['phase'], plan['phase'], plan['expected_head'], m.digest(m.encoded(plan)))
        try:
            result = m.execute(self, plan, approved, journal, approval)
            if plan['phase'] == 'ready': self.ready_ref = self.save('ready_receipt.json', result)
            return result
        finally: journal.close()


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
    approval = {'format': 'pr411-explicit-administration-approval-v1', 'phase': phase, 'plan_sha256': m.digest(m.encoded(plan)),
                'expected_head': plan['expected_head'], 'expected_main': plan['main_head'], 'authorize_one_phase': True}
    approval_ref = w.save('approval.json', approval)
    if operation == 'reconcile': w.apply(plan, approved)
    def ref(value): return value['path'] + ':' + value['sha256']
    argv = [str(HELPER), operation, '--phase', phase, '--case', str(root), '--head', w.head, '--main', w.main,
            '--map', ref(w.map_ref), '--evidence', ref(w.evidence_ref), '--person-name', 'Synthetic Test',
            '--person-email', 'test@example.invalid', '--commit-date', '2026-10-13T00:00:00Z']
    if receipt: argv.extend(['--integration', ref(receipt)])
    if phase == 'merge': argv.extend(['--ready', ref(w.ready_ref)])
    if operation == 'apply': argv.extend(['--plan', ref(plan_ref), '--approval', ref(approval_ref), '--journal-root', str(root / 'cli_journal'), '--run-id', 'actual_cli'])
    if operation == 'reconcile': argv.extend(['--plan', ref(plan_ref)])
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
    expected = result.get('native_write') is False if operation == 'plan' else result['result'] == ('OBSERVED_EXACT_OUTCOME' if operation == 'reconcile' else 'CONFIRMED')
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
    test('stable_canonical_plan_after_fresh_GET', lambda: m.need(w.prepare()[0] == plan, 'plan timestamp drift'))
    receipt = w.save('integration.json', w.apply(plan, approved))
    ready, approved = w.prepare('ready', receipt); w.apply(ready, approved)
    merge, approved = w.prepare('merge', receipt); outcome = w.apply(merge, approved)
    test('modeled_full_three_phase_flow_and_first_parent_preservation', lambda: m.need(outcome['result'] == 'CONFIRMED' and w.merged, 'flow failed'))
    test('one_nonforce_PATCH_one_ready_one_expectedSHA_merge', lambda: m.need(sum(c[0] == 'PATCH' for c in w.calls) == 1 and sum(c[1] == 'graphql' for c in w.calls) == 1 and sum(c[0] == 'PUT' for c in w.calls) == 1, 'write count'))
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
        test('exclusive_no_blind_retry_' + route, lambda v=v,p=p: rejects('repeat intent', lambda: m.Journal(v.journal_root,'retry',p['phase'],p['expected_head'],m.digest(m.encoded(p)))))
    v = fixture('unknown_ready_no_merge'); p,a = v.prepare(); receipt = v.save('integration.json',v.apply(p,a))
    p,a = v.prepare('ready',receipt); v.loss = 'graphql'
    rejects('unknown ready',lambda: v.apply(p,a))
    test('unknown_ready_cannot_advance_to_merge', lambda: rejects('unknownready advancement',lambda: v.prepare('merge',receipt)))
    for phase in ('integrate', 'ready', 'merge'):
        for operation in ('plan', 'apply', 'reconcile'):
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
