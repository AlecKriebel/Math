"""Offline adversarial integration tests; all GWS calls are mocked."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('append_publication', HERE / 'append_publication.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

PROBLEM = 'https://www.unsolvedmath.com/problems/OWR-123-009'
DOI = '10.5281/zenodo.123456'


class FakeGWS:
    def __init__(self, rows=None, response_override=None, readback_override=None, timeout=False, readback_metadata=None, malformed_updates=False):
        self.rows = rows if rows is not None else [app.HEADERS]
        self.response_override = response_override
        self.readback_override = readback_override
        self.timeout = timeout
        self.readback_metadata = readback_metadata
        self.malformed_updates = malformed_updates
        self.appends = 0
        self.dry_runs = 0
        self.requested = None

    def run(self, argv, **kwargs):
        assert isinstance(argv, list) and not kwargs.get('shell', False)
        params = json.loads(argv[argv.index('--params') + 1])
        if argv[1:4] == ['sheets', 'spreadsheets', 'get']:
            value = {'spreadsheetId': app.SPREADSHEET_ID, 'sheets': [
                {'properties': {'sheetId': 0, 'title': 'Papers'}},
                {'properties': {'sheetId': app.SHEET_ID, 'title': 'Math Puzzles'}},
            ]}
        elif argv[1:5] == ['sheets', 'spreadsheets', 'values', 'get']:
            if params['range'] == "'Math Puzzles'!A:D":
                value = {'majorDimension': 'ROWS', 'values': self.rows, 'range': "'Math Puzzles'!A1:D1006"}
            else:
                value = {'majorDimension': 'ROWS', 'values': self.readback_override if self.readback_override is not None else
                         [self.requested if self.requested is not None else self.rows[int(params['range'].split('!A')[1].split(':')[0])-1]],
                         'range': params['range']}
                if self.readback_metadata:
                    value.update(self.readback_metadata)
        else:
            assert argv[1:5] == ['sheets', 'spreadsheets', 'values', 'append']
            body = json.loads(argv[argv.index('--json') + 1])
            assert params['range'] == "'Math Puzzles'!A:D"
            assert params['valueInputOption'] == 'RAW'
            assert params['insertDataOption'] == 'INSERT_ROWS'
            assert len(body['values']) == 1 and len(body['values'][0]) == 4
            assert body['values'][0][1] == ''
            if '--dry-run' in argv:
                self.dry_runs += 1
                value = {'dryRun': True}
            else:
                self.appends += 1
                self.requested = body['values'][0]
                if self.timeout:
                    raise subprocess.TimeoutExpired(argv, 60, output='partial response')
                value = {'spreadsheetId': app.SPREADSHEET_ID, 'updates': {
                    'spreadsheetId': app.SPREADSHEET_ID, 'updatedRows': 1,
                    'updatedColumns': 4, 'updatedCells': 4,
                    'updatedRange': "'Math Puzzles'!A11:D11",
                    'updatedData': {'majorDimension': 'ROWS', 'range': "'Math Puzzles'!A11:D11", 'values': [self.requested]},
                }}
                if self.response_override:
                    value['updates'].update(self.response_override)
                if self.malformed_updates:
                    value['updates'] = None
        return subprocess.CompletedProcess(argv, 0, stdout=json.dumps(value), stderr='')


class AppendSafetyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=HERE)
        self.receipts = Path(self.tmp.name)
        self.notes = self.receipts / 'notes.txt'
        self.notes.write_text('=Literal notes, with commas\nSecond line\n', encoding='utf-8')
        self.args = ['--problem-url', PROBLEM, '--doi', DOI, '--notes-file', str(self.notes),
                     '--receipt-dir', str(self.receipts)]

    def tearDown(self):
        self.tmp.cleanup()

    def execute(self, fake, write=False):
        with patch.object(app.shutil, 'which', return_value='/fake/gws'), patch.object(app.subprocess, 'run', fake.run), \
                patch('sys.stdout'), patch('sys.stderr'):
            return app.main(self.args + (['--execute'] if write else []))

    def test_default_only_dry_runs_and_keeps_evidence(self):
        fake = FakeGWS()
        self.assertEqual(self.execute(fake), 0)
        self.assertEqual((fake.dry_runs, fake.appends), (1, 0))
        attempt = next(self.receipts.glob('tracker-attempt-*'))
        self.assertTrue((attempt / 'request.json').exists())
        self.assertTrue((attempt / 'dry-run.json').exists())
        self.assertFalse((attempt / 'append-attempted.json').exists())

    def test_execute_appends_once_preserving_literal_notes_and_exact_readback(self):
        fake = FakeGWS()
        self.assertEqual(self.execute(fake, True), 0)
        self.assertEqual(fake.appends, 1)
        self.assertEqual(fake.requested[3], '=Literal notes, with commas\nSecond line')
        attempt = next(self.receipts.glob('tracker-attempt-*'))
        self.assertTrue((attempt / 'append-attempted.json').exists())
        self.assertTrue((attempt / 'response.json').exists())
        self.assertTrue((attempt / 'readback.json').exists())

    def test_existing_pair_is_independently_read_without_append_or_notes_claim(self):
        rows = [app.HEADERS, [PROBLEM, '', 'https://doi.org/' + DOI, 'Existing notes']]
        fake = FakeGWS(rows)
        self.assertEqual(self.execute(fake, True), 0)
        self.assertEqual(fake.appends, 0)
        result = json.loads(next(self.receipts.glob('tracker-attempt-*/result.json')).read_text())
        self.assertEqual(result['state'], 'verified_existing')
        self.assertFalse(result['requested_row_matches'])

    def test_crossed_peer_keys_and_duplicate_pairs_fail_before_append(self):
        for rows in ([app.HEADERS, [PROBLEM, '', '10.5281/zenodo.999', ''],
                      ['OWR-999-001', '', DOI, '']],
                     [app.HEADERS, [PROBLEM, '', DOI, ''], [PROBLEM, '', DOI, '']]):
            fake = FakeGWS(rows)
            self.assertEqual(self.execute(fake, True), 1)
            self.assertEqual(fake.appends, 0)

    def test_ranges_counts_and_wrong_spreadsheet_rejected_after_only_one_append(self):
        for override in ({'updatedRange': "'Math Puzzles'!A11:D12"},
                         {'updatedRange': "'Math Puzzles'!A1:D1"},
                         {'updatedRange': "'Papers'!A11:D11"},
                         {'updatedRange': "'Math Puzzles'!B11:E11"},
                         {'updatedRows': True}, {'spreadsheetId': 'wrong'}):
            with self.subTest(override=override):
                # Distinct receipt folders model distinct one-shot attempts.
                original = self.args[-1]
                folder = self.receipts / ('case-' + str(len(list(self.receipts.iterdir()))))
                self.args[-1] = str(folder)
                fake = FakeGWS(response_override=override)
                self.assertEqual(self.execute(fake, True), 1)
                self.assertEqual(fake.appends, 1)
                self.args[-1] = original

    def test_lost_response_marker_prevents_second_append(self):
        fake = FakeGWS(timeout=True)
        self.assertEqual(self.execute(fake, True), 1)
        self.assertEqual(fake.appends, 1)
        self.assertEqual(self.execute(fake, True), 1)
        self.assertEqual(fake.appends, 1)

    def test_wrong_empty_or_overwide_readback_fails_without_retry(self):
        for readback in ([], [['wrong', '', 'https://doi.org/' + DOI, 'wrong']],
                         [['a', '', 'c', 'd', 'extra']]):
            original = self.args[-1]
            folder = self.receipts / ('readback-' + str(len(list(self.receipts.iterdir()))))
            self.args[-1] = str(folder)
            fake = FakeGWS(readback_override=readback)
            self.assertEqual(self.execute(fake, True), 1)
            self.assertEqual(fake.appends, 1)
            self.args[-1] = original

    def test_normalization_preserves_problem_identity_and_doi_equivalence(self):
        self.assertEqual(app.normalize_problem(PROBLEM + '/?ref=x#fragment'), app.normalize_problem('OWR-123-009'))
        self.assertNotEqual(app.normalize_problem(PROBLEM), app.normalize_problem(PROBLEM.replace('www.unsolvedmath.com', 'unsolvedmath.com.evil.example')))
        with self.assertRaises(app.TrackerError):
            app.normalize_problem(PROBLEM + '/extra')
        self.assertEqual(app.normalize_doi('DOI: ' + DOI.upper()), app.normalize_doi('http://dx.doi.org/' + DOI))
        with self.assertRaises(app.TrackerError):
            app.normalize_doi('https://doi.org.evil.example/' + DOI)
        with self.assertRaises(app.TrackerError):
            app.normalize_doi(' ')
        self.assertNotEqual(app.normalize_problem('https://example.org/#/problem/1'), app.normalize_problem('https://example.org/#/problem/2'))
        self.assertEqual(app.normalize_problem('https://www.unsolvedmath.com/problems/30005473/?ref=x#y'), app.normalize_problem('30005473'))
        self.assertEqual(app.normalize_doi('HTTPS://DOI.ORG/' + DOI), DOI)
        with self.assertRaises(app.TrackerError):
            app.normalize_doi('https://doi.org:notaport/' + DOI)

    def test_verified_numeric_code_alias_avoids_second_record_and_conflicts_fail(self):
        self.args[1] = 'https://www.unsolvedmath.com/problems/30005473'
        fake = FakeGWS([app.HEADERS, [PROBLEM, '', 'https://doi.org/' + DOI, 'Existing']])
        self.assertEqual(self.execute(fake, True), 1)  # Same DOI, unverified different problem key.
        self.args += ['--problem-alias', 'OWR-123-009']
        self.assertEqual(self.execute(fake, True), 0)  # Explicit independently verified alias.
        self.assertEqual(fake.appends, 0)
        fake_conflict = FakeGWS([app.HEADERS, [PROBLEM, '', '10.5281/zenodo.999', 'Existing']])
        self.assertEqual(self.execute(fake_conflict, True), 1)
        self.assertEqual(fake_conflict.appends, 0)

    def test_malformed_post_append_objects_and_false_readback_metadata_fail(self):
        for override in ({'updatedData': None}, {'updatedData': []}):
            original = self.args[-1]
            folder = self.receipts / ('malformed-' + str(len(list(self.receipts.iterdir()))))
            self.args[-1] = str(folder)
            fake = FakeGWS(response_override=override)
            self.assertEqual(self.execute(fake, True), 1)
            self.assertEqual(fake.appends, 1)
            self.assertTrue(next(folder.glob('tracker-attempt-*/failure.json')).is_file())
            self.args[-1] = original
        original = self.args[-1]
        self.args[-1] = str(self.receipts / 'updates-null')
        fake = FakeGWS(malformed_updates=True)
        self.assertEqual(self.execute(fake, True), 1)
        self.assertEqual(fake.appends, 1)
        self.assertTrue(next(Path(self.args[-1]).glob('tracker-attempt-*/failure.json')).is_file())
        self.args[-1] = original

    def test_wrong_readback_range_or_dimension_and_malformed_existing_key_fail(self):
        for metadata in ({'range': "'Wrong Tab'!A11:D11"}, {'majorDimension': 'COLUMNS'}):
            original = self.args[-1]
            self.args[-1] = str(self.receipts / ('false-readback-' + str(len(list(self.receipts.iterdir())))))
            fake = FakeGWS(readback_metadata=metadata)
            self.assertEqual(self.execute(fake, True), 1)
            self.assertEqual(fake.appends, 1)
            self.args[-1] = original
        fake = FakeGWS([app.HEADERS, ['OWR-999-001', '', 'malformed-nonempty-doi', '']])
        self.assertEqual(self.execute(fake, True), 1)
        self.assertEqual(fake.appends, 0)

    def test_range_parser_accepts_canonical_unquoted_title_and_escaped_apostrophe(self):
        self.assertEqual(app.range_row('Simple!A9:D9', 'Simple'), 9)
        self.assertEqual(app.range_row("'O''Brien'!A9:D9", "O'Brien"), 9)
        with self.assertRaises(app.TrackerError):
            app.range_row("'Wrong Tab'!A9:D9", 'Math Puzzles')


if __name__ == '__main__':
    unittest.main()
