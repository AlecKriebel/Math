#!/usr/bin/env python3
"""Resolve paper/metadata/license links read-only; responses stay ignored."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,urllib.request
HERE=Path(__file__).resolve().parent;PUB=HERE.parents[1]/'publication'
pdf=json.loads((HERE/'PDF_REVIEW.json').read_text());metadata=json.loads((PUB/'zenodo-metadata.json').read_text())
urls={row['uri'] for row in pdf['links'] if 'uri' in row}
urls|={r['identifier'] if r['scheme']=='url' else 'https://doi.org/'+r['identifier'] for r in metadata['related_identifiers']}
urls.add('https://creativecommons.org/licenses/by/4.0/')
def fetch(item):
 i,url=item;row={'url':url,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-package-audit/1.0'})
  with urllib.request.urlopen(req,timeout=35) as response:
   body=response.read();row.update(status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type'),bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
  (HERE/'sources/private'/('link_'+str(i)+'.body')).write_bytes(body)
 except Exception as error:row['error']=type(error).__name__+': '+str(error)
 return row
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(fetch,enumerate(sorted(urls))))
 (HERE/'LINK_CHECK.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n');print(json.dumps(results,indent=2))
