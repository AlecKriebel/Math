from pathlib import Path
from urllib.request import urlopen,Request
import hashlib,json,datetime
from pypdf import PdfReader
base=Path(__file__).parent/'primary'
items={
 'FLO': 'https://offen.net.technion.ac.il/files/2016/09/On.representations.distinguished.by_.unitary.groups.pdf',
 'LM16': 'https://arxiv.org/pdf/1411.6310v3',
 'JPSS': 'https://www.math.columbia.edu/~hj/Rankin%20Selberg%20convolutions.pdf',
 'OWR': 'https://ems.press/content/serial-article-files/46327',
}
records=[]
for key,url in items.items():
 try:
  req=Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urlopen(req,timeout=50) as r: data=r.read(); final=r.url
  if not data.startswith(b'%PDF'): raise ValueError('not PDF')
  path=base/(key+'.pdf');path.write_bytes(data)
  reader=PdfReader(path)
  (base/(key+'.txt')).write_text('\n\n'.join(f'===== PDF PAGE {i+1} =====\n'+(p.extract_text() or '') for i,p in enumerate(reader.pages)))
  records.append({'key':key,'url':url,'final_url':final,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'pages':len(reader.pages)})
 except Exception as e: records.append({'key':key,'url':url,'error':str(e)})
(base/'receipts.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'items':records},indent=2)+'\n')
print(json.dumps(records,indent=2))
