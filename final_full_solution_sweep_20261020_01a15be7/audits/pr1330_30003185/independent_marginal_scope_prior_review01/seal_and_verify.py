"""Freeze or verify this owned independent read-only mathematical packet."""
from pathlib import Path
import hashlib,json,datetime,gzip,sys
P=Path(__file__).resolve().parent;M=P/'MANIFEST.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,why):
 if not ok:raise RuntimeError(why)
def strict(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(strict(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(strict(x,y)for x,y in zip(a,b))
 return a==b
def files():
 v=[]
 for q in P.rglob('*'):
  need(not q.is_symlink(),'unexpected symlink')
  if q.is_file()and q!=M:v.append(q)
 return sorted(v,key=lambda q:q.relative_to(P).as_posix())
def rows():return [{'path':q.relative_to(P).as_posix(),'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())}for q in files()]
def controls():
 c=json.loads((P/'CLOSURE.json').read_text());need(c['publication_ready']is False and c['full_new_generation_acceptance']is False,'scope/readiness drift')
 for k in ['service_write_calls','git_mutations','PR_comments']:
  need(type(c[k])is int and c[k]==0,'unexpected action')
 need(c['CASE_created']is False and c['previous_packets_touched']is False,'preservation control')
 need(not any(q.name=='CASE'for q in P.rglob('*')),'unexpected CASE')
 pins=json.loads((P/'PINNED_PR_INPUTS.json').read_text());need(len(pins)==34,'input count')
 for x in pins:
  b=(P/'pinned_pr'/x['path']).read_bytes()
  need(len(b)==x['bytes']and sha(b)==x['sha256'],'input content mismatch')
  need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'],'native hash mismatch')
 for x in json.loads((P/'SOURCE_REVERIFICATION.json').read_text())['fresh_primary_PDF_matches']:
  b=(P/x['path']).read_bytes();need(len(b)==x['bytes']and sha(b)==x['sha256'],'primary PDF mismatch')
 for x in json.loads((P/'EXECUTION_SOURCE_BINDING.json').read_text())['bindings']:
  need(sha((P/x['script']).read_bytes())==x['source_sha256'],'test source drift')
  base=None
  for y,mode in zip(x['results'],[0,1,2]):
   b=(P/y['path']).read_bytes();need(len(b)==y['bytes']and sha(b)==y['sha256'],'test result drift')
   j=json.loads(b);need(type(j['optimization'])is int and j.pop('optimization')==mode,'mode')
   need(j['status']=='PASS'and type(j['checks'])is int and j['checks']==x['checks_per_mode'],'test status/count')
   if base is None:base=j
   else:need(strict(j,base),'result identity across modes')
 for n in ['LEDGER_DUPLICATE_CHECK.json','LEDGER_DUPLICATE_CHECK_FINAL.json']:
  j=json.loads((P/n).read_text());need(j['sheet_gid']==1254632077 and j['columns']==43,'sheet target')
  need(strict(j['row_counts'],{'UNFORMATTED_VALUE':191,'FORMULA':191}),'row-count record')
  d=P/j['private_capture'];views=[]
  for mode in ['UNFORMATTED_VALUE','FORMULA']:
   raw=json.loads(gzip.decompress((d/(mode+'.stdout.gz')).read_bytes()))
   views.append(raw['valueRanges'][0]['valueRange']['values'])
  need(strict(views[0],views[1])and len(views[0])==191,'raw two-view identity')
  before=json.loads(gzip.decompress((d/'metadata_before.stdout.gz').read_bytes()))
  after=json.loads(gzip.decompress((d/'metadata_after.stdout.gz').read_bytes()))
  need(strict(before,after),'raw metadata identity')
 proposal=json.loads((P/'QUALIFIED_EXISTING_PUBLICATION_ROW.json').read_text());r=proposal['row_A_to_D']
 need(type(r)is list and len(r)==4 and all(type(v)is str for v in r)and r[1]=='','four literal cells/B blank')
 need('https://github.com/AlecKriebel/Math/pull/1330'in r[3]and r[2]=='https://doi.org/10.1016/j.jalgebra.2019.09.009','qualified proposal identity')
 need(proposal['publication_ready']is False and proposal['append_authorized_by_this_packet']is False,'proposal action drift')
 nested=[q.relative_to(P).as_posix()for q in files()if 'MANIFEST'in q.name]
 need(len(nested)==3,'all three nested input manifests retained')
controls()
if '--verify-only'not in sys.argv:
 need(not M.exists(),'already sealed')
 data={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Marginal/source/priority family only. No full new generation/action/novelty approval.','exclude_exactly':'MANIFEST.json','all_other_files_included':True,'members':rows()}
 with M.open('x')as f:json.dump(data,f,indent=2,ensure_ascii=False);f.write('\n')
need(M.is_file(),'missing manifest');data=json.loads(M.read_text())
need(data['exclude_exactly']=='MANIFEST.json'and strict(data['members'],rows()),'sealed inventory drift')
allocated=sum(q.stat().st_blocks*512 for q in [*files(),M]);need(allocated<=8*1024**2,'allocation cap')
print(json.dumps({'status':'PASS','members':len(data['members']),'manifest_sha256':sha(M.read_bytes()),'conservative_allocated_bytes':allocated,'cap_bytes':8*1024**2,'publication_ready':False,'generation_acceptance':False,'qualified_inactive_prior_row_proposals':1},indent=2))
