from pathlib import Path
import urllib.request,json,datetime,concurrent.futures,hashlib
R=Path(__file__).resolve().parent;M=R/'tmp/mirror';meta=json.loads((M/'zenodo-metadata.json').read_text())
urls=['https://orcid.org/0009-0001-9320-500X']+[('https://doi.org/'+x['identifier']) if x['scheme']=='doi' else x['identifier'] for x in meta['related_identifiers']]
def fetch(url):
 row={'url':url,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical package review'}),timeout=30) as resp:
   b=resp.read();row.update(status=resp.status,final_url=resp.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest());name='link-'+hashlib.sha256(url.encode()).hexdigest()[:12];(R/'sources/private'/name).write_bytes(b)
 except Exception as e:row['error']=str(e)
 return row
out=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(fetch,urls));(R/'LINK_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
