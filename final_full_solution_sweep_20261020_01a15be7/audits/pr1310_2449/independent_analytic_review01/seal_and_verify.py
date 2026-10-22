"""Seal only this owned analytic packet, or verify its existing closed inventory."""
from pathlib import Path
import json,hashlib,sys,datetime,gzip
P=Path(__file__).resolve().parent
M=P/'MANIFEST.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,why):
 if not ok:raise RuntimeError(why)
def files():
 out=[]
 for q in P.rglob('*'):
  require(not q.is_symlink(),'symlink in packet')
  if q.is_file() and q!=M:out.append(q)
 return sorted(out,key=lambda q:q.relative_to(P).as_posix())
def rows():return [{'path':q.relative_to(P).as_posix(),'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())}for q in files()]
def controls():
 c=json.loads((P/'CLOSURE.json').read_text())
 require(c['publication_ready'] is False and c['row_proposal'] is False,'readiness drift')
 require(c['service_write_calls']==0 and c['git_mutations']==0 and c['production_CASE_created'] is False,'action drift')
 nested=[q for q in files()if q.name=='MANIFEST.json']
 require(len(nested)==2,'both nested input manifests must be included')
 pins=json.loads((P/'PINNED_PR_INPUTS.json').read_text())
 require(len(pins)==21,'pinned count')
 for x in pins:
  b=(P/'pinned_pr'/x['path']).read_bytes()
  require(len(b)==x['bytes'] and sha(b)==x['sha256'],'pinned content drift')
  require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'],'native blob drift')
 c=json.loads((P/'SOURCE_COMPRESSION.json').read_text())
 b=gzip.decompress((P/c['stored_name']).read_bytes())
 require(len(b)==c['original_bytes'] and sha(b)==c['original_sha256'],'original compressed source drift')
 for x in json.loads((P/'RAW_CAPTURE_COMPRESSION.json').read_text())['files']:
  z=(P/x['compressed_path']).read_bytes();b=gzip.decompress(z)
  require(sha(z)==x['compressed_sha256'] and len(b)==x['original_bytes'] and sha(b)==x['original_sha256'],'raw capture drift')
 for prefix in ['DIAGNOSTICS','FIXED_CANDIDATE']:
  base=None
  for mode,num in [('NORMAL',0),('O',1),('OO',2)]:
   d=json.loads((P/(prefix+'_'+mode+'.json')).read_text())
   require(d['status']=='PASS' and d.pop('optimization')==num,'own output status/mode')
   if base is None:base=d
   else:require(d==base,'own result mode drift')
  if prefix=='DIAGNOSTICS':require(base['checks']==15766,'diagnostic count')
  else:require(base['T_minus_width_upper_at_least_numerator_over_10_to_40']==42327065090,'upper comparison witness')
 for name in ['LEDGER_DUPLICATE_CHECK.json','LEDGER_DUPLICATE_CHECK_FINAL.json']:
  d=json.loads((P/name).read_text())
  require(d['sheet_gid']==1254632077 and d['columns']==43 and d['row_counts']=={'UNFORMATTED_VALUE':191,'FORMULA':191},'ledger coverage')
  require(d['typed_views_identical'] is True and d['metadata_stable'] is True and d['lead_count']==0,'ledger outcome')
 require(not any('CASE'==q.name for q in P.rglob('*')),'unexpected CASE')
controls()
if '--verify-only' not in sys.argv:
 require(not M.exists(),'packet is already sealed')
 data={'sealed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'independent analytic review only; no action/global numerical acceptance','exclude_exactly':'MANIFEST.json','all_other_files_included':True,'members':rows()}
 with M.open('x')as f:json.dump(data,f,indent=2,ensure_ascii=False);f.write('\n')
require(M.is_file(),'missing manifest')
data=json.loads(M.read_text());require(data['exclude_exactly']=='MANIFEST.json','exclusion drift')
require(data['members']==rows(),'member set/content drift')
allocated=sum(q.stat().st_blocks*512 for q in [*files(),M])
require(allocated<=8*1024*1024,'owned allocation cap')
print(json.dumps({'status':'PASS','members':len(data['members']),'manifest_sha256':sha(M.read_bytes()),'conservative_allocated_bytes':allocated,'allocation_limit_bytes':8*1024*1024,'nested_input_manifests_included':2,'publication_ready':False,'full_global_numerical_acceptance':False},indent=2))
