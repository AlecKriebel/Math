"""F1/F2/F3/O1 regression controls, all files/network substitutes stay local."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import types
import unittest
import run_native_transport as bootstrap
from unittest.mock import MagicMock, patch

import test_native_transport as original

nt, zenodo = original.nt, original.zenodo


class RepairTests(unittest.TestCase):
    def setUp(self):
        self.case = original.NativeTransportTests(methodName='runTest')
        self.case.setUp()
        self.folder, self.client = self.case.folder, self.case.client

    def tearDown(self):
        self.case.tearDown()

    def private_captured_inputs(self):
        root = self.folder / 'input-copies'
        root.mkdir()
        manifest = root / 'zenodo-deposit.json'
        manifest.write_bytes(original.CAPTURED.manifest.read_bytes())
        for entry in original.FILES:
            (root / entry['name']).write_bytes(entry['path'].read_bytes())
        return root, nt.capture_inputs(manifest)

    def private_client(self, captured):
        client = original.FakeClient(self.folder)
        client.files = {entry['name']: entry for entry in captured.files}
        return client

    def test_f1_fresh_adapter_ignores_preloaded_unreviewed_zenodo(self):
        stale = types.ModuleType('zenodo')
        stale.__file__ = str(nt.KIT_PATH)
        stale.run = lambda *args, **kwargs: {'unreviewed_loaded_code_executed': True}
        stale.digest = lambda *args: nt.KIT_SHA
        # Compile the actual current adapter under a new identity, exactly as a
        # fresh launch does; do not modify the global kit or original module.
        source = nt.HERE.joinpath('native_transport.py').read_bytes()
        adapter = types.ModuleType('fresh_adapter_f1_probe')
        adapter.__file__ = str(nt.HERE / 'native_transport.py')
        with patch.dict(sys.modules, {'zenodo': stale}):
            exec(compile(source, adapter.__file__, 'exec', dont_inherit=True), adapter.__dict__)
            captured = adapter.capture_inputs()
            args = types.SimpleNamespace(command='check', manifest=captured.manifest, sandbox=False)
            result = adapter.run_captured_kit(args, captured)
            self.assertIs(sys.modules['zenodo'], stale)
            self.assertIsNot(adapter.zenodo, stale)
        self.assertNotIn('unreviewed_loaded_code_executed', result)
        self.assertEqual(result['files'][0]['sha256'], original.FILES[0]['sha256'])
        self.assertEqual(adapter.zenodo.__verified_source_sha256__, nt.KIT_SHA)
        self.assertEqual(adapter.zenodo.__file__, str(nt.KIT_PATH))
        self.assertEqual(adapter.zenodo.ROOT, nt.ROOT)
        self.assertTrue(adapter.zenodo.__name__.startswith('_pr623_verified_zenodo_'))
        self.assertNotEqual(adapter.zenodo.__name__, nt.zenodo.__name__)

    def test_f1_bad_kit_snapshot_rejected_before_top_level_execution(self):
        source_path = self.folder / 'bad-kit.py'
        marker = self.folder / 'unreviewed-executed'
        source_path.write_text('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("bad")\n')
        with self.assertRaises(nt.BootstrapError): nt.load_checked_kit(source_path)
        self.assertFalse(marker.exists())
        self.assertEqual(self.case.writes(), [])

    def test_f1_single_kit_capture_survives_path_swap_after_read(self):
        source_path = self.folder / 'kit-source.py'
        source = nt.KIT_PATH.read_bytes()
        source_path.write_bytes(source)
        read = Path.read_bytes
        calls = []
        def swapping_read(path):
            data = read(path)
            if path == source_path:
                calls.append(path)
                path.write_bytes(b'raise RuntimeError("unreviewed replacement executed")\n')
            return data
        with patch.object(Path, 'read_bytes', new=swapping_read):
            checked = nt.load_checked_kit(source_path)
        self.assertEqual(len(calls), 1)
        self.assertEqual(checked.__verified_source_sha256__, nt.KIT_SHA)
        self.assertEqual(checked.ROOT, nt.ROOT)
        result = checked.run(types.SimpleNamespace(command='check', manifest=original.CAPTURED.manifest, sandbox=False))
        self.assertEqual(result['title'], original.METADATA['title'])
        self.assertNotEqual(hashlib.sha256(source_path.read_bytes()).hexdigest(), nt.KIT_SHA)

    def test_f1_manifest_and_payloads_read_once_then_path_drift_is_irrelevant(self):
        root, first = self.private_captured_inputs()
        reads = []
        original_read = Path.read_bytes
        def tracked_read(path):
            reads.append(path)
            return original_read(path)
        with patch.object(Path, 'read_bytes', new=tracked_read):
            captured = nt.capture_inputs(root / 'zenodo-deposit.json')
        self.assertEqual(len(reads), 3)
        self.assertEqual(len(set(reads)), 3)
        # No later kit manifest/loading/checksum read touches these disk paths.
        (root / 'zenodo-deposit.json').write_text('{"metadata": {"title":"changed"}, "files":[]}')
        for entry in captured.files:
            (root / entry['name']).write_bytes(b'changed')
        args = types.SimpleNamespace(command='check', manifest=nt.MANIFEST, sandbox=False)
        with patch.object(Path, 'read_bytes', side_effect=RuntimeError('Second mutable source read')):
            result = nt.run_captured_kit(args, captured)
        self.assertEqual(result['title'], original.METADATA['title'])
        self.assertEqual(result['files'], self.case.run_kit('check')['files'])
        self.assertEqual(str(args.manifest), str(root / 'zenodo-deposit.json'))

    def test_f1_changed_manifest_rejected_before_payload_reads(self):
        root, _ = self.private_captured_inputs()
        path = root / 'zenodo-deposit.json'
        data = path.read_bytes()
        path.write_bytes(data.replace(b'counterexample', b'counterexamplf', 1))
        reads = []
        original_read = Path.read_bytes
        def tracked(path):
            reads.append(path)
            return original_read(path)
        with patch.object(Path, 'read_bytes', new=tracked):
            with self.assertRaises(zenodo.DepositError): nt.capture_inputs(path)
        self.assertEqual(reads, [path])
        self.assertEqual(self.case.writes(), [])

    def test_f2_legitimate_automatic_oai_receipts_normal_and_lost_response(self):
        self.case.stage()
        result = self.case.run_kit('publish')
        self.assertTrue(result['receipt_saved'])
        self.assertEqual(result['doi'], nt.DOI)
        self.assertEqual(self.client.backend.record()['pids']['oai'], {'identifier': nt.OAI, 'provider':'oai'})
        self.assertEqual(zenodo.read_json(self.case.place)['publication'], result)
        self.assertEqual(self.case.run_kit('inspect')['state'], 'published')
        self.assertEqual(sum(url.endswith('/actions/publish') for _,url in self.case.writes()), 1)
        # Existing original lost-publication test now runs over the same complete
        # DOI+OAI map; this independent fresh client also checks receipt recovery.
        before = list(self.case.writes())
        restarted = original.FakeClient(self.folder, self.client.backend)
        again = self.case.run_kit('publish', restarted)
        self.assertTrue(again['already_published'])
        self.assertEqual(self.case.writes(), before)

    def test_f2_unknown_malformed_doi_oai_schemes_providers_clients_rejected(self):
        self.case.stage()
        self.client.backend.published = True
        exact = self.client.backend.record()['pids']
        malformed = [
            {'doi': exact['doi']},
            {'oai': exact['oai']},
            {**exact, 'ark': {'identifier':'x','provider':'ark'}},
            {**exact, 'oai': {'identifier':'oai:zenodo.org:23356539','provider':'oai'}},
            {**exact, 'oai': {'identifier':nt.OAI,'provider':'external'}},
            {**exact, 'oai': {'identifier':nt.OAI,'provider':'oai','client':'oai'}},
            {**exact, 'oai': {'identifier':nt.OAI,'provider':'oai','extra':'hidden'}},
            {**exact, 'oai': {'identifier':nt.OAI}},
            {**exact, 'oai': None},
            {**exact, 'doi': {'identifier':nt.DOI,'provider':'datacite','client':None}},
            {**exact, 'doi': {'identifier':nt.DOI,'provider':'datacite','client':'other'}},
            {**exact, 'doi': {'identifier':nt.DOI,'provider':'external'}},
            {**exact, 'doi': {'identifier':nt.DOI,'provider':'datacite','extra':'hidden'}},
        ]
        for pids in malformed:
            with self.subTest(pids=pids):
                self.client.backend.record_change = lambda x,p=pids:x.update(pids=p)
                with self.assertRaises(zenodo.DepositError): self.case.run_kit('inspect')
        self.assertNotIn('publication', zenodo.read_json(self.case.place))
        self.assertEqual(sum(url.endswith('/actions/publish') for _,url in self.case.writes()), 0)

    def test_f3_changed_payload_capture_is_rejected_no_mutation(self):
        root, _ = self.private_captured_inputs()
        path = root / original.FILES[0]['name']
        data = path.read_bytes()
        path.write_bytes(bytes([data[0] ^ 1]) + data[1:])
        with self.assertRaises(zenodo.DepositError): nt.capture_inputs(root / 'zenodo-deposit.json')
        self.assertEqual(self.case.writes(), [])

    def test_f3_payload_modification_during_capture_is_rejected(self):
        root, _ = self.private_captured_inputs()
        target = root / original.FILES[0]['name']
        read = Path.read_bytes
        def mixed_read(path):
            data = read(path)
            if path == target:
                path.write_bytes(bytes([data[0] ^ 1]) + data[1:])
                return data[:10] + bytes([data[10] ^ 1]) + data[11:]
            return data
        with patch.object(Path,'read_bytes',new=mixed_read):
            with self.assertRaises(zenodo.DepositError): nt.capture_inputs(root / 'zenodo-deposit.json')
        self.assertEqual(self.case.writes(), [])

    def test_f3_source_path_replaced_after_validation_sends_only_snapshot(self):
        root, captured = self.private_captured_inputs()
        client = self.private_client(captured)
        entry = captured.files[0]
        source = root / entry['name']
        original_wire = client._wire_request
        observed = {'swapped':False}
        def swapping_wire(method,url,payload=None,file=None,accept='application/json'):
            if method == 'PUT' and not observed['swapped']:
                replacement = root / 'replacement'
                data = source.read_bytes()
                replacement.write_bytes(bytes([data[0] ^ 1]) + data[1:])
                os.replace(replacement,source)
                observed['swapped'] = True
            return original_wire(method,url,payload=payload,file=file,accept=accept)
        client._wire_request = swapping_wire
        item = client.upload(nt.DRAFT+'/files',entry)
        self.assertTrue(observed['swapped'])
        self.assertEqual(item['status'],'completed')
        self.assertEqual(hashlib.sha256(client.backend.content[entry['name']]).hexdigest(),entry['sha256'])
        self.assertNotEqual(hashlib.sha256(source.read_bytes()).hexdigest(),entry['sha256'])
        self.assertEqual(sum(method == 'PUT' for method,_ in client.backend.calls),1)
        self.assertFalse(client.backend.published)

    def test_f3_actual_kit_stream_is_immune_to_inplace_write_and_path_replacement(self):
        root,captured = self.private_captured_inputs()
        client = self.private_client(captured)
        entry = captured.files[0]
        source = root / entry['name']
        original_wire = client._wire_request
        sent,headers = [],{}
        connection = MagicMock()
        connection.putheader.side_effect = lambda key,value:headers.update({key:value})
        def send(block):
            sent.append(block)
            if len(sent) == 1:
                # Replace the pathname, then modify its new inode while the
                # unchanged kit is still reading/sending later snapshot chunks.
                replacement = root / 'replacement-during-stream'
                data = source.read_bytes()
                replacement.write_bytes(bytes([data[0] ^ 1]) + data[1:])
                os.replace(replacement,source)
                with source.open('r+b') as mutable:
                    mutable.seek(2048)
                    mutable.write(b'RACED')
        connection.send.side_effect = send
        response = MagicMock(status=200)
        def wire(method,url,payload=None,file=None,accept='application/json'):
            if method != 'PUT':
                return original_wire(method,url,payload=payload,file=file,accept=accept)
            response.read.return_value = json.dumps(client.backend.entries[entry['name']]).encode()
            connection.getresponse.return_value = response
            with patch.object(nt.http.client,'HTTPSConnection',return_value=connection),patch.object(zenodo,'CHUNK',1024):
                result = nt.NativeOwnDraftClient._wire_request(client,method,url,payload=payload,file=file,accept=accept)
            client.backend.calls.append((method,url))
            client.backend.content[entry['name']] = b''.join(sent)
            return result
        client._wire_request = wire
        item = client.upload(nt.DRAFT+'/files',entry)
        transmitted = b''.join(sent)
        self.assertGreater(len(sent),2)
        self.assertEqual(len(transmitted),entry['size'])
        self.assertEqual(hashlib.sha256(transmitted).hexdigest(),entry['sha256'])
        self.assertEqual(hashlib.md5(transmitted).hexdigest(),entry['md5'])
        self.assertEqual(headers['Content-Length'],str(entry['size']))
        self.assertEqual(headers['Content-Type'],'application/octet-stream')
        self.assertNotEqual(hashlib.sha256(source.read_bytes()).hexdigest(),entry['sha256'])
        self.assertEqual(item['status'],'completed')
        connection.close.assert_called_once()
        self.assertFalse(client.backend.published)

    def test_f3_raw_path_payload_and_snapshot_mutation_rejected(self):
        root,captured = self.private_captured_inputs()
        files = [{**f,'path':root/f['name']} for f in captured.files]
        with self.assertRaises(zenodo.DepositError):
            nt.NativeOwnDraftClient('offline-test-token',captured.metadata,files,journal_path=self.folder/'new-journal.json')
        payload = captured.files[0]['path']
        with self.assertRaises(AttributeError): payload._data = b'replacement'
        reader = payload.open('rb')
        self.assertFalse(hasattr(reader,'write'))
        self.assertEqual(reader.read(5),payload.read_bytes()[:5])
        self.assertEqual(self.case.writes(), [])

    def test_o1_file_and_directory_fsync_precede_each_mutation_dispatch(self):
        trace = []
        actual_fsync,actual_replace = nt.os.fsync,nt.os.replace
        wire = self.client._wire_request
        def sync(fd):
            trace.append('dir_sync' if stat.S_ISDIR(os.fstat(fd).st_mode) else 'file_sync')
            return actual_fsync(fd)
        def replace(source,target):
            trace.append('replace')
            return actual_replace(source,target)
        def checked_wire(method,url,payload=None,file=None,accept='application/json'):
            if method != 'GET':
                saved = zenodo.read_json(self.client.journal_path)
                # Each wire action sees a saved attempted marker and the most
                # recent atomic write has both file and directory barriers.
                self.assertEqual(trace[-4:],['file_sync','replace','dir_sync','dir_sync'])
                self.assertTrue(any(value['phase']=='attempted' for value in saved['operations'].values()))
                self.assertEqual(self.client.journal_path.stat().st_mode & 0o777,0o600)
                trace.append('dispatch')
            return wire(method,url,payload=payload,file=file,accept=accept)
        self.client._wire_request = checked_wire
        with patch.object(nt.os,'fsync',side_effect=sync),patch.object(nt.os,'replace',side_effect=replace):
            self.case.stage()
        self.assertEqual(trace.count('dispatch'),6)
        self.assertGreaterEqual(trace.count('file_sync'),6)
        self.assertGreaterEqual(trace.count('dir_sync'),6)

    def test_o1_file_or_directory_sync_failure_blocks_first_dispatch_and_later_writes(self):
        actual = nt.os.fsync
        for fail_on in (1,2,3):
            with self.subTest(fail_on=fail_on):
                folder = self.folder / ('sync-failure-'+str(fail_on))
                folder.mkdir()
                client = original.FakeClient(folder)
                counter = [0]
                def sync(fd):
                    counter[0] += 1
                    if counter[0] == fail_on: raise OSError('modeled sync failure')
                    return actual(fd)
                with patch.object(nt.os,'fsync',side_effect=sync):
                    with self.assertRaises(zenodo.DepositError): client.upload(nt.DRAFT+'/files',original.FILES[0])
                self.assertTrue(client._storage_failed)
                self.assertFalse(any(m in ('POST','PUT') for m,_ in client.backend.calls))
                with self.assertRaises(zenodo.DepositError): client.upload(nt.DRAFT+'/files',original.FILES[0])
                self.assertFalse(any(m in ('POST','PUT') for m,_ in client.backend.calls))

    def test_o1_sync_failure_after_acknowledgment_is_process_fail_stop(self):
        actual = nt.os.fsync
        counter = [0]
        def sync(fd):
            counter[0] += 1
            if counter[0] == 4: raise OSError('response-state fsync failed')
            return actual(fd)
        with patch.object(nt.os,'fsync',side_effect=sync):
            with self.assertRaises(zenodo.DepositError): self.case.run_kit('stage')
        self.assertEqual(len(self.case.writes()),1)
        self.assertTrue(self.client._storage_failed)
        before = list(self.case.writes())
        with self.assertRaises(zenodo.DepositError): self.case.run_kit('stage')
        self.assertEqual(self.case.writes(),before)

    def test_o1_new_journal_directories_are_synced_and_replace_error_stops(self):
        path = self.folder/'new'/'nested'/'intent.json'
        actual = nt.os.fsync
        synced_dirs = []
        def sync(fd):
            if stat.S_ISDIR(os.fstat(fd).st_mode): synced_dirs.append(os.fstat(fd).st_ino)
            return actual(fd)
        with patch.object(nt.os,'fsync',side_effect=sync): nt.durable_journal_save(path,{'test':True})
        self.assertGreaterEqual(len(synced_dirs),5)
        self.assertEqual(zenodo.read_json(path),{'test':True})
        with patch.object(nt.os,'replace',side_effect=OSError('modeled replace failure')):
            with self.assertRaises(zenodo.DepositError): self.case.run_kit('stage')
        self.assertEqual(self.case.writes(),[])
        self.assertTrue(self.client._storage_failed)


    def test_f1_bootstrap_uses_pinned_adapter_snapshot_and_ignores_stale_module(self):
        stale = types.ModuleType('native_transport')
        stale.main = lambda: 'unreviewed implementation'
        with patch.dict(sys.modules,{'native_transport':stale}):
            adapter = bootstrap.load_reviewed_adapter()
            self.assertIs(sys.modules['native_transport'],stale)
            self.assertIsNot(adapter,stale)
        self.assertEqual(adapter.__verified_source_sha256__,bootstrap.ADAPTER_SHA256)
        self.assertEqual(adapter.zenodo.__verified_source_sha256__,nt.KIT_SHA)
        captured = adapter.capture_inputs()
        result = adapter.run_captured_kit(types.SimpleNamespace(command='check',manifest=nt.MANIFEST,sandbox=False),captured)
        self.assertEqual(result['files'][0]['sha256'],original.FILES[0]['sha256'])

    def test_f1_bootstrap_rejects_bad_adapter_before_side_effect(self):
        source = self.folder/'bad-adapter.py'
        marker = self.folder/'bad-adapter-executed'
        source.write_text('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("bad")\n')
        with self.assertRaises(RuntimeError): bootstrap.load_reviewed_adapter(source)
        self.assertFalse(marker.exists())
        self.assertEqual(self.case.writes(),[])

    def test_f1_bootstrap_single_read_survives_adapter_path_replacement(self):
        source = self.folder/'adapter-copy.py'
        source.write_bytes(bootstrap.ADAPTER.read_bytes())
        read = Path.read_bytes
        counter = [0]
        def swapped(path):
            data = read(path)
            if path == source:
                counter[0] += 1
                path.write_bytes(b'raise RuntimeError("raced replacement executed")\n')
            return data
        with patch.object(Path,'read_bytes',new=swapped):
            adapter = bootstrap.load_reviewed_adapter(source)
        self.assertEqual(counter[0],1)
        self.assertEqual(adapter.__verified_source_sha256__,bootstrap.ADAPTER_SHA256)
        self.assertEqual(adapter.zenodo.ROOT,nt.ROOT)

    def test_f1_bound_kit_dispatch_refuses_other_workflows_and_environment(self):
        for command,sandbox in (('metadata',False),('update-metadata',False),('publish-metadata',False),('check',True)):
            args = types.SimpleNamespace(command=command,manifest=nt.MANIFEST,sandbox=sandbox)
            with self.assertRaises(zenodo.DepositError): nt.run_captured_kit(args,original.CAPTURED,self.client)
        self.assertEqual(self.case.writes(),[])


    def test_f1_adapter_direct_script_entry_refuses_dispatch(self):
        module = types.ModuleType('__main__')
        module.__file__ = str(nt.HERE/'native_transport.py')
        with self.assertRaises(SystemExit) as refused:
            exec(compile(Path(module.__file__).read_bytes(),module.__file__,'exec',dont_inherit=True),module.__dict__)
        self.assertIn('byte-snapshot bootstrap',str(refused.exception))
        self.assertEqual(self.case.writes(),[])


    def test_f4_download_negotiation_accepts_wildcard_not_upload_media_type(self):
        entry = original.FILES[0]
        data = entry['path'].read_bytes()
        url = nt.DRAFT+'/files/'+entry['name']+'/content'
        connection = MagicMock()
        response = MagicMock()
        observed = []
        def negotiate(method,target,headers):
            observed.append((method,target,headers['Accept']))
            if headers['Accept'] == '*/*':
                response.status = 200
                response.read.side_effect = [data,b'']
            else:
                # Reproduce the deployed content endpoint's 406 response for
                # Accept: application/octet-stream, without any real request.
                response.status = 406
                response.read.side_effect = [b'{"status":406,"message":"Not acceptable"}',b'']
        connection.request.side_effect = negotiate
        connection.getresponse.return_value = response
        with patch.object(nt.http.client,'HTTPSConnection',return_value=connection):
            digest = nt.NativeOwnDraftClient._wire_digest(self.client,url,entry['size'])
        self.assertEqual(digest,entry['sha256'])
        self.assertEqual(observed,[('GET',url.removeprefix(nt.BASE),'*/*')])
        connection.close.assert_called_once()
        # The actual kit streaming positive control separately asserts that
        # content PUT remains Content-Type: application/octet-stream.


if __name__ == '__main__':
    unittest.main(verbosity=2)
