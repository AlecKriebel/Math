from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
import json

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
E=P/'verification/hafnian-retract-live-root-20261117'
N=P/'verification/hafnian-retract-production-prepare-sol-20261117'
plan=json.loads((N/'TARGETS.json').read_text())
names=plan['additions_public_relative']+plan['modifications_public_relative']+['research/research.css']
assert len(names)==len(set(names))==12
rows=[]
for name in names:
    route='/' + name
    if route.endswith('/index.html'): route=route[:-10]
    rows.append(dict(path=name,url='https://aleckriebel.com'+route))
rows.append(dict(path='research/index.html',url='https://aleckriebel.com/research/index.html'))
assert not (E/'HTTP_FINAL.json').exists()

def check(row):
    expected=(W/'public'/row['path']).read_bytes()
    request=Request(row['url'],headers={'User-Agent':'AlecKriebel-research-publication-check/1.0','Accept-Encoding':'identity'})
    with urlopen(request,timeout=45) as response:
        body=response.read()
        result=dict(**row,status=response.status,final_url=response.url,
                    bytes=len(body),SHA256=sha256(body).hexdigest(),
                    expected_bytes=len(expected),expected_SHA256=sha256(expected).hexdigest(),
                    whole_bytes_equal=body==expected,headers=dict(response.headers.items()))
    assert result['status']==200 and body==expected,row['url']
    content_type=next((v for k,v in result['headers'].items() if k.lower()=='content-type'),'').split(';')[0]
    if row['path'].endswith('.pdf'): assert content_type=='application/pdf'
    if row['path'].endswith('.html'): assert content_type=='text/html'
    canonical=row['url'][:-10] if row['url'].endswith('/index.html') else row['url']
    assert result['final_url']==canonical,(row['url'],result['final_url'],canonical)
    return result

with ThreadPoolExecutor(max_workers=4) as pool:
    futures=[pool.submit(check,row) for row in rows]
    results=[]
    for row,future in zip(rows,futures,strict=True):
        try: results.append(future.result())
        except Exception as error:
            results.append(dict(**row,error=repr(error)))
out=dict(UTC=datetime.now(timezone.utc).isoformat(),scope='Direct HTTPS GET and complete file identity only; no browser/mobile/embedded-PDF UI certificate.',
         requests=len(rows),results=results,all_passed=all(r.get('whole_bytes_equal') is True for r in results),
         actual_UI_verified=False,AA=None)
(E/'HTTP_FINAL.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
assert out['all_passed'],[r for r in results if not r.get('whole_bytes_equal')]
print(json.dumps(dict(UTC=out['UTC'],requests=len(rows),all_status_200=True,all_whole_files_equal=True,
                     PDF_mime_verified=True,actual_UI_verified=False,AA=None)))
