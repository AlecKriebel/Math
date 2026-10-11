#!/usr/bin/env python3
"""Read-only original-stage provenance and isolated original code replay."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import sys

OWN = Path(__file__).resolve().parent
AUDIT = OWN.parent
ROOT = OWN.parents[3]
HEAD = '53b6e68be6d2cc5966c25746618951d5dae2183b'
MERGEBASE = '60292bed09f59236aa192cb17aa138f7b4750e1a'
ATTEMPT = 'unsolved_math_prioritization/attempts/30003955'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def command(*args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, check=True).stdout


def file_hashes():
    paths = [ROOT/'unsolved_math_prioritization'/p for p in ['QUEUE.md', 'state.json', 'history.jsonl', 'assessment_history.jsonl', 'update_history.jsonl']]
    paths += list((AUDIT/'source_snapshot').rglob('*'))
    return {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in paths if p.is_file()}


def run():
    before = file_hashes()
    manifest = json.loads((AUDIT/'snapshot_manifest.json').read_text())
    branch = command('git', 'branch', '--show-current').decode().strip()
    assert branch == 'main'
    read_receipts = []
    for entry in manifest['files']:
        raw = (AUDIT/'source_snapshot'/entry['path']).read_bytes()
        blob = command('git', 'show', f'{HEAD}:{ATTEMPT}/{entry["path"]}')
        assert raw == blob
        assert sha(raw) == entry['sha256']
        assert len(raw) == entry['bytes']
        blob_oid = command('git', 'rev-parse', f'{HEAD}:{ATTEMPT}/{entry["path"]}').decode().strip()
        assert blob_oid == entry['git_blob_sha1']
        read_receipts.append({'path': entry['path'], 'sha256': sha(raw), 'bytes': len(raw), 'exact_git_blob': blob_oid, 'verified_equal': True})
    assert len(read_receipts) == 15
    diff = command('git', 'diff', '--no-ext-diff', MERGEBASE, HEAD)
    (OWN/'original_exact16_diff.patch').write_bytes(diff)
    names = command('git', 'diff', '--no-ext-diff', '--name-only', MERGEBASE, HEAD).decode().splitlines()
    assert names == manifest['changed_paths'] and len(names) == 16
    assert command('git', 'merge-base', MERGEBASE, HEAD).decode().strip() == MERGEBASE
    before_paths = command('git', 'ls-tree', '-r', '--name-only', MERGEBASE, ATTEMPT).decode().splitlines()
    assert not before_paths
    frozen_metadata = json.loads((AUDIT/'pr_input'/'pr.json').read_text())
    live_raw = command('gh', 'pr', 'view', '30', '--json', 'number,title,body,url,state,isDraft,headRefName,headRefOid,baseRefName,baseRefOid,commits,files')
    (OWN/'pr_metadata_readonly.json').write_bytes(live_raw)
    live = json.loads(live_raw)
    assert live['headRefOid'] == HEAD
    assert live['isDraft'] and live['state'] == 'OPEN'
    assert [x['path'] for x in live['files']] == names
    # Re-read the frozen original metadata. It may report an advanced base tip;
    # neither that tip nor the live tip substitutes for the true merge base.
    ledger = [json.loads(line) for line in (AUDIT/'source_snapshot'/'turns.jsonl').read_text().splitlines()]
    ready = json.loads((AUDIT/'source_snapshot'/'readiness.json').read_text())
    assert [x['turn'] for x in ledger] == [1, 2]
    assert all(x['full_target_resolved'] is False for x in ledger)
    assert ready['used_substantive_attempts'] == 2 and ready['maximum_substantive_attempts'] == 5
    assert ready['full_target_resolved'] is False
    head_queue = command('git', 'show', f'{HEAD}:unsolved_math_prioritization/QUEUE.md').decode()
    head_row = next(line for line in head_queue.splitlines() if '| 30003955 /' in line)
    assert '| unsolved | 2/5 |' in head_row
    main_row = next(line for line in (ROOT/'unsolved_math_prioritization/QUEUE.md').read_text().splitlines() if '| 30003955 /' in line)
    assert '| queued | 0/5 |' in main_row
    # Main's pre-merge row does not disprove the original branch's 2/5 ledger.
    temporary = OWN/'tmp'/'original_replay'
    if temporary.exists():
        shutil.rmtree(temporary)
    shutil.copytree(AUDIT/'source_snapshot', temporary)
    replays = []
    for stem, script, output in [
        ('original31', temporary/'check_monodromy.py', temporary/'check_results.json'),
        ('old_independent', temporary/'review'/'independent_checks.py', temporary/'review'/'independent_results.json'),
    ]:
        retained = output.read_bytes()
        proc = subprocess.run([sys.executable, str(script)], cwd=temporary, capture_output=True)
        (OWN/f'{stem}_stdout.txt').write_bytes(proc.stdout)
        (OWN/f'{stem}_stderr.txt').write_bytes(proc.stderr)
        generated = output.read_bytes()
        (OWN/f'{stem}_replayed_results.json').write_bytes(generated)
        replays.append({'suite': stem, 'returncode': proc.returncode, 'stdout_sha256': sha(proc.stdout), 'stderr_sha256': sha(proc.stderr), 'stderr_bytes': len(proc.stderr), 'saved_output_sha256': sha(retained), 'replayed_output_sha256': sha(generated), 'byte_identical_to_original': retained == generated, 'json_equal_to_original': json.loads(retained) == json.loads(generated), 'assertions': json.loads(generated)['assertions']})
        assert proc.returncode == 0 and retained == generated
    after = file_hashes()
    assert before == after
    result = {
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'all_passed': True,
        'source_head': HEAD,
        'actual_mergebase': MERGEBASE,
        'frozen_metadata_base_tip': frozen_metadata.get('baseRefOid'),
        'live_metadata_base_tip': live.get('baseRefOid'),
        'branch': branch,
        'all15_snapshot_files_match_exact_original_git': read_receipts,
        'exact16_changed_paths': names,
        'original_exact_diff_sha256': sha(diff),
        'head_queue_row': head_row,
        'main_premerge_queue_row': main_row,
        'attempt_accounting': {'ledger_entries': len(ledger), 'maximum': 5, 'no_new_attempts': True, 'audit_is_verification_only': True},
        'replays': replays,
        'snapshot_and_shared_ledger_hashes_unchanged': True,
        'before_shared_and_snapshot_hashes': before,
        'scope_corrections': [
            'Original PR body incorrectly says all changes are confined to attempt folder: QUEUE.md also changed.',
            'Frozen PARTIAL pending-review status is historically preserved; a superseding review-status addendum should explain the later original review and current audit.',
        ],
        'original_and_live_pr_bodies_match': frozen_metadata.get('body') == live.get('body'),
        'no_git_or_github_mutation': True,
    }
    (OWN/'original_replay_and_integrity.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['all_passed', 'source_head', 'actual_mergebase', 'frozen_metadata_base_tip', 'live_metadata_base_tip', 'attempt_accounting', 'replays', 'snapshot_and_shared_ledger_hashes_unchanged', 'scope_corrections']}, indent=2))


if __name__ == '__main__':
    run()
