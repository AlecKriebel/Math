from pathlib import Path
import contextlib,copy,datetime,hashlib,importlib.util,io,json,shutil,types,zipfile
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'publication';REPO=A.parents[2];L=R/'_local'
def load(p):
 s=importlib.util.spec_from_file_location('probe_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def need(x,msg):
 if not x:raise RuntimeError(msg)
def reject(f,label,errors=(RuntimeError,ValueError,KeyError)):
 try:f()
 except errors:return label
 raise RuntimeError('invalid accepted '+label)
def save(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2)+'\n')
def quiet(f):
 with contextlib.redirect_stdout(io.StringIO()):return f()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
C=json.loads((A/'CURRENT_PR1262_CONTEXT.json').read_text());B=json.loads((P/'BUILD_RECEIPT.json').read_text());S=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text())
coordinator=REPO/'draft_pr_actual_outcomes_1200_1300_20261017/publication_coordinators/pr1262.py';mergeprog=coordinator.with_name('verify_pr1262_merge.py')
# Actual metadata/artifact bytes, actual coordinator and shared kit, wholly mocked clients.
coordinator_cases=[]
for field in list(C['metadata'])+['exact_success','wrong_fresh_id','uncertain_recovery']:
 d=L/('coordinator-'+field)
 if d.exists():shutil.rmtree(d)
 d.mkdir();shutil.copyfile(P/'zenodo-deposit.json',d/'zenodo-deposit.json');shutil.copyfile(P/'append_tracker.py',d/'append_tracker.py')
 for key in ['pdf','verification_zip']:shutil.copyfile(P/B[key]['path'],d/B[key]['path'])
 c=load(coordinator);c.P=d;gate={'synthetic_runtime_only':True,'metadata_sha256':sha(d/'zenodo-deposit.json'),'pdf_sha256':B['pdf']['sha256'],'verification_zip_sha256':B['verification_zip']['sha256']};c.authenticate_release=lambda:gate;c.live_preflight=lambda:None;k=c.load_exact_kit();k.STATE_DIR=d/'state';k.doi_status=lambda doi:{'status':'resolved','http_status':200,'url':'https://doi.org/'+doi}
 events=[];state={'deposit':None,'alter':None,'lost':False,'lost_get':False}
 class Client:
  def create(self,metadata):
   events.append('POST create');state['deposit']={'id':123,'submitted':False,'metadata':copy.deepcopy(metadata),'files':[],'links':{'bucket':'mock://bucket'}};return copy.deepcopy(state['deposit'])
  def upload(self,bucket,entry):events.append('PUT file');state['deposit']['files'].append({'filename':entry['name'],'filesize':entry['size'],'checksum':'md5:'+entry['md5']})
  def update(self,number,metadata):events.append('PUT metadata');state['deposit']['metadata']=copy.deepcopy(metadata)
  def get(self,number):
   events.append('GET '+str(number));need(number==123,'wrong requested id')
   if state['lost_get']:state['lost_get']=False;raise k.DepositError('mock lost followup')
   out=copy.deepcopy(state['deposit'])
   if state['alter']:
    key=state['alter'];state['alter']=None
    if key=='wrong_fresh_id':out['id']=124
    else:out['metadata'][key]=None
   return out
  def publish(self,number):
   events.append('POST publish');state['deposit'].update(submitted=True,doi='10.5281/zenodo.123')
   if state['lost']:state['lost']=False;state['lost_get']=True;raise k.DepositError('mock lost publish')
 client=Client()
 def call(kit,command,known_id=None,check_doi=False):
  if command=='publish' and field in C['metadata']:state['alter']=field
  return k.run(types.SimpleNamespace(command=command,manifest=d/'zenodo-deposit.json',sandbox=False,confirm_id=known_id,check_doi=check_doi),client=client)
 c.call_kit=call;c.execute('stage',k)
 reject(lambda:c.execute('stage',k),'duplicate stage')
 if field in C['metadata']:
  reject(lambda:c.execute('publish',k),'actual-field-before-kit-POST:'+field,(RuntimeError,ValueError,k.DepositError));need(events.count('POST publish')==0,'metadata drift published')
  reject(lambda:c.execute('publish',k),'unresolved publish intent',(RuntimeError,ValueError,k.DepositError));need(events.count('POST publish')==0,'intent permitted retry')
 elif field=='wrong_fresh_id':
  state['alter']=field;reject(lambda:c.execute('publish',k),'fresh wrong id',(RuntimeError,ValueError,k.DepositError));need(events.count('POST publish')==0,'wrong id published')
 else:
  if field=='uncertain_recovery':
   state['lost']=True;reject(lambda:c.execute('publish',k),'lost POST and followup',(RuntimeError,ValueError,k.DepositError))
  result=c.execute('publish',k);need(result['id']==123 and result['state']=='published','same id result');c.execute('publish',k);need(events.count('POST publish')==1,'repeated POST')
 coordinator_cases.append({'case':field,'events':events,'publish_POSTs':events.count('POST publish')})
# Explicit exclusive open control: existing intent is never overwritten.
intent=L/'exclusive-intent.json'
if intent.exists():intent.unlink()
c.write_intent(intent,{'synthetic':1});reject(lambda:c.write_intent(intent,{'synthetic':2}),'exclusive intent');need(json.loads(intent.read_text())=={'synthetic':1},'intent overwritten')
# All actual supplied public fields, exact schema projection, blank B and all4 cells.
t=load(P/'append_tracker.py');pub={'environment':'production','state':'published','metadata_normalizations':[],'id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','url':'https://doi.org/10.5281/zenodo.123','title':C['title'],'doi_resolution':{'status':'resolved','http_status':200},'files':[{'name':B[k]['path'],'size':B[k]['bytes'],'sha256':B[k]['sha256']} for k in ['pdf','verification_zip']]}
row=t.expected_row(pub,C['title']);need(len(row)==4 and row[1]=='','blank B');tracker={'spreadsheetId':t.SID,'gid':t.GID,'readback_verified':True,'updatedRange':"'Math Puzzles'!A2:D2",'row':row};t.validate_tracker_receipt(tracker,pub,C['title']);rowneg=[]
for i in range(4):
 bad=copy.deepcopy(tracker);bad['row'][i]='wrong';rowneg.append(reject(lambda:t.validate_tracker_receipt(bad,pub,C['title']),'full-cell-'+str(i)))
md=load(P/'check_public_downloads.py');publicmeta=copy.deepcopy(C['metadata']);publicmeta['resource_type']={'type':publicmeta.pop('upload_type'),'subtype':publicmeta.pop('publication_type')};publicmeta['license']={'id':publicmeta['license']};md.verify_public_metadata(publicmeta,C['metadata']);metaneg=[]
for key in C['metadata']:
 bad=copy.deepcopy(publicmeta)
 if key=='upload_type':bad['resource_type']['type']=None
 elif key=='publication_type':bad['resource_type']['subtype']=None
 elif key=='license':bad['license']['id']=None
 else:bad[key]=None
 metaneg.append(reject(lambda:md.verify_public_metadata(bad,C['metadata']),key))
# Actual thirteen output bytes and actual post-merge verification logic, mocked Git/services only.
program=L/'postmerge-program';a=program/'audits/pr1262_30001248';p=a/'publication';p.mkdir(parents=True,exist_ok=True);(program/'RESEARCH_LOG.md').write_text('SYNTHETIC TEST LOG\n');(a/'RESEARCH_LOG.md').write_text('SYNTHETIC TEST LOG\n')
for name in ['zenodo-deposit.json',B['pdf']['path'],B['verification_zip']['path']]:shutil.copyfile(P/name,p/name)
shutil.copyfile(A/'SUBMITTED_SNAPSHOT.json',a/'SUBMITTED_SNAPSHOT.json');shutil.copytree(A/'current_edition',a/'current_edition',dirs_exist_ok=True)
save(p/'FINAL_REVIEW_GATE.json',{'synthetic_fixture_only':True,'reviews':[{'reviewer_id':'SYNTHETIC_ONLY','status':'SYNTHETIC_ONLY'}],'latest_review':{'status':'SYNTHETIC_ONLY'}});save(p/'PUBLICATION_RECEIPT.json',pub);save(p/'tracker/TRACKER_RECEIPT.json',tracker)
public={'all_supplied_metadata_exact':True,'public_record_identity_verified':True,'metadata_manifest_sha256':sha(p/'zenodo-deposit.json'),'doi':pub['doi'],'id':123,'doi_url':pub['doi_url'],'record_url':pub['record_url'],'metadata_fields_verified':sorted(C['metadata']),'files':[{'name':B[k]['path'],'bytes':B[k]['bytes'],'sha256':B[k]['sha256']} for k in ['pdf','verification_zip']]};save(p/'PUBLIC_DOWNLOAD_VERIFICATION.json',public)
u=load(P/'update_pr_publication.py');u.ROOT=p;u.current_context=lambda:C;u.validate_workflow_gate=lambda g:None
files,additions,note=u.desired_files(B,pub,tracker,S);need(len(files)==13 and len(additions)==5,'actual13 scope');body=note+'\nThe eight-file MANIFEST.json binds the seven other current mathematical edition records through entries/file/bytes/sha256. publication_20261017/ adds the reviewed preprint, portable verification archive, matching deposit metadata, publication receipt and README. Original historical files are preserved in the portable archive.\n';(p/'PR_BODY_FINAL.md').write_text(body)
head='a'*40;merge='b'*40;parent='c'*40;wanted=u.expected_identity(pub,tracker,files,body);receipt={**wanted,'commit':head,'body_readback_verified':True,'remote_readback_verified':True}
save(p/'PR_BRANCH_RECEIPT.json',receipt);save(p/'BUILD_RECEIPT.json',B);save(a/'SUBMITTED_SNAPSHOT.json',S)
fault={'kind':None};calls=[]
def git(*args,data=None):
 calls.append(args)
 if args==('branch','--show-current'):return b'main\n'
 if args[0]=='rev-list':
  if args[-1]==head:return (head+' '+u.ORIGINAL+'\n').encode()
  return (merge+' '+parent+' '+('d'*40 if fault['kind']=='merge-parent' else head)+'\n').encode()
 if args[0]=='diff-tree':return ('\n'.join(sorted(files)+(['outside/file'] if fault['kind']=='paths' else []))+'\n').encode()
 if args[0]=='show':
  name=args[1].split(':',1)[1];return b'wrong' if fault['kind']=='blob:'+name else files[name]
 if args[0] in {'fetch','update-ref'}:return b''
 raise RuntimeError('unmocked git '+repr(args))
u.git=git
post=load(mergeprog);post.P=p;post.A=a;post.PROGRAM=program;post.REPO=REPO
# Keep actual tracker validators, inject only authenticated context and read-only fake rows.
t.runpy=types.SimpleNamespace(run_path=lambda path:{'load_context':lambda:C})
def rows(*args,**kwargs):
 rr=[['Original Problem','Solution Chat URL','DOI','Notes'],copy.deepcopy(row)]
 if fault['kind']=='duplicate-row':rr.append(copy.deepcopy(row))
 if fault['kind']=='row-notes':rr[1][3]='wrong'
 return {'values':rr}
t.call=rows
post.runpy=types.SimpleNamespace(run_path=lambda path:vars(u) if Path(path).name=='update_pr_publication.py' else vars(t))
def live(*args,**kwargs):
 return json.dumps({'state':'MERGED','headRefOid':'e'*40 if fault['kind']=='head' else head,'headRefName':u.BRANCH,'mergeCommit':{'oid':merge},'mergedAt':'2026-10-17T00:00:00Z','body':'wrong' if fault['kind']=='body' else body,'url':'https://fixture.invalid'} )
post.subprocess=types.SimpleNamespace(check_output=live)
readload=post.load
saved=[]
def input_load(path):
 if path==program/'PROGRAM_STATE.json':return {'current_pr':1262,'completed_prs':[],'publications':[],'eligible_count':3}
 if path==p/'PUBLICATION_RECEIPT.json':
  result=copy.deepcopy(pub)
  if fault['kind'] in {'doi404','doi-fallback200'}:result['doi_resolution']={'status':'not_resolved','http_status':404}
  return result
 if path==p/'DOI_INSPECT.json':
  result=copy.deepcopy(pub);result['doi_resolution']={'status':'resolved','http_status':200} if fault['kind']=='doi-fallback200' else {'status':'not_resolved','http_status':404};return result
 return readload(path)
post.load=input_load;post.save=lambda path,obj:saved.append((str(path),obj))
quiet(post.main);need(any(x[0].endswith('FINAL_DISPOSITION.json') for x in saved),'positive postmerge did not complete');need(any(x[1].get('all13_merged_files_exact') for x in saved),'postmerge exact13 missing')
negative=[]
for kind in ['head','body','merge-parent','paths','duplicate-row','row-notes','doi404']+['blob:'+n for n in files]:
 fault['kind']=kind;saved.clear();negative.append(reject(lambda:quiet(post.main),'postmerge:'+kind));need(not any(x[0].endswith('FINAL_DISPOSITION.json') for x in saved),'failed probe completed')
fault['kind']='doi-fallback200';saved.clear();quiet(post.main);need(any(x[0].endswith('FINAL_DISPOSITION.json') for x in saved),'DOI200 fallback rejected')
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_metadata_sha256':sha(P/'zenodo-deposit.json'),'actual_metadata_keys':sorted(C['metadata']),'coordinator_actual_metadata_cases':coordinator_cases,'exclusive_intent_preserved':True,'public_each_field_corruption_rejected':metaneg,'blank_B':True,'full_four_cells_rejected':rowneg,'exact_actual13_output_paths':sorted(files),'postmerge_checks':{'actual_program':str(mergeprog),'complete_main_mocked_positive':True,'DOI200_fallback_positive':True,'negative_controls':negative,'Git_service_calls_mocked':True},'limits':'Runtime release authentication bypassed only inside own scratch fixtures to reach downstream code. The deployed workflow worker separately tests actual review-gate validation with synthetic evidence. No actual final gate, live DOI, release, tracker entry, PR change or merge exists by virtue of these probes.'}
(R/'WORKFLOW_PROBES.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','actual11_prePOST_corruptions':11,'postmerge_negative_controls':len(negative),'actual13_paths':len(files)}))
