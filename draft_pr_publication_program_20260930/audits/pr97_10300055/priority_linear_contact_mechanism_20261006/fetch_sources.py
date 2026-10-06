"""Bounded public-primary retrieval with actual HTTP/process receipts. No credentials."""
import datetime, hashlib, json, os, pathlib, subprocess, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
tasks=[
 ('zois2000v4','https://arxiv.org/pdf/hep-th/0006169v4'),
 ('ndiaye_wade2023v2','https://arxiv.org/pdf/2306.15060v2'),
 ('mori2002','https://ocu-omu.repo.nii.ac.jp/record/2009833/files/111F0000002-03901-1.pdf'),
 ('asai2011_pa','https://www.numdam.org/item/10.5802/aif.2569.pdf'),
 ('bowden2016','https://msp.org/gt/2016/20-2/gt-v20-n2-p02-p.pdf'),
 ('dathe_rukimbira2011_publisher','https://www.degruyterbrill.com/document/doi/10.1515/advgeom.2010.043/pdf'),
 ('dathe_rukimbira2004_publisher','https://www.degruyterbrill.com/document/doi/10.1515/advg.2004.008/pdf'),
 ('confoliations_ams','https://www.ams.org/books/ulect/013/ulect013.pdf')]
records=[]
for key,url in tasks:
 rec={'key':key,'requested_url':url,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_pid':os.getpid()}
 try:
  request=urllib.request.Request(url,headers={'User-Agent':'Independent mathematics source audit; read-only public-source retrieval'})
  with urllib.request.urlopen(request,timeout=25) as response:
   body=response.read(12*1024*1024+1)
   rec.update(final_url=response.url,status=response.status,headers=dict(response.headers),bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
  if len(body)>12*1024*1024: raise ValueError('bounded-size response exceeded')
  suffix='.pdf' if body.startswith(b'%PDF') else '.response.bin'
  path=ROOT/(key+suffix);path.write_bytes(body);rec['saved_path']=path.name
  if suffix=='.pdf':
   cmd=['/opt/homebrew/bin/pdftotext','-layout',str(path),str(path.with_suffix('.txt'))]
   cp=subprocess.run(cmd,capture_output=True)
   (ROOT/(key+'.pdftotext.stdout.bin')).write_bytes(cp.stdout);(ROOT/(key+'.pdftotext.stderr.bin')).write_bytes(cp.stderr)
   rec['pdftotext']={'argv':cmd,'returncode':cp.returncode,'stdout_sha256':hashlib.sha256(cp.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(cp.stderr).hexdigest()}
 except Exception as e:rec.update(error_type=type(e).__name__,error=str(e))
 rec['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();records.append(rec)
 (ROOT/'HTTP_PROCESS_RECORDS.json').write_text(json.dumps(records,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:v for k,v in rec.items() if k in ['key','status','bytes','saved_path','error']}),flush=True)
