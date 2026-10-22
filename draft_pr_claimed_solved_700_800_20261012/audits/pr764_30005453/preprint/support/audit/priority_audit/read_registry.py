#!/usr/bin/env python3
"""Bounded read-only official-registry queries. No credential use or writes."""
from pathlib import Path
import urllib.request, urllib.parse, urllib.error, json, hashlib, datetime
BASE=Path(__file__).resolve().parent
QUERIES=[
 ('zenodo','"weakly reinforced"'),
 ('zenodo','"homogenization" AND "urn"'),
 ('zenodo','"WARM" AND "urn"'),
 ('zenodo','"30005453"'),
 ('zenodo','"graph-based" AND "reinforced"'),
 ('datacite','"weakly reinforced"'),
 ('datacite','"homogenization" AND "urn"'),
 ('datacite','"30005453"'),
 ('crossref','Long-time behavior of graph-based weakly reinforced Polya urns'),
 ('crossref','Homogenization weakly reinforced Polya urns countable networks'),
 ('arxiv','ti:"weakly reinforced"'),
]
def request(source,q):
 params={'zenodo':{'q':q,'size':25,'page':1},'datacite':{'query':q,'page[size]':25},'crossref':{'query.bibliographic':q,'rows':20},'arxiv':{'search_query':q,'start':0,'max_results':25}}[source]
 endpoint={'zenodo':'https://zenodo.org/api/records','datacite':'https://api.datacite.org/dois','crossref':'https://api.crossref.org/works','arxiv':'https://export.arxiv.org/api/query'}[source]
 url=endpoint+'?'+urllib.parse.urlencode(params)
 rec={'source':source,'query':q,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical priority audit (read-only primary-source verification)','Accept':'application/json' if source!='arxiv' else 'application/atom+xml'})
  with urllib.request.urlopen(req,timeout=25) as s: data=s.read();rec.update(http_status=s.status,response_sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
  if source=='arxiv':
   import xml.etree.ElementTree as ET
   root=ET.fromstring(data);ns={'a':'http://www.w3.org/2005/Atom','o':'http://a9.com/-/spec/opensearch/1.1/'}
   rec['total']=root.findtext('o:totalResults',namespaces=ns);rec['hits']=[{'id':x.findtext('a:id',namespaces=ns),'title':x.findtext('a:title',namespaces=ns),'published':x.findtext('a:published',namespaces=ns),'updated':x.findtext('a:updated',namespaces=ns)} for x in root.findall('a:entry',ns)]
  else:
   obj=json.loads(data)
   if source=='zenodo':
    rec['total']=obj['hits']['total'];rec['hits']=[{k:x.get(k) for k in ['id','doi','created','updated']} | {'metadata':{k:x['metadata'].get(k) for k in ['title','publication_date','version','resource_type','upload_type','related_identifiers','keywords']}, 'creators':[{'name':y.get('name')} for y in x['metadata'].get('creators',[])]} for x in obj['hits']['hits']]
   elif source=='datacite':rec['total']=obj.get('meta',{}).get('total');rec['hits']=[{'id':x['id'],'attributes':{k:x['attributes'].get(k) for k in ['titles','creators','publisher','publicationYear','dates','url','created','registered','published','relatedIdentifiers']}} for x in obj.get('data',[])]
   else:rec['total']=obj['message'].get('total-results');rec['hits']=[{k:x.get(k) for k in ['DOI','title','author','created','deposited','published','published-online','issued','link','URL']} for x in obj['message'].get('items',[])]
 except urllib.error.HTTPError as e:rec.update(http_status=e.code,error=str(e))
 except Exception as e:rec['error']=repr(e)
 return rec
if __name__=='__main__':
 out=[]
 for source,q in QUERIES:
  rec=request(source,q);out.append(rec);print(source,q,'status',rec.get('http_status'),'total',rec.get('total'),'hits',len(rec.get('hits',[])),flush=True)
  BASE.joinpath('REGISTRY_SEARCH.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
