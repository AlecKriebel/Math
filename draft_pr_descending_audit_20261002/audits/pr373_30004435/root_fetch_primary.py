"""Fresh read-only primary acquisition; all third-party bytes stay private."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime, hashlib, json, subprocess

A=Path(__file__).resolve().parent;R=A/'raw_sources';R.mkdir(exist_ok=True)
items=[('owr_2020_11.pdf', 'https://ems.press/content/serial-article-files/46847', '9dbb5e7b6cd613e3dd111bdb56ce72714d32bb6d1c368d01cdf8c52ec80b07a3'), ('alnajjar_shmaya_2014.pdf', 'https://arxiv.org/pdf/1406.6670', '3b0ee74e13136388c9d557c88861a1d195bc48b1677a87448466a77c3b9f116e'), ('lemanczyk_thesis.pdf', 'https://www.mimuw.edu.pl/media/uploads/doctorates/thesis-michal-lemanczyk.pdf', '811de0919aeeda6f1f3cb79deedf79a878d8849f45191256ab83ba38ba6fbde4'), ('bressaud_fernandez_galves_1999.pdf', 'https://arxiv.org/pdf/math/9806132', '54d177c978932ac1d52bf65a14b898328cb260cb2ed07f6f07f64ff771e3555a')]
def run(item):
    name,url,pinned=item;p=R/name;assert not p.exists(),'Preserve earlier acquisition.'
    r=subprocess.run(['/usr/bin/curl','-L','--fail','--silent','--show-error','--dump-header',str(R/(name+'.headers')),'--output',str(p),'--write-out','%{http_code}\n%{url_effective}\n',url],capture_output=True)
    (A/('root_'+name+'.download.stdout')).write_bytes(r.stdout);(A/('root_'+name+'.download.stderr')).write_bytes(r.stderr)
    assert r.returncode==0 and p.read_bytes().startswith(b'%PDF-'),(name,r.stderr.decode())
    b=p.read_bytes();h=hashlib.sha256(b).hexdigest()
    x=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(p),str(R/(name+'.txt'))],capture_output=True)
    (A/('root_'+name+'.extract.stdout')).write_bytes(x.stdout);(A/('root_'+name+'.extract.stderr')).write_bytes(x.stderr)
    assert x.returncode==0,(name,x.stderr.decode())
    return dict(file=name,url=url,http_observation=r.stdout.decode().splitlines(),bytes=len(b),sha256=h,pinned_sha256=pinned,pinned_exact=h==pinned,extract_exit=x.returncode,extract_stderr_bytes=len(x.stderr))
with ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(run,items))
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=rows,passages_read_pending=True,third_party_raw_extract_render_private=True)
(A/'root_primary_source_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
