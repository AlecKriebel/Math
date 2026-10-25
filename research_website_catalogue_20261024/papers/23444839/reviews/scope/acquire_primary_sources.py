import concurrent.futures,datetime,hashlib,json,pathlib,subprocess,urllib.request
base=pathlib.Path(__file__).parent
out=base/'cache'/'primary-sources';out.mkdir(parents=True,exist_ok=True)
urls={
'nevo-owr-2005':'https://ems.press/content/serial-article-files/45990',
'nevo-arxiv-v2':'https://arxiv.org/pdf/math/0505334v2',
'nevo-published':'https://link.springer.com/content/pdf/10.1007/s00454-007-9017-y.pdf',
'swartz-v1':'https://arxiv.org/pdf/math/0512086v1',
'lsv-v2':'https://arxiv.org/pdf/math/0406217v2',
'lm-author':'https://www.ma.huji.ac.il/~alexlub/PAPERS/a%20Moore%20Bound%20for%20simplicial%20complexes/a%20Moore%20Bound%20for%20simplicial%20complexes.pdf',
'ballmann-swiatkowski':'https://archive.mpim-bonn.mpg.de/id/eprint/2255/1/preprint_1996_127.pdf',
'januszkiewicz-swiatkowski':'https://www.numdam.org/article/PMIHES_2006__104__1_0.pdf',
'larson-stapledon-v2':'https://arxiv.org/pdf/2504.20264v2'}
def one(item):
 name,url=item
 r={'name':name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 research verification'})
  with urllib.request.urlopen(req,timeout=45) as f:
   data=f.read();r['final_url']=f.url
  if not data.startswith(b'%PDF'): raise ValueError('Not PDF')
  path=out/(name+'.pdf');path.write_bytes(data)
  r.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),path=str(path))
  subprocess.run(['pdftotext','-layout',str(path),str(path.with_suffix('.txt'))],check=True)
  r['pdfinfo']=subprocess.check_output(['pdfinfo',str(path)],text=True)
 except Exception as e:r['error']=str(e)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:results=list(ex.map(one,urls.items()))
(base/'primary-source-receipts.json').write_text(json.dumps(results,indent=2)+'\n')
for r in results:print(r['name'],r.get('bytes'),r.get('sha256'),r.get('error'))
