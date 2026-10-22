"""Inventory official-domain mentions outside fully spelled HTTP URL tokens."""
import collections,json,re
from pathlib import Path
from urllib.parse import unquote
H=Path(__file__).resolve().parent
account=json.loads((H/'private/source_14_account.json').read_bytes());rows=json.loads((H/'private/source_10_ledger_live.json').read_bytes())['response']['values']
def walk(v,p='$'):
 if isinstance(v,str):yield p,v
 elif isinstance(v,list):
  for i,x in enumerate(v):yield from walk(x,p+'['+str(i)+']')
 elif isinstance(v,dict):
  for k,x in v.items():yield p+'.KEY('+k+')',k;yield from walk(x,p+'.'+k)
items=[]
for r in account['records']:
 for p,v in walk(r):items.append(('account',r['id'],p,v))
for p,v in walk(rows):items.append(('ledger',None,p,v))
non_http=[];count=0
for kind,i,p,v in items:
 for _ in range(8):
  nxt=unquote(v)
  if nxt==v:break
  v=nxt
 urls=list(re.finditer(r'https?://[^\s<>"\x27]+',v,re.I))
 for m in re.finditer(r'(?<![A-Za-z0-9_.-])(?:www\.)?(?:zenodo\.org|shortdoi\.org|(?:dx\.)?doi\.org)\.*[^\s<>"\x27]*',v,re.I):
  count+=1
  if not any(u.start()<=m.start()<u.end() for u in urls):non_http.append({'kind':kind,'id':i,'path':p,'match':m.group(),'context':v[max(0,m.start()-60):m.end()+60]})
r={'official_domain_occurrences':count,'outside_http_url_occurrences':len(non_http),'outside_http_url_contexts':non_http,'scope':'Broad exact official/resolver-domain surface inventory after bounded decoding; no project/helper imports or service activity.'}
(H/'DOMAIN_SURFACE_SUPPLEMENT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
