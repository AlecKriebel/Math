from pathlib import Path
import argparse,contextlib,copy,datetime,hashlib,importlib.util,io,json,os,runpy,shutil,subprocess,tempfile,types,unittest.mock,sys
H=Path(__file__).resolve().parent;A=H.parent.parent;P=A/'publication';PROGRAM=A.parents[1];scratch=H/'_local';tempfile.tempdir=str(scratch)
def need(c,m):
 if not c:raise RuntimeError(m)
def load(p):
 s=importlib.util.spec_from_file_location('fresh_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
result={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Actual frozen source, actual current metadata and exact local artifact bytes; isolated synthetic service responses and receipts. No real service/Git operation. Gate authentication is an explicitly trusted stub only for the isolated ready-and-merge negative probes, because no actual final gate yet exists.'}
# Merge-runner probe: a valid earlier review gate covers the package/code but not
# generated branch/body receipts. Hold that gate constant and alter only receipts.
source=A/'_local/ready_and_merge.py';code=source.read_text();names=sorted(json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text())['files'],key=lambda e:e['path']);paths=[e['path'] for e in names]+['attempts/30003587/publication_20261017/'+n for n in ['Diagonal_Actions_Strong_Approximate_Innerness_Note_v1.0.pdf','Diagonal_Actions_Strong_Approximate_Innerness_Verification_v1.0.zip','zenodo-deposit.json','PUBLICATION_RECEIPT.json','README.md']]
ready=[]
for case in ['baseline_minimal_receipt','unreviewed_head','unverified_receipt_flags','missing_publication_tracker_and_public_receipts','unreviewed_14_path_contents','unreviewed_commit_parent','retargeted_pr_base']:
 with tempfile.TemporaryDirectory(prefix='ready-negative-',dir=scratch) as tmp:
  a=Path(tmp)/'audit';p=a/'publication';p.mkdir(parents=True);fakefile=a/'_local/ready_and_merge.py';fakefile.parent.mkdir();head=('b' if case=='unreviewed_head' else 'a')*40;body='GENERATED BODY OUTSIDE FROZEN PACKAGE';gate={'earlier_review_gate_valid':True};save(p/'FINAL_REVIEW_GATE.json',gate);save(p/'PR_BRANCH_RECEIPT.json',{'commit':head,'branch':'publish-diagonal-30003587-20261011','paths':paths,'body_readback_verified':False,'remote_readback_verified':False});(p/'PR_BODY_FINAL.md').write_text(body);events=[];draft={'value':True};guardcalls=[]
  live={'url':'https://github.com/AlecKriebel/Math/pull/1280','state':'OPEN','headRefOid':head,'headRefName':'publish-diagonal-30003587-20261011','body':body,'files':[{'path':n} for n in paths],'baseRefName':'other' if case=='retargeted_pr_base' else 'main'}
  def checkout(args,**kwargs):
   events.append({'read':args})
   if args[:3]==['git','branch','--show-current']:return 'main\n'
   if args[0]=='gh':return json.dumps({**live,'isDraft':draft['value']})
   if args[:2]==['git','ls-remote']:return head+' refs/heads/'+live['headRefName']+'\n'
   raise RuntimeError('Unexpected read operation')
  def mutation(args,**kwargs):
   events.append({'mutation':args})
   if args[:3]==['gh','pr','ready']:draft['value']=False
   return types.SimpleNamespace(returncode=0,stdout='MOCK ONLY',stderr='')
  def gatecheck(g):need(g==gate,'gatechanged');guardcalls.append('valid earlier frozen package gate')
  realrunpy=runpy.run_path
  def module(path,*args,**kwargs):
   if Path(path).name=='update_pr_publication.py':return {'validate_workflow_gate':gatecheck}
   raise RuntimeError('Unexpected module')
  with unittest.mock.patch.object(subprocess,'check_output',checkout),unittest.mock.patch.object(subprocess,'run',mutation),unittest.mock.patch.object(runpy,'run_path',module),contextlib.redirect_stdout(io.StringIO()):
   exec(compile(code,str(source),'exec'),{'__file__':str(fakefile),'__name__':'__main__'})
  merges=[e for e in events if e.get('mutation',[])[:3]==['gh','pr','merge']];need(len(merges)==1,'probe failed to reach merge');ready.append({'case':case,'unexpected_merge_requested':True,'head':head,'all14_paths_matched':True,'baseRefName':live['baseRefName'],'blob_or_parent_reads':sum(e.get('read',[])[1:2] in [['show'],['rev-list']] for e in events),'gate_calls':guardcalls,'events':events})
result['ready_merge_guard_gap']=ready
# Shared identity predicate on exact current source.
t=load(P/'append_tracker.py');pub={'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123'};identities=[]
for text in ['PR1280','PR 1280','#1280','https://github.com/AlecKriebel/Math/pull/1280','Published DOI: 10.5281/zenodo.123','Published at https://doi.org/10.5281/zenodo.123 (v1.0)','10.5281/zenodo.123','OWR-15585-006']:
 for cell in range(4):
  row=['','','',''];row[cell]=text;identities.append({'text':text,'cell':cell,'recognized':bool(t.row_has_problem_identity(row,pub))})
result['additional_identity_matrix']=identities
# Coordinator+actual shared kit with actual metadata/artifacts on isolated copy.
results=[];actualmeta=json.loads((P/'zenodo-deposit.json').read_text())['metadata'];need(len(actualmeta)==11,'actual11metadata')
for case in ['success','unknown_create_outcome','known_id_upload_outcome','wrong_id_first','wrong_id_second','lost_publish']+['field_'+k for k in sorted(actualmeta)]:
 with tempfile.TemporaryDirectory(prefix='actual-metadata-',dir=scratch) as tmp:
  p=Path(tmp)/'publication';p.mkdir();shutil.copyfile(P/'zenodo-deposit.json',p/'zenodo-deposit.json');shutil.copyfile(P/'append_tracker.py',p/'append_tracker.py')
  for name in ['Diagonal_Actions_Strong_Approximate_Innerness_Note_v1.0.pdf','Diagonal_Actions_Strong_Approximate_Innerness_Verification_v1.0.zip']:shutil.copyfile(P/name,p/name)
  c=load(PROGRAM/'publication_coordinators/pr1280.py');c.P=p;c.A=p.parent;kit=c.load_exact_kit();kit.STATE_DIR=p/'state';kit.doi_status=lambda doi:{'status':'resolved','http_status':200};events=[];state={'deposit':None,'get_count':0,'second_mutation':None,'lost_followup':False}
  class Client:
   def create(self,metadata):
    events.append('POST create')
    if case=='unknown_create_outcome':raise kit.DepositError('mock unknown creation outcome')
    state['deposit']={'id':123,'submitted':False,'metadata':copy.deepcopy(metadata),'files':[],'links':{'bucket':'fixture://bucket'}};return copy.deepcopy(state['deposit'])
   def upload(self,bucket,e):
    events.append('PUT file');state['deposit']['files'].append({'filename':e['name'],'filesize':e['size'],'checksum':'md5:'+e['md5']})
    if case=='known_id_upload_outcome' and len(state['deposit']['files'])==2:raise kit.DepositError('mock lost final upload response')
   def update(self,identifier,metadata):events.append('PUT metadata');state['deposit']['metadata']=copy.deepcopy(metadata)
   def get(self,identifier):
    events.append('GET '+str(identifier));need(identifier==123,'sameid requested');state['get_count']+=1
    if state['lost_followup']:state['lost_followup']=False;raise kit.DepositError('mock lost publication readback')
    d=copy.deepcopy(state['deposit'])
    if state['second_mutation'] is not None:
     key=state['second_mutation'];state['second_mutation']=None
     if key=='id':d['id']=124
     else:d['metadata'][key]=None
    return d
   def publish(self,identifier):
    events.append('POST publish');state['deposit']['submitted']=True;state['deposit']['doi']='10.5281/zenodo.123'
    if case=='lost_publish':state['lost_followup']=True;raise kit.DepositError('mock lost publish response')
  client=Client();gate={'metadata_sha256':sha(p/'zenodo-deposit.json'),'pdf_sha256':sha(p/'Diagonal_Actions_Strong_Approximate_Innerness_Note_v1.0.pdf'),'verification_zip_sha256':sha(p/'Diagonal_Actions_Strong_Approximate_Innerness_Verification_v1.0.zip')};c.authenticate_release=lambda:copy.deepcopy(gate);c.live_preflight=lambda:None
  def call(loaded,command,known_id=None,check_doi=False):
   if command=='publish' and (case.startswith('field_') or case=='wrong_id_second'):state['second_mutation']=case.removeprefix('field_') if case.startswith('field_') else 'id'
   return kit.run(argparse.Namespace(command=command,manifest=p/'zenodo-deposit.json',sandbox=False,confirm_id=known_id,check_doi=check_doi),client=client)
  c.call_kit=call
  def rejects(fn):
   try:fn()
   except (RuntimeError,ValueError,kit.DepositError):return True
   raise RuntimeError('negative unexpectedly accepted '+case)
  if case=='unknown_create_outcome':
   rejects(lambda:c.execute('stage',kit));rejects(lambda:c.execute('stage',kit));need(events.count('POST create')==1,'no repeated create')
  elif case=='known_id_upload_outcome':
   rejects(lambda:c.execute('stage',kit));rejects(lambda:c.execute('stage',kit));n=len(events);d=c.execute('inspect',kit);need(events[n:]==['GET 123'] and d['id']==123,'readonly knownid recovery')
  else:
   c.execute('stage',kit);rejects(lambda:c.execute('stage',kit))
   if case=='wrong_id_first':state['second_mutation']='id'
   if case.startswith('field_') or case in ['wrong_id_first','wrong_id_second']:
    rejects(lambda:c.execute('publish',kit));need('POST publish' not in events,'badmetadata reached publish')
   elif case=='lost_publish':
    rejects(lambda:c.execute('publish',kit));d=c.execute('publish',kit);c.execute('publish',kit);need(d['state']=='published' and events.count('POST publish')==1,'lostpublish no duplicate')
   else:
    d=c.execute('publish',kit);c.execute('publish',kit);need(d['state']=='published' and events.count('POST publish')==1,'success no duplicate')
  results.append({'case':case,'events':events,'all_external_operations_mocked':True,'actual_metadata_sha256':sha(P/'zenodo-deposit.json'),'actual_pdf_sha256':gate['pdf_sha256'],'actual_archive_sha256':gate['verification_zip_sha256']})
result['actual_metadata_artifacts_coordinator_probes']=results;result['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save(H/('EXTRA_WORKFLOW_CHECKS'+('' if sys.flags.optimize==0 else '_'+str(sys.flags.optimize))+'.json'),result);print(json.dumps({'completed_utc':result['completed_utc'],'merge_gap_cases':len(ready),'identity_matrix_cases':len(identities),'actual_metadata_coordinator_cases':len(results)}))
