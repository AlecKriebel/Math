import sys
if not sys.flags.safe_path:raise SystemExit('safe startup')
import pathlib,json,hashlib,copy,contextlib,io,types,datetime
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';W=A/'reviews/full_package_01';source=P/'accept_pr946.py';b=source.read_bytes()
if hashlib.sha256(b).hexdigest()!='c9dc84ce258488ce9929fba2b2e7cc3a19077a3cf52d9fac1cea0c9798ab9ad8':raise ValueError('pin')
N={'__name__':'_mock_finalize_','__file__':str(source)};exec(compile(b,str(source),'exec'),N)
fix=W/'private/finalize_fixture';effort=fix/'effort';audit=effort/'audits/pr946_6000001';audit.mkdir(parents=True);N['P']=effort;N['A']=audit;N['D']=audit/'preprint'
for q in [effort/'README.md',effort/'RESEARCH_LOG.md',audit/'RESEARCH_LOG.md']:q.write_text('Synthetic fixture only.\n')
oldbody='reviewed original synthetic body';pub={'id':12,'doi':'10.5281/zenodo.12','record_url':'https://zenodo.org/records/12'};merge={'number':946,'state':'MERGED','baseRefName':'main','headRefOid':N['HEAD'],'mergeCommit':{'oid':'a'*40}};tracker={'updated_range':"'Math Puzzles'!A2:D2",'row':['p','','https://doi.org/10.5281/zenodo.12','note']};native={'commit':'b'*40};accepted={'exact_claim':'Synthetic theorem fixture.','full_package_reviews':[{'manifest_sha256':'1'*64},{'manifest_sha256':'2'*64}]};freeze={'pr_description_sha256':hashlib.sha256(oldbody.encode()).hexdigest(),'revision_candidate':1}
oldpub='PR904_PR905_PR906_PR908_PR909_PR919_PR938_published_tracker_native_ledgers_verified';oldtool='Separatesealedv2FIFO/caprepairrootauthenticatedandfreshnormal/4negativePASS; oldv1immutable'
state={'active_pr':946,'active_problem_id':'6000001','eligible_prs':[904,905,906,908,909,919,938,946,947],'completed_prs':[904,905,906,908,909,919,938],'completed_results':[{'pr':n,'outcome':'accepted_merged_preprint_published'} for n in [904,905,906,908,909,919,938]],'publication':oldpub,'portable_release_tooling':oldtool,'review_families':['pr946_jet'],'active_original_head':N['HEAD']}
saved={};calls=[]
N['accepted_package']=lambda c:(accepted,freeze);N['merged_gate']=lambda a,f:{};N['publication_links']=lambda *a:(pub,merge);N['native_verify']=lambda *a:{'status':'PASS','synthetic':True};N['gws']=lambda args:{'range':tracker['updated_range'],'values':[tracker['row']]}
def load(path):
 if path==audit/'TRACKER_RECEIPT.json':return copy.deepcopy(tracker)
 if path==audit/'NATIVE_PUBLICATION_RECEIPT.json':return copy.deepcopy(native)
 if path==effort/'CURRENT_STATE.json':return copy.deepcopy(state)
 if path==effort/'inventory.json':return [{'number':946},{'number':947}]
 raise RuntimeError('unexpected mock read '+str(path))
N['load']=load;N['save']=lambda path,value,**k:saved.__setitem__(path,copy.deepcopy(value));N['gate_next']=lambda inventory,st:([],{'number':947,'problem_id':'synthetic_next','headRefOid':'c'*40})
counter=[0]
def view():
 counter[0]+=1
 if counter[0]==1:return {**merge,'body':oldbody,'title':'old'}
 return {**merge,'body':(audit/'PR_PUBLISHED_BODY.md').read_text(),'title':'6000001: accepted global Hessian construction and published preprint'}
N['pr_view']=view
oldrun=N['subprocess'].run
N['subprocess'].run=lambda args,**kwargs:calls.append(args) or types.SimpleNamespace(returncode=0,stdout='mock',stderr='')
try:
 with contextlib.redirect_stdout(io.StringIO()):N['finalize'](types.SimpleNamespace(),{})
finally:N['subprocess'].run=oldrun
out=saved[effort/'CURRENT_STATE.json']
if out['active_pr']!=947 or 946 not in out['published_prs'] or out['publication']!=oldpub or out['portable_release_tooling']!=oldtool:raise RuntimeError('observation not reproduced')
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'OBSERVATION_REPRODUCED','id':'FP01-OPS-003','active_pr_after':out['active_pr'],'published_prs_after':out['published_prs'],'stale_publication_after':out['publication'],'stale_portable_release_tooling_after':out['portable_release_tooling'],'external_actions':0,'mocked_commands':len(calls),'recommendation':'Refresh global publication summary from completed_results/published_prs and clear or scope portable_release_tooling to PR946 before selecting next active target.'}
(W/'FINALIZE_STATE_ADVERSARY.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
