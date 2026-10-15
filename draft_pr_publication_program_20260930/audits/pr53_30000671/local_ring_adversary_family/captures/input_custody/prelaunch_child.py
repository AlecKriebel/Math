from pathlib import Path
import hashlib, json, stat
from closure_common import F, R, check_external, check_row, digest

e = json.loads((F / 'EXTERNAL_REFERENCES.json').read_bytes())
n = check_external()
o = R / e['original_family_path']
b = (o / 'MANIFEST.json').read_bytes()
assert digest(b) == e['original_manifest_sha256']
m = json.loads(b)
assert m['schema'] == 'pr53-original-closed-manifest/v1' and m['root_approval'] is False
names = {row['path'] for row in m['files']}
assert len(names) == len(m['files'])
assert {p.relative_to(o).as_posix() for p in o.rglob('*') if p.is_file()} == names
assert {'.'} | {p.relative_to(o).as_posix() for p in o.rglob('*') if p.is_dir()} == set(m['directories'])
for row in m['files']:
    if row['path'] == 'MANIFEST.json':
        assert row['sha256'] == 'LITERAL_SELF_REFERENCE_NOT_A_DIGEST' and row['bytes'] is None
        assert row['mode'] == '0444'
    else:
        check_row(o, row)
        assert row['mode'] == '0444'
auth = json.loads((o / 'GITHUB_AUTHENTICATION.json').read_bytes())
assert auth['head'] == 'd49a1bd56d8cc268159331e5ce868e258a32bb58'
assert len(auth['files']) == 11
for row in auth['files']:
    t = (o / row['archive_path']).read_bytes()
    assert len(t) == row['bytes'] and digest(t) == row['sha256']
    assert hashlib.sha1(('blob ' + str(len(t)) + '\0').encode() + t).hexdigest() == row['git_blob_sha1']
record = json.loads((o / 'original_archive/source_record.json').read_bytes())
assert record['record']['id'] == 30000671 and record['record']['problem_number'] == 'OWR-1453-004'
assert record['research_result_for_code'] is None
raw = json.loads((o / 'RAW_PRIOR_REPORT_JOIN.json').read_bytes())
sql = json.loads((o / 'SELECTED_SQL_ROW.json').read_bytes())
assert raw['raw_research_results_key_present'] is False and raw['sql_report_literal'] == '{}'
assert sql['report_sql_type'] == 'text' and sql['report_literal'] == '{}'
assert sql['payload_json'] == record['record']
readiness = json.loads((o / 'original_archive/readiness.json').read_bytes())
assert readiness['status'] == readiness['recommended_queue_status'] == 'already_solved'
assert readiness['used_substantive_attempts'] == 0 and readiness['maximum_substantive_attempts'] == 5
assert (o / 'original_archive/turns.jsonl').read_bytes() == b''
assert readiness['our_new_discovery'] is False and readiness['historical_construction_independently_reproved'] is False
assert readiness['full_2008_article_retrieved'] is False
assert digest((o / 'original_archive/SOURCE_STATUS.md').read_bytes()) == readiness['artifact_sha256']
assert len(e['root_complete_capture_paths']) == 2
for i, p in enumerate(e['root_complete_capture_paths']):
    c = json.loads((R / p).read_bytes())
    out = json.loads(((R / p).parent / c['stdout']['path']).read_bytes())
    if i == 0:
        assert c['argv'] == ['/usr/bin/python3', '-B', str(o / 'close_for_ROOT.py')]
        assert out['manifest_sha256'] == e['original_manifest_sha256']
        assert out['status'] == 'PASS_ORIGINAL_CUSTODY_ONLY'
    else:
        assert c['argv'] == ['/usr/bin/python3', '-B', str(o / 'verify_closed_readonly.py'), e['original_manifest_sha256']]
        assert out['actual_manifest_sha256'] == e['original_manifest_sha256']
        assert out['status'] == 'PASS_SEPARATE_ORIGINAL_READBACK_ONLY'
fresh = json.loads((F / 'FRESH_PRIMARY_SCOPE.json').read_bytes())
assert fresh['pdf_sha256'] == 'b1001aadcbbf3a8c35707b4b58cddbce46132e7ecb7601869e676d5f702f805d'
assert len(fresh['scope_checks']) == 12 and all(x is True for x in fresh['scope_checks'].values())
cap = json.loads((F / 'captures/fresh_primary/CAPTURE.json').read_bytes())
assert cap['pid'] == 11789 and cap['exit_code'] == 0 and cap['status'] == 'PASS'
for k in ('stdout', 'stderr', 'operator_prelaunch', 'child_prelaunch'):
    r = cap[k]
    z = F / r['path']
    assert len(z.read_bytes()) == r['bytes'] and digest(z.read_bytes()) == r['sha256']
assert digest((F / 'check_fresh_primary.py').read_bytes()) == cap['child_prelaunch']['sha256']
assert digest((F / 'capture_command.py').read_bytes()) == cap['operator_prelaunch']['sha256']
assert json.loads((F / 'captures/fresh_primary/stdout.bin').read_bytes()) == fresh
print(json.dumps({'status': 'PASS_INPUT_CUSTODY', 'original_manifest_sha256': digest(b),
                  'original_files_including_literal_self': len(names),
                  'exact_original_science_files': len(auth['files']),
                  'external_whole_body_rows': n,
                  'real_root_closure_and_separate_readback_bound': True,
                  'fresh_textual_source_scope_predicates': 12,
                  'independent_counterexample_construction_verified': False,
                  'root_approval': False}, indent=2))
