from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2]/'sources/primary'; C=R/'.cache'; C.mkdir(parents=True,exist_ok=True)
(R/'.gitignore').write_text('.cache/\n')
items=[
('dgp-published','https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.612.pdf'),
('dgp-v1','https://arxiv.org/pdf/2008.05352v1'),
('ss-v1','https://arxiv.org/pdf/1705.00377v1'),
('ll-v3','https://arxiv.org/pdf/1602.05094v3'),
('dsii-v1','https://arxiv.org/pdf/1507.05082v1'),
('sga2','https://arxiv.org/pdf/math/0511279'),
('hacon-kv','https://www.math.utah.edu/~hacon/7800/Math7800-2018.pdf'),
('serre-gaga','https://www.numdam.org/article/AIF_1956__6__1_0.pdf'),
('fujita-preview','https://link.springer.com/content/pdf/10.1007/BFb0083337.pdf'),
('lwx-v4','https://arxiv.org/pdf/1411.0761v4'),
('oss-v3','https://arxiv.org/pdf/1210.0858v3'),
('pw-v2','https://arxiv.org/pdf/alg-geom/9306010v2'),
('spotti-thesis','https://arxiv.org/pdf/1211.5334'),
('vcoev-v3','https://arxiv.org/pdf/0806.3728v3'),
('cs-published','https://msp.org/gt/2019/23-3/gt-v23-n3-p05-p.pdf'),
('kszz-current','https://drive.google.com/uc?export=download&id=1eB16wLGE2G5QrbV-pUDmw_ieLMiLlOcO'),
('kszz-author-page','https://sites.google.com/uic.edu/jzhao/research'),
('stacks-0BEM','https://stacks.math.columbia.edu/tag/0BEM'),
('stacks-0BEL','https://stacks.math.columbia.edu/tag/0BEL'),
('oai-gap-pinned','https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-ordinary-double-point-gap-in-every-dimension-September-24-2026/paper.pdf'),
('oai-four-pinned','https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-normalized-volume-gap-in-dimension-four-September-24-2026/paper.pdf'),
('liu-xu','https://arxiv.org/pdf/1706.01933'),
('liu-four-v2','https://arxiv.org/pdf/2007.14320v2'),
('hoering-current','https://math.univ-cotedazur.fr/u/hoering/articles/a57-fano-split-tangent.pdf')]
def get(it):
 n,u=it; d={'id':n,'request_url':u,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  with urlopen(Request(u,headers={'User-Agent':'Research source scope review'}),timeout=70) as z:
   b=z.read(25*1024*1024); d.update(status=z.status,final_url=z.url,headers=dict(z.headers))
  ext='.pdf' if b.startswith(b'%PDF-') else '.html'; p=C/(n+ext);p.write_bytes(b)
  d.update(path=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),is_pdf=ext=='.pdf')
  if ext=='.pdf':
   q=C/(n+'.txt'); a=subprocess.run(['pdftotext','-layout',str(p),str(q)],capture_output=True,text=True);d.update(extraction_exit=a.returncode,text_path=str(q.resolve()),text_sha256=hashlib.sha256(q.read_bytes()).hexdigest() if q.exists() else None)
 except Exception as e: d.update(error=repr(e))
 print(n,d.get('status'),d.get('bytes'),d.get('error'),flush=True)
 return d
with ThreadPoolExecutor(max_workers=6) as ex: receipts=list(ex.map(get,items))
(R/'transport_receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
