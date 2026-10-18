from pathlib import Path
import datetime,hashlib,json,subprocess,urllib.request
HERE=Path(__file__).resolve().parent
SRC=HERE.parent/'sources';SRC.mkdir(exist_ok=True)
items=[('costakis2008.pdf','https://ems.press/content/serial-article-files/46147'),('nikula2012v1.pdf','https://arxiv.org/pdf/1209.6209v1'),('bayart_matheron2011v1.pdf','https://arxiv.org/pdf/1112.1289v1'),('nikula2012v1_record.html','https://arxiv.org/abs/1209.6209v1'),('bayart_matheron2011v1_record.html','https://arxiv.org/abs/1112.1289v1'),('nikula_crossref.json','https://api.crossref.org/works/10.1007/s11785-013-0328-0'),('bayart_matheron_crossref.json','https://api.crossref.org/works/10.1515/crelle-2014-0002')]
receipt=[]
for name,url in items:
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent-Math-Package-Review/1.0'})
  with urllib.request.urlopen(req,timeout=45) as r:data=r.read();final=r.url
  p=SRC/name;p.write_bytes(data)
  item={'url':url,'final_url':final,'file':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
  if name.endswith('.pdf'):
   subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
  if name.endswith('_crossref.json'):
   m=json.loads(data)['message'];item['metadata']={k:m.get(k) for k in ['DOI','title','author','publisher','volume','issue','page','published-online','published-print']}
  receipt.append(item)
 except Exception as e:receipt.append({'url':url,'error':str(e)})
(HERE/'primary_sources.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
