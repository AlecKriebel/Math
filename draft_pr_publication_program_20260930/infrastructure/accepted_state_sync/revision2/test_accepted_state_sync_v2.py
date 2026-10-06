"""Exact-current PR21/22 and duplicate accounting tests on frozen offline copies.

No legacy rank/status/turn command or function is invoked. No live input changes.
"""
import ast
from contextlib import closing
import copy
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest

import accepted_state_sync_v2 as sync

LIVE_REPO = sync.HERE.parents[3]
STAMP = '2026-10-01T20:45:00+00:00'


class ExactCurrentRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (sync.HERE / 'tmp').mkdir(exist_ok=True)
        cls.snapshot = sync.HERE / 'tmp' / 'frozen_current_inputs'
        if cls.snapshot.exists():
            shutil.rmtree(cls.snapshot)
        cls.snapshot.mkdir()
        cls.original_spec = sync.load(sync.HERE / 'bindings_v2.json')
        plan = sync.build_plan(LIVE_REPO, cls.original_spec, STAMP)
        sync.validate_plan(LIVE_REPO, plan)
        for binding in plan['bindings']:
            path = cls.snapshot / binding['path']
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(sync.bound(LIVE_REPO, binding))
        q = cls.snapshot / 'unsolved_math_prioritization'
        for filename in ['state.json', 'history.jsonl']:
            (q / filename).write_bytes((LIVE_REPO / 'unsolved_math_prioritization' / filename).read_bytes())
        ids = {x['id'] for x in cls.original_spec['entries']} | {x['id'] for x in cls.original_spec['duplicate_mirrors']}
        cache = q / 'cache'
        cache.mkdir(exist_ok=True)
        with closing(sqlite3.connect((LIVE_REPO / 'unsolved_math_prioritization/cache/catalog.sqlite').as_uri() + '?mode=ro', uri=True)) as live:
            with closing(sqlite3.connect(cache / 'catalog.sqlite')) as offline:
                offline.execute('CREATE TABLE records (key TEXT PRIMARY KEY,payload TEXT,report TEXT)')
                for identity in ids:
                    row = live.execute('SELECT key,payload,report FROM records WHERE key=?', (identity,)).fetchone()
                    offline.execute('INSERT INTO records VALUES (?,?,?)', row)
                offline.commit()
        cls.snapshot_plan = plan

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=sync.HERE / 'tmp')
        self.repo = Path(self.temp.name)
        shutil.copytree(self.snapshot, self.repo, dirs_exist_ok=True)
        self.spec = copy.deepcopy(self.original_spec)
        self.q = self.repo / 'unsolved_math_prioritization'

    def tearDown(self):
        self.temp.cleanup()

    def entry(self, pr):
        return next(x for x in self.spec['entries'] if x['pr'] == pr)

    def refresh(self, binding):
        binding['sha256'] = sync.sha((self.repo / binding['path']).read_bytes())

    def mutate(self, binding, callback):
        path = self.repo / binding['path']
        obj = sync.load(path)
        callback(obj)
        path.write_bytes(sync.encode(obj))
        self.refresh(binding)

    def update_package(self, pr, relative_names):
        """Refresh enclosing receipts so semantic falsifications reach their own gate."""
        entry = self.entry(pr)
        manifest_path = self.repo / entry['canonical_manifest']['path']
        manifest = sync.load(manifest_path)
        for item in manifest['files']:
            if item['path'] in relative_names:
                data = (manifest_path.parent / item['path']).read_bytes()
                item.update(sha256=sync.sha(data), bytes=len(data))
        manifest_path.write_bytes(sync.encode(manifest))
        self.refresh(entry['canonical_manifest'])
        self.mutate(entry['audit_acceptance'], lambda x: x.update(canonical_manifest_sha256=entry['canonical_manifest']['sha256']))

    def change_acceptance(self, pr, callback):
        self.mutate(self.entry(pr)['acceptance'], callback)
        self.update_package(pr, {'acceptance.json'})

    def plan(self):
        return sync.build_plan(self.repo, self.spec, STAMP)

    def reject(self, message):
        with self.assertRaisesRegex(sync.Rejected, message):
            self.plan()

    def test_exact_current_twelve_primaries_and_one_duplicate(self):
        plan = self.plan()
        self.assertEqual((plan['primary_count'], plan['duplicate_count'], len(plan['decisions'])), (12, 1, 13))
        self.assertEqual({x['pr'] for x in plan['decisions'] if x['status'] != 'duplicate'}, set(range(9, 18)) | {19, 21, 22})
        for identity in ['30001696', '20002011']:
            self.assertEqual((plan['state_after'][identity]['status'], plan['state_after'][identity]['turns_used']), ('already_solved', 1))
        duplicate = plan['state_after']['20002052']
        self.assertEqual((duplicate['status'], duplicate['turns_used'], duplicate['turn_limit']), ('duplicate', 0, 5))
        self.assertEqual((duplicate['shared_budget_owner'], duplicate['shared_turns_used'], duplicate['shared_turn_limit']), ('20002011', 1, 5))
        self.assertFalse(duplicate['independent_budget_allocated'])
        self.assertEqual(sum(x['turns_used'] for x in plan['state_after'].values()), 16)
        self.assertFalse(duplicate['evidence']['historical_transitions_asserted'])
        self.assertNotIn('candidate_turn', duplicate)
        self.assertNotIn('readiness_review_hash', duplicate)
        self.assertNotIn('20002052', {x['id'] for x in self.spec['entries']})

    def test_pending_primary_inventory_is_rejected(self):
        self.mutate(self.spec['inventory'], lambda x: next(y for y in x['items'] if y['number'] == 21).update(stage='pending'))
        self.reject('scope changed/ambiguous')

    def test_unpublished_publication_receipt_is_rejected(self):
        self.mutate(self.entry(9)['publication'], lambda x: x.update(published_state_verified_by_repository_tool=False, state='draft'))
        self.reject('Publication not verified public')

    def test_duplicate_queue_doi_owner_is_rejected(self):
        path = self.q / 'QUEUE.md'
        text = path.read_text()
        row = next(x for x in text.splitlines() if '| 20002052 /' in x)
        cells = row.split('|')
        cells[-2] = ' 10.5281/zenodo.23074543 '
        path.write_text(text.replace(row, '|'.join(cells)))
        self.refresh(self.spec['queue'])
        self.reject('Duplicate/wrong-row DOI')

    def test_missing_current_primary_budget_is_not_inferred(self):
        path = self.q / 'QUEUE.md'
        text = path.read_text()
        row = next(x for x in text.splitlines() if '| 30001696 /' in x)
        path.write_text(text.replace(row, row.replace('| 1/5 |', '|  |')))
        self.refresh(self.spec['queue'])
        self.reject('Explicit queue/policy budget mismatch')

    def test_current21_remote_head_must_match_exact_accepted_head(self):
        self.mutate(self.entry(21)['remote'], lambda x: x.update(headRefOid=self.entry(22)['id'].ljust(40, '0')))
        self.reject('exact-head/merge mismatch')

    def test_current22_remote_must_be_merged(self):
        self.mutate(self.entry(22)['remote'], lambda x: x.update(state='OPEN', mergedAt=None))
        self.reject('MERGED')

    def test_crosswired21_and22_remote_receipts_are_rejected(self):
        self.entry(21)['remote'] = self.entry(22)['remote']
        self.reject('exact-head/merge mismatch')

    def test_current21_original_budget_cannot_be_changed(self):
        self.entry(21)['budget']['used'] = 2
        self.reject('budget mismatch')

    def test_current22_numbered_original_ledger_is_checked(self):
        self.mutate(self.entry(22)['budget']['ledger'], lambda x: x['turns'][0].update(number=2))
        self.reject('numbered attempt')

    def test_current21_canonical_package_file_change_is_rejected(self):
        parent = (self.repo / self.entry(21)['canonical_manifest']['path']).parent
        (parent / 'CLASSICAL_PRIOR_ADAPTER.md').write_text('Unaccepted replacement adapter.\n')
        self.reject('Stale/mismatched')

    def test_current22_wrong_canonical_manifest_receipt_is_rejected(self):
        self.mutate(self.entry(22)['audit_acceptance'], lambda x: x.update(canonical_manifest_sha256='0' * 64))
        self.reject('manifest mismatch')

    def test_eligible_duplicate_cannot_be_silently_ignored(self):
        self.spec['duplicate_mirrors'] = []
        self.reject('explicit bound mirror needed')

    def test_duplicate_relation_must_be_explicitly_accepted(self):
        self.change_acceptance(22, lambda x: x.update(duplicate_id=20002053))
        self.reject('relation mismatch')

    def test_duplicate_status_must_be_explicitly_accepted(self):
        self.change_acceptance(22, lambda x: x.update(duplicate_queue_status='queued'))
        self.reject('disposition not accepted')

    def test_no_independent_duplicate_proof_turn_can_be_erased(self):
        self.change_acceptance(22, lambda x: x.update(duplicate_additional_attempts_used=1))
        self.reject('independent proof turn')

    def test_requested_extra_duplicate_turn_is_rejected(self):
        self.spec['duplicate_mirrors'][0]['additional_independent_proof_turns'] = 1
        self.reject('add zero proof turns')

    def test_wrong_shared_budget_owner_is_rejected(self):
        self.spec['duplicate_mirrors'][0]['shared_budget_owner'] = '30001696'
        self.reject('explicit bound mirror needed')

    def test_duplicate_queue_zero_additional_budget_required(self):
        path = self.q / 'QUEUE.md'
        text = path.read_text()
        rows = text.splitlines()
        row = next(x for x in rows if '| 20002052 /' in x)
        path.write_text(text.replace(row, row.replace('| 0/5 |', '| 1/5 |')))
        self.refresh(self.spec['queue'])
        self.reject('Duplicate queue disposition/budget')

    def test_existing_duplicate_extra_usage_is_not_reset(self):
        (self.q / 'state.json').write_bytes(sync.encode({'20002052': {'turns_used': 1, 'status': 'in_progress'}}))
        self.reject('cannot be erased')

    def test_changed_duplicate_exact_statement_is_rejected(self):
        duplicate = self.spec['duplicate_mirrors'][0]
        self.mutate(duplicate['accepted_source'], lambda x: x.update(statement='A different repaired FSA conjecture.'))
        self.mutate(duplicate['relation_evidence'], lambda x: x.update(duplicate_source_record_sha256=duplicate['accepted_source']['sha256']))
        # Same provenance appears as primary duplicate evidence: refresh its binding too.
        self.entry(22)['duplicate_evidence']['sha256'] = duplicate['relation_evidence']['sha256']
        self.update_package(22, {'duplicate_source_record.json', 'provenance.json'})
        self.reject('full source record mismatch')

    def test_completed_scope_cannot_omit21_or_add_pending23(self):
        self.spec['required_completed_prs'].remove(21)
        self.reject('scope changed/ambiguous')

    def test_original_v1_artifact_change_is_rejected(self):
        seal = sync.load(self.repo / self.spec['historical_v1_seal']['path'])
        parent = (self.repo / self.spec['historical_v1_seal']['path']).parent
        (parent / next(x['path'] for x in seal['files'] if x['path'].endswith('CURRENT_PLAN.json'))).write_text('Changed historical proposal.\n')
        self.reject('Stale/mismatched')

    def test_old_duplicate_decisions_remain_ineligible_and_unmodified(self):
        plan = self.plan()
        for identity in ['30005796', '30002868', '30006391']:
            self.assertNotIn(identity, plan['state_after'])
        self.assertEqual(plan['state_after']['30005795']['evidence']['duplicate_ids'], ['30005796'])
        self.assertEqual(plan['state_after']['30002867']['evidence']['duplicate_ids'], ['30002868'])
        self.assertEqual(plan['state_after']['30006390']['evidence']['duplicate_ids'], ['30006391'])

    def test_idempotent_thirteen_event_replay_and_no_new_budget(self):
        plan = self.plan()
        sync.replay_sandbox(plan, self.q)
        before = ((self.q / 'state.json').read_bytes(), (self.q / 'history.jsonl').read_bytes())
        sync.replay_sandbox(plan, self.q)
        self.assertEqual(before, ((self.q / 'state.json').read_bytes(), (self.q / 'history.jsonl').read_bytes()))
        again = sync.build_plan(self.repo, self.spec, '2026-10-02T20:45:00+00:00')
        self.assertEqual(again['history_append'], [])
        self.assertEqual(again['state_after_bytes'].encode(), before[0])
        self.assertEqual(again['state_after']['20002052']['at'], STAMP)
        history = [json.loads(x) for x in before[1].decode().splitlines()]
        self.assertEqual(len(history), 13)
        self.assertEqual(sum(x['event'] == 'acceptance_duplicate_mirror_import' for x in history), 1)

    def test_duplicate_interrupted_history_state_recovery_is_once_only(self):
        plan = self.plan()
        with self.assertRaisesRegex(RuntimeError, 'Injected'):
            sync.replay_sandbox(plan, self.q, fail_after_history=True)
        sync.replay_sandbox(plan, self.q)
        events = [json.loads(x) for x in (self.q / 'history.jsonl').read_text().splitlines()]
        self.assertEqual(len(events), 13)
        self.assertEqual(sum(x['id'] == '20002052' for x in events), 1)
        self.assertEqual(sync.load(self.q / 'state.json')['20002052']['turns_used'], 0)

    def test_actual_legacy_eligibility_expression_excludes_duplicate(self):
        # Read/evaluate one pure expression only; never call a legacy command.
        legacy = LIVE_REPO / 'unsolved_math_prioritization/queue.py'
        tree = ast.parse(legacy.read_text())
        rank = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'rank')
        assignment = next(x for x in ast.walk(rank) if isinstance(x, ast.Assign) and any(isinstance(y, ast.Name) and y.id == 'eligible' for y in x.targets))
        expression = compile(ast.Expression(assignment.value), str(legacy), 'eval')
        self.assertFalse(eval(expression, {'a': {'holds': []}, 'local_status': 'duplicate', 'turns': 0, 'cfg': {'turn_limit': 5}}))

    def test_reviewed_primary_status_tamper_with_refreshed_hash_is_rejected(self):
        plan = self.plan()
        plan['state_after']['30001696']['status'] = 'unsolved'
        plan['state_after_bytes'] = sync.encode(plan['state_after']).decode()
        plan['state_after_sha256'] = sync.sha(plan['state_after_bytes'].encode())
        with self.assertRaisesRegex(sync.Rejected, 'exact accepted evidence/accounting'):
            sync.validate_plan(self.repo, plan)

    def test_reviewed_history_event_tamper_with_refreshed_hash_is_rejected(self):
        plan = self.plan()
        events = [json.loads(x) for x in plan['history_append_bytes'].splitlines()]
        events[-1]['turns_used'] = 1
        plan['history_append_bytes'] = ''.join(json.dumps(x, ensure_ascii=False, sort_keys=True) + '\n' for x in events)
        plan['history_after_sha256'] = sync.sha((self.q / 'history.jsonl').read_bytes() + plan['history_append_bytes'].encode())
        with self.assertRaisesRegex(sync.Rejected, 'exact accepted evidence/accounting'):
            sync.validate_plan(self.repo, plan)

    def test_reviewed_duplicate_shared_accounting_tamper_rejected(self):
        plan = self.plan()
        plan['state_after']['20002052']['shared_turns_used'] = 0
        plan['state_after_bytes'] = sync.encode(plan['state_after']).decode()
        plan['state_after_sha256'] = sync.sha(plan['state_after_bytes'].encode())
        with self.assertRaisesRegex(sync.Rejected, 'shared owner accounting'):
            sync.validate_plan(self.repo, plan)


if __name__ == '__main__':
    unittest.main(verbosity=2)
