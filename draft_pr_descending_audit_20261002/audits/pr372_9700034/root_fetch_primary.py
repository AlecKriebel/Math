"""Fresh source acquisition; source locators only, prior to candidate mathematics."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,datetime,subprocess
A=Path(__file__).resolve().parent;R=A/'raw_sources';R.mkdir(exist_ok=True)
items=json.loads((A/'snapshot/problems/9700034_sirsn_maximal_routes/SOURCE_MANIFEST.json').read_bytes())['files']
def acquire(item):
 name=item['name'];p=R/name;assert not p.exists()
 r=subprocess.run(['/usr/bin/curl','-L','--fail','--silent','--show-error','--dump-header',str(R/(name+'.headers')),'--output',str(p),'--write-out','%{http_code}\n%{url_effective}\n',item['url']],capture_output=True)
 (A/('root_'+name+'.download.stdout')).write_bytes(r.stdout);(A/('root_'+name+'.download.stderr')).write_bytes(r.stderr);assert r.returncode==0,(name,r.stderr.decode())
 b=p.read_bytes();h=hashlib.sha256(b).hexdigest();row={'file':name,'url':item['url'],'http_observation':r.stdout.decode().splitlines(),'bytes':len(b),'sha256':h,'pinned_bytes':item['bytes'],'pinned_sha256':item['sha256'],'pinned_exact':len(b)==item['bytes'] and h==item['sha256']}
 if name.endswith('.pdf'):
  assert b.startswith(b'%PDF-');x=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(p),str(R/(name+'.txt'))],capture_output=True);(A/('root_'+name+'.extract.stdout')).write_bytes(x.stdout);(A/('root_'+name+'.extract.stderr')).write_bytes(x.stderr);assert x.returncode==0;row.update(extract_exit=x.returncode,extract_stderr_bytes=len(x.stderr))
 return row
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(acquire,items))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':rows,'passages_read_pending':True,'raw_extract_render_private':True,'source_first_before_candidate_proofs_programs_receipts_or_reviews':True}
(A/'root_primary_source_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
