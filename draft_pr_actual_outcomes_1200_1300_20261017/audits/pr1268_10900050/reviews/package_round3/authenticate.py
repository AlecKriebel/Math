import os,sys,json,hashlib,pathlib,datetime
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent
A=R.parent.parent
x=json.loads((R/'INPUT_FREEZE.json').read_text())
rows=[]
for typ in ('files','external_readonly_inputs'):
 for q in x[typ]:
  p=pathlib.Path(q['path']); p=p if p.is_absolute() else A/p
  try:
   b=p.read_bytes(); ok=len(b)==q['bytes'] and hashlib.sha256(b).hexdigest()==q['sha256']
   row={'kind':typ,'path':q['path'],'ok':ok,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
  except Exception as e: row={'kind':typ,'path':q['path'],'ok':False,'error':repr(e)}
  rows.append(row)
r={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_freeze_sha256':hashlib.sha256((R/'INPUT_FREEZE.json').read_bytes()).hexdigest(),'count':len(rows),'failures':[v for v in rows if not v['ok']],'inputs':rows}
(R/sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='inputs'},indent=2))
