"""Small primary-source transport receipt. Retains text privately, not full PDFs."""
from pathlib import Path
import urllib.request, subprocess, hashlib, json, datetime
base=Path(__file__).resolve().parent
private=base/'private_reading';private.mkdir(exist_ok=True)
receipts=json.loads((base/'FRESH_PRIMARY_FETCH_RECEIPT.json').read_text()) if (base/'FRESH_PRIMARY_FETCH_RECEIPT.json').exists() else []
for name,url in [('stachel_triple','https://hrcak.srce.hr/file/417316'),('harmonic_v3','https://arxiv.org/pdf/2112.02545v3'),('pedal_curves','https://arxiv.org/pdf/2009.02581'),('ks_landen_v1','https://arxiv.org/pdf/math-ph/0312074v1'),('ks_pramana_final_ias','https://www.ias.ac.in/article/fulltext/pram/063/05/0921-0936'),('ks_pramana_final_springer','https://link.springer.com/content/pdf/10.1007/BF02704331.pdf')]:
 if any(i['id']==name for i in receipts): continue
 item={'id':name,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (primary mathematical literature audit)'})
  with urllib.request.urlopen(req,timeout=40) as r: data=r.read(3500000);item['final_url']=r.url
  item['bytes']=len(data);item['sha256']=hashlib.sha256(data).hexdigest()
  if not data.startswith(b'%PDF'): raise ValueError('Payload is not a PDF')
  result=subprocess.run(['pdftotext','-layout','-','-'],input=data,capture_output=True,check=True)
  out=private/(name+'.txt');out.write_bytes(result.stdout)
  item['private_text_path']=str(out.relative_to(base));item['text_sha256']=hashlib.sha256(result.stdout).hexdigest();item['status']='primary_pdf_fetched_text_retained_only'
 except Exception as e:item['status']='access_failed';item['error']=str(e)
 receipts.append(item)
(base/'FRESH_PRIMARY_FETCH_RECEIPT.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps(receipts,indent=2))
