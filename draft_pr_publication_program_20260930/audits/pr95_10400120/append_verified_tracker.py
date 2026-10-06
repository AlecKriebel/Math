"""One actual append, preceded and followed by complete target-tab duplicate reads."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent;C=A.parents[2]
D=A/'tracker_acceptance_20261005';D.mkdir(exist_ok=False);records=[]
GWS='/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'
SID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';TAB="'Math Puzzles'!A:D"
def require(ok,message):
    if not ok:raise RuntimeError(message)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def load(p):return json.loads(p.read_text())
def run(label,args):
    dest=D/label;dest.mkdir(exist_ok=False);argv=[GWS,*args];started=now()
    dump(dest/'started.json',{'argv':argv,'UTC':started,'recorder_PID':os.getpid()})
    child=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
    (dest/'stdout.bin').write_bytes(out);(dest/'stderr.bin').write_bytes(err)
    x={'argv':argv,'child_PID':child.pid,'UTC_start':started,'UTC_end':now(),'exit_code':child.returncode,
       'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()}
    dump(dest/'execution.json',x);records.append({'label':label,**x});dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records})
    require(child.returncode==0,'CLI failed; reconcile actual sheet before considering another append: '+label)
    return json.loads(out)
def read(label):return run(label,['sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':SID,'range':TAB,'majorDimension':'ROWS','valueRenderOption':'FORMATTED_VALUE'})])
ready=load(A/'ROOT_READY_FOR_PUBLICATION.json');require(ready['publication_clearance'] is True,'review gate')
pub=load(A/'actual_operations/zenodo_publish/stdout.bin');public=load(A/'ROOT_PUBLIC_DEPOSIT_VERIFICATION.json')
require(pub['state']=='published' and public['verified'] and public['DOI']==pub['doi'],'publication gate')
title=pub['title'];doi=pub['doi'];url=pub['doi_url']
metadata=run('tab_metadata',['sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':SID,'fields':'sheets(properties(sheetId,title))'})])
require(any(s['properties']['sheetId']==1254632077 and s['properties']['title']=='Math Puzzles' for s in metadata['sheets']),'target gid/title')
notes=(title+' — Alec Kriebel (ORCID 0009-0001-9320-500X), 2026-10-05, v1.0. Verified ordinary full SU(5) counterexample at WZW level 5 (shifted level 10) to printed Ohtsuki Conjecture 7.5: L(5,1) and L(5,2), both pi1=Z/5, have unequal positive S3-normalized squares 3475 + 1550 sqrt(5) and 4025 + 1800 sqrt(5). Historical priority UNRESOLVED: Kuriya\'s directly relevant preprint could not be obtained; it is credited, and we cannot rule out its containing or circumscribing this result. No firstness, exhaustive novelty, current global openness or new historical resolution claim. Imported RT/modular-category and Hansen-Takata formula inputs; edition/read gaps disclosed. Extensive AI use; unrefereed without conventional human peer review. Fresh sequential whole-package adversarial reviews; PDF, source and portable exact verification package with checks active under optimized Python. PR95: https://github.com/AlecKriebel/Math/pull/95. Original author effort 2/5; zero new central proof-search turns.')
row=['https://www.unsolvedmath.com/problems/AMR-103-0120','',url,notes]
dump(D/'PROPOSED_ROW.json',{'spreadsheetId':SID,'range':TAB,'values':[row]})
before=read('before_append');values=before.get('values',[])
require(values and values[0][:4]==['Original Problem','Solution Chat URL','DOI','Notes'],'headers')
duplicates=[(i+1,r) for i,r in enumerate(values) if any(doi in str(v) or title in str(v) for v in r)]
require(not duplicates,'existing DOI/title match: inspect rather than append duplicate')
params={'spreadsheetId':SID,'range':TAB,'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True}
body={'majorDimension':'ROWS','values':[row]};dump(D/'APPEND_PARAMS.json',params);dump(D/'APPEND_BODY.json',body)
# Exactly one mutating invocation. Lost/failed response exits, retaining attempted row for reconciliation.
appended=run('append',['sheets','spreadsheets','values','append','--params',json.dumps(params),'--json',json.dumps(body)])
updates=appended['updates'];target=updates['updatedRange']
require(updates['updatedRows']==1 and updates['updatedColumns']==4 and updates['updatedCells']==4,'append dimensions')
require(updates['updatedData']['values']==[row],'append exact response')
after=read('after_append');hits=[(i+1,r) for i,r in enumerate(after.get('values',[])) if any(doi in str(v) for v in r)]
require(len(hits)==1 and hits[0][1]==row,'unique exact complete-tab readback')
actual="'Math Puzzles'!A"+str(hits[0][0])+':D'+str(hits[0][0])
require(target==actual,'actual updated range')
result={'schema':'pr95-qualified-tracker-verified/v1','UTC':now(),'actual_operator_PID':os.getpid(),
   'spreadsheetId':SID,'gid':1254632077,'DOI':doi,'range':actual,'row':row,'unique_verified':True,
   'priority_clearance':False,'qualified_publication_user_authorized':True,
   'actual_append_execution':'tracker_acceptance_20261005/append/execution.json',
   'actual_readback_execution':'tracker_acceptance_20261005/after_append/execution.json',
   'append_response_sha256':sha(D/'append/stdout.bin'),'readback_response_sha256':sha(D/'after_append/stdout.bin')}
dump(A/'ROOT_TRACKER_RECORD.json',result);print(json.dumps({k:v for k,v in result.items() if k!='row'}))
