#!/usr/bin/env python3
"""R3 current-postmerge review. R2 scaffolding and its broad baseline cases reused explicitly; new casefold/all-cell/whitespace, fallback-identity and individual15-blob perturbations added. All external/Git operations mocked; no production integration."""
import os,sys
sys.dont_write_bytecode=True
from pathlib import Path
R=Path(__file__).resolve().parent;A=R.parents[1];S=R/'ignored_scratch/current_postmerge';S.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(R/'ignored_scratch/tmp');os.environ['PYTHONDONTWRITEBYTECODE']='1'
import contextlib,copy,hashlib,importlib.util,io,json,shutil,types

def need(v,m):
 if not v:raise RuntimeError(m)
def load(p):
 s=importlib.util.spec_from_file_location('r2_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def save(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2)+'\n')
def sources():
 p=S/'source/program/audits/pr1268_10900050/publication';p.mkdir(parents=True,exist_ok=True)
 for name in ['append_tracker.py','build_package.py','check_public_downloads.py','compile_note.py','prepare_package.py','update_pr_publication.py','workflow_regression.py','verification/verify.py','zenodo-deposit.json']:
  q=p/name;q.parent.mkdir(exist_ok=True);shutil.copyfile(A/'publication'/name,q)
 c=p.parents[2]/'publication_coordinators';c.mkdir(exist_ok=True)
 for n in ['pr1268.py','verify_pr1268_merge.py']:shutil.copyfile(A.parents[1]/'publication_coordinators'/n,c/n)
 return p,c/'verify_pr1268_merge.py'
def probe(w,operative,case):
 root=S/(str(sys.flags.optimize)+'_'+case)
 if root.exists():shutil.rmtree(root)
 root.mkdir()
 f=w.fixture(root/'fixture')
 with contextlib.redirect_stdout(io.StringIO()):
  pub,tracker,_=w.publication_and_tracker_controls(f)
  pub['doi_resolution']={'status':'resolved','http_status':200};save(f['pub']/'PUBLICATION_RECEIPT.json',pub)
  w.update_controls(f,pub,tracker)
 u=load(f['pub']/'update_pr_publication.py');t=load(f['pub']/'append_tracker.py')
 if case=='doi_fallback_valid':pub['doi_resolution']={'status':'not_checked'};save(f['pub']/'DOI_INSPECT.json',{**pub,'doi_resolution':{'status':'resolved','http_status':200}})
 if case in {'doi_unresolved','doi_wrong_status'}:
  pub['doi_resolution']={'status':'not_checked'};save(f['pub']/'DOI_INSPECT.json',{**pub,'doi_resolution':{'status':'resolved','http_status':201}if case=='doi_wrong_status'else{'status':'not_resolved','http_status':404}})
 if case=='doi_fallback_wrong_identity':
  pub['doi_resolution']={'status':'not_checked'};save(f['pub']/'DOI_INSPECT.json',{**pub,'id':124,'doi_resolution':{'status':'resolved','http_status':200}})
 save(f['pub']/'PUBLICATION_RECEIPT.json',pub)
 files,_,_=u.desired_files(f['build'],pub,tracker,f['snapshot']);body=(f['pub']/'PR_BODY_FINAL.md').read_text();wanted=u.expected_identity(pub,tracker,files,body)
 for n in ['PR_BRANCH_INTENT.json','PR_BRANCH_RECEIPT.json']:
  old=json.loads((f['pub']/n).read_text());old.update(wanted);save(f['pub']/n,old)
 if case=='saved_body_unverified':old=json.loads((f['pub']/'PR_BRANCH_RECEIPT.json').read_text());old['body_readback_verified']=False;save(f['pub']/'PR_BRANCH_RECEIPT.json',old)
 if case=='saved_remote_unverified':old=json.loads((f['pub']/'PR_BRANCH_RECEIPT.json').read_text());old['remote_readback_verified']=False;save(f['pub']/'PR_BRANCH_RECEIPT.json',old)
 events=[];head='a'*40;merge='c'*40;first='d'*40
 def git(*args,data=None):
  events.append({'git':list(args)})
  if args==('branch','--show-current'):return b'wrong\n'if case=='checkout_wrong'else b'main\n'
  if args[0]=='rev-list':
   if args[-1]==merge:
    parents=[first,head]if case!='merge_parent_wrong'else[head,first]
    if case=='merge_single_parent':parents=[head]
    if case=='merge_three_parents':parents=[first,head,'e'*40]
    return (' '.join([merge]+parents)+'\n').encode()
   return (head+' '+u.ORIGINAL+'\n').encode()
  if args[0]=='diff-tree':return ('\n'.join(sorted(files))+'\n').encode()
  if args[0]=='show':
   n=args[1].split(':',1)[1]
   if case.startswith('individual_merged_blob_') and args[1].startswith(merge+':') and n==sorted(files)[int(case.rsplit('_',1)[1])]:return b'R3 individual merged blob corruption'
   return b'R2 changed'if case=='merged_bytes_wrong'and args[1].startswith(merge+':')else files[n]
  if args[0]in{'fetch','update-ref'}:return b''
  raise RuntimeError('Unexpected mock Git '+repr(args))
 u.git=git
 tabs=[{'properties':{'sheetId':t.GID,'title':'Math Puzzles'}}]
 if case=='wrong_gid_same_title':tabs=[{'properties':{'sheetId':t.GID,'title':'Renamed'}},{'properties':{'sheetId':999,'title':'Math Puzzles'}}]
 if case=='missing_gid':tabs=[{'properties':{'sheetId':999,'title':'Math Puzzles'}}]
 if case=='duplicate_designated_gid':tabs=tabs+copy.deepcopy(tabs)
 if case=='wrong_title':tabs[0]['properties']['title']='Other'
 rows=[['Original Problem','Solution Chat URL','DOI','Notes'],copy.deepcopy(tracker['row'])]
 if case=='bad_headers':rows[0][1]='Chat URL'
 if case=='missing_row':rows=rows[:1]
 if case.startswith('wrong_cell_'):rows[1][int(case[-1])]='R2 WRONG'
 ids={'duplicate_bare_doi':pub['doi'],'duplicate_doi_url':pub['doi_url'],'duplicate_numeric':'10900050','duplicate_AMR':'AMR-108-0050','duplicate_PR':'https://github.com/AlecKriebel/Math/pull/1268'}
 if case in ids:rows.append([ids[case],'','',''])
 extra={'mixed_AMR_notes':['','','','aMr-108-0050'],'mixed_PR_B':['','HTTPS://GITHUB.COM/ALECKRIEBEL/MATH/PULL/1268','',''],'trimmed_bare_DOI_C':['','','  '+pub['doi']+'\t',''],'trimmed_DOI_URL_B':['','  '+pub['doi_url'].upper()+'  ','',''],'numeric_notes':['','','','See 10900050 here']}
 if case in extra:rows.append(extra[case])
 if case=='unrelated_safe':rows.append(['AMR-108-0051','','10.5281/zenodo.999','Unrelated'])
 if case=='range_wrong':tracker['updatedRange']="'Math Puzzles'!A3:D3";save(f['pub']/'tracker/TRACKER_RECEIPT.json',tracker)
 def call(parts,params,body=None):
  events.append({'gws':parts,'params':params})
  if parts==['spreadsheets','get']:return {'sheets':copy.deepcopy(tabs)}
  if parts==['spreadsheets','values','get']:return {'values':copy.deepcopy(rows)}
  raise RuntimeError('Unexpected service mutation')
 t.call=call
 m=load(operative);m.A=f['audit'];m.P=f['pub'];m.PROGRAM=f['audit'].parents[1];m.REPO=root
 real_run=m.runpy.run_path
 def run_path(path):
  if Path(path).name=='update_pr_publication.py':return u.__dict__
  if Path(path).name=='append_tracker.py':return t.__dict__
  return real_run(path)
 m.runpy=types.SimpleNamespace(run_path=run_path)
 live={'state':'MERGED','headRefOid':head,'headRefName':u.BRANCH,'mergeCommit':{'oid':merge},'mergedAt':'2026-10-18T00:00:00Z','body':body,'url':'https://github.com/AlecKriebel/Math/pull/1268'}
 for label,key,val in [('live_open','state','OPEN'),('live_head_wrong','headRefOid','e'*40),('live_branch_wrong','headRefName','other'),('live_body_wrong','body','outside body')]:
  if case==label:live[key]=val
 def external(args,**kw):events.append({'gh':args});return json.dumps(live)
 m.subprocess=types.SimpleNamespace(check_output=external)
 public=json.loads((f['pub']/'PUBLIC_DOWNLOAD_VERIFICATION.json').read_text())
 for label,key,val in [('public_false','all_supplied_metadata_exact',False),('public_identity_false','public_record_identity_verified',False),('public_id_wrong','id',124),('public_doi_wrong','doi','10.5281/zenodo.124')]:
  if case==label:public[key]=val
 save(f['pub']/'PUBLIC_DOWNLOAD_VERIFICATION.json',public)
 # Rebind current public receipt hash so the case reaches postmerge's own check.
 for n in ['PR_BRANCH_INTENT.json','PR_BRANCH_RECEIPT.json']:
  x=json.loads((f['pub']/n).read_text());x['public_verification_receipt_sha256']=hashlib.sha256((f['pub']/'PUBLIC_DOWNLOAD_VERIFICATION.json').read_bytes()).hexdigest();save(f['pub']/n,x)
 state={'current_pr':1268,'completed_prs':[],'publications':[],'eligible_count':50};save(m.PROGRAM/'PROGRAM_STATE.json',state)
 try:
  with contextlib.redirect_stdout(io.StringIO()):m.main()
  accepted=True;error=None
 except (RuntimeError,ValueError,FileNotFoundError,KeyError)as e:accepted=False;error=type(e).__name__+': '+str(e)
 after=json.loads((m.PROGRAM/'PROGRAM_STATE.json').read_text());readback=f['pub']/'tracker/POSTMERGE_READBACK.json'
 observed=json.loads(readback.read_text()).get('observed_sheet_properties')if readback.exists()else None
 return {'case':case,'accepted':accepted,'error':error,'state_current_pr':after['current_pr'],'fresh_sheet_properties_read':any(e.get('gws')==['spreadsheets','get']for e in events),'observed_sheet_properties':observed,'events':events}
def main():
 source,operative=sources();w=load(source/'workflow_regression.py')
 cases=['baseline','doi_fallback_valid','wrong_gid_same_title','missing_gid','duplicate_designated_gid','wrong_title','bad_headers','missing_row',*[f'wrong_cell_{i}'for i in range(4)],'duplicate_bare_doi','duplicate_doi_url','duplicate_numeric','duplicate_AMR','duplicate_PR','range_wrong','checkout_wrong','merge_parent_wrong','merge_single_parent','merge_three_parents','merged_bytes_wrong','live_open','live_head_wrong','live_branch_wrong','live_body_wrong','saved_body_unverified','saved_remote_unverified','public_false','public_identity_false','public_id_wrong','public_doi_wrong','doi_unresolved','doi_wrong_status']
 newcases=['mixed_AMR_notes','mixed_PR_B','trimmed_bare_DOI_C','trimmed_DOI_URL_B','numeric_notes','unrelated_safe','doi_fallback_wrong_identity']+[f'individual_merged_blob_{i}'for i in range(15)]
 cases=(cases+newcases)if sys.flags.optimize==0 else ['baseline','doi_fallback_valid',*newcases]
 out=[probe(w,operative,c)for c in cases]
 unexpected=[x['case']for x in out if x['accepted']!=(x['case']in{'baseline','doi_fallback_valid','unrelated_safe'})or x['state_current_pr']!=(1271 if x['case']in{'baseline','doi_fallback_valid','unrelated_safe'}else 1268)]
 for x in out:
  if x['accepted']:need(x['fresh_sheet_properties_read']and x['observed_sheet_properties']=={'sheetId':1254632077,'title':'Math Puzzles'},'successful observed identity missing')
 receipt={'at_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'optimization':sys.flags.optimize,'operative_sha256':hashlib.sha256(operative.read_bytes()).hexdigest(),'source_equals_actual_current':operative.read_bytes()==(A.parents[1]/'publication_coordinators/verify_pr1268_merge.py').read_bytes(),'cases':out,'unexpected':unexpected,'fixture_scope':'Existing synthetic builder and R2 broad baseline scaffold reused; R3 extra independently selected action-time identity/fallback/each15blob cases, actual current operative module, no actual production integration. All external/Git operations mocked.'}
 save(R/('CURRENT_POSTMERGE_'+str(sys.flags.optimize)+'.json'),receipt);need(not unexpected,'Unexpected fresh cases '+repr(unexpected));print(json.dumps({'optimization':sys.flags.optimize,'cases':len(out),'unexpected':unexpected}))
if __name__=='__main__':main()
