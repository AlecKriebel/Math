"""New full03 recovery-state and silent-loss probes. All external seams are inert.
Executes actual pinned finalize/reconciliation/atomic-write functions at requested
compile optimization; every filesystem fixture remains under this review.
"""
import sys,pathlib,json,hashlib,copy,tempfile,types,os,io,contextlib,datetime
R=pathlib.Path(__file__).resolve().parent;A=R.parents[1];P=A.parents[1];CORE=P/'accept_pr952.py';raw=CORE.read_bytes();PIN='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec'
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
need(hashlib.sha256(raw).hexdigest()==PIN,'external actual core pin')
def enc(v):return (json.dumps(v,indent=2)+'\n').encode()
EVENTS=[]
with tempfile.TemporaryDirectory(prefix='full03-recovery-',dir=R/'private') as td:
 root=pathlib.Path(td);pr=root/'project';au=root/'audit';w=root/'workflow'
 for p in [pr,au,w]:p.mkdir()
 n={'__name__':'_full03_inert_actual_core_','__file__':str(CORE)};exec(compile(raw,str(CORE),'exec',dont_inherit=True,optimize=sys.flags.optimize),n);n.update(ROOT=root,P=pr,A=au,W=w)
 calls=[]
 def counted(name,result):
  def f(*a,**k):calls.append(name);return copy.deepcopy(result)
  return f
 accepted={'freeze_sha256':'a'*64,'full_package_reviews':[{'manifest_sha256':'b'*64},{'manifest_sha256':'c'*64}]};freeze={};tracker={'updated_range':"'Math Puzzles'!A9:D9",'row':['p','','doi','n']};native={'commit':'d'*40};publication={'id':19,'doi':'10.5281/zenodo.19','record_url':'https://zenodo.org/records/19'};merge={'mergeCommit':{'oid':'e'*40}}
 n.update(accepted_package=counted('accepted_package',(accepted,freeze)),accepted_review_check=counted('accepted_review_check',None),merged_gate=counted('merged_gate',{'synthetic':True}),publication_links=counted('publication_links',(publication,merge)),descriptor_check=counted('descriptor_check',({},[])),independent_public_verify=counted('public_GET_verification',{'confirmed':True}),native_verify=counted('native_readback',{'confirmed':True}),finalize_pr_metadata=counted('metadata_ALREADY_CORRECT_readback',None),gws=counted('GWS_GET_only',{'range':tracker['updated_range'],'values':[tracker['row']]}),gate_next=counted('status_only_next_gate',([] ,{'number':955,'problem_id':'future','headRefOid':'f'*40})))
 def forbidden(*a,**k):raise RuntimeError('REAL_COMMAND_OR_SERVICE_MUTATION_FORBIDDEN')
 n['run']=forbidden;n['subprocess']=types.SimpleNamespace(run=forbidden)
 paths=[pr/'inventory.json',pr/'CURRENT_STATE.json',pr/'RESEARCH_LOG.md',au/'RESEARCH_LOG.md'];logs=[b'project unrelated\xff\r\nno newline',b'audit unrelated\xfe\x00\n']
 initial_state={'eligible_prs':[952,955],'completed_prs':[],'published_prs':[],'completed_results':[],'active_pr':952,'active_problem_id':'10400145','next_pr':952,'phase':'PR952','active_pr_completion_estimate_percent':90,'unrelated':{'literal':['KEEP',2]}}
 initial_inventory=[{'number':952,'headRefOid':n['HEAD'],'baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952','entries':[{'id':'10400145'}],'disposition':'pending_audit','unrelated_target':'KEEP'},{'number':955,'unrelated':'KEEP_LATER'}]
 def reset():
  for p in w.iterdir():p.unlink()
  for p,b in zip(paths,[enc(initial_inventory),enc(initial_state),*logs]):p.write_bytes(b);p.chmod(0o644)
  (w/'TRACKER_RECEIPT.json').write_bytes(enc(tracker));(w/'NATIVE_PUBLICATION_RECEIPT.json').write_bytes(enc(native));calls.clear()
 def invoke():
  with contextlib.redirect_stdout(io.StringIO()):return n['finalize'](None,{'inert_external_seams':True})
 def check(later=None):
  iv,st=[json.loads(p.read_bytes()) for p in paths[:2]];need(st['completed_prs']==[952] and st['published_prs']==[952] and len(st['completed_results'])==1,'single completion');need(iv[0]['disposition']=='accepted_merged_preprint_published' and iv[1]==initial_inventory[1] and iv[0]['unrelated_target']=='KEEP','inventory/outside preservation');need(st['unrelated']==initial_state['unrelated'],'state outside preservation')
  if later is not None:need(all(st[k]==v for k,v in later.items()),'later active context preserved')
  for p,b in zip(paths[2:],logs):need(p.read_bytes().startswith(b) and p.read_bytes().count(b'PR952-LOCAL-COMPLETION-V1 ')==1,'raw log prefix/single marker')
  receipt=json.loads((w/'LOCAL_FINALIZATION_RECEIPT.json').read_bytes());need(receipt['confirmed'] is True and receipt['both_research_logs_confirmed'] is True,'canonical success missing')
  for role,p in zip(['inventory','state','project_log','audit_log'],paths):need(receipt['after'][role]==n['fingerprint'](p.read_bytes()),'exact current canonical pin')
  old=[p.read_bytes() for p in paths];calls.clear();invoke();need(old==[p.read_bytes() for p in paths] and 'status_only_next_gate' not in calls,'idempotent retry without next selection')
 reset();initial=[p.read_bytes() for p in paths];invoke();complete=[p.read_bytes() for p in paths];record=(w/'PUBLICATION_RECORD.json').read_bytes()
 # Every compatible subset of four already-completed files, including initial
 # state plus completed inventory, independently missing logs, and later program.
 for mask in range(16):
  for preserve_later in [False,True]:
   reset();(w/'PUBLICATION_RECORD.json').write_bytes(record)
   for i,p in enumerate(paths):p.write_bytes(complete[i] if mask&(1<<i) else initial[i])
   later=None
   if preserve_later:
    later={'active_pr':969,'active_problem_id':'later969','next_pr':969,'active_original_head':'9'*40,'phase':'ONGOING_LATER','active_pr_completion_estimate_percent':72,'priority_status':{'keep':'LATER'}};st=json.loads(paths[1].read_bytes());st.update(later);paths[1].write_bytes(enc(st))
   invoke();check(later);EVENTS.append({'case':'all_compatible_four_view_subsets','mask':mask,'later':preserve_later,'status':'PASS'})
 # A filesystem replace that returns success while discarding the requested write
 # must fail exact readback. No exception-based injection is used for the loss.
 for victim in paths:
  reset();realos=n['os'];dropped=[False]
  class SilentLoss:
   def __getattr__(self,k):return getattr(os,k)
   def replace(self,src,dst,**kw):
    if dst==victim.name and not dropped[0]:dropped[0]=True;os.unlink(src,dir_fd=kw['src_dir_fd']);return None
    return os.replace(src,dst,**kw)
  # Two logs share a basename. Reach the correct role via the actual target dirfd.
  class ExactSilentLoss(SilentLoss):
   def replace(self,src,dst,**kw):
    same=os.fstat(kw['dst_dir_fd']).st_ino==victim.parent.stat().st_ino
    if dst==victim.name and same and not dropped[0]:dropped[0]=True;os.unlink(src,dir_fd=kw['src_dir_fd']);return None
    return os.replace(src,dst,**kw)
  n['os']=ExactSilentLoss()
  try:invoke()
  except RuntimeError as e:need(dropped[0] and 'local atomic exact readback' in str(e),'silent loss must reach exact readback')
  else:raise RuntimeError('silent lost write reported complete')
  need(json.loads((w/'LOCAL_FINALIZATION_RECEIPT.json').read_bytes())['confirmed'] is False,'early canonical success on silent loss');n['os']=realos;invoke();check();EVENTS.append({'case':'silent_successful_replace_loss','path_role':paths.index(victim),'status':'REJECTED_THEN_RECOVERED'})
 reset();save=n['save'];dropped=[False]
 def lose_receipt(path,value,*a,**k):
  if path==w/'LOCAL_FINALIZATION_RECEIPT.json' and value.get('confirmed') is True and not dropped[0]:dropped[0]=True;return None
  return save(path,value,*a,**k)
 n['save']=lose_receipt
 try:invoke()
 except RuntimeError as e:need('canonical local completion receipt exact readback' in str(e),'silent receipt loss not detected')
 else:raise RuntimeError('silent receipt loss reported success')
 n['save']=save;invoke();check();EVENTS.append({'case':'silent_confirmed_receipt_save_loss','status':'REJECTED_THEN_RECOVERED'})
 reset();load=n['load'];lost=[False]
 def lost_readback(path):
  v=load(path)
  if path==w/'LOCAL_FINALIZATION_RECEIPT.json' and v.get('confirmed') is True and not lost[0]:lost[0]=True;raise OSError('INERT_LOST_CANONICAL_READBACK')
  return v
 n['load']=lost_readback
 try:invoke()
 except OSError as e:need(str(e)=='INERT_LOST_CANONICAL_READBACK','wrong lost readback')
 else:raise RuntimeError('readback loss not reached')
 n['load']=load;before=[p.read_bytes() for p in paths];invoke();check();need(before==[p.read_bytes() for p in paths],'lost readback retry rewrote four views');EVENTS.append({'case':'lost_final_canonical_readback_after_actual_save','status':'RECOVERED_WITHOUT_DUPLICATION'})
print(json.dumps({'schema':'full03-independent-recovery-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_INERT_NEW_ATTACKS','core_sha256':PIN,'actual_compile_optimization':sys.flags.optimize,'events':EVENTS,'event_count':len(EVENTS),'real_external_mutations':0,'scope':'Explicit inert accepted/source/publication/GWS/native/metadata seams; actual local finalizer and all local bytes/writes/readbacks.'},sort_keys=True))
