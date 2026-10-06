"""Offline fixtures only. No prepare call reaches Git, SQL, native assess or services."""
from pathlib import Path
import copy, csv, io, json, stat, tempfile, unittest, zipfile
import prepare_review_bundle as helper

class ScopeFixtures(unittest.TestCase):
    def rows(self):
        original = [{'id': helper.K, 'local_status': 'queued', 'turns_used': 0,
                     'eligible': True, 'rank': 124, 'ev': 0.22285411, 'review_hash': helper.REVIEW}]
        states = {helper.K: {'status': 'claimed_solved', 'turns_used': 2}}
        for i in range(48):
            key = 'fixture_' + str(i)
            original.append({'id': key, 'local_status': 'queued', 'turns_used': 0,
                             'eligible': True, 'rank': i + 125, 'ev': 0.123, 'review_hash': 'fixture_source'})
            states[key] = {'status': 'already_solved', 'turns_used': 1}
        regenerated = copy.deepcopy(original)
        for row in regenerated:
            row.update(local_status=states[row['id']]['status'], turns_used=states[row['id']]['turns_used'],
                       eligible=False, rank=None)
        return original, regenerated, states

    def test_48_synthetic_projection_drifts_are_preserved_exactly(self):
        old, regenerated, states = self.rows()
        result, drift = helper.scoped_catalog(old, regenerated, states)
        self.assertEqual(len(drift), 48)
        self.assertEqual(result[1:], old[1:])
        self.assertEqual(result[0], regenerated[0])
        self.assertEqual(old[0]['turns_used'], 0)

    def test_unrelated_score_drift_is_rejected(self):
        old, regenerated, states = self.rows()
        regenerated[1]['ev'] = 0.999
        with self.assertRaisesRegex(ValueError, 'source/score/hold'):
            helper.scoped_catalog(old, regenerated, states)

    def test_unrelated_state_drift_needs_explanation(self):
        old, regenerated, states = self.rows()
        regenerated[1]['turns_used'] = 2
        with self.assertRaisesRegex(ValueError, 'Unexplained'):
            helper.scoped_catalog(old, regenerated, states)

    def test_missing_or_duplicate_catalog_id_is_rejected(self):
        old, regenerated, states = self.rows()
        with self.assertRaises(ValueError):
            helper.scoped_catalog(old, regenerated[:-1], states)
        with self.assertRaises(ValueError):
            helper.scoped_catalog(old + [old[-1]], regenerated, states)

    def test_campaign_bytes_and_all_target_scores_are_preserved(self):
        target = '| 124 | 30003996 / OWR-16633-013 | Target | 0.2229 | 5.5 | 3 | 2018 | queued | 0/5 | private_chat |  |  |\r\n'
        other = '| 125 | fixture / OTHER | Other | 0.1234 | 6.0 | 2 | 2017 | blocked | 3/5 | x | keep this | old doi |\n'
        baseline = ('header\n' + target + other + 'footer without newline').encode()
        result = helper.campaign_overlay(baseline, 'Fixture note contains enough words to exercise only the overlay function.', '10.5281/zenodo.123456')
        before = baseline.decode().splitlines(keepends=True)
        after = result.decode().splitlines(keepends=True)
        self.assertEqual([before[i] for i in [0, 2, 3]], [after[i] for i in [0, 2, 3]])
        b, a = before[1].rstrip('\r\n').split('|'), after[1].rstrip('\r\n').split('|')
        for index in set(range(len(b))) - {8, 9, 11, 12}:
            self.assertEqual(b[index], a[index])
        self.assertEqual(a[8].strip(), 'claimed_solved')
        self.assertEqual(a[9].strip(), '2/5')
        self.assertTrue(after[1].endswith('\r\n'))
        with self.assertRaises(ValueError):
            helper.campaign_overlay(baseline.replace(b'0/5', b'1/5'), 'Fixture note with enough words to pass validation here.', '10.5281/zenodo.123456')

    def test_csv_overlay_preserves_other_rows(self):
        data = b'id,local_status,turns_used,eligible,rank,ev,holds,reasons\r\n30003996,queued,0,True,124,0.22285411,,old\r\nfixture,blocked,3,False,,0.123,keep hold,keep reason\r\n'
        target = {'id': helper.K, 'local_status': 'claimed_solved', 'turns_used': 2,
                  'eligible': False, 'rank': None, 'ev': 0.22285411, 'holds': [], 'reasons': ['old']}
        result = helper.csv_overlay(data, target)
        self.assertEqual(data.splitlines(keepends=True)[0], result.splitlines(keepends=True)[0])
        self.assertEqual(data.splitlines(keepends=True)[2], result.splitlines(keepends=True)[2])
        self.assertEqual(list(csv.DictReader(io.StringIO(result.decode())))[0]['turns_used'], '2')

    def test_csv_multiline_unrelated_fields_are_preserved(self):
        data = b'id,local_status,turns_used,eligible,rank,ev,holds,reasons\r\nfixture,blocked,3,False,,0.123,"keep\r\nthis hold",keep reason\r\n30003996,queued,0,True,124,0.22285411,,old\r\n'
        target = {'id': helper.K, 'local_status': 'claimed_solved', 'turns_used': 2,
                  'eligible': False, 'rank': None, 'ev': 0.22285411, 'holds': [], 'reasons': ['old']}
        result = helper.csv_overlay(data, target)
        self.assertEqual(data[:data.index(b'30003996')], result[:result.index(b'30003996')])
        rows = list(csv.DictReader(io.StringIO(result.decode(), newline='')))
        self.assertEqual(rows[0]['holds'], 'keep\r\nthis hold')
        self.assertEqual(rows[1]['turns_used'], '2')

    def gate(self, role='final'):
        return {'schema': 'pr108-publication-root-gate/v1', 'role': role, 'PR': 108, 'problem_id': 30003996,
                'original_head': helper.HEAD, 'review_hash': helper.REVIEW, 'statement_hash': helper.STATEMENT,
                'effective_proof_sha256': helper.PROOF, 'package_manifest_sha256': 'fixture_hash',
                'actual_root_review': True, 'clearance': True, 'original_budget': '2/5',
                'new_central_proof_search_turns': 0, 'UTC': '2026-10-06T05:21:27+00:00', 'exact_claim': 'Fixture claim',
                'checked_artifacts': [{'fixture': True}], 'mathematical_clearance': True, 'priority_clearance': True,
                'package_clearance': True, 'native_integration_clearance': True, 'pre_execution_adversary_clearance': True}

    def test_each_final_clearance_is_required(self):
        for field in ['mathematical_clearance', 'priority_clearance', 'package_clearance',
                      'native_integration_clearance', 'pre_execution_adversary_clearance']:
            gate = self.gate()
            gate[field] = False
            with self.assertRaises(ValueError):
                helper.validate_gate(gate, 'final', 'fixture_hash')

    def test_gate_identity_proof_and_fixture_rejections(self):
        for field, value in [('review_hash', 'wrong'), ('effective_proof_sha256', 'wrong'),
                             ('original_budget', '0/5'), ('fixture', True), ('simulated', True), ('dry_run', True)]:
            gate = self.gate()
            gate[field] = value
            with self.assertRaises(ValueError):
                helper.validate_gate(gate, 'final', 'fixture_hash')

    def test_uncommissioned_config_fails_before_external_reads(self):
        with tempfile.TemporaryDirectory(dir=helper.D, prefix='fixture_') as temporary:
            path = Path(temporary) / 'config.json'
            path.write_text(json.dumps({'schema': 'pr108-native-publication-integration-config/v1', 'mode': 'review_bundle_only'}))
            with self.assertRaisesRegex(ValueError, 'Not commissioned'):
                helper.prepare(path)

    def test_path_escape_and_symlink_inputs_are_rejected(self):
        for value in ['../escape', '/absolute', 'a//b', 'a\\b', 'a\nb']:
            with self.assertRaises(ValueError):
                helper.rel(value)
        with tempfile.TemporaryDirectory(dir=helper.D, prefix='fixture_') as temporary:
            root = Path(temporary)
            (root / 'target').write_text('fixture')
            (root / 'link').symlink_to(root / 'target')
            with self.assertRaisesRegex(ValueError, 'Symlink'):
                helper.regular(root / 'link')

    def test_zip_member_transport_is_verified_without_extraction(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            archive.writestr('package/PROOF.md', b'fixture proof')
        self.assertEqual(helper.zip_member(buffer.getvalue(), 'package/PROOF.md', 13), b'fixture proof')
        for name, size in [('missing', 13), ('../package/PROOF.md', 13), ('package/PROOF.md', 100)]:
            with self.assertRaises(ValueError):
                helper.zip_member(buffer.getvalue(), name, size)

    def test_zip_symlink_member_is_rejected(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            info = zipfile.ZipInfo('link')
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(info, b'target')
        with self.assertRaises(ValueError):
            helper.zip_member(buffer.getvalue(), 'link', 6)

if __name__ == '__main__':
    unittest.main()
