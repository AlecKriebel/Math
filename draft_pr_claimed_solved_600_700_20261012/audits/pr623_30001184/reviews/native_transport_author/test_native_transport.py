"""Offline lifecycle/failure probes. Every network boundary is replaced."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import os
import stat
import sys
import types

from unittest.mock import patch, MagicMock

import native_transport as nt
zenodo = nt.zenodo

CAPTURED = nt.capture_inputs()
METADATA, FILES = CAPTURED.metadata, CAPTURED.files
FIXTURE = json.loads((nt.HERE / 'native_shape.json').read_text())


class Backend:
    def __init__(self):
        self.entries = {}
        self.content = {}
        self.published = False
        self.calls = []
        self.faults = {}
        self.pending_downloads = False
        self.record_change = None
        self.list_change = None
        self.read_failure = False

    def entry(self, name, completed=False):
        root = (nt.REC if self.published else nt.DRAFT) + '/files/' + name
        item = {'key': name, 'status': 'completed' if completed else 'pending', 'metadata': None,
                'links': {'self': root, 'content': root + '/content'}}
        if not self.published:
            item['links']['commit'] = root + '/commit'
        if completed:
            file = next(f for f in FILES if f['name'] == name)
            data = self.content[name]
            item.update(size=len(data), checksum='md5:' + hashlib.md5(data).hexdigest())
        return item

    def record(self):
        result = deepcopy(FIXTURE)
        if self.published:
            result.update(is_draft=False, is_published=True, status='published')
            result['links'].update(self=nt.REC, self_html=nt.BASE + f'/records/{nt.RECORD_ID}', files=nt.REC + '/files')
            result['pids'] = {'doi': {'identifier': nt.DOI, 'provider': 'datacite', 'client': 'datacite'},
                              'oai': {'identifier': nt.OAI, 'provider': 'oai'}}
        result['files'].update(count=len(self.entries), entries={name: {} for name in self.entries},
                               total_bytes=sum(item.get('size') if type(item.get('size')) in (int,float) else 0 for item in self.entries.values()))
        if self.record_change:
            self.record_change(result)
        return result

    def collection(self):
        entries = []
        for name, item in self.entries.items():
            copy = deepcopy(item)
            if self.published:
                root = nt.REC + '/files/' + name
                copy['links'] = {'self': root, 'content': root + '/content'}
            entries.append(copy)
        result = {'enabled': True, 'entries': entries, 'default_preview': None, 'order': [],
                  'links': {'self': (nt.REC if self.published else nt.DRAFT) + '/files'}}
        if self.list_change:
            self.list_change(result)
        return result


class FakeClient(nt.NativeOwnDraftClient):
    def __init__(self, folder, backend=None, allow_writes=True):
        self.backend = backend or Backend()
        super().__init__('offline-test-token', METADATA, FILES, allow_writes=allow_writes,
                         journal_path=folder / 'journal.json')

    def _wire_request(self, method, url, payload=None, file=None, accept='application/json'):
        b = self.backend
        b.calls.append((method, url))
        fault = b.faults.pop((method, url), None)
        if fault == 'before':
            raise zenodo.DepositError('Simulated lost response/no remote action')
        if method == 'GET':
            if b.read_failure:
                raise zenodo.DepositError('Simulated failed GET')
            if url == nt.DRAFT:
                if b.published:
                    raise zenodo.DepositError('HTTP 404 draft removed')
                return b.record()
            if url == nt.REC:
                if not b.published:
                    raise zenodo.DepositError('HTTP 404 record unpublished')
                return b.record()
            if url in (nt.DRAFT + '/files', nt.REC + '/files'):
                return b.collection()
            raise AssertionError(('Unexpected offline GET', url))
        if method == 'POST' and url == nt.DRAFT + '/files':
            nt.require(isinstance(payload, list) and len(payload) == 1 and set(payload[0]) == {'key'}, 'Offline initialization payload shape')
            name = payload[0]['key']
            nt.require(name not in b.entries, 'Duplicate initialization reached wire')
            b.entries[name] = b.entry(name)
            result = b.collection()
        elif method == 'PUT' and url.endswith('/content'):
            name = url.split('/')[-2]
            nt.require(name not in b.content, 'Repeated content PUT reached wire')
            b.content[name] = file.read_bytes()
            if fault == 'partial':
                b.content[name] = b.content[name][:7]
            result = deepcopy(b.entries[name])
        elif method == 'POST' and url.endswith('/commit'):
            name = url.split('/')[-2]
            nt.require(len(b.content[name]) == nt.FILE_PINS[name][0], 'Offline byte count differs')
            b.entries[name] = b.entry(name, True)
            result = deepcopy(b.entries[name])
        elif method == 'POST' and url == nt.DRAFT + '/actions/publish':
            nt.require(len(b.entries) == 2 and all(item['status'] == 'completed' for item in b.entries.values()), 'Offline publication incomplete')
            b.published = True
            result = b.record()
        else:
            raise AssertionError(('Unexpected offline mutation', method, url))
        if fault in {'after', 'partial'}:
            raise zenodo.DepositError('Simulated lost mutating response')
        if fault == 'errors':
            result['errors'] = ['Simulated transfer error']
        return result

    def _wire_digest(self, url, expected_size):
        b = self.backend
        b.calls.append(('GET_BINARY', url))
        name = url.split('/')[-2]
        if b.entries[name]['status'] == 'pending' and not b.pending_downloads:
            raise zenodo.DepositError('Pending content download unavailable')
        content = b.content.get(name, b'')
        nt.require(len(content) == expected_size, 'Offline remote content wrong length')
        return hashlib.sha256(content).hexdigest()


class NativeTransportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=nt.HERE / 'tmp')
        self.folder = Path(self.temp.name)
        self.client = FakeClient(self.folder)
        self.state_patch = patch.object(zenodo, 'STATE_DIR', self.folder / 'kit-state')
        self.state_patch.start()
        self.doi_patch = patch.object(zenodo, 'doi_status', return_value={'status': 'resolved', 'http_status': 200,
                                  'url': 'https://doi.org/' + nt.DOI, 'resolved_url': nt.BASE + f'/records/{nt.RECORD_ID}'})
        self.doi_patch.start()
        self.place = zenodo.state_path(nt.MANIFEST, 'production')
        zenodo.save_state(self.place, {'manifest': str(nt.MANIFEST), 'environment': 'production', 'id': nt.RECORD_ID})

    def tearDown(self):
        self.doi_patch.stop()
        self.state_patch.stop()
        self.temp.cleanup()

    def run_kit(self, command, client=None):
        return nt.run_captured_kit(argparse.Namespace(command=command, manifest=nt.MANIFEST, sandbox=False,
                          confirm_id=nt.RECORD_ID, check_doi=True), CAPTURED, client=client or self.client)

    def writes(self):
        return [(method, url) for method, url in self.client.backend.calls if method in {'POST', 'PUT', 'DELETE'}]

    def stage(self):
        result = self.run_kit('stage')
        self.assertEqual(result['state'], 'ready_to_publish')
        self.assertEqual(len(result['files']), 2)
        self.assertNotIn('publication', zenodo.read_json(self.place))
        return result

    def fault(self, operation, name=None, when='after'):
        if operation == 'initialize': method, url = 'POST', nt.DRAFT + '/files'
        elif operation == 'content': method, url = 'PUT', nt.DRAFT + '/files/' + name + '/content'
        elif operation == 'commit': method, url = 'POST', nt.DRAFT + '/files/' + name + '/commit'
        else: method, url = 'POST', nt.DRAFT + '/actions/publish'
        self.client.backend.faults[(method, url)] = when

    def test_exact_projection_and_readonly_get(self):
        self.assertEqual(nt.legacy_projection(FIXTURE), METADATA)
        result = self.client.get(nt.RECORD_ID)
        self.assertFalse(result['submitted'])
        self.assertEqual(result['files'], [])
        self.assertEqual(self.writes(), [])

    def test_native_drift_rich_metadata_and_state_fail_closed(self):
        mutations = [
            lambda x: x.update(id='23356541'),
            lambda x: x.update(is_published=True),
            lambda x: x.update(is_draft='true'),
            lambda x: x.update(status='published'),
            lambda x: x['metadata'].update(publisher='Other'),
            lambda x: x['metadata'].update(languages=[{'id':'eng'}]),
            lambda x: x['metadata']['creators'][0]['affiliations'].append({'name':'Other'}),
            lambda x: x['metadata']['subjects'][0].update(id='controlled'),
            lambda x: x['metadata']['rights'].append({'id':'other'}),
            lambda x: x['metadata']['related_identifiers'][0].update(extra='other'),
            lambda x: x.update(custom_fields={'extra':'x'}),
            lambda x: x['access'].update(files='restricted'),
            lambda x: x['access']['embargo'].update(active=True),
            lambda x: x['access']['embargo'].update(active=0),
            lambda x: x['pids'].update(other={'identifier':'x'}),
            lambda x: x['links'].update(self='https://other.example/api/records/23356540/draft'),
            lambda x: x['links'].update(files=nt.DRAFT + '/files?bypass=1'),
            lambda x: x['files'].update(count=1),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.client.backend.record_change = mutation
                with self.assertRaises(zenodo.DepositError): self.client.get(nt.RECORD_ID)
        self.assertEqual(self.writes(), [])

    def test_only_known_id_endpoints_no_create_update_delete(self):
        for method, url in [('POST', nt.BASE + '/api/records'), ('DELETE', nt.DRAFT),
                            ('PUT', nt.DRAFT), ('POST', nt.REC + '/versions'),
                            ('POST', nt.BASE + '/api/records/23356541/draft/files'),
                            ('GET', nt.BASE + '/api/user/records'),
                            ('GET', nt.DRAFT + '/files?x=1')]:
            with self.assertRaises(zenodo.DepositError): self.client.request(method, url)
        for function, arg in [(self.client.get, 23356541), (self.client.get, True),
                              (self.client.create, METADATA), (self.client.edit, nt.RECORD_ID),
                              (self.client.discard, nt.RECORD_ID)]:
            with self.assertRaises(zenodo.DepositError): function(arg)
        with self.assertRaises(zenodo.DepositError): self.client.update(nt.RECORD_ID, {**METADATA, 'version':'2.0'})
        self.assertEqual(self.writes(), [])

    def test_disabled_writes(self):
        self.client.allow_writes = False
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        self.assertEqual(self.writes(), [])

    def test_no_saved_state_never_creates(self):
        self.place.unlink()
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        self.assertEqual(self.writes(), [])

    def test_acknowledged_upload_no_precommit_download_needed(self):
        self.stage()
        self.assertEqual([method for method, _ in self.writes()], ['POST','PUT','POST'] * 2)
        self.assertFalse(any(method == 'PUT' and url == nt.DRAFT for method,url in self.writes()))
        self.run_kit('inspect')
        before = list(self.writes())
        self.stage()
        self.assertEqual(self.writes(), before)

    def test_lost_init_after_registration_recovers_once(self):
        self.fault('initialize')
        self.stage()
        self.assertEqual(sum(url == nt.DRAFT + '/files' for _,url in self.writes()), 2)

    def test_lost_init_no_registration_never_retries(self):
        self.fault('initialize', when='before')
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        before = list(self.writes())
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        self.assertEqual(self.writes(), before)
        self.assertEqual(self.client.journal['operations']['initialize:' + FILES[0]['name']]['phase'], 'attempted')

    def test_lost_content_complete_readable_recovers_once(self):
        self.client.backend.pending_downloads = True
        self.fault('content', FILES[0]['name'])
        self.stage()
        self.assertEqual(sum(method == 'PUT' for method,_ in self.writes()), 2)

    def test_lost_content_pending_unreadable_stops_and_restart_no_put(self):
        self.fault('content', FILES[0]['name'])
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        before = list(self.writes())
        restarted = FakeClient(self.folder, self.client.backend)
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage', restarted)
        self.assertEqual(self.writes(), before)
        self.assertFalse(any(url.endswith('/commit') for _,url in self.writes()))

    def test_lost_partial_content_rejects_no_commit_no_repeat(self):
        self.client.backend.pending_downloads = True
        self.fault('content', FILES[0]['name'], 'partial')
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        before = list(self.writes())
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        self.assertEqual(self.writes(), before)
        self.assertFalse(any(url.endswith('/commit') for _,url in self.writes()))

    def test_200_content_transfer_errors_do_not_acknowledge_or_commit(self):
        self.fault('content', FILES[0]['name'], 'errors')
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        self.assertEqual(self.client.journal['operations']['content:' + FILES[0]['name']]['phase'], 'attempted')
        self.assertFalse(any(url.endswith('/commit') for _,url in self.writes()))

    def test_lost_commit_after_completion_recovers_once(self):
        self.fault('commit', FILES[0]['name'])
        self.stage()
        self.assertEqual(sum(url.endswith('/commit') for _,url in self.writes()), 2)

    def test_lost_commit_no_completion_never_retries(self):
        self.fault('commit', FILES[0]['name'], 'before')
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        before = list(self.writes())
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        self.assertEqual(self.writes(), before)

    def test_foreign_pending_upload_stops(self):
        name = FILES[0]['name']
        self.client.backend.entries[name] = self.client.backend.entry(name)
        with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        self.assertEqual(self.writes(), [])

    def test_extra_duplicate_names_status_and_links_stop(self):
        changes = [lambda x:x['entries'].append({'key':'foreign.pdf'}),
                   lambda x:x['entries'].append(deepcopy(x['entries'][0])),
                   lambda x:x['entries'][0].update(status='failed'),
                   lambda x:x['entries'][0]['links'].update(content='https://other.example/content'),
                   lambda x:x['entries'][0]['links'].update(commit=nt.REC+'/files/other/commit'),
                   lambda x:x['entries'][0].update(metadata={'user':'custom'}),
                   lambda x:x.update(enabled=False)]
        self.stage()
        before = list(self.writes())
        for change in changes:
            with self.subTest(change=change):
                self.client.backend.list_change = change
                with self.assertRaises(zenodo.DepositError): self.run_kit('inspect')
        self.assertEqual(self.writes(), before)

    def test_committed_size_md5_and_sha256_guards(self):
        self.stage()
        name = FILES[0]['name']
        original = deepcopy(self.client.backend.entries[name])
        for delta in ({'size':1}, {'size':str(FILES[0]['size'])}, {'checksum':'md5:'+'0'*32},
                      {'checksum':'sha256:'+FILES[0]['sha256']}):
            self.client.backend.entries[name] = {**original, **delta}
            with self.assertRaises(zenodo.DepositError): self.run_kit('inspect')
        self.client.backend.entries[name] = original
        data = self.client.backend.content[name]
        self.client.backend.content[name] = b'x' + data[1:]
        with self.assertRaises(zenodo.DepositError): self.run_kit('inspect')
        self.assertEqual(len(self.writes()), 6)

    def test_publish_final_native_readback_kit_receipt(self):
        self.stage()
        result = self.run_kit('publish')
        self.assertEqual(result['state'], 'published')
        self.assertEqual(result['id'], nt.RECORD_ID)
        self.assertEqual(result['environment'], 'production')
        self.assertEqual(result['doi'], nt.DOI)
        self.assertEqual(result['doi_resolution']['http_status'], 200)
        self.assertTrue(result['receipt_saved'])
        self.assertEqual(zenodo.read_json(self.place)['publication'], result)
        before = list(self.writes())
        again = self.run_kit('publish')
        self.assertTrue(again['already_published'])
        self.assertEqual(self.writes(), before)

    def test_lost_publish_response_recovers_no_second_post(self):
        self.stage()
        self.fault('publish')
        result = self.run_kit('publish')
        self.assertTrue(result['recovered_after_publish_error'])
        self.assertEqual(result['state'], 'published')
        self.run_kit('publish')
        self.assertEqual(sum(url.endswith('/actions/publish') for _,url in self.writes()), 1)

    def test_lost_publish_no_publication_never_retries(self):
        self.stage()
        self.fault('publish', when='before')
        with self.assertRaises(zenodo.DepositError): self.run_kit('publish')
        before = list(self.writes())
        with self.assertRaises(zenodo.DepositError): self.run_kit('publish')
        self.assertEqual(self.writes(), before)
        self.assertNotIn('publication', zenodo.read_json(self.place))

    def test_wrong_published_doi_no_confirmed_receipt(self):
        self.stage()
        self.client.backend.record_change = lambda x:x['pids'].update(doi={'identifier':'10.5281/zenodo.23356539','provider':'datacite'}) if self.client.backend.published else None
        with self.assertRaises(zenodo.DepositError): self.run_kit('publish')
        self.assertNotIn('publication', zenodo.read_json(self.place))

    def test_journal_persistence_failure_prevents_mutation(self):
        with patch.object(nt, 'durable_journal_save', side_effect=OSError('storage unavailable')):
            with self.assertRaises(zenodo.DepositError): self.run_kit('stage')
        self.assertEqual(self.writes(), [])

    def test_publication_receipt_failure_is_not_fake_unpublication(self):
        self.stage()
        original = zenodo.save_state
        def fail_receipt(place, state):
            if 'publication' in state: raise OSError('receipt storage unavailable')
            return original(place,state)
        with patch.object(zenodo, 'save_state', side_effect=fail_receipt):
            result = self.run_kit('publish')
        self.assertEqual(result['state'], 'published')
        self.assertFalse(result['receipt_saved'])
        self.assertTrue(self.client.backend.published)


    def test_binary_reader_exact_bounds_status_and_connection_failure(self):
        name = FILES[0]['name']
        data = FILES[0]['path'].read_bytes()
        url = nt.DRAFT + '/files/' + name + '/content'
        for status, body in ((200, data), (302, data), (200, data + b'x'), (200, data[:7])):
            with self.subTest(status=status, size=len(body)):
                connection = MagicMock()
                response = MagicMock(status=status)
                response.read.side_effect = [body, b'']
                connection.getresponse.return_value = response
                with patch.object(nt.http.client, 'HTTPSConnection', return_value=connection):
                    if status == 200 and len(body) == len(data):
                        digest = nt.NativeOwnDraftClient._wire_digest(self.client, url, len(data))
                        self.assertEqual(digest, FILES[0]['sha256'])
                    else:
                        with self.assertRaises(zenodo.DepositError):
                            nt.NativeOwnDraftClient._wire_digest(self.client, url, len(data))
                connection.close.assert_called_once()
                self.assertEqual(connection.request.call_args.args[:2], ('GET', url.removeprefix(nt.BASE)))
                self.assertEqual(connection.request.call_args.kwargs['headers']['Accept'], '*/*')
        connection = MagicMock()
        connection.getresponse.side_effect = OSError('lost response')
        with patch.object(nt.http.client, 'HTTPSConnection', return_value=connection):
            with self.assertRaises(zenodo.DepositError):
                nt.NativeOwnDraftClient._wire_digest(self.client, url, len(data))
        connection.close.assert_called_once()

    def test_direct_allowed_mutation_cannot_bypass_journal(self):
        for method,url,payload in (('POST',nt.DRAFT+'/files',[{'key':FILES[0]['name']}]),
                                   ('POST',nt.DRAFT+'/actions/publish',None)):
            with self.assertRaises(zenodo.DepositError):
                self.client.request(method,url,payload=payload)
        self.assertEqual(self.writes(), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
