from pathlib import Path
from urllib.request import Request, urlopen
import datetime, hashlib, json, subprocess

BASE=Path(__file__).parent
SOURCES=BASE/'private_sources'
URLS=[
 ('cable_trench_2025.pdf','https://link.springer.com/content/pdf/10.1007/s10878-025-01289-0.pdf'),
 ('cable_trench_arxiv_abs.html','https://arxiv.org/abs/2312.13810'),
 ('optima85.pdf','https://mathopt.zib.de/Optima-Issues/optima85.pdf'),
 ('kaibel_ovgu.html','https://www.ovgu.de/Kaibel.html?rewrite_engine=fast'),
 ('kaibel_discopt.html','https://discopt.ovgu.de/people/kaibel.php'),
 ('dellamico_maffioli_1996_repository.html','https://iris.unimore.it/handle/11380/451178'),
 ('dellamico_maffioli_1996_publisher.html','https://www.sciencedirect.com/science/article/pii/0166218X9500035P'),
 ('owr_metadata.html','https://ems.press/journals/owr/articles/16633'),
 ('combining_linear_nonlinear_preprint.pdf','https://iris.unimore.it/retrieve/bcf0f9f5-acc8-4d58-b733-f27ac638a63a/0186.pdf'),
]

def main():
 record=BASE/'RETRIEVALS.json'
 receipts=json.loads(record.read_text()) if record.exists() else []
 for filename,url in URLS:
  p=SOURCES/filename
  rec={'requested_url':url,'file':str(p.relative_to(BASE)),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
  try:
   with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:
    data=r.read();rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
   p.write_bytes(data)
   rec.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),is_pdf=data.startswith(b'%PDF-'))
   if rec['is_pdf']:
    out=p.with_suffix('.txt')
    subprocess.run(['pdftotext','-layout',str(p),str(out)],check=True)
    rec['text_file']=str(out.relative_to(BASE))
  except Exception as e:
   rec['error']=repr(e)
  receipts.append(rec)
  print(json.dumps(rec))
 record.write_text(json.dumps(receipts,indent=2)+'\n')

if __name__=='__main__':main()
