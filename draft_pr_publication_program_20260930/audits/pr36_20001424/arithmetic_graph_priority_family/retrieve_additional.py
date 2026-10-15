from pathlib import Path
from urllib.request import urlopen
import datetime,json,hashlib,subprocess
D=Path(__file__).resolve().parent;F=D/'tmp'/'foreign_sources'
sources={'goodman_hawkins.pdf':'https://www.ams.org/journals/ecgd/2014-18-06/S1088-4173-2014-00265-3/S1088-4173-2014-00265-3.pdf','milnor_bicritical.pdf':'https://arxiv.org/pdf/math/9709226','milnor_abs.html':'https://arxiv.org/abs/math/9709226','bresciani_uniform.pdf':'https://arxiv.org/pdf/2405.03621','bresciani_uniform_abs.html':'https://arxiv.org/abs/2405.03621','bbm.pdf':'https://arxiv.org/pdf/1512.01850','bbm_abs.html':'https://arxiv.org/abs/1512.01850','cordwell_ams.html':'https://www.ams.org/journals/ecgd/2015-19-11/S1088-4173-2015-00275-1/','silverman_metadata.html':'https://www.numdam.org/item/CM_1995__98_3_269_0/'}
receipts=[]
for name,url in sources.items():
 r={'name':name,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  response=urlopen(url,timeout=30);body=response.read();(F/name).write_bytes(body);r.update(status=response.status,final_url=response.url,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),headers=dict(response.headers))
  if name.endswith('.pdf'):r['pdftotext']=subprocess.run(['pdftotext','-layout',str(F/name),str((F/name).with_suffix('.txt'))],capture_output=True,text=True).returncode
 except Exception as e:r['error']=repr(e)
 receipts.append(r);(D/'ADDITIONAL_RETRIEVAL_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n');print(name,r.get('status'),r.get('bytes'),r.get('error'),flush=True)
