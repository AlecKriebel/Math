from pathlib import Path
import contextlib,copy,datetime,hashlib,importlib.util,io,json,shutil,types
R=Path(__file__).resolve().parent;A=Path(json.loads((R/'INPUT_FREEZE.json').read_text())['root']);W=R/'scratch_local/external';W.mkdir(exist_ok=True)
def load(n):
 s=importlib.util.spec_from_file_location('ind_external_'+n.replace('/','_'),A/'publication'/(n+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def need(c,m):
 if not c:raise RuntimeError(m)
def quiet(f):
 with contextlib.redirect_stdout(io.StringIO()):return f()
def pub():
 title=json.loads((A/'publication/zenodo-deposit.json').read_text())['metadata']['title'];return {'environment':'production','state':'published','metadata_normalizations':[],'id':981,'doi':'10.5281/zenodo.981','doi_url':'https://doi.org/10.5281/zenodo.981','record_url':'https://zenodo.org/records/981','url':'https://doi.org/10.5281/zenodo.981','title':title}
t=load('append_tracker');tracker_results=[]
def tracker_case(label,mode):
 p=W/('tracker_'+label);p.mkdir(exist_ok=True);t.ROOT=p;publication=pub();write(p/'PUBLICATION_RECEIPT.json',publication);shutil.copyfile(A/'publication/zenodo-deposit.json',p/'zenodo-deposit.json');row=t.expected_row(publication,publication['title']);rows=[['Original Problem','Solution Chat URL','DOI','Notes']];events=[]
 if mode=='existing':rows.append(row)
 if mode=='duplicate':rows.extend([row,row])
 if mode=='mismatch':rows.append([row[0],'',row[2],'different notes'])
 if mode=='header':rows[0][1]='Changed header'
 def call(parts,params,body=None):
  events.append(parts[-1]);need(params['spreadsheetId']==t.SID,'wrong sheet request')
  if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':t.GID,'title':'Other' if mode=='renamed' else 'Math Puzzles'}}]}
  if parts==['spreadsheets','values','append']:
   need(body['values']==[row] and params['range']=="'Math Puzzles'!A:D",'wrong append')
   if mode!='unconfirmed':rows.append(row)
   if mode in ('lost','unconfirmed'):raise RuntimeError('fake uncertain append')
   return {'updates':{'updatedRange':"'Math Puzzles'!A2:D2",'updatedRows':1,'updatedColumns':4}}
  if params['range']=="'Math Puzzles'!A:D":return {'values':copy.deepcopy(rows)}
  return {'values':[[*row[:3],'wrong']] if mode=='bad_readback' else [row]}
 t.call=call;out=[]
 for i in range(2 if mode in ('lost','unconfirmed','new','existing') else 1):
  try:quiet(t.main);out.append(True)
  except Exception as e:out.append(type(e).__name__+': '+str(e))
 append_count=events.count('append');expected={'new':([True,True],1),'existing':([True,True],0),'lost':(None,1),'unconfirmed':(None,1)}
 if mode in ('new','existing'):need(out==expected[mode][0] and append_count==expected[mode][1],'tracker idempotency')
 elif mode=='lost':need(out[0] is not True and out[1] is True and append_count==1,'lost append recovery')
 elif mode=='unconfirmed':need(all(x is not True for x in out) and append_count==1,'uncertain retry appended')
 elif mode=='bad_readback':need(out[0] is not True and append_count==1 and not (p/'tracker/TRACKER_RECEIPT.json').exists(),'bad readback receipt')
 else:need(out[0] is not True and append_count==0,'prewrite tracker refusal')
 return {'case':label,'outcomes':out,'appends':append_count,'events':events}
for mode in ('new','existing','duplicate','mismatch','header','renamed','lost','unconfirmed','bad_readback'):tracker_results.append(tracker_case(mode,mode))
# Public verifier entire main: exact source metadata/public projection and content.
public_results=[];cm=load('check_public_downloads');original_runpath=cm.runpy.run_path
for mode in ['exact','bad_id','bad_doi','duplicate_files','bad_content',*['field_'+k for k in json.loads((A/'publication/zenodo-deposit.json').read_text())['metadata']]]:
 p=W/('public_'+mode);p.mkdir(exist_ok=True);cm.ROOT=p;publication=pub();write(p/'PUBLICATION_RECEIPT.json',publication);write(p/'BUILD_RECEIPT.json',json.loads((A/'publication/BUILD_RECEIPT.json').read_text()));shutil.copyfile(A/'publication/zenodo-deposit.json',p/'zenodo-deposit.json');shutil.copyfile(A/'publication/append_tracker.py',p/'append_tracker.py');wanted=json.loads((p/'zenodo-deposit.json').read_text())['metadata'];build=json.loads((p/'BUILD_RECEIPT.json').read_text());meta=copy.deepcopy(wanted);meta['resource_type']={'type':meta.pop('upload_type'),'subtype':meta.pop('publication_type')};meta['license']={'id':meta['license']};meta['doi']=publication['doi'];body={'id':981,'doi':publication['doi'],'metadata':meta,'files':[{'key':build[k]['path'],'links':{'self':'https://offline.invalid/'+k}} for k in ('pdf','verification_zip')]}
 if mode=='bad_id':body['id']=982
 if mode=='bad_doi':body['doi']='10.5281/zenodo.982'
 if mode=='duplicate_files':body['files'].append(copy.deepcopy(body['files'][0]))
 if mode.startswith('field_'):
  field=mode[6:]
  if field in ('upload_type','publication_type'):meta['resource_type']['type' if field=='upload_type' else 'subtype']='wrong'
  elif field=='license':meta['license']['id']='wrong'
  else:meta[field]=None
 def fetch(url,limit):
  if '/api/records/' in url:return json.dumps(body).encode()
  key=url.rsplit('/',1)[1];data=(A/'publication'/build[key]['path']).read_bytes();return data+b'corrupted' if mode=='bad_content' else data
 cm.fetch=fetch
 try:quiet(cm.main);ok=True;err=None
 except Exception as e:ok=False;err=type(e).__name__+': '+str(e)
 need(ok==(mode=='exact'),'full public main wrong acceptance '+mode);public_results.append({'case':mode,'accepted':ok,'error':err})
# PR whole main using the real exact archive and current eight, synthetic release
# receipts, and a fake Git/PR server. Only saved-intent resumption is driven;
# every actual commit tree read is independently checked against desired bytes.
pr_results=[]
def pr_case(label,mode):
 m=load('update_pr_publication');p=W/('pr_'+label)/'publication';p.mkdir(parents=True,exist_ok=True);m.ROOT=p;m.REPO=p.parent
 for n in ('update_pr_publication.py','append_tracker.py','build_package.py','compile_note.py','prepare_package.py','check_public_downloads.py','workflow_regression.py','zenodo-deposit.json','BUILD_RECEIPT.json','Johnson_Filtration_Multiplicity_Note_v1.0.pdf','Johnson_Filtration_Multiplicity_Verification_v1.0.zip','verification/verify.py'):
  q=p/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A/'publication'/n,q)
 shutil.copytree(A/'current_edition',p.parent/'current_edition',dirs_exist_ok=True);shutil.copyfile(A/'SUBMITTED_SNAPSHOT.json',p.parent/'SUBMITTED_SNAPSHOT.json')
 rev=p.parent/'reviews/fixture';rev.mkdir(parents=True);(rev/'REPORT.md').write_text('Synthetic clean gate test only.');write(rev/'VERDICT.json',{'status':'CLEAN'});build=json.loads((p/'BUILD_RECEIPT.json').read_text());publication=pub();publication['files']=[{'name':build[k]['path'],'sha256':build[k]['sha256'],'size':build[k]['bytes']} for k in ('pdf','verification_zip')];tracker={'spreadsheetId':t.SID,'gid':t.GID,'row':t.expected_row(publication,publication['title']),'updatedRange':"'Math Puzzles'!A2:D2",'readback_verified':True};write(p/'PUBLICATION_RECEIPT.json',publication);write(p/'tracker/TRACKER_RECEIPT.json',tracker)
 public={'public_record_identity_verified':True,'all_supplied_metadata_exact':True,'metadata_manifest_sha256':m.digest(p/'zenodo-deposit.json'),'doi':publication['doi'],'id':981,'doi_url':publication['doi_url'],'record_url':publication['record_url'],'metadata_fields_verified':sorted(json.loads((p/'zenodo-deposit.json').read_text())['metadata']),'files':[{'name':build[k]['path'],'bytes':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ('pdf','verification_zip')]};write(p/'PUBLIC_DOWNLOAD_VERIFICATION.json',public)
 gate={'schema':'math-preprint-final-review-gate-v1','pr':1241,'problem_id':11000082,'original_head':m.ORIGINAL,'status':'pass','workflow':{n:m.digest(p/n) for n in m.REQUIRED_WORKFLOW},'latest_review':{'status':'CLEAN','report':'../reviews/fixture/REPORT.md','report_sha256':m.digest(rev/'REPORT.md'),'verdict':'../reviews/fixture/VERDICT.json','verdict_sha256':m.digest(rev/'VERDICT.json')},'pdf_sha256':build['pdf']['sha256'],'verification_zip_sha256':build['verification_zip']['sha256'],'metadata_sha256':m.digest(p/'zenodo-deposit.json')};write(p/'FINAL_REVIEW_GATE.json',gate)
 snapshot=json.loads((p.parent/'SUBMITTED_SNAPSHOT.json').read_text());files,publication_files,note=m.desired_files(build,publication,tracker,snapshot);need(len(files)==13,'PR desired paths');body=note+'\nThe eight-file MANIFEST.json binds the current mathematical edition. publication_20261017/ adds the reviewed preprint, portable verification archive, matching deposit metadata and publication receipt. Eligibility followed the explicit full original-target solution outcome recorded in this PR because QUEUE.md may be stale.\n';commit='a'*40;wanted=m.expected_identity(publication,tracker,files,body);saved={**wanted,'commit':commit};write(p/'PR_BRANCH_INTENT.json',saved)
 state={'remote':m.ORIGINAL if mode in ('push','push_lost') else commit,'head':m.ORIGINAL if mode in ('push','push_lost','api_lag') else commit,'body':'original body','edits':0,'pushes':0};events=[];first={'value':True}
 # Read original body from immutable submitted SHA is unavailable as content in
 # this fixture; substitute only its captured hash equality in the fixture copy.
 snapshot['body_sha256']=hashlib.sha256(b'original body').hexdigest();write(p.parent/'SUBMITTED_SNAPSHOT.json',snapshot)
 # Archive demands the immutable snapshot bytes. Restore it and choose the
 # intended final body as current; the body helper can be tested separately.
 shutil.copyfile(A/'SUBMITTED_SNAPSHOT.json',p.parent/'SUBMITTED_SNAPSHOT.json');state['body']=body
 if mode=='unknown_body':state['body']='external unexpected edit'
 if mode=='wrong_public_id':public['id']=982;write(p/'PUBLIC_DOWNLOAD_VERIFICATION.json',public)
 if mode=='tracker_cell':tracker['row'][3]='unexpected';write(p/'tracker/TRACKER_RECEIPT.json',tracker)
 if mode=='tracker_range':tracker['updatedRange']="'Math Puzzles'!A1:D1";write(p/'tracker/TRACKER_RECEIPT.json',tracker)
 if mode=='gate_missing':gate['workflow'].pop('compile_note.py');write(p/'FINAL_REVIEW_GATE.json',gate)
 if mode=='stale_intent':saved['metadata_sha256']='0'*64;write(p/'PR_BRANCH_INTENT.json',saved)
 def git(*args,data=None):
  events.append(args[0])
  if args==('branch','--show-current'):return b'main\n'
  if args[0]=='rev-list':return (commit+' '+('b'*40 if mode=='parent' else m.ORIGINAL)+'\n').encode()
  if args[0]=='diff-tree':return ('\n'.join(sorted(files)+(['foreign/file'] if mode=='paths' else []))+'\n').encode()
  if args[0]=='show':return b'changed' if mode=='bytes' else files[args[1].split(':',1)[1]]
  if args[0]=='ls-remote':return (state['remote']+' refs/heads/'+m.BRANCH+'\n').encode()
  if args[0]=='push':
   state['pushes']+=1;state['remote']=commit;state['head']=commit
   if mode=='push_lost' and first['value']:first['value']=False;raise RuntimeError('fake accepted push with lost response')
   return b''
  raise RuntimeError('Forbidden unmocked Git operation '+repr(args))
 m.git=git;m.pr=lambda:{'headRefOid':state['head'],'headRefName':m.BRANCH,'state':'OPEN','body':state['body']};m.subprocess=types.SimpleNamespace(run=lambda *a,**kw:(_ for _ in ()).throw(RuntimeError('Unexpected external body process')))
 outcomes=[]
 for n in range(2 if mode in ('exact','push','push_lost') else 1):
  try:quiet(m.main);outcomes.append(True)
  except Exception as e:outcomes.append(type(e).__name__+': '+str(e))
 if mode in ('exact','push'):need(outcomes==[True,True] and state['pushes']==(mode=='push'),'PR main idempotence')
 elif mode=='push_lost':need(outcomes[0] is not True and outcomes[1] is True and state['pushes']==1,'uncertain push retry')
 else:need(outcomes[0] is not True and state['pushes']==0 and not (p/'PR_BRANCH_RECEIPT.json').exists(),'bad PR completed '+mode)
 return {'case':label,'outcomes':outcomes,'pushes':state['pushes'],'edits':state['edits'],'read_commands':sorted(set(events)),'desired_paths':len(files)}
for mode in ('exact','push','push_lost','api_lag','unknown_body','parent','paths','bytes','wrong_public_id','tracker_cell','tracker_range','gate_missing','stale_intent'):pr_results.append(pr_case(mode,mode))
report={'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tracker_whole_main':tracker_results,'public_whole_main':public_results,'pr_whole_main':pr_results,'limits':'All mutations are in-memory server events or isolated copied receipts. No actual external/Git/index/ref mutation. PR main tests cover saved-intent and completed-receipt branches, pinned 13-file byte trees, non-force push/retry and API lag; final-body edit/lost-response paths are also exercised by the copied workflow worker, not falsely certified as live operations.'}
(R/'EXTERNAL_WORKFLOW_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','tracker':len(tracker_results),'public':len(public_results),'PR':len(pr_results)}))
