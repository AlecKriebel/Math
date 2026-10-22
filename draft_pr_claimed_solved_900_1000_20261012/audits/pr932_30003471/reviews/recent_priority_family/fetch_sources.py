import pathlib,urllib.request,hashlib,json,datetime,concurrent.futures
OUT=pathlib.Path(__file__).parent; PR=OUT/'private_sources'
SOURCES={'Bi':'2608.06320v1','WXY3':'2606.30130v1','WXY':'2112.01510v6','WX':'2203.09511v2','BHS':'2202.05180v2','Brendle':'2301.05087v4','BW':'2308.08000v2'}
def fetch(item):
 key,ident=item; rows=[]
 for kind,url in [('abs','https://arxiv.org/abs/'+ident.split('v')[0]),('pdf','https://arxiv.org/pdf/'+ident)]:
  start=datetime.datetime.now(datetime.timezone.utc).isoformat(); req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematics research audit/1.0'})
  try:
   with urllib.request.urlopen(req,timeout=50) as r: b=r.read(); final=r.url; ct=r.headers.get('Content-Type')
   p=PR/(key+'_'+ident+('.html' if kind=='abs' else '.pdf'));p.write_bytes(b)
   rows.append({'source':key,'id':ident,'kind':kind,'url':url,'final_url':final,'retrieved_utc':start,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'content_type':ct,'private_path':str(p.relative_to(OUT))})
  except Exception as e: rows.append({'source':key,'id':ident,'kind':kind,'url':url,'retrieved_utc':start,'error':str(e)})
 return rows
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool: rows=[r for rs in pool.map(fetch,SOURCES.items()) for r in rs]
(OUT/'SOURCE_RETRIEVAL.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
