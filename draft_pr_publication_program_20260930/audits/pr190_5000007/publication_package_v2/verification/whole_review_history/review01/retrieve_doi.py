from pathlib import Path
import json,hashlib,urllib.request,datetime,concurrent.futures
O=Path(__file__).resolve().parent;P=O/'private_sources';A=O.parent
j=json.loads((P/'zenodo_record_23267641.json').read_text())
site={'AMR-049-paper.pdf':A/'current_literature_priority_adversary/private_sources/ferudun_paper_current.pdf','AMR-049-source.zip':A/'current_literature_priority_adversary/private_sources/ferudun_source_current.zip'}
def fetch(f):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat();u=f['links']['self'];r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'independent-readonly-research-audit/1.0'}),timeout=40);b=r.read();(P/f['key']).write_bytes(b);row={'UTC':t,'url':u,'final_url':r.url,'status':r.status,'name':f['key'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'md5':hashlib.md5(b).hexdigest(),'record_size_match':len(b)==f['size'],'record_checksum_match':'md5:'+hashlib.md5(b).hexdigest()==f['checksum']}
 if f['key'] in site:row['byte_identical_to_local_current_website_pin']=b==site[f['key']].read_bytes()
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(fetch,j['files']))
(O/'DOI_FILE_IDENTITY_RESULTS.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'record_created':j['created'],'record_updated':j['updated'],'version':j['metadata']['version'],'files':rows,'historical_limit':'Present exact file identity only; no historical visibility, firstness, awareness or independence inference.'},indent=2));print(json.dumps(rows,indent=2))
