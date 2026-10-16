#!/usr/bin/env python3
"""Exercise exact prepare code guards in an isolated review-owned test directory.

No provider calls or primary Git metadata access. Early-guard tests stop at the
reader entry point; they do not claim a resulting tree/commit has passed.
"""
import base64
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
import types

sys.dont_write_bytecode = True
R = Path('/Users/alec/Documents/Math')
W = R / 'draft_pr_descending_audit_20261002/audits/pr263_30000170/initial_review_20261011'
OWN = W / 'native_integration_adversarial_review'
PREP = W / 'integration_preparation/prepare_native_reconciliation.py'
EXPECTED = '18b4f2dafe04776a58505a8972bb4f18d71e0e40186efe08249ca728bddf884a'
TARGET = 'attempts/30000170'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
MAIN = 'd8540c93d2b763c3c287e2c493dec7019d8bd41b'
MAIN_TREE = '25aefa44bfb8bcc9475eba326661b7b3d7206003'
AUTHOR = 'c4eff3253932a504f8e558c8b5f5b1b5e155de0f'

def pin(path):
    b = path.read_bytes()
    return {'path': str(path), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

class ReachedReader(Exception):
    pass

class StubReader:
    @staticmethod
    def git_oid(kind, body):
        return hashlib.sha1(kind.encode() + b' ' + str(len(body)).encode() + b'\0' + body).hexdigest()

    @staticmethod
    def private_environment(output):
        raise ReachedReader('Initial selected-source guards reached private reader')

def run():
    now = dt.datetime.now(dt.timezone.utc)
    source = PREP.read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED, 'Root helper changed: stop before tests'
    fixtures = OWN / 'private_instrumented_tests'
    assert not fixtures.exists(), 'Harness is single-run; do not overwrite prior test evidence'
    fixtures.mkdir()
    acceptance = fixtures / 'acceptance.json'
    acceptance.write_text(json.dumps({'accepted_for_native_preparation': True,
                                      'deliberately_unrelated_fixture_only': True}) + '\n')
    original = json.loads((W / 'original_submission/MANIFEST_WITH_MODES.json').read_bytes())
    entries = []
    for old in original:
        if not old['path'].startswith(TARGET + '/'):
            continue
        body = Path(old['local']).read_bytes()
        assert hashlib.sha256(body).hexdigest() == old['sha256']
        dest = fixtures / 'sources' / old['path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        entries.append(dict(path=old['path'], source=str(dest), bytes=len(body),
                            sha256=hashlib.sha256(body).hexdigest()))
    for rel in ['output/pdf/nonunique_nearest_stable_complex_quadratics.pdf',
                'output/nonunique_nearest_stable_complex_quadratics_verification.zip']:
        body = (W / 'preprint_package_v03' / rel).read_bytes()
        dest = fixtures / 'sources' / TARGET / 'preprint' / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        entries.append(dict(path=TARGET + '/preprint/' + rel, source=str(dest),
                            bytes=len(body), sha256=hashlib.sha256(body).hexdigest()))
    base = W / 'integration_preparation/FRESH_MAIN_QUEUE.md'
    basebody = base.read_bytes()
    # This synthetic patch is solely for source-guard testing; it is not Root's queue candidate.
    qsource = fixtures / 'sources' / QUEUE
    qsource.parent.mkdir(parents=True, exist_ok=True)
    qsource.write_bytes(basebody)
    entries.append(dict(path=QUEUE, source=str(qsource), bytes=len(basebody),
                        sha256=hashlib.sha256(basebody).hexdigest()))
    control = dict(main=MAIN, author=AUTHOR, candidate_acceptance=pin(acceptance),
                   files=entries, base_queue=pin(base),
                   queue_before_base64='', queue_after_base64='')
    module = types.ModuleType('adversarial_exact_prepare')
    module.__file__ = str(PREP)
    exec(compile(source, str(PREP), 'exec'), module.__dict__)
    module.ROOT = fixtures
    real_spec = module.importlib.util.spec_from_file_location
    class Loader:
        @staticmethod
        def create_module(spec):
            return None
        @staticmethod
        def exec_module(mod):
            mod.git_oid = StubReader.git_oid
            mod.private_environment = StubReader.private_environment
    from importlib.machinery import ModuleSpec
    module.importlib.util.spec_from_file_location = lambda name, path: ModuleSpec(name, Loader())
    tests = []
    def case(name, changes=None, expectation='rejected', raw=None):
        c = copy.deepcopy(control)
        if changes:
            changes(c)
        cpath = fixtures / (name + '.json')
        cpath.write_text(raw(c) if raw else json.dumps(c) + '\n')
        previous = sys.argv
        sys.argv = [str(PREP), '--main', c['main'], '--selection', str(cpath),
                    '--date', now.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    '--output', str(fixtures / (name + '_output'))]
        try:
            module.main()
            observed, reason = 'unexpected_full_success', ''
        except ReachedReader as exc:
            observed, reason = 'reached_private_reader', str(exc)
        except (ValueError, UnicodeError, KeyError, TypeError) as exc:
            observed, reason = 'rejected', str(exc)
        finally:
            sys.argv = previous
        tests.append(dict(name=name, expected=expectation, observed=observed,
                          passed=(observed == expectation), reason=reason))
    try:
        case('positive_originals_and_exact_binary_fixture', expectation='reached_private_reader')
        case('foreign_destination', lambda c: c['files'].__setitem__(0, dict(c['files'][0], path='attempts/OTHER/x.md')))
        case('wrong_unsolved_target_placement', lambda c: c['files'].__setitem__(0, dict(c['files'][0], path='unsolved_math_prioritization/attempts/30000170/x.md')))
        case('path_traversal', lambda c: c['files'].__setitem__(0, dict(c['files'][0], path=TARGET + '/../x.md')))
        case('doubled_slash', lambda c: c['files'].__setitem__(0, dict(c['files'][0], path=TARGET + '//x.md')))
        case('duplicate_destination', lambda c: c['files'].append(copy.deepcopy(c['files'][0])))
        case('missing_original17', lambda c: c['files'].pop(0))
        case('incorrect_sha256', lambda c: c['files'].__setitem__(0, dict(c['files'][0], sha256='0' * 64)))
        case('incorrect_byte_count', lambda c: c['files'].__setitem__(0, dict(c['files'][0], bytes=c['files'][0]['bytes'] + 1)))
        case('binary_disguised_unknown_pdf', lambda c: c['files'].__setitem__(0, dict(c['files'][0], path=TARGET + '/unknown.pdf')))
        case('only_one_binary', lambda c: c['files'].__setitem__(slice(17, 19), c['files'][17:18]))
        # Sources with corrected pins are needed to test content/mode bypasses rather than drift rejection.
        def extra(c, name, body, **fields):
            f = fixtures / 'sources' / name
            f.write_bytes(body)
            c['files'].append(dict(path=TARGET + '/' + name, source=str(f), bytes=len(body),
                                   sha256=hashlib.sha256(body).hexdigest(), **fields))
        case('invalid_utf8', lambda c: extra(c, 'invalid_utf8.md', b'\xff'))
        case('nul_in_utf8', lambda c: extra(c, 'nul.md', b'a\0b'))
        def historic(c):
            record = next(e for e in c['files'] if e['path'] == TARGET + '/REVIEW_REQUEST.md')
            f = fixtures / 'sources' / 'altered_historical.md'
            f.write_bytes(Path(record['source']).read_bytes() + b'\nALTERED\n')
            record.update(source=str(f), bytes=f.stat().st_size,
                          sha256=hashlib.sha256(f.read_bytes()).hexdigest())
        case('historical9_body_changed', historic)
        symlink = fixtures / 'sources' / 'link.md'
        symlink.symlink_to(Path(entries[0]['source']))
        case('source_symlink', lambda c: c['files'].__setitem__(0, dict(c['files'][0], source=str(symlink))))
        case('wrong_literal_author', lambda c: c.__setitem__('author', '0' * 40))
        case('unbound_acceptance_fixture', expectation='reached_private_reader')
        case('tree_oid_used_as_main', lambda c: c.__setitem__('main', MAIN_TREE), expectation='reached_private_reader')
        case('ignored_manifest_mode', lambda c: c['files'][0].__setitem__('mode', '100755'), expectation='reached_private_reader')
        case('private_text_destination_allowed_by_prefix',
             lambda c: extra(c, 'private_observation.md', b'fixture only\n'), expectation='reached_private_reader')
        case('duplicate_json_author_key', expectation='reached_private_reader',
             raw=lambda c: '{"author":"' + '0' * 40 + '",' + json.dumps(c)[1:] + '\n')
    finally:
        module.importlib.util.spec_from_file_location = real_spec
    result = dict(schema='pr263-adversarial-selected-guard-tests-v1',
                  UTC=dt.datetime.now(dt.timezone.utc).isoformat(),
                  helper=pin(PREP), checked_helper_sha256=EXPECTED,
                  exact_source_executed=True,
                  injected_changes=['Only ROOT redirects output/control to review-owned fixtures.',
                                    'Reader module is stubbed; stops before Git after initial guards.'],
                  provider_calls=0, primary_Git_metadata_access=0, remote_operations=0,
                  fixture_not_root_candidate=True,
                  passed=sum(t['passed'] for t in tests), test_count=len(tests), tests=tests,
                  remaining_gap='These tests stop before Git; exact Root-selected candidate and prepared raw objects still require independent audit.',
                  review_completion_estimate_percent=30)
    (OWN / 'ADVERSARIAL_GUARD_TEST_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(passed=result['passed'], test_count=result['test_count'], tests=tests), indent=2))

if __name__ == '__main__':
    run()
