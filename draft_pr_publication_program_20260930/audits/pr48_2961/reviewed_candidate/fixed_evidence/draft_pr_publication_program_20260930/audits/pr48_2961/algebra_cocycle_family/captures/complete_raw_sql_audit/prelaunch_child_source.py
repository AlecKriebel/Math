#!/usr/bin/env python3
"""Read complete raw and SQLite provenance in place, preserving type distinctions."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sqlite3
import sys
from capture import ref
from reproduce_original import strict_load, typed

assert __debug__ and sys.flags.optimize == 0
FAMILY = Path(__file__).resolve().parent
REPO = FAMILY.parent.parents[2]
CACHE = REPO / 'unsolved_math_prioritization/cache'
started = datetime.now(timezone.utc).isoformat()
paths = [CACHE / 'problems.json', CACHE / 'research_results.json', CACHE / 'catalog.sqlite']
bindings = [ref(path) for path in paths]
raw_problem_bytes = paths[0].read_bytes()
raw_report_bytes = paths[1].read_bytes()
problems = strict_load(raw_problem_bytes)
reports = strict_load(raw_report_bytes)
assert isinstance(problems, list) and len(problems) == 15458
assert isinstance(reports, dict) and len(reports) == 6701
assert all(type(row['id']) is int for row in problems)
by_id = {row['id']: row for row in problems}
assert len(by_id) == len(problems)
database = sqlite3.connect('file:' + str(paths[2]) + '?mode=ro', uri=True)
schema = database.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
revision = database.execute('SELECT revision FROM metadata').fetchall()
assert revision == [('37e53eabe540fb458758e198be61634bd02ee008',)]
rows = database.execute('SELECT key,payload,report FROM records ORDER BY key').fetchall()
assert len(rows) == len(problems)
sql_read_rows = []
selected = []
selected_ids = {2961: 'KP-4.85', 30004403: 'OWR-17471-009'}
for key, payload_text, report_text in rows:
    assert type(key) is str and key.isdecimal()
    identity = int(key)
    assert identity in by_id
    problem = strict_load(payload_text)
    report = strict_load(report_text)
    assert typed(problem) == typed(by_id[identity])
    expected_report = reports.get(problem['problem_number'], {})
    assert typed(report) == typed(expected_report)
    sql_read_rows.append({'key': key, 'payload_bytes': len(payload_text.encode()),
                          'payload_sha256': hashlib.sha256(payload_text.encode()).hexdigest(),
                          'report_bytes': len(report_text.encode()),
                          'report_sha256': hashlib.sha256(report_text.encode()).hexdigest(),
                          'payload_and_report_recursive_types_equal_raw': True})
    if identity in selected_ids:
        code = selected_ids[identity]
        assert problem['problem_number'] == code
        assert code not in reports
        assert report_text == '{}' and type(report) is dict and report == {}
        filename = 'source_record.json' if identity == 2961 else 'related_source_record.json'
        literal = strict_load((FAMILY.parent / 'source_snapshot' / filename).read_bytes())
        assert typed(literal) == typed(problem) and type(literal['id']) is int
        assert 'prior_research' not in literal and 'problem' not in literal
        selected.append({'id': identity, 'problem_code': code, 'source_record': ref(FAMILY.parent / 'source_snapshot' / filename),
                         'raw_upstream_prior_key_present': False, 'raw_upstream_prior_presence': 'ABSENT',
                         'raw_upstream_prior_value_type': 'not applicable: absent key',
                         'sqlite_prior_literal': report_text, 'sqlite_prior_value': report,
                         'sqlite_prior_value_type': 'dict', 'empty_object_fallback_is_not_null': True,
                         'plain_source_has_no_prior_wrapper': True,
                         'original_prior_report_file_exists': (FAMILY.parent / 'source_snapshot/prior_report.json').exists()})
database.close()
assert len(selected) == 2 and all(not row['original_prior_report_file_exists'] for row in selected)
assert [ref(path) for path in paths] == bindings
result = {'schema': 'pr48-algebra-family-in-place-complete-raw-sql-audit/v1',
          'status': 'PASS_COMPLETE_RAW_SQL_TYPE_IDENTITY', 'actual_pid': os.getpid(),
          'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
          'raw_and_database_files': bindings, 'raw_problem_bytes_fully_read': len(raw_problem_bytes),
          'raw_prior_bytes_fully_read': len(raw_report_bytes), 'raw_problem_count': len(problems),
          'raw_prior_count': len(reports), 'database_schema': schema, 'database_revision': revision,
          'all_sql_rows': sql_read_rows, 'selected': sorted(selected, key=lambda row: row['id']),
          'foreign_raw_and_database_bodies_copied': False, 'ROOT_or_merge_approval': False,
          'source_audit_null_report_claim_verified': False,
          'required_provenance_repair': 'Describe an absent upstream prior key and literal SQLite empty-object fallback; preserve original prose as archive.'}
(FAMILY / 'COMPLETE_RAW_SQL_AUDIT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'actual_pid': os.getpid(), 'raw_bytes': len(raw_problem_bytes) + len(raw_report_bytes),
                  'sql_rows': len(rows), 'selected_prior_presence': [row['raw_upstream_prior_presence'] for row in selected],
                  'sqlite_priors': [row['sqlite_prior_value'] for row in selected]}, indent=2))
