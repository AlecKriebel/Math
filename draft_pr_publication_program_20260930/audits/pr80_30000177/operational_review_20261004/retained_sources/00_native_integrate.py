"""ROOT sequential exact-head merge, present-day acceptance and checkpoint.

Preparation authorizes nothing. Every phase requires exact ROOT plan/evidence,
a fresh cooperative acknowledgment covering this whole operation, empty index,
unchanged foreign bodies/index entries and the preceding phase's receipt.
Failures retain partial state; this operator never resets, stashes or rolls back.
"""
import argparse, datetime, hashlib, json, os, sqlite3, stat
from pathlib import Path
from capture import capture
R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr80_30000177'
F=Path(__file__).parent
AUTH=A/'original_source_authentication_20261004'
HEAD='dcfeb5d8ad68b397ec509c70e85c6fca46cd01e3'
PREFIX='unsolved_math_prioritization/attempts/30000177'
QUEUE='unsolved_math_prioritization/QUEUE.md'
STATE='unsolved_math_prioritization/state.json'
HISTORY='unsolved_math_prioritization/history.jsonl'
STATUS=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
def require(ok,msg):
    if not ok: raise RuntimeError(msg+'; STOP and inspect retained state')
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def pin(p):
    require(p.is_file() and not p.is_symlink(),'Regular pinned file missing')
    b=p.read_bytes()
    return {'path':str(p.relative_to(R)),'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(p.stat().st_mode)}
def row(b):
    found=[x for x in b.splitlines(keepends=True) if b'| 30000177 /' in x]
    require(len(found)==1 and len(found[0].decode().split('|'))==14,'Exact target row missing')
    return found[0]
def names(b): return {x.decode() for x in b.split(b'\0') if x}
def sourcepair():
    source=load(AUTH/'original_head'/PREFIX/'source_record.json')
    require(type(source)==dict and type(source['id'])==int and source['id']==30000177 and source['problem_number']=='OWR-785-003' and 'problem' not in source,'Flat source shape changed')
    require('proposed_by' in source and source['proposed_by'] is None,'Typed proposed_by changed')
    manifest=load(R/'unsolved_math_prioritization/manifest.json')
    require(manifest['revision']=='37e53eabe540fb458758e198be61634bd02ee008','Source revision changed')
    data={}
    for name in ('problems.json','research_results.json'):
        b=(R/'unsolved_math_prioritization/cache'/name).read_bytes()
        require(len(b)==manifest['files'][name]['bytes'] and sha(b)==manifest['files'][name]['sha256'],'Full raw source drift')
        data[name]=json.loads(b)
    require([x for x in data['problems.json'] if str(x['id'])=='30000177']==[source],'Raw flat selected target drift')
    require('OWR-785-003' not in data['research_results.json'],'Raw prior key appeared')
    dbpath=R/'unsolved_math_prioritization/cache/catalog.sqlite'
    require(all(not Path(str(dbpath)+s).exists() for s in ('-wal','-shm','-journal')),'SQL sidecar present')
    with sqlite3.connect('file:'+str(dbpath)+'?mode=ro&immutable=1',uri=True) as db:
        result=db.execute('SELECT payload,report FROM records WHERE key=?',('30000177',)).fetchall()
        require(len(result)==1 and result[0][0] is not None and result[0][1] is not None,'SQL selected pair absent or SQL NULL')
        problem,report=map(json.loads,result[0])
        require(problem==source and type(report)==dict and report=={},'SQL typed pair differs')
    review_hash=sha(json.dumps([source,{}],sort_keys=True).encode())
    catalog=[x for x in load(R/'unsolved_math_prioritization/catalog.json') if x['id']=='30000177']
    require(len(catalog)==1 and catalog[0]['review_hash']==review_hash and catalog[0]['present'] is True and catalog[0]['holds']==[],'Current catalog/holds drift')
    require(review_hash=='a1074b51667f3ddaacd28e9a42378defc9ad192192d243a0a8a917215a4d829f','Authenticated fingerprint mismatch')
    return {'source_record_is_flat':True,'proposed_by_present_null':True,'raw_prior_key_present':False,'SQL_report_is_NULL':False,'SQL_report_literal':'{}','review_hash':review_hash,'statement_hash':sha(source['statement'].encode()),'review_hash_rule':'Existing SQL typed pair [problem, {}]; no absent source field becomes null','dataset_revision':manifest['revision']}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('phase',choices=['merge','accept','checkpoint']); ap.add_argument('--plan',required=True); ap.add_argument('--ack',required=True); ap.add_argument('--token',required=True)
    args=ap.parse_args()
    require(not __import__('sys').flags.optimize,'Optimization forbidden')
    plan_path=Path(args.plan).resolve(); ack_path=Path(args.ack).resolve()
    plan=load(plan_path); ack=load(ack_path)
    plan_pin=pin(plan_path)
    require(plan['ROOT_reviewed_for_execution'] is True and plan['PR']==80 and plan['head']==HEAD,'Unreviewed/incorrect plan')
    require(ack['token']==args.token and ack['PR']==80 and ack['covers_phases']==['merge','accept','checkpoint'] and ack['exact_owned_paths']==plan['exact_owned_paths'],'Fresh lease scope mismatch')
    require(ack['ROOT_plan_sha256']==sha(plan_path.read_bytes()),'Acknowledgment does not bind plan')
    require(datetime.datetime.fromisoformat(ack['UTC'].replace('Z','+00:00'))>=datetime.datetime.fromisoformat(plan['UTC'].replace('Z','+00:00')),'ACK predates concrete plan')
    ack_pin=pin(ack_path); status_pin=pin(STATUS)
    current=ack['starting_main']
    if args.phase=='accept': current=load(A/'ROOT_NATIVE_MERGE_RECEIPT_20261004.json')['commit']
    if args.phase=='checkpoint': current=load(A/'ROOT_NATIVE_ACCEPTANCE_RECEIPT_20261004.json')['commit']
    count=0
    def run(argv,allowed=(0,)):
        nonlocal count
        count+=1
        result,out,err=capture('native_'+args.phase+'_'+str(count),argv,sources=[str(Path(__file__).resolve()),str(plan_path),str(ack_path)])
        require(result['exit_code'] in allowed,'Command failure '+repr(argv))
        return out,result['exit_code']
    def git(*argv,allowed=(0,)): return run(['git','--no-optional-locks',*argv],allowed)[0]
    def pr():
        out,_=run(['/opt/homebrew/bin/gh','pr','view','80','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,mergeCommit,mergedAt'])
        value=json.loads(out); require(value['headRefOid']==HEAD and value['baseRefName']=='main','PR identity drift'); return value
    def check_inputs():
        require(pin(plan_path)==plan_pin,'Concrete ROOT plan changed')
        require(pin(ack_path)==ack_pin and pin(STATUS)==status_pin,'Cooperative control drift')
        status=load(STATUS)
        require(status['shared_git_writes_paused'] is True and status['ascending_pr80_publication_integration_lease_token']==args.token,'Writer lease released/changed')
        require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==current,'Shared branch/head drift')
        for entry in plan['bound_inputs']:
            require(pin(R/entry['path'])==entry,'Bound plan input drift '+entry['path'])
        gate=load(A/'ROOT_FINAL_PACKAGE_GATE_20261004.json')
        require(gate['publication_clearance'] is True,'Whole-package gate absent')
        pub=load(A/'ROOT_PUBLICATION_VERIFICATION_20261004.json'); track=load(A/'ROOT_TRACKER_VERIFICATION_20261004.json')
        require(pub['all8_public_bytes_identical'] and pub['intended_metadata_exact'] and pub['DOI']==track['DOI']==plan['DOI'] and track['fresh_full_table_exactly_one_pair'],'Published/tracker evidence differs')
    check_inputs()
    require(git('ls-remote','origin','refs/heads/main').split()[0].decode()==current,'Actual remote main differs')
    require(git('diff','--cached','--name-only','-z')==b'','Index is not empty')
    require(not (R/'.git/MERGE_HEAD').exists(),'Existing merge in progress')
    owned=set(plan['exact_owned_paths'])
    dirty=names(git('diff','--name-only','-z','HEAD'))
    require(not dirty.intersection(owned),'Owned tracked path unexpectedly dirty')
    foreign={p:pin(R/p) for p in dirty}
    foreign_diff=git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b''
    index=git('ls-files','--stage','-z')
    flags=git('ls-files','-v','-z')
    def exclude(b): return b'\0'.join(x for x in b.split(b'\0') if x and (x.split(b'\t',1)[-1].decode() if b'\t' in x else x[2:].decode()) not in owned)
    def stable():
        check_inputs()
        require({p:pin(R/p) for p in dirty}==foreign,'Foreign worktree body/mode drift')
        require(names(git('diff','--name-only','-z','HEAD'))-owned==dirty,'Foreign dirty path scope drift')
        require((git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b'')==foreign_diff,'Foreign tracked diff drift')
        require(exclude(git('ls-files','--stage','-z'))==exclude(index) and exclude(git('ls-files','-v','-z'))==exclude(flags),'Foreign index entries/flags drift')
    originals=[x for x in load(AUTH/'ORIGINAL_BLOB_MANIFEST.json')['files'] if x['path'].startswith(PREFIX+'/')]
    require(len(originals)==19,'Original file count changed')
    def original_bytes(commit,native=False):
        for entry in originals:
            b=git('show',commit+':'+entry['path'])
            require(len(b)==entry['bytes'] and sha(b)==entry['sha256'] and blob(b)==entry['git_blob_sha1'],'Original blob drift')
            require(git('ls-tree',commit,'--',entry['path']).decode().split()[:3]==[entry['mode'],'blob',entry['git_blob_sha1']],'Original Git mode drift')
            if native: require(pin(R/entry['path'])['sha256']==entry['sha256'] and stat.S_IMODE((R/entry['path']).stat().st_mode)==0o644,'Original native body/mode drift')
    info=pr(); identity=sourcepair()
    if args.phase=='merge':
        require(info['state']=='OPEN' and info['isDraft'] is True and current==ack['starting_main'],'Initial PR not open draft')
        metadata=json.loads(run(['/opt/homebrew/bin/gh','pr','view','80','--repo','AlecKriebel/Math','--json','title,body,headRefOid'])[0])
        require(metadata['headRefOid']==HEAD and metadata['title']==plan['submitted_title'] and sha(metadata['body'].encode())==plan['submitted_body_sha256'],'PR metadata drift before current publication annotation')
        stable()
        run(['/opt/homebrew/bin/gh','pr','edit','80','--repo','AlecKriebel/Math','--title',plan['current_title'],'--body-file',str(A/'native_preparation_20261004/PR_BODY.md')])
        fresh_metadata=json.loads(run(['/opt/homebrew/bin/gh','pr','view','80','--repo','AlecKriebel/Math','--json','title,body,headRefOid'])[0])
        require(fresh_metadata['headRefOid']==HEAD and fresh_metadata['title']==plan['current_title'] and fresh_metadata['body'].encode()==(A/'native_preparation_20261004/PR_BODY.md').read_bytes(),'Current publication PR annotation readback differs')
        require(not (R/PREFIX).exists(),'Native original destination exists')
        incoming=json.loads(run(['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/80/files?per_page=100'])[0])
        targets={x['path'] for x in originals}|{QUEUE}
        require(len(incoming)==20 and {x['filename'] for x in incoming}==targets,'Incoming scope drift')
        git('fetch','--no-tags','--no-write-fetch-head','origin','refs/pull/80/head')
        require(pr()['headRefOid']==HEAD,'Head changed during fetch')
        original_bytes(HEAD)
        common=git('merge-base',current,HEAD).decode().strip()
        require(names(git('diff','--name-only','-z',common,HEAD))==targets,'Local incoming domain differs')
        before=(R/QUEUE).read_bytes(); old=row(before)
        require(before==git('show',current+':'+QUEUE),'QUEUE dirty')
        require(old.decode().split('|')[8].strip()=='queued' and old.decode().split('|')[9].strip()=='0/5','Native queued baseline changed')
        new=plan['queue_after_row'].encode()
        oldcells,newcells=old.decode().split('|'),new.decode().split('|')
        require(all(oldcells[i]==newcells[i] for i in range(14) if i not in (8,9,11,12)),'Unapproved target-cell change')
        require(newcells[8].strip()=='preprint_published' and newcells[9].strip()=='1/5' and plan['DOI'] in newcells[12],'Current target replacement wrong')
        after=before.replace(old,new,1)
        stable()
        merge_out,merge_exit=run(['git','--no-optional-locks','merge','--no-ff','--no-commit',HEAD],allowed=(0,1))
        conflicts=names(git('diff','--name-only','--diff-filter=U','-z'))
        require(conflicts<={QUEUE} and (R/'.git/MERGE_HEAD').read_text().strip()==HEAD,'Unexpected merge conflict/state')
        (R/QUEUE).write_bytes(after)
        git('add','--',QUEUE)
        require(not git('diff','--name-only','--diff-filter=U','-z') and names(git('diff','--cached','--name-only','-z'))==targets,'Merge index scope differs')
        original_bytes(HEAD,native=True); stable()
        base=current
        git('commit','-m','Accept PR80 W-state LOCC dense-coding result and published preprint')
        current=git('rev-parse','HEAD').decode().strip()
        require(git('show','-s','--format=%P',current).decode().split()==[base,HEAD],'Exact merge parents differ')
        require(names(git('diff','--name-only','-z',base,current))==targets and git('show',current+':'+QUEUE)==after,'Merge scope/foreign QUEUE rows differ')
        original_bytes(current,native=True); stable()
        git('push','origin','main')
        require(git('ls-remote','origin','refs/heads/main').split()[0].decode()==current,'Merge push differs')
        fresh=pr(); require(fresh['state']=='MERGED' and fresh['mergeCommit']['oid']==current and fresh['mergedAt'],'GitHub merged-head readback failed')
        result={'commit':current,'parent':base,'second_parent':HEAD,'merge_exit':merge_exit,'merged_at':fresh['mergedAt'],'19_original_bodies_modes_blobs_preserved':True}
    elif args.phase=='accept':
        merge=load(A/'ROOT_NATIVE_MERGE_RECEIPT_20261004.json')
        require(info['state']=='MERGED' and info['mergeCommit']['oid']==current==merge['commit'],'Merged predecessor differs')
        original_bytes(current,native=True)
        sb,hb=(R/STATE).read_bytes(),(R/HISTORY).read_bytes()
        require(sb==git('show',current+':'+STATE) and hb==git('show',current+':'+HISTORY),'Native globals dirty')
        state=json.loads(sb)
        require(type(state)==dict and '30000177' not in state and all(str(json.loads(x).get('id'))!='30000177' for x in hb.splitlines()),'Native target already has state/history')
        require(not hb or hb.endswith(b'\n'),'Incomplete history suffix')
        require(all(not (R/PREFIX/name).exists() for name in ('acceptance.json','CURRENT_RESULT.md','CURRENT_PRIORITY.md')),'Current acceptance destinations exist')
        acceptance={'schema':'pr80-current-published-result-acceptance/v1','at':now(),'actual_PID':os.getpid(),'PR':80,'problem_id':'30000177','problem_code':'OWR-785-003','status':'preprint_published','reviewed_head':HEAD,'merge_commit':current,'merged_at':merge['merged_at'],'DOI':plan['DOI'],'record_url':plan['record_url'],'tracker_range':plan['tracker_range'],'original_budget':'1/5','new_central_proof_search_turns':0,'whole_original_attempt_preserved':True,'historical_lifecycle_transitions_reconstructed':False,'native_status_is_present_day_mirror':True,'source_identity':identity,'exact_claim':plan['exact_claim'],'bounded_priority_audit_complete':True,'worldwide_priority_guarantee':False,'AI_tools_used_extensively':True,'human_peer_review':False,'final_package_gate':pin(A/'ROOT_FINAL_PACKAGE_GATE_20261004.json'),'publication_verification':pin(A/'ROOT_PUBLICATION_VERIFICATION_20261004.json'),'tracker_verification':pin(A/'ROOT_TRACKER_VERIFICATION_20261004.json')}
        event={'schema':'pr80-present-day-native-import/v1','event':'acceptance_mirror_import','at':acceptance['at'],'id':'30000177','status':'preprint_published','turns_used':1,'turn_limit':5,'review_hash':identity['review_hash'],'readiness_review_hash':identity['review_hash'],'statement_hash':identity['statement_hash'],'note':plan['queue_after_row'].split('|')[11].strip(),'evidence':{'acceptance_path':PREFIX+'/acceptance.json','DOI':plan['DOI'],'merge_commit':current,'original_budget':'1/5','new_central_proof_search_turns':0,'historical_transitions_asserted':False}}
        end=len(sb.rstrip())-1; prefix=sb[:end]; cut=len(prefix.rstrip())
        require(sb[end:end+1]==b'}','State delimiter mismatch')
        insertion=(b',' if state else b'')+b'\n  "30000177": '+json.dumps(event,ensure_ascii=False,sort_keys=True,indent=2).replace('\n','\n  ').encode()
        sa=prefix[:cut]+insertion+prefix[cut:]+sb[end:]
        ha=hb+canon(event).encode()+b'\n'
        require(sa[:cut]+sa[cut+len(insertion):]==sb and {k:v for k,v in json.loads(sa).items() if k!='30000177'}==state,'Foreign state bytes not preserved')
        stable()
        (R/PREFIX/'acceptance.json').write_text(json.dumps(acceptance,indent=2)+'\n')
        for name in ('CURRENT_RESULT.md','CURRENT_PRIORITY.md'): (R/PREFIX/name).write_bytes((A/'native_preparation_20261004'/name).read_bytes())
        (R/STATE).write_bytes(sa); (R/HISTORY).write_bytes(ha)
        targets={PREFIX+'/'+n for n in ('acceptance.json','CURRENT_RESULT.md','CURRENT_PRIORITY.md')}|{STATE,HISTORY}
        git('add','--',*sorted(targets)); require(names(git('diff','--cached','--name-only','-z'))==targets,'Acceptance staged scope differs')
        stable(); base=current
        git('commit','-m','Record current PR80 publication acceptance without altering original proof ledger')
        current=git('rev-parse','HEAD').decode().strip()
        require(git('show','-s','--format=%P',current).decode().split()==[base] and names(git('diff','--name-only','-z',base,current))==targets,'Acceptance commit parent/domain differs')
        require(git('show',current+':'+STATE)==sa and git('show',current+':'+HISTORY)==ha,'Native global readback mismatch')
        require(len([x for x in ha.splitlines() if str(json.loads(x).get('id'))=='30000177'])==1,'Multiple native target events')
        original_bytes(current,native=True); stable()
        git('push','origin','main'); require(git('ls-remote','origin','refs/heads/main').split()[0].decode()==current,'Acceptance push readback failed')
        result={'commit':current,'parent':base,'merge_commit':base,'original19_preserved':True,'foreign_state_bytes_preserved':True,'history_exact_prefix_preserved':True,'present_day_import_event_count':1}
    else:
        targets=set(plan['checkpoint_files'])
        stable()
        git('add','--',*sorted(targets))
        staged=names(git('diff','--cached','--name-only','-z'))
        require(staged and staged<=targets,'Checkpoint staged scope mismatch')
        for p in staged:
            b=git('show',':'+p); require(sha(b)==plan['checkpoint_files'][p]['sha256'] and len(b)==plan['checkpoint_files'][p]['bytes'],'Checkpoint pin mismatch')
        stable(); base=current
        git('commit','-m','Publish PR80 corrected preprint package and complete adversarial audit records')
        current=git('rev-parse','HEAD').decode().strip()
        require(git('show','-s','--format=%P',current).decode().split()==[base] and names(git('diff','--name-only','-z',base,current))==staged,'Checkpoint committed domain differs')
        for p in staged: require(sha(git('show',current+':'+p))==plan['checkpoint_files'][p]['sha256'],'Checkpoint committed pin mismatch')
        original_bytes(current,native=True); stable()
        git('push','origin','main'); require(git('ls-remote','origin','refs/heads/main').split()[0].decode()==current,'Checkpoint push readback failed')
        result={'commit':current,'parent':base,'committed_paths':sorted(staged),'all_checkpoint_pins_verified':True}
    require(git('diff','--cached','--name-only','-z')==b'','Final index not empty'); stable()
    result.update({'UTC':now(),'status':'COMMITTED_PUSHED_INDEPENDENTLY_READ_BACK','phase':args.phase,'original_head':HEAD,'lease_token':args.token,'actual_PID':os.getpid(),'index_empty':True,'foreign_dirty_bodies_modes_diffs_and_index_preserved':True,'original_budget':'1/5','new_central_proof_search_turns':0})
    receipt=A/('ROOT_NATIVE_'+{'merge':'MERGE','accept':'ACCEPTANCE','checkpoint':'CHECKPOINT'}[args.phase]+'_RECEIPT_20261004.json')
    with receipt.open('x') as f: f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
