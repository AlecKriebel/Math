"""Read-only public-source acquisition; copied bodies stay ignored."""
import concurrent.futures, datetime, hashlib, json, pathlib, subprocess, urllib.request
R = pathlib.Path(__file__).resolve().parent
SOURCES = [
 ('FL_v3','https://arxiv.org/pdf/1502.04690v3'),
 ('Farrell_thesis','https://pi.math.cornell.edu/files/Research/SeniorTheses/farrellMatthewThesis.pdf'),
 ('GRM_journal','https://www.combinatorics.org/ojs/index.php/eljc/article/download/v33i2p5/pdf'),
 ('GRM_v2','https://arxiv.org/pdf/2411.18364v2'),
 ('Klivans_book','https://www.dam.brown.edu/people/cklivans/Chip-Firing.pdf'),
 ('Abelian_logic_v2','https://arxiv.org/pdf/1511.00422v2'),
 ('Abelian_II','https://lionellevine.github.io/abelian-networks-II-halting.pdf'),
 ('Hujter_undirected','https://cs.bme.hu/jh2017/jXaio4T11ygd57.pdf'),
 ('BIRS_2015','https://www.birs.ca/cmo-workshops/2015/15w5119/report15w5119.pdf'),
 ('Cairns','https://arxiv.org/pdf/1508.00161'),
 ('HKT_v4','https://arxiv.org/pdf/1507.03209v4'),
]
def one(pair):
 name,url=pair; out=R/'sources/raw'/f'{name}.pdf'; row={'id':name,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mathematical priority audit (public read-only retrieval)'})
  with urllib.request.urlopen(req,timeout=45) as response: data=response.read(); row['effective_url']=response.url
  if not data.startswith(b'%PDF'): raise ValueError('not PDF bytes')
  out.write_bytes(data)
  row.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),status='DOWNLOADED',path=str(out.relative_to(R)))
  dst=R/'sources/extracted'/f'{name}.txt'
  p=subprocess.run(['pdftotext','-layout',str(out),str(dst)],capture_output=True,text=True)
  if p.returncode: raise RuntimeError(p.stderr)
  row.update(text_path=str(dst.relative_to(R)),text_bytes=dst.stat().st_size,text_sha256=hashlib.sha256(dst.read_bytes()).hexdigest())
 except Exception as exc: row.update(status='FAILED',error=str(exc))
 return row
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(one,SOURCES))
 (R/'SOURCE_ACQUISITION.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(json.dumps([{k:r[k] for k in ('id','status','bytes','error') if k in r} for r in rows],indent=2))
