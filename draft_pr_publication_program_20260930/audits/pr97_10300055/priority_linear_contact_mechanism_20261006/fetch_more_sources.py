import datetime, hashlib, json, os, pathlib, subprocess, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
tasks=[
 ('drame2025_html','https://onlinelibrary.wiley.com/doi/full/10.1155/jom/6799367'),
 ('drame2025_pdf','https://onlinelibrary.wiley.com/doi/pdf/10.1155/jom/6799367'),
 ('dathe2026_html','https://onlinelibrary.wiley.com/doi/full/10.1155/jom/8818157'),
 ('mitsumatsu2002','https://www.ms.u-tokyo.ac.jp/~hirachi/scv/hayama-archive/2002/proceedings/Mitsumatsu.pdf'),
 ('etnyre_ghrist2002','https://etnyre.math.gatech.edu/preprints/papers/anosovproc.pdf'),
 ('abbas_cieliebak_hofer2005v2','https://arxiv.org/pdf/math/0409355v2'),
 ('crossref_dr2011','https://api.crossref.org/works/10.1515/advgeom.2010.043'),
 ('publisher_dr2011_html','https://www.degruyterbrill.com/document/doi/10.1515/advgeom.2010.043/html')]
records=[]
for key,url in tasks:
 rec={'key':key,'requested_url':url,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_pid':os.getpid()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematics source audit; read-only public-source retrieval'}),timeout=20) as response:
   body=response.read(8*1024*1024+1);rec.update(final_url=response.url,status=response.status,headers=dict(response.headers),bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
  if len(body)>8*1024*1024:raise ValueError('bounded-size response exceeded')
  suffix='.pdf' if body.startswith(b'%PDF') else '.response.bin';p=ROOT/(key+suffix);p.write_bytes(body);rec['saved_path']=p.name
  if suffix=='.pdf':
   cmd=['/opt/homebrew/bin/pdftotext','-layout',str(p),str(p.with_suffix('.txt'))];cp=subprocess.run(cmd,capture_output=True)
   (ROOT/(key+'.pdftotext.stdout.bin')).write_bytes(cp.stdout);(ROOT/(key+'.pdftotext.stderr.bin')).write_bytes(cp.stderr)
   rec['pdftotext']={'argv':cmd,'returncode':cp.returncode,'stdout_sha256':hashlib.sha256(cp.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(cp.stderr).hexdigest()}
 except Exception as e:rec.update(error_type=type(e).__name__,error=str(e))
 rec['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();records.append(rec)
 (ROOT/'HTTP_PROCESS_RECORDS_02.json').write_text(json.dumps(records,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in rec.items() if k in ['key','status','bytes','saved_path','error']}),flush=True)
