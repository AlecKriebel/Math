"""Public scholarly retrieval only; foreign response bytes stay in ignored sources/.

Run from any cwd with Python 3. No closed audit or shared-state writes occur.
Receipts retain wrong-format responses and HTTP failures, not just successes.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import datetime, hashlib, json, subprocess

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / 'sources'
SOURCES.mkdir(exist_ok=True)
ITEMS = [
 ('question.tex','https://www.imo.universite-paris-saclay.fr/~pansu/problems_MTDG.tex'),
 ('fv2018.pdf','https://arxiv.org/pdf/1804.11096v1'),
 ('fv2020_author_response.html','https://www.researchgate.net/publication/340658748_Flag_structures_on_real_3-manifolds'),
 ('fv2020_publisher_response.pdf','https://link.springer.com/content/pdf/10.1007/s10711-020-00528-4.pdf'),
 ('fv2020_rg_pdf_response.pdf','https://www.researchgate.net/publication/profile/Jose-Veloso-2/publication/340658748_Flag_structures_on_real_3-manifolds/links/5e9c88ef4585150839ebc0b1/Flag-structures-on-real-3-manifolds.pdf'),
 ('duchamp.pdf','https://sites.math.washington.edu/~duchamp/preprints/totally-real.pdf'),
 ('forstneric1986.pdf','https://users.fmf.uni-lj.si/forstneric/papers/1986Expositiones.pdf'),
 ('borrelli2002.ps','https://math.univ-lyon1.fr/~borrelli/Articles/IMRN2002.ps'),
 ('koshkin_journal.pdf','https://tcms.org.ge/Journals/JHRS/xvolumes/2009/n1a16/v4n1a16.pdf'),
 ('global2023.pdf','https://arxiv.org/pdf/2306.17705v1'),
 ('reductions2024.pdf','https://arxiv.org/pdf/2406.11509v1'),
 ('reductions_accepted.pdf','https://personal-homepages.mis.mpg.de/mionmouton/reduction-final.pdf'),
 ('surgeries2024.pdf','https://arxiv.org/pdf/2406.02053v1'),
 ('surgeries_accepted.pdf','https://www.i2m.univ-amu.fr/perso/martin.mion-mouton/varietesdrapeauxnonKleiniennes-accepted.pdf'),
 ('automorphisms2021.pdf','https://arxiv.org/pdf/2105.02090v1'),
 ('configurations2018.pdf','https://arxiv.org/pdf/1802.10315v1'),
 ('derdzinski_tams.pdf','https://people.math.osu.edu/derdzinski.1/preprints/tams10.pdf'),
 ('derdzinski_pjm.pdf','https://math.osu.edu/~derdzinski.1/preprints/pjm.pdf'),
]

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(item):
    name,url=item
    receipt={'name':name,'requested_url':url,'started_utc':utc()}
    try:
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 (independent mathematical source audit)'}),timeout=55) as response:
            data=response.read()
            receipt.update(status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type'))
    except HTTPError as exc:
        data=exc.read()
        receipt.update(status=exc.code,final_url=exc.url,content_type=exc.headers.get('Content-Type'),error=str(exc))
    except Exception as exc:
        data=b''
        receipt.update(error=repr(exc))
    (SOURCES/name).write_bytes(data)
    receipt.update(finished_utc=utc(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),is_pdf=data.startswith(b'%PDF-'))
    if receipt['is_pdf']:
        out=SOURCES/(Path(name).stem+'.txt')
        process=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(SOURCES/name),str(out)],capture_output=True,text=True)
        receipt['text_extraction']={'exit':process.returncode,'stderr':process.stderr,'path':out.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(out.read_bytes()).hexdigest() if out.exists() else None}
    return receipt

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=8) as pool:
        receipts=list(pool.map(fetch,ITEMS))
    (ROOT/'FRESH_SOURCE_RECEIPTS.json').write_text(json.dumps({'generated_utc':utc(),'receipts':receipts},indent=2)+'\n')
    print(json.dumps([{'name':x['name'],'status':x.get('status'),'bytes':x['bytes'],'pdf':x['is_pdf'],'error':x.get('error')} for x in receipts],indent=2))
