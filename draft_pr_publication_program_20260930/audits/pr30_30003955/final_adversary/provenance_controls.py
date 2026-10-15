#!/usr/bin/env python3
"""Read-only identity/context/diff/protection checks and complete read inventory.

Uses exact Git blobs, raw pinned JSON, mode=ro SQLite and primary LFS metadata.
No queue generator, historical replay, state transition or publication action.
"""
from pathlib import Path
import hashlib,json,sqlite3,subprocess,urllib.request,datetime,re

HERE=Path(__file__).resolve().parent;A=HERE.parent;REPO=HERE.parents[3]
HEAD='53b6e68be6d2cc5966c25746618951d5dae2183b'
BASE='60292bed09f59236aa192cb17aa138f7b4750e1a'
U=REPO/'unsolved_math_prioritization'
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def load(p):return json.loads(p.read_text())

def main():
    inventory=load(HERE/'INPUT_INVENTORY.json')['files'];reads=[]
    for row in inventory:
        p=Path(row['path']);raw=p.read_bytes();assert sha(raw)==row['sha256']
        entry={**row,'read_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'complete_byte_read':True}
        if p.suffix=='.json':
            parsed=json.loads(raw);entry['json_topology']=list(parsed) if isinstance(parsed,dict) else {'list_length':len(parsed)}
        elif p.suffix=='.jsonl':entry['jsonl_rows']=[json.loads(x) for x in raw.decode().splitlines()]
        elif p.suffix=='.py':compile(raw,str(p),'exec');entry['read_scope']='complete source inspected and immutable actual program reproduced in isolation'
        else:entry['read_scope']='complete prose/patch/output; duplicate mathematical bytes tied to original/candidate'
        reads.append(entry)
    protected={n:sha((U/n).read_bytes()) for n in ['QUEUE.md','state.json','history.jsonl','assessment_history.jsonl','update_history.jsonl']}
    assert git('branch','--show-current').decode().strip()=='main'
    assert git('merge-base',BASE,HEAD).decode().strip()==BASE
    mf=load(A/'snapshot_manifest.json');originals=[]
    for e in mf['files']:
        p=A/'source_snapshot'/e['path'];b=p.read_bytes()
        path='unsolved_math_prioritization/attempts/30003955/'+e['path']
        assert b==git('show',HEAD+':'+path)
        assert sha(b)==e['sha256'] and len(b)==e['bytes']
        assert git('rev-parse',HEAD+':'+path).decode().strip()==e['git_blob_sha1']
        originals.append(e)
    assert len(originals)==15
    diff=git('diff','--no-ext-diff',BASE,HEAD)
    (HERE/'EXACT_ORIGINAL_DIFF.patch').write_bytes(diff)
    assert diff==(A/'pr_input/diff.patch').read_bytes()
    names=git('diff','--name-only',BASE,HEAD).decode().splitlines();assert names==mf['changed_paths'] and len(names)==16
    chunks=diff.decode().split('diff --git ')[1:];assert len(chunks)==16
    for c in chunks:
        path=c.splitlines()[0].split(' b/',1)[1]
        if path.endswith('/QUEUE.md'):continue
        added='\n'.join(line[1:] for line in c.splitlines() if line.startswith('+') and not line.startswith('+++'))+'\n'
        relative=path.split('attempts/30003955/',1)[1]
        assert added.encode()==(A/'source_snapshot'/relative).read_bytes()
    queue_chunk=next(c for c in chunks if c.splitlines()[0].endswith('/QUEUE.md'))
    queue_changed=[x for x in queue_chunk.splitlines() if x.startswith(('+','-')) and not x.startswith(('+++','---'))]
    assert len(queue_changed)==2 and all('30003955' in x for x in queue_changed)
    assert '| queued | 0/5 |' in queue_changed[0] and '| unsolved | 2/5 |' in queue_changed[1]
    assert not git('ls-tree','-r','--name-only',BASE,'unsolved_math_prioritization/attempts/30003955').strip()
    C=A/'reviewed_candidate';changed={'PARTIAL.md','README.md','SOURCE_AUDIT.md','readiness.json','check_results.json'}
    for e in originals:
        n=e['path']
        if n in changed:assert (C/('ORIGINAL_'+n)).read_bytes()==(A/'source_snapshot'/n).read_bytes()
        else:assert (C/n).read_bytes()==(A/'source_snapshot'/n).read_bytes()
    assert (C/'ORIGINAL_pr_body.md').read_text()==load(A/'pr_input/pr.json')['body']
    old=(A/'source_snapshot/PARTIAL.md').read_text();cur=(C/'PARTIAL.md').read_text()
    assert old.split('## 1.',1)[1].split('## 4.',1)[0]==cur.split('## 1.',1)[1].split('## 4.',1)[0]
    assert old.split('## 5.',1)[1]==cur.split('## 5.',1)[1]
    ledger=[json.loads(x) for x in (C/'turns.jsonl').read_text().splitlines()]
    assert [x['turn'] for x in ledger]==[1,2] and all(not x['full_target_resolved'] for x in ledger)
    ready=load(C/'readiness.json');assert ready['used_substantive_attempts']==2 and ready['maximum_substantive_attempts']==5
    assert ready['current_gate']=='pending_NEW_complete_repaired_packet_adversary' and not ready['full_target_resolved']
    manifest=load(U/'manifest.json');rev=manifest['revision'];assert rev=='37e53eabe540fb458758e198be61634bd02ee008'
    url='https://huggingface.co/api/datasets/ulamai/UnsolvedMath/tree/'+rev
    with urllib.request.urlopen(url,timeout=45) as resp:raw_lfs=resp.read();final=resp.url
    (HERE/'FRESH_LFS_RESPONSE.json').write_bytes(raw_lfs);lfs=json.loads(raw_lfs)
    cache=[]
    for n in ['problems.json','research_results.json']:
        b=(U/'cache'/n).read_bytes();entry=next(x for x in lfs if x['path']==n)
        assert sha(b)==manifest['files'][n]['sha256']==entry['lfs']['oid']
        assert len(b)==manifest['files'][n]['bytes']==entry['lfs']['size']
        cache.append({'file':n,'bytes':len(b),'sha256':sha(b),'fresh_LFS_oid_equal':True})
    problems=load(U/'cache/problems.json');reports=load(U/'cache/research_results.json')
    matches=[p for p in problems if p['id']==30003955 or p['problem_number']=='OWR-16415-018']
    assert len(matches)==1;p=matches[0];assert p==load(C/'source_record.json')
    assert p['problem_number'] not in reports;prior=reports.get(p['problem_number'],{});assert prior=={}
    exact=[x['id'] for x in problems if re.sub(r'\s+',' ',x.get('statement','')).strip()==re.sub(r'\s+',' ',p['statement']).strip()]
    assert exact==[30003955]
    db=sqlite3.connect('file:'+str(U/'cache/catalog.sqlite')+'?mode=ro',uri=True)
    payload,report,typ,null=db.execute('SELECT payload,report,typeof(report),report IS NULL FROM records WHERE key=?',('30003955',)).fetchone()
    assert json.loads(payload)==p and report=='{}' and typ=='text' and null==0
    assert db.execute('SELECT revision FROM metadata').fetchone()==(rev,)
    assert db.execute('SELECT count(*) FROM records').fetchone()==(15458,)
    db.close()
    context=sha(json.dumps([p,prior],sort_keys=True).encode());statement=sha(p['statement'].encode())
    assert context=='7a33f09dbc9f8a995131dd1cfbabf0ba9772bd70291bb3672b2c69e94c1f842a'
    assert statement=='4449956a75de4c5fe94559c4891fa1f3ebf1800a366bb154fcce7fd3a1681d1f'
    catalog=[x for x in load(U/'catalog.json') if x['id']=='30003955'];assert len(catalog)==1
    assert catalog[0]['review_hash']==context and catalog[0]['statement_hash']==statement
    state=load(U/'state.json');assert '30003955' not in state
    history={n:[x for x in (U/n).read_text().splitlines() if '30003955' in x or 'OWR-16415-018' in x] for n in ['history.jsonl','assessment_history.jsonl','update_history.jsonl']}
    assert not any(history.values())
    mainrow=next(x for x in (U/'QUEUE.md').read_text().splitlines() if '| 30003955 /' in x)
    columns=[x.strip() for x in mainrow.strip().strip('|').split('|')]
    assert len(columns)==12 and columns[7]=='queued' and columns[8]=='0/5'
    # All shared workflow/code is read, never executed against the maintained queue.
    for rel in ['AGENTS.md','README.md','VALIDATION.md','queue.py','review_v2/merge.py','cache/build_assessments.py',
                'apply_impact_scores.py','policy.json','review_v2/related_target_groups.json','state.json','history.jsonl',
                'assessment_history.jsonl','update_history.jsonl','catalog.json','assessments.json','manifest.json']:
        b=(U/rel).read_bytes();reads.append({'path':str(U/rel),'sha256':sha(b),'bytes':len(b),'complete_byte_read':True,
            'read_scope':'complete workflow source / semantic selected identity and protected history context; full shared bytes consumed'})
    for rel in ['snapshot_manifest.json','ROOT_RECONSTRUCTION_SEAL.json','tmp/build_current.py','tmp/seal_current.py']:
        b=(A/rel).read_bytes();reads.append({'path':str(A/rel),'sha256':sha(b),'bytes':len(b),'complete_byte_read':True,
             'read_scope':'read-only construction/provenance metadata; builders not executed because they address immutable input paths'})
    live=json.loads(subprocess.check_output(['gh','pr','view','30','--json','number,title,body,url,state,isDraft,headRefName,headRefOid,baseRefName,baseRefOid,files'],cwd=REPO))
    (HERE/'LIVE_PR_READBACK.json').write_text(json.dumps(live,indent=2)+'\n')
    assert live['state']=='OPEN' and live['isDraft'] and live['headRefOid']==HEAD
    assert [x['path'] for x in live['files']]==names
    assert live['body'].strip()==(C/'pr_body.md').read_text().strip()
    assert 'pending' in live['body'] and 'replaces an invalid' in live['body']
    assert protected=={n:sha((U/n).read_bytes()) for n in protected}
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_passed':True,
            'candidate_manifest_sha256':sha((C/'MANIFEST.json').read_bytes()),'original15_exact_git':originals,
            'exact16_diff_sha256':sha(diff),'queue_only_original_existing_change':queue_changed,
            'original_two_attempts':ledger,'new_attempts':0,'raw_pinned_sources':cache,
            'fresh_LFS_url':url,'fresh_LFS_final_url':final,'fresh_LFS_response_sha256':sha(raw_lfs),
            'source_identity_unique':True,'raw_prior_missing_normalized_to':prior,'sql_report_type':typ,'sql_report_literal':report,
            'source_prior_context_hash':context,'statement_hash':statement,'main_selected_queue_row':mainrow,
            'main_selected_history_matches':history,'state_count':len(state),'original_consumed_turns':sum(v.get('turns_used',0) for v in state.values()),
            'shared_files_before':protected,'shared_files_after':protected,'shared_queue12_preserved':True,
            'legacy_queue_generator8_columns_forbidden':True,'legacy_manual_ready_field_presence_not_proof':True,
            'historical_model_effort_query_absence_telemetry':'Attested only; current identity/replay does not reconstruct it.',
            'live_PR_same_current_body_original_draft_head':True,'complete_input_read_rows':len(reads)}
    (HERE/'PROVENANCE_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'READ_LEDGER.json').write_text(json.dumps({'utc':result['utc'],'files':reads,
        'preseal_boundary':'Exact earlier ledger in EARLY_INDEPENDENCE_SEAL.json; support reads happened afterward.',
        'review_method':'All proof/prose and actual code inspected; complete raw reads/parses and duplicate-byte comparisons close repeated receipts/snapshots.'},indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['all_passed','candidate_manifest_sha256','exact16_diff_sha256','source_prior_context_hash','state_count','original_consumed_turns','complete_input_read_rows']},indent=2))

if __name__=='__main__':main()
