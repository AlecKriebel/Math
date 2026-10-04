"""Read-only selected component PDF rendering; private images, no proof certification."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat,subprocess,sys
P=Path(__file__).absolute().parent;T=P.parent/'priority_access_resolution/tmp'
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def need(v,m):
 if not v:raise ValueError(m)
def put(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
rows=[];command_rows=[]
try:
 for name,page,expected in [('topology_v2',6,'e0414fa992bd06415d05cb8177c4b03fb2ca4665325de2bde3a13461a7f5621b')]:
  pdf=T/(name+'.pdf');b=pdf.read_bytes();need(sha(b)==expected and not pdf.is_symlink(),'Exact reused primary PDF')
  out=P/'private_cache'/(name+'_page'+str(page));need(not out.with_suffix('.png').exists(),'Private new render absent')
  argv=['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-r','90','-png','-singlefile',str(pdf),str(out)]
  z=dict(argv=argv,cwd=str(P),started_utc=utc());c=subprocess.Popen(argv,cwd=P,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);z['actual_pid']=c.pid;a,e=c.communicate();z.update(finished_utc=utc(),exit_code=c.returncode,stdout_hex=a.hex(),stderr_hex=e.hex());command_rows.append(z);need(c.returncode==0,'Render child failed')
  png=out.with_suffix('.png');image=png.read_bytes();need(pdf.read_bytes()==b,'Primary PDF unchanged')
  rows.append(dict(primary_pdf=str(pdf),primary_bytes=len(b),primary_sha256=expected,primary_mode=stat.S_IMODE(pdf.stat().st_mode),page=page,private_png=str(png),png_bytes=len(image),png_sha256=sha(image)))
 out=dict(schema='pr18-component-private-render/v1',actual_pid=os.getpid(),actual_argv=sys.argv,utc=utc(),status='PASS_RENDER_ONLY',rows=rows,commands=command_rows,no_mathematical_review_credit=True,no_new_download=True)
 put(P/'TOPOLOGY_PAGE6_RENDER.json',(json.dumps(out,indent=2)+'\n').encode());print(json.dumps(dict(status=out['status'],actual_pid=os.getpid(),rendered_pages=len(rows))))
finally:
 put(P/'TOPOLOGY_PAGE6_RENDER_COMMANDS.json',(json.dumps(command_rows,indent=2)+'\n').encode())
