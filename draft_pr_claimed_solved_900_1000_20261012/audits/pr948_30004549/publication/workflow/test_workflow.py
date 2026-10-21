#!/usr/bin/env python3
"""Offline workflow guards; faked external service calls, owned tiny fixtures only."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise RuntimeError('Use -I -S -B')
import argparse,copy,hashlib,json,subprocess,tempfile,traceback
from pathlib import Path
from datetime import datetime,timezone
W=Path(__file__).absolute().parent
ROOT=W.parents[4]
P=ROOT/'draft_pr_claimed_solved_900_1000_20261012'
CORE=P/'accept_pr948.py'
N={'__name__':'_offline_workflow_test_','__file__':str(CORE)}
exec(compile(CORE.read_bytes(),str(CORE),'exec',dont_inherit=True,optimize=0),N)
RESULTS=[]

def check(name,call):
    try:call();RESULTS.append({'name':name,'status':'PASS'})
    except Exception as e:RESULTS.append({'name':name,'status':'FAIL','error':repr(e)});raise

def must(test):
    if not test:raise RuntimeError('test condition false')

def reject(call):
    try:call()
    except (RuntimeError,ValueError,KeyError,TypeError):return
    raise RuntimeError('unsafe fixture unexpectedly accepted')

class Patch:
    def __init__(self,**changes):self.changes=changes
    def __enter__(self):self.old={k:N[k] for k in self.changes};N.update(self.changes)
    def __exit__(self,*args):N.update(self.old)

def main():
    for name in N['HELPERS']:
        raw=(P/name).read_bytes()
        check('compile_'+name,lambda raw=raw,name=name:compile(raw,str(P/name),'exec',dont_inherit=True,optimize=0))
        check('no_inherited_PR946_'+name,lambda raw=raw:must(b'pr946' not in raw and b'PR946' not in raw and b'PR=946' not in raw))
        for flags,label in [(['-I','-B'],'site'),(['-S','-B'],'isolation'),(['-I','-S'],'bytecode')]:
            result=subprocess.run([sys.executable,*flags,str(P/name),'--help'],capture_output=True)
            check('startup_reject_'+label+'_'+name,lambda result=result:must(result.returncode!=0 and b'Invoke with Python -I -S -B' in result.stderr))
    check('duplicate_JSON_keys',lambda:reject(lambda:N['strict_json'](b'{"a":1,"a":2}')))
    check('nonfinite_JSON',lambda:reject(lambda:N['strict_json'](b'{"a":NaN}')))
    check('bool_file_bytes',lambda:reject(lambda:N['validate_pin']({'bytes':True,'sha256':'0'*64})))
    check('unsafe_path',lambda:must(not N['safe']('a/../private') and not N['safe']('/absolute') and not N['safe']('a//b')))
    records={(P.relative_to(ROOT)/n).as_posix():N['fingerprint']((P/n).read_bytes()) for n in N['HELPERS']}
    records[N['KIT']]=N['fingerprint']((ROOT/N['KIT']).read_bytes())
    inv={'schema':'pr948-operations-v1','pr':948,'problem_id':'30004549','original_pr_head':N['HEAD'],'files':records}
    check('whole_seven_source_inventory',lambda:must(N['validate_inventory'](inv)==records))
    bad=copy.deepcopy(inv);bad['files'].pop(N['KIT'])
    check('missing_kit_fails_inventory',lambda:reject(lambda:N['validate_inventory'](bad)))
    bad=copy.deepcopy(inv);bad['pr']=946
    check('wrong_PR_fails_inventory',lambda:reject(lambda:N['validate_inventory'](bad)))
    kit=N['captured_kit']({'captured':{N['KIT']:(ROOT/N['KIT']).read_bytes()}})
    metadata={'title':'test','notes':'Requirements Python>=3.11; unrefereed.'}
    remote={'id':17,'submitted':False,'metadata':metadata,'files':[]}
    check('exact_notes',lambda:must(N['normalize_notes'](remote,metadata)[1] is False))
    html=copy.deepcopy(remote);html['metadata']['notes']=metadata['notes'].replace('Python>=3.11','Python&gt;=3.11')
    check('only_observed_notes_escape',lambda:must(N['normalize_notes'](html,metadata)==(remote,True)))
    edited=copy.deepcopy(html);edited['metadata']['notes']+=' unauthorized'
    check('edited_notes_rejected',lambda:reject(lambda:N['normalize_notes'](edited,metadata)))
    amp=copy.deepcopy(remote);amp['metadata']['notes']=metadata['notes'].replace('unrefereed','unrefereed &amp;')
    check('no_broad_HTML_decode',lambda:reject(lambda:N['normalize_notes'](amp,metadata)))
    class FakeClient:
        def __init__(self,submitted=False):self.posts=0;self.created=0;self.record=copy.deepcopy(remote);self.record['submitted']=submitted
        def create(self,metadata):self.created+=1;return copy.deepcopy(self.record)
        def get(self,ident):must(ident==17);return copy.deepcopy(self.record)
        def publish(self,ident):self.posts+=1;self.record['submitted']=True;return copy.deepcopy(self.record)
        def update(self,*args):raise RuntimeError('test has no update authorization')
        def upload(self,*args):raise RuntimeError('test has no upload authorization')
    guardedkit={'validate_record':kit['validate_record'],'verify':lambda *args:[]}
    guards=[];client=FakeClient()
    guarded=N['GuardedZenodoClient'](client,guardedkit,metadata,[],lambda:guards.append(1),'publish',17)
    check('one_exact_ID_publish',lambda:must(guarded.publish(17)['submitted'] is True and client.posts==1 and len(guards)>=2))
    check('publish_second_POST_rejected',lambda:reject(lambda:guarded.publish(17)))
    check('wrong_publish_ID_rejected',lambda:reject(lambda:guarded.publish(18)))
    client=FakeClient(True);guarded=N['GuardedZenodoClient'](client,guardedkit,metadata,[],lambda:None,'publish',17)
    check('already_published_GET_no_POST',lambda:must(guarded.publish(17)['submitted'] is True and client.posts==0))
    client=FakeClient();guarded=N['GuardedZenodoClient'](client,guardedkit,metadata,[],lambda:None,'inspect',17)
    check('inspect_has_no_publish',lambda:reject(lambda:guarded.publish(17)))
    check('inspect_has_no_create',lambda:reject(lambda:guarded.create(metadata)))
    client=FakeClient();guarded=N['GuardedZenodoClient'](client,guardedkit,metadata,[],lambda:None,'stage')
    check('create_once',lambda:must(guarded.create(metadata)['id']==17 and client.created==1))
    check('create_repeat_rejected',lambda:reject(lambda:guarded.create(metadata)))
    expected=[{'name':'a.pdf','size':1,'sha256':N['sha'](b'a')},{'name':'b.zip','size':1,'sha256':N['sha'](b'b')}]
    pub={'environment':'production','title':N['TITLE'],'files':expected,'id':17,'state':'published','doi':'10.5281/zenodo.17','record_url':'https://zenodo.org/records/17'}
    check('public_receipt_exact',lambda:must(N['validate_zenodo_receipt'](pub,expected,N['TITLE'],'publish',17)==17))
    for key,value in [('id',True),('environment','sandbox'),('doi','10.5281/zenodo.18'),('title','wrong'),('state','ready_to_publish'),('files',[])]:
        bad={**pub,key:value}
        check('receipt_reject_'+key,lambda bad=bad:reject(lambda:N['validate_zenodo_receipt'](bad,expected,N['TITLE'],'publish',17)))
    row=N['tracker_row'](pub);headers=['Original Problem','Solution Chat URL','DOI','Notes']
    check('tracker_absent',lambda:must(N['duplicate_tracker']([headers],row) is None))
    check('tracker_recover_exact',lambda:must(N['duplicate_tracker']([headers,row],row)==2))
    check('tracker_duplicate_rejected',lambda:reject(lambda:N['duplicate_tracker']([headers,row,row],row)))
    badrow=copy.deepcopy(row);badrow[2]='https://doi.org/10.5281/zenodo.18'
    check('tracker_same_problem_other_DOI_rejected',lambda:reject(lambda:N['duplicate_tracker']([headers,badrow],row)))
    check('tracker_headers_rejected',lambda:reject(lambda:N['duplicate_tracker']([['wrong']],row)))
    for value in ["'Math Puzzles'!A1:D1","Math Puzzles!A2:D2","'Math Puzzles'!A2:E2","'Math Puzzles'!A2:D3"]:
        check('tracker_invalid_range_'+value,lambda value=value:must(not N['valid_tracker_range'](value)))
    check('tracker_valid_range',lambda:must(N['valid_tracker_range']("'Math Puzzles'!A72:D72")))
    realqueue=N['blob'](N['HEAD'],N['QUEUE']);_,target,_,_=N['queue_parts'](realqueue)
    queue=b'PREFIX unrelated\n'+target+b'SUFFIX unrelated\n'
    event=N['native_event']({'freeze_sha256':'f'*64},pub,{'mergeCommit':{'oid':'a'*40}},{'updated_range':"'Math Puzzles'!A72:D72"})
    state='{"other": {"literal":"caf\u00e9", "number":1.00} \n}'.encode();history=b'{"id":"other","raw":1.00}'
    changed=N['native_replacements'](queue,state,history,event)
    check('native_unrelated_QUEUE_bytes',lambda:must(N['queue_parts'](queue)[0]==N['queue_parts'](changed[N['QUEUE']])[0]))
    check('native_unrelated_state_raw_prefix',lambda:must(changed[N['STATE']].startswith(state[:state.rfind(b'}')])) )
    check('native_unrelated_history_prefix',lambda:must(changed[N['HISTORY']].startswith(history)))
    check('native_no_fabricated_turns',lambda:must(event['turns_used']==4 and 'not authenticated' in event['turns_used_basis'] and 'candidate_turn' not in event and event['historical_native_turn_count']=='UNKNOWN' and event['new_author_proof_responses']==0))
    check('native_renderer_counter4of5_without_history_certification',lambda:must(str(event.get('turns_used',0))+'/'+str(event.get('turn_limit','unknown'))=='4/5' and event['author_native_history_authenticated'] is False and event['event']=='audited_imported_candidate_publication'))
    with Patch(blob=lambda ref,name:state if name==N['STATE'] else history):
        check('dynamic_native_absent_UNKNOWN',lambda:must(N['native_safety']('fake')['historical_native_turn_count']=='UNKNOWN'))
    with Patch(blob=lambda ref,name:json.dumps({N['KEY']:{'status':'claimed_solved'}}).encode() if name==N['STATE'] else history):
        check('dynamic_native_existing_state_rejected',lambda:reject(lambda:N['native_safety']('fake')))
    with Patch(blob=lambda ref,name:state if name==N['STATE'] else json.dumps({'id':N['KEY']}).encode()):
        check('dynamic_native_prior_target_event_rejected',lambda:reject(lambda:N['native_safety']('fake')))
    with Patch(blob=lambda ref,name:json.dumps({N['KEY']:event}).encode() if name==N['STATE'] else json.dumps(event).encode()):
        check('dynamic_native_exact_recovery',lambda:must(N['native_safety']('fake',event)['target_history_entries']==1))
    def publicget(url,cap):
        if '/api/records/' in url:return json.dumps({'id':17,'doi':pub['doi'],'metadata':{'title':N['TITLE']},'files':[{'key':x['name']} for x in expected]}).encode(),url,200
        if 'a.pdf' in url:return b'a',url,200
        if 'b.zip' in url:return b'b',url,200
        return b'page','https://zenodo.org/records/17',200
    with Patch(bounded_public_get=publicget):
        check('independent_public_bytes_DOI_fake_only',lambda:must(N['independent_public_verify'](pub,expected)['confirmed'] is True))
    def corrupt(url,cap):
        data,final,status=publicget(url,cap)
        return (b'x' if 'a.pdf' in url else data),final,status
    with Patch(bounded_public_get=corrupt):
        check('independent_public_wrong_bytes_rejected',lambda:reject(lambda:N['independent_public_verify'](pub,expected)))
    # Authenticate the real reviewed descriptor using only local kit check.
    D=N['D'];localfiles={name:N['fingerprint']((D/name).read_bytes()) for name in [N['PDF'],N['ZIP'],'zenodo-deposit.json']}
    check('actual_prepared_descriptor',lambda:must(len(N['descriptor_check']({'files':localfiles})[1])==2))
    check('actual_unchanged_kit_local_dry_run',lambda:must(kit['run'](argparse.Namespace(command='check',manifest=D/'zenodo-deposit.json',sandbox=False))['title']==N['TITLE']))
    files={name.relative_to(D).as_posix():N['fingerprint'](name.read_bytes()) for name in (D/'package').rglob('*') if name.is_file()}
    for name in [N['PDF'],N['ZIP'],'zenodo-deposit.json','FINDING_DISPOSITIONS.json','PR_DESCRIPTION.md','BUILD_RECEIPT.json',*['PACKAGE_REPLAY_'+x+'.json' for x in ['normal','O','OO','env2']]]:files[name]=N['fingerprint']((D/name).read_bytes())
    evidence={str((N['A']/name).relative_to(ROOT)):N['fingerprint']((N['A']/name).read_bytes()) for name in ['ORIGINAL_FILE_RECORDS.json','TARGET_IDENTITY_PREFLIGHT.json','ROOT_PRE_PACKAGE_SOURCE_CONTINUITY_06.json','source_record_private.txt','PUBLICATION_FINDINGS_REGISTER.md','ROOT_ORIGINAL_AUTHENTICATION_AND_BUDGET.json','ROOT_PROFILE_ROOT01_AUTHENTICATION.json','ROOT_PROFILE_ROOT01_REPLAY.json',*['reviews/'+family+'/MANIFEST.json' for family in N['FAMILY_PINS']]]}
    freeze={'schema':'pr948-publication-freeze-v1','created_utc':'2026-10-16T00:00:00+00:00','revision_candidate':1,'pr':948,'problem_id':N['KEY'],'original_pr_head':N['HEAD'],'operations_inventory_sha256':'1'*64,'pr_description_sha256':'2'*64,'package_manifest_sha256':N['sha']((D/'package/PACKAGE_MANIFEST.json').read_bytes()),'package_pdf':'paper/note.pdf','package_verifier':'profile/verify_package.py','files':files,'evidence_files':evidence,'future_helpers':{name:records[(P.relative_to(ROOT)/name).as_posix()] for name in N['HELPERS']},'replay_normalization_ignored':[]}
    context={'inventory_sha256':'1'*64,'inventory':inv}
    def authenticated_freeze(value):
        raw=json.dumps(value).encode();return N['freeze_check'](raw,N['sha'](raw),context)
    check('actual_closed_package_archive_PDF_freeze_rehearsal_no_approval',lambda:must(authenticated_freeze(freeze)['package_pdf']=='paper/note.pdf'))
    check('actual50_inherited_finding_ids',lambda:must(len(N['inherited_findings'](freeze))==50))
    check('actual_four_current50_canonical_replay_anchors',lambda:must(all(json.loads((D/('PACKAGE_REPLAY_'+label+'.json')).read_text()).get('package_manifest_sha256')==freeze['package_manifest_sha256'] and json.loads((D/('PACKAGE_REPLAY_'+label+'.json')).read_text()).get('returncode')==0 and json.loads((D/('PACKAGE_REPLAY_'+label+'.json')).read_text()).get('normalized_fields_ignored')==[] and json.loads((D/('PACKAGE_REPLAY_'+label+'.json')).read_text()).get('observed_outer_optimization')==opt for label,opt in zip(['normal','O','OO','env2'],[0,1,2,0]))))
    bad=copy.deepcopy(freeze);bad['extra_unreviewed_key']=True
    check('freeze_unknown_schema_key_rejected',lambda:reject(lambda:authenticated_freeze(bad)))
    bad=copy.deepcopy(freeze);bad['pr']=True
    check('freeze_boolean_PR_rejected',lambda:reject(lambda:authenticated_freeze(bad)))
    bad=copy.deepcopy(freeze);bad['evidence_files']={}
    check('freeze_missing_private_original_anchors_rejected',lambda:reject(lambda:authenticated_freeze(bad)))
    bad=copy.deepcopy(freeze);bad['package_manifest_sha256']='0'*64
    check('freeze_stale_manifest_anchor_rejected',lambda:reject(lambda:authenticated_freeze(bad)))
    raw=json.dumps(freeze).encode()
    check('freeze_external_pin_before_profile_execution',lambda:reject(lambda:N['freeze_check'](raw,'0'*64,context)))

    # Review schema/history fixtures are small and removed only in our own W.
    with tempfile.TemporaryDirectory(prefix='private-fixture-',dir=W) as temporary:
        F=Path(temporary);(F/'reviews').mkdir();(F/'preprint').mkdir()
        originals={'original':{'bytes':1,'sha256':'a'*64,'git_blob':'b'*40,'git_mode':'100644','disk_mode':'0644'}}
        helpers={'accept_pr948.py':{'bytes':1,'sha256':'c'*64}}
        freeze={'revision_candidate':1,'created_utc':'2026-10-16T00:00:00+00:00','package_manifest_sha256':'d'*64,'package_verifier':'profile/verify_package.py','future_helpers':helpers,'files':{N['PDF']:{'bytes':1,'sha256':'e'*64},'package/profile/verify_package.py':{'bytes':1,'sha256':'f'*64}}}
        pin='1'*64
        receipts={label:{'test_mode':label,'result':'pass'} for label in ['normal','O','OO','env2']}
        for label,receipt in receipts.items():(F/'preprint'/('PACKAGE_REPLAY_'+label+'.json')).write_text(json.dumps({'receipt':receipt}))
        def write_round(number,change=None):
            base=F/'reviews'/f'full_package_{number:02d}';base.mkdir(exist_ok=True)
            result={'pr':948,'problem_id':N['KEY'],'original_pr_head':N['HEAD'],'reviewer_agent_id':'fresh'+str(number),'clean_context':True,'entire_package_review':True,'full_reproducer_completed':True,'started_utc':f'2026-10-16T00:{number:02d}:00+00:00','completed_utc':f'2026-10-16T00:{number:02d}:59+00:00','candidate_revision':1,'candidate_pins':{'freeze':pin,'manifest':'d'*64,'pdf':'e'*64},'inspected_helper_hashes':helpers,'required_issues':[],'optional_issues':[],'clean_for_preprint':True,'strongest_verified_theorem':'Exact scoped theorem.','mathematical_remaining_gap_for_stated_theorem':None,'prior_issue_resolution':{},'inherited_finding_dispositions':{'finding':{'verified':True,'evidence':'Checked full package.'}}}
            if change:change(result)
            auth={'status':'PASS','utc':f'2026-10-16T00:{number:02d}:01+00:00','original_pr_head':N['HEAD'],'freeze_sha256':pin,'package_manifest_sha256':'d'*64,'future_helpers':helpers,'candidate_files':freeze['files'],'originals':{'original':{**originals['original'],'archive_mode':'100644','disk_and_archive_match':True}}}
            cold={'status':'PASS','utc':f'2026-10-16T00:{number:02d}:30+00:00','cold_extraction':True,'package_manifest_sha256':'d'*64,'externally_pinned_verifier_sha256':'f'*64,'normalized_fields_ignored':[],'modes':[{'mode':label,'observed_outer_optimization':opt,'returncode':0,'receipt':receipts[label]} for label,opt in zip(['normal','O','OO','env2'],[0,1,2,0])]}
            data={'RESULT.json':result,'AUTHENTICATION_START.json':auth,'AUTHENTICATION_END.json':{**auth,'utc':f'2026-10-16T00:{number:02d}:58+00:00'},'COLD_REPLAY.json':cold,'FULL_AUDIT.md':'Full independent report.','RESEARCH_LOG.md':'Completed all required checks.'}
            for name,value in data.items():(base/name).write_text(json.dumps(value) if name.endswith('.json') else value)
            mapping={'files':{name:N['fingerprint']((base/name).read_bytes()) for name in data},'explicit_public_allowlist':list(data)}
            raw=(json.dumps(mapping)+'\n').encode();(base/'MANIFEST.json').write_bytes(raw)
            return f'{number:02d}:'+N['sha'](raw)
        specs=[write_round(1),write_round(2)]
        with Patch(A=F,D=F/'preprint',original_check=lambda:originals,inherited_findings=lambda *args:{'finding'}):
            check('two_fresh_current_entire_reviews',lambda:must(len(N['review_check'](specs,freeze,pin,{})[0])==2))
            check('one_review_cannot_accept',lambda:reject(lambda:N['review_check'](specs[:1],freeze,pin,{})))
            badspec=[specs[0],write_round(2,lambda r:r.update(reviewer_agent_id='fresh1'))]
            check('duplicate_reviewer_rejected',lambda:reject(lambda:N['review_check'](badspec,freeze,pin,{})))
            badspec=[specs[0],write_round(2,lambda r:r.update(entire_package_review=False))]
            check('partial_review_rejected',lambda:reject(lambda:N['review_check'](badspec,freeze,pin,{})))
            badspec=[specs[0],write_round(2,lambda r:r.update(inherited_finding_dispositions={}))]
            check('missing_inherited_disposition_rejected',lambda:reject(lambda:N['review_check'](badspec,freeze,pin,{})))
            badspec=[specs[0],write_round(2,lambda r:r.update(optional_issues=[{'id':'OPTIONAL-1'}],clean_for_preprint=False))]
            check('optional_findings_require_fix_and_two_clean_reviews',lambda:reject(lambda:N['review_check'](badspec,freeze,pin,{})))
            clean3=write_round(3,lambda r:r.update(prior_issue_resolution={'OPTIONAL-1':{'verified':True,'evidence':'Fixed and independently checked.'}}))
            check('one_clean_after_optional_fix_is_insufficient',lambda:reject(lambda:N['review_check'](badspec+[clean3],freeze,pin,{})))
            clean4=write_round(4,lambda r:r.update(prior_issue_resolution={'OPTIONAL-1':{'verified':True,'evidence':'Fixed and independently checked.'}}))
            check('two_clean_after_optional_fix_accept_complete_history',lambda:must(len(N['review_check'](badspec+[clean3,clean4],freeze,pin,{})[0])==4))
            (F/'reviews'/'full_package_05').mkdir()
            check('unfinished_round_cannot_be_hidden',lambda:reject(lambda:N['review_check'](badspec,freeze,pin,{})))
    # This function is called only with fake gh/network reads; excluded mathematics
    # is never opened. The fake changed status chooses967 after952 is skipped.
    calls=[]
    def fakepr(number):return {'number':number,'state':'OPEN','isDraft':True,'headRefOid':str(number).zfill(40),'baseRefName':'main','baseRefOid':'f'*40,'currentBaseRefOid':'f'*40,'url':'https://example.invalid'}
    def fakerun(args,**kwargs):
        calls.append(args);head=args[-1].split('=',1)[1].split(':',1)[0];key='30000552' if head.endswith('952') else '30000967';status='unsolved' if key=='30000552' else 'claimed_solved'
        cells=['','1',key+' / CODE','title','0','0','0','0',status,'0/5','','','',''];queue='| '+ ' | '.join(cells[1:-1])+' |\n'
        return json.dumps({'data':{'repository':{'object':{'text':queue,'isBinary':False,'byteSize':len(queue.encode()),'oid':'x'}}}})
    with Patch(pr_view=fakepr,run=fakerun):
        inventory=[{'number':952,'headRefOid':str(952).zfill(40),'currentBaseRefOid':'f'*40,'entries':[{'id':'30000552'}]},{'number':967,'headRefOid':str(967).zfill(40),'currentBaseRefOid':'f'*40,'entries':[{'id':'30000967'}]}]
        check('dynamic_next952_skip_then967_status_only',lambda:must(N['gate_next'](inventory)[1]['number']==967 and len(calls)==2 and all(a[:3]==['gh','api','graphql'] for a in calls)))

if __name__=='__main__':
    started=datetime.now(timezone.utc).isoformat();error=None
    try:main()
    except Exception:
        error=traceback.format_exc()
    existing=list(W.glob('DEVELOPMENT_ATTEMPT_*.json'));number=len(existing)+1
    receipt={'schema':'pr948-workflow-development-tests-v1','started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'FAIL' if error else 'PASS','tests':RESULTS,'passed':sum(x['status']=='PASS' for x in RESULTS),'failed':sum(x['status']=='FAIL' for x in RESULTS),'external_mutations':0,'fake_external_calls_only':True,'own_temporary_fixtures_only':True,'error':error,'completion_percent':85}
    output=W/f'DEVELOPMENT_ATTEMPT_{number:02d}.json';output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'passed':receipt['passed'],'failed':receipt['failed'],'receipt':str(output)}))
    if error:print(error,file=sys.stderr);raise SystemExit(1)
