"""Independent synthetic fault injection. No live publication or Sheets writes."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sp = importlib.util.spec_from_file_location('base_admin_tests', PARENT / 'test_publication_admin.py')
b = importlib.util.module_from_spec(sp); sp.loader.exec_module(b)
m = b.m


class AdversarialTests(b.AdminTests):
    def setUp(self):
        own_private = m.PRIVATE / 'publication_admin_software_adversary0'
        with patch.object(m, 'HERE', HERE), patch.object(m, 'PRIVATE', own_private):
            super().setUp()

    def count_op(self, service, operation):
        return sum(x[:2] == (service, operation) for x in self.api.calls)

    def test_create_fails_before_object_no_restaging(self):
        e = self.engine(); s, digest, content = e.load_spec(self.spec_path)
        self.api.fail = ('zenodo', 'POST /api/deposit/depositions')
        with self.assertRaises(m.Stop): e.stage(s, digest, content)
        j = json.loads(self.state.read_text())
        self.assertIsNone(self.api.metadata); self.assertIsNone(j['id'])
        self.assertEqual(j['phase'], 'unknown_write'); self.assertEqual(len(j['intents']), 1)
        before = len(self.writes())
        with self.assertRaises(m.Stop): self.engine().stage(s, digest, content)
        self.assertEqual(len(self.writes()), before)

    def test_upload_failure_before_apply_no_repeat(self):
        e = self.engine(); s, digest, content = e.load_spec(self.spec_path)
        op = 'PUT /api/files/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/preprint.pdf'
        self.api.fail = ('zenodo', op)
        with self.assertRaises(m.Stop): e.stage(s, digest, content)
        self.assertFalse(self.api.assets)
        self.assertEqual(self.count_op('zenodo', op), 1)
        j = json.loads(self.state.read_text()); self.assertEqual(j['phase'], 'unknown_write')
        self.api.fail = None; before = len(self.writes())
        result = self.engine().reconcile(digest)
        self.assertEqual(result['status'], 'draft_observed_publication_unconfirmed')
        with self.assertRaises(m.Stop): self.engine().stage(s, digest, content)
        self.assertEqual(len(self.writes()), before)

    def test_upload_applied_then_lost_response_no_repeat(self):
        e = self.engine(); s, digest, content = e.load_spec(self.spec_path)
        op = 'PUT /api/files/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/preprint.pdf'
        self.api.fail = ('zenodo', op); self.api.applied_before_error = True
        with self.assertRaises(m.Stop): e.stage(s, digest, content)
        self.assertEqual(set(self.api.assets), {'preprint.pdf'})
        self.api.fail = None; before = len(self.writes())
        self.assertEqual(self.engine().reconcile(digest)['status'], 'draft_observed_publication_unconfirmed')
        self.assertEqual(len(self.writes()), before)

    def test_metadata_put_failure_complete_assets_no_repeat(self):
        e = self.engine(); s, digest, content = e.load_spec(self.spec_path)
        op = f'PUT /api/deposit/depositions/{self.api.id}'
        self.api.fail = ('zenodo', op)
        with self.assertRaises(m.Stop): e.stage(s, digest, content)
        self.assertEqual(len(self.api.assets), 3); self.assertEqual(self.count_op('zenodo', op), 1)
        j = json.loads(self.state.read_text()); self.assertEqual(j['last_intent']['operation'], op)
        self.api.fail = None; before = len(self.writes())
        self.assertEqual(self.engine().reconcile(digest)['status'], 'draft_observed_publication_unconfirmed')
        self.assertEqual(len(self.writes()), before)

    def test_publish_failure_before_apply_consumes_intent(self):
        digest, native = self.staged()
        op = f'POST /api/deposit/depositions/{self.api.id}/actions/publish'
        self.api.fail = ('zenodo', op)
        with self.assertRaises(m.Stop): self.engine().publish(digest, self.api.id, native)
        self.assertFalse(self.api.submitted); self.assertTrue(json.loads(self.state.read_text())['publish_intent'])
        self.api.fail = None; before = len(self.writes())
        self.assertEqual(self.engine().reconcile(digest, native_approval=native)['status'], 'draft_observed_publication_unconfirmed')
        with self.assertRaises(m.Stop): self.engine().publish(digest, self.api.id, native)
        self.assertEqual(len(self.writes()), before)

    def test_unknown_publish_cannot_transition_into_tracker_mutation(self):
        digest, native = self.staged()
        op = f'POST /api/deposit/depositions/{self.api.id}/actions/publish'
        self.api.fail = ('zenodo', op); self.api.applied_before_error = True
        with self.assertRaises(m.Stop): self.engine().publish(digest, self.api.id, native)
        self.api.fail = None; self.assertTrue(self.api.submitted); before = len(self.writes())
        self.assertEqual(self.engine().reconcile(digest, native_approval=native)['status'], 'publication_verified_tracker_absent_observed')
        self.assertEqual(json.loads(self.state.read_text())['phase'], 'unknown_write')
        with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
        self.assertEqual(len(self.writes()), before)

    def test_append_failure_before_apply_consumes_intent(self):
        digest, native = self.published(); self.api.fail = ('sheet', 'append')
        with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
        self.assertEqual(len(self.api.rows), 1); self.assertTrue(json.loads(self.state.read_text())['append_intent'])
        self.api.fail = None; before = len(self.writes())
        self.assertEqual(self.engine().reconcile(digest, native_approval=native)['status'], 'publication_verified_tracker_absent_observed')
        with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
        self.assertEqual(len(self.writes()), before)

    def test_stale_draft_get_after_applied_unknown_publish_cannot_enable_retry(self):
        digest, native = self.staged()
        op = f'POST /api/deposit/depositions/{self.api.id}/actions/publish'
        self.api.fail = ('zenodo', op); self.api.applied_before_error = True
        with self.assertRaises(m.Stop): self.engine().publish(digest, self.api.id, native)
        self.assertTrue(self.api.submitted); self.api.fail = None
        original = self.api.deposit
        def stale_deposit():
            value = original(); value['submitted'] = False; return value
        before = len(self.writes())
        with patch.object(self.api, 'deposit', stale_deposit):
            self.assertEqual(self.engine().reconcile(digest, native_approval=native)['status'], 'draft_observed_publication_unconfirmed')
        with self.assertRaises(m.Stop): self.engine().publish(digest, self.api.id, native)
        self.assertEqual(len(self.writes()), before)

    def test_stale_doi_get_after_applied_unknown_append_cannot_enable_retry(self):
        digest, native = self.published(); self.api.fail = ('sheet', 'append'); self.api.applied_before_error = True
        with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
        self.assertEqual(len(self.api.rows), 2); self.api.fail = None
        original = self.api.sheet
        def stale_sheet(op, params, payload=None):
            value = original(op, params, payload)
            if op == 'batchGet' and params['ranges'] == [m.TAB + 'C2:C']:
                value['valueRanges'][0]['values'] = []
            return value
        before = len(self.writes())
        with patch.object(self.api, 'sheet', stale_sheet):
            result = self.engine().reconcile(digest, native_approval=native)
        self.assertEqual(result['status'], 'publication_verified_tracker_absent_observed')
        with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
        self.assertEqual(len(self.writes()), before)

    def test_intent_persistence_failure_sends_zero_requests(self):
        e = self.engine(); s, digest, content = e.load_spec(self.spec_path); original = m.save
        def failed_save(path, obj, exclusive=False):
            if Path(path) == self.state and obj.get('phase') == 'intent_recorded':
                raise OSError('synthetic storage unavailable')
            return original(path, obj, exclusive)
        with patch.object(m, 'save', failed_save):
            with self.assertRaises(OSError): e.stage(s, digest, content)
        self.assertFalse(self.writes()); self.assertEqual(json.loads(self.state.read_text())['phase'], 'prepared')

    def test_private_frozen_uploads_preserve_approved_bytes(self):
        e = self.engine(); s, digest, content = e.load_spec(self.spec_path)
        for f in s['assets']: Path(f['local_path']).write_bytes(b'changed after inspection')
        result = e.stage(s, digest, content)
        self.assertEqual(result['status'], 'staged_pending_native_acceptance')
        self.assertEqual(self.api.assets, content)

    def test_local_mutation_lock_excludes_concurrent_process_context(self):
        with patch.object(m, 'PRIVATE', self.priv):
            with m.mutation_lock():
                with self.assertRaises(m.Stop):
                    with m.mutation_lock(): pass
            with m.mutation_lock(): pass

    def test_native_generated_doi_chronology_access_and_file_shapes(self):
        digest, native = self.staged(); original = self.api.native_record
        changes = [
            lambda r: r['pids']['doi'].update(identifier='10.5281/zenodo.999999'),
            lambda r: r.update(created='2026-10-13T02:00:01Z', updated='2026-10-13T02:00:00Z'),
            lambda r: r.update(created='2026-10-13T02:00:00'),
            lambda r: r['access'].update(files='restricted'),
            lambda r: r['files']['entries']['preprint.pdf'].update(checksum='md5:'+'0'*32),
        ]
        for change in changes:
            def changed(change=change):
                r=original(); change(r); return r
            before = len(self.writes())
            with patch.object(self.api, 'native_record', changed):
                with self.assertRaises((m.Stop, m.z.DepositError)): self.engine().publish(digest, self.api.id, native)
            self.assertEqual(len(self.writes()), before)
        def timestamp_only():
            r=original(); r.update(created='2026-10-12T23:59:59Z', updated='2026-10-13T03:00:00+00:00'); return r
        with patch.object(self.api, 'native_record', timestamp_only):
            self.assertEqual(self.engine().publish(digest, self.api.id, native)['status'], 'published_verified')

    def test_generated_doi_url_is_normalized_to_canonical_url(self):
        digest, native = self.staged(); original_d = self.api.deposit; original_n = self.api.native_record
        def url_deposit():
            r=original_d()
            if self.api.submitted:
                r['doi'] = r['metadata']['doi'] = 'https://doi.org/10.5281/zenodo.' + str(self.api.id)
            return r
        def url_native():
            r=original_n(); r['pids']['doi']['identifier'] = 'https://doi.org/10.5281/zenodo.' + str(self.api.id); return r
        with patch.object(self.api, 'deposit', url_deposit), patch.object(self.api, 'native_record', url_native):
            result = self.engine().publish(digest, self.api.id, native)
        self.assertEqual(result['doi'], '10.5281/zenodo.' + str(self.api.id))
        self.assertEqual(result['doi_url'], 'https://doi.org/10.5281/zenodo.' + str(self.api.id))

    def test_extra_legacy_metadata_blocks_before_publish(self):
        digest, native = self.staged(); self.api.metadata['extra_editable'] = 'unapproved'
        before = len(self.writes())
        with self.assertRaises(m.Stop): self.engine().publish(digest, self.api.id, native)
        self.assertEqual(len(self.writes()), before)

    def test_private_native_snapshot_path_scope_before_read(self):
        digest, native = self.staged(); j = json.loads(self.state.read_text())
        original = Path(j['native_snapshot_path']); outside = self.tmp / 'outside_private_snapshot.json'
        outside.write_bytes(original.read_bytes()); j['native_snapshot_path'] = str(outside); m.save(self.state, j)
        before = len(self.writes())
        with self.assertRaises(m.Stop): self.engine().publish(digest, self.api.id, native)
        self.assertEqual(len(self.writes()), before)

    def test_dependency_executes_exact_pinned_bytes_without_reopening(self):
        p = self.tmp / 'fake_admin_dependency.py'; good=b'value = "verified"\n'; bad=b'value = "unverified"\n'; p.write_bytes(good)
        loader_spec = m.importlib.util.spec_from_file_location
        def changed_after_hash(name, path):
            if path == p: p.write_bytes(bad)
            return loader_spec(name, path)
        with patch.object(m.importlib.util, 'spec_from_file_location', changed_after_hash):
            result = m.module('race_fixture', p, m.sha(good))
        self.assertEqual(result.value, 'verified')
        self.assertEqual(p.read_bytes(), bad)

    def test_dependency_symlink_fifo_bad_hash_rejected(self):
        p = self.tmp / 'dependency.py'; raw=b'value=1\n'; p.write_bytes(raw)
        q = self.tmp / 'alias.py'; q.symlink_to(p)
        with self.assertRaises(RuntimeError): m.module('symlink_fixture', q, m.sha(raw))
        with self.assertRaises(RuntimeError): m.module('hash_fixture', p, '0'*64)
        q.unlink(); b.os.mkfifo(q)
        with self.assertRaises(RuntimeError): m.module('fifo_fixture', q, m.sha(raw))

    def test_state_evidence_paths_outside_private_rejected_before_creation(self):
        out = self.tmp / 'outside_evidence'
        with self.assertRaises(m.Stop): m.Admin(self.api, out, self.state)
        self.assertFalse(out.exists())
        inside = self.priv / 'fresh_custody'
        with self.assertRaises(m.Stop): m.Admin(self.api, inside, self.tmp / 'outside_state.json')
        self.assertFalse(inside.exists())



if __name__ == '__main__': unittest.main(verbosity=2)
