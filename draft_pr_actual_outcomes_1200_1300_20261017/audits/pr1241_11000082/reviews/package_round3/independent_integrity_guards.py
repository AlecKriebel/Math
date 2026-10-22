from pathlib import Path
import contextlib,copy,datetime,hashlib,importlib.util,io,json,shutil,types
R=Path(__file__).resolve().parent;F=json.loads((R/'INPUT_FREEZE.json').read_text());A=Path(F['root']);W=R/'scratch_local/integrity';W.mkdir(exist_ok=True)
def load(label,path):
 s=importlib.util.spec_from_file_location('ind_integrity_'+label,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def need(c,m):
 if not c:raise RuntimeError(m)
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def quiet(f):
 with contextlib.redirect_stdout(io.StringIO()):return f()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Coupled outer-manifest rewrites must not bypass nested immutable bindings.
z=W/'archive';shutil.copytree(A/'publication/verification',z,dirs_exist_ok=True);v=load('verifier',A/'publication/verification/verify.py');v.ROOT=z;outer_original=(z/'MANIFEST.json').read_bytes();cases=[]
def rehash():
 d=json.loads((z/'MANIFEST.json').read_text())
 for e in d['files']:
  b=(z/e['path']).read_bytes();e['bytes']=len(b);e['sha256']=hashlib.sha256(b).hexdigest()
 write(z/'MANIFEST.json',d)
def reject(label,action,restore):
 action()
 try:quiet(v.main)
 except Exception as e:cases.append({'case':label,'rejected':True,'error':str(e)})
 else:raise RuntimeError('Invalid archive accepted '+label)
 restore();(z/'MANIFEST.json').write_bytes(outer_original)
p=z/'priority/independent/CROSS_REPORT.md';orig=p.read_bytes()
reject('payload_and_outer_changed',lambda:(p.write_bytes(orig+b' altered'),rehash()),lambda:p.write_bytes(orig))
reg=json.loads((z/'provenance/CURRENT_PR1241_CONTEXT.json').read_text())['authored_freezes'];item=next(x for x in reg if x['path']=='priority/independent/CROSS_MANIFEST.json');mf=z/item['path'];mb=mf.read_bytes()
def coupled():
 p.write_bytes(orig+b' altered');d=json.loads(mb)
 for e in d[item['entries_key']]:
  if e[item['path_key']]=='CROSS_REPORT.md':e['bytes']=len(p.read_bytes());e['sha256']=sha(p)
 write(mf,d);rehash()
reject('payload_nested_and_outer_changed_external_registry_unchanged',coupled,lambda:(p.write_bytes(orig),mf.write_bytes(mb)))
p=z/'provenance/SUBMITTED_SNAPSHOT.json';orig=p.read_bytes()
def wrong_blob():
 d=json.loads(orig);d['files'][0]['blob']='0'*40;write(p,d);rehash()
reject('submitted_Git_blob_wrong_with_outer_rehashed',wrong_blob,lambda:p.write_bytes(orig))
p=z/'unlisted.txt';reject('unlisted_member',lambda:p.write_text('unlisted'),lambda:p.unlink())
# True source/PDF/compile/QA coupling using the actual six-page PDF.
b=load('builder',A/'publication/build_package.py');doc=W/'document';shutil.copytree(A/'publication',doc,dirs_exist_ok=True);b.ROOT=doc;shutil.copyfile(A/'CURRENT_PR1241_CONTEXT.json',doc.parent/'CURRENT_PR1241_CONTEXT.json');shutil.copyfile(A/'PRIORITY_ADJUDICATION.json',doc.parent/'PRIORITY_ADJUDICATION.json');baseline=b.document_bindings();doc_cases=[]
for label,filename in [('source','manuscript/main.tex'),('PDF','output/pdf/main.pdf'),('compile_receipt','COMPILE_RECEIPT.json'),('layout_receipt','LAYOUT_VERIFICATION.json')]:
 p=doc/filename;orig=p.read_bytes()
 if label in ('source','PDF'):p.write_bytes(orig+b' altered')
 else:
  d=json.loads(orig)
  if label=='compile_receipt':d['source_date_epoch']='0'
  else:d['page_indices_inspected']=[1,2,3,4,5]
  write(p,d)
 try:b.document_bindings()
 except Exception as e:doc_cases.append({'case':label,'rejected':True,'error':str(e)})
 else:raise RuntimeError('Stale document accepted '+label)
 p.write_bytes(orig)
need(b.document_bindings()==baseline,'document fixture restored')
# Actual operative release authenticator against every frozen member, with an
# explicitly synthetic future gate. It uses all real current artifact/helper bytes.
q=W/'auth_audit';q.mkdir(exist_ok=True)
for e in F['files']:
 p=q/e['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A/e['path'],p)
P=q/'publication';review=q/'reviews/synthetic_gate';review.mkdir(parents=True);(review/'REPORT.md').write_text('Synthetic gate test; not a publication authorization.');write(review/'VERDICT.json',{'status':'CLEAN'});shutil.copyfile(R/'INPUT_FREEZE.json',review/'INPUT_FREEZE.json');u=load('PRgate',P/'update_pr_publication.py');gate={'schema':'math-preprint-final-review-gate-v1','pr':1241,'problem_id':11000082,'original_head':u.ORIGINAL,'status':'pass','workflow':{n:sha(P/n) for n in u.REQUIRED_WORKFLOW},'latest_review':{'status':'CLEAN','report':'../reviews/synthetic_gate/REPORT.md','report_sha256':sha(review/'REPORT.md'),'verdict':'../reviews/synthetic_gate/VERDICT.json','verdict_sha256':sha(review/'VERDICT.json'),'input_freeze_sha256':sha(review/'INPUT_FREEZE.json')},'pdf_sha256':sha(P/'Johnson_Filtration_Multiplicity_Note_v1.0.pdf'),'verification_zip_sha256':sha(P/'Johnson_Filtration_Multiplicity_Verification_v1.0.zip'),'metadata_sha256':sha(P/'zenodo-deposit.json'),'source_sha256':sha(P/'manuscript/main.tex')};write(P/'FINAL_REVIEW_GATE.json',gate);c=load('actual_coordinator',Path(F['external_readonly_inputs'][2]['path']));c.A=q;c.P=P;need(c.authenticate_release()==gate,'whole release authenticator baseline');auth_cases=[]
for label,rel in [('metadata','publication/zenodo-deposit.json'),('source','publication/manuscript/main.tex'),('release_pdf','publication/Johnson_Filtration_Multiplicity_Note_v1.0.pdf'),('archive','publication/Johnson_Filtration_Multiplicity_Verification_v1.0.zip'),('current8','current_edition/AUDIT.md'),('review_family','priority/independent/CROSS_REPORT.md'),('post_build_R2_receipt','R2_FIX_RECEIPT.json'),('operative_helper','publication/append_tracker.py')]:
 p=q/rel;orig=p.read_bytes();p.write_bytes(orig+b' drift')
 try:c.authenticate_release()
 except Exception as e:auth_cases.append({'case':label,'rejected':True,'error':str(e)})
 else:raise RuntimeError('Release drift accepted '+label)
 p.write_bytes(orig)
need(c.authenticate_release()==gate,'restored release authenticates')
# Final-body step: real helper state machine, independent fake server, pre/post
# head guards, outside edit protection, idempotence and accepted lost response.
u.ROOT=W/'body';u.ROOT.mkdir(exist_ok=True);write(u.ROOT/'FINAL_REVIEW_GATE.json',{});(u.ROOT/'PR_BODY_FINAL.md').write_text('final');body_state={'head':'a'*40,'remote':'a'*40,'body':'original','edits':0,'lost':False};u.pr=lambda:{'state':'OPEN','headRefName':u.BRANCH,'headRefOid':body_state['head'],'body':body_state['body']};u.git=lambda *a,**kw:(body_state['remote']+' remote\n').encode()
def edit(args,**kw):
 body_state['edits']+=1;body_state['body']='final';return types.SimpleNamespace(returncode=1 if body_state['lost'] else 0,stderr='fake lost body response' if body_state['lost'] else '')
u.subprocess=types.SimpleNamespace(run=edit);initial=hashlib.sha256(b'original').hexdigest();u.synchronize_pr_body('a'*40,'final',initial);u.synchronize_pr_body('a'*40,'final',initial);need(body_state['edits']==1,'body idempotency');body_state.update(body='original',lost=True)
try:u.synchronize_pr_body('a'*40,'final',initial)
except RuntimeError:pass
else:raise RuntimeError('lost body response wrongly complete')
body_state['lost']=False;u.synchronize_pr_body('a'*40,'final',initial);need(body_state['edits']==2,'body lost-response duplicated')
body_cases=[]
for label,change in [('unknown_body',{'body':'external'}),('API_lag',{'head':'b'*40}),('remote_drift',{'remote':'b'*40})]:
 body_state.update(head='a'*40,remote='a'*40,body='original',**{})
 body_state.update(change);before=body_state['edits']
 try:u.synchronize_pr_body('a'*40,'final',initial)
 except RuntimeError:body_cases.append(label)
 else:raise RuntimeError('unsafe body edit '+label)
 need(body_state['edits']==before,'body mutation before refusal')
report={'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'coupled_archive_controls':cases,'real_document_controls':doc_cases,'actual_release_authenticator_full_frozen_inputs':314,'release_controls':auth_cases,'body_controls':body_cases,'body_idempotence_lost_response':True,'limits':'Only synthetic future gate/receipts in copies; no actual final review gate created and no real Git/network/application operation. Coordinated rewriting of all outside anchors is outside self-contained integrity authentication.'};(R/'INTEGRITY_GUARD_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','archive_controls':len(cases),'document_controls':len(doc_cases),'release_controls':len(auth_cases)}))
