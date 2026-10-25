from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,datetime,subprocess

BASE=Path(__file__).resolve().parents[2];OUT=BASE/'reviews/scope';CACHE=OUT/'cache/primary-sources';CACHE.mkdir(parents=True,exist_ok=True)
ledger=json.loads((BASE/'sources/published-source/SOURCE_LEDGER.json').read_text())
ids={'FL_v3','Farrell_thesis','Abelian_logic_v2','Stockmeyer_Meyer','Gramlich_2003','Eriksson_AMS','Dusart_2010','Abelian_II','GRM_journal','Esparza_survey'}
# Only raw bibliographic fields are used, never historical review consequences.
todo=[{k:q.get(k) for k in ['citation_id','authors','title','url','edition','sha256']} for q in ledger['sources'] if q['citation_id'] in ids]
def fetch(q):
    try:
        with urlopen(Request(q['url'],headers={'User-Agent':'Mozilla/5.0 ResearchSourceCheck'}),timeout=45) as resp: data=resp.read();resolved=resp.url
        if not data.startswith(b'%PDF'): raise ValueError('Response is not PDF')
        p=CACHE/(q['citation_id']+'.pdf');p.write_bytes(data)
        subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True,capture_output=True)
        inf=subprocess.check_output(['pdfinfo',str(p)],text=True)
        sha=hashlib.sha256(data).hexdigest()
        return {**q,'published_ledger_sha256':q['sha256'],'sha256':sha,'matches_published_ledger':sha==q['sha256'],'resolved_url':resolved,'bytes':len(data),'pages':int(next(l for l in inf.splitlines() if l.startswith('Pages:')).split(':',1)[1]),'path':str(p),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'retrieved'}
    except Exception as e:return {**q,'status':'unavailable','error':str(e),'attempted_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with ThreadPoolExecutor(max_workers=6) as ex: results=list(ex.map(fetch,todo))
(OUT/'primary_source_receipts.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps([{k:q.get(k) for k in ['citation_id','status','pages','matches_published_ledger','error']} for q in results],indent=2))
