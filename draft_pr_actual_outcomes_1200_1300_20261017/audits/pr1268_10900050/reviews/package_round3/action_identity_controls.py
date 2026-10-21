#!/usr/bin/env python3
import os,sys
sys.dont_write_bytecode=True
from pathlib import Path
R=Path(__file__).resolve().parent;A=R.parents[1];S=R/'ignored_scratch/action_identity';S.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(R/'ignored_scratch/tmp');os.environ['PYTHONDONTWRITEBYTECODE']='1'
import copy,contextlib,datetime,hashlib,importlib.util,io,json,shutil,types

def need(v,m):
 if not v:raise RuntimeError(m)
def load(p):
 sp=importlib.util.spec_from_file_location('r3_action_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
context=json.loads((A/'CURRENT_PR1268_CONTEXT.json').read_text());title=context['title'];pub={'id':798123,'environment':'production','state':'published','metadata_normalizations':[],'doi':'10.5281/zenodo.798123','doi_url':'https://doi.org/10.5281/zenodo.798123','record_url':'https://zenodo.org/records/798123','title':title}
rowspecs=[('numeric','10900050',True,True),('AMR_mixed','aMr-108-0050',True,True),('PR_mixed','HTTPS://GITHUB.COM/ALECKRIEBEL/MATH/PULL/1268',True,True),('DOI_trim',' \t10.5281/zenodo.798123  ',False,True),('URL_trim','  HTTPS://DOI.ORG/10.5281/ZENODO.798123\t',False,True),('other','Unrelated issue 10900051',False,False)]
results=[]
for kind in ['preflight','append']:
 for label,identity,pre,post in rowspecs:
  for col in range(4):
   root=S/(str(sys.flags.optimize)+'_'+kind+'_'+label+'_'+str(col));root.mkdir(exist_ok=True);P=root/'publication';P.mkdir(exist_ok=True)
   for n in ['append_tracker.py','zenodo-deposit.json']:shutil.copyfile(A/'publication'/n,P/n)
   shutil.copyfile(A.parents[1]/'publication_coordinators/pr1268.py',root/'pr1268.py');t=load(P/'append_tracker.py');c=load(root/'pr1268.py');c.P=P;c.A=root
   save(P/'PUBLICATION_RECEIPT.json',pub);save(P/'FINAL_REVIEW_GATE.json',{})
   row=['','','',''];row[col]=identity;rows=[['Original Problem','Solution Chat URL','DOI','Notes'],row];events=[]
   def call(parts,params,body=None):
    events.append(parts)
    if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':t.GID,'title':'Math Puzzles'}}]}
    if parts==['spreadsheets','values','get']:return {'values':copy.deepcopy(rows if params['range']=="'Math Puzzles'!A:D"else[rows[-1]])}
    if parts==['spreadsheets','values','append']:
     rows.append(copy.deepcopy(body['values'][0]));return {'updates':{'updatedRange':"'Math Puzzles'!A3:D3",'updatedRows':1,'updatedColumns':4}}
    raise RuntimeError('unmocked external call')
   t.call=call
   def run(p):
    if Path(p).name=='append_tracker.py':return t.__dict__
    if Path(p).name=='prepare_package.py':return {'load_context':lambda:copy.deepcopy(context)}
    if Path(p).name=='update_pr_publication.py':return {'validate_workflow_gate':lambda g:None}
    raise RuntimeError('unexpected dynamic dependency')
   t.runpy=types.SimpleNamespace(run_path=run);c.runpy=types.SimpleNamespace(run_path=run)
   body='R3 synthetic original';snap={'head':'f'*40,'branch':'synthetic-branch','body_sha256':hashlib.sha256(body.encode()).hexdigest()};save(root/'SUBMITTED_SNAPSHOT.json',snap)
   live={'state':'OPEN','isDraft':True,'headRefOid':snap['head'],'headRefName':snap['branch'],'body':body};c.subprocess=types.SimpleNamespace(check_output=lambda args,**kw:json.dumps(live)if args[0]=='gh'else snap['head']+' ref\n')
   try:
    with contextlib.redirect_stdout(io.StringIO()):(c.live_preflight if kind=='preflight'else t.main)()
    accepted=True;error=None
   except RuntimeError as e:accepted=False;error=str(e)
   expected=not(pre if kind=='preflight'else post);need(accepted==expected,'action identity '+kind+label+str(col));count=events.count(['spreadsheets','values','append']);need(count==(1 if expected and kind=='append'else 0),'append count')
   results.append({'stage':kind,'identity':label,'cell':col,'accepted':accepted,'append_count':count,'error':error})
# Exact existing intended row with accepted earlier intent recovers without append.
root=S/(str(sys.flags.optimize)+'_recovery');root.mkdir(exist_ok=True);P=root/'publication';P.mkdir(exist_ok=True)
shutil.copyfile(A/'publication/append_tracker.py',P/'append_tracker.py');shutil.copyfile(A/'publication/zenodo-deposit.json',P/'zenodo-deposit.json');t=load(P/'append_tracker.py')
t.runpy=types.SimpleNamespace(run_path=lambda p:{'load_context':lambda:copy.deepcopy(context)}if Path(p).name=='prepare_package.py'else{'validate_workflow_gate':lambda g:None});save(P/'FINAL_REVIEW_GATE.json',{});save(P/'PUBLICATION_RECEIPT.json',pub);row=t.expected_row(pub,title);save(P/'tracker/INTENT.json',{'spreadsheetId':t.SID,'gid':t.GID,'range':"'Math Puzzles'!A:D",'row':row});events=[]
def recover(parts,params,body=None):
 events.append(parts)
 if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':t.GID,'title':'Math Puzzles'}}]}
 if parts==['spreadsheets','values','get']:return {'values':[['Original Problem','Solution Chat URL','DOI','Notes'],row]if params['range']=="'Math Puzzles'!A:D"else[row]}
 raise RuntimeError('recovery attempted mutation')
t.call=recover
with contextlib.redirect_stdout(io.StringIO()):t.main();t.main()
receipt=json.loads((P/'tracker/TRACKER_RECEIPT.json').read_text());need(receipt['recovered_existing_exact_row']and receipt['row']==row and row[1]=='','exact recovery')
save(R/('ACTION_IDENTITY_'+str(sys.flags.optimize)+'.json'),{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimization':sys.flags.optimize,'cases':results,'exact_intended_lost_append_recovery':{'two_runs':True,'append_calls':events.count(['spreadsheets','values','append']),'range':receipt['updatedRange'],'full_four_cell_exact':True,'B_blank':True},'scope':'Fresh independent action-time matrix, actual append/preflight bodies copied. Only gate and context dependencies stubbed; all services mocked. Unknown future DOI-only row deliberately does not identify problem before creation.'})
print(json.dumps({'optimization':sys.flags.optimize,'action_cases':len(results),'exact_recovery':'PASS'}))
