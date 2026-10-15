import datetime, hashlib, json, pathlib, subprocess, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent
SOURCES = [
 ('zelik_review_current','https://arxiv.org/pdf/2208.12101'),
 ('wias_preprint777','https://www.wias-berlin.de/preprint/777/wias_preprints_777.pdf'),
]
receipts = []
for name, url in SOURCES:
    item = {'name':name,'url':url,'started_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'IndependentMathAudit/1.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read(30*1024*1024+1)
            if len(body)>30*1024*1024: raise RuntimeError('body cap exceeded')
            item.update(http_status=response.status,final_url=response.url,bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
        if not body.startswith(b'%PDF'): raise RuntimeError('not PDF')
        pdf = ROOT/'private_sources'/(name+'.pdf')
        txt = ROOT/'private_sources'/(name+'.txt')
        pdf.write_bytes(body)
        result = subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(txt)],capture_output=True,timeout=30)
        if result.returncode: raise RuntimeError('extraction failed')
        item.update(success=True,extracted_text_bytes=txt.stat().st_size,extracted_text_sha256=hashlib.sha256(txt.read_bytes()).hexdigest())
    except Exception as error:
        item.update(success=False,error=str(error))
    item['completed_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipts.append(item)
    (ROOT/'REVIEW_RETRIEVAL_RECEIPTS.json').write_text(json.dumps(receipts,indent=2,sort_keys=True)+'\n')
    print(json.dumps(item),flush=True)
