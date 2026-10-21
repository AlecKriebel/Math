"""Independent read-only binding against immutable Git objects; own outputs only."""
from pathlib import Path
import datetime, hashlib, json, re, subprocess

O=Path(__file__).resolve().parent
REPO=O.parents[2]
I=O/'inputs'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args):
    return subprocess.check_output(['git',*args],cwd=REPO,stderr=subprocess.PIPE)
def save(p,b):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def row(line,path):
    if not line.startswith('|'): return None
    c=[s.strip() for s in line.split('|')[1:-1]]
    if len(c)<9 or not c[0].isdigit(): return None
    m=re.match(r'(\d+)(?:\s|/|$)',c[1])
    if not m:return None
    return {'queue_path':path,'source_line':line,'problem_id':m[1],'status':c[7]}
def key(x):return (x['queue_path'],x['source_line'],x['problem_id'],x['status'])

inv=json.loads((I/'rest_inventory.json').read_text())
prs={p['number']:p for p in inv['pull_requests']}
journal=[json.loads(s) for s in (I/'dispositions.jsonl').read_text().splitlines() if s.strip()]
pub={810,815,822,826}
results=[]
for n in range(790,833):
    p=prs[n];e=json.loads((I/f'eligibility/pr{n:04d}.json').read_text());d=json.loads((I/f'PR{n:04d}_DISPOSITION.json').read_text())
    out=O/f'git_inputs/pr{n:04d}';errors=[]
    identity=(e['pr']==n==d['pr'] and p['headRefOid']==e['inventory_head_sha']==d['inventory_head_sha'] and p['baseRefOid']==e['inventory_base_sha']==d['inventory_base_sha'] and p['state']==d['pr_state'] and sha(p['body'].encode())==d['inventory_body_sha256'])
    if not identity:errors.append('inventory/evidence/disposition identity')
    comparison=p['baseRefOid']+'...'+p['headRefOid']
    wire=git('diff','--no-ext-diff','--no-renames','--name-only','-z',comparison);save(out/'paths.nul',wire)
    paths=wire.decode().rstrip('\0').split('\0') if wire else []
    paths_ok=(len(paths)==len(set(paths))==e['file_count']==len(e['files']) and set(paths)==set(e['changed_paths']) and sorted(paths)==sorted(f['filename'] for f in e['files']))
    if not paths_ok:errors.append('complete path set')
    rows=[];blobs=[]
    for path in sorted(set(paths)&{'QUEUE.md','unsolved_math_prioritization/QUEUE.md'}):
        patch=git('diff','--no-ext-diff','--no-renames','--unified=0',comparison,'--',path);save(out/'QUEUE.patch',patch)
        b=git('show',p['headRefOid']+':'+path);save(out/'QUEUE.head.md',b)
        rows.extend(r for s in patch.decode().splitlines() if s.startswith('+') and not s.startswith('+++') if (r:=row(s[1:],path)))
        actual=git('rev-parse',p['headRefOid']+':'+path).decode().strip();cache=[x for x in e['queue_changes'] if x['path']==path]
        blobs.append({'path':path,'actual':actual,'cached':cache[0]['sha'] if len(cache)==1 else None,'equal':len(cache)==1 and actual==cache[0]['sha']})
    rows_ok=sorted(map(key,rows))==sorted(map(key,e['added_queue_rows']))
    if not rows_ok:errors.append('own added canonical rows')
    ids=sorted(set(x['problem_id'] for x in rows))
    if ids!=sorted(d['problem_ids']): errors.append('problem identities')
    if [x for x in journal if x.get('pr')==n]!=[d]: errors.append('journal exact single disposition')
    if d['new_mathematical_audit'] or d['new_publication'] or d['spreadsheet_mutation']:errors.append('unexpected new action flag')
    if n not in pub|{799}:
        if d['disposition']!='skip_explicit_non_claimed_solved' or any(x['status'] not in {'unsolved','already_solved'} for x in rows):errors.append('ordinary explicit negative')
        if [x['source_line'] for x in rows]!=d['queue_source_lines']:errors.append('negative stated row differs')
    if n not in pub and any(not b['equal'] for b in blobs): errors.append('nonpublic cached queue blob differs')
    science=[];merge=None
    if n in pub:
        m=p['mergeCommit']['oid']; parents=git('show','-s','--format=%P',m).decode().strip().split()
        merge_wire=git('diff','--no-ext-diff','--no-renames','--name-only','-z',m+'^1',m);save(out/'actual_merge_paths.nul',merge_wire)
        merge_paths=merge_wire.decode().rstrip('\0').split('\0') if merge_wire else []
        merge={'commit':m,'parents':parents,'first_parent_paths_equal':set(merge_paths)==set(paths),'path_count':len(merge_paths)}
        if len(parents)!=2 or parents[1]!=p['headRefOid'] or not merge['first_parent_paths_equal']:errors.append('actual merge binding')
        for f in e['files']:
            if f['filename'] in {'QUEUE.md','unsolved_math_prioritization/QUEUE.md'}:continue
            actual=git('rev-parse',p['headRefOid']+':'+f['filename']).decode().strip()
            science.append({'path':f['filename'],'actual':actual,'cached':f.get('sha'),'equal':actual==f['sha'] if f.get('sha') else None})
        if any(x['equal'] is False for x in science):errors.append('cached scientific blob differs')
        if n!=826 and any(not b['equal'] for b in blobs):errors.append('undisclosed queue mismatch')
    results.append({'pr':n,'head':p['headRefOid'],'base':p['baseRefOid'],'comparison':comparison,'identity_pass':identity,'paths':paths,'complete_paths_pass':paths_ok,'added_rows':rows,'added_rows_pass':rows_ok,'queue_blobs':blobs,'merge':merge,'scientific_blob_checks':science,'disposition':d['disposition'],'errors':errors,'pass':not errors})

canonical=json.loads((I/'CURRENT_CANONICAL_QUEUE_SNAPSHOT.json').read_text());commit=canonical['main'];path='unsolved_math_prioritization/QUEUE.md'
try:
    wire=git('show',commit+':'+path);save(O/'git_inputs/current_canonical_QUEUE.md',wire)
except subprocess.CalledProcessError:
    remote=json.loads((O/'git_inputs/canonical_queue_remote_receipt.json').read_text())
    wire=(O/'git_inputs/current_canonical_QUEUE.md').read_bytes()
    if remote['ref']!=commit or not remote['equal'] or sha(wire)!=remote['sha256']:raise RuntimeError('Canonical remote blob binding failed')
rows=[r for s in wire.decode().splitlines() if (r:=row(s,path)) and r['problem_id']=='30002364']
d799=json.loads((I/'PR0799_DISPOSITION.json').read_text()); live=json.loads((O/'private/pr0799.live.json').read_text()); comment=json.loads((O/'private/comment6223000406.live.json').read_text())
withdraw={'canonical_commit':commit,'actual_git_row':rows,'snapshot_row_equal':len(rows)==1 and rows[0]['source_line']==canonical['rows']['30002364']['source_line']==d799['canonical_statuses'][0]['source_line'],'status_is_already_solved':len(rows)==1 and rows[0]['status']=='already_solved','dated_prior_withdrawal_in_row':'2026-10-16' in rows[0]['source_line'],'current_pr_closed_unmerged_unchanged':live['state']=='closed' and live['merged'] is False and live['head']['sha']==d799['inventory_head_sha'] and live['updated_at']==d799['inventory_updated_at'],'comment_id':comment['id'],'comment_created_at':comment['created_at'],'comment_prior_to_review':comment['created_at']<'2026-10-21','comment_identifies_closing_after_pass_and_priority':'Closing without merge' in comment['body'] and 'priority' in comment['body'],'fresh_priority_audit':False}
withdraw['pass']=all(withdraw[k] for k in ['snapshot_row_equal','status_is_already_solved','dated_prior_withdrawal_in_row','current_pr_closed_unmerged_unchanged','comment_prior_to_review','comment_identifies_closing_after_pass_and_priority']) and comment['id']==6223000406
result={'at':now(),'scope':[790,832],'count':len(results),'results':results,'withdrawal799':withdraw,'pass':all(x['pass'] for x in results) and withdraw['pass']}
(O/'SCOPE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'count':len(results),'pass':result['pass'],'failures':[(x['pr'],x['errors']) for x in results if x['errors']],'withdrawal799_pass':withdraw['pass'],'queue_mismatches':[(x['pr'],b) for x in results for b in x['queue_blobs'] if not b['equal']],'ordinary_negative_status_counts':{s:sum(x['added_rows'][0]['status']==s for x in results if x['pr'] not in pub|{799}) for s in ['unsolved','already_solved']}}))
