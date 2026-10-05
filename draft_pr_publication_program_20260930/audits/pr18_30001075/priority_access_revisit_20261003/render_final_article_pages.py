"""Selected final-article formula rendering; original is read-only, images private."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat,subprocess,sys
P=Path(__file__).absolute().parent;F=Path('/Users/alec/Downloads/Some-New-Results-on-Geometric-Transversals.pdf')
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def need(v,m):
 if not v:raise ValueError(m)
def put(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
rows=[];commands=[];b=F.read_bytes();need(len(b)==596169 and sha(b)=='478c879b6fea91b1aa17b0ea90172c10e01432b90e11c0873881f864151fdafc' and not F.is_symlink(),'Exact original full body')
try:
 for page in [1,11,20,22,24,28]:
  out=P/'private_cache'/('final_article_page'+str(page));need(not out.with_suffix('.png').exists(),'Absent private image')
  argv=['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-r','100','-png','-singlefile',str(F),str(out)]
  z=dict(argv=argv,cwd=str(P),started_utc=utc());c=subprocess.Popen(argv,cwd=P,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);z['actual_pid']=c.pid;a,e=c.communicate();z.update(finished_utc=utc(),exit_code=c.returncode,stdout_hex=a.hex(),stderr_hex=e.hex());commands.append(z);need(c.returncode==0,'Render failed')
  png=out.with_suffix('.png');a=png.read_bytes();rows.append(dict(page=page,printed_page=673+page,private_png=str(png),bytes=len(a),sha256=sha(a)))
 need(F.read_bytes()==b,'Original bytes unchanged')
 out=dict(schema='pr18-final-article-selected-private-render/v1',actual_pid=os.getpid(),actual_argv=sys.argv,utc=utc(),status='PASS_RENDER_ONLY',original_sha256=sha(b),source_full_mode=stat.S_IMODE(F.stat().st_mode),rows=rows,commands=commands,proof_certification=False,redistribution=False)
 put(P/'FINAL_ARTICLE_RENDER.json',(json.dumps(out,indent=2)+'\n').encode());print(json.dumps(dict(status=out['status'],actual_pid=os.getpid(),rendered_pages=len(rows))))
finally:put(P/'FINAL_ARTICLE_RENDER_COMMANDS.json',(json.dumps(commands,indent=2)+'\n').encode())
