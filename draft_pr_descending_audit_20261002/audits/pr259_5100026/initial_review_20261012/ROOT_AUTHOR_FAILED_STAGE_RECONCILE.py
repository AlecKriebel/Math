"""Root audit terminal failed193-call stage, then reconcile exact desired state with80freshGETs. No mutation or stage replay."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,base64,subprocess,collections
B=Path(__file__).resolve().parent;O=B/'author_repair_operator_preparation_01';X=O/'actual_author_01';V=B/'root_actual_author_failure_reconciliation_01'
V.mkdir(exist_ok=False);checks=[]
def ck(v,n):
    assert v,n
    checks.append(n)
def sha(v):return hashlib.sha256(v).hexdigest()
def pin(p):
    v=p.read_bytes();return {'bytes':len(v),'sha256':sha(v)}
def obj(t,v):return hashlib.sha1(t+b' '+str(len(v)).encode()+b'\0'+v).hexdigest()
def load(p):return json.loads(p.read_bytes())
def canon(j):return json.dumps(j,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def tree(es):return obj(b'tree',b''.join(e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in sorted(es,key=lambda e:(e['path']+('/' if e['type']=='tree' else '')).encode())))
def commit(j,tz):
    rows=['tree '+j['tree']['sha']]+['parent '+p['sha'] for p in j['parents']]
    for role in ['author','committer']:
        i=j[role];epoch=int(datetime.fromisoformat(i['date'].replace('Z','+00:00')).timestamp());rows.append(role+' '+i['name']+' <'+i['email']+'> '+str(epoch)+' '+tz)
    return ('\n'.join(rows)+'\n\n'+j['message']).encode()
c=load(O/'CONTROL.json');g=load(O/'REQUEST_GRAPH.json');done=load(X/'FAILURE.json');go=load(X/'ROOT_GO_CAPTURE.json');bindings=load(O/'DRAFT_BINDINGS.json')['bindings']
ck(done['status']=='FAIL' and done['completed'] is False and done['local_mock_only'] is False and done['authority_consumed'] is True and done['error']=='AssertionError()','terminal failed actual production193calls notmock')
ck(done['bindings']==go['bindings']==bindings and go['status']=='AUTHORIZED','exact consumed action bindings')
ck(not (X/'COMPLETE.json').exists() and not any(X.glob('*interrupt*')) and not (X/'FINAL_INTERRUPT_OBSERVATION.json').exists(),'no fabricated COMPLETE or interruption; actual FAILURE preserved')
for src,dst in [('CONTROL.json','CONTROL.json'),('REQUEST_GRAPH.json','REQUEST_GRAPH.json'),('DESIRED_SEMANTIC_DIFF.json','DESIRED_SEMANTIC_DIFF.json'),('author_operator.py','OPERATOR_SOURCE.py'),('CANONICAL_COMMIT.bin','CANONICAL_COMMIT.bin'),('ORIGINAL_CANONICAL_COMMIT.bin','ORIGINAL_CANONICAL_COMMIT.bin'),('ROOT_AUTHOR_STAGE_GO.json','ROOT_GO_CAPTURE.json')]:ck((O/src).read_bytes()==(X/dst).read_bytes(),'same-read actual captured '+dst)
for role,spec in go['reviews'].items():
    p=Path(spec['path']);v=p.read_bytes();ck(v==(X/('REVIEW_'+role+'.json')).read_bytes() and len(v)==spec['size'] and sha(v)==spec['sha256'],'actual ownreceipt pin '+role)
    j=json.loads(v);ck(j['status']=='PASS' and j['completed'] is True and j['review_role']==role and j['bindings']==spec['binding_expectation'],'actual completedrole '+role)
attempts=[json.loads(x) for x in (X/'ATTEMPT_INDEX.jsonl').read_bytes().splitlines()]
ck(attempts==done['attempts'] and len(attempts)==193 and len(g['requests'])==270,'all193 actualattempts; planned270notcompleted')
expected_files={'ROOT_GO_CAPTURE.json','CONTROL.json','REQUEST_GRAPH.json','DESIRED_SEMANTIC_DIFF.json','OPERATOR_SOURCE.py','CANONICAL_COMMIT.bin','ORIGINAL_CANONICAL_COMMIT.bin','CONSUMED.json','ATTEMPT_INDEX.jsonl','FAILURE.json'}|{'REVIEW_'+r+'.json' for r in go['reviews']}
for q in g['requests'][:193]:
    stem=f"{q['index']:04d}_{q['kind']}"
    expected_files.update(stem+s for s in ['.stdin','.stdout','.stderr','.result.json'])
ck({p.relative_to(X).as_posix() for p in X.rglob('*') if p.is_file()}==expected_files,'whole785 realcapture inventory no omittedextras')
ck(done['checked_requests']==[{'index':q['index'],'kind':q['kind'],'status':'PASS'} for q in g['requests'][:192]],'only192 validated responses;193mismatch preserved')
responses={};rawpins={}
old=c['expected_author_head'];new=c['desired_commit_sha']
def check_pr(j,head):
    ck(j['number']==259 and j['state']=='open' and j['draft'] is True and j['merged'] is False,'real ownOPEN DRAFT unmerged')
    ck(j['head']['sha']==head and j['head']['ref']==c['author_ref'] and j['head']['repo']['full_name']=='AlecKriebel/Math' and j['base']['ref']=='main' and j['base']['repo']['full_name']=='AlecKriebel/Math','real exact own PR head/base')
def check_ref(j,head):ck(j['ref']=='refs/heads/'+c['author_ref'] and j['object']['type']=='commit' and j['object']['sha']==head,'real exact own ref')
for q,a in zip(g['requests'][:193],attempts):
    stem=f"{q['index']:04d}_{q['kind']}";r=load(X/(stem+'.result.json'))
    ck(r==a and r['argv']==q['argv'] and r['index']==q['index'] and r['kind']==q['kind'] and r['method']==q['method'] and r['endpoint']==q['endpoint'],'actual exact indexed call '+stem)
    body=b'' if q['body'] is None else canon(q['body']);ck((X/(stem+'.stdin')).read_bytes()==body and sha(body)==r['request_body_sha256']==q['body_sha256'] and len(body)==r['request_body_size']==q['body_size'],'literal actual memory stdin '+stem)
    ck(r['launched'] is True and r['timeout'] is False and r['returncode']==0 and r['error'] is None and r['interrupt_pending'] is False,'actual successful terminaltransport '+stem)
    for stream in ['stdout','stderr']:
        p=X/(stem+'.'+stream);v=p.read_bytes();ck(len(v)==r[stream+'_size'] and sha(v)==r[stream+'_sha256'],'actual rawcapture pin '+stem+stream);rawpins[p.name]=pin(p)
    j=load(X/(stem+'.stdout'));responses[q['index']]=j;k=q['kind']
    ck(datetime.fromisoformat(go['issued_at'])<=datetime.fromisoformat(r['launch_observed_at'])<=datetime.fromisoformat(go['expires_at']),'actual launch within Rootauthority '+stem)
    if k.startswith('pr_'):check_pr(j,old if q['index']<=193 else new)
    elif k.startswith('ref_') or k=='updated_ref':check_ref(j,old if q['index']<191 else new)
    elif k in ['created_blob','created_tree','created_commit']:ck(j['sha']==q['expected_sha'],'actual created nativeoid '+stem)
    elif k in ['original_commit','desired_commit_before_update','desired_commit_after_update']:
        before=k=='original_commit';wanted=old if before else new;v=commit(j,'-0700' if before else '+0000');binary=X/('ORIGINAL_CANONICAL_COMMIT.bin' if before else 'CANONICAL_COMMIT.bin')
        ck(j['sha']==wanted and obj(b'commit',v)==wanted and v==binary.read_bytes(),'entire actual canonical unsignedcommit '+stem)
        ck(j['verification']['reason']=='unsigned' and j['verification']['signature'] is None and j['verification']['verified'] is False,'actual unsigned signature '+stem)
        if not before:ck(j['verification']['payload'] is None,'no unsigned hiddenpayload')
    elif 'tree' in k:
        es=[{a:e[a] for a in ['mode','path','type','sha']} for e in j['tree']]
        ck(j['truncated'] is False and es==q['expected_entries'] and tree(es)==j['sha']==q['expected_sha'],'entire real native tree '+stem)
    elif 'blob' in k:
        v=base64.b64decode(j['content']);ck(j['encoding']=='base64' and len(v)==j['size']==q['expected_size'] and sha(v)==q['expected_sha256'] and obj(b'blob',v)==j['sha']==q['expected_sha'],'fullactual selected/original blob '+stem)
    else:ck(False,'unknown actualresponse '+k)
ck(collections.Counter(x['method'] for x in attempts)=={'GET':116,'POST':76,'PATCH':1},'actual failed-stage method scope116GET77writes')
# Every full selected/native-node before and after PATCH equals Root-reviewed complete images.
for q in g['requests'][:193]:
    if q['kind'].startswith('desired_tree_'):ck(tree(responses[q['index']]['tree'])==c['desired_nodes'][q['native_path']]['sha'],'real full reviewed desirednode')
    if q['kind'].startswith('selected_blob_'):ck(base64.b64decode(responses[q['index']]['content'])==(O/next(x['local_path'] for x in c['selection'] if x['native_path']==q['native_path'])).read_bytes(),'actual reviewedselectedbytes')
root_review=load(B/'ROOT_AUTHOR_OPERATOR_REVIEW_ACCEPTANCE.json');ck(root_review['status']=='PASS' and root_review['completed'] and root_review['bindings']==bindings,'actual unchanged Root scope acceptance145/101')
# Exactly80new read-only reconciliation GETs; no resumed graph, retries, mutation or GO reuse.
gh='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';ck(sha(Path(gh).read_bytes())=='91f6e182bce24da56581ab999088c55ae0216309af19bc6167bbc4396c3f4ea5','fixed actual GHbinary')
fresh={}
fresh_plan=[('PR_START','repos/AlecKriebel/Math/pulls/259'),('REF_START','repos/AlecKriebel/Math/git/ref/heads/'+c['author_ref']),('COMMIT','repos/AlecKriebel/Math/git/commits/'+new)]
fresh_plan += [('TREE_'+str(i).zfill(2),'repos/AlecKriebel/Math/git/trees/'+n['sha']) for i,(path,n) in enumerate(c['desired_nodes'].items())]
fresh_plan += [('BLOB_'+str(i).zfill(2),'repos/AlecKriebel/Math/git/blobs/'+r['blob_sha']) for i,r in enumerate(c['selection'])]
fresh_plan += [('PR_END','repos/AlecKriebel/Math/pulls/259'),('REF_END','repos/AlecKriebel/Math/git/ref/heads/'+c['author_ref'])]
ck(len(fresh_plan)==80,'exact80newread-only reconciliation plan')
(V/'READ_ONLY_PLAN.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'scope':'80newGETonly, original193terminalFAIL unchanged, no stage resumption or mutation','requests':fresh_plan},indent=2)+'\n')
for name,endpoint in fresh_plan:
    argv=[gh,'api','--hostname','github.com','--method','GET',endpoint]
    with (V/(name+'.stdout')).open('xb') as out,(V/(name+'.stderr')).open('xb') as err:
        start=datetime.now(timezone.utc).isoformat();p=subprocess.run(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,timeout=60)
    r={'argv':argv,'method':'GET','started_at':start,'finished_at':datetime.now(timezone.utc).isoformat(),'returncode':p.returncode,'stdout':pin(V/(name+'.stdout')),'stderr':pin(V/(name+'.stderr'))}
    (V/(name+'.result.json')).write_text(json.dumps(r,indent=2)+'\n');ck(p.returncode==0,'fresh actual GET '+name);fresh[name]=load(V/(name+'.stdout'));j=fresh[name]
    if name.startswith('PR_'):check_pr(j,new)
    elif name.startswith('REF_'):check_ref(j,new)
    elif name=='COMMIT':ck(commit(j,'+0000')==(O/'CANONICAL_COMMIT.bin').read_bytes() and obj(b'commit',commit(j,'+0000'))==new and j['verification']['reason']=='unsigned' and j['verification']['signature'] is None and j['verification']['payload'] is None,'fresh fullcanonical nativecommit')
    elif name.startswith('TREE_'):
        n=list(c['desired_nodes'].values())[int(name[5:])];es=[{a:e[a] for a in ['mode','path','type','sha']} for e in j['tree']]
        ck(j['truncated'] is False and es==n['entries'] and tree(es)==j['sha']==n['sha'],'fresh full14native tree '+name)
    else:
        item=c['selection'][int(name[5:])];v=base64.b64decode(j['content'])
        ck(j['encoding']=='base64' and len(v)==j['size']==item['size'] and sha(v)==item['sha256'] and obj(b'blob',v)==j['sha']==item['blob_sha'] and v==(O/item['local_path']).read_bytes(),'fresh full61selectedblob '+name)
utc=datetime.now(timezone.utc).isoformat();receipt={'schema':'pr259-root-reconciled-actual-author-publication-acceptance-v1','utc':utc,'status':'PASS','decision':'PASS','completed':True,'review_role':'actual_author_publication','bindings':{k:bindings[k] for k in ['selection_manifest_sha256','frozen_payload_manifest_sha256']},'operator_bindings':bindings,'author_head':new,'author_tree':c['commit_body']['tree'],'actual_production_capture':str(X),'actual_terminal_FAILURE_pin':pin(X/'FAILURE.json'),'original_stage_completed':False,'reconciliation_complete':True,'original193_PR_head_mismatch':{'expected':new,'actual':old,'latency_cause_not_proven':True},'no_replay_or_mutation_in_reconciliation':True,'root_operator_acceptance_pin':pin(B/'ROOT_AUTHOR_OPERATOR_REVIEW_ACCEPTANCE.json'),'actual_requests':{'GET':116,'POST':76,'PATCH':1,'total':193},'root_fresh_native_GETs':80,'checks':len(checks),'case_complete':False,'math_percent':100,'priority_percent':100,'workflow_percent':65,'counters':{'completed':37,'published':14,'native_merges':14,'tracker_pending':0},'no_Main_PR_metadata_merge_close_paper_DOI_tracker_Git_mutation':True,'authority_consumed':True,'checks_labels':checks,'actual_raw_capture_pins':rawpins,'fresh_native_result_pins':{n:pin(V/(n+'.result.json')) for n in fresh}}
t=B/'ROOT_ACTUAL_AUTHOR_PUBLICATION_ACCEPTANCE.json'
with t.open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
(V/'VERIFICATION.json').write_text(json.dumps({'utc':utc,'status':'PASS','checks':len(checks),'receipt_pin':pin(t),'actual_scope':receipt['actual_requests'],'fresh_GETs':80},indent=2)+'\n')
with (B/'ROOT_SUBSEQUENT_RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc+' — Root independently accepted actual author publication '+new+' after193terminal failed-stage captures plus80newread-only fullpoststate GETs/fullcanonical commit; originalFAILURE retained and authority not replayed. Math100%, priority100%, workflow65%; counters37/14/14/0 unchanged; Main/PRmetadata and finalcase acceptance still pending.\n')
print(json.dumps({'status':'PASS','checks':len(checks),'actual_head':new,'receipt':str(t),'pin':pin(t)}))
