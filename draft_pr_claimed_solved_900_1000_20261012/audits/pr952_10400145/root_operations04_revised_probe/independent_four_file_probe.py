import argparse,contextlib,hashlib,io,json,pathlib,sys
p=argparse.ArgumentParser();p.add_argument('--compile-opt',type=int,choices=(0,1,2),required=True);args=p.parse_args()
P=pathlib.Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012');A=P/'audits/pr952_10400145';E=A/'operations_engineering_04';R=A/'root_operations04_revised_probe'
raw=(E/'PROPOSED_accept_pr952.py').read_bytes();EXPECTED='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec'
def need(x,m):
 if not x:raise RuntimeError(m)
need(hashlib.sha256(raw).hexdigest()==EXPECTED,'external proposal pin')
events=[]
for window in ('after_reconcile_return','before_audit_log','before_project_log'):
 n={'__name__':'inert_root_four_file_recovery','__file__':str(P/'accept_pr952.py')}
 exec(compile(raw,str(E/'PROPOSED_accept_pr952.py'),'exec',dont_inherit=True,optimize=args.compile_opt),n)
 own=R/('private_fixture_opt'+str(args.compile_opt)+'_'+window);own.mkdir();pr=own/'program';au=own/'audit';w=own/'workflow'
 for q in (pr,au,w):q.mkdir()
 n.update(P=pr,A=au,W=w)
 prefix=b'EXACT UNRELATED NONUTF8 \xff\r\nLATER TEXT WITHOUT FINAL NEWLINE'
 logs=[pr/'RESEARCH_LOG.md',au/'RESEARCH_LOG.md']
 for q in logs:q.write_bytes(prefix)
 accepted={'freeze_sha256':'f'*64,'full_package_reviews':[{'manifest_sha256':'1'*64},{'manifest_sha256':'2'*64}]};freeze={}
 pub={'id':17,'doi':'10.5281/zenodo.17','record_url':'https://zenodo.org/records/17'}
 merge={'mergeCommit':{'oid':'b'*40}};tracker={'updated_range':"'Math Puzzles'!A2:D2",'row':['Original','','https://doi.org/10.5281/zenodo.17','Synthetic']};native={'commit':'c'*40}
 state={'active_pr':952,'completed_prs':[],'completed_results':[],'published_prs':[],'eligible_prs':[952,955]}
 inventory=[{'number':952,'disposition':'pending_audit','headRefOid':n['HEAD'],'baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952','entries':[{'id':'10400145'}]},{'number':955,'disposition':'eligible','unrelated_bytes':'PRESERVE'}]
 for q,obj in[(pr/'CURRENT_STATE.json',state),(pr/'inventory.json',inventory),(w/'TRACKER_RECEIPT.json',tracker),(w/'NATIVE_PUBLICATION_RECEIPT.json',native)]:n['save'](q,obj)
 calls=[];gates=[]
 n['accepted_package']=lambda context:(accepted,freeze);n['merged_gate']=lambda *a:{};n['publication_links']=lambda *a:(pub,merge);n['independent_public_verify']=lambda *a:{'confirmed':True};n['descriptor_check']=lambda *a:({},[]);n['gws']=lambda *a:{'range':tracker['updated_range'],'values':[tracker['row']]};n['native_verify']=lambda *a:{'confirmed':True};n['accepted_review_check']=lambda *a:None;n['finalize_pr_metadata']=lambda *a:None
 def gate(*a):
  gates.append('SYNTHETIC_METADATA_ONLY');return [],{'number':955,'problem_id':'SYNTHETIC_NEXT','headRefOid':'d'*40}
 n['gate_next']=gate
 def forbidden(*a,**k):raise RuntimeError('real service/process forbidden')
 n['run']=forbidden;n['subprocess']=type('NoProcesses',(),{'run':staticmethod(forbidden)})
 first=[True]
 if window=='after_reconcile_return':
  real=n['reconcile_local_finalization']
  def interrupted(*a):
   result=real(*a)
   if first[0]:first[0]=False;raise OSError('OWN_INERT_INTERRUPTION')
   return result
  n['reconcile_local_finalization']=interrupted
 else:
  real=n['local_atomic_bytes'];target=logs[1 if window=='before_audit_log' else 0]
  def interrupted(path,*a):
   if path==target and first[0]:first[0]=False;raise OSError('OWN_INERT_INTERRUPTION')
   return real(path,*a)
  n['local_atomic_bytes']=interrupted
 try:n['finalize'](None,{})
 except OSError as e:need(str(e)=='OWN_INERT_INTERRUPTION','wrong actual failure')
 else:raise RuntimeError('injection not reached')
 before=[q.read_bytes()for q in logs]
 if window=='after_reconcile_return':need(all(b'PR952-LOCAL-COMPLETION-V1 'in b for b in before),'postreturn logs not complete')
 elif window=='before_audit_log':need(b'PR952-LOCAL-COMPLETION-V1 'in before[0] and before[1]==prefix,'between-log window not reached')
 else:need(before==[prefix,prefix],'before-first-log window not reached')
 value=json.loads((pr/'CURRENT_STATE.json').read_bytes());value.update(active_pr=969,active_problem_id='OWN_LATER_WORK',phase='KEEP_LATER_PHASE',next_pr=969,active_pr_completion_estimate_percent=73);n['save'](pr/'CURRENT_STATE.json',value);state_bytes=(pr/'CURRENT_STATE.json').read_bytes()
 out=io.StringIO()
 with contextlib.redirect_stdout(out):n['finalize'](None,{})
 result=json.loads(out.getvalue());after=[q.read_bytes()for q in logs]
 need(result['local_finalization']['confirmed']is True and result['local_finalization']['both_research_logs_confirmed']is True,'canonical not four-file complete')
 need((pr/'CURRENT_STATE.json').read_bytes()==state_bytes,'later state regressed')
 for old,b in zip(before,after):
  need(b.startswith(prefix+b'\n') and b.count(b'PR952-LOCAL-COMPLETION-V1 ')==1,'prefix lost/duplicate/missing log')
  if b'PR952-LOCAL-COMPLETION-V1 'in old:need(b==old,'existing marker rewritten')
  marker=json.loads(b.split(b'PR952-LOCAL-COMPLETION-V1 ')[1]);need(marker['approved_outcome']['doi']==pub['doi']and marker['workflow_completion_estimate_percent']==100,'wrong marker outcome')
 stable=[(pr/'CURRENT_STATE.json').read_bytes(),(pr/'inventory.json').read_bytes(),*after]
 with contextlib.redirect_stdout(io.StringIO()):n['finalize'](None,{})
 need(stable==[(pr/'CURRENT_STATE.json').read_bytes(),(pr/'inventory.json').read_bytes(),*[q.read_bytes()for q in logs]],'completed retry rewrites required files')
 need(len(gates)==1,'repeated metadata status gate')
 events.append({'window':window,'actual_compiled_core_optimization':args.compile_opt,'status':'PASS','later_active969_bytes_preserved':True,'existing_log_entries_bytes_preserved':True,'both_log_prefixes_and_unique_markers_verified':True,'all_four_files_stable_on_next_retry':True})
print(json.dumps({'status':'PASS_ROOT_ACTUAL_REVISED_PROPOSAL_FOUR_FILE_RECOVERY','core_sha256':EXPECTED,'actual_compiled_core_optimization':args.compile_opt,'events':events,'scope':'Actual proposed finalize/reconcile/read_regular/atomic byte writes and real fsync/rename under owned fixtures; accepted/source/merge/public/GWS/native/metadata boundaries explicitly inert. No service/Git/production-file changes or mathematical/clean-review credit.'},sort_keys=True))
