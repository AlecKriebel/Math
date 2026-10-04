#!/usr/bin/env python3
"""Fresh public-primary retrieval, exact hashes, full text and visual pages."""
import datetime, hashlib, json, pathlib, urllib.request
from capture import ROOT, PRIVATE, now, run

sources=[('hayman_lingham_2018','https://arxiv.org/pdf/1809.07200',1706228,'8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0'),
 ('carleson_1976','https://www.acadsci.fi/mathematica/Vol02/vol02pp035-039.pdf',3653618,'4f4d183b2bdb68752b9c46d7bd866748a25615d2ab2d8b3b7a2644d28cc29aae')]
out=[]
for stem,url,size,sha in sources:
    start=now()
    with urllib.request.urlopen(url, timeout=90) as r:
        data=r.read(); headers=dict(r.headers.items()); final_url=r.url; status=r.status
    path=PRIVATE/(stem+'.pdf'); path.write_bytes(data)
    info=dict(name=stem,url=url,final_url=final_url,status=status,started_utc=start,finished_utc=now(),headers=headers,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),expected_bytes=size,expected_sha256=sha)
    assert len(data)==size and info['sha256']==sha, info
    out.append(info)
    p=run(stem+'_text',['/opt/homebrew/bin/pdftotext','-layout',str(path),'-'])
    assert p.returncode==0
    pages=[61] if stem.startswith('hayman') else [1,2,3,4,5]
    for page in pages:
        p=run(stem+'_render_'+str(page),['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-r','110','-singlefile','-png',str(path),str(PRIVATE/(stem+'_page_'+str(page)))])
        assert p.returncode==0
(ROOT/'retrieval.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
