#!/usr/bin/env python3
"""Fresh review probes; all mutations confined to this review's scratch directory.
External GitHub/GWS/Zenodo operations are replaced with in-memory mocks.
"""
from pathlib import Path
import contextlib,copy,datetime,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,tempfile,types,zipfile
Q=Path(__file__).resolve().parents[1]
INPUT=Q.parents[1]
COPY=Q/'scratch/package'
PUB=COPY/'publication'
RESULTS=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def mod(name,path=None):
 p=path or PUB/(name+'.py');spec=importlib.util.spec_from_file_location('review_'+name.replace('/','_')+str(len(RESULTS)),p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def record(name,**kw):RESULTS.append({'name':name,'status':'PASS',**kw})
def reject(name,call,contains=None):
 try:call()
 except Exception as e:
  if isinstance(e,AssertionError):raise
  if contains and contains not in str(e):raise AssertionError((name,str(e),contains))
  record(name,error=str(e)[:240]);return
 raise AssertionError('Unexpected acceptance: '+name)
def quiet(fn):
 with contextlib.redirect_stdout(io.StringIO()):return fn()
def fixture(tag):return Path(tempfile.mkdtemp(prefix=tag+'-',dir=Q/'scratch'))

def archive_probes():
 root=fixture('archive');shutil.copytree(PUB/'verification',root/'v');v=mod('verification/verify');v.ROOT=root/'v';quiet(v.main)
 manifest=v.ROOT/'MANIFEST.json';original_manifest=manifest.read_bytes();obj=json.loads(original_manifest)
 def reseal():
  x=json.loads(original_manifest)
  for e in x['files']:e.update(bind(v.ROOT/e['path']))
  save(manifest,x)
 record('portable_baseline',members=len(obj['files'])+1,nested=v.authenticate_nested_manifests(v.ROOT))
 for key in ['missing','corrupt','unlisted','duplicate','unsafe']:
  manifest.write_bytes(original_manifest);target=v.ROOT/'README.md';old=target.read_bytes()
  if key=='missing':target.unlink()
  elif key=='corrupt':target.write_bytes(old+b'corruption')
  elif key=='unlisted':(v.ROOT/'extra.txt').write_text('unlisted')
  else:
   x=json.loads(original_manifest)
   if key=='duplicate':x['files'].append(x['files'][0])
   else:x['files'][0]['path']='../unsafe'
   save(manifest,x)
  reject('archive_'+key,lambda:quiet(v.main))
  target.write_bytes(old);(v.ROOT/'extra.txt').unlink(missing_ok=True)
 manifest.write_bytes(original_manifest)
 nested=v.authenticate_nested_manifests(v.ROOT)
 for n in nested:
  path=v.ROOT/n['path'];d=json.loads(path.read_text());e=d.get('entries',d.get('files'))[0];base=v.ROOT/n['base'];p=base/e.get('file',e.get('path'));old=p.read_bytes();p.write_bytes(old+b'changed');reseal()
  reject('nested_corruption_outer_resealed:'+n['path'],lambda:quiet(v.main))
  p.write_bytes(old);manifest.write_bytes(original_manifest)
 # Git-blob identity is independently checked beyond SHA256/length.
 p=v.ROOT/'provenance/SUBMITTED_SNAPSHOT.json';old=p.read_bytes();d=json.loads(old);d['files'][0]['blob']='0'*40;save(p,d);reseal();reject('submitted_git_identity_resealed',lambda:quiet(v.main),'Git object');p.write_bytes(old);manifest.write_bytes(original_manifest)
 # Written archive bytes are read back before release files are replaced.
 b=mod('build_package');b.ROOT=PUB;b.PACKAGE=PUB/'verification';before={n:sha(PUB/n) for n in ['Real_Complement_Modulus_Verification_v1.0.zip','Real_Complement_Modulus_Note_v1.0.pdf']};original=zipfile.ZipFile
 class CorruptZip(original):
  def writestr(self,zinfo,data,*a,**kw):
   if getattr(zinfo,'filename',zinfo)=='README.md':data+=b'written corruption'
   return super().writestr(zinfo,data,*a,**kw)
 b.zipfile=types.SimpleNamespace(ZipFile=CorruptZip,ZipInfo=zipfile.ZipInfo,ZIP_DEFLATED=zipfile.ZIP_DEFLATED)
 reject('build_written_zip_corruption',lambda:quiet(b.main),'Written ZIP bytes differ')
 assert before=={n:sha(PUB/n) for n in before};record('build_failure_preserves_release_artifacts')

def documents_and_prepare():
 b=mod('build_package');p=mod('prepare_package');c=mod('compile_note');r=fixture('documents');b.ROOT=r;p.ROOT=r;p.AUDIT=r.parent;p.EDITION=r.parent/'current_edition';p.PACKAGE=r/'verification'
 (r/'manuscript').mkdir();(r/'output/pdf').mkdir(parents=True);src=r/'manuscript/main.tex';pdf=r/'output/pdf/main.pdf';src.write_bytes(b'source');pdf.write_bytes(b'pdf')
 goodc={'returncode':0,'source_sha256':sha(src),'pdf_sha256':sha(pdf)};goodl={'status':'pass','source_sha256':sha(src),'pdf_sha256':sha(pdf),'all_pages_visually_inspected':True,'pages':7,'page_indices_inspected':list(range(1,8))}
 def restore():src.write_bytes(b'source');pdf.write_bytes(b'pdf');save(r/'COMPILE_RECEIPT.json',goodc);save(r/'LAYOUT_VERIFICATION.json',goodl)
 for key in ['missing_source','missing_pdf','missing_compile','missing_layout','source_drift','pdf_drift','failed_compile','stale_compile_source','stale_compile_pdf','stale_layout_source','stale_layout_pdf','layout_failed','wrong_pages','omitted_page','not_visually_checked']:
  restore()
  if key.startswith('missing_'):{'missing_source':src,'missing_pdf':pdf,'missing_compile':r/'COMPILE_RECEIPT.json','missing_layout':r/'LAYOUT_VERIFICATION.json'}[key].unlink()
  elif key=='source_drift':src.write_bytes(b'new source')
  elif key=='pdf_drift':pdf.write_bytes(b'new pdf')
  elif key in ['failed_compile','stale_compile_source','stale_compile_pdf']:
   x=copy.deepcopy(goodc);x['returncode' if key=='failed_compile' else 'source_sha256' if key.endswith('source') else 'pdf_sha256']=1 if key=='failed_compile' else '0'*64;save(r/'COMPILE_RECEIPT.json',x)
  else:
   x=copy.deepcopy(goodl)
   if key=='layout_failed':x['status']='fail'
   elif key=='wrong_pages':x['pages']=6;x['page_indices_inspected']=list(range(1,7))
   elif key=='omitted_page':x['page_indices_inspected']=[1,2,3,5,6,7]
   elif key=='not_visually_checked':x['all_pages_visually_inspected']=False
   else:x['source_sha256' if key.endswith('source') else 'pdf_sha256']='0'*64
   save(r/'LAYOUT_VERIFICATION.json',x)
  reject('document_'+key,b.document_bindings)
 restore();b.document_bindings();record('document_valid_binding')
 for key in ['missing_priority','novelty','firstness','openness','missing_original_proof']:
  a=p.AUDIT/'PRIORITY_ADJUDICATION.json';save(a,{'novelty_clearance':False,'firstness_claim':False,'current_openness_claim':False})
  if key=='missing_priority':a.unlink()
  elif key in ['novelty','firstness','openness']:
   x=json.loads(a.read_text());x[{'novelty':'novelty_clearance','firstness':'firstness_claim','openness':'current_openness_claim'}[key]]=True;save(a,x)
  reject('prepare_'+key,p.main)
 # compile_note executes no compiler after an unavailable lookup, and fails on
 # compiler failure or mid-build source change; success creates current bindings.
 c.ROOT=r;c.PROGRAM=r;compiler=r/'compiler';compiler.write_text('offline mock compiler')
 c.shutil=types.SimpleNamespace(which=lambda n:None);reject('compile_missing_compiler',lambda:quiet(c.main))
 c.shutil=types.SimpleNamespace(which=lambda n:str(compiler))
 for case in ['failure','source_changed','success']:
  restore()
  def run(*a,**kw):
   if case=='source_changed':src.write_text('changed during compile')
   (r/'output/pdf/main.pdf').write_bytes(b'generated')
   return types.SimpleNamespace(returncode=1 if case=='failure' else 0,stdout='offline fixture',stderr='offline fixture failed' if case=='failure' else '')
  c.subprocess=types.SimpleNamespace(check_output=lambda *a,**kw:'Mock compiler 1\n',run=run)
  if case!='success':reject('compile_'+case,lambda:quiet(c.main))
  else:
   quiet(c.main);d=json.loads((r/'COMPILE_RECEIPT.json').read_text());assert d['source_sha256']==sha(src) and d['pdf_sha256']==sha(pdf) and d['compiler_sha256']==sha(compiler);record('compile_success_receipt_binds_current_source_pdf_compiler')

def setup_release(tag):
 root=fixture(tag);p=root/'publication';shutil.copytree(PUB,p);shutil.copytree(COPY/'current_edition',root/'current_edition');shutil.copyfile(COPY/'SUBMITTED_SNAPSHOT.json',root/'SUBMITTED_SNAPSHOT.json')
 t=mod('append_tracker');m=mod('update_pr_publication');d=mod('check_public_downloads');m.ROOT=p;t.ROOT=p;d.ROOT=p
 meta=json.loads((p/'zenodo-deposit.json').read_text())['metadata'];build=json.loads((p/'BUILD_RECEIPT.json').read_text());pub={'id':123,'environment':'production','state':'published','metadata_normalizations':[],'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','url':'https://doi.org/10.5281/zenodo.123','title':meta['title'],'files':[{'name':build[k]['path'],'size':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]}
 tracker={'spreadsheetId':t.SID,'gid':t.GID,'readback_verified':True,'updatedRange':"'Math Puzzles'!A77:D77",'row':t.expected_row(pub,meta['title'])};save(p/'PUBLICATION_RECEIPT.json',pub);save(p/'tracker/TRACKER_RECEIPT.json',tracker)
 public={'id':pub['id'],'doi':pub['doi'],'doi_url':pub['doi_url'],'record_url':pub['record_url'],'public_record_identity_verified':True,'all_supplied_metadata_exact':True,'metadata_manifest_sha256':sha(p/'zenodo-deposit.json'),'metadata_fields_verified':sorted(meta),'files':[{'name':build[k]['path'],'bytes':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]};save(p/'PUBLIC_DOWNLOAD_VERIFICATION.json',public)
 review=root/'reviews/fresh';review.mkdir(parents=True);(review/'REPORT.md').write_text('CLEAN offline fixture, not an actual review clearance');save(review/'VERDICT.json',{'status':'CLEAN'})
 gate={'schema':'math-preprint-final-review-gate-v1','pr':1225,'problem_id':2307058,'original_head':m.ORIGINAL,'status':'pass','pdf_sha256':build['pdf']['sha256'],'verification_zip_sha256':build['verification_zip']['sha256'],'metadata_sha256':sha(p/'zenodo-deposit.json'),'workflow':{n:sha(p/n) for n in m.REQUIRED_WORKFLOW},'latest_review':{'status':'CLEAN','report':'../reviews/fresh/REPORT.md','verdict':'../reviews/fresh/VERDICT.json','report_sha256':sha(review/'REPORT.md'),'verdict_sha256':sha(review/'VERDICT.json')}};save(p/'FINAL_REVIEW_GATE.json',gate)
 state=json.loads((INPUT/'LIVE_PR_PREFLIGHT.json').read_text());snapshot=json.loads((root/'SUBMITTED_SNAPSHOT.json').read_text());files,_,_=m.desired_files(build,pub,tracker,snapshot);remote={'head':m.ORIGINAL};calls=[];commit='a'*40
 def git(*args,data=None):
  if args==('branch','--show-current'):return b'main\n'
  if args[0]=='rev-parse':return (next(x['blob'] for x in snapshot['files'] if args[1].split(':',1)[1]==x['path'])+'\n').encode()
  if args[0]=='hash-object':return (hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()+'\n').encode()
  if args[0]=='commit-tree':calls.append(('commit-tree',args));return (commit+'\n').encode()
  if args[0]=='update-ref':calls.append(('update-ref',args));return b''
  if args[0]=='rev-list':return (commit+' '+m.ORIGINAL+'\n').encode()
  if args[0]=='diff-tree':return ('\n'.join(sorted(files))+'\n').encode()
  if args[0]=='show':return files[args[1].split(':',1)[1]]
  if args[0]=='ls-remote':return (remote['head']+' refs/heads/'+m.BRANCH+'\n').encode()
  if args[0]=='push':
   assert args==('push','origin',commit+':refs/heads/'+m.BRANCH);calls.append(('push',args));remote['head']=commit;state['headRefOid']=commit;return b''
  raise AssertionError('Unexpected Git call '+repr(args))
 m.git=git;m.put=lambda base,parts,oid,kind='blob',mode='100644':'b'*40;m.pr=lambda:copy.deepcopy(state)
 def edit(args,**kw):
  assert args==['gh','pr','edit','1225','--repo','AlecKriebel/Math','--body-file',str(p/'PR_BODY_FINAL.md')]
  calls.append(('body_edit',args));state['body']=(p/'PR_BODY_FINAL.md').read_text();return types.SimpleNamespace(returncode=0,stdout='',stderr='')
 m.subprocess=types.SimpleNamespace(run=edit)
 return m,t,d,p,meta,build,pub,tracker,public,gate,state,remote,calls,files

def updater_probes():
 fx=setup_release('update');m,t,d,p,meta,build,pub,tracker,public,gate,state,remote,calls,files=fx
 quiet(m.main);assert [x[0] for x in calls].count('push')==1 and [x[0] for x in calls].count('body_edit')==1;assert len(files)==13 and all(n.startswith(m.BASE+'/') for n in files);receipt=json.loads((p/'PR_BRANCH_RECEIPT.json').read_text());assert receipt['body_readback_verified'] and receipt['remote_readback_verified'];record('updater_full_main_13_paths_exact_branch_and_final_body')
 before=len(calls);quiet(m.main);assert len(calls)==before;record('updater_completed_receipt_idempotent_zero_writes')
 # Lost push response: intent known and remote already moved; no repeat push.
 (p/'PR_BRANCH_RECEIPT.json').unlink();state['body']=json.loads((INPUT/'LIVE_PR_PREFLIGHT.json').read_text())['body'];before=len(calls);quiet(m.main);assert [x[0] for x in calls[before:]]==['body_edit'];record('updater_lost_push_response_recovers_known_head_without_push')
 for scenario in ['wrong_head','wrong_branch','closed','third_party_body','missing_gate','nonclean_review','missing_workflow','stale_pdf_gate','stale_zip_gate','stale_metadata_gate','wrong_pub_doi','wrong_pub_record','pub_normalized','public_wrong_id','public_wrong_doi','public_incomplete_fields','public_wrong_bytes','tracker_changed_A','tracker_changed_B','tracker_changed_C','tracker_changed_D','tracker_wrong_range','missing_source','stale_source_vs_zip','stale_snapshot']:
  fx=setup_release('update-negative');a,tt,dd,pp,me,bu,pu,tr,pv,ga,st,re,ca,fi=fx
  if scenario=='wrong_head':st['headRefOid']='c'*40
  elif scenario=='wrong_branch':st['headRefName']='foreign'
  elif scenario=='closed':st['state']='CLOSED'
  elif scenario=='third_party_body':st['body']='external revision'
  elif scenario=='missing_gate':(pp/'FINAL_REVIEW_GATE.json').unlink()
  elif scenario=='nonclean_review':ga['latest_review']['status']='CHANGES_REQUIRED';save(pp/'FINAL_REVIEW_GATE.json',ga)
  elif scenario=='missing_workflow':ga['workflow'].pop('compile_note.py');save(pp/'FINAL_REVIEW_GATE.json',ga)
  elif scenario.startswith('stale_') and scenario.endswith('_gate'):
   ga[{'stale_pdf_gate':'pdf_sha256','stale_zip_gate':'verification_zip_sha256','stale_metadata_gate':'metadata_sha256'}[scenario]]='0'*64;save(pp/'FINAL_REVIEW_GATE.json',ga)
  elif scenario in ['wrong_pub_doi','wrong_pub_record','pub_normalized']:
   pu[{'wrong_pub_doi':'doi','wrong_pub_record':'record_url','pub_normalized':'metadata_normalizations'}[scenario]]='10.5281/zenodo.999' if scenario=='wrong_pub_doi' else 'https://zenodo.org/records/999' if scenario=='wrong_pub_record' else ['changed'];save(pp/'PUBLICATION_RECEIPT.json',pu)
  elif scenario.startswith('public_'):
   if scenario=='public_wrong_id':pv['id']=999
   elif scenario=='public_wrong_doi':pv['doi']='10.5281/zenodo.999'
   elif scenario=='public_incomplete_fields':pv['metadata_fields_verified'].pop()
   else:pv['files'][0]['sha256']='0'*64
   save(pp/'PUBLIC_DOWNLOAD_VERIFICATION.json',pv)
  elif scenario.startswith('tracker_'):
   if scenario=='tracker_wrong_range':tr['updatedRange']="'Other'!A77:D77"
   else:tr['row']['ABCD'.index(scenario[-1])]='wrong'
   save(pp/'tracker/TRACKER_RECEIPT.json',tr)
  elif scenario=='missing_source':(pp.parent/'current_edition/PROOF.md').unlink()
  elif scenario=='stale_source_vs_zip':(pp.parent/'current_edition/PROOF.md').write_text('changed source')
  elif scenario=='stale_snapshot':(pp.parent/'SUBMITTED_SNAPSHOT.json').write_text('{}')
  reject('updater_main_'+scenario,lambda:quiet(a.main));assert not ca,'Mutation before rejection '+scenario
  shutil.rmtree(pp.parent)
 # Current intent cannot be reused under changed gate/body/deposit identities.
 fx=setup_release('update-oldintent');a,tt,dd,pp,me,bu,pu,tr,pv,ga,st,re,ca,fi=fx;quiet(a.main);(pp/'PR_BRANCH_RECEIPT.json').unlink();old=json.loads((pp/'PR_BRANCH_INTENT.json').read_text());old['review_gate_sha256']='0'*64;save(pp/'PR_BRANCH_INTENT.json',old);ca.clear();reject('updater_full_main_stale_intent_before_mutations',lambda:quiet(a.main));assert not ca

 def actual_tree_probe():
  rr=fixture('git-object-replay');subprocess.run(['git','init','-q',str(rr)],check=True);u=mod('update_pr_publication');u.REPO=rr
  blob=u.git('hash-object','-w','--stdin',data=b'preserved foreign file').decode().strip();base=u.put(None,['foreign','keep.txt'],blob);basecommit=u.git('-c','user.name=Offline reviewer','-c','user.email=offline@example.invalid','commit-tree',base,data=b'Offline fixture base\n').decode().strip();tree=basecommit
  for n,data in sorted(files.items()):oid=u.git('hash-object','-w','--stdin',data=data).decode().strip();tree=u.put(tree,n.split('/'),oid)
  new=u.git('-c','user.name=Offline reviewer','-c','user.email=offline@example.invalid','commit-tree',tree,'-p',basecommit,data=b'Offline fixture publication\n').decode().strip()
  assert sorted(u.git('diff-tree','--no-commit-id','--name-only','-r',new).decode().splitlines())==sorted(files)
  assert all(u.git('show',new+':'+n)==data for n,data in files.items());assert u.git('show',new+':foreign/keep.txt')==b'preserved foreign file';record('actual_git_object_tree_13_paths_parent_and_foreign_bytes_preserved',commit=new,parent=basecommit)
 actual_tree_probe()

def tracker_probes():
 for case in ['append','existing','lost_response','prior_intent_absent_row','mismatch','duplicate','wrong_header','renamed_tab','wrong_readback','bad_dimensions']:
  fx=setup_release('tracker');m,t,d,p,meta,build,pub,tracker,public,gate,state,remote,calls,files=fx;row=tracker['row'];rows=[['Original Problem','Solution Chat URL','DOI','Notes']];appends=[];gets=[];first={'lost':case=='lost_response'}
  if case in ['existing','mismatch','duplicate']:rows.append(copy.deepcopy(row))
  if case=='mismatch':rows[1][1]='wrong'
  if case=='duplicate':rows.append(copy.deepcopy(row))
  if case=='wrong_header':rows[0][1]='Changed header'
  if case=='prior_intent_absent_row':save(p/'tracker/INTENT.json',{'old':True})
  def call(parts,params,body=None):
   gets.append((parts,params))
   if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':t.GID,'title':'Renamed' if case=='renamed_tab' else 'Math Puzzles'}}]}
   if parts==['spreadsheets','values','get']:
    return {'values':copy.deepcopy(rows if params['range']=="'Math Puzzles'!A:D" else [['bad']] if case=='wrong_readback' else [row])}
   if parts==['spreadsheets','values','append']:
    assert body['values']==[row] and row[1]=='';appends.append(body);rows.append(copy.deepcopy(row))
    if first['lost']:first['lost']=False;raise RuntimeError('simulated lost accepted append response')
    return {'updates':{'updatedRange':"'Math Puzzles'!A2:D2",'updatedRows':1,'updatedColumns':3 if case=='bad_dimensions' else 4}}
   raise AssertionError('Unexpected GWS call '+repr(parts))
  t.call=call
  if case in ['append','existing']:quiet(t.main);assert len(appends)==(1 if case=='append' else 0);before=len(appends);quiet(t.main);assert len(appends)==before;record('tracker_main_'+case+'_and_idempotence')
  elif case=='lost_response':reject('tracker_lost_append_response',lambda:quiet(t.main));assert (p/'tracker/INTENT.json').exists();quiet(t.main);assert len(appends)==1;record('tracker_lost_response_exact_reconciliation_no_second_append')
  else:
   reject('tracker_main_'+case,lambda:quiet(t.main));assert len(appends)==(1 if case in ['wrong_readback','bad_dimensions'] else 0)
  shutil.rmtree(p.parent)

def public_and_kit():
 fx=setup_release('public');m,t,d,p,meta,build,pub,tracker,public,gate,state,remote,calls,files=fx
 actualmeta=copy.deepcopy(meta);actualmeta['resource_type']={'type':actualmeta.pop('upload_type'),'subtype':actualmeta.pop('publication_type')};actualmeta['license']={'id':actualmeta['license']};actualmeta['doi']=pub['doi'];actual={'id':pub['id'],'doi':pub['doi'],'metadata':actualmeta,'files':[{'key':build[k]['path'],'links':{'self':'https://zenodo.org/records/123/files/'+build[k]['path']}} for k in ['pdf','verification_zip']]}
 def fetch(url,limit):
  if url=='https://zenodo.org/api/records/123':return json.dumps(actual).encode()
  return (p/url.rsplit('/',1)[1]).read_bytes()
 d.fetch=fetch;quiet(d.main);got=json.loads((p/'PUBLIC_DOWNLOAD_VERIFICATION.json').read_text());assert len(got['metadata_fields_verified'])==11;record('public_download_main_all_11_metadata_fields_two_exact_files')
 for key in meta:
  old=copy.deepcopy(actual['metadata'])
  if key in ['upload_type','publication_type']:actual['metadata']['resource_type']['type' if key=='upload_type' else 'subtype']='wrong'
  elif key=='license':actual['metadata']['license']['id']='wrong'
  else:actual['metadata'][key]=None
  reject('public_metadata_'+key,lambda:quiet(d.main));actual['metadata']=old
 for key in ['wrong_id','wrong_doi','missing_file','duplicate_file','bad_download']:
  old=copy.deepcopy(actual)
  if key=='wrong_id':actual['id']=999
  elif key=='wrong_doi':actual['metadata']['doi']='10.5281/zenodo.999'
  elif key=='missing_file':actual['files'].pop()
  elif key=='duplicate_file':actual['files'].append(actual['files'][0])
  else:
   orig=d.fetch;d.fetch=lambda url,limit:orig(url,limit) if url.endswith('/123') else b'corrupt bytes'
  reject('public_main_'+key,lambda:quiet(d.main));actual.clear();actual.update(old)
  if key=='bad_download':d.fetch=orig
 z=mod('zenodo_kit',INPUT.parents[2]/'zenodo_deposit_tool/zenodo.py');z.STATE_DIR=Q/'scratch/zenodo-state';z.SECRETS=Q/'scratch/nonexistent-secrets';path=p/'zenodo-deposit.json';md,ff=z.load_manifest(path);assert len(ff)==2 and len(md)==11
 summary=z.run(types.SimpleNamespace(command='check',manifest=path,sandbox=False));assert summary['files']==pub['files'];record('generic_kit_local_check_exact_artifacts_metadata')
 class FakeClient:
  def __init__(self):self.posts=0;self.gets=0;self.dep={'id':123,'submitted':False,'metadata':copy.deepcopy(md),'files':[{'filename':f['name'],'filesize':f['size'],'checksum':'md5:'+f['md5']} for f in ff]}
  def get(self,n):assert n==123;self.gets+=1;return copy.deepcopy(self.dep)
  def publish(self,n):assert n==123;self.posts+=1;self.dep['submitted']=True;self.dep['doi']='10.5281/zenodo.123';raise z.DepositError('lost publication response')
 fake=FakeClient();sp=z.state_path(path.resolve(),'production');z.save_state(sp,{'manifest':str(path.resolve()),'environment':'production','id':123});z.doi_status=lambda d:{'status':'not_checked','scope':'offline fixture'}
 args=types.SimpleNamespace(command='publish',manifest=path,sandbox=False,confirm_id=999);reject('generic_kit_wrong_confirm_id',lambda:z.run(args,fake));assert fake.posts==0
 args.confirm_id=123;out=z.run(args,fake);assert out['state']=='published' and out['recovered_after_publish_error'] and fake.posts==1;again=z.run(args,fake);assert again['already_published'] and fake.posts==1;record('generic_kit_lost_publish_response_same_id_readback_no_second_POST')
 fake.dep['metadata']['title']='changed';reject('generic_kit_stale_published_metadata',lambda:z.run(args,fake));assert fake.posts==1

if __name__=='__main__':
 archive_probes();documents_and_prepare();updater_probes();tracker_probes();public_and_kit()
 result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','count':len(RESULTS),'checks':RESULTS,'execution_scope':'Only scratch writes; external mutations fully mocked. Real Git object test in an isolated scratch repository; no remote configured. No individual contacted.'}
 save(Q/'checks/independent_checks_receipt.json',result);print(json.dumps({'status':result['status'],'count':len(RESULTS)},indent=2))
