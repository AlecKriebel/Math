"""Additional offline controls; no API boundary uses a real network connection."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'native_transport_author'
sys.path.insert(0, str(AUTHOR))
spec = importlib.util.spec_from_file_location('supplied_native_tests', AUTHOR / 'test_native_transport.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)
s.nt.HERE = HERE
nt, zenodo = s.nt, s.zenodo
results = []


def kit_case(fn):
    case = s.NativeTransportTests()
    case.setUp()
    try:
        return fn(case)
    finally:
        case.tearDown()


def legitimate_oai(case):
    case.stage()
    case.client.backend.record_change = lambda x: x['pids'].update(
        oai={'identifier': 'oai:zenodo.org:23356540', 'provider': 'oai'}
    ) if case.client.backend.published else None
    try:
        case.run_kit('publish')
        raise RuntimeError('Expected rejection of legitimate OAI PID')
    except zenodo.DepositError as exc:
        results.append({'name': 'legitimate_oai_postpublication', 'error': str(exc),
                        'remote_model_published': case.client.backend.published,
                        'receipt_saved': 'publication' in zenodo.read_json(case.place),
                        'publish_posts': sum(u.endswith('/actions/publish') for m, u in case.writes())})


def source_swap(case):
    # Use private file copies so no reviewed publication input is modified.
    copies = []
    for f in s.FILES:
        p = case.folder / f['name']
        shutil.copyfile(f['path'], p)
        copies.append({**f, 'path': p})
    case.client.files = {f['name']: f for f in copies}
    original_wire = case.client._wire_request
    swapped = {'done': False}
    target = copies[0]
    def honest_entry(name, completed=False):
        item = s.Backend.entry(case.client.backend, name, completed)
        if completed:
            data = case.client.backend.content[name]
            item.update(size=len(data), checksum='md5:' + hashlib.md5(data).hexdigest())
        return item
    case.client.backend.entry = honest_entry
    def wire(method, url, payload=None, file=None, accept='application/json'):
        if method == 'PUT' and not swapped['done']:
            data = target['path'].read_bytes()
            target['path'].write_bytes(bytes([data[0] ^ 1]) + data[1:])
            swapped['done'] = True
        return original_wire(method, url, payload=payload, file=file, accept=accept)
    case.client._wire_request = wire
    try:
        case.client.upload(nt.DRAFT + '/files', target)
        raise RuntimeError('Expected committed checksum rejection')
    except zenodo.DepositError as exc:
        observed = case.client.backend.content[target['name']]
        results.append({'name': 'source_path_swap_after_validation', 'error': str(exc),
                        'expected_sha256': target['sha256'],
                        'wire_bytes_sha256': hashlib.sha256(observed).hexdigest(),
                        'unpinned_content_was_uploaded': hashlib.sha256(observed).hexdigest() != target['sha256'],
                        'commit_post_was_sent': any(u.endswith('/commit') for m, u in case.writes()),
                        'published': case.client.backend.published})


def process_restart(case):
    case.fault('content', s.FILES[0]['name'], when='before')
    try:
        case.run_kit('stage')
    except zenodo.DepositError:
        pass
    before = list(case.writes())
    fresh = s.FakeClient(case.folder, backend=case.client.backend)
    try:
        case.run_kit('stage', client=fresh)
    except zenodo.DepositError:
        pass
    results.append({'name': 'new_client_process_restart_no_repeat',
                    'writes_before': len(before), 'writes_after': len(case.writes()),
                    'no_repeat': case.writes() == before})


def lock_and_sync(case):
    lock = case.folder / 'lock'
    with nt.runner_lock(lock):
        try:
            with nt.runner_lock(lock):
                raise RuntimeError('Expected second lock to fail')
        except zenodo.DepositError:
            locked_out = True
    with patch.object(zenodo.os, 'fsync', wraps=zenodo.os.fsync) as sync:
        case.stage()
        sync_count = sync.call_count
    results.append({'name': 'lock_and_journal_sync', 'second_lock_rejected': locked_out,
                    'lock_mode': oct(lock.stat().st_mode & 0o777),
                    'journal_mode': oct((case.folder/'journal.json').stat().st_mode & 0o777),
                    'fsync_calls_for_six_mutations': sync_count})


def acknowledgments(case):
    keys = ('initialize:' + s.FILES[0]['name'], 'content:' + s.FILES[0]['name'],
            'commit:' + s.FILES[0]['name'], 'publish')
    rejects = 0
    for key in keys:
        for response in (None, [], {}, {'errors': ['transfer failed']}, {'id': '999'}):
            try:
                case.client.validate_write_response(key, response)
            except zenodo.DepositError:
                rejects += 1
            else:
                raise RuntimeError('Malformed ack accepted')
    results.append({'name': 'malformed_acknowledgment_matrix', 'rejected': rejects})


def pid_fidelity(case):
    baseline = deepcopy(s.FIXTURE)
    rejected = []
    for pid in ({'identifier': nt.DOI, 'provider': 'external'},
                {'identifier': nt.DOI, 'provider': 'datacite', 'client': 'wrong'},
                {'identifier': '10.5281/zenodo.23356539', 'provider': 'datacite'},
                {'identifier': nt.DOI, 'provider': 'datacite', 'extra': 'hidden'}):
        case.client.backend.record_change = lambda x, p=pid: x.update(pids={'doi': p})
        try:
            case.client.get(nt.RECORD_ID)
        except zenodo.DepositError:
            rejected.append(pid)
        else:
            raise RuntimeError('Hostile PID accepted')
    results.append({'name': 'doi_provider_client_extra_fidelity', 'rejected': len(rejected), 'writes': len(case.writes())})


for fn in (legitimate_oai, source_swap, process_restart, lock_and_sync, acknowledgments, pid_fidelity):
    kit_case(fn)
out = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'optimization': sys.flags.optimize,
       'remote_mutations': 0, 'controls': results}
destination = HERE / ('ADVERSARIAL_OPTIMIZED.json' if sys.flags.optimize else 'ADVERSARIAL_NORMAL.json')
destination.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
