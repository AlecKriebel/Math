"""Bind an explicitly root-authored provisional decision; infer no mathematics.

Root-only serial writer. No PR, branch, publication or spreadsheet mutations.
The existing numerical journal enforces cursor continuity. Scientific review
and all irreversible-action duplicate checks remain separate requirements.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess

from record_decision import record
from record_missing_status_stable import read_live_pr
from sweep_io import atomic_json

ROOT = Path(__file__).resolve().parent


def capture(pr, problem_ids, classification, reason, duplicate_check,
            scope_text, read_scope, disposition='independent_review_required'):
    if type(pr) is not int or pr < 9:
        raise RuntimeError('Invalid PR number')
    if not problem_ids or any(not re.fullmatch(r'[0-9]+', s) for s in problem_ids):
        raise RuntimeError('Explicit numeric problem identifiers required')
    if not all(type(s) is str and s.strip() for s in
               (classification, reason, duplicate_check, scope_text)):
        raise RuntimeError('Root-authored substantive descriptions required')
    state = json.loads((ROOT/'STATE.json').read_bytes())
    if state['next_pr'] != pr:
        raise RuntimeError('Root decision must follow the numerical cursor')
    inventory = json.loads((ROOT/'rest_inventory.json').read_bytes())
    metadata = next(p for p in inventory['pull_requests'] if p['number'] == pr)
    evidence = json.loads((ROOT/f'eligibility/pr{pr:04d}.json').read_bytes())
    pinned = json.loads((ROOT/f'PR{pr:04d}_PINNED_SCOPE_VERIFICATION.json').read_bytes())
    head = evidence['inventory_head_sha']
    if not (head == metadata['headRefOid'] == pinned['head']
            and pinned['all_complete_paths_equal'] and pinned['all_added_rows_equal']
            and not pinned['added_queue_rows']):
        raise RuntimeError('Exact missing-status path binding required')
    leads = json.loads((ROOT/f'PR{pr:04d}_PUBLICATION_LEADS.json').read_bytes())
    if leads['pr'] != pr:
        raise RuntimeError('Publication preflight belongs to another PR')
    blobs = []
    for item in evidence['files']:
        blob = subprocess.check_output(
            ['git', 'rev-parse', head+':'+item['filename']], text=True).strip()
        if item['sha'] is not None and blob != item['sha']:
            raise RuntimeError('Actual head blob drift: '+item['filename'])
        blobs.append({'path': item['filename'], 'blob': blob})
    if len(blobs) != pinned['path_count']:
        raise RuntimeError('Incomplete head inventory')
    live = read_live_pr(pr)
    if live['head']['sha'] != head or (live.get('body') or '') != (metadata.get('body') or ''):
        raise RuntimeError('Live head/body changed; root must reread')
    audit = ROOT/'audits'/f'pr{pr:04d}_{problem_ids[0]}'
    audit.mkdir(exist_ok=True)
    scope = audit/'ROOT_SCOPE.md'
    binding = audit/'ROOT_INPUT_BINDING.json'
    if scope.exists() or binding.exists():
        raise RuntimeError('Existing root evidence must not be overwritten')
    scope.write_text(scope_text.rstrip()+'\n')
    atomic_json(binding, {
        'at': dt.datetime.now(dt.timezone.utc).isoformat(), 'pr': pr,
        'head': head, 'blobs': blobs, 'live_state': live['state'],
        'draft': live['draft'], 'merged': live['merged'],
        'body_sha256': hashlib.sha256((live.get('body') or '').encode()).hexdigest(),
        'root_authored_read_scope': read_scope,
        'preflight_checked_at': leads['checked_at'],
        'helper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'inference_performed_by_helper': False,
    })
    return record(pr, {
        'problem_ids': problem_ids, 'explicit_pr_queue_statuses': [],
        'current_classification': classification, 'disposition': disposition,
        'missing_status_examined': True, 'scientific_final': False,
        'reason': reason, 'duplicate_check': duplicate_check,
        'audit_folder': str(audit.relative_to(ROOT)),
    })
