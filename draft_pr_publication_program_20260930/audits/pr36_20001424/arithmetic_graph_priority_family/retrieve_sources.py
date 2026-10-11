from pathlib import Path
from urllib.request import urlopen,Request
import datetime,json,hashlib,subprocess
D=Path(__file__).resolve().parent; F=D/'tmp'/'foreign_sources'; F.mkdir(parents=True,exist_ok=True)
sources={
'silverman1995.pdf':'https://www.numdam.org/article/CM_1995__98_3_269_0.pdf',
'hidalgo_quispe.pdf':'https://arxiv.org/pdf/1502.05306',
'hidalgo_quispe_v1.pdf':'https://arxiv.org/pdf/1502.05306v1',
'cordwell.pdf':'https://arxiv.org/pdf/1308.5895',
'cordwell_v1.pdf':'https://arxiv.org/pdf/1308.5895v1',
'hlushchanka_v1.pdf':'https://arxiv.org/pdf/1904.04759v1',
'hidalgo_abs.html':'https://arxiv.org/abs/1502.05306',
'cordwell_abs.html':'https://arxiv.org/abs/1308.5895',
'hlushchanka_abs.html':'https://arxiv.org/abs/1904.04759',
'bresciani_abs.html':'https://arxiv.org/abs/2405.03612',
'aim.html':'http://aimpl.org/finitedynamics/2/'
}
receipts=[]
for name,url in sources.items():
 r={'name':name,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  response=urlopen(url,timeout=30); body=response.read();(F/name).write_bytes(body)
  r.update(status=response.status,final_url=response.url,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),headers=dict(response.headers))
  if name.endswith('.pdf'):r['pdftotext']=subprocess.run(['pdftotext','-layout',str(F/name),str((F/name).with_suffix('.txt'))],capture_output=True,text=True).returncode
 except Exception as e:r['error']=repr(e)
 receipts.append(r)
 (D/'RETRIEVAL_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
 print(name,r.get('status'),r.get('bytes'),r.get('error'),flush=True)
