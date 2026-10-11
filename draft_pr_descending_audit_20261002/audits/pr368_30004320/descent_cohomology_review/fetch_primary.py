from pathlib import Path
import json,hashlib,subprocess,datetime
O=Path(__file__).resolve().parent;P=O.parent/'snapshot/problems/30004320_laurent_descent'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
routes=[]
for name in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T1.json','SOURCE_ADDITION_T4.json','SOURCE_ADDITION_T5.json']:
 def walk(o):
  if isinstance(o,dict):
   if all(k in o for k in ['url','sha256','bytes']):routes.append({k:o[k] for k in ['url','sha256','bytes']})
   for v in o.values():walk(v)
  elif isinstance(o,list):
   for v in o:walk(v)
 walk(json.loads((P/name).read_text()))
rows=[]
for i,r in enumerate(routes,1):
 f=O/'private/sources'/f's{i:02d}.pdf';rc=0;err=''
 if not f.exists():
  p=subprocess.run(['curl','--fail','--location','--retry','2','--connect-timeout','15','--max-time','90',r['url'],'--output',str(f)],capture_output=True,text=True);rc=p.returncode;err=p.stderr
 if rc or not f.exists():rows.append({'id':f's{i:02d}',**r,'download_returncode':rc,'error':err});continue
 d=f.read_bytes();t=f.with_suffix('.txt');p=subprocess.run(['pdftotext','-layout',str(f),str(t)],capture_output=True,text=True)
 rows.append({'id':f's{i:02d}',**r,'actual_bytes':len(d),'actual_sha256':hashlib.sha256(d).hexdigest(),'historical_match':len(d)==r['bytes'] and hashlib.sha256(d).hexdigest()==r['sha256'],'verified_at':now(),'extraction_returncode':p.returncode,'extraction_stderr':p.stderr,'text_bytes':t.stat().st_size,'text_sha256':hashlib.sha256(t.read_bytes()).hexdigest()})
j={'verified_at':now(),'pre_candidate_routing_only':True,'initial_failure':'First urllib parallel acquisition downloaded ten of eleven files but failed on s10 with URLError(ConnectionResetError54); this retry retained and validated those ten actual downloads. A combined source read was truncated and reissued in bounded portions.','sources':rows};(O/'SOURCE_ACQUISITION.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
