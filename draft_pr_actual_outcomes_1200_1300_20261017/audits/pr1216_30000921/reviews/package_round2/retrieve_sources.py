from pathlib import Path
import urllib.request,hashlib,json,subprocess,datetime
R=Path(__file__).resolve().parent
sources={'nikula_abs':'https://arxiv.org/abs/1209.6209v1','nikula_pdf':'https://arxiv.org/pdf/1209.6209v1','bayart_abs':'https://arxiv.org/abs/1112.1289v1','bayart_pdf':'https://arxiv.org/pdf/1112.1289v1','costakis_pdf':'https://ems.press/content/serial-article-files/46147','nikula_publisher':'https://link.springer.com/article/10.1007/s11785-013-0328-0'}
receipts=[]
for name,url in sources.items():
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source verification/1.0'})
  with urllib.request.urlopen(req,timeout=45) as f:
   data=f.read();resolved=f.url;status=f.status;ctype=f.headers.get('Content-Type')
  suffix='.pdf' if name.endswith('_pdf') else '.html';p=R/'_local/sources'/(name+suffix);p.write_bytes(data)
  if suffix=='.pdf':subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
  receipts.append({'url':url,'resolved':resolved,'status':status,'content_type':ctype,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
 except Exception as e:receipts.append({'url':url,'error':str(e)})
(R/'SOURCE_RECEIPT.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'receipts':receipts,'scope':'Fetched exact primary inputs. Inspected Costakis printed330, Nikula theorem1 pp2-3 and Gaussian p10, Bayart-Matheron settings p1-2/11-15/proof17 and version records. No claim to independent checking every proof of the cited sources.'},indent=2)+'\n')
print(json.dumps(receipts,indent=2))
