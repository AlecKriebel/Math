from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime as dt,hashlib,json,subprocess,urllib.request
Q=Path(__file__).resolve().parent
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
sources=[
('628_original','https://publications.mfo.de/bitstream/handle/mfo/2936/OWR_2006_06.pdf?isAllowed=y&sequence=1','803471040d06fcc1f83d5a0bd605e72bfd3a61434ee2a3dcd5259c48e2869412','Original pp325-328; fixed-target coarse point and universal bound only.'),
('628_bresciani_divisor','https://arxiv.org/pdf/2211.03438v1','712012ee8faa1ca54a858031ae4f3a864d8a82c14a2ac28523af8a678f576738','Proposition2 pp3-4 and Lemma11 pp7-8; disposition evidence check, not new historical-priority survey.'),
('628_bresciani_structures','https://arxiv.org/pdf/2303.01409v2','ec3c50004c1576c0f7110be426e9ae43f13f6138412d9257a9c17f23a9f7dd03','Theorem2 and Lemma6; faithful-family and compression mechanism.'),
('628_huggins','https://arxiv.org/pdf/math/0407088v1','126b76a8fd3320030f7a801cd6a72d12c8eed84756ed87c9e1ba697adcbbe8a2','Lemma5.5/Proposition5.6 pp11-12; existing lower-bound mechanism.'),
('630_original','https://ems.press/content/serial-article-files/46093?nt=1','d38624e71305f8fbd26b92a7903e8d7fb57c22c24763409b1a7126887ba10496','Printed pp502-503, definition and TheoremH/question; no nonzero-a assumption.'),
('630_older_example','https://www.impan.pl/shop/en/publication/transaction/download/product/84815','7a5c5d254a756742a1ade67b5b10ad925a7e0f2eec1384b69bea6d0585a6c45d','Printed pp67-69, Example1; its additional predicate differs from target.'),
('662_original','https://arxiv.org/pdf/1809.07200v2',None,'Printed pp114 and147, Problem6.86; qualitative fixed-point interpretation only, no firstness.')]
def fetch(source):
 key,url,expected,scope=source;req=urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-source-custody/1.0'})
 with urllib.request.urlopen(req,timeout=45) as resp:b=resp.read();http=dict(status=resp.status,final_url=resp.url)
 if not b.startswith(b'%PDF-') or expected is not None and sha(b)!=expected:raise RuntimeError('Fresh primary source differs '+key)
 dest=Q/'private/fresh_sources'/f'{key}.pdf';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);text=subprocess.run(['pdftotext','-layout',str(dest),'-'],capture_output=True,check=True).stdout;dest.with_suffix('.txt').write_bytes(text)
 return dict(key=key,url=url,at=now(),bytes=len(b),sha256=sha(b),expected_sha256=expected,exact_prior_source_match=sha(b)==expected if expected else None,http=http,read_scope=scope,text_sha256=sha(text))
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,sources))
(Q/'fresh_primary_source_receipts.json').write_text(json.dumps(dict(at=now(),sources=results,scope='Direct fresh source and bounded locators for disposition/coverage; no exhaustive science/priority audit.'),indent=2)+'\n')
print(json.dumps(dict(primary_PDFs=len(results),exact_prior_source_matches=sum(x['exact_prior_source_match'] is True for x in results))))
