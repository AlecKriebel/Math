import datetime, hashlib, json, os, pathlib, subprocess, urllib.request, re
ROOT=pathlib.Path(__file__).resolve().parent
TASKS=[["dathe_khoule2012_html","https://www.researchgate.net/publication/258228980_Sur_les_deformations_d%27un_feuilletage_de_codimension_1_en_structures_de_contact"],["drame2025_rg","https://www.researchgate.net/profile/Ameth-Ndiaye-2/publication/393938083_Deformations_of_Integral_1-Form_Into_Contact-Symplectic_Pair/links/6880ccdb078693798454076a/Deformations-of-Integral-1-Form-Into-Contact-Symplectic-Pair.pdf"],["khoule_manso_ndiaye_war2025","https://arxiv.org/pdf/2503.00454v1"],["foulon_hasselblatt_vaugon2021","https://www.numdam.org/item/10.5802/ahl.98.pdf"],["affine_pairs2025_publisher","https://link.springer.com/content/pdf/10.1007/s00022-025-00742-z.pdf"]]
records=[]
for key,url in TASKS:
 rec={'key':key,'requested_url':url,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_pid':os.getpid()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematics source audit; read-only public-source retrieval'}),timeout=20) as res:
   body=res.read(12*1024*1024+1);rec.update(final_url=res.url,status=res.status,headers=dict(res.headers),bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
  if len(body)>12*1024*1024:raise ValueError('bounded-size response exceeded')
  suffix='.pdf' if body.startswith(b'%PDF') else '.response.bin';p=ROOT/(key+suffix);p.write_bytes(body);rec['saved_path']=p.name
  if suffix=='.pdf':
   cmd=['/opt/homebrew/bin/pdftotext','-layout',str(p),str(p.with_suffix('.txt'))];cp=subprocess.run(cmd,capture_output=True)
   (ROOT/(key+'.pdftotext.stdout.bin')).write_bytes(cp.stdout);(ROOT/(key+'.pdftotext.stderr.bin')).write_bytes(cp.stderr)
   rec['pdftotext']={'argv':cmd,'returncode':cp.returncode,'stdout_sha256':hashlib.sha256(cp.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(cp.stderr).hexdigest()}
  elif key=='dathe_khoule2012_html':
   links=[u for u in re.findall(r'(?:href|data-href)=[\"\x27]([^\"\x27]+)',body.decode('utf-8','replace')) if '.pdf' in u];rec['observed_pdf_links']=links;print(json.dumps(links),flush=True)
 except Exception as e:rec.update(error_type=type(e).__name__,error=str(e))
 rec['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();records.append(rec);(ROOT/'HTTP_PROCESS_RECORDS_03.json').write_text(json.dumps(records,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in rec.items() if k in ['key','status','bytes','saved_path','error']}),flush=True)

