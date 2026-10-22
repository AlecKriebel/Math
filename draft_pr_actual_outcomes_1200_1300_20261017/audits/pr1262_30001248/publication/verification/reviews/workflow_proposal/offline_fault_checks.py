#!/usr/bin/env python3
"""Additional explicitly synthetic postmerge and actual-kit mutation fault tests."""
from pathlib import Path
import contextlib,copy,datetime,hashlib,importlib.util,io,json,os,subprocess,sys,tempfile,types
ROOT=Path(__file__).resolve().parent
POSTMERGE=(ROOT/'verify_pr1262_merge.py') if (ROOT/'verify_pr1262_merge.py').exists() else ROOT.parents[2]/'publication_coordinators/verify_pr1262_merge.py'
def load(p):
 spec=importlib.util.spec_from_file_location('fault_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def need(v,m):
 if not v:raise RuntimeError(m)
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def reject(fn,label,errors=(ValueError,RuntimeError,KeyError,FileNotFoundError)):
 try:fn()
 except errors:return label
 raise RuntimeError('Unexpected acceptance '+label)
def capture(fn):
 with contextlib.redirect_stdout(io.StringIO()):return fn()
def postmerge_cases(w,f):
 pub=f['pub'];audit=f['audit'];program=pub.parents[2];os.environ['PATH']=f['env']['PATH'];u=w.load(pub/'update_pr_publication.py');t=w.load(pub/'append_tracker.py')
 p,tracker,_=w.publication_and_tracker_controls(f);p['doi_resolution']={'status':'resolved','http_status':200};save(pub/'PUBLICATION_RECEIPT.json',p)
 files,_,note=u.desired_files(f['build'],p,tracker,f['snapshot']);body=note+'\nThe eight-file MANIFEST.json binds the seven other current mathematical edition records through entries/file/bytes/sha256. publication_20261017/ adds the reviewed preprint, portable verification archive, matching deposit metadata, publication receipt and README. Original historical files are preserved in the portable archive.\n';(pub/'PR_BODY_FINAL.md').write_text(body)
 head='a'*40;merge='b'*40;oldmain='c'*40;wanted=u.expected_identity(p,tracker,files,body);receipt={**wanted,'commit':head,'body_readback_verified':True,'remote_readback_verified':True};save(pub/'PR_BRANCH_RECEIPT.json',receipt)
 path=program/'publication_coordinators/verify_pr1262_merge.py';path.write_bytes(POSTMERGE.read_bytes());m=w.load(path);case={'fault':None};events=[];source_gate=u.validate_workflow_gate;source_saved=u.validate_saved
 # Actual gate and saved-commit validation run. Only external/Git I/O is mocked.
 def git(*args,data=None):
  events.append(args);fault=case['fault']
  if args==('branch','--show-current'):return b'main\n'
  if args[0]=='rev-list':
   commit=args[-1]
   return (head+' '+u.ORIGINAL+'\n').encode() if commit==head else (merge+' '+oldmain+' '+('d'*40 if fault=='merge_parent' else head)+'\n').encode()
  if args[0]=='diff-tree':return ('\n'.join(sorted(files))+'\n').encode()
  if args[0]=='show':
   commit,name=args[1].split(':',1);return b'corrupted merged bytes' if commit==merge and fault=='merged_blob' else files[name]
  if args[0] in {'fetch','update-ref'}:return b''
  raise RuntimeError('Unexpected mocked Git call '+repr(args))
 u.git=git
 def pr_read(args,**kwargs):
  need(args[:4]==['gh','pr','view','1262'],'Unexpected external call')
  return json.dumps({'state':'MERGED','headRefOid':'d'*40 if case['fault']=='wrong_head' else head,'headRefName':u.BRANCH,'mergeCommit':{'oid':merge},'mergedAt':'2026-10-17T23:00:00Z','body':'outside' if case['fault']=='wrong_body' else body,'url':'https://github.com/AlecKriebel/Math/pull/1262'})
 def tracker_read(parts,params,body=None):
  need(parts==['spreadsheets','values','get'],'Unexpected sheet operation')
  headers=['Original Problem','Solution Chat URL','DOI','Notes'];row=tracker['row'][:]
  if case['fault']=='column_B':row[1]='nonempty'
  if case['fault']=='headers':headers[0]='outside'
  return {'values':[headers,row]+([row[:]] if case['fault']=='duplicate_row' else [])}
 t.call=tracker_read
 m.runpy=types.SimpleNamespace(run_path=lambda raw:vars(u) if Path(raw).name=='update_pr_publication.py' else vars(t) if Path(raw).name=='append_tracker.py' else (_ for _ in ()).throw(RuntimeError('Unexpected script '+str(raw))))
 m.subprocess=types.SimpleNamespace(check_output=pr_read)
 base_state={'current_pr':1262,'completed_prs':[1205,1211,1216,1225,1241,1261],'publications':[],'eligible_count':12}
 saved_pub=(pub/'PUBLICATION_RECEIPT.json').read_bytes();faults=['wrong_head','wrong_body','merge_parent','merged_blob','duplicate_row','column_B','headers','unresolved_DOI'];rejections=[]
 for fault in faults:
  case['fault']=fault;save(program/'PROGRAM_STATE.json',base_state);(pub/'PUBLICATION_RECEIPT.json').write_bytes(saved_pub)
  if fault=='unresolved_DOI':bad=copy.deepcopy(p);bad['doi_resolution']={'status':'unresolved'};save(pub/'PUBLICATION_RECEIPT.json',bad);save(pub/'DOI_INSPECT.json',bad)
  rejections.append(reject(lambda:capture(m.main),fault));need(json.loads((program/'PROGRAM_STATE.json').read_text())==base_state,'Fault advanced state '+fault)
  if (pub/'DOI_INSPECT.json').exists():(pub/'DOI_INSPECT.json').unlink()
 case['fault']=None;save(program/'PROGRAM_STATE.json',base_state);(pub/'PUBLICATION_RECEIPT.json').write_bytes(saved_pub);capture(m.main)
 actual=json.loads((program/'PROGRAM_STATE.json').read_text());disposition=json.loads((audit/'FINAL_DISPOSITION.json').read_text());need(actual['current_pr']==1268 and actual['completed_prs']==base_state['completed_prs']+[1262] and len(actual['publications'])==1,'Successful postmerge state differs');need(disposition['all13_merged_files_exact'] and len(json.loads((pub/'MERGE_RECEIPT.json').read_text())['files'])==13,'Postmerge does not check thirteen')
 return {'success_advances_only1262_to1268':True,'all13_blobs_body_parents_unique_full_row_resolved_DOI_checked':True,'actual_gate_and_saved_tree_checks_executed':True,'faults_rejected_without_state_advance':rejections,'all_external_Git_service_calls_mocked':True,'git_io_operations_mocked':sorted({e[0] for e in events})}
def strict_actual_kit_cases(w,f):
 pub=f['pub'];os.environ['PATH']=f['env']['PATH'];c=w.load(pub.parents[2]/'publication_coordinators/pr1262.py');kit=c.load_exact_kit();kit.STATE_DIR=pub/'additional-synthetic-kit-state';meta,files=kit.load_manifest(pub/'zenodo-deposit.json');kit.doi_status=lambda doi:{'status':'synthetic_not_checked'}
 # The real kit.run re-fetches a known draft and invokes the installed exact
 # verifier inside its publish branch, before the mock client's publish method.
 base={'id':123,'submitted':False,'metadata':copy.deepcopy(meta),'files':[{'filename':e['name'],'filesize':e['size'],'checksum':'md5:'+e['md5']} for e in files]};current=copy.deepcopy(base);events=[]
 class Client:
  def get(self,number):events.append('GET');need(number==123,'Unexpected ID');return copy.deepcopy(current)
  def publish(self,number):events.append('POST publish');current.update(submitted=True,doi='10.5281/zenodo.123')
 client=Client()
 def invoke():return kit.run(types.SimpleNamespace(command='publish',manifest=pub/'zenodo-deposit.json',sandbox=False,confirm_id=123,check_doi=False),client=client)
 # The actual kit requires its own persisted known-ID state, scoped to scratch.
 manifest=(pub/'zenodo-deposit.json').resolve();place,_=kit.local_state(manifest,'production');kit.save_state(place,{'manifest':str(manifest),'environment':'production','id':123})
 rejected=[]
 for field in sorted(meta):
  current=copy.deepcopy(base)
  if field=='description':current['metadata'][field]=meta[field].replace('&','&amp;')
  elif isinstance(meta[field],list):current['metadata'][field]=[] if meta[field] else [{'unexpected':'wrong'}]
  else:current['metadata'][field]='corrupt'
  before=len(events);rejected.append(reject(invoke,'metadata_'+field,errors=(kit.DepositError,RuntimeError,ValueError)));need('POST publish' not in events[before:],'Fault reached POST '+field)
 for label,mutate in [('file_size',lambda d:d['files'][0].update(filesize=0)),('file_digest',lambda d:d['files'][0].update(checksum='md5:'+'0'*32)),('file_missing',lambda d:d['files'].pop()),('file_extra',lambda d:d['files'].append(copy.deepcopy(d['files'][0]))),('wrong_id',lambda d:d.update(id=124))]:
  current=copy.deepcopy(base);mutate(current);before=len(events);rejected.append(reject(invoke,label,errors=(kit.DepositError,RuntimeError,ValueError)));need('POST publish' not in events[before:],'Fault reached POST '+label)
 current=copy.deepcopy(base);result=invoke();need(result['state']=='published' and events.count('POST publish')==1,'Unchanged draft should have exactly one mock POST')
 return {'all11_supplied_field_corruptions_rejected_before_POST':True,'generic_kit_accepted_entity_normalization_rejected_inside_actual_kit_run':True,'file_and_ID_faults':rejected,'unchanged_permitted_exactly_one_mock_POST':True,'all_network_calls_mocked':True}
def worker():
 w=load(ROOT/'workflow_regression.py');scratch=ROOT/'_local';scratch.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='additional-offline-',dir=scratch) as tmp:
  base=Path(tmp);post=postmerge_cases(w,w.fixture(base/'postmerge'));strict=strict_actual_kit_cases(w,w.fixture(base/'strict'))
 # Actual current submitted bindings, not fabricated mathematical clearance.
 v=load(ROOT/'verification_verify.py' if (ROOT/'verification_verify.py').exists() else ROOT/'verification/verify.py');audit=ROOT.parents[1] if (ROOT/'verification_verify.py').exists() else ROOT.parent;snapshot=json.loads((audit/'SUBMITTED_SNAPSHOT.json').read_text());v.authenticate_snapshot(audit/'submitted',snapshot)
 need(not (ROOT/'zenodo-deposit.json').exists(),'This proposal expects no actual supplied metadata; rerun actual-data regressions after deployment')
 return {'postmerge':post,'strict_actual_kit':strict,'actual_original_eight_Git_blobs_and_seven_nonself_manifest_entries_authenticated':True,'scope':'Offline synthetic release/compiler/reviews/service fixtures only; actual originals authenticated read-only; no real acceptance, publication or Git mutation.'}
def main():
 if '--worker' in sys.argv:print(json.dumps(worker(),sort_keys=True));return
 runs=[]
 for flags in [[],['-O'],['-OO']]:
  r=subprocess.run([sys.executable,'-B',*flags,str(Path(__file__).resolve()),'--worker'],capture_output=True,text=True);need(r.returncode==0,r.stderr);runs.append({'flags':flags,'result':json.loads(r.stdout)})
 need(all(x['result']==runs[0]['result'] for x in runs),'Optimization-dependent additional checks')
 result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','all_modes_identical':True,'runs':runs,'program_sha256':sha(Path(__file__))};save(ROOT/'_local/ADDITIONAL_FAULT_RECEIPT.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
