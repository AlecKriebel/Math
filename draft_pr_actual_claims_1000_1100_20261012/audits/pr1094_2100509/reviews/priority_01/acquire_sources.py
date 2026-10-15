from pathlib import Path
import urllib.request,hashlib,json,subprocess,datetime,sys
R=Path(__file__).resolve().parent
P=R/'private_sources'
ledger=R/'SOURCE_FETCH_LEDGER.json'
rows=json.loads(ledger.read_text()) if ledger.exists() else []
for identifier in sys.argv[1:]:
 url=('https://arxiv.org/pdf/'+identifier) if not identifier.startswith('https:') else identifier
 name=identifier.replace('https://','').replace('/','_') if identifier.startswith('https:') else identifier
 target=P/(name+'.pdf')
 row={'id':identifier,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 scholarly source verification'})
  with urllib.request.urlopen(request,timeout=35) as response: data=response.read(); row['final_url']=response.url;row['http']=response.status
  if not data.startswith(b'%PDF'): raise ValueError('response is not a PDF')
  target.write_bytes(data)
  row.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),local_path=target.relative_to(R).as_posix(),status='PDF_FETCHED')
  result=subprocess.run(['pdftotext','-layout',str(target),str(target.with_suffix('.txt'))],capture_output=True,text=True)
  row['pdftotext_exit']=result.returncode
  info=subprocess.run(['pdfinfo',str(target)],capture_output=True,text=True)
  for line in info.stdout.splitlines():
   if line.startswith('Pages:'):row['pages']=int(line.split(':')[1])
 except Exception as e: row.update(status='FETCH_FAILED',error=str(e))
 rows.append(row); ledger.write_text(json.dumps(rows,indent=2)+'\n'); print(json.dumps(row))
