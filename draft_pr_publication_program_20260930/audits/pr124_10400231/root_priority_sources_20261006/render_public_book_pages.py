"""Authenticate freely available publisher matter and render into own ignored folder."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent.parent
D=A/'root_priority_sources_20261006'
S=A/'original_conjecture_priority_adversary_20261006/private_sources'
def req(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
out=D/'ACTUAL_PUBLIC_BOOK_PAGE_RENDER.json'
req(not out.exists(),'Do not repeat a completed actual render')
events=[]
for name,pin,pages in [
 ('turaev_frontmatter','e93ab1a4ccdafaf6975dff9810ff54c26c1f36ed0a7fc52fb063448c899b16a9',[3,4,6]),
 ('turaev_backmatter','bc3f64fe9570826942f058ea7bd78b86f64d5f3ff24912f45b9fee8beef31e5f',[1])]:
 source=S/(name+'.pdf');body=source.read_bytes()
 req(body.startswith(b'%PDF-') and sha(body)==pin,'Source authentication '+name)
 for page in pages:
  dest=D/'private_sources'/(name+'_page_'+str(page))
  argv=['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1800','-png',str(source),str(dest)]
  child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);stdout,stderr=child.communicate()
  req(child.returncode==0,'Page render exit')
  pixels=dest.with_suffix('.png').read_bytes()
  events.append({'source':str(source),'source_sha256':pin,'one_based_PDF_page':page,'output':str(dest.with_suffix('.png')),'output_bytes':len(pixels),'output_sha256':sha(pixels),'argv':argv,'actual_child_PID':child.pid,'UTC':now(),'exit_code':child.returncode,'stderr_sha256':sha(stderr)})
record={'schema':'pr124-public-book-matter-page-render/v1','actual_operator_PID':os.getpid(),'UTC':now(),'events':events,'pages_rendered':len(events),'rendering_is_not_reading':True,'source_full_book_chapters_read':False,'shared_tracked_or_service_mutations':False}
out.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps({'PID':os.getpid(),'UTC':record['UTC'],'pages':len(events),'full_book_chapters_read':False}))
