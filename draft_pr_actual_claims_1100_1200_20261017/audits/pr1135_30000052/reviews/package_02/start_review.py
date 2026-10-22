from pathlib import Path
import hashlib,json,zipfile,datetime
R=Path(__file__).resolve().parent; A=R.parents[1]; P=A/'publication'
def h(p):
 b=p.read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(n,x): (R/n).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
files=['main.tex','output/pdf/random-lattice-counterexample.pdf','output/random-lattice-counterexample-source-and-verification.zip','output/zenodo-upload-kit.zip','zenodo-metadata.json','zenodo-deposit.json','PACKAGE_RECEIPT.json']
pins={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'publication':{n:h(P/n) for n in files},'inputs':{p.name:h(p) for p in sorted((A/'inputs').iterdir()) if p.is_file()}}
put('START_PINS.json',pins)
inv={}
for n in files[2:4]:
 with zipfile.ZipFile(P/n) as z:
  names=z.namelist(); rows=[]
  for i in z.infolist():
   b=z.read(i.filename); rows.append({'name':i.filename,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'compress_type':i.compress_type,'timestamp':i.date_time,'safe':not i.filename.startswith('/') and '..' not in Path(i.filename).parts})
  inv[n]={'members':len(names),'unique_names':len(set(names)),'files':rows,'all_crc_valid':z.testzip() is None}
  if n==files[2]:
   if not all(q['safe'] for q in rows): raise ValueError('unsafe archive')
   z.extractall(R/'tmp/mirror')
put('ARCHIVE_INVENTORY.json',inv)
put('LIVE_INVENTORY.json',{str(p.relative_to(P)):h(p) for p in sorted(P.rglob('*')) if p.is_file()})
(R/'LOG.md').write_text('# Package round 2 log\n\n- '+pins['timestamp']+' — 5%: started independent whole-package audit; new review directory and ignored private/tmp areas created before retrieval. Main branch observed. No Git mutations. Initial six operative files, receipt and all ten original inputs pinned; archives inventoried and source extracted to ignored mirror.\n')
print(json.dumps({'pins':pins,'archive_counts':{k:v['members'] for k,v in inv.items()}},indent=2))
