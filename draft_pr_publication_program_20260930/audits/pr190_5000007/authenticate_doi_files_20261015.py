"""Read-only primary DOI identity check; no external programs executed."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,urllib.request
A=Path(__file__).resolve().parent
D=A/'root_doi_identity_20261015';D.mkdir(exist_ok=False)
def fetch(url):
 t=datetime.datetime.now(datetime.UTC).isoformat()
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'IndependentResearchAudit/1.0'}),timeout=90) as r:
  b=r.read();q={'URL':url,'UTC':t,'final_URL':r.url,'status':r.status,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 return q,b
q,b=fetch('https://zenodo.org/api/records/23267641');(D/'record.private.json').write_bytes(b);j=json.loads(b)
expected={'AMR-049-paper.pdf':'ff6b9ba5f9bac0027a39d6e06319f04ff08bf24776a47cf7070213924d454707','AMR-049-source.zip':'d17acdd2a34f34685b3d854d3abfd4dbf19e253599c5c3f89f94e1ea078dd8d0','AMR-049-verification-report.md':'6f89f5ee24d11fa7bc0dbc7677bb883a8173160a2ca466708c6718f9d2b5f6a5'}
def check(x):
 n=x['key'];q,b=fetch(x['links']['self']);q['name']=n;q['record_checksum']=x['checksum'];q['computed_md5']='md5:'+hashlib.md5(b).hexdigest();q['record_size']=x['size'];q['matches_previously_pinned_current_website_SHA256']=q['sha256']==expected[n]
 if q['computed_md5']!=q['record_checksum'] or len(b)!=x['size'] or not q['matches_previously_pinned_current_website_SHA256']:raise RuntimeError('Primary identity mismatch '+n)
 (D/('private_'+n)).write_bytes(b)
 return q
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:files=list(ex.map(check,j['files']))
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'DOI_VERSION_CURRENT_FILES_AUTHENTICATED_AND_MATCH_PRIOR_WEBSITE_PINS','DOI':j['doi'],'record':q,'files':files,'all_three_files_authenticated':True,'downloaded_external_code_executed':False,'historical_limit':'This authenticates presently retrieved DOI-version files, not historical server visibility, firstness, awareness or independence.'}
if out['DOI']!='10.5281/zenodo.23267641' or set(x['name'] for x in files)!=set(expected):raise RuntimeError('Unexpected identity/membership')
p=A/'ROOT_DOI_FILE_IDENTITY_20261015_01.json';p.write_text(json.dumps(out,indent=2)+'\n');p.chmod(0o444)
print(json.dumps(out))
