#!/usr/bin/env python3
"""Re-fetch primary sources into PRIVATE storage; never publish source bytes."""
import datetime, hashlib, json, pathlib, subprocess, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
URLS = {
    'owr': 'https://ems.press/content/serial-article-files/46961',
    'lmr': 'https://homepages.math.uic.edu/~mubayi/papers/XizhiReiherInduced.pdf',
    'pr': 'https://pikhurko.github.io/E/PikhurkoRazborov17cpc.pdf',
    'semi2026': 'https://homepages.math.uic.edu/~mubayi/papers/Semi_Inducibility.pdf',
    'cograph': 'https://dmtcs.episciences.org/13878/pdf',
}
PAGES = {'owr': [63,64], 'lmr': [1,2,4,10,23], 'pr': [2,3,8,9], 'semi2026':[1,2,3], 'cograph':[18]}
records=[]
for name,url in URLS.items():
    request = urllib.request.Request(url, headers={'User-Agent':'Independent mathematical audit source fetch'})
    with urllib.request.urlopen(request, timeout=90) as response:
        data=response.read()
        headers=dict(response.headers)
        final_url=response.geturl()
    path=ROOT/'private'/'sources'/(name+'.pdf')
    path.write_bytes(data)
    text_path=path.with_suffix('.txt')
    proc=subprocess.run(['pdftotext','-layout',str(path),str(text_path)],capture_output=True,text=True)
    record={'source':name,'url':url,'final_url':final_url,'downloaded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pdf_sha256':hashlib.sha256(data).hexdigest(),'pdf_bytes':len(data),'headers':headers,'extract_exit':proc.returncode,'extract_stdout':proc.stdout,'extract_stderr':proc.stderr}
    if proc.returncode: raise RuntimeError(record)
    record['text_sha256']=hashlib.sha256(text_path.read_bytes()).hexdigest()
    record['renders']=[]
    for page in PAGES[name]:
        prefix=ROOT/'private'/'renders'/f'{name}_p{page:02}'
        proc=subprocess.run(['pdftoppm','-f',str(page),'-singlefile','-scale-to','2000','-png',str(path),str(prefix)],capture_output=True,text=True)
        record['renders'].append({'page':page,'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'sha256':hashlib.sha256(prefix.with_suffix('.png').read_bytes()).hexdigest() if proc.returncode==0 else None})
        if proc.returncode: raise RuntimeError(record)
    records.append(record)
receipt={'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':records}
(ROOT/'private'/'source_fetch_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='sources'},sort_keys=True))
for r in records: print(r['source'],r['pdf_sha256'],r['pdf_bytes'])
