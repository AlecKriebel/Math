"""Independent crash-window probe of actual finalize local state/inventory writes."""
import contextlib,hashlib,io,json,pathlib,sys
P=pathlib.Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012');A=P/'audits/pr952_10400145';R=A/'root_finalization_replay/full_package_02'
def need(x,m):
 if not x:raise RuntimeError(m)
raw=(P/'accept_pr952.py').read_bytes();need(hashlib.sha256(raw).hexdigest()=='888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8','external current actual core')
n={'__name__':'inert_finalize_crash_probe','__file__':str(P/'accept_pr952.py')};exec(compile(raw,str(P/'accept_pr952.py'),'exec',dont_inherit=True,optimize=sys.flags.optimize),n)
own=R/('private_finalize_crash_'+str(sys.flags.optimize));own.mkdir();p=own/'program';p.mkdir();a=own/'audit';a.mkdir();w=own/'workflow';w.mkdir();n.update(P=p,A=a,W=w)
for log in [p/'RESEARCH_LOG.md',a/'RESEARCH_LOG.md']:log.write_text('SYNTHETIC LOCAL FINALIZATION FIXTURE\n')
accepted={'freeze_sha256':'f'*64,'full_package_reviews':[{'manifest_sha256':'1'*64},{'manifest_sha256':'2'*64}]};freeze={};pub={'id':17,'doi':'10.5281/zenodo.17','record_url':'https://zenodo.org/records/17'};merge={'mergeCommit':{'oid':'b'*40}}
tracker={'updated_range':"'Math Puzzles'!A2:D2",'row':['Original','','https://doi.org/10.5281/zenodo.17','Synthetic']};native={'commit':'c'*40}
state={'active_pr':952,'completed_prs':[],'completed_results':[],'published_prs':[],'eligible_prs':[952,955]};inventory=[{'number':952,'disposition':'claimed_solved'},{'number':955,'disposition':'eligible'}]
REAL_SAVE=n['save']
for path,obj in [(p/'CURRENT_STATE.json',state),(p/'inventory.json',inventory),(w/'TRACKER_RECEIPT.json',tracker),(w/'NATIVE_PUBLICATION_RECEIPT.json',native)]:REAL_SAVE(path,obj)
counts={'metadata':0,'gates':0,'inventory_write_attempts':0};crash={'once':True}
n['accepted_package']=lambda context:(accepted,freeze);n['merged_gate']=lambda *args:{};n['publication_links']=lambda *args:(pub,merge);n['independent_public_verify']=lambda *args:{'confirmed':True};n['descriptor_check']=lambda *args:({},[]);n['gws']=lambda *args:{'range':tracker['updated_range'],'values':[tracker['row']]};n['native_verify']=lambda *args:{'confirmed':True};n['accepted_review_check']=lambda *args:None
def metadata(*args):counts['metadata']+=1
def gate(*args):counts['gates']+=1;return [],{'number':955,'problem_id':'SYNTHETIC_NEXT','headRefOid':'d'*40}
n['finalize_pr_metadata']=metadata;n['gate_next']=gate
def save(path,value,exclusive=False):
 if path==p/'inventory.json':
  counts['inventory_write_attempts']+=1
  if crash['once']:crash['once']=False;raise OSError('INERT_CRASH_AFTER_CURRENT_STATE_BEFORE_INVENTORY')
 return REAL_SAVE(path,value,exclusive)
n['save']=save
first_error=None
try:n['finalize'](None,{})
except OSError as e:first_error=str(e)
need(first_error=='INERT_CRASH_AFTER_CURRENT_STATE_BEFORE_INVENTORY','exact crash window not reached')
after_first_state=n['load'](p/'CURRENT_STATE.json');after_first_inventory=n['load'](p/'inventory.json')
need(952 in after_first_state['completed_prs'] and after_first_inventory[0]['disposition']=='claimed_solved','first write was not durably applied before failed second write')
second=io.StringIO()
with contextlib.redirect_stdout(second):n['finalize'](None,{})
second_output=json.loads(second.getvalue());after_second_state=n['load'](p/'CURRENT_STATE.json');after_second_inventory=n['load'](p/'inventory.json')
reproduced=(second_output.get('already_finalized') is True and after_second_inventory==inventory and 952 in after_second_state['completed_prs'] and counts['inventory_write_attempts']==1)
need(reproduced,'suspected local finalization recovery gap not reproduced')
print(json.dumps({'status':'REPRODUCED_CURRENT_CANDIDATE_FINALIZATION_RECOVERY_GAP','outer_optimization':sys.flags.optimize,'actual_core_compile_optimize':sys.flags.optimize,'core_sha256':hashlib.sha256(raw).hexdigest(),'first_exception':first_error,'second_actual_output':second_output,'state_marks_PR952_completed':952 in after_second_state['completed_prs'],'inventory_PR952_disposition_after_successful_rerun':after_second_inventory[0]['disposition'],'inventory_has_DOI_after_successful_rerun':'doi' in after_second_inventory[0],'inert_counts':counts,'real_service_or_Git_mutations':0,'actual_function':'finalize','synthetic_boundaries':['accepted_package','merged_gate','publication_links','independent_public_verify','descriptor_check','gws','native_verify','accepted_review_check','finalize_pr_metadata','gate_next'],'scope':'Actual finalize, actual raw local load/save and its already-finalized branch; one injected I/O error between two actual own-fixture state writes. No production file or service mutation.'},sort_keys=True))
