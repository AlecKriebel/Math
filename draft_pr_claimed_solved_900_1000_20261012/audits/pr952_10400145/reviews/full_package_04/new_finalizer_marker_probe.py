"""New full04 design: actual finalizer adoption/rejection of log markers.
Fixture setup follows inspected earlier four-file tests, but marker-boundary
case designs are new. All service/acceptance/source/metadata seams are inert.
"""
from pathlib import Path
import sys,json,copy,hashlib,tempfile,datetime,contextlib,io,types
R=Path(__file__).resolve().parent;A=R.parents[1];P=A.parents[1];raw=(P/'accept_pr952.py').read_bytes();PIN='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec'
def need(v,m):
 if not v:raise RuntimeError(m)
need(hashlib.sha256(raw).hexdigest()==PIN,'external core pin')
def encode(v):return (json.dumps(v,indent=2)+'\n').encode()
events=[]
with tempfile.TemporaryDirectory(prefix='marker04-',dir=R/'fixtures') as td:
 root=Path(td);pr=root/'project';au=pr/'audit';w=au/'workflow'
 w.mkdir(parents=True)
 n={'__name__':'inert_full04_actual_core','__file__':str(P/'accept_pr952.py')};exec(compile(raw,str(P/'accept_pr952.py'),'exec',dont_inherit=True,optimize=sys.flags.optimize),n);n.update(ROOT=root,P=pr,A=au,W=w)
 calls=[]
 accepted={'freeze_sha256':'a'*64,'full_package_reviews':[{'manifest_sha256':'b'*64},{'manifest_sha256':'c'*64}]};freeze={};publication={'id':23,'doi':'10.5281/zenodo.23','record_url':'https://zenodo.org/records/23'};merge={'mergeCommit':{'oid':'d'*40}};tracker={'updated_range':"'Math Puzzles'!A7:D7",'row':['p','','d','n']};native={'commit':'e'*40}
 def seam(name,v):
  def f(*a,**k):calls.append(name);return copy.deepcopy(v)
  return f
 n.update(accepted_package=seam('accepted',(accepted,freeze)),accepted_review_check=seam('authority',None),merged_gate=seam('merge',{}),publication_links=seam('links',(publication,merge)),descriptor_check=seam('descriptor',({},[])),independent_public_verify=seam('public',{'confirmed':True}),native_verify=seam('native',{'confirmed':True}),finalize_pr_metadata=seam('metadata',None),gws=seam('GWS_GET',{'range':tracker['updated_range'],'values':[tracker['row']]}),gate_next=seam('next',([],None)))
 def forbidden(*a,**k):raise RuntimeError('REAL_SERVICE_OR_GIT_BOUNDARY_FORBIDDEN')
 n.update(run=forbidden,subprocess=types.SimpleNamespace(run=forbidden),urlopen=forbidden)
 paths=[pr/'inventory.json',pr/'CURRENT_STATE.json',pr/'RESEARCH_LOG.md',au/'RESEARCH_LOG.md']
 inv=[{'number':952,'headRefOid':n['HEAD'],'baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952','entries':[{'id':'10400145'}],'disposition':'claimed_solved'},{'number':971,'untouched':['Ω',3]}]
 st={'eligible_prs':[952,971],'completed_prs':[],'published_prs':[],'completed_results':[],'active_pr':952,'unrelated':{'text':'keep'}}
 prefixes=[b'project\x00\xff\r\n',b'audit\xfe\n']
 def reset():
  for q in w.iterdir():q.unlink()
  for q,b in zip(paths,[encode(inv),encode(st),*prefixes]):q.write_bytes(b);q.chmod(0o644)
  (w/'TRACKER_RECEIPT.json').write_bytes(encode(tracker));(w/'NATIVE_PUBLICATION_RECEIPT.json').write_bytes(encode(native));calls.clear()
 def invoke():
  with contextlib.redirect_stdout(io.StringIO()):n['finalize'](None,{'seams':'inert'})
 reset();invoke();record=(w/'PUBLICATION_RECORD.json').read_bytes();completed=[q.read_bytes() for q in paths];marker=completed[2][len(prefixes[0]):];need(marker.startswith(b'PR952-LOCAL-COMPLETION-V1 '),'actual canonical marker extracted')
 token=b'PR952-LOCAL-COMPLETION-V1 ';md=json.loads(marker[len(token):])
 cases=[]
 bad=copy.deepcopy(md);bad['approved_outcome']['accepted_freeze_sha256']='f'*64;bad['approved_sha256']=hashlib.sha256(json.dumps(bad['approved_outcome'],sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()).hexdigest();cases.append(('internally_consistent_foreign_freeze_marker',token+json.dumps(bad,sort_keys=True,separators=(',',':')).encode()+b'\n'))
 bad=copy.deepcopy(md);bad['approved_outcome']['clean_final_review_manifest_sha256']='f'*64;bad['approved_sha256']=hashlib.sha256(json.dumps(bad['approved_outcome'],sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()).hexdigest();cases.append(('internally_consistent_foreign_review_marker',token+json.dumps(bad,sort_keys=True,separators=(',',':')).encode()+b'\n'))
 cases += [('equivalent_noncanonical_spacing',token+json.dumps(md,sort_keys=True).encode()+b'\n'),('CRLF_marker',marker[:-1]+b'\r\n'),('BOM_prefixed_marker',b'\xef\xbb\xbf'+marker),('duplicate_marker',marker+marker),('embedded_reserved_token',b'narrative '+marker),('truncated_marker',marker[:-1])]
 for role in (2,3):
  for name,malformed in cases:
   reset();(w/'PUBLICATION_RECORD.json').write_bytes(record);paths[role].write_bytes(prefixes[role-2]+malformed);before=[q.read_bytes() for q in paths]
   try:invoke()
   except RuntimeError as e:
    need([q.read_bytes() for q in paths]==before,'conflicting marker changed required files');need('next' not in calls,'conflict reached later gate');events.append({'role':role,'test':name,'status':'REJECTED_BEFORE_REQUIRED_WRITES','guard':str(e)})
   else:raise RuntimeError('marker attack accepted '+name)
 # Compatible completed markers may appear anywhere in both logs, followed by
 # arbitrary non-UTF8 new narrative. They must not be removed, duplicated or moved.
 for later in (False,True):
  reset();(w/'PUBLICATION_RECORD.json').write_bytes(record)
  for idx in (2,3):paths[idx].write_bytes(completed[idx]+b'later independent notes\xff\x00\n')
  if later:
   state=copy.deepcopy(st);state.update(active_pr=971,active_problem_id='later971',phase='ongoing',priority_status={'keep':True});paths[1].write_bytes(encode(state))
  saved_logs=[q.read_bytes() for q in paths[2:]];invoke();need([q.read_bytes() for q in paths[2:]]==saved_logs,'compatible marked raw logs moved/rewritten');need(json.loads(paths[0].read_bytes())[1]==inv[1],'unrelated inventory changed')
  if later:need('next' not in calls and json.loads(paths[1].read_bytes())['priority_status']=={'keep':True},'later context disturbed')
  need(json.loads((w/'LOCAL_FINALIZATION_RECEIPT.json').read_bytes())['both_research_logs_confirmed'] is True,'missing actual final receipt')
  events.append({'test':'adopt_exact_markers_with_later_raw_notes','later_context':later,'status':'PASS_PRESERVE_EXACT_LOG_BYTES'})
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_NEW_ACTUAL_FINALIZER_MARKER_ATTACKS','actual_compile_optimization':sys.flags.optimize,'core_sha256':PIN,'event_count':len(events),'events':events,'real_service_or_Git_mutations':0,'scope':'Actual finalize/reconcile/load/save/atomic/readback functions. Explicit inert external authority/public/GWS/native/metadata boundaries. No multiwriter CAS or cross-file transaction claim.'},sort_keys=True))
