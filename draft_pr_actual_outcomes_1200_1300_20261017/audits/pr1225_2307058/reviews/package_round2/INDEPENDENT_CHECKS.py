#!/usr/bin/env python3
"""Second review's independent offline contract checks. No remote operations."""
from pathlib import Path
import contextlib,copy,datetime,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,types,zipfile
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
COPY=HERE/'scratch/audit'
PUB=COPY/'publication'
REAL_RUN=subprocess.run
checks=[]
def load(path):
 s=importlib.util.spec_from_file_location('r2_'+hashlib.sha256(str(path).encode()).hexdigest()[:12],path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):Path(p).write_text(json.dumps(d,indent=2)+'\n')
def need(c,m):
 if not c:raise RuntimeError(m)
def ok(n,**d):checks.append({'check':n,'status':'PASS',**d})
def reject(n,fn,types_=(RuntimeError,ValueError,FileNotFoundError)):
 try:fn()
 except types_ as e:ok(n,rejection=str(e)[:240]);return
 raise RuntimeError('Unexpected acceptance: '+n)
def quiet(fn):
 with contextlib.redirect_stdout(io.StringIO()):return fn()
def get(p):return json.loads(Path(p).read_text())
# Actual package regeneration was run on COPY by the reviewer before this script.
need(sha(PUB/'Real_Complement_Modulus_Verification_v1.0.zip')==sha(AUDIT/'publication/Real_Complement_Modulus_Verification_v1.0.zip'),'ZIP rebuild differs')
for p in (AUDIT/'current_edition').iterdir():
 if p.is_file():need(p.read_bytes()==(COPY/'current_edition'/p.name).read_bytes(),'Current-edition regeneration differs '+p.name)
with zipfile.ZipFile(PUB/'Real_Complement_Modulus_Verification_v1.0.zip') as z:
 need(len(z.namelist())==118 and len(set(z.namelist()))==118,'ZIP inventory');z.extractall(HERE/'scratch/extracted')
v=load(HERE/'scratch/extracted/verify.py');quiet(v.main)
ok('exact_118_member_zip_rebuild_and_extracted_verifier',nested_freezes=10,current_edition_files=8)
# Each actual nested freeze is challenged while resealing the outer manifest.
ex=HERE/'scratch/extracted';nested=v.authenticate_nested_manifests(ex)
for n in nested:
 manifest=ex/n['path'];data=get(manifest);entry=data.get('entries',data.get('files'))[0];rel=entry.get('file',entry.get('path'));target=ex/n['base']/rel;old=target.read_bytes();rootman=ex/'MANIFEST.json';rootold=rootman.read_bytes();target.write_bytes(old+b'\nchanged by second review\n');outer=get(rootman)
 for e in outer['files']:
  if e['path']==target.relative_to(ex).as_posix():e.update(bytes=target.stat().st_size,sha256=sha(target))
 save(rootman,outer);reject('nested_freeze_'+n['path'],lambda:quiet(v.main));target.write_bytes(old);rootman.write_bytes(rootold)
# Build guard checks operate on COPY and preserve its last valid release files.
b=load(PUB/'build_package.py');b.document_bindings()
for name in ['COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json']:
 p=PUB/name;old=p.read_bytes();d=get(p)
 for key in (['returncode','source_sha256','pdf_sha256'] if name.startswith('COMPILE') else ['status','source_sha256','pdf_sha256','pages','all_pages_visually_inspected','page_indices_inspected']):
  x=copy.deepcopy(d);x[key]=False if key=='all_pages_visually_inspected' else [] if key=='page_indices_inspected' else 9 if key in ['pages','returncode'] else 'changed';save(p,x);reject('build_'+name+'_'+key,b.document_bindings)
 p.write_bytes(old)
release_names=['Real_Complement_Modulus_Verification_v1.0.zip','Real_Complement_Modulus_Note_v1.0.pdf'];before={n:sha(PUB/n) for n in release_names}
orig_zip=b.zipfile.ZipFile
class CorruptZip(orig_zip):
 def writestr(self,zinfo,data,*a,**kw):
  if self.mode=='w' and getattr(zinfo,'filename',zinfo)=='current_edition/AUDIT.md':data=data+b'corrupt'
  return super().writestr(zinfo,data,*a,**kw)
b.zipfile=types.SimpleNamespace(ZipFile=CorruptZip,ZIP_DEFLATED=zipfile.ZIP_DEFLATED,ZipInfo=zipfile.ZipInfo)
reject('written_temporary_zip_corruption_before_release_replace',lambda:quiet(b.main));need(before=={n:sha(PUB/n) for n in release_names},'Release changed on ZIP guard failure')
b.zipfile=zipfile
orig_copy=b.shutil.copyfile;lp=PUB/'LAYOUT_VERIFICATION.json';old=lp.read_bytes()
def change_layout(src,dst,*a,**kw):
 ans=orig_copy(src,dst,*a,**kw)
 if Path(src)==PUB/'output/pdf/main.pdf':d=get(lp);d['status']='changed-during-build';save(lp,d)
 return ans
b.shutil=types.SimpleNamespace(copyfile=change_layout)
reject('document_state_drift_after_temporary_write',lambda:quiet(b.main));lp.write_bytes(old);need(before=={n:sha(PUB/n) for n in release_names},'Release changed on drift guard')
# Execute compile helper with a local only-cached adapter and original PDF epoch.
c=load(PUB/'compile_note.py')
def cached_run(args,**kwargs):
 if args[0].endswith('tectonic') and '--version' not in args:
  args=[args[0],'--only-cached',*args[1:]];kwargs['env']={**kwargs.get('env',os.environ),'SOURCE_DATE_EPOCH':'1792267163'}
 return REAL_RUN(args,**kwargs)
c.subprocess=types.SimpleNamespace(run=cached_run,check_output=subprocess.check_output)
quiet(c.main);need(sha(PUB/'output/pdf/main.pdf')==sha(AUDIT/'publication/Real_Complement_Modulus_Note_v1.0.pdf'),'Original-epoch compile differs')
copy_compile=get(PUB/'COMPILE_RECEIPT.json');save(HERE/'COMPILE_REPLAY.json',{'status':'PASS','offline_only_cached':True,'source_date_epoch':1792267163,'compile_receipt':copy_compile,'pdf_byte_exact':True,'scope':'Actual compile_note.main with only-cached/SOURCE_DATE_EPOCH adapter; no claim that new wall-clock compilation reproduces original PDF bytes.'})
ok('actual_compile_main_original_epoch_byte_exact',pages=7)
# Restore baseline receipt for remaining exact-release workflows.
shutil.copyfile(AUDIT/'publication/COMPILE_RECEIPT.json',PUB/'COMPILE_RECEIPT.json')
# Public verification complete main: all 11 supplied fields, wrong metadata and bytes.
p=load(PUB/'check_public_downloads.py');t=load(PUB/'append_tracker.py');metadata=get(PUB/'zenodo-deposit.json')['metadata'];build=get(PUB/'BUILD_RECEIPT.json')
need(len(metadata)==11,'Expected exactly11 supplied metadata fields')
pub={'environment':'production','state':'published','metadata_normalizations':[],'id':987654321,'doi':'10.5281/zenodo.987654321','doi_url':'https://doi.org/10.5281/zenodo.987654321','record_url':'https://zenodo.org/records/987654321','url':'https://doi.org/10.5281/zenodo.987654321','title':metadata['title'],'files':[{'name':build[k]['path'],'size':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]}
save(PUB/'PUBLICATION_RECEIPT.json',pub)
publicmeta=copy.deepcopy(metadata);publicmeta['resource_type']={'type':publicmeta.pop('upload_type'),'subtype':publicmeta.pop('publication_type')};publicmeta['license']={'id':publicmeta['license']};publicmeta['doi']=pub['doi']
record={'id':pub['id'],'doi':pub['doi'],'metadata':publicmeta,'files':[{'key':build[k]['path'],'links':{'self':'https://zenodo.org/records/987654321/files/'+build[k]['path']}} for k in ['pdf','verification_zip']]}
remote={'record':record,'corrupt':False};fetches=[]
def fetch(url,limit):
 fetches.append(url)
 if '/api/records/' in url:return json.dumps(remote['record']).encode()
 ans=(PUB/url.rsplit('/',1)[1]).read_bytes();return ans+b'corrupt' if remote['corrupt'] else ans
p.fetch=fetch;quiet(p.main);need(get(PUB/'PUBLIC_DOWNLOAD_VERIFICATION.json')['metadata_fields_verified']==sorted(metadata),'Public fields incomplete');ok('public_main_exact_11_fields_and_both_downloads',fields=sorted(metadata))
for k in metadata:
 bad=copy.deepcopy(record)
 if k=='upload_type':bad['metadata']['resource_type']['type']='wrong'
 elif k=='publication_type':bad['metadata']['resource_type']['subtype']='wrong'
 elif k=='license':bad['metadata']['license']['id']='wrong'
 else:bad['metadata'][k]=None
 remote['record']=bad;reject('public_main_metadata_'+k,lambda:quiet(p.main))
remote['record']=record;remote['corrupt']=True;reject('public_main_corrupt_download',lambda:quiet(p.main));remote['corrupt']=False
for k,val in [('id',True),('doi_url','https://example.com'),('record_url','https://zenodo.org/records/1'),('doi','10.5281/zenodo.1'),('metadata_normalizations',[{'field':'description'}])]:
 bad=copy.deepcopy(pub);bad[k]=val;reject('canonical_identity_'+k,lambda bad=bad:t.validate_publication_identity(bad,metadata['title']))
# Complete tracker main: append, exact idempotence, accepted append/lost response.
headers=['Original Problem','Solution Chat URL','DOI','Notes'];row=t.expected_row(pub,metadata['title']);need(row[1]=='','Tracker B must stay blank')
tracker_state={'rows':[headers],'appends':0,'lost':False}
def tracker_call(parts,params,body=None):
 if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':t.GID,'title':'Math Puzzles'}}]}
 if parts==['spreadsheets','values','append']:
  need((PUB/'tracker/INTENT.json').exists(),'Append intent was not persisted first');tracker_state['appends']+=1;tracker_state['rows'].append(copy.deepcopy(body['values'][0]))
  if tracker_state['lost']:raise RuntimeError('Simulated accepted append with lost response')
  return {'updates':{'updatedRange':"'Math Puzzles'!A2:D2",'updatedRows':1,'updatedColumns':4}}
 if parts==['spreadsheets','values','get']:
  return {'values':copy.deepcopy(tracker_state['rows'] if params['range'].endswith('A:D') else [tracker_state['rows'][1]])}
 raise RuntimeError('Unexpected tracker operation')
t.call=tracker_call;quiet(t.main);quiet(t.main);need(tracker_state['appends']==1,'Idempotent tracker appended twice');ok('tracker_full_main_append_then_idempotent_exact_row')
shutil.rmtree(PUB/'tracker');tracker_state.update(rows=[headers],appends=0,lost=True);reject('tracker_accepted_append_lost_response',lambda:quiet(t.main));tracker_state['lost']=False;quiet(t.main);need(tracker_state['appends']==1,'Tracker lost response recovery repeated append');ok('tracker_lost_response_recovered_without_second_append')
for cell in range(4):
 old=tracker_state['rows'][1][cell];tracker_state['rows'][1][cell]='changed';reject('tracker_existing_wrong_cell_'+str(cell),lambda:quiet(t.main));tracker_state['rows'][1][cell]=old
tracker_state['rows'].append(copy.deepcopy(row));reject('tracker_duplicate_problem_row',lambda:quiet(t.main));tracker_state['rows'].pop()
tracker=get(PUB/'tracker/TRACKER_RECEIPT.json')
for rg in ["'Other'!A2:D2","'Math Puzzles'!A1:D1","'Math Puzzles'!A2:D3","'Math Puzzles'!A2:C2"]:
 x={**tracker,'updatedRange':rg};reject('tracker_range_'+rg,lambda x=x:t.validate_tracker_receipt(x,pub,metadata['title']))
# Genuine local Git objects on a review-only clone; all remote calls intercepted.
repo=HERE/'scratch/git-copy'
if not (repo/'.git').exists():
 r=REAL_RUN(['git','clone','--shared','--no-checkout','--quiet','/Users/alec/Documents/Math',str(repo)],capture_output=True,text=True);need(r.returncode==0,r.stderr)
u=load(PUB/'update_pr_publication.py');u.REPO=repo
review=COPY/'reviews/fixture';review.mkdir(parents=True,exist_ok=True);(review/'REPORT.md').write_text('Offline fixture, not a mathematical review');save(review/'VERDICT.json',{'status':'CLEAN'})
gate={'schema':'math-preprint-final-review-gate-v1','pr':1225,'problem_id':2307058,'original_head':u.ORIGINAL,'status':'pass','pdf_sha256':build['pdf']['sha256'],'verification_zip_sha256':build['verification_zip']['sha256'],'metadata_sha256':sha(PUB/'zenodo-deposit.json'),'workflow':{n:sha(PUB/n) for n in u.REQUIRED_WORKFLOW},'latest_review':{'status':'CLEAN','report':'../reviews/fixture/REPORT.md','report_sha256':sha(review/'REPORT.md'),'verdict':'../reviews/fixture/VERDICT.json','verdict_sha256':sha(review/'VERDICT.json')}}
save(PUB/'FINAL_REVIEW_GATE.json',gate)
origgit=u.git;state={'head':u.ORIGINAL,'body':'','lostbody':False,'pushes':0,'edits':0};snapshot=get(COPY/'SUBMITTED_SNAPSHOT.json');state['body']=''
# The authenticated original body is read from the frozen preflight record.
pre=get(COPY/'LIVE_PR_PREFLIGHT.json');body_candidates=[]
def strings(x):
 if isinstance(x,str):yield x
 elif isinstance(x,dict):
  for v in x.values():yield from strings(v)
 elif isinstance(x,list):
  for v in x:yield from strings(v)
for doc in [pre,snapshot]:
 body_candidates += [x for x in strings(doc) if hashlib.sha256(x.encode()).hexdigest()==snapshot['body_sha256']]
need(body_candidates,'Pinned original PR body absent from preflight');state['body']=body_candidates[0]
def fakegit(*args,data=None):
 if args[:2]==('ls-remote','origin'):return (state['head']+'\trefs/heads/'+u.BRANCH+'\n').encode()
 if args[:2]==('push','origin'):
  commit=args[2].split(':')[0];need(state['head']==u.ORIGINAL,'Unexpected second/non-original push');state['pushes']+=1;state['head']=commit;return b''
 return origgit(*args,data=data)
u.git=fakegit;u.pr=lambda:{'headRefOid':state['head'],'headRefName':u.BRANCH,'state':'OPEN','isDraft':True,'body':state['body']}
def gh_run(args,**kw):
 need(args[:3]==['gh','pr','edit'],'Unmocked external operation');state['edits']+=1;state['body']=(PUB/'PR_BODY_FINAL.md').read_text();return types.SimpleNamespace(returncode=1 if state['lostbody'] else 0,stderr='simulated lost response' if state['lostbody'] else '',stdout='')
# original git refers to module subprocess: retain real git implementation explicitly.
def isolated_git(*args,data=None):
 run=REAL_RUN(['git','-c','gc.auto=0',*args],cwd=repo,input=data,capture_output=True)
 if run.returncode:raise RuntimeError(run.stderr.decode())
 return run.stdout
origgit=isolated_git;u.subprocess=types.SimpleNamespace(run=gh_run)
index=repo/'.git/index';index_before=index.read_bytes() if index.exists() else None
state['lostbody']=True;reject('pr_full_main_accepted_body_lost_response',lambda:quiet(u.main));need(state['pushes']==1 and state['edits']==1 and not (PUB/'PR_BRANCH_RECEIPT.json').exists(),'Lost body result wrongly completed')
state['lostbody']=False;quiet(u.main);quiet(u.main);receipt=get(PUB/'PR_BRANCH_RECEIPT.json');need(state['pushes']==1 and state['edits']==1,'PR resume repeated remote writes');need(receipt['body_readback_verified'] and len(receipt['paths'])==13,'PR complete receipt absent');need(index_before==(index.read_bytes() if index.exists() else None),'Review clone index changed')
ok('pr_full_main_real_local_13_file_commit_and_lost_response_idempotence',pushes_mocked=1,body_edits_mocked=1,index_unchanged=True)
for cell in range(4):
 pth=PUB/'tracker/TRACKER_RECEIPT.json';old=pth.read_bytes();x=get(pth);x['row'][cell]='wrong';save(pth,x);reject('pr_main_full_tracker_cell_'+str(cell),lambda:quiet(u.main));pth.write_bytes(old)
for key in ['id','doi','doi_url','record_url','metadata_fields_verified','metadata_manifest_sha256']:
 path=PUB/'PUBLIC_DOWNLOAD_VERIFICATION.json';old=path.read_bytes();x=get(path);x[key]=[] if key=='metadata_fields_verified' else 'changed';save(path,x);reject('pr_main_public_receipt_'+key,lambda:quiet(u.main));path.write_bytes(old)
for key in ['workflow','original_head','latest_review']:
 old=(PUB/'FINAL_REVIEW_GATE.json').read_bytes();x=copy.deepcopy(gate)
 if key=='workflow':x[key]={}
 elif key=='original_head':x[key]='0'*40
 else:x[key]['status']='CHANGES_REQUIRED'
 save(PUB/'FINAL_REVIEW_GATE.json',x);reject('pr_main_review_gate_'+key,lambda:quiet(u.main));(PUB/'FINAL_REVIEW_GATE.json').write_bytes(old)
for key in ['review_gate_sha256','metadata_sha256','body_sha256','files','tracker_receipt_sha256','deposit_id']:
 path=PUB/'PR_BRANCH_RECEIPT.json';old=path.read_bytes();x=get(path);x[key]={} if key=='files' else 'changed';save(path,x);reject('pr_main_saved_receipt_'+key,lambda:quiet(u.main));path.write_bytes(old)
# Same-parent wrong actual tree is rejected even with a saved intent-shaped record.
files,_,note=u.desired_files(build,pub,tracker,snapshot);body=(PUB/'PR_BODY_FINAL.md').read_text();wanted=u.expected_identity(pub,tracker,files,body)
wrongtree=isolated_git('rev-parse',u.ORIGINAL+'^{tree}').decode().strip();wrongcommit=isolated_git('commit-tree',wrongtree,'-p',u.ORIGINAL,data=b'wrong tree fixture\n').decode().strip();reject('saved_commit_actual_wrong_paths',lambda:u.validate_saved({**wanted,'commit':wrongcommit},wanted,files))
oldhead=state['head'];state['head']=u.ORIGINAL;reject('pr_completed_receipt_expected_head_changed',lambda:quiet(u.main));state['head']=oldhead
oldbody=state['body'];state['body']='unrecognized body';reject('pr_unknown_body_not_overwritten',lambda:quiet(u.main));state['body']=oldbody
# Generic repository kit, only local preparation and mocked remote lifecycle.
z=load(Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py'));z.STATE_DIR=HERE/'scratch/zenodo-state';z.doi_status=lambda doi:{'status':'resolved','scope':'mock only'}
args=types.SimpleNamespace(command='check',manifest=PUB/'zenodo-deposit.json',sandbox=False,confirm_id=None,check_doi=False);need(z.run(args)['title']==metadata['title'],'Kit local check');meta,fs=z.load_manifest(args.manifest.resolve())
class Client:
 def __init__(self):self.creates=0;self.posts=0;self.uploads=0;self.dep=None
 def create(self,md):self.creates+=1;self.dep={'id':pub['id'],'submitted':False,'metadata':copy.deepcopy(md),'files':[],'links':{'bucket':'https://zenodo.org/fixture-bucket'}};return copy.deepcopy(self.dep)
 def get(self,id):need(id==pub['id'],'Wrong mock record');return copy.deepcopy(self.dep)
 def upload(self,bucket,entry):self.uploads+=1;self.dep['files'].append({'filename':entry['name'],'filesize':entry['size'],'checksum':'md5:'+entry['md5']})
 def update(self,id,md):self.dep['metadata']=copy.deepcopy(md)
 def publish(self,id):self.posts+=1;self.dep['submitted']=True;self.dep['doi']=pub['doi'];raise z.DepositError('Mock accepted publication response lost')
cl=Client();args.command='stage';z.run(args,cl);z.run(args,cl);need(cl.creates==1 and cl.uploads==2,'Kit restage duplicated create/uploads');args.command='inspect';need(z.run(args,cl)['metadata_normalizations']==[],'Exact metadata required');args.command='publish';args.confirm_id=1;reject('kit_wrong_known_publish_id',lambda:z.run(args,cl),(z.DepositError,));args.confirm_id=pub['id'];out=z.run(args,cl);need(out['recovered_after_publish_error'] and cl.posts==1,'Lost publish not reconciled');z.run(args,cl);need(cl.posts==1,'Publish retry posted twice');ok('generic_zenodo_kit_mocked_saved_id_stage_inspect_lost_publish_idempotence',creates=cl.creates,publishes=cl.posts,metadata_normalizations=[])
# Input receipts/inventories are not replaced by claims about absent external bodies.
for n in ['priority/independent/evidence/MANIFEST.json','priority/adversary/EVIDENCE_INVENTORY.json','reviews/analytic_adversary/EVIDENCE_HASHES.json']:
 need((AUDIT/n).exists(),'Source receipt absent')
save(HERE/'INDEPENDENT_CHECKS_RECEIPT.json',{'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(checks),'checks':checks,'scope':'All external GitHub/GWS/Zenodo calls mocked; only review-copy Git objects created. PDF compilation real, offline cached with original epoch. These tests validate workflow contracts, not analytic theorem truth or live publication.'})
print(json.dumps({'status':'PASS','checks':len(checks)},indent=2))
