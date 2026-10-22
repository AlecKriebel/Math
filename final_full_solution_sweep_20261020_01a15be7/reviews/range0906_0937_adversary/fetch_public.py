from pathlib import Path
import json,urllib.request,hashlib,datetime,concurrent.futures
W=Path(__file__).resolve().parent;P=W/'private';P.mkdir(exist_ok=True)
def fetch(url,target):
 req=urllib.request.Request(url,headers={'User-Agent':'Independent-bounded-research-review/1.0'})
 with urllib.request.urlopen(req,timeout=45) as f: b=f.read(); receipt={'url':url,'final_url':f.url,'status':f.status,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 target.write_bytes(b);return receipt

def case(n):
 d=json.loads((P/f'inputs/PR{n:04}_DISPOSITION.json').read_text());record=d['doi'].rsplit('.',1)[-1];folder=P/f'public{n:04}';folder.mkdir(exist_ok=True);out={'pr':n,'record':int(record)}
 out['doi']=fetch('https://doi.org/'+d['doi'],folder/'doi_landing.html');out['metadata']=fetch('https://zenodo.org/api/records/'+record,folder/'metadata.json');meta=json.loads((folder/'metadata.json').read_text());out['files']=[]
 for f in meta['files']:
  rec=fetch(f['links']['self'],folder/f['key']);rec.update(name=f['key'],provider_size=f['size'],provider_checksum=f['checksum']);b=(folder/f['key']).read_bytes();rec['provider_md5_equal']=hashlib.md5(b).hexdigest()==f['checksum'].removeprefix('md5:');rec['provider_size_equal']=len(b)==f['size'];out['files'].append(rec)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:res=list(pool.map(case,[906,908,909,919]))
(W/'PUBLIC_FETCH_CHECKS.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps([{'pr':r['pr'],'doi_status':r['doi']['status'],'metadata_status':r['metadata']['status'],'files':[(f['name'],f['bytes'],f['provider_md5_equal']) for f in r['files']]} for r in res],indent=2))
