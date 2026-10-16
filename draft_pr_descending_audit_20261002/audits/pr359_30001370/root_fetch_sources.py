"""Fresh unauthenticated primary downloads and complete extraction, no author proof access."""
from pathlib import Path
import datetime,hashlib,json,subprocess,urllib.request
A=Path(__file__).resolve().parent;D=A/'root_sources_private'
sources=[('owr2009_49.pdf','https://ems.press/content/serial-article-files/46250'),('bkz_author.pdf','https://mat.univie.ac.at/~zweimueller/MyPub/bkz.pdf'),('bkz_arxiv_v1.pdf','https://arxiv.org/pdf/0812.4040v1')]
records=[]
for name,url in sources:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 request=urllib.request.Request(url,headers={'User-Agent':'Independent-Math-Source-Audit/1.0'})
 with urllib.request.urlopen(request,timeout=60) as response:
  b=response.read();status=response.status;final=response.url;kind=response.headers.get('Content-Type')
 assert status==200 and b.startswith(b'%PDF')
 (D/name).write_bytes(b)
 args=['pdftotext','-layout',str(D/name),str(D/name.replace('.pdf','.txt'))];p=subprocess.run(args,capture_output=True)
 (D/(name+'.extraction.stdout')).write_bytes(p.stdout);(D/(name+'.extraction.stderr')).write_bytes(p.stderr);assert p.returncode==0 and not p.stderr
 text=(D/name.replace('.pdf','.txt')).read_bytes()
 records.append({'name':name,'url':url,'final_url':final,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'http_status':status,'content_type':kind,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'text_bytes':len(text),'text_sha256':hashlib.sha256(text).hexdigest(),'extraction_argv':args,'extraction_exit_code':p.returncode,'extraction_stdout_bytes':len(p.stdout),'extraction_stderr_bytes':len(p.stderr),'unauthenticated_public_download':True})
(A/'ROOT_PRIMARY_SOURCE_IDENTITIES.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':records,'scope':'Fresh primary identities, not a substantive proof review or novelty certification.'},indent=2)+'\n')
print(json.dumps(records,indent=2))
