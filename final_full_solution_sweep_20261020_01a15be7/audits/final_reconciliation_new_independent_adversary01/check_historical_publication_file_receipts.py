"""Read-only historical file-receipt check; no new public downloads."""
from pathlib import Path
import json,lzma,hashlib,re,collections
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
W=Path(__file__).resolve().parent;J=R/'audits/final_reconciliation_join_preparation01'
H=lambda b:hashlib.sha256(b).hexdigest()
b=(W/'HISTORICAL_DEDUPLICATION_AND_FAMILY_COUNTS.json').read_bytes()
if H(b)!='967a76864be5c91b252637586b69ee32adda890f2677ed8ac93e7472a8c7aecf':raise RuntimeError('Historical category pin')
skips=json.loads(b)['historical_already_correctly_recorded_PRs']
v=json.loads(lzma.decompress((J/'EFFECTIVE_JOIN.json.xz').read_bytes()));by={x['pr']:x for x in v['rows']}
out=[];filecount=pdfcount=supportcount=0
for pr in skips:
 candidates=[]
 for p in sorted(R.glob('PR%04d_*.json'%pr)):
  if not('PUBLICATION'in p.name and any(k in p.name for k in ['VERIFICATION','COVERAGE_DETAILS'])):continue
  b=p.read_bytes();j=json.loads(b)
  if j.get('doi','').lower().replace('https://doi.org/','')!=by[pr]['coverage']['doi'].lower():continue
  for key in ['files','public_files']:
   if type(j.get(key))is list and j[key]:candidates.append((p,b,j,key));break
 if not candidates:raise RuntimeError('No historical full file-list receipt '+str(pr))
 p,b,j,key=candidates[0];files=j[key];pdfs=[f for f in files if f['name'].lower().endswith('.pdf')];support=[f for f in files if not f['name'].lower().endswith('.pdf')]
 if not pdfs or not support:raise RuntimeError('Paper/support list incomplete '+str(pr))
 for f in files:
  size=f.get('size',f.get('bytes',f.get('remote_bytes')))
  if type(size)is not int or size<=0:raise RuntimeError('Bad positive file size '+str(pr))
  for flag in ['download_verified','matches','zip_crc_ok']:
   if flag in f and f[flag]is not True:raise RuntimeError('Recorded verification failure '+str(pr)+' '+flag)
  if 'local_bytes'in f and f['local_bytes']!=f['remote_bytes']:raise RuntimeError('Recorded size disagreement '+str(pr))
  if 'local_md5'in f and f['local_md5']!=f['remote_md5']:raise RuntimeError('Recorded MD5 disagreement '+str(pr))
  for k,pattern in [('md5',r'[a-f0-9]{32}'),('remote_md5',r'[a-f0-9]{32}'),('sha256',r'[a-f0-9]{64}'),('checksum',r'md5:[a-f0-9]{32}')]:
   if k in f and not re.fullmatch(pattern,f[k]):raise RuntimeError('Malformed reported payload digest '+str(pr))
  if not any(k in f for k in ['md5','remote_md5','sha256','checksum']):raise RuntimeError('No reported file digest '+str(pr))
 filecount+=len(files);pdfcount+=len(pdfs);supportcount+=len(support)
 out.append({'pr':pr,'doi':by[pr]['coverage']['doi'],'current_ledger_row':by[pr]['coverage']['row'],'source':{'path':str(p),'bytes':len(b),'sha256':H(b)},'receipt_field':key,'files':[{'name':f['name'],'bytes':f.get('size',f.get('bytes',f.get('remote_bytes'))),'reported_sha256':f.get('sha256'),'reported_md5':f.get('md5',f.get('remote_md5',f.get('checksum')))}for f in files]})
if len(out)!=139:raise RuntimeError('Historical skip count')
print(json.dumps({'status':'PASS_139_HISTORICAL_REPORTED_PAPER_AND_SUPPORT_RECEIPT_BINDINGS','PR_count':139,'reported_files':filecount,'reported_PDFs':pdfcount,'reported_support_files':supportcount,'records':out,'new_downloads_or_service_calls':0,'new_mathematical_audit':False,'claim_scope':'Dated retained affirmative receipt consistency; not fresh remote-state or payload reconstruction'},indent=2,sort_keys=True))
