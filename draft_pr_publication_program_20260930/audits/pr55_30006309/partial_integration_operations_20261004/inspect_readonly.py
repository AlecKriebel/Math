"""Actual read-only PR55/native/source inspection; writes only its own evidence.

This is evidence of observation, not ROOT approval or execution permission.
No ref fetch, Git lock/index write, native file write or remote mutation occurs.
"""
import base64
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import subprocess

ID = '30006309'
HEAD = '85c78d0cf3959d9d492a637cb90835ebc6a0e828'
PREFIX = 'unsolved_math_prioritization/attempts/' + ID
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
GOAL = Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')

def sha(b): return hashlib.sha256(b).hexdigest()
def must(ok, msg):
    if not ok: raise RuntimeError(msg)
def jbytes(v): return (json.dumps(v, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()

def main():
    own = Path(__file__).resolve().parent
    audit = own.parent
    repo = own.parents[3]
    actual = own / 'private' / 'actual_readonly_inspection'
    must(not actual.exists(), 'Do not overwrite an actual observation')
    actual.mkdir(parents=True)
    (actual / 'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    commands = []
    def run(argv, allowed=(0,)):
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        proc = subprocess.Popen(argv, cwd=repo, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        n = str(len(commands) + 1)
        (actual / (n + '.stdout')).write_bytes(out)
        (actual / (n + '.stderr')).write_bytes(err)
        commands.append({'argv': argv, 'actual_pid': proc.pid, 'started_UTC': start,
                         'finished_UTC': dt.datetime.now(dt.timezone.utc).isoformat(), 'exit_code': proc.returncode,
                         'stdout_sha256': sha(out), 'stderr_sha256': sha(err)})
        (actual / 'COMMANDS.json').write_bytes(jbytes(commands))
        must(proc.returncode in allowed, 'Read command failed; actual output preserved privately')
        return out, proc.returncode
    def git(*a): return run(['git', '--no-optional-locks', *a])[0]
    def pin(p):
        p = p.resolve()
        b = p.read_bytes()
        return {'path': str(p), 'bytes': len(b), 'sha256': sha(b), 'mode': oct(stat.S_IMODE(p.stat().st_mode))}
    auth_path = audit / 'original_preparation_family/ORIGINAL_AUTHENTICATION.json'
    auth = json.loads(auth_path.read_bytes())
    must(auth['original_head'] == HEAD and auth['original_science_file_count'] == 16, 'Original domain differs')
    for item in auth['original_science_files']:
        body = Path(item['local_path']).read_bytes()
        must(len(body) == item['bytes'] and sha(body) == item['sha256'], 'Original source cache differs')
        blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        must(blob == item['git_blob_sha1'] and item['git_mode'] == '100644', 'Original blob/mode differs')
    pr = json.loads(run(['gh', 'pr', 'view', '55', '--repo', 'AlecKriebel/Math', '--json',
                         'number,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,url'])[0])
    files = json.loads(run(['gh', 'api', 'repos/AlecKriebel/Math/pulls/55/files?per_page=100'])[0])
    api_queue = json.loads(run(['gh', 'api', 'repos/AlecKriebel/Math/contents/' + QUEUE + '?ref=' + HEAD])[0])
    submitted_queue = base64.b64decode(api_queue['content'])
    actual_blob = hashlib.sha1(b'blob ' + str(len(submitted_queue)).encode() + b'\0' + submitted_queue).hexdigest()
    must(actual_blob == api_queue['sha'] == auth['original_queue_destination_blob_sha1'], 'Current original queue blob differs')
    row = [s for s in submitted_queue.decode().splitlines() if '| ' + ID + ' /' in s]
    must(len(row) == 1, 'Current original target row not unique')
    cells = row[0].split('|')
    branch = git('branch', '--show-current').decode().strip()
    local = git('rev-parse', 'HEAD').decode().strip()
    remote = git('ls-remote', '--heads', 'origin', 'main').decode().split()[0]
    staged = git('diff', '--cached', '--name-only', '-z').split(b'\0')
    dirty = [p.decode() for p in git('diff', '--name-only', '-z').split(b'\0') if p]
    original_available = run(['git', '--no-optional-locks', 'cat-file', '-e', HEAD + '^{commit}'], allowed=(0,128))[1] == 0
    original = json.loads((audit / 'original_preparation_family/original/source_record.json').read_bytes())
    manifest = json.loads((repo / 'unsolved_math_prioritization/manifest.json').read_bytes())
    raw_pins = []
    for name in ('problems.json', 'research_results.json'):
        p = repo / 'unsolved_math_prioritization/cache' / name
        b = p.read_bytes()
        must({'bytes': len(b), 'sha256': sha(b)} == manifest['files'][name], 'Raw corpus manifest mismatch')
        raw_pins.append(pin(p))
    problems = json.loads((repo / 'unsolved_math_prioritization/cache/problems.json').read_bytes())
    matches = [p for p in problems if str(p['id']) == ID]
    must(len(matches) == 1 and matches[0] == original['problem'], 'Unique raw selected problem differs')
    code = original['problem']['problem_number']
    reports = json.loads((repo / 'unsolved_math_prioritization/cache/research_results.json').read_bytes())
    must(code not in reports, 'Selected raw report is no longer absent')
    with sqlite3.connect('file:' + str(repo / 'unsolved_math_prioritization/cache/catalog.sqlite') + '?mode=ro', uri=True) as db:
        selected = db.execute('SELECT payload,report FROM records WHERE key=?', (ID,)).fetchone()
        revision = db.execute('SELECT revision FROM metadata').fetchall()
    must(selected is not None and json.loads(selected[0]) == original['problem'], 'Selected SQL problem differs')
    must(selected[1] is not None and selected[1] == '{}' and json.loads(selected[1]) == {}, 'SQL report is not the exact empty-object fallback')
    must(original['upstream_report'] is None, 'Original wrapper null placeholder differs')
    must(revision == [(manifest['revision'],)], 'SQL revision differs')
    pair_hash = sha(json.dumps([original['problem'], {}], sort_keys=True).encode())
    wrapper_hash = sha(json.dumps([original['problem'], None], sort_keys=True).encode())
    catalog = [p for p in json.loads((repo / 'unsolved_math_prioritization/catalog.json').read_bytes()) if p['id'] == ID]
    must(len(catalog) == 1 and catalog[0]['review_hash'] == pair_hash, 'Catalog selected hash differs')
    state = json.loads((repo / 'unsolved_math_prioritization/state.json').read_bytes())
    history = (repo / 'unsolved_math_prioritization/history.jsonl').read_bytes()
    native_rows = [s for s in (repo / QUEUE).read_text().splitlines() if '| ' + ID + ' /' in s]
    must(len(native_rows) == 1, 'Native target row not unique')
    expected_paths = {QUEUE} | {x['repository_path'] for x in auth['original_science_files']}
    result = {'schema': 'pr55-partial-operation-readonly-inspection/v1', 'UTC': dt.datetime.now(dt.timezone.utc).isoformat(),
              'actual_pid': os.getpid(), 'source': pin(Path(__file__)), 'goal': pin(GOAL), 'PR': pr,
              'literal_current_submitted_status': cells[8].strip(), 'literal_current_submitted_budget': cells[9].strip(),
              'eligible_at_current_intake': pr['state'] == 'OPEN' and pr['headRefOid'] == HEAD and cells[8].strip() == 'claimed_solved',
              'submitted_queue_row': row[0], 'submitted_queue_sha256': sha(submitted_queue), 'submitted_queue_blob_SHA1': actual_blob,
              'current_changed_file_count': len(files), 'current_changed_paths_equal_17_authenticated_paths':
              {f['filename'] for f in files} == expected_paths, 'all_16_original_cache_bodies_sizes_and_git_blobs_verified': True,
              'native_branch': branch, 'native_main': local, 'remote_main': remote, 'current_main_remote_equal': local == remote,
              'staged_paths': [p.decode() for p in staged if p], 'foreign_dirty_tracked_path_count': len(dirty),
              'native_target_original_paths_present': [p for p in sorted(expected_paths - {QUEUE}) if (repo / p).exists()],
              'original_commit_currently_available_locally': original_available, 'native_target_queue_row': native_rows[0],
              'native_target_state_present': ID in state,
              'native_target_history_event_count': sum(str(json.loads(s).get('id')) == ID for s in history.splitlines()),
              'raw_report_key_present': False, 'raw_report_interpretation': 'ABSENT; no raw value',
              'SQL_report_is_NULL': False, 'SQL_report_literal': '{}', 'original_wrapper_upstream_report': None,
              'catalog_review_hash_for_SQL_typed_pair': pair_hash, 'wrapper_null_pair_hash_is_distinct': wrapper_hash,
              'current_catalog_selected': catalog[0], 'raw_corpus_pins': raw_pins,
              'writer_window_is_not_claimed': True, 'root_scope_decision_is_not_supplied': True,
              'source_only': True, 'Git_native_PR_paper_Zenodo_DOI_tracker_mutation': False,
              'new_central_proof_attempts': 0, 'preparation_percent': 35, 'dated_program_percent': 4.040404}
    out = own / 'READONLY_INSPECTION.json'
    must(not out.exists(), 'Inspection already exists')
    out.write_bytes(jbytes(result))
    print(json.dumps(result, indent=2))

if __name__ == '__main__': main()
