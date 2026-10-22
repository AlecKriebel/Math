"""PR1280 coordinator. The actual shared kit verifier is made strict before use.
Fresh exact same-ID inspection precedes publication; the kit repeats strict
verification before its POST. Uncertain attempts reconcile read-only.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,runpy,subprocess,sys,zipfile
REPO=Path('/Users/alec/Documents/Math')
PROGRAM=Path(__file__).resolve().parents[1]
A=PROGRAM/'audits/pr1280_30003587';P=A/'publication'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,m):
 if not c:raise RuntimeError(m)
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def write_intent(p,d):
 try:
  with p.open('x') as stream:stream.write(json.dumps(d,indent=2)+'\n')
 except FileExistsError:raise RuntimeError('Prior attempt intent exists; reconcile read-only')
def authenticate_release():
 g=json.loads((P/'FINAL_REVIEW_GATE.json').read_text());runpy.run_path(str(P/'update_pr_publication.py'))['validate_workflow_gate'](g)
 for n,k in [('Diagonal_Actions_Strong_Approximate_Innerness_Note_v1.0.pdf','pdf_sha256'),('Diagonal_Actions_Strong_Approximate_Innerness_Verification_v1.0.zip','verification_zip_sha256'),('zenodo-deposit.json','metadata_sha256'),('manuscript/main.tex','source_sha256')]:require(digest(P/n)==g[k],'Reviewed release drift '+n)
 f=(P/g['latest_review']['input_freeze']).resolve();require(digest(f)==g['latest_review']['input_freeze_sha256'],'Latest input-freeze anchor differs');freeze=json.loads(f.read_text())
 for e in freeze['files']+freeze['external_readonly_inputs']:
  p=Path(e['path']);p=p if p.is_absolute() else A/p;b=p.read_bytes();require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'Frozen input drift '+str(p))
 current_documents=runpy.run_path(str(P/'build_package.py'))['document_bindings']()
 require(json.loads((P/'BUILD_RECEIPT.json').read_text())['document_bindings']==current_documents,'Built artifact current document/context/gate bindings differ')
 context=runpy.run_path(str(P/'prepare_package.py'))['load_context']()
 manifest=json.loads((P/'zenodo-deposit.json').read_text())
 require(set(manifest)=={'metadata','files'} and manifest['metadata']==context['metadata'] and manifest['files']==[{'path':'Diagonal_Actions_Strong_Approximate_Innerness_Note_v1.0.pdf'},{'path':'Diagonal_Actions_Strong_Approximate_Innerness_Verification_v1.0.zip'}],'Exact two-file metadata manifest required')
 with zipfile.ZipFile(P/'Diagonal_Actions_Strong_Approximate_Innerness_Verification_v1.0.zip') as z:
  require(z.read('manuscript/main.tex')==(P/'manuscript/main.tex').read_bytes(),'Archive source drift')
  for n in sorted({'ACCEPTANCE.json','CHECK_RESULTS.json','EDITORIAL_CHANGE_MAP.json','INDEPENDENT_AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCE_METADATA.json','SOURCE_VERIFICATION.md'}):require(z.read('current_edition/'+n)==(A/'current_edition'/n).read_bytes(),'Current edition drift '+n)
  require(z.read('provenance/SUBMITTED_SNAPSHOT.json')==(A/'SUBMITTED_SNAPSHOT.json').read_bytes(),'Archive original snapshot drift')
  require(z.read('provenance/CURRENT_PR1280_CONTEXT.json')==(A/'CURRENT_PR1280_CONTEXT.json').read_bytes(),'Archive current context drift')
  if context['edition_mode']=='documented_correction':require(z.read('provenance/CURRENT_EDITION_CORRECTION.json')==(A/'CURRENT_EDITION_CORRECTION.json').read_bytes(),'Archive correction drift')
  for n in ['COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json']:require(z.read('provenance/'+n)==(P/n).read_bytes(),'Archive current assurance drift '+n)
 return g

def live_preflight():
 s=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text());l=json.loads(subprocess.check_output(['gh','pr','view','1280','--repo','AlecKriebel/Math','--json','state,isDraft,headRefOid,headRefName,baseRefName,body'],text=True))
 require(l.get('baseRefName')=='main' and l['state']=='OPEN' and l['isDraft'] is True and l['headRefOid']==s['head'] and l['headRefName']==s['branch'] and hashlib.sha256(l['body'].encode()).hexdigest()==s['body_sha256'],'Live original draft/head/body changed; no deposit mutation')
 remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/'+s['branch']],cwd=REPO,text=True).split();require(remote and remote[0]==s['head'],'Live branch changed; no deposit mutation')
 t=runpy.run_path(str(P/'append_tracker.py'));m=t['call'](['spreadsheets','get'],{'spreadsheetId':t['SID'],'fields':'sheets.properties'});tabs=[e['properties'] for e in m.get('sheets',[]) if e.get('properties',{}).get('sheetId')==t['GID']];require(len(tabs)==1 and tabs[0].get('title')=='Math Puzzles','Tracker designated ID/title changed')
 rows=t['call'](['spreadsheets','values','get'],{'spreadsheetId':t['SID'],'range':"'Math Puzzles'!A:D",'valueRenderOption':'UNFORMATTED_VALUE'}).get('values',[])
 require(rows and rows[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'Tracker headers changed')
 known=None
 for filename in ['PUBLICATION_RECEIPT.json','STAGE_RECEIPT.json','STAGE_INSPECT.json']:
  if (P/filename).exists():
   saved=json.loads((P/filename).read_text());identifier=saved.get('id');require(type(identifier) is int and identifier>0,'Invalid saved preflight deposit ID');candidate={'doi':'10.5281/zenodo.'+str(identifier),'doi_url':'https://doi.org/10.5281/zenodo.'+str(identifier)}
   require(known is None or known==candidate,'Saved preflight deposit identities disagree');known=candidate
 require(not any(t['row_has_problem_identity'](row,known) for row in rows),'Existing problem/known DOI row; reconcile before deposit mutation')

def install_exact_verifier(kit):
 if getattr(kit,'pr1280_exact_verifier',False):return kit
 original=kit.verify
 def exact_verify(deposit,metadata,files):
  changes=original(deposit,metadata,files)
  if changes:raise kit.DepositError('Exact supplied metadata required; normalization refused before publication')
  return []
 kit.verify=exact_verify;kit.pr1280_exact_verifier=True;return kit

def load_exact_kit():
 require(digest(REPO/'zenodo_deposit_tool/zenodo.py')=='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca','Pinned shared kit drift');spec=importlib.util.spec_from_file_location('pr1280_exact_zenodo_kit',REPO/'zenodo_deposit_tool/zenodo.py');kit=importlib.util.module_from_spec(spec);spec.loader.exec_module(kit);return install_exact_verifier(kit)

def validate_summary(d,kit,known_id=None,state=None):
 meta,files=kit.load_manifest(P/'zenodo-deposit.json');require(d.get('environment')=='production' and d.get('title')==meta['title'],'Deposit summary identity differs')
 require(d.get('files')==[{'name':f['name'],'size':f['size'],'sha256':f['sha256']} for f in files],'Deposit summary files differ')
 require('metadata_normalizations' in d and d['metadata_normalizations']==[],'Exact inspected metadata required')
 require(type(d.get('id')) is int and d['id']>0 and (known_id is None or d['id']==known_id),'Deposit ID differs')
 require(d.get('state') in {'ready_to_publish','published'} and (state is None or d['state']==state),'Deposit state differs')
 if d['state']=='published':runpy.run_path(str(P/'append_tracker.py'))['validate_publication_identity'](d,meta['title'])

def call_kit(kit,command,known_id=None,check_doi=False):return kit.run(argparse.Namespace(command=command,manifest=P/'zenodo-deposit.json',sandbox=False,confirm_id=known_id,check_doi=check_doi))
def known_stage_id(kit):
 s=json.loads((P/'STAGE_RECEIPT.json').read_text());validate_summary(s,kit,state='ready_to_publish');_,state=kit.local_state((P/'zenodo-deposit.json').resolve(),'production');require(state and state['id']==s['id'],'Kit draft and stage receipt differ');return s['id']

def execute(action,kit=None):
 require(action in {'stage','inspect','publish','inspect-doi'},'Unsupported action');g=authenticate_release();kit=load_exact_kit() if kit is None else install_exact_verifier(kit)
 if action=='stage':
  require(not any((P/n).exists() for n in ['STAGE_RECEIPT.json','STAGE_INTENT.json','PUBLISH_INTENT.json','PUBLICATION_RECEIPT.json']),'Earlier stage/publication state exists; reconcile saved ID read-only')
  _,saved=kit.local_state((P/'zenodo-deposit.json').resolve(),'production');require(not saved,'Kit draft exists; inspect saved ID read-only')
  live_preflight();require(authenticate_release()==g,'Release gate changed during preflight')
  write_intent(P/'STAGE_INTENT.json',{'metadata_sha256':g['metadata_sha256'],'pdf_sha256':g['pdf_sha256'],'verification_zip_sha256':g['verification_zip_sha256'],'policy':'One stage attempt; uncertain creation requires saved-ID/account read-only reconciliation, never blind restaging'})
  d=call_kit(kit,'stage');validate_summary(d,kit,state='ready_to_publish');write(P/'STAGE_RECEIPT.json',d);return d
 if action in {'inspect','inspect-doi'}:
  d=call_kit(kit,'inspect',check_doi=action=='inspect-doi');validate_summary(d,kit)
  if (P/'STAGE_RECEIPT.json').exists():require(d['id']==known_stage_id(kit),'Inspection changed known ID')
  else:
   _,saved=kit.local_state((P/'zenodo-deposit.json').resolve(),'production');require(saved and saved['id']==d['id'],'Inspection has no known saved same-ID state')
   if d['state']=='ready_to_publish':write(P/'STAGE_RECEIPT.json',d)
  write(P/('DOI_INSPECT.json' if action=='inspect-doi' else 'STAGE_INSPECT.json'),d);return d
 known=known_stage_id(kit)
 # Fresh server inspection; a saved or stale inspect receipt is never authority.
 d=call_kit(kit,'inspect');validate_summary(d,kit,known);write(P/'STAGE_INSPECT.json',d)
 receipt=P/'PUBLICATION_RECEIPT.json';intent=P/'PUBLISH_INTENT.json'
 if d['state']=='published':
  if receipt.exists():
   old=json.loads(receipt.read_text());validate_summary(old,kit,known,'published');require(old['doi']==d['doi'],'Saved DOI differs')
  else:write(receipt,d)
  return d
 require(not receipt.exists(),'Saved publication not confirmed by server; reconcile read-only');require(not intent.exists(),'Prior attempt unresolved; inspect known ID, never retry blindly');validate_summary(d,kit,known,'ready_to_publish');live_preflight()
 require(authenticate_release()==g,'Release gate changed during preflight')
 write_intent(intent,{'id':known,'metadata_sha256':g['metadata_sha256'],'pdf_sha256':g['pdf_sha256'],'verification_zip_sha256':g['verification_zip_sha256'],'inspection_sha256':digest(P/'STAGE_INSPECT.json'),'policy':'One attempt; reconcile known ID read-only on uncertain outcome'})
 # kit.run performs another GET and our strict verify BEFORE its publish POST.
 d=call_kit(kit,'publish',known);validate_summary(d,kit,known,'published');write(receipt,d);return d

def main():
 require(len(sys.argv)==2,'Expected one action');d=execute(sys.argv[1]);print(json.dumps({k:d[k] for k in ['id','state','doi','doi_url','record_url','metadata_normalizations','doi_resolution','receipt_saved'] if k in d},indent=2))
if __name__=='__main__':main()
