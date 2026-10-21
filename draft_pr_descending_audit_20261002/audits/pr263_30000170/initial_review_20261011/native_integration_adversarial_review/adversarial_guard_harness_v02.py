#!/usr/bin/env python3
"""Adversarial initial-guard tests of exact strengthened helper; no actual Git writes.

W/ROOT are redirected to an owned synthetic fixture, the pinned-reader import is
replaced with a stub implementing only initial validation operations, and Git
configuration reading is stubbed. No provider or primary Git operations occur.
The test stop is the first read-tree operation, before index/object writes.
"""
import base64
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
import types
from importlib.machinery import ModuleSpec

sys.dont_write_bytecode = True
R = Path('/Users/alec/Documents/Math')
W = R / 'draft_pr_descending_audit_20261002/audits/pr263_30000170/initial_review_20261011'
OWN = W / 'native_integration_adversarial_review'
PREP = W / 'integration_preparation/prepare_native_reconciliation.py'
EXPECTED = '7833158162faf6d68dc7d293ee42926fa357a6116004ab87636c6417ba0ece20'
TARGET = 'attempts/30000170'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
MAIN = 'd8540c93d2b763c3c287e2c493dec7019d8bd41b'
MAIN_TREE = '25aefa44bfb8bcc9475eba326661b7b3d7206003'
AUTHOR = 'c4eff3253932a504f8e558c8b5f5b1b5e155de0f'
B = R / 'draft_pr_descending_audit_20261002/audits/pr278_30005468/resume_20261011'

def oid(kind, b):
    return hashlib.sha1(kind.encode() + b' ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def pin(path):
    b = path.read_bytes()
    return {'path': str(path), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def load(path):
    def pairs(items):
        out = {}
        for k, v in items:
            if k in out:
                raise ValueError('Duplicate JSON key ' + k)
            out[k] = v
        return out
    return json.loads(path.read_bytes(), object_pairs_hook=pairs)

class ReachedWrites(Exception):
    pass

def main():
    now = dt.datetime.now(dt.timezone.utc)
    source = PREP.read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED
    fixture = OWN / 'private_instrumented_tests_v03'
    assert not fixture.exists(), 'Single-run fixture must be new'
    fixture.mkdir()
    fw = fixture / 'W'
    candidate = fw / 'publication_candidate/attempts/30000170'
    candidate.mkdir(parents=True)
    original = load(W / 'original_submission/MANIFEST_WITH_MODES.json')
    original_dir = fw / 'original_submission'
    original_dir.mkdir()
    for name in ['MANIFEST_WITH_MODES.json', 'BINDING.json']:
        (original_dir / name).write_bytes((W / 'original_submission' / name).read_bytes())
    entries = []
    def add(path, body):
        dest = candidate / path[len(TARGET) + 1:]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        entries.append(dict(path=path, source=str(dest), bytes=len(body), sha256=hashlib.sha256(body).hexdigest()))
    for e in original:
        if e['path'].startswith(TARGET + '/'):
            add(e['path'], Path(e['local']).read_bytes())
    for rel in ['output/pdf/nonunique_nearest_stable_complex_quadratics.pdf',
                'output/nonunique_nearest_stable_complex_quadratics_verification.zip']:
        add(TARGET + '/preprint/' + rel, (W / 'preprint_package_v03' / rel).read_bytes())
    add(TARGET + '/CANDIDATE_MANIFEST.json', b'{"synthetic_guard_test_fixture":true}\n')
    base = fw / 'integration_preparation/FRESH_MAIN_QUEUE.md'
    base.parent.mkdir(parents=True)
    base.write_bytes((W / 'integration_preparation/FRESH_MAIN_QUEUE.md').read_bytes())
    lines = base.read_bytes().splitlines(keepends=True)
    index = next(i for i, row in enumerate(lines) if len(row.split(b'|')) > 3 and row.split(b'|')[2].strip() == b'30000170 / OWR-783-002')
    oldrow = lines[index]
    cols = oldrow.split(b'|')
    cols[8], cols[9] = b' claimed_solved ', b' 1/5 '
    cols[10] = b' synthetic guard fixture: ../attempts/30000170/PROOF.md DOI 10.5281/zenodo.23306332 '
    newrow = b'|'.join(cols)
    lines[index] = newrow
    qsource = fw / 'synthetic_queue.md'
    qsource.write_bytes(b''.join(lines))
    entries.append(dict(path=QUEUE, source=str(qsource), bytes=qsource.stat().st_size, sha256=hashlib.sha256(qsource.read_bytes()).hexdigest()))
    acceptance_path = fixture / 'acceptance.json'
    target_bodies = sorted([dict(path=e['path'][len(TARGET) + 1:], bytes=e['bytes'], sha256=e['sha256']) for e in entries if e['path'] != QUEUE], key=lambda e:e['path'])
    acceptance = dict(schema='pr263-root-final-publication-candidate-acceptance-v1', accepted_for_native_preparation=True,
                      candidate_root=str(candidate), candidate_manifest=pin(candidate / 'CANDIDATE_MANIFEST.json'), target_bodies=target_bodies)
    acceptance_path.write_text(json.dumps(acceptance) + '\n')
    control = dict(main=MAIN, author=AUTHOR, candidate_acceptance=pin(acceptance_path), files=entries,
                   base_queue=pin(base), queue_before_base64=base64.b64encode(oldrow).decode(),
                   queue_after_base64=base64.b64encode(newrow).decode(),
                   original_manifest=pin(original_dir / 'MANIFEST_WITH_MODES.json'), original_binding=pin(original_dir / 'BINDING.json'))
    module = types.ModuleType('exact_strengthened_prepare_guard_test')
    module.__file__ = str(PREP)
    exec(compile(source, str(PREP), 'exec'), module.__dict__)
    module.W, module.ROOT = fw, fixture
    baseline = {QUEUE: dict(mode='100644', type='blob', sha=oid('blob', base.read_bytes())),
                'foreign/executable': dict(mode='100755', type='blob', sha='2' * 40),
                'foreign/symlink': dict(mode='120000', type='blob', sha='3' * 40),
                'foreign': dict(mode='040000', type='tree', sha='4' * 40)}
    state = {'inventory': baseline, 'kind': 'commit', 'remote_code': 1, 'remote_stdout': b''}
    def run_git(env, *args, data=None):
        if args[:2] == ('cat-file', '-t'):
            return ((state['kind'] if args[2] == MAIN else 'tree') + '\n').encode()
        if args[0] == 'rev-parse':
            return (MAIN_TREE + '\n').encode()
        if args == ('read-tree', '--empty'):
            raise ReachedWrites('Passed initial guards; stop before any private index/object write')
        raise AssertionError('Unexpected stub operation ' + repr(args))
    class Loader:
        @staticmethod
        def create_module(spec):
            return None
        @staticmethod
        def exec_module(mod):
            mod.git_oid = oid
            mod.load_json_no_duplicates = load
            mod.DRIVER = B / 'checkpoint_resume/driver.git'
            mod.OBJECTS = B / 'checkpoint_resume/private_objects'
            mod.ALTERNATES = [B / 'reconciliation/private_objects', B / 'objects.git/objects']
            mod.private_environment = lambda output: {}
            mod.run_git = run_git
            mod.inventory = lambda env, tree: state['inventory']
    real_spec = module.importlib.util.spec_from_file_location
    real_run = module.subprocess.run
    module.importlib.util.spec_from_file_location = lambda name, path: ModuleSpec(name, Loader())
    module.subprocess.run = lambda *args, **kwargs: types.SimpleNamespace(returncode=state['remote_code'], stdout=state['remote_stdout'])
    tests = []
    def case(name, modify=None, expectation='rejected', raw=None, modify_state=None, mutate_body=None):
        c = copy.deepcopy(control)
        if modify:
            modify(c)
        if modify_state:
            modify_state(state)
        cpath = fixture / (name + '.json')
        oldargv = sys.argv
        restore = mutate_body(c) if mutate_body else lambda: None
        cpath.write_text(raw(c) if raw else json.dumps(c) + '\n')
        sys.argv = [str(PREP), '--main', c['main'], '--selection', str(cpath), '--date', now.strftime('%Y-%m-%dT%H:%M:%SZ'), '--output', str(fixture / (name + '_output'))]
        try:
            module.main()
            observed, reason = 'unexpected_full_success', ''
        except ReachedWrites as e:
            observed, reason = 'reached_private_writes', str(e)
        except (ValueError, UnicodeError, KeyError, TypeError) as e:
            observed, reason = 'rejected', str(e)
        finally:
            sys.argv = oldargv
            restore()
            state.update(inventory=baseline, kind='commit', remote_code=1, remote_stdout=b'')
        tests.append(dict(name=name, expected=expectation, observed=observed, passed=observed == expectation, reason=reason))
    def candidate_change(c, rel, body):
        f = candidate / rel
        saved_body = f.read_bytes() if f.exists() else None
        saved_acceptance = acceptance_path.read_bytes()
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(body)
        rec = next((e for e in c['files'] if e['path'] == TARGET + '/' + rel), None)
        new = dict(path=TARGET + '/' + rel, source=str(f), bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
        if rec is None:
            c['files'].append(new)
        else:
            rec.update(new)
        ac = json.loads(saved_acceptance)
        ac['target_bodies'] = sorted([dict(path=e['path'][len(TARGET) + 1:], bytes=e['bytes'], sha256=e['sha256']) for e in c['files'] if e['path'] != QUEUE], key=lambda e:e['path'])
        if rel == 'CANDIDATE_MANIFEST.json':
            ac['candidate_manifest'] = pin(f)
        acceptance_path.write_text(json.dumps(ac) + '\n')
        c['candidate_acceptance'] = pin(acceptance_path)
        def restore():
            acceptance_path.write_bytes(saved_acceptance)
            if saved_body is None:
                f.unlink()
            else:
                f.write_bytes(saved_body)
        return restore
    def acceptance_change(c, modify):
        saved = acceptance_path.read_bytes()
        ac = json.loads(saved)
        modify(ac)
        acceptance_path.write_text(json.dumps(ac) + '\n')
        c['candidate_acceptance'] = pin(acceptance_path)
        return lambda:acceptance_path.write_bytes(saved)
    try:
        case('positive_complete_fixture', expectation='reached_private_writes')
        case('foreign_destination', lambda c:c['files'].__setitem__(0, dict(c['files'][0], path='attempts/OTHER/x.md')))
        case('wrong_unsolved_target_placement', lambda c:c['files'].__setitem__(0, dict(c['files'][0], path='unsolved_math_prioritization/attempts/30000170/x.md')))
        case('path_traversal', lambda c:c['files'].__setitem__(0, dict(c['files'][0], path=TARGET + '/../x.md')))
        case('doubled_slash', lambda c:c['files'].__setitem__(0, dict(c['files'][0], path=TARGET + '//x.md')))
        case('duplicate_destination', lambda c:c['files'].append(copy.deepcopy(c['files'][0])))
        case('missing_original17', lambda c:c['files'].pop(0))
        case('incorrect_sha256', lambda c:c['files'].__setitem__(0, dict(c['files'][0], sha256='0' * 64)))
        case('incorrect_byte_count', lambda c:c['files'].__setitem__(0, dict(c['files'][0], bytes=c['files'][0]['bytes'] + 1)))
        case('source_destination_mismatch', lambda c:c['files'].__setitem__(0, dict(c['files'][0], source=c['files'][1]['source'])))
        case('wrong_author', lambda c:c.__setitem__('author', '0' * 40))
        case('tree_oid_main', lambda c:c.__setitem__('main', MAIN_TREE))
        case('main_kind_not_commit', modify_state=lambda s:s.__setitem__('kind', 'tree'))
        case('duplicate_json_key', raw=lambda c:'{"author":"' + '0' * 40 + '",' + json.dumps(c)[1:])
        case('unbound_acceptance_pin', lambda c:c['candidate_acceptance'].__setitem__('sha256', '0' * 64))
        case('unbound_original_manifest', lambda c:c['original_manifest'].__setitem__('sha256', '0' * 64))
        case('unbound_original_binding', lambda c:c['original_binding'].__setitem__('sha256', '0' * 64))
        case('private_driver_remote_present', modify_state=lambda s:s.update(remote_code=0, remote_stdout=b'remote.fixture.url invalid\n'))
        case('queue_wrong_base_blob', modify_state=lambda s:s.__setitem__('inventory', dict(baseline, **{QUEUE:dict(mode='100644', type='blob', sha='0' * 40)})))
        case('queue_mode_100755', modify_state=lambda s:s.__setitem__('inventory', dict(baseline, **{QUEUE:dict(mode='100755', type='blob', sha=baseline[QUEUE]['sha'])})))
        case('existing_top_target', modify_state=lambda s:s.__setitem__('inventory', dict(baseline, **{TARGET + '/existing.md':dict(mode='100644', type='blob', sha='0' * 40)})))
        case('existing_unsolved_target', modify_state=lambda s:s.__setitem__('inventory', dict(baseline, **{'unsolved_math_prioritization/attempts/30000170/existing.md':dict(mode='100644', type='blob', sha='0' * 40)})))
        case('empty_tree_foreign', modify_state=lambda s:s.__setitem__('inventory', dict(baseline, **{'empty':dict(mode='040000', type='tree', sha='0' * 40)})))
        case('target_ancestor_leaf', modify_state=lambda s:s.__setitem__('inventory', dict(baseline, **{'attempts':dict(mode='120000', type='blob', sha='0' * 40)})))
        case('queue_exact_row_control_mismatch', lambda c:c.__setitem__('queue_after_base64', base64.b64encode(b'invalid\n').decode()))
        def change_queue(c, newbody):
            old = qsource.read_bytes()
            qsource.write_bytes(newbody)
            rec = next(e for e in c['files'] if e['path'] == QUEUE)
            rec.update(bytes=len(newbody), sha256=hashlib.sha256(newbody).hexdigest())
            # The control on disk must also be updated to avoid testing only source-drift.
            (fixture / 'queue_outside_target_row.json').write_text(json.dumps(c) + '\n')
            return lambda:qsource.write_bytes(old)
        case('queue_outside_target_row', mutate_body=lambda c:change_queue(c, qsource.read_bytes() + b'\nforeign fixture edit\n'))
        case('utf8_invalid_selected_body', mutate_body=lambda c:candidate_change(c, 'RESULT.md', b'\xff'))
        case('nul_selected_body', mutate_body=lambda c:candidate_change(c, 'RESULT.md', b'a\0b'))
        case('unknown_binary_path', mutate_body=lambda c:candidate_change(c, 'unknown.pdf', b'fixture unknown binary\n'))
        case('wrong_published_pdf_bytes', mutate_body=lambda c:candidate_change(c, 'preprint/output/pdf/nonunique_nearest_stable_complex_quadratics.pdf', b'%PDF-fixture-invalid\n'))
        case('historical9_altered_despite_new_acceptance_pins', mutate_body=lambda c:candidate_change(c, 'REVIEW_REQUEST.md', (candidate / 'REVIEW_REQUEST.md').read_bytes() + b'\nALTERED\n'))
        case('acceptance_wrong_schema', mutate_body=lambda c:acceptance_change(c, lambda ac:ac.__setitem__('schema', 'unbound-fixture')))
        case('acceptance_false', mutate_body=lambda c:acceptance_change(c, lambda ac:ac.__setitem__('accepted_for_native_preparation', False)))
        case('acceptance_missing_target_body', mutate_body=lambda c:acceptance_change(c, lambda ac:ac['target_bodies'].pop()))
        def source_symlink(c):
            f = candidate / 'RESULT.md'
            saved = f.read_bytes()
            f.unlink()
            f.symlink_to(candidate / 'STATUS.md')
            def restore():
                f.unlink()
                f.write_bytes(saved)
            return restore
        case('selected_source_symlink', mutate_body=source_symlink)
        def extra_inventory(c):
            f = candidate / 'unselected_fixture.md'
            f.write_bytes(b'unselected fixture\n')
            return lambda:f.unlink()
        case('unselected_candidate_file', mutate_body=extra_inventory)
    finally:
        module.importlib.util.spec_from_file_location = real_spec
        module.subprocess.run = real_run
    result = dict(schema='pr263-adversarial-initial-guard-tests-v3', UTC=dt.datetime.now(dt.timezone.utc).isoformat(),
                  helper=pin(PREP), harness_source=pin(Path(__file__)), exact_source_executed=True,
                  instrumentation=['W/ROOT redirect to review-owned synthetic fixture.',
                                   'Pinned-reader import provides independent stub; stop at first read-tree.',
                                   'Private Git configuration subprocess is stubbed.'],
                  provider_calls=0, primary_Git_metadata_access=0, remote_operations=0, actual_Git_operations=0,
                  fixture_not_root_candidate=True, passed=sum(t['passed'] for t in tests), test_count=len(tests), tests=tests,
                  remaining_gap='Actual selected bodies/raw tree/commit and native provider execution/readback require separate audit.',
                  review_completion_estimate_percent=45)
    (OWN / 'ADVERSARIAL_GUARD_TEST_RESULTS_V03.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
