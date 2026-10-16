import urllib.request, hashlib, json, datetime, pathlib, subprocess, sys
root=pathlib.Path(__file__).resolve().parent
url, stem=sys.argv[1:3]
receipt={'requested_url':url,'UTC_started':datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
    req=urllib.request.Request(url,headers={'User-Agent':'Independent read-only mathematical source audit'})
    with urllib.request.urlopen(req, timeout=45) as response:
        data=response.read()
        receipt.update(final_url=response.geturl(), http_status=response.status, headers=dict(response.headers))
    target=root/'sources'/stem
    target.write_bytes(data)
    receipt.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),saved_as=str(target.relative_to(root)))
    if data.startswith(b'%PDF'):
        result=subprocess.run(['pdftotext','-layout',str(target),str(target.with_suffix('.txt'))],capture_output=True,text=True)
        receipt['pdftotext']={'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
except Exception as e:
    receipt['error']=repr(e)
receipt['UTC_finished']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(root/'receipts'/(stem+'.retrieval.json')).write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt,indent=2))
