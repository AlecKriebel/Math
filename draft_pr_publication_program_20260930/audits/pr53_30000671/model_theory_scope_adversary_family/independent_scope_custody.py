"""Read original source/custody in place, never import another audit's code."""
from pathlib import Path
import hashlib
import json
import sqlite3
import stat

F = Path(__file__).resolve().parent
A = F.parent
R = F.parents[3]
O = A / 'original_preparation_family'
A45 = R / 'draft_pr_publication_program_20260930/audits/pr45_9900007'
EXPECTED_MF = 'd10783bb3d60becaa765d36a5cd5ff303c978049b9527266a2be4b2dc92f49b7'
checks = 0

def check(claim):
    global checks
    assert claim
    checks += 1

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def row(path):
    s = path.lstat()
    check(stat.S_ISREG(s.st_mode) and not path.is_symlink())
    return {'absolute_path': str(path), 'bytes': s.st_size, 'sha256': sha(path),
            'mode': format(stat.S_IMODE(s.st_mode), '04o')}

mf = O / 'MANIFEST.json'
check(sha(mf) == EXPECTED_MF)
d = json.loads(mf.read_bytes())
check(d['schema'] == 'pr53-original-closed-manifest/v1')
check(d['root_approval'] is False)
external = [row(mf)]
declared = {item['path'] for item in d['files']}
check(len(declared) == 174)
check({str(p.relative_to(O)) for p in O.rglob('*') if p.is_file()} == declared)
check({'.'} | {str(p.relative_to(O)) for p in O.rglob('*') if p.is_dir()}
      == set(d['directories']))
for item in d['files']:
    p = O / item['path']
    r = row(p)
    check(r['mode'] == '0444')
    if item['path'] != 'MANIFEST.json':
        check(r['bytes'] == item['bytes'] and r['sha256'] == item['sha256'])
        external.append(r)
for name in d['directories']:
    p = O if name == '.' else O / name
    s = p.lstat()
    check(stat.S_ISDIR(s.st_mode) and not p.is_symlink())
    check(stat.S_IMODE(s.st_mode) == 0o755)

capture_facts = []
for name, pid, script in [
    ('root_pr53_original_preparation_closure_actual_capture', 27668, 'close_for_ROOT.py'),
    ('root_pr53_original_preparation_closed_readback_actual_capture', 30517,
     'verify_closed_readonly.py')]:
    directory = A45 / name
    check({p.name for p in directory.iterdir()} ==
          {'CAPTURE.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin'})
    cap = json.loads((directory / 'CAPTURE.json').read_bytes())
    check(cap['schema'] == 'root-explicit-command-capture/v1')
    check(cap['status'] == 'PASS' and cap['actual_execution'] is True
          and cap['completed'] is True and cap['exit_code'] == 0
          and type(cap['pid']) is int and cap['pid'] == pid)
    check(cap['argv'][0:2] == ['/usr/bin/python3', '-B'])
    check(cap['argv'][2] == str(O / script))
    if script == 'verify_closed_readonly.py':
        check(cap['argv'][3:] == [EXPECTED_MF])
    else:
        check(cap['argv'][3:] == [])
    check(cap['operator_unchanged'] is True)
    check(sha(directory / 'prelaunch_operator.py') == cap['operator_sha256'])
    for stream in ('stdout', 'stderr'):
        p = directory / (stream + '.bin')
        check(p.stat().st_size == cap[stream]['bytes'])
        check(sha(p) == cap[stream]['sha256'])
    result = json.loads((directory / 'stdout.bin').read_bytes())
    check(result['root_approval'] is False)
    check(result.get('manifest_sha256', result.get('actual_manifest_sha256')) == EXPECTED_MF)
    capture_facts.append({k: cap[k] for k in ('pid', 'started_utc', 'finished_utc', 'exit_code')})
    external.extend(row(p) for p in directory.iterdir())

archive = O / 'original_archive'
rec = json.loads((archive / 'source_record.json').read_bytes())
check(rec['record']['id'] == 30000671)
check(rec['record']['problem_number'] == 'OWR-1453-004')
check(rec['research_result_for_code'] is None)
check('complete local Noetherian rings' in rec['record']['statement'])
check('every natural number' in rec['record']['statement'])
check('domain' not in rec['record']['statement'])
check('compatible' not in rec['record']['statement'])
check('finite residue' not in rec['record']['statement'])
check((archive / 'turns.jsonl').read_bytes() == b'')

auth = json.loads((O / 'GITHUB_AUTHENTICATION.json').read_bytes())
check(auth['head'] == 'd49a1bd56d8cc268159331e5ce868e258a32bb58')
check(len(auth['files']) == 11)
for item in auth['files']:
    p = O / item['archive_path']
    b = p.read_bytes()
    check(len(b) == item['bytes'] and hashlib.sha256(b).hexdigest() == item['sha256'])
    check(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
          == item['git_blob_sha1'])
    check(item['git_mode'] == '100644')
diff = (O / 'FULL_PR_DIFF.patch').read_text()
paths = [line.split(' b/', 1)[1] for line in diff.splitlines()
         if line.startswith('diff --git a/')]
check(len(paths) == 12 and len(set(paths)) == 12
      and 'unsolved_math_prioritization/QUEUE.md' in paths)
check(set(paths) - {'unsolved_math_prioritization/QUEUE.md'}
      == {x['repo_path'] for x in auth['files']})

# Direct source precision, checked in the original pinned local data. No
# current-network or live-record claim is made for these immutable observations.
cache = R / 'unsolved_math_prioritization/cache'
expected_cache = json.loads((O / 'RAW_CACHE_HASHES.json').read_bytes())
for item in expected_cache:
    p = Path(item['absolute_path'])
    check(p.parent == cache)
    r = row(p)
    check(r['bytes'] == item['bytes'] and r['sha256'] == item['sha256'])
    r['kind'] = 'dated pinned raw source; read in place, not copied'
    external.append(r)
reports = json.loads((cache / 'research_results.json').read_bytes())
check('OWR-1453-004' not in reports)
del reports
con = sqlite3.connect('file:' + str(cache / 'catalog.sqlite') + '?mode=ro&immutable=1', uri=True)
try:
    rows = con.execute("SELECT key,payload,report,typeof(report) FROM records "
                       "WHERE json_extract(payload,'$.id')=?", (30000671,)).fetchall()
finally:
    con.close()
check(len(rows) == 1)
key, payload, report, report_type = rows[0]
check(key == '30000671' and report == '{}' and report_type == 'text')
check(json.loads(payload) == rec['record'])

join = json.loads((O / 'RAW_PRIOR_REPORT_JOIN.json').read_bytes())
check(join['raw_research_results_key_present'] is False and join['sql_report_literal'] == '{}')
scope = json.loads((O / 'ORIGINAL_SCOPE_CHECKS.json').read_bytes())
check(scope['author_math_checkers_present'] is False
      and scope['counterexample_construction_independently_verified'] is False
      and scope['full_2008_article_inspected'] is False)
check(scope['original_attempt_budget'] == {'used': 0, 'maximum': 5, 'turn_file_bytes': 0})
check(len({r['absolute_path'] for r in external}) == len(external))
index = {'schema': 'pr53-model-theory-fixed-external-inputs/v1',
         'original_manifest_sha256': EXPECTED_MF, 'references': sorted(external,
         key=lambda x: x['absolute_path']), 'original_root_actual_captures': capture_facts,
         'original_custody_is_not_root_mathematical_approval': True,
         'root_approval': False}
out = F / 'FIXED_EXTERNAL_INPUTS.json'
with out.open('x') as f:
    f.write(json.dumps(index, indent=2) + '\n')
print(json.dumps({'status': 'PASS_SCOPE_AND_CUSTODY_ONLY', 'assertions': checks,
                  'original_fixed_files': 174, 'external_fixed_references': len(external),
                  'original_actual_root_pids': [x['pid'] for x in capture_facts],
                  'raw_prior_report_key_present': False, 'selected_sql_report_type': 'text',
                  'selected_sql_report_literal': '{}', 'original_author_math_checker_present': False,
                  'original_substantive_attempts': 0, 'full_diff_files': 12,
                  'historical_gabber_construction_reproduced': False,
                  'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'root_approval': False}, indent=2, sort_keys=True))
