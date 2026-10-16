"""Retrieve public primary sources into memory; retain only receipts and scope."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime,hashlib,json,subprocess,urllib.request

ROOT=Path(__file__).resolve().parent
URLS=[
('Qin_v1_abs','https://arxiv.org/abs/2610.11780v1'),
('Qin_v1_html','https://arxiv.org/html/2610.11780v1'),
('OWR','https://ems.press/content/serial-article-files/47008'),
('MATRIX_prepublication','https://www.matrix-inst.org.au/wp_Matrix2016/wp-content/uploads/2023/Aletti.pdf'),
('CH_v2','https://arxiv.org/html/2010.03347v2'),
('WARM_v1','https://arxiv.org/pdf/1406.0449v1'),
('thesis','https://www.theorie.physik.uni-muenchen.de/TMP/theses/couziniethesis.pdf'),
('PR764','https://api.github.com/repos/AlecKriebel/Math/pulls/764'),
]

def fetch(item):
    key,url=item
    rec={'key':key,'requested_url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Independent-research-verification/1.0'})
        with urllib.request.urlopen(req,timeout=45) as response:
            raw=response.read();rec.update({'status':response.status,'final_url':response.url,'content_type':response.headers.get('Content-Type'),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        if raw.startswith(b'%PDF-'):
            text=subprocess.run(['pdftotext','-','-'],input=raw,capture_output=True,check=True).stdout
            rec['extracted_text_sha256']=hashlib.sha256(text).hexdigest()
        if key=='PR764':
            data=json.loads(raw)
            rec['observed_public_fields']={k:data.get(k) for k in ['html_url','state','draft','created_at','updated_at','merged_at']}
            rec['observed_public_fields']['head_sha']=data.get('head',{}).get('sha')
    except Exception as exc:
        rec['error']=str(exc)
    return rec

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=4) as pool: records=list(pool.map(fetch,URLS))
    result={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Standard public GET; bodies held only in memory and not redistributed. Browser web tool independently supplied readable primary text. No access-denial bypass.','retrievals':records}
    (ROOT/'PRIMARY_RETRIEVAL_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
