#!/usr/bin/env python3
import pathlib,json,urllib.request,datetime,hashlib,concurrent.futures
W=pathlib.Path(__file__).resolve().parent

def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Independent bounded publication-integrity review (read-only)'})
 with urllib.request.urlopen(req,timeout=60) as r:return r.read(),r.status,r.url,dict(r.headers)
def one(n):
 c=json.loads((W/'inputs'/f'PR{n:04}_PUBLICATION_COVERAGE_DETAILS.json').read_text()); record=c['record'];p=W/'downloads_private'/str(n);p.mkdir(exist_ok=True)
 raw,status,url,headers=get(f'https://zenodo.org/api/records/{record}');(p/'record.json').write_bytes(raw);j=json.loads(raw)
 out={'pr':n,'record':record,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'metadata_status':status,'metadata_url':url,'metadata_sha256':hashlib.sha256(raw).hexdigest(),'published':j.get('is_published',j.get('status')),'doi':j['doi'],'title':j['metadata']['title'],'description':j['metadata'].get('description'),'files':[]}
 try:
  raw,status,url,headers=get('https://doi.org/'+c['doi']);(p/'doi_landing.html').write_bytes(raw);out['doi_resolution']={'status':status,'url':url,'sha256':hashlib.sha256(raw).hexdigest()}
 except Exception as ex:out['doi_resolution']={'error':str(ex)}
 for f in j['files']:
  key=f['key'];body,st,fu,fh=get(f['links']['self']);(p/key).write_bytes(body);expected=next((x for x in c['public_files'] if x['name']==key),None)
  out['files'].append({'name':key,'url':fu,'status':st,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'provider_checksum':f.get('checksum'),'provider_bytes':f.get('size'),'provider_checksum_equal':f.get('checksum')=='md5:'+hashlib.md5(body).hexdigest(),'expected_receipt_equal':expected is not None and expected['bytes']==len(body) and expected['sha256']==hashlib.sha256(body).hexdigest()})
 return out
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:
  out=list(e.map(one,[883,885,888,894,904,905]))
 (W/'PUBLIC_FETCH_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
 for x in out:print(x['pr'],x['doi'],x['doi_resolution'],[(f['name'],f['bytes'],f['provider_checksum_equal'],f['expected_receipt_equal']) for f in x['files']])
