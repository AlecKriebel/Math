#!/usr/bin/env python3
"""Root repair reproduction of sealed R2 identity variants at the preflight and append action times.
Actual operative bodies; synthetic saved snapshot/publication, mocked services.
"""
import os,sys
sys.dont_write_bytecode=True
from pathlib import Path
R=Path(__file__).resolve().parent;A=R.parents[1];S=R/'scratch/tracker_identity';S.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(S);os.environ['PYTHONDONTWRITEBYTECODE']='1'
import contextlib,copy,hashlib,importlib.util,io,json,shutil,types

def load(p):
 sp=importlib.util.spec_from_file_location('r2_id_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def save(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def probe(kind,identifier):
 root=S/(str(sys.flags.optimize)+'_'+kind+'_'+identifier)
 if root.exists():shutil.rmtree(root)
 root.mkdir(exist_ok=True);P=root/'publication';P.mkdir(exist_ok=True)
 for n in ['append_tracker.py','zenodo-deposit.json']:shutil.copyfile(A/'publication'/n,P/n)
 cpath=root/'pr1268.py';shutil.copyfile(A.parents[1]/'publication_coordinators/pr1268.py',cpath)
 t=load(P/'append_tracker.py');c=load(cpath);c.A=root;c.P=P
 context=json.loads((A/'CURRENT_PR1268_CONTEXT.json').read_text());meta=context['metadata'];events=[]
 pub={'environment':'production','state':'published','metadata_normalizations':[],'id':73123456,'doi':'10.5281/zenodo.73123456','doi_url':'https://doi.org/10.5281/zenodo.73123456','record_url':'https://zenodo.org/records/73123456','url':'https://doi.org/10.5281/zenodo.73123456','title':meta['title']};save(P/'PUBLICATION_RECEIPT.json',pub);save(P/'FINAL_REVIEW_GATE.json',{'synthetic_fixture_only':True})
 ids={'AMR':'AMR-108-0050','numeric':'10900050','PR':'https://github.com/AlecKriebel/Math/pull/1268','bareDOI':pub['doi'],'DOIURL':pub['doi_url'],'AMRlower':'amr-108-0050','unrelated':'Unrelated problem 42','exact':'EXACT_INTENDED_ROW'}
 rows=[['Original Problem','Solution Chat URL','DOI','Notes'],[ids[identifier],'','','']]
 row=t.expected_row # actual function; runpy dependency below returns actual current context.
 def call(parts,params,body=None):
  events.append({'service':parts,'range':params.get('range')})
  if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':t.GID,'title':'Math Puzzles'}}]}
  if parts==['spreadsheets','values','get']:return {'values':copy.deepcopy(rows if params['range']=="'Math Puzzles'!A:D"else[rows[-1]])}
  if parts==['spreadsheets','values','append']:
   rows.append(copy.deepcopy(body['values'][0]));return {'updates':{'updatedRange':"'Math Puzzles'!A3:D3",'updatedRows':1,'updatedColumns':4}}
  raise RuntimeError('unmocked service')
 t.call=call
 def run_path(p):
  if Path(p).name=='append_tracker.py':return t.__dict__
  if Path(p).name=='prepare_package.py':return {'load_context':lambda:copy.deepcopy(context)}
  if Path(p).name=='update_pr_publication.py':return {'validate_workflow_gate':lambda gate:None}
  raise RuntimeError('unmocked path '+str(p))
 t.runpy=types.SimpleNamespace(run_path=run_path);c.runpy=types.SimpleNamespace(run_path=run_path)
 if identifier=='exact':rows[1]=t.expected_row(pub,meta['title'])
 body='SYNTHETIC ORIGINAL BODY';snapshot={'head':'b'*40,'branch':'research/10900050-prime-difference-counterexample','body_sha256':hashlib.sha256(body.encode()).hexdigest()};save(root/'SUBMITTED_SNAPSHOT.json',snapshot)
 live={'state':'OPEN','isDraft':True,'headRefOid':snapshot['head'],'headRefName':snapshot['branch'],'body':body}
 def external(args,**kw):
  events.append({'external':args});return json.dumps(live)if args[0]=='gh'else snapshot['head']+' refs/heads/'+snapshot['branch']+'\n'
 c.subprocess=types.SimpleNamespace(check_output=external)
 try:
  with contextlib.redirect_stdout(io.StringIO()):(c.live_preflight if kind=='preflight'else t.main)()
  accepted=True;error=None
 except(RuntimeError,ValueError,KeyError,StopIteration)as e:accepted=False;error=str(e)
 return {'kind':kind,'existing_identifier':identifier,'accepted':accepted,'error':error,'append_calls':sum(e.get('service')==['spreadsheets','values','append']for e in events),'data_rows_after':len(rows)-1,'events':events}
def main():
 out=[probe(k,i)for k in ['preflight','append']for i in ['AMR','AMRlower','numeric','PR','bareDOI','DOIURL','unrelated','exact']]
 for case in out:
  expected=(case['existing_identifier'] in {'bareDOI','DOIURL','unrelated'} if case['kind']=='preflight' else case['existing_identifier'] in {'unrelated','exact'})
  append_expected=1 if case['kind']=='append' and case['existing_identifier']=='unrelated' else 0
  if case['accepted']!=expected or case['append_calls']!=append_expected:raise RuntimeError('Identity guard/recovery differs '+str(case))
 save(R/('TRACKER_IDENTITY_'+str(sys.flags.optimize)+'.json'),{'optimization':sys.flags.optimize,'operative_source_sha256':{'append_tracker.py':hashlib.sha256((A/'publication/append_tracker.py').read_bytes()).hexdigest(),'pr1268.py':hashlib.sha256((A.parents[1]/'publication_coordinators/pr1268.py').read_bytes()).hexdigest()},'all_external_operations_mocked':True,'cases':out})
 print(json.dumps([{k:x[k]for k in ['kind','existing_identifier','accepted','append_calls','data_rows_after']}for x in out]))
if __name__=='__main__':main()
