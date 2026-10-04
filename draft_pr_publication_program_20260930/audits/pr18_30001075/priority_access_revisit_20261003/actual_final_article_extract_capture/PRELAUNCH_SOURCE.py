"""Lawful user-supplied final article: read-only identity/extraction, no redistribution."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat,subprocess,sys
P=Path(__file__).absolute().parent;F=Path('/Users/alec/Downloads/Some-New-Results-on-Geometric-Transversals.pdf');E=P/'private_cache/final_article.txt'
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def need(v,m):
 if not v:raise ValueError(m)
def put(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
commands=[]
b=F.read_bytes();need(len(b)==596169 and sha(b)=='478c879b6fea91b1aa17b0ea90172c10e01432b90e11c0873881f864151fdafc' and F.is_file() and not F.is_symlink(),'Exact lawful source');need(not E.exists(),'Private extraction destination absent')
try:
 for argv in [['/opt/homebrew/bin/pdfinfo',str(F)],['/opt/homebrew/bin/pdftotext','-layout',str(F),'-']]:
  z=dict(argv=argv,cwd=str(P),started_utc=utc());c=subprocess.Popen(argv,cwd=P,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);z['actual_pid']=c.pid;a,e=c.communicate();z.update(finished_utc=utc(),exit_code=c.returncode,stdout_bytes=len(a),stdout_sha256=sha(a),stderr_hex=e.hex());commands.append(z);need(c.returncode==0,'Read-only extraction command failed')
  if 'pdfinfo' in argv[0]:need(b'Pages:           30' in a,'Actual 30pages');put(P/'FINAL_ARTICLE_PDFINFO.txt',a)
  else:put(E,a)
 need(F.read_bytes()==b,'Lawful original bytes unchanged')
 out=dict(schema='pr18-lawful-final-article-extraction/v1',actual_pid=os.getpid(),actual_argv=sys.argv,utc=utc(),status='PASS_IDENTITY_AND_EXTRACTION_ONLY',source=dict(path=str(F),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(F.stat().st_mode),acquisition='Human user supplied local licensed article; no further access search/download'),pages=30,private_text=dict(path=str(E),bytes=E.stat().st_size,sha256=sha(E.read_bytes()),pages_by_formfeed=E.read_bytes().count(b'\x0c')),commands=commands,read_or_mathematical_certification=False,redistribution=False)
 put(P/'FINAL_ARTICLE_EXTRACTION.json',(json.dumps(out,indent=2)+'\n').encode());print(json.dumps(dict(status=out['status'],actual_pid=os.getpid(),source_sha256=sha(b),pages=30,extracted_text_bytes=E.stat().st_size)))
finally:put(P/'FINAL_ARTICLE_EXTRACTION_COMMANDS.json',(json.dumps(commands,indent=2)+'\n').encode())
