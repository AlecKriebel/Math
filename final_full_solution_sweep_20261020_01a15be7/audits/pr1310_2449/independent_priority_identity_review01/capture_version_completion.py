from pathlib import Path
import json,gzip,urllib.request,urllib.parse,hashlib,datetime,concurrent.futures,subprocess
P=Path(__file__).resolve().parent;D=P/'private/sources';PIN='0804de278fdf1d355aea7b584ac5b67e0955f27b'
def url(base,**params):return base+'?'+urllib.parse.urlencode(params)
q={
'osf_node_public':'https://api.osf.io/v2/nodes/d6uq5/',
'osf_identifiers':'https://api.osf.io/v2/nodes/d6uq5/identifiers/',
'osf_files_public':'https://api.osf.io/v2/nodes/d6uq5/files/osfstorage/?page[size]=100',
'osf_v2':'https://osf.io/download/ynb6j/',
'osf_v2_versions':'https://api.osf.io/v2/files/6a52b62709018c51897afb80/versions/',
'osf_v3_versions':'https://api.osf.io/v2/files/6a576d8420180521b4de6d2d/versions/',
'datacite_osf':url('https://api.datacite.org/dois',query='d6uq5',**{'page[size]':100}),
'zenodo_upper_record':'https://zenodo.org/api/records/19503638',
'zenodo_upper_concept':'https://zenodo.org/api/records/19444425',
'zenodo_piranian_page2':'https://zenodo.org/api/records?page=2&q=Piranian&size=25&sort=bestmatch',
'zenodo_title1038':url('https://zenodo.org/api/records',q='title:1038 AND (Erdos OR Erdős)'),
'zenodo_dpt':url('https://zenodo.org/api/records',q='"Darvas" AND "Peng"'),
'zenodo_wang':url('https://zenodo.org/api/records',q='"Shouqiao Wang"'),
}
for n in range(2,7):q['datacite_title_1038_page'+str(n)]=url('https://api.datacite.org/dois',query='titles.title:1038',**{'page[size]':100,'page[number]':n})
for fn in ['README.md','contact_existence.py','erdos1038_forcing_exact.py','erdos1038_exact_endpoint_certificate.py','symbolic_contact_verifier.py','symbolic_endpoint_verifier.py']:
 q['dpt_certificate_'+fn.replace('.','_')]=f'https://raw.githubusercontent.com/Pengbinghui/pipeline-math/{PIN}/papers/erdos1038/certificates/{fn}'
def fetch(k,u):
 at=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'IndependentMathematicsAudit/1.0'}),timeout=35) as r:b=r.read(2200001);status=r.status;final=r.url
  if len(b)>2200000:raise RuntimeError('bounded-source limit')
  (D/(k+'.gz')).write_bytes(gzip.compress(b,mtime=0))
  return dict(key=k,url=u,at_utc=at,status=status,final_url=final,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),capture='private/sources/'+k+'.gz',private=True)
 except Exception as e:return dict(key=k,url=u,at_utc=at,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:results=list(ex.map(lambda x:fetch(*x),q.items()))
(P/'VERSION_COMPLETION_INDEX.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
for r in results:print(json.dumps({k:r[k] for k in ['key','status','bytes','error'] if k in r}))
if (D/'osf_v2.gz').exists():
 b=gzip.decompress((D/'osf_v2.gz').read_bytes());r=subprocess.run(['pdftotext','-layout','-','-'],input=b,capture_output=True)
 if r.returncode:raise RuntimeError('pdftotext')
 (D/'osf_v2_text.gz').write_bytes(gzip.compress(r.stdout,mtime=0))
print('TOTAL_BYTES',sum(f.stat().st_size for f in P.rglob('*') if f.is_file()))
