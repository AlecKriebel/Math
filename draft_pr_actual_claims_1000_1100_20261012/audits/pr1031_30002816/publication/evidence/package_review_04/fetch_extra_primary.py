import concurrent.futures,datetime,hashlib,json,pathlib,subprocess,sys,urllib.request
sys.dont_write_bytecode=True
O=pathlib.Path(__file__).resolve().parent;X=O/'extracted/grassmann_calibrations_v1';R=O/'sources/raw'
ledger=json.loads((X/'evidence/submitted/historical/PRIORITY_SOURCE_LEDGER.json').read_text())['sources']
selected=[r for r in ledger if r['id']in('sanyal_sottile_sturmfels2011','eckert2002','paul_zhao_dai2026','burgos_gil_et_al2021')]
def one(r):
 obj={'id':r['id'],'url':r['public_pdf_url'],'version':r['version'],'inspection_ledger':r['inspection'],'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(r['public_pdf_url'],timeout=60)as f:d=f.read();obj.update(final_url=f.url,content_type=f.headers.get('Content-Type'))
  p=R/(r['id']+'.pdf');p.write_bytes(d);obj.update(bytes=len(d),sha256=hashlib.sha256(d).hexdigest(),matches_ledger=hashlib.sha256(d).hexdigest()==r['sha256'],pdf_signature=d.startswith(b'%PDF'))
  if d.startswith(b'%PDF'):
   s=subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],capture_output=True);obj.update(text_exit=s.returncode,status='retrieved')
  else:obj['status']='not_pdf'
 except Exception as e:obj.update(status='error',error=str(e))
 return obj
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(one,selected))
(O/'sources/EXTRA_SOURCE_FETCH_RECEIPT.json').write_text(json.dumps({'sources':rows},indent=2)+'\n');print(json.dumps(rows,indent=2))
