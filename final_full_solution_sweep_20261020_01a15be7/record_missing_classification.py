"""Capture a root-authored missing-QUEUE eligibility decision; infer nothing."""
import datetime as dt
import hashlib
import json
import subprocess
import time
from pathlib import Path

from record_decision import record

ROOT = Path(__file__).resolve().parent


def read_live_pr(pr):
    """Retry transient read-only gateway failures before recording anything."""
    for attempt in range(4):
        try:
            return json.loads(subprocess.check_output(
                ['gh', 'api', f'repos/AlecKriebel/Math/pulls/{pr}'],
                stderr=subprocess.PIPE))
        except subprocess.CalledProcessError as exc:
            message = (exc.stderr or b'').decode(errors='replace')
            if attempt == 3 or not any(code in message for code in
                                      ('HTTP 502', 'HTTP 503', 'HTTP 504')):
                raise
            time.sleep(2 ** attempt)


def capture(pr, problem_ids, classification, reason, read_files, scope_file,
            expected_scope, duplicate_check=None):
    """Bind a manually reviewed negative classification to actual immutable inputs.

    This helper does not decide whether a theorem is full, correct, original or
    published. The root must read the PR and sufficient actual scope documents,
    supply the precise reason, and use another workflow for any full candidate.
    """
    evidence = json.loads((ROOT / f'eligibility/pr{pr:04d}.json').read_text())
    pinned = json.loads((ROOT / f'PR{pr:04d}_PINNED_SCOPE_VERIFICATION.json').read_text())
    head = evidence['inventory_head_sha']
    if not (pinned['head'] == head and pinned['all_complete_paths_equal']
            and pinned['all_added_rows_equal'] and not pinned['added_queue_rows']):
        raise RuntimeError('Missing-status decision lacks exact no-QUEUE binding')
    checks = []
    for item in evidence['files']:
        blob = subprocess.check_output(
            ['git', 'rev-parse', head + ':' + item['filename']], text=True).strip()
        if item['sha'] is not None and blob != item['sha']:
            raise RuntimeError('Actual head blob differs: ' + item['filename'])
        checks.append({'path': item['filename'], 'actual_head_blob': blob,
                       'cached_blob': item['sha'],
                       'cached_equal_or_missing_rebound': True})
    if len(checks) != pinned['path_count']:
        raise RuntimeError('Incomplete actual-head inventory')
    readings = []
    for path in read_files:
        body = subprocess.check_output(['git', 'show', head + ':' + path])
        readings.append({'path': path, 'bytes': len(body),
                         'sha256': hashlib.sha256(body).hexdigest()})
    scope = json.loads(subprocess.check_output(['git', 'show', head + ':' + scope_file]))
    for key, expected in expected_scope.items():
        if key not in scope or type(scope[key]) is not type(expected) or scope[key] != expected:
            raise RuntimeError('Manually expected scope field differs: ' + key)
    live = read_live_pr(pr)
    if live['head']['sha'] != head:
        raise RuntimeError('Live head changed; rereview required')
    duplicate_check = duplicate_check or (
        'Not required for this ineligible partial/prior application claim; '
        'no substantive proof/priority audit or publication performed.')
    name = f'PR{pr:04d}_MISSING_STATUS_CLASSIFICATION.json'
    receipt = {
        'at': dt.datetime.now(dt.timezone.utc).isoformat(), 'pr': pr, 'head': head,
        'current_live_state': live['state'], 'merged': live['merged'], 'draft': live['draft'],
        'complete_paths': len(checks), 'blob_checks': checks,
        'missing_QUEUE_status': True, 'scope_fields': scope,
        'read_for_eligibility': ['PR description', *readings],
        'inferred_status': classification, 'reason': reason,
        'classification_is_root_authored_not_automatically_inferred': True,
        'new_mathematical_or_priority_audit': False,
        'duplicate_check': duplicate_check, 'provider_mutations': False,
    }
    (ROOT / name).write_text(json.dumps(receipt, indent=2) + '\n')
    result = record(pr, {
        'problem_ids': problem_ids, 'explicit_pr_queue_statuses': [],
        'current_classification': classification,
        'disposition': 'skip_inferred_non_claimed_solved', 'reason': reason,
        'duplicate_check': duplicate_check, 'classification_evidence': name,
        'missing_status_examined': True,
    })
    with (ROOT / 'checkpoint.py').open('a') as stream:
        stream.write('\nNAMES.extend(' + repr([
            f'PR{pr:04d}_PINNED_SCOPE_VERIFICATION.json', name]) + ')\n')
    return result
