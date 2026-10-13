#!/usr/bin/env python3
"""Selected PR50 read-only observations; writes only this new plan directory."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

REPO = Path('/Users/alec/Documents/Math')
OUT = REPO / 'draft_pr_publication_program_20260930/audits/pr50_10600042/native_acceptance_plan_20261004'
A50 = REPO / 'draft_pr_publication_program_20260930/audits/pr50_10600042'
HEAD = '7260315f8b8b193020c09d4ef6df9d943a3a13ff'
ID = '10600042'
NATIVE = REPO / 'unsolved_math_prioritization'
CAP = OUT / 'actual_readonly_observation'
SNAP = OUT / 'source_snapshots'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def binding(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': digest(data),
            'full_mode': stat.S_IMODE(path.stat().st_mode)}

def snapshot(path, destination):
    data = path.read_bytes()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise RuntimeError('Refuse snapshot overwrite: ' + str(destination))
    destination.write_bytes(data)
    return {'source': binding(path), 'snapshot': binding(destination)}

commands = []
def run(name, argv):
    n = len(commands) + 1
    prefix = CAP / f'{n:02d}_{name}'
    started = utc()
    env = os.environ.copy()
    env['GIT_OPTIONAL_LOCKS'] = '0'
    proc = subprocess.Popen(argv, cwd=REPO, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    ended = utc()
    op = Path(str(prefix) + '.stdout.bin')
    ep = Path(str(prefix) + '.stderr.bin')
    op.write_bytes(out)
    ep.write_bytes(err)
    receipt = {'name': name, 'argv': argv, 'cwd': str(REPO),
               'parent_pid': os.getpid(), 'child_pid': proc.pid,
               'started_utc': started, 'ended_utc': ended,
               'exit_code': proc.returncode, 'GIT_OPTIONAL_LOCKS': '0',
               'stdout': binding(op), 'stderr': binding(ep)}
    write_json(Path(str(prefix) + '.COMMAND.json'), receipt)
    commands.append(receipt)
    if proc.returncode:
        raise RuntimeError('Read-only command failed: ' + name)
    return out

def selected(rows):
    if isinstance(rows, dict):
        if ID in rows:
            return rows[ID]
        for key in ('records', 'problems', 'results', 'assessments', 'entries'):
            if key in rows:
                return selected(rows[key])
    if isinstance(rows, list):
        result = [r for r in rows if isinstance(r, dict) and str(r.get('id')) == ID]
        if len(result) == 1:
            return result[0]
    raise RuntimeError('Expected exactly one selected record')

def selected_history(path):
    result = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if str(item.get('id')) == ID or str(item.get('problem_id')) == ID:
            result.append(item)
    return result

if OUT.resolve() != Path(__file__).resolve().parent:
    raise RuntimeError('Unexpected script location')
if CAP.exists() or SNAP.exists():
    raise RuntimeError('Refuse to overwrite a prior capture')
CAP.mkdir()
SNAP.mkdir()
source = Path(__file__).read_bytes()
(CAP / 'PRELAUNCH_SOURCE.py').write_bytes(source)
started = utc()
write_json(CAP / 'PRELAUNCH.json', {'started_utc': started, 'pid': os.getpid(),
           'script': binding(Path(__file__)), 'source_snapshot': binding(CAP / 'PRELAUNCH_SOURCE.py'),
           'write_boundary': str(OUT), 'read_only_repository_operations': True})

snapshots = []
for path, name in [
    (REPO / 'AGENTS.md', 'root_AGENTS.md'),
    (NATIVE / 'AGENTS.md', 'unsolved_AGENTS.md'),
    (NATIVE / 'README.md', 'unsolved_README.md'),
    (NATIVE / 'QUEUE.md', 'native_QUEUE.md'),
    (NATIVE / 'state.json', 'native_state.json'),
    (NATIVE / 'history.jsonl', 'native_history.jsonl'),
    (NATIVE / 'manifest.json', 'dataset_manifest.json'),
    (NATIVE / 'review_v2/related_target_groups.json', 'related_target_groups.json'),
    (A50 / 'ORIGINAL_MANIFEST.json', 'ORIGINAL_MANIFEST.json'),
    (A50 / 'SELECTED_SOURCE_INVENTORY.json', 'prior_selected_inventory.json'),
    (A50 / 'ROOT_FINAL_SUBMISSION_DECISION.json', 'dated_ROOT_FINAL_SUBMISSION_DECISION.json'),
    (A50 / 'publication_package_v1/zenodo-deposit.json', 'final_zenodo-deposit.json'),
    (A50 / 'publication_package_v1/README.md', 'final_README.md'),
    (Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md'), 'goal-objective.md'),
]:
    snapshots.append(snapshot(path, SNAP / name))

original = json.loads((SNAP / 'ORIGINAL_MANIFEST.json').read_text())
if original['head'] != HEAD or original['files_count'] != 15:
    raise RuntimeError('Original head/count mismatch')
ref_text = run('refs_before', ['git', 'rev-parse', 'HEAD', 'refs/heads/main', 'refs/remotes/origin/main']).decode()
refs = ref_text.splitlines()
branch = run('branch', ['git', 'branch', '--show-current']).decode().strip()
remote = run('remote_main', ['git', 'ls-remote', 'origin', 'refs/heads/main']).decode().strip()
pr = json.loads(run('pr50_metadata', ['gh', 'pr', 'view', '50', '--json',
        'number,url,state,isDraft,headRefOid,baseRefName,baseRefOid,mergeable,mergeStateStatus']))
if pr['headRefOid'] != HEAD or pr['state'] != 'OPEN' or not pr['isDraft']:
    raise RuntimeError('Selected PR identity/eligibility changed')
mergebase = run('mergebase', ['git', 'merge-base', refs[0], HEAD]).decode().strip()
changed_pr = run('changed_pr', ['git', 'diff', '--name-status', mergebase, HEAD]).decode()
changed_main = run('changed_main_selected_paths', ['git', 'diff', '--name-status', mergebase,
    refs[0], '--', 'unsolved_math_prioritization/QUEUE.md', 'unsolved_math_prioritization/attempts/10600042']).decode()
tree = run('original_scientific_tree', ['git', 'ls-tree', '-r', HEAD, '--',
    'unsolved_math_prioritization/attempts/10600042']).decode()
head_queue = run('exact_head_queue', ['git', 'show', HEAD + ':unsolved_math_prioritization/QUEUE.md']).decode()
head_rows = [line for line in head_queue.splitlines() if '| 10600042 /' in line]
native_queue = (SNAP / 'native_QUEUE.md').read_text()
native_rows = [line for line in native_queue.splitlines() if '| 10600042 /' in line]
if len(head_rows) != 1 or len(native_rows) != 1 or head_rows[0].split('|')[8].strip() != 'claimed_solved':
    raise RuntimeError('Selected queue eligibility mismatch')
index_paths = run('index_paths', ['git', 'diff', '--cached', '--name-status']).decode()
dirty_paths = run('worktree_paths', ['git', 'diff', '--name-status']).decode()
target_tracking = run('target_tracking', ['git', 'ls-files', '--stage', '--',
    'unsolved_math_prioritization/attempts/10600042']).decode()

tree_records = {}
for line in tree.splitlines():
    metadata, path = line.split('\t', 1)
    mode, typ, blob = metadata.split()
    tree_records[path] = (mode, typ, blob)
table = []
if len(tree_records) != 15:
    raise RuntimeError('Unexpected original tree file count')
for entry in original['files']:
    path = A50 / 'original' / entry['path']
    body = path.read_bytes()
    mode, typ, blob = tree_records[entry['original_git_path']]
    git_body = run('original_blob_' + entry['path'].replace('/', '_').replace('.', '_'),
                   ['git', 'cat-file', 'blob', blob])
    if body != git_body or digest(body) != entry['sha256'] or len(body) != entry['bytes']:
        raise RuntimeError('Original bytes mismatch: ' + entry['path'])
    if mode != entry['git_mode'] or blob != entry['git_blob_sha1'] or typ != 'blob':
        raise RuntimeError('Original tree mismatch: ' + entry['path'])
    snapshots.append(snapshot(path, SNAP / 'original' / entry['path']))
    table.append({'canonical_path': entry['original_git_path'], 'git_blob': blob,
        'git_mode': mode, 'sha256': digest(body), 'bytes': len(body),
        'custody_path': str(path), 'custody_full_mode': stat.S_IMODE(path.stat().st_mode),
        'current_worktree_path_exists': (REPO / entry['original_git_path']).exists()})

selected_sources = {}
source_bindings = []
for filename in ('catalog.json', 'assessments.json', 'cache/problems.json', 'cache/research_results.json'):
    path = NATIVE / filename
    data = path.read_bytes()
    source_bindings.append(binding(path))
    parsed = json.loads(data)
    if filename == 'cache/research_results.json':
        record = parsed['AMR-105-0042']
    else:
        record = selected(parsed)
    name = filename.replace('/', '__')
    write_json(SNAP / ('selected_' + name), record)
    selected_sources[filename] = record
assessment_history = selected_history(NATIVE / 'assessment_history.jsonl')
write_json(SNAP / 'selected_assessment_history.json', assessment_history)
source_bindings.append(binding(NATIVE / 'assessment_history.jsonl'))
native_state = json.loads((SNAP / 'native_state.json').read_text())
states = native_state.get('problems', native_state.get('records', native_state))
if not isinstance(states, dict):
    raise RuntimeError('Unexpected state schema')
native_selected = states.get(ID)
history_selected = selected_history(SNAP / 'native_history.jsonl')
turns = [json.loads(line) for line in (SNAP / 'original/turns.jsonl').read_text().splitlines() if line.strip()]
status = json.loads((SNAP / 'original/status.json').read_text())
record = json.loads((SNAP / 'original/source_record.json').read_text())
groups = json.loads((SNAP / 'related_target_groups.json').read_text())
selected_groups = [g for g in (groups if isinstance(groups, list) else groups.get('groups', []))
                   if ID in json.dumps(g)]
package = {}
for filename in ('even_strand_markov.tex', 'even_strand_markov.pdf',
                 'even-strand-markov-verification-v1.zip', 'zenodo-deposit.json'):
    package[filename] = binding(A50 / 'publication_package_v1' / filename)
refs_after = run('refs_after', ['git', 'rev-parse', 'HEAD', 'refs/heads/main', 'refs/remotes/origin/main']).decode().splitlines()
observations = {'schema': 'pr50-readonly-native-acceptance-observation/v1',
    'started_utc': started, 'ended_utc': utc(), 'actual_pid': os.getpid(),
    'branch': branch, 'refs_before': refs, 'refs_after': refs_after,
    'refs_stable_during_observation': refs == refs_after, 'remote_main': remote,
    'pr50': pr, 'original_head': HEAD, 'actual_merge_base': mergebase,
    'changed_paths_original_pr': changed_pr, 'changed_main_selected_paths_since_base': changed_main,
    'original_files': table, 'original_files_count': len(table),
    'head_selected_queue_row': head_rows[0], 'native_selected_queue_row': native_rows[0],
    'native_selected_state': native_selected, 'native_selected_history': history_selected,
    'state_schema_top_keys': list(native_state), 'native_state_entries': len(states),
    'native_total_turns': sum(v.get('turns_used', 0) for v in states.values() if isinstance(v, dict)),
    'original_status': status, 'original_turn_ledger': turns, 'original_source_record': record,
    'current_selected_sources': selected_sources, 'selected_assessment_history': assessment_history,
    'selected_related_groups': selected_groups, 'large_source_bindings_only': source_bindings,
    'package_bindings_dated_only': package, 'index_paths_dated_only': index_paths,
    'foreign_worktree_paths_dated_only': dirty_paths, 'target_tracking': target_tracking,
    'source_snapshots': snapshots, 'math_or_priority_approval_conferred': False,
    'publication_acceptance_or_merge_performed': False,
    'repository_writes_by_this_helper': [], 'only_written_directory': str(OUT)}
write_json(OUT / 'OBSERVATIONS.json', observations)
write_json(CAP / 'COMPLETE_COMMANDS.json', commands)
write_json(CAP / 'RECEIPT.json', {'schema': 'pr50-actual-readonly-capture/v1',
    'actual_pid': os.getpid(), 'started_utc': started, 'ended_utc': utc(),
    'script': binding(Path(__file__)), 'prelaunch_source': binding(CAP / 'PRELAUNCH_SOURCE.py'),
    'all_commands_exit_zero': all(x['exit_code'] == 0 for x in commands),
    'command_count': len(commands), 'observations': binding(OUT / 'OBSERVATIONS.json'),
    'full_stdout_stderr_preserved': True, 'repository_writes': []})
print(json.dumps({'status': 'READONLY_OBSERVATION_COMPLETE', 'pid': os.getpid(),
    'original_files': len(table), 'commands': len(commands), 'merge_base': mergebase,
    'branch': branch, 'native_selected_state': native_selected,
    'native_selected_history_count': len(history_selected)}))
