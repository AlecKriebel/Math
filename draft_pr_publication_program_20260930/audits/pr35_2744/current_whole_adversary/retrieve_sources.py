from pathlib import Path
import urllib.request,datetime,hashlib,subprocess,json,concurrent.futures
ROOT=Path(__file__).resolve().parent
sources={
'hp-v2':'https://arxiv.org/pdf/math/0302075v2','boyle-v1':'https://arxiv.org/pdf/2403.07157v1','porti2017':'https://www.numdam.org/item/10.5802/wbln.18.pdf','crs-v3':'https://arxiv.org/pdf/1706.00952v3','crs-v1':'https://arxiv.org/pdf/1706.00952v1','crs-published':'https://par.nsf.gov/servlets/purl/10382294','long-reid':'https://math.rice.edu/~ar99/fields_of_defn_published.pdf','porti-weiss':'https://arxiv.org/pdf/math/0510432','kojima':'https://arxiv.org/pdf/math/9809034','two-bridge':'https://mat.uab.cat/~porti/twobridge040127.pdf','boileau-porti':'https://www.numdam.org/item/AST_2001__272__R1_0.pdf','flat-table':'https://msp.org/agt/2023/23-8/agt-v23-n8-p11-p.pdf','hantzsche-wendt':'https://arxiv.org/pdf/2009.06691','branched-cover':'https://ocu-omu.repo.nii.ac.jp/record/2010740/files/00306126-56-3-497.pdf','dix':'https://escholarship.org/content/qt27j2v475/qt27j2v475_noSplash_7f3e70d717e17eaf9515cffc4ef313be.pdf'}
def retrieve(item):
 name,url=item; o={'name':name,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=45) as r:data=r.read();o.update(final_url=r.url,status=r.status)
  assert data[:4]==b'%PDF'
  p=ROOT/'tmp'/f'{name}.pdf';p.write_bytes(data)
  r=subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],capture_output=True,text=True)
  o.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),text_sha256=hashlib.sha256(p.with_suffix('.txt').read_bytes()).hexdigest(),pdftotext_exit=r.returncode,stderr=r.stderr)
 except Exception as e:o.update(status='FAILED',error=repr(e))
 return o
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:result=list(ex.map(retrieve,sources.items()))
(ROOT/'SOURCE_RETRIEVAL.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
