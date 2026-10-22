"""Bind a manually reviewed explicit claimed_solved candidate; infer no mathematics."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
from record_decision import record
from record_missing_status_stable import read_live_pr
from sweep_io import atomic_json
ROOT=Path(__file__).resolve().parent

def capture(pr,problem_ids,classification,reason,duplicate_check,scope_text,read_scope,disposition):
    state=json.loads((ROOT/'STATE.json').read_bytes())
    if type(pr)is not int or state['next_pr']!=pr:raise RuntimeError('Numerical cursor mismatch')
    if not problem_ids or any(type(x)is not str or not x.isascii() or not x.isdigit()for x in problem_ids):raise RuntimeError('Explicit identifiers required')
    if any(type(x)is not str or not x.strip()for x in [classification,reason,duplicate_check,scope_text,disposition]):raise RuntimeError('Root authored descriptions required')
    meta=next(p for p in json.loads((ROOT/'rest_inventory.json').read_bytes())['pull_requests']if p['number']==pr)
    evidence=json.loads((ROOT/f'eligibility/pr{pr:04d}.json').read_bytes())
    pin=json.loads((ROOT/f'PR{pr:04d}_PINNED_SCOPE_VERIFICATION.json').read_bytes())
    head=evidence['inventory_head_sha']
    if not(head==meta['headRefOid']==pin['head']and pin['all_complete_paths_equal']and pin['all_added_rows_equal']):raise RuntimeError('Pinned scope mismatch')
    rows=pin['added_queue_rows']
    for identifier in problem_ids:
        matching=[x for x in rows if str(x['problem_id'])==identifier]
        if not matching or any(x['status']!='claimed_solved'for x in matching):raise RuntimeError('Explicit claimed_solved status required')
    leads=json.loads((ROOT/f'PR{pr:04d}_PUBLICATION_LEADS.json').read_bytes())
    if leads['pr']!=pr:raise RuntimeError('Wrong publication preflight')
    blobs=[]
    for item in evidence['files']:
        blob=subprocess.check_output(['git','rev-parse',head+':'+item['filename']],text=True).strip()
        if item['sha']is not None and blob!=item['sha']:raise RuntimeError('Head blob mismatch')
        blobs.append({'path':item['filename'],'blob':blob})
    if len(blobs)!=pin['path_count']:raise RuntimeError('Incomplete path list')
    live=read_live_pr(pr)
    if live['head']['sha']!=head or(live.get('body')or'')!=(meta.get('body')or''):raise RuntimeError('Live head/body changed')
    a=ROOT/'audits'/f'pr{pr:04d}_{problem_ids[0]}';a.mkdir(exist_ok=True)
    if any((a/n).exists()for n in ['ROOT_SCOPE.md','ROOT_INPUT_BINDING.json']):raise RuntimeError('Preserve existing evidence')
    (a/'ROOT_SCOPE.md').write_text(scope_text.rstrip()+'\n')
    atomic_json(a/'ROOT_INPUT_BINDING.json',{'at':dt.datetime.now(dt.timezone.utc).isoformat(),'pr':pr,'head':head,'blobs':blobs,'actual_pinned_claimed_solved_rows':rows,'root_authored_read_scope':read_scope,'preflight_checked_at':leads['checked_at'],'live_state':live['state'],'draft':live['draft'],'merged':live['merged'],'live_body_sha256':hashlib.sha256((live.get('body')or'').encode()).hexdigest(),'helper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'mathematical_inference_performed_by_helper':False})
    return record(pr,{'problem_ids':problem_ids,'explicit_pr_queue_statuses':['claimed_solved'],'current_classification':classification,'disposition':disposition,'missing_status_examined':False,'scientific_final':False,'reason':reason,'duplicate_check':duplicate_check,'audit_folder':str(a.relative_to(ROOT))})
