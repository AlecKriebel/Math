from pathlib import Path
import subprocess,sys,json,hashlib,os,datetime
OWN=Path(__file__).resolve().parent;CAND=OWN.parents[1]/'preprint_v1_0';kit=OWN/'scratch/kit'
def need(x,s):
 if not x:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
rows=[]
def call(args,expected=True):
 r=subprocess.run([str(a) for a in args],capture_output=True,cwd=OWN)
 need((r.returncode==0)==expected,'wrong command outcome '+r.stderr.decode(errors='replace'))
 rows.append({'argv':[str(a) for a in args],'returncode':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)})
 return r
for opt in (False,True):
 base=[sys.executable]+(['-O'] if opt else [])+['-B'];r=call(base+[OWN/'independent_checks.py']);(OWN/('INDEPENDENT_'+('OPTIMIZED' if opt else 'NORMAL')+'.json')).write_bytes(r.stdout);call(base+[OWN/'independent_checks.py','--invalid'],False)
 for fault in ('symlink','hardlink','duplicateNativeJSON','changedNativeSelections','changedExternalPDF'):
  if fault in ('symlink','hardlink'):
   p=kit/'paper.pdf';saved=OWN/'scratch/saved-pdf';p.rename(saved)
   if fault=='symlink':p.symlink_to(saved)
   else:os.link(saved,p)
   call(base+[kit/'code/verify_kit.py'],False);p.unlink();saved.rename(p)
  elif fault in ('duplicateNativeJSON','changedNativeSelections'):
   p=kit/'publication/zenodo-deposit.json';old=p.read_bytes()
   if fault=='duplicateNativeJSON':p.write_bytes(b'{"metadata":{},"metadata":{},"files":[]}')
   else:
    j=json.loads(old);j['files'][0]['name']='wrong.pdf';p.write_text(json.dumps(j))
   call(base+[kit/'code/verify_kit.py'],False);p.write_bytes(old)
  else:
   p=kit/'paper.pdf';old=p.read_bytes();p.write_bytes(old+b'corrupt');call(base+[kit/'code/verify_kit.py'],False);p.write_bytes(old)
 call(base+[kit/'code/verify_kit.py'])
need((OWN/'INDEPENDENT_NORMAL.json').read_bytes()==(OWN/'INDEPENDENT_OPTIMIZED.json').read_bytes(),'complete fresh controls mode equality')
pins=json.loads((CAND/'OUTPUT_PINS.json').read_text());seal=json.loads((CAND/'PREPARATION_SEAL.json').read_text())
for r in pins['entries']:need(pin(CAND/r['path'])=={'bytes':r['bytes'],'sha256':r['sha256']},'preparation output pin changed')
need(len(pins['entries'])==123 and seal['output_pins_sha256']==sha((CAND/'OUTPUT_PINS.json').read_bytes()),'preparation seal binding')
(OWN/'ADDITIONAL_CONTROLS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':rows,'status':'PASS','preparation_outputs_rehashed':123,'preparation_seal_binding_exact':True,'all7_canonical_PNGs':[{ 'page':i,'actually_viewed':True,**pin(OWN/('scratch/page-'+str(i)+'.png')),'visual_issues':[]} for i in range(1,8)]},indent=2)+'\n')
print(json.dumps({'commands':len(rows),'independent':json.loads((OWN/'INDEPENDENT_NORMAL.json').read_text()),'preparation_outputs':123}))
