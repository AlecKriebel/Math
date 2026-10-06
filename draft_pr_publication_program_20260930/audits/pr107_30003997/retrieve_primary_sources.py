from pathlib import Path
import datetime,hashlib,json,os,subprocess,urllib.request
A=Path(__file__).resolve().parent;D=A/'primary_sources_20261006';D.mkdir(exist_ok=False);records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
sources=json.loads((A/'original_source_authentication_20261006/original_attempt/source_manifest.json').read_text())['sources']
for source in sources:
 start=now();req=urllib.request.Request(source['url'],headers={'User-Agent':'Mathematical source verification'})
 with urllib.request.urlopen(req,timeout=40) as response:
  body=response.read();url=response.url;ctype=response.headers.get('Content-Type')
 if not body.startswith(b'%PDF-'):raise RuntimeError('not PDF: '+source['url'])
 f=D/source['file'];f.write_bytes(body);h=hashlib.sha256(body).hexdigest()
 if h!=source['sha256']:raise RuntimeError('primary body differs from submitted pin')
 args=['/opt/homebrew/bin/pdftotext','-layout',str(f),str(f.with_suffix('.txt'))];p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
 if p.returncode:raise RuntimeError(err.decode())
 records.append({'UTC_start':start,'UTC_end':now(),'reader_PID':os.getpid(),'requested_url':source['url'],'resolved_url':url,'content_type':ctype,
 'file':f.name,'bytes':len(body),'sha256':h,'matches_submitted_pin':True,'extraction':{'argv':args,'PID':p.pid,'exit_code':p.returncode,'text_sha256':hashlib.sha256(f.with_suffix('.txt').read_bytes()).hexdigest()}})
 (D/'RETRIEVAL_MANIFEST.json').write_text(json.dumps({'UTC':now(),'actual_operator_PID':os.getpid(),'records':records},indent=2)+'\n')
for name,first,last in [('owr.pdf',46,47),('karp-original.pdf',10,11)]:
 args=['/opt/homebrew/bin/pdftoppm','-f',str(first),'-l',str(last),'-scale-to','1600','-png',str(D/name),str(D/name.removesuffix('.pdf'))]
 p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
 (D/(name+'.render.json')).write_text(json.dumps({'argv':args,'PID':p.pid,'exit_code':p.returncode,'UTC':now(),'stderr':err.decode()},indent=2)+'\n')
 if p.returncode:raise RuntimeError(err.decode())
print(json.dumps({'primary_source_count':len(records),'all_submitted_pins_match':True,'directory':str(D)}))
