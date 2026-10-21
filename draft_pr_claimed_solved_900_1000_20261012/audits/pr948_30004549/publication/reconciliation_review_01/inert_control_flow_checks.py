"""Inert tests of authenticated publication control flow; no service/Git calls.

Only selected, unmodified AST function/class definitions are compiled. Every
outside dependency used by those definitions is an in-memory test double.
These checks do not replay or independently observe the original failed process.
"""
import argparse
import ast
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_claimed_solved_900_1000_20261012'
OUT = Path(__file__).resolve().parent
CORE = P / 'accept_pr948.py'
KIT = ROOT / 'zenodo_deposit_tool/zenodo.py'
EXPECTED = {
    CORE: '3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823',
    KIT: 'a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca',
}
raws = {}
for path, pin in EXPECTED.items():
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == pin
    raws[path] = raw


def selected(path, names, namespace):
    tree = ast.parse(raws[path], filename=str(path))
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    module = ast.Module(body=nodes, type_ignores=[])
    exec(compile(module, str(path), 'exec', dont_inherit=True), namespace)
    return namespace


def need(value, label):
    if not value:
        raise RuntimeError('PR948 guard: ' + label)


checks = []


def check(label, value):
    if not value:
        raise AssertionError(label)
    checks.append({'check': label, 'passed': True})


def refused(call, text):
    try:
        call()
    except RuntimeError as error:
        return text in str(error)
    return False


# Extract the unchanged core zenodo function. The only simulated failure is
# the second merged_gate call, corresponding to guard() at actual source 865.
events = []
metadata = {'title': 'fixture title'}
files = [{'name': 'fixture', 'size': 1, 'sha256': 'f' * 64}]
accepted = {'freeze_sha256': 'fixture-freeze'}
freeze = {'files': {'zenodo-deposit.json': {'sha256': 'fixture-descriptor'}}}
runtime = OUT / 'in-memory-runtime-manifest.json'
calls = {'merged_gate': 0, 'kit_publish': 0, 'client': 0, 'token': 0}


def merged_gate(*unused):
    calls['merged_gate'] += 1
    events.append('merged_gate_' + str(calls['merged_gate']))
    if calls['merged_gate'] == 2:
        raise RuntimeError('PR948 guard: live merged PR changed across readback')
    return {'merge_commit': 'fixture-merge'}


def kit_run(args, **unused):
    events.append('kit_run_' + args.command)
    if args.command == 'publish':
        calls['kit_publish'] += 1
        raise AssertionError('publish command must not be reached')
    assert args.command == 'check'
    return {'environment': 'production', 'title': metadata['title'], 'files': files}


def token(*unused):
    calls['token'] += 1
    raise AssertionError('token must not be read')


def client(*unused):
    calls['client'] += 1
    raise AssertionError('client must not be constructed')


saved = []
namespace = {
    'accepted_package': lambda context: (accepted, freeze),
    'merged_gate': merged_gate,
    'descriptor_check': lambda value: ({'metadata': metadata}, files),
    'captured_kit': lambda context: {
        'load_manifest': lambda path: (metadata, files), 'run': kit_run,
        'local_state': lambda path, env: (OUT / 'memory-only-state', {'id': 23422055}),
        'token_for': token, 'ZenodoClient': client,
    },
    'runtime_upload_copy': lambda value: runtime,
    'need': need, 'exact': lambda a, b: a == b,
    'argparse': argparse, 'TITLE': metadata['title'],
    'save': lambda path, data, **kwargs: saved.append((path.name, copy.deepcopy(data))),
    'load': lambda path: {'id': 23422055},
    'validate_zenodo_receipt': lambda *args: 23422055,
    'W': OUT / 'memory-only-workflow', 'ROOT': ROOT,
    'utc_now': lambda: 'inert-clock', 'PR': 948, 'HEAD': 'fixture-head',
    'KIT': 'zenodo_deposit_tool/zenodo.py',
    'accepted_review_check': lambda *args: events.append('accepted_review_check'),
    'GuardedZenodoClient': client,
}
selected(CORE, {'zenodo'}, namespace)
context = {'inventory_sha256': 'fixture-inventory', 'inventory': {'files': {
    'zenodo_deposit_tool/zenodo.py': {'sha256': EXPECTED[KIT]}}}}
check('actual zenodo function propagates simulated line865 guard exception', refused(
    lambda: namespace['zenodo'](argparse.Namespace(action='publish'), context),
    'live merged PR changed across readback'))
check('publish intent is saved before that guard failure', any(n == 'ZENODO_PUBLISH_INTENT.json' for n, _ in saved))
check('pre-client failure produces no inner-try failure receipt', not any(n == 'ZENODO_PUBLISH_FAILURE.json' for n, _ in saved))
check('only earlier kit command is inert check', [e for e in events if e.startswith('kit_run_')] == ['kit_run_check'])
check('client construction and token retrieval remain unreachable', calls['client'] == 0 and calls['token'] == 0)
check('publish-command kit.run remains unreachable', calls['kit_publish'] == 0)

# Test the exact guarded client class without any network-capable object.
class Remote:
    def __init__(self, submitted=False, fail=False):
        self.submitted = submitted
        self.fail = fail
        self.posts = 0
        self.gets = 0

    def get(self, ident):
        self.gets += 1
        return {'id': ident, 'submitted': self.submitted, 'metadata': {'notes': 'same'}}

    def publish(self, ident):
        self.posts += 1
        if self.fail:
            raise RuntimeError('inert uncertain transport')
        self.submitted = True
        return {'id': ident, 'submitted': True}


guards = []
ns = selected(CORE, {'GuardedZenodoClient'}, {
    'need': need, 'exact': lambda a, b: a == b,
    'normalize_notes': lambda value, meta: (value, False),
    'sha': lambda b: hashlib.sha256(b).hexdigest(),
})
kit_validators = {'validate_record': lambda d, i: need(d['id'] == i, 'ID'),
                  'verify': lambda *args: []}


def guarded(remote, action='publish'):
    return ns['GuardedZenodoClient'](remote, kit_validators, {'notes': 'same'}, [],
                                     lambda: guards.append('guard'), action, 23422055)


remote = Remote()
c = guarded(remote)
check('different ID is rejected before any GET or POST', refused(lambda: c.publish(23422056), 'one exact-ID') and remote.posts == remote.gets == 0)
c.publish(23422055)
check('fresh unpublished exact ID permits one POST', remote.posts == 1 and c.published == 1)
check('a second publish on same guarded instance is refused', refused(lambda: c.publish(23422055), 'one exact-ID') and remote.posts == 1)
remote = Remote(submitted=True)
c = guarded(remote)
c.publish(23422055)
check('fresh submitted exact ID returns without POST', remote.posts == 0 and c.published == 0)
remote = Remote(fail=True)
c = guarded(remote)
check('uncertain publish exception is preserved', refused(lambda: c.publish(23422055), 'inert uncertain'))
check('publish counter increments before uncertain call', c.published == remote.posts == 1)
check('uncertain POST cannot be repeated on same client', refused(lambda: c.publish(23422055), 'one exact-ID') and remote.posts == 1)
remote = Remote()
c = guarded(remote, 'inspect')
check('inspect client cannot publish', refused(lambda: c.publish(23422055), 'one exact-ID') and remote.posts == 0)

# Test unmodified kit.run with all local I/O and service operations stubbed.
class DepositError(Exception):
    pass


class Client:
    def __init__(self, submitted=False, uncertain=False):
        self.submitted = submitted
        self.uncertain = uncertain
        self.posts = 0
        self.gets = 0

    def get(self, ident):
        self.gets += 1
        return {'id': ident, 'submitted': self.submitted, 'links': {'html': 'fixture'}}

    def publish(self, ident):
        self.posts += 1
        if self.uncertain:
            raise DepositError('inert uncertain POST')
        self.submitted = True


ns = selected(KIT, {'run'}, {
    'argparse': argparse, 'ZenodoClient': Client, 'DepositError': DepositError,
    'load_manifest': lambda path: (metadata, files),
    'local_state': lambda *args: (OUT / 'memory-only-state', {'id': 23422055}),
    'validate_record': lambda d, i: need(d['id'] == i and type(d['submitted']) is bool, 'ID/state'),
    'verify': lambda *args: [],
    'published_summary': lambda summary, deposit, *unused: {**summary, 'state': 'published'},
})


def run(command, c, ident=23422055):
    return ns['run'](argparse.Namespace(command=command, manifest=runtime, sandbox=False,
                                        confirm_id=ident, check_doi=False), c)


c = Client()
check('kit check returns before client or saved state use', run('check', c)['files'] == files and c.posts == c.gets == 0)
c = Client()
check('kit inspect unpublished performs GET and no POST', run('inspect', c)['state'] == 'ready_to_publish' and c.posts == 0 and c.gets == 1)
c = Client(submitted=True)
check('kit inspect published performs no POST', run('inspect', c)['state'] == 'published' and c.posts == 0)
c = Client(submitted=True)
check('kit publish already submitted performs no POST', run('publish', c)['state'] == 'published' and c.posts == 0)
c = Client()
try:
    run('publish', c, 23422056)
except DepositError:
    check('kit wrong confirm ID rejected without POST', c.posts == 0)
else:
    raise AssertionError('wrong confirm ID accepted')
c = Client(uncertain=True)
try:
    run('publish', c)
except DepositError:
    check('kit uncertain unpublished outcome performs one POST then GET without retry', c.posts == 1 and c.gets == 2)
else:
    raise AssertionError('uncertain unpublished outcome accepted')

result = {'schema': 'pr948-focused-publish-reconciliation-inert-controls-v1',
          'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
          'network_calls': 0, 'git_calls': 0, 'authoritative_file_writes': 0,
          'actual_source_pins': {str(k.relative_to(ROOT)): v for k, v in EXPECTED.items()},
          'checks': checks, 'simulated_failure_events': events,
          'limitations': 'Inert source-function checks; no independent replay or witness of original failed invocation, no live account-wide history audit.'}
(OUT / 'INERT_CONTROL_FLOW_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'checks': len(checks), 'network_calls': 0, 'git_calls': 0}))
