from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,urllib.request
R=Path(__file__).resolve().parent
P=R.parent.parent/'publication'
plan=json.loads((P/'evidence/package_review_01/sources/SOURCE_FETCH_RECEIPT.json').read_text())
def fetch(s):
 row={k:s[k] for k in ('id','url','version')}
 row['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  req=urllib.request.Request(s['url'],headers={'User-Agent':'Independent mathematical source verification'})
  with urllib.request.urlopen(req,timeout=45) as response:
   data=response.read(); row['final_url']=response.url; row['content_type']=response.headers.get('Content-Type')
  row.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),pdf_signature=data.startswith(b'%PDF-'))
  target=R/'sources/raw'/(s['id']+'.pdf'); target.write_bytes(data)
  row['raw_path']=str(target.relative_to(R))
  row['previous_hash_match']=row['sha256']==s['sha256']
  if row['pdf_signature']:
   q=subprocess.run(['pdftotext','-layout',str(target),str(target.with_suffix('.txt'))],capture_output=True,text=True)
   row.update(extraction_exit=q.returncode,extraction_stderr=q.stderr)
   if q.returncode==0: row['text_sha256']=hashlib.sha256(target.with_suffix('.txt').read_bytes()).hexdigest()
 except Exception as e: row['error']=str(e)
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(fetch,plan))
(R/'sources/SOURCE_FETCH_RECEIPT.json').write_text(json.dumps(rows,indent=2)+'\n')
for row in rows: print(row['id'],row.get('bytes'),row.get('previous_hash_match'),row.get('error','OK'))
