"""Unauthenticated bounded public metadata GETs, no mutation or credentials."""
import concurrent.futures,datetime,gzip,json,pathlib,urllib.parse,urllib.request
O=pathlib.Path(__file__).resolve().parent
Q={932:'"Stoker" AND "tensegrities"',967:'"Kourovka" AND "21.107"',1036:'"A Topologically Convex Vertex-Ununfoldable Polyhedron"',1063:'"Infinite geometric lattices of finite rank have matchings"',1170:'"Tokengrinder" AND "factorial"',1182:'"A Proposed Solution to Erdos Problem 486"',1183:'"Gessel" AND "density-doubling"',1184:'"STARFLEET" AND "538"',1189:'"Freud" AND "Adding Numbers"',1190:'"Blair" AND "730"',1224:'"Tao" AND "Sieving by coprime numbers"'}
def run(z):
 pr,q=z;records=[];ids=set();total=None;at=datetime.datetime.now(datetime.timezone.utc).isoformat();result={'pr':pr,'query':q,'started_at':at,'pages':[]}
 try:
  for page in range(1,11):
   url='https://zenodo.org/api/records?'+urllib.parse.urlencode({'q':q,'size':25,'page':page,'sort':'mostrecent'})
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-source-accounting-readonly-audit/1.0','Accept':'application/json'}),timeout=40)as r:
    body=r.read(2*1024*1024+1);assert len(body)<=2*1024*1024
   raw=json.loads(body);hits=raw['hits']['hits'];t=raw['hits']['total'];t=t['value']if isinstance(t,dict)else t
   assert total is None or total==t;total=t
   new=[str(x['id'])for x in hits];assert not ids.intersection(new);ids.update(new);records+=hits
   dest=O/f'public_{pr}_{page}.json.gz';dest.write_bytes(gzip.compress(body,mtime=0));result['pages'].append(dest.name)
   if len(ids)>=total or not hits:break
  result.update(total=total,complete=len(ids)==total,ids=sorted(ids),records=records)
 except Exception as e:result.update(complete=False,error=type(e).__name__+': '+str(e),ids=sorted(ids),records=records)
 result['ending_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:r=list(ex.map(run,Q.items()))
(O/'PUBLIC_QUERY_RESULTS.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps([{k:v for k,v in x.items()if k!='records'}for x in r],indent=2))
