"""Fresh read-only primary acquisition; all third-party bytes stay private."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime, hashlib, json, subprocess

A=Path(__file__).resolve().parent;R=A/'raw_sources';R.mkdir(exist_ok=True)
items=[
 ('owr2022-22.pdf','https://ems.press/content/serial-article-files/46961','b94a5ab624e47ddb3db11370099db7ef4bf30acfc2f0993d5c365c2795ff6d79'),
 ('lmr-feasible.pdf','https://homepages.math.uic.edu/~mubayi/papers/XizhiReiherInduced.pdf','f9b7951b9926ffba50a886226fbe0ab4715cfdccffaf5c92e00f8eee783a270c'),
 ('semi2026.pdf','https://homepages.math.uic.edu/~mubayi/papers/Semi_Inducibility.pdf','e178ea4009a84fbe6a3da2959ee1ccead2fe598f19b490f4755c0b7140bc60f7'),
 ('pikhurko-razborov2017.pdf','https://pikhurko.github.io/E/PikhurkoRazborov17cpc.pdf','049c2c9a40579d8b0495b74d723c05ef269233e851c207dbf41234576dfc0101'),
 ('cograph-terminology2024.pdf','https://dmtcs.episciences.org/13878/pdf','60225bbd9266276d6a0ffd852f9f218fea0e963c95341a57b4bb6b7349100b6d')]
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
