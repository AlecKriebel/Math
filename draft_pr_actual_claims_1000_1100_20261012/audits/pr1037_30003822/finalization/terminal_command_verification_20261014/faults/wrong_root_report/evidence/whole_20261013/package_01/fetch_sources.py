from pathlib import Path
import urllib.request,hashlib,json,datetime,concurrent.futures
out=Path(__file__).parent/'sources';raw=out/'raw'
urls={'CSS_v2.pdf':'https://arxiv.org/pdf/0706.1509v2','Sportiello.pdf':'https://pcteserver.mi.infn.it/~caraccio/PhD/Sportiello.pdf','KW_v4.pdf':'https://arxiv.org/pdf/math/0608422v4','CJSSS.pdf':'https://arxiv.org/pdf/cond-mat/0403271','Ferudun.html':'https://eulersolve.org/papers/owr-16164-020/','DataCite.json':'https://api.datacite.org/dois/10.5281/zenodo.23298482','PR1037.json':'https://api.github.com/repos/AlecKriebel/Math/pulls/1037','commit.json':'https://api.github.com/repos/AlecKriebel/Math/commits/e87236a97c4b87818d2768cd5789043c7c3f4e39','SNS.html':'https://ricerca.sns.it/handle/11384/85875'}
def fetch(x):
 name,url=x;stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical package audit'}),timeout=60) as r:data=r.read();final=r.url;status=r.status
  (raw/name).write_bytes(data)
  return {'name':name,'url':url,'resolved_url':final,'utc':stamp,'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
 except Exception as e:return {'name':name,'url':url,'utc':stamp,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:rows=list(e.map(fetch,urls.items()))
(out/'SOURCE_FETCHES.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
