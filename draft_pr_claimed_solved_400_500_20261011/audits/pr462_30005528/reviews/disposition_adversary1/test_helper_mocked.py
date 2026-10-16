#!/usr/bin/env python3
"""Execute the reviewed helper main() with private evidence and a pure API mock.

No gh, network, Git or real gate is used. Acceptance uses explicit exceptions,
and an untouched copy of the reviewed helper. Private synthetic final-review
records are fixtures, never genuine review approvals.
"""
import argparse
import base64
import contextlib
import copy
import datetime
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
PROGRAM = AUDIT.parent.parent
HELPER = HERE / 'REVIEWED_HELPER_8563d0ac.py'
ORIGINAL = '3d5701d67e18745715d384c3db3fbee588b42a98'
COMMIT = 'a' * 40
PUBLISHED = 'f8e78179779f03cebfffa4e04d8c6403bb1e5dc1'
REPO = 'AlecKriebel/Math'
BRANCH = 'compact-domino-30005528-20261003'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')


def binding(audit, path):
    data = (audit / path).read_bytes()
    return {'path': path, 'bytes': len(data), 'sha256': digest(data)}


class Fixture:
    def __init__(self, directory):
        self.program = directory / PROGRAM.name
        self.audit = self.program / 'audits/pr462_30005528'
        self.audit.mkdir(parents=True)
        self.helper = self.program / HELPER.name
        shutil.copy2(HELPER, self.helper)
        mandatory = ['SOURCE_RECEIPT.json', 'pr_metadata.json', 'selected_queue_row.md',
                     'DISPOSITION_SYNTHESIS.md', 'reviews/priority/APPLICABILITY_CHAIN.md',
                     'reviews/priority/SOURCE_RECEIPT.json', 'reviews/priority/SEARCH_COVERAGE.md',
                     'MATHEMATICAL_FAMILY_READBACK.json', 'PRIORITY_FAMILY_READBACK.json',
                     'CANDIDATE_FAMILY_READBACK.json']
        self.source = json.loads((AUDIT / 'SOURCE_RECEIPT.json').read_text())
        frozen = ['source_snapshot/' + x['path'] for x in self.source['files']]
        config = [('source_admissibility', 'RESULT.json'), ('dynamical_adversary', 'RESULT.json'),
                  ('reproduction', 'RESULT.json'), ('priority', 'DECISION.json'),
                  ('candidate_adversary', 'RESULT.json')]
        pairs = [p for family, name in config for p in
                 ['reviews/' + family + '/REPORT.md', 'reviews/' + family + '/' + name]]
        self.paths = mandatory + frozen + pairs
        for path in self.paths:
            target = self.audit / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(AUDIT / path, target)
        # This synthetic queue isolates schema/preservation tests. It is not the
        # original whole queue, and its hash is changed only in this private copy.
        header = '| Rank | ID / code | Problem | EV | Impact (/10) | Difficulty | Proposed | Status | Turns | Chat | Findings | DOI |\n'
        sentinel = '| 999 | fixture / MOCK | Synthetic sentinel | 0 | 1 | 1 | 2000 | ignored_fixture | 2/5 | x | untouched | mock-doi |\n'
        self.before = ('# Private synthetic queue\n\n' + header + self.source['selected_queue_row'] + '\n' + sentinel).encode()
        self.source['queue_sha256'] = digest(self.before)
        write_json(self.audit / 'SOURCE_RECEIPT.json', self.source)
        final_dir = 'reviews/disposition_adversary1/'
        self.final = {'reviewer': '/root/pr462_disposition_adversary1', 'pr': 462,
                      'problem_id': '30005528', 'frozen_head': ORIGINAL,
                      'blocking_issues': 0, 'unresolved_disposition_issues': 0,
                      'required_corrections': 0, 'unresolved_mathematical_gaps': 0,
                      'reviewed_helper_sha256': digest(self.helper.read_bytes()),
                      'reviewed_synthesis_sha256': digest((self.audit / 'DISPOSITION_SYNTHESIS.md').read_bytes()),
                      'fixture_only': True}
        write_json(self.audit / (final_dir + 'RESULT.json'), self.final)
        (self.audit / (final_dir + 'REPORT.md')).write_text('PRIVATE SYNTHETIC MOCK REVIEW; NOT APPROVAL.\n')
        self.paths += [final_dir + 'REPORT.md', final_dir + 'RESULT.json']
        self.gate = {'verdict': 'ACCEPTED_PRIORITY_CLASSIFICATION', 'pr': 462,
                     'problem_id': '30005528', 'original_head': ORIGINAL,
                     'recommended_status': 'already_solved',
                     'acceptance_scope': 'one_row_priority_correction_then_immediate_skip',
                     'root_read_entire_final_reports': True,
                     'helper_sha256': digest(self.helper.read_bytes()),
                     'retained_v1_verification_blockers': 1,
                     'retained_v1_required_publication_repairs': 1,
                     'retained_candidate_publication_blockers': 2,
                     'published_disposition_url': 'https://github.com/AlecKriebel/Math/blob/' + PUBLISHED + '/' + PROGRAM.name + '/audits/pr462_30005528/DISPOSITION_SYNTHESIS.md',
                     'published_disposition_sha256': digest((self.audit / 'DISPOSITION_SYNTHESIS.md').read_bytes()),
                     'reviews': []}
        for family, name in config + [('disposition_adversary', 'RESULT.json')]:
            directory_name = 'disposition_adversary1' if family == 'disposition_adversary' else family
            result = self.final if family == 'disposition_adversary' else json.loads((self.audit / ('reviews/' + directory_name + '/' + name)).read_text())
            self.gate['reviews'].append({'family': family, 'reviewer': '/root/pr462_' + directory_name,
                                         'report_path': 'reviews/' + directory_name + '/REPORT.md',
                                         'result_path': 'reviews/' + directory_name + '/' + name,
                                         'raw_blocking_issues': None if family == 'priority' else result['blocking_issues'],
                                         'unresolved_disposition_issues': 0})
        self.remote = {'state': 'open', 'draft': True,
                       'head': {'sha': ORIGINAL, 'ref': BRANCH, 'repo': {'full_name': REPO}},
                       'base': {'ref': 'main', 'repo': {'full_name': REPO}}}
        self.ref = ORIGINAL
        self.calls = []
        self.eligible_calls = 0
        self.mutations = []
        self.after = None
        self.behavior = None
        self.queue_mode = '100644'
        self.queue_type = 'blob'
        self.comparison = [QUEUE]
        self.published_bytes = (self.audit / 'DISPOSITION_SYNTHESIS.md').read_bytes()
        self.published_type = 'file'
        self.published_encoding = 'base64'
        self.published_path_suffix = ''
        self.save_gate()

    def save_gate(self):
        self.gate['reviewed_files'] = [binding(self.audit, p) for p in self.paths]
        write_json(self.audit / 'PRIORITY_DISPOSITION_GATE.json', self.gate)

    def edit_result(self, family, field, value):
        directory = 'disposition_adversary1' if family == 'disposition_adversary' else family
        name = 'DECISION.json' if family == 'priority' else 'RESULT.json'
        path = self.audit / ('reviews/' + directory + '/' + name)
        data = json.loads(path.read_text())
        parts = field.split('.')
        target = data
        for part in parts[:-1]:
            target = target[part]
        target[parts[-1]] = value
        write_json(path, data)
        self.save_gate()

    def api(self, endpoint, payload=None, method='POST'):
        self.calls.append({'endpoint': endpoint, 'mutation': payload is not None, 'method': method})
        if payload is not None:
            self.mutations.append({'endpoint': endpoint, 'method': method})
        if endpoint.startswith('contents/'):
            path = endpoint[len('contents/'):].split('?')[0]
            return {'type': self.published_type, 'encoding': self.published_encoding,
                    'path': path + self.published_path_suffix,
                    'content': base64.b64encode(self.published_bytes).decode()}
        if endpoint == 'pulls/462':
            self.eligible_calls += 1
            data = copy.deepcopy(self.remote)
            if self.behavior == 'freshness_second_check' and self.eligible_calls >= 2:
                data['head']['sha'] = 'b' * 40
            if self.behavior == 'freshness_third_check' and self.eligible_calls >= 3:
                data['head']['sha'] = 'b' * 40
            return data
        if endpoint.startswith('git/ref/heads/'):
            return {'object': {'sha': self.ref}}
        if endpoint == 'git/commits/' + ORIGINAL:
            return {'tree': {'sha': 'original-tree'}}
        if endpoint == 'git/trees/original-tree':
            return {'tree': [{'path': 'unsolved_math_prioritization', 'type': 'tree', 'mode': '040000', 'sha': 'queue-tree'}]}
        if endpoint == 'git/trees/queue-tree':
            return {'tree': [{'path': 'QUEUE.md', 'type': self.queue_type, 'mode': self.queue_mode, 'sha': 'original-blob'}]}
        if endpoint == 'git/blobs/original-blob':
            return {'content': base64.b64encode(self.before).decode()}
        if endpoint == 'git/blobs' and payload is not None:
            self.after = base64.b64decode(payload['content'])
            return {'sha': 'new-blob'}
        if endpoint == 'git/trees' and payload is not None:
            require(payload == {'base_tree': 'original-tree', 'tree': [{'path': QUEUE, 'mode': '100644', 'type': 'blob', 'sha': 'new-blob'}]}, 'Unexpected tree payload')
            return {'sha': 'new-tree'}
        if endpoint == 'git/commits' and payload is not None:
            require(payload['parents'] == [ORIGINAL] and payload['tree'] == 'new-tree', 'Unexpected commit payload')
            return {'sha': COMMIT}
        if endpoint.startswith('compare/'):
            return {'files': [{'filename': p} for p in self.comparison]}
        if endpoint.startswith('git/refs/heads/') and method == 'PATCH':
            require(payload == {'sha': COMMIT, 'force': False}, 'Unexpected ref payload')
            if self.behavior == 'uncertain_no_update':
                raise RuntimeError('Mock transport uncertainty, no update')
            self.ref = COMMIT if self.behavior != 'wrong_ref_readback' else 'b' * 40
            if self.behavior == 'uncertain_updated':
                raise RuntimeError('Mock transport uncertainty, update applied')
            return {'object': {'sha': self.ref}}
        if endpoint == 'git/blobs/new-blob':
            data = self.after + b'wrong' if self.behavior == 'wrong_blob_readback' else self.after
            return {'content': base64.b64encode(data).decode()}
        raise RuntimeError('Unexpected API endpoint: ' + endpoint)

    def execute(self, apply):
        spec = importlib.util.spec_from_file_location('private_reviewed_helper', self.helper)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.api = self.api
        # Prohibit accidental subprocess use even if the tested helper changes.
        module.subprocess.run = lambda *a, **k: (_ for _ in ()).throw(RuntimeError('Real subprocess forbidden in mock'))
        old_argv = sys.argv
        output = io.StringIO()
        error = None
        try:
            sys.argv = [str(self.helper)] + (['--apply'] if apply else [])
            with contextlib.redirect_stdout(output):
                module.main()
        except (Exception, SystemExit) as exc:
            error = type(exc).__name__ + ': ' + str(exc)
        finally:
            sys.argv = old_argv
        return error

    def verify_success(self, apply):
        require(self.after is not None if apply else self.after is None, 'Mutation/preflight mismatch')
        if apply:
            before_lines = self.before.decode().splitlines()
            after_lines = self.after.decode().splitlines()
            require(len(before_lines) == len(after_lines), 'Line count changed')
            changed = [i for i, (a, b) in enumerate(zip(before_lines, after_lines)) if a != b]
            require(changed == [3], 'Other row changed')
            old = before_lines[3].split('|')[1:-1]
            new = after_lines[3].split('|')[1:-1]
            require([i for i, (a, b) in enumerate(zip(old, new)) if a != b] == [7, 10], 'Other cells changed')
            require(new[7].strip() == 'already_solved' and new[8].strip() == '1/5' and new[11].strip() == '', 'Status/count/DOI mismatch')
            require(self.ref == COMMIT and (self.audit / 'STATUS_REPAIR_RECEIPT.json').exists(), 'Missing verified apply')
            require(len([x for x in self.mutations if x['method'] == 'PATCH']) == 1, 'Ref PATCH repeated')
        else:
            require(not self.mutations and (self.audit / 'STATUS_REPAIR_PREFLIGHT.json').exists(), 'Preflight mutated')


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    public_inputs = [HELPER, AUDIT / 'DISPOSITION_SYNTHESIS.md']
    hashes_before = {str(p): digest(p.read_bytes()) for p in public_inputs}
    tests = []

    def test(name, change=None, apply=True, expectation='reject', no_dispatch=False):
        with tempfile.TemporaryDirectory(prefix='case_', dir=HERE / 'private_cases') as temporary:
            fixture = Fixture(Path(temporary))
            if change is not None:
                change(fixture)
            error = fixture.execute(apply)
            accepted = error is None
            if accepted and expectation == 'accept':
                fixture.verify_success(apply)
            passed = accepted if expectation == 'accept' else not accepted
            if no_dispatch and fixture.calls:
                passed = False
            tests.append({'case': name, 'expected': expectation, 'accepted': accepted,
                          'test_passed': passed, 'error': error,
                          'api_dispatches': len(fixture.calls), 'mock_mutations': len(fixture.mutations),
                          'patch_attempts': len([x for x in fixture.mutations if x['method'] == 'PATCH'])})

    (HERE / 'private_cases').mkdir(exist_ok=True)
    test('valid_preflight', apply=False, expectation='accept')
    test('valid_apply_one_row_preserved', expectation='accept')
    test('uncertain_updated_readback_only', lambda f: setattr(f, 'behavior', 'uncertain_updated'), expectation='accept')
    test('uncertain_no_update_no_retry', lambda f: setattr(f, 'behavior', 'uncertain_no_update'))
    test('wrong_ref_readback_no_retry', lambda f: setattr(f, 'behavior', 'wrong_ref_readback'))
    test('wrong_blob_readback', lambda f: setattr(f, 'behavior', 'wrong_blob_readback'))
    test('missing_gate', lambda f: (f.audit / 'PRIORITY_DISPOSITION_GATE.json').unlink(), no_dispatch=True)
    for path in ['SOURCE_RECEIPT.json', 'pr_metadata.json', 'selected_queue_row.md',
                 'DISPOSITION_SYNTHESIS.md', 'reviews/priority/APPLICABILITY_CHAIN.md',
                 'reviews/priority/SOURCE_RECEIPT.json', 'reviews/priority/SEARCH_COVERAGE.md',
                 'MATHEMATICAL_FAMILY_READBACK.json', 'PRIORITY_FAMILY_READBACK.json',
                 'CANDIDATE_FAMILY_READBACK.json']:
        def change(f, p=path):
            f.paths.remove(p)
            f.save_gate()
        test('missing_mandatory_' + path.replace('/', '_'), change, no_dispatch=True)
    for label, edit in [('duplicate_path', lambda e: e.append(copy.deepcopy(e[0]))),
                        ('parent_traversal', lambda e: e[0].update(path='../outside')),
                        ('absolute_path', lambda e: e[0].update(path='/outside')),
                        ('private_path', lambda e: e[0].update(path='private_cases/case.json')),
                        ('zero_length', lambda e: e[0].update(bytes=0)),
                        ('boolean_length', lambda e: e[0].update(bytes=True)),
                        ('wrong_digest', lambda e: e[0].update(sha256='0'*64))]:
        def change(f, func=edit):
            func(f.gate['reviewed_files'])
            write_json(f.audit / 'PRIORITY_DISPOSITION_GATE.json', f.gate)
        test('evidence_' + label, change, no_dispatch=True)
    for field, value in [('verdict', 'PASS'), ('pr', 461), ('problem_id', 'other'), ('original_head', 'b'*40),
                         ('recommended_status', 'claimed_solved'), ('acceptance_scope', 'publication'),
                         ('root_read_entire_final_reports', False), ('helper_sha256', '0'*64),
                         ('retained_v1_verification_blockers', 0), ('retained_v1_required_publication_repairs', False),
                         ('retained_candidate_publication_blockers', 0)]:
        def change(f, key=field, val=value):
            f.gate[key] = val
            f.save_gate()
        test('gate_' + field, change, no_dispatch=True)
    for index in range(12):
        def change(f, i=index):
            f.paths.remove('source_snapshot/' + f.source['files'][i]['path'])
            f.save_gate()
        test('missing_frozen_source_' + str(index), change, no_dispatch=True)
        def drift(f, i=index):
            path = f.audit / ('source_snapshot/' + f.source['files'][i]['path'])
            path.write_bytes(path.read_bytes()+b'\n')
        test('drift_frozen_source_' + str(index), drift, no_dispatch=True)
    test('evidence_same_size_digest_drift', lambda f: (f.audit / 'selected_queue_row.md').write_bytes(b'X' * (f.audit / 'selected_queue_row.md').stat().st_size), no_dispatch=True)
    for family in ['source_admissibility', 'dynamical_adversary', 'reproduction', 'priority', 'candidate_adversary', 'disposition_adversary']:
        test('wrong_identity_' + family, lambda f, x=family: f.edit_result(x, 'reviewer', '/root/other'), no_dispatch=True)
        test('wrong_head_' + family, lambda f, x=family: f.edit_result(x, 'frozen_head', 'b'*40), no_dispatch=True)
        for kind in ['report', 'result']:
            def change(f, x=family, field=kind):
                review = next(r for r in f.gate['reviews'] if r['family'] == x)
                f.paths.remove(review[field+'_path'])
                f.save_gate()
            test('missing_' + family + '_' + kind, change, no_dispatch=True)
    def wrong_numbered(f):
        next(r for r in f.gate['reviews'] if r['family']=='disposition_adversary')['reviewer'] = '/root/pr462_disposition_adversary'
        f.save_gate()
    test('final_numbered_reviewer_missing', wrong_numbered, no_dispatch=True)
    def duplicate_family(f):
        f.gate['reviews'][-1] = copy.deepcopy(f.gate['reviews'][0])
        f.save_gate()
    test('duplicate_review_family', duplicate_family, no_dispatch=True)
    for family, field, value in [
        ('source_admissibility', 'blocking_issues', False),
        ('dynamical_adversary', 'unresolved_mathematical_gaps', True),
        ('reproduction', 'blocking_issues', 0),
        ('reproduction', 'required_repairs', 0),
        ('reproduction', 'exact_counts.author_mutation_rejections_optimized', False),
        ('reproduction', 'exact_counts.author_mutation_rejections_normal', 6.0),
        ('candidate_adversary', 'blocking_issues', 0),
        ('candidate_adversary', 'required_repairs', True),
        ('candidate_adversary', 'required_changes', 1),
        ('candidate_adversary', 'current_publication_scope.blocking_issues', 0),
        ('candidate_adversary', 'current_publication_scope.required_verification_repairs', 0),
        ('candidate_adversary', 'current_publication_scope.priority_classification_changes', False),
        ('candidate_adversary', 'proposed_disposition_scope.unresolved_issues', False),
        ('candidate_adversary', 'proposed_disposition_scope.immediate_skip_after_already_solved', False),
        ('candidate_adversary', 'proposed_disposition_scope.verification_repair_required_for_classification', True),
        ('candidate_adversary', 'proposed_disposition_scope.further_math_repair_paper_publication_merge_close_comment', True),
        ('candidate_adversary', 'operations_approval', True),
        ('candidate_adversary', 'helper_reviewed', True),
        ('candidate_adversary', 'disposition_synthesis_scope_review.sha256', '0'*64),
        ('priority', 'first_priority_certified', True),
        ('priority', 'earlier_explicit_numbered_answer_located', True),
        ('priority', 'status_action_taken', True),
        ('disposition_adversary', 'blocking_issues', 1),
        ('disposition_adversary', 'required_corrections', False),
        ('disposition_adversary', 'reviewed_helper_sha256', '0'*64),
        ('disposition_adversary', 'reviewed_synthesis_sha256', '0'*64)]:
        test('result_' + family + '_' + field, lambda f, x=family, k=field, v=value: f.edit_result(x, k, v), no_dispatch=True)
    for label, transform in [('mutable_branch', lambda x: x.replace(PUBLISHED, 'main')),
                             ('wrong_path', lambda x: x.replace('DISPOSITION_SYNTHESIS.md', 'OTHER.md')),
                             ('query', lambda x: x+'?x=1'), ('fragment', lambda x: x+'#x'),
                             ('uppercase_sha', lambda x: x.replace(PUBLISHED, PUBLISHED.upper())),
                             ('wrong_repo', lambda x: x.replace('/Math/', '/Other/'))]:
        def change(f, func=transform):
            f.gate['published_disposition_url'] = func(f.gate['published_disposition_url'])
            f.save_gate()
        test('url_' + label, change, no_dispatch=True)
    for field, value in [('published_bytes', b'different'), ('published_type', 'dir'),
                         ('published_encoding', 'utf8'), ('published_path_suffix', '.other')]:
        test('remote_' + field, lambda f, k=field, v=value: setattr(f, k, v))
    for label, mutate in [('closed', lambda p: p.update(state='closed')),
                          ('not_draft', lambda p: p.update(draft=False)),
                          ('wrong_head', lambda p: p['head'].update(sha='b'*40)),
                          ('wrong_branch', lambda p: p['head'].update(ref='other')),
                          ('head_repo', lambda p: p['head']['repo'].update(full_name='Other/Math')),
                          ('base_repo', lambda p: p['base']['repo'].update(full_name='Other/Math')),
                          ('base_branch', lambda p: p['base'].update(ref='other'))]:
        test('freshness_' + label, lambda f, func=mutate: func(f.remote))
    test('changed_native_ref', lambda f: setattr(f, 'ref', 'b'*40))
    test('freshness_second_check_no_commit_patch', lambda f: setattr(f, 'behavior', 'freshness_second_check'))
    test('freshness_third_check_no_patch', lambda f: setattr(f, 'behavior', 'freshness_third_check'))
    test('queue_digest_drift', lambda f: setattr(f, 'before', f.before+b'\n'))
    test('queue_nonregular_mode', lambda f: setattr(f, 'queue_mode', '120000'))
    test('queue_nonblob', lambda f: setattr(f, 'queue_type', 'tree'))
    for label, transform in [('duplicate_selected', lambda b: b + (AUDIT / 'selected_queue_row.md').read_bytes()),
                             ('excluded_status', lambda b: b.replace(b' claimed_solved ', b' already_solved ')),
                             ('duplicate_header', lambda b: b + b.splitlines(keepends=True)[2]),
                             ('schema_column_missing', lambda b: b.replace(b'| DOI |', b'|'))]:
        def change(f, func=transform):
            f.before = func(f.before)
            f.source['queue_sha256'] = digest(f.before)
            write_json(f.audit / 'SOURCE_RECEIPT.json', f.source)
            f.save_gate()
        test('queue_' + label, change)
    test('compare_extra_file', lambda f: setattr(f, 'comparison', [QUEUE, 'extra.md']))
    test('compare_no_file', lambda f: setattr(f, 'comparison', []))
    test('repeat_apply_operation_exists', lambda f: (f.audit / 'STATUS_REPAIR_OPERATION.json').write_text('{}'), no_dispatch=True)
    for label in ['symlink', 'hardlink', 'directory', 'fifo', 'ancestor_alias']:
        def change(f, kind=label):
            output = f.audit / 'STATUS_REPAIR_PREFLIGHT.json'
            if kind == 'symlink':
                output.symlink_to(f.audit / 'DISPOSITION_SYNTHESIS.md')
            elif kind == 'hardlink':
                os.link(f.audit / 'DISPOSITION_SYNTHESIS.md', output)
            elif kind == 'directory':
                output.mkdir()
            elif kind == 'fifo':
                os.mkfifo(output)
            else:
                original = f.audit
                moved = original.parent / 'private_moved'
                original.rename(moved)
                original.symlink_to(moved, target_is_directory=True)
        test('output_' + label, change, no_dispatch=True)
    require({str(p): digest(p.read_bytes()) for p in public_inputs} == hashes_before, 'Shared helper/synthesis drifted')
    failed = [x for x in tests if not x['test_passed']]
    result = {'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'reviewer': '/root/pr462_disposition_adversary1', 'pr': 462, 'problem_id': '30005528',
              'frozen_head': ORIGINAL, 'mode': 'optimized' if sys.flags.optimize else 'normal',
              'optimization_level': sys.flags.optimize, 'actual_tests': len(tests),
              'passed_tests': len(tests)-len(failed), 'failed_tests': len(failed),
              'unexpected_acceptances': [x['case'] for x in failed if x['accepted']],
              'helper_sha256': hashes_before[str(HELPER)],
              'synthesis_sha256': hashes_before[str(AUDIT / 'DISPOSITION_SYNTHESIS.md')],
              'synthetic_final_review_gate_private_only': True,
              'real_subprocess_or_api_mutations': 0, 'shared_inputs_unchanged': True, 'tests': tests}
    write_json(Path(args.output), result)
    print(json.dumps({k: v for k, v in result.items() if k != 'tests'}, indent=2))


if __name__ == '__main__':
    run()
