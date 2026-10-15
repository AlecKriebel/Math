import urllib.request, json, hashlib, pathlib, datetime, sys
BASE=pathlib.Path(__file__).resolve().parent
ledger=BASE/'SOURCE_RETRIEVALS.jsonl'
for spec in sys.argv[1:]:
    name,url=spec.split('|',1)
    row={'id':name,'requested_url':url,'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 independent scholarly source check'})
        with urllib.request.urlopen(req,timeout=25) as r:
            data=r.read(); row.update(status=r.status,resolved_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),pdf_signature=data.startswith(b'%PDF'))
        path=BASE/'.cache'/f'{name}.bin'; path.write_bytes(data); row['cache_path']=str(path.relative_to(BASE))
    except Exception as e: row['error']=str(e)
    with ledger.open('a') as f: f.write(json.dumps(row,sort_keys=True)+'\n')
    print(json.dumps(row,sort_keys=True))
