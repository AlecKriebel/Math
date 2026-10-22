#!/usr/bin/env python3
"""Whole entry-point fixtures. Every Git/gh/GWS/Zenodo operation is mocked.
This is ordinary error/retry testing, not a certification of live later actions.
"""
from pathlib import Path
import copy,datetime,hashlib,importlib.util,io,json,shutil,subprocess,sys,types,zipfile
from contextlib import redirect_stdout
HERE=Path(__file__).resolve().parent;PUB=HERE.parent.parent/'publication';TMP=HERE/'_entrypoints'
def need(c,m):
 if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2)+'\n')
def load(path):
 s=importlib.util.spec_from_file_location('r3_'+path.stem+'_'+str(id(path)),path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
checks=[]
def okay(name,fn):
 with redirect_stdout(io.StringIO()):r=fn()
 checks.append({'name':name,'outcome':'PASS'});return r
def reject(name,fn,after=None):
 try:
  with redirect_stdout(io.StringIO()):fn()
 except (RuntimeError,ValueError,KeyError,FileNotFoundError):checks.append({'name':name,'outcome':'REJECTED'})
 else:raise RuntimeError('Negative fixture accepted '+name)
 if after:after()

def base(name):
 root=TMP/name/'publication';root.mkdir(parents=True)
 for n in ['prepare_package.py','build_package.py','compile_note.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py','verification/verify.py','manuscript/main.tex','CURRENT_SIMULTANEOUS_PROOF.md','zenodo-deposit.json','BUILD_RECEIPT.json','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json','Polynomial_Multipliers_Note_v1.0.pdf','Polynomial_Multipliers_Verification_v1.0.zip']:
  p=root/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PUB/n,p)
 return root

def tracker_tests():
 root=base('tracker');m=load(root/'append_tracker.py');title=json.loads((root/'zenodo-deposit.json').read_text())['metadata']['title'];pub={'environment':'production','state':'published','metadata_normalizations':[],'id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','title':title};save(root/'PUBLICATION_RECEIPT.json',pub)
 row=m.expected_row(pub,title);state={'rows':[['Original Problem','Solution Chat URL','DOI','Notes']],'append':0,'lost':False,'tab':'Math Puzzles','bad_readback':False}
 def call(parts,params,body=None):
  need(params['spreadsheetId']==m.SID,'bad SID')
  if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':m.GID,'title':state['tab']}}]}
  if parts==['spreadsheets','values','get']:
   if params['range'].endswith('!A:D'):return {'values':copy.deepcopy(state['rows'])}
   return {'values':[['wrong']] if state['bad_readback'] else [state['rows'][-1]]}
  if parts==['spreadsheets','values','append']:
   need((root/'tracker/INTENT.json').exists(),'append happened before intent');need(body['values']==[row],'row');state['append']+=1;state['rows'].append(row)
   if state['lost']:raise RuntimeError('accepted append; simulated lost response')
   return {'updates':{'updatedRange':"'"+state['tab']+"'!A2:D2",'updatedRows':1,'updatedColumns':4}}
  raise RuntimeError('unmocked GWS operation')
 m.call=call;okay('tracker_main_append_once_and_exact_readback',m.main);okay('tracker_main_retry_recovers_exact_row',m.main);need(state['append']==1,'duplicate append')
 (root/'tracker').rename(root/'old-tracker');state['rows']=state['rows'][:1];state['lost']=True;reject('tracker_main_lost_response',m.main);state['lost']=False;okay('tracker_main_reconciles_accepted_lost_response',m.main);need(state['append']==2,'lost append duplicated')
 state['rows'].append(row);reject('tracker_main_duplicate_existing_problem',m.main);state['rows'].pop();state['rows'][1]=row[:2]+['wrong',row[3]];reject('tracker_main_existing_conflicting_row',m.main);state['rows'][1]=row
 state['rows'][0]=['wrong'];reject('tracker_main_wrong_header_before_append',m.main)
 # Renamed same-gid tab: observe whether it mutates before hard-coded range validation.
 state['rows']=[['Original Problem','Solution Chat URL','DOI','Notes']];state['tab']='Renamed';shutil.rmtree(root/'tracker');before=state['append'];reject('tracker_renamed_tab',m.main)
 return {'renamed_tab_append_before_rejection':state['append']-before,'scope':'The exact same designated gid remains selected after rename; final hard-coded title validation rejects its returned range.'}

def public_tests():
 root=base('public');m=load(root/'check_public_downloads.py');build=json.loads((root/'BUILD_RECEIPT.json').read_text());wanted=json.loads((root/'zenodo-deposit.json').read_text())['metadata'];pub={'environment':'production','state':'published','metadata_normalizations':[],'id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','title':wanted['title']};save(root/'PUBLICATION_RECEIPT.json',pub)
 meta=copy.deepcopy(wanted);meta['resource_type']={'type':meta.pop('upload_type'),'subtype':meta.pop('publication_type')};meta['license']={'id':meta['license']};meta['doi']=pub['doi']
 record={'id':123,'doi':pub['doi'],'metadata':meta,'files':[{'key':build[k]['path'],'links':{'self':'https://fixture.invalid/'+build[k]['path']}} for k in ['pdf','verification_zip']]};mode={'corrupt':False}
 def fetch(url,limit):
  if url=='https://zenodo.org/api/records/123':return json.dumps(record).encode()
  p=root/url.rsplit('/',1)[1];need(p.name in [build[k]['path'] for k in ['pdf','verification_zip']],'unmocked Zenodo endpoint');return p.read_bytes()+(b'bad' if mode['corrupt'] else b'')
 m.fetch=fetch;okay('public_main_exact_same_record_all_metadata_and_files',m.main)
 for key in wanted:
  old=copy.deepcopy(record['metadata'])
  if key=='upload_type':record['metadata']['resource_type']['type']='bad'
  elif key=='publication_type':record['metadata']['resource_type']['subtype']='bad'
  elif key=='license':record['metadata']['license']['id']='bad'
  else:record['metadata'][key]=None
  reject('public_main_changed_metadata_'+key,m.main);record['metadata']=old
 record['id']=999;reject('public_main_other_record',m.main);record['id']=123;mode['corrupt']=True;reject('public_main_corrupt_public_file',m.main);mode['corrupt']=False
 record['files'].append(record['files'][0]);reject('public_main_duplicate_public_file',m.main)

def prepare_fixture():
 root=base('build');audit=root.parent;archive=PUB/'verification'
 shutil.copytree(archive,root/'verification',dirs_exist_ok=True);shutil.copytree(archive/'original_submitted',audit/'submitted');shutil.copytree(archive/'current_edition',audit/'current_edition');shutil.copytree(archive/'reviews',audit/'reviews');shutil.copytree(archive/'priority',audit/'priority')
 for p in (archive/'provenance').iterdir():shutil.copyfile(p,audit/p.name)
 shutil.copyfile(archive/'diagnostics/root_diagnostics.py',audit/'root_diagnostics.py')
 shutil.copyfile(archive/'reviews/analytic_source_adversary/exact_normal.json',audit/'reviews/analytic_source_adversary/exact_normal.json')
 (root/'output/pdf').mkdir(parents=True);shutil.copyfile(PUB/'Polynomial_Multipliers_Note_v1.0.pdf',root/'output/pdf/main.pdf')
 return root

def build_tests():
 root=prepare_fixture();p=load(root/'prepare_package.py');okay('prepare_main_in_copied_audit_context',p.main)
 for n in p.NAMES:need((root.parent/'current_edition'/n).read_bytes()==(PUB/'verification/current_edition'/n).read_bytes(),'prepare drift '+n)
 m=load(root/'build_package.py');okay('build_main_from_copied_audit_context',m.main);need((root/'Polynomial_Multipliers_Verification_v1.0.zip').read_bytes()==(PUB/'Polynomial_Multipliers_Verification_v1.0.zip').read_bytes(),'rebuild nonidentical ZIP');need((root/'Polynomial_Multipliers_Note_v1.0.pdf').read_bytes()==(PUB/'Polynomial_Multipliers_Note_v1.0.pdf').read_bytes(),'rebuild PDF')
 # Patch ONLY local subprocess preparation/replay to avoid redundant drivers in fault cases.
 m.subprocess=types.SimpleNamespace(run=lambda *a,**kw:types.SimpleNamespace(stdout=json.dumps(json.loads((root/'BUILD_RECEIPT.json').read_text())['verification_run']),returncode=0))
 before={n:(root/n).read_bytes() for n in ['Polynomial_Multipliers_Verification_v1.0.zip','Polynomial_Multipliers_Note_v1.0.pdf','BUILD_RECEIPT.json']}
 def unchanged():need(all((root/n).read_bytes()==b for n,b in before.items()),'release replaced after invalid document state')
 for name in ['manuscript/main.tex','output/pdf/main.pdf','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json']:
  path=root/name;raw=path.read_bytes();path.write_bytes(raw+b'changed');reject('build_main_preflight_corrupt_'+name,m.main,unchanged);path.write_bytes(raw)
 # Source or assurance changes during temporary ZIP creation must precede replacement.
 realzip=zipfile.ZipFile
 for kind in ['source','pdf','compile','layout']:
  path=root/({'source':'manuscript/main.tex','pdf':'output/pdf/main.pdf','compile':'COMPILE_RECEIPT.json','layout':'LAYOUT_VERIFICATION.json'}[kind]);raw=path.read_bytes()
  class ChangeOnClose(realzip):
   def close(self):
    writing=self.mode=='w';super().close()
    if writing and not getattr(self,'changed_once',False):self.changed_once=True;path.write_bytes(raw+b'\n ')
  m.zipfile=types.SimpleNamespace(ZipFile=ChangeOnClose,ZipInfo=zipfile.ZipInfo,ZIP_DEFLATED=zipfile.ZIP_DEFLATED)
  reject('build_main_midzip_document_drift_'+kind,m.main,unchanged);path.write_bytes(raw)
 m.zipfile=zipfile
 return {'deterministic_rebuild_exact_zip_pdf':True,'source_pdf_qa_preflight_and_postzip_drift_controls':8}

def updater_tests():
 root=base('updater');audit=root.parent;m=load(root/'update_pr_publication.py');t=load(root/'append_tracker.py');title=json.loads((root/'zenodo-deposit.json').read_text())['metadata']['title']
 shutil.copytree(PUB/'verification/current_edition',audit/'current_edition')
 snapshot=json.loads((PUB/'verification/provenance/SUBMITTED_SNAPSHOT.json').read_text());snapshot['body_sha256']=sha(b'original fixture body');save(audit/'SUBMITTED_SNAPSHOT.json',snapshot)
 zp=root/'Polynomial_Multipliers_Verification_v1.0.zip'
 with zipfile.ZipFile(zp) as z:members={n:z.read(n) for n in z.namelist()}
 members['provenance/SUBMITTED_SNAPSHOT.json']=(audit/'SUBMITTED_SNAPSHOT.json').read_bytes()
 with zipfile.ZipFile(zp,'w') as z:
  for n,b in members.items():z.writestr(n,b)
 build=json.loads((root/'BUILD_RECEIPT.json').read_text());build['verification_zip'].update(bytes=zp.stat().st_size,sha256=sha(zp.read_bytes()));save(root/'BUILD_RECEIPT.json',build)
 pub={'environment':'production','state':'published','metadata_normalizations':[],'id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','title':title,'files':[{'name':build[k]['path'],'sha256':build[k]['sha256'],'size':build[k]['bytes']} for k in ['pdf','verification_zip']]};save(root/'PUBLICATION_RECEIPT.json',pub)
 tracker={'spreadsheetId':t.SID,'gid':t.GID,'updatedRange':"'Math Puzzles'!A999:D999",'row':t.expected_row(pub,title),'readback_verified':True};save(root/'tracker/TRACKER_RECEIPT.json',tracker)
 metadata=json.loads((root/'zenodo-deposit.json').read_text())['metadata'];public={'id':123,'doi':pub['doi'],'doi_url':pub['doi_url'],'record_url':pub['record_url'],'public_record_identity_verified':True,'all_supplied_metadata_exact':True,'metadata_manifest_sha256':sha((root/'zenodo-deposit.json').read_bytes()),'metadata_fields_verified':sorted(metadata),'files':[{'name':build[k]['path'],'bytes':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]};save(root/'PUBLIC_DOWNLOAD_VERIFICATION.json',public)
 review=audit/'reviews/current';save(review/'VERDICT.json',{'status':'CLEAN'});(review/'REPORT.md').write_text('synthetic clean fixture, not a real clearance')
 gate={'schema':'math-preprint-final-review-gate-v1','pr':1216,'problem_id':30000921,'original_head':m.ORIGINAL,'status':'pass','workflow':{n:sha((root/n).read_bytes()) for n in m.REQUIRED_WORKFLOW},'latest_review':{'status':'CLEAN','report':'../reviews/current/REPORT.md','report_sha256':sha((review/'REPORT.md').read_bytes()),'verdict':'../reviews/current/VERDICT.json','verdict_sha256':sha((review/'VERDICT.json').read_bytes())},'pdf_sha256':build['pdf']['sha256'],'verification_zip_sha256':build['verification_zip']['sha256'],'metadata_sha256':sha((root/'zenodo-deposit.json').read_bytes())};save(root/'FINAL_REVIEW_GATE.json',gate)
 objects={};trees={};commits={};origfiles={f['path']:members['original_submitted/'+Path(f['path']).name] for f in snapshot['files']};origfiles['unrelated/preserved.txt']=b'untouched'
 def blob(b):h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();objects[h]=b;return h
 def initial_tree(files):
  entries={};groups={}
  for p,b in files.items():
   h,sep,tail=p.partition('/')
   if sep:groups.setdefault(h,{})[tail]=b
   else:entries[h]=('100644','blob',blob(b))
  for h,g in groups.items():entries[h]=('040000','tree',initial_tree(g))
  h=hashlib.sha1(json.dumps(entries,sort_keys=True).encode()).hexdigest();trees[h]=entries;return h
 trees[m.ORIGINAL]=trees[initial_tree(origfiles)]
 def flatten(ref):
  ref=commits[ref]['tree'] if ref in commits else ref;out={}
  for name,(mode,kind,h) in trees[ref].items():
   if kind=='blob':out[name]=objects[h]
   else:out.update({name+'/'+p:b for p,b in flatten(h).items()})
  return out
 state={'headRefOid':m.ORIGINAL,'headRefName':m.BRANCH,'state':'OPEN','isDraft':True,'body':'original fixture body'};remote={'head':m.ORIGINAL};calls=[];lost={'push':False,'body':False}
 def git(*args,data=None):
  calls.append(args)
  if args==('branch','--show-current'):return b'main\n'
  if args[0]=='rev-parse':return next(f['blob'] for f in snapshot['files'] if args[1]==m.ORIGINAL+':'+f['path']).encode()+b'\n'
  if args[0]=='hash-object':return blob(data).encode()+b'\n'
  if args[0]=='ls-tree':return b'\0'.join((mode+' '+kind+' '+h+'\t'+name).encode() for name,(mode,kind,h) in sorted(trees[args[-1]].items()))+b'\0'
  if args[0]=='mktree':
   entries={}
   for line in data.rstrip(b'\0').split(b'\0'):
    v,n=line.decode().split('\t');entries[n]=tuple(v.split())
   h=hashlib.sha1(json.dumps(entries,sort_keys=True).encode()).hexdigest();trees[h]=entries;return h.encode()+b'\n'
  if args[0]=='commit-tree':
   h=hashlib.sha1((args[1]+args[3]).encode()+data).hexdigest();commits[h]={'tree':args[1],'parent':args[3]};return h.encode()+b'\n'
  if args[0]=='update-ref':return b''
  if args[0]=='rev-list':return (args[-1]+' '+commits[args[-1]]['parent']+'\n').encode()
  if args[0]=='diff-tree':
   now=flatten(args[-1]);prev=flatten(commits[args[-1]]['parent']);return ('\n'.join(sorted(p for p in set(now)|set(prev) if now.get(p)!=prev.get(p)))+'\n').encode()
  if args[0]=='show':ref,path=args[1].split(':',1);return flatten(ref)[path]
  if args[0]=='ls-remote':return (remote['head']+' refs/heads/'+m.BRANCH+'\n').encode()
  if args[0]=='push':
   need(args[1]=='origin' and len(args)==3 and not any('force' in x for x in args),'push scope');commit,dest=args[2].split(':');need(dest=='refs/heads/'+m.BRANCH,'wrong branch');remote['head']=commit;state['headRefOid']=commit
   if lost['push']:raise RuntimeError('accepted push, lost response')
   return b'ok\n'
  raise RuntimeError('UNMOCKED Git operation '+repr(args))
 edits=[]
 def edit(args,**kwargs):
  edits.append(args);need(args[:3]==['gh','pr','edit'],'UNMOCKED command');need(state['headRefOid']==remote['head'],'head before edit');state['body']=(root/'PR_BODY_FINAL.md').read_text();return types.SimpleNamespace(returncode=1 if lost['body'] else 0,stderr='lost edit response' if lost['body'] else '',stdout='')
 m.git=git;m.pr=lambda:copy.deepcopy(state);m.subprocess=types.SimpleNamespace(run=edit)
 # All preflights precede any object/push/body operation.
 def no_mutation():need(not any(c[0] in {'hash-object','commit-tree','update-ref','push'} for c in calls),'negative preflight mutated Git')
 for name,change in [('missing_required_workflow',lambda g:g['workflow'].pop('compile_note.py')),('nonclean_review',lambda g:g['latest_review'].update(status='CHANGES_REQUIRED')),('wrong_pdf_gate',lambda g:g.update(pdf_sha256='0'*64))]:
  g=copy.deepcopy(gate);change(g);save(root/'FINAL_REVIEW_GATE.json',g);calls.clear();reject('updater_main_'+name,m.main,no_mutation)
 save(root/'FINAL_REVIEW_GATE.json',gate)
 for field in ['id','doi_url','record_url','metadata_manifest_sha256','metadata_fields_verified']:
  x=copy.deepcopy(public);x[field]=999 if field=='id' else [] if field=='metadata_fields_verified' else 'wrong';save(root/'PUBLIC_DOWNLOAD_VERIFICATION.json',x);calls.clear();reject('updater_main_bad_public_'+field,m.main,no_mutation)
 save(root/'PUBLIC_DOWNLOAD_VERIFICATION.json',public)
 for idx in range(4):
  x=copy.deepcopy(tracker);x['row'][idx]='bad';save(root/'tracker/TRACKER_RECEIPT.json',x);calls.clear();reject('updater_main_bad_tracker_cell_'+str(idx),m.main,no_mutation)
 save(root/'tracker/TRACKER_RECEIPT.json',tracker)
 lost['push']=True;reject('updater_main_accepted_push_lost_response',m.main);need((root/'PR_BRANCH_INTENT.json').exists() and not (root/'PR_BRANCH_RECEIPT.json').exists(),'lost push receipt');lost['push']=False
 lost['body']=True;reject('updater_main_accepted_body_lost_response',m.main);need(not (root/'PR_BRANCH_RECEIPT.json').exists(),'lost body completed falsely');lost['body']=False
 okay('updater_main_reconciles_push_and_body_without_repeat_writes',m.main);pushes=sum(c[0]=='push' for c in calls);okay('updater_main_completed_idempotent_readback',m.main);need(sum(c[0]=='push' for c in calls)==pushes==1,'duplicate push');need(flatten(remote['head'])['unrelated/preserved.txt']==b'untouched','foreign changed');need(len(json.loads((root/'PR_BRANCH_RECEIPT.json').read_text())['paths'])==13,'13 paths');need(len(edits)==1,'body edit repeated on recovery')
 intent=(root/'PR_BRANCH_INTENT.json').read_bytes();receipt=(root/'PR_BRANCH_RECEIPT.json').read_bytes()
 for field in ['review_gate_sha256','metadata_sha256','doi','deposit_id','body_sha256','files','paths','tracker_range']:
  x=json.loads(receipt);x[field]='stale';save(root/'PR_BRANCH_RECEIPT.json',x);reject('updater_main_stale_saved_receipt_'+field,m.main)
 (root/'PR_BRANCH_RECEIPT.json').write_bytes(receipt)
 state['body']='unknown new body';reject('updater_main_never_overwrites_unknown_current_body',m.main);need(state['body']=='unknown new body','body overwrite')
 return {'mocked_real_tree_logic':True,'intended_changed_paths':13,'push_calls':pushes,'body_edit_calls':len(edits),'unrelated_file_preserved':True,'scope':'Synthetic Git objects/parent/tree bytes and GitHub state; no actual Git, gh, GWS, or Zenodo command executed.'}

def compile_tests():
 root=base('compile');m=load(root/'compile_note.py');fake=root/'fake-compiler';fake.write_bytes(b'compiler fixture');m.shutil=types.SimpleNamespace(which=lambda x:str(fake));state={'change':False}
 def run(args,**kwargs):
  (root/'output/pdf').mkdir(parents=True,exist_ok=True);(root/'output/pdf/main.pdf').write_bytes(b'%PDF mock output')
  if state['change']:(root/'manuscript/main.tex').write_text('source changed while compiler ran')
  return types.SimpleNamespace(returncode=0,stdout='mock compiler success',stderr='')
 m.subprocess=types.SimpleNamespace(check_output=lambda *a,**k:'Mock compiler1',run=run);okay('compile_main_mock_success_binds_saved_source_and_pdf',m.main);state['change']=True;reject('compile_main_source_change_during_compilation',m.main)

if __name__=='__main__':
 shutil.rmtree(TMP,ignore_errors=True);TMP.mkdir()
 report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tracker':tracker_tests(),'public':public_tests(),'build':build_tests(),'updater':updater_tests(),'compile':compile_tests(),'checks':checks,'scope':'All writes stay in ignored fixtures beneath this review. Every external operation mocked; offline tests do not authenticate future live state.'}
 (HERE/'OFFLINE_ENTRYPOINT_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'checks':len(checks),'tracker':report['tracker'],'build':report['build'],'updater':report['updater']},indent=2))
