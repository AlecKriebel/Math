import concurrent.futures,datetime,hashlib,json,pathlib,subprocess,sys,urllib.request
sys.dont_write_bytecode=True
B=pathlib.Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1031_30002816')
O=B/'reviews/package_04/sources';R=O/'raw';R.mkdir(parents=True,exist_ok=True);(O/'.gitignore').write_text('raw/\n')
records=json.loads((B/'publication/evidence/priority_review_01/sources/SOURCE_PINS.json').read_text())['sources']
def one(r):
 out={'id':r['id'],'url':r['url'],'version_ledger':r.get('version'),'date_ledger':r.get('publication_date'),'locators_ledger':r.get('locators',[]),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(r['url'],headers={'User-Agent':'Independent mathematical source verification'})
  with urllib.request.urlopen(req,timeout=60) as f: data=f.read();out['final_url']=f.url;out['content_type']=f.headers.get('Content-Type')
  out.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),matches_ledger_hash=hashlib.sha256(data).hexdigest()==r['sha256'])
  p=R/(r['id']+'.pdf');p.write_bytes(data)
  if data.startswith(b'%PDF'):
   result=subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],capture_output=True)
   out.update(status='retrieved',text_extract_exit=result.returncode,text_sha256=hashlib.sha256(p.with_suffix('.txt').read_bytes()).hexdigest(),text_extract_stderr=result.stderr.decode(),path=str(p.relative_to(O)))
  else:out['status']='non_pdf_response'
 except Exception as exc:out.update(status='fetch_error',error=str(exc))
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(one,records))
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':rows,'raw_policy':'All newly retrieved third-party bodies/text/images stay solely under this review sources/raw; metadata is authored separately.'}
(O/'SOURCE_FETCH_RECEIPT.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps({'count':len(rows),'retrieved':sum(r['status']=='retrieved' for r in rows),'outcomes':[{k:r[k] for k in ('id','status','bytes','matches_ledger_hash') if k in r} for r in rows]},indent=2))
