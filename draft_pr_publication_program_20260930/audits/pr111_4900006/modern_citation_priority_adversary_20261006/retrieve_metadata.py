import datetime, hashlib, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent
SOURCES = [
 ('pg_record','https://arxiv.org/abs/2510.14870'),
 ('anikushin_romanov_record','https://arxiv.org/abs/2503.11150'),
 ('anikushin_record','https://arxiv.org/abs/2304.05713'),
 ('anikushin_journal_record','https://link.springer.com/article/10.1007/s00030-025-01163-2'),
 ('kr_chapter6_record','https://link.springer.com/chapter/10.1007/978-3-030-50987-3_6'),
 ('kr_book_record','https://link.springer.com/book/10.1007/978-3-030-50987-3'),
 ('bochi_record','https://arxiv.org/abs/1712.01612'),
 ('zelik_review_record','https://arxiv.org/abs/2208.12101'),
]
receipts = []
for name, url in SOURCES:
    item = {'name':name,'url':url,'started_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url,headers={'User-Agent':'IndependentMathAudit/1.0'})
        with urllib.request.urlopen(req,timeout=30) as response:
            body=response.read(5*1024*1024+1)
            if len(body)>5*1024*1024: raise RuntimeError('body cap exceeded')
            item.update(http_status=response.status,final_url=response.url,bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
        (ROOT/'private_sources'/(name+'.html')).write_bytes(body)
        item['success']=True
    except Exception as error:
        item.update(success=False,error=str(error))
    item['completed_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipts.append(item)
    (ROOT/'METADATA_RETRIEVAL_RECEIPTS.json').write_text(json.dumps(receipts,indent=2,sort_keys=True)+'\n')
    print(json.dumps(item),flush=True)
