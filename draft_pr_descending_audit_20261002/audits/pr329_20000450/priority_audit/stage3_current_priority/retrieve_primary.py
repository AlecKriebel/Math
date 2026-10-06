"""Native source retrieval with complete process receipts; own namespace only."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,hashlib,json,sys,re
N=Path(__file__).resolve().parent
assert len(sys.argv)==3
name,url=sys.argv[1:]
assert re.fullmatch('[a-z0-9_]+',name)
E=N/'private_evidence'/name
E.mkdir(parents=True,exist_ok=False)
def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(N)),'bytes':len(b),'sha256':sha(b)}
def run(tag,argv):
 start=utc();r=subprocess.run(argv,capture_output=True);end=utc()
 (E/(tag+'.stdout')).write_bytes(r.stdout);(E/(tag+'.stderr')).write_bytes(r.stderr)
 record={'kind':'genuine_native_subprocess_receipt','argv':argv,'started_utc':start,'finished_utc':end,'actual_exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)}
 (E/(tag+'.receipt.json')).write_text(json.dumps(record,indent=2)+'\n')
 return r,record
r,rec=run('retrieval',['/usr/bin/curl','--location','--fail','--silent','--show-error','--max-time','45','--dump-header',str(E/'headers.txt'),'--output',str(E/'source.bytes'),'--write-out','%{json}',url])
try:meta=json.loads(r.stdout)
except Exception:meta={}
summary={'kind':'computed_retrieval_summary_not_exit_receipt','url':url,'native_receipt':'retrieval.receipt.json','http_status':meta.get('http_code'),'url_effective':meta.get('url_effective'),'actual_exit_code':r.returncode,'finished_utc':rec['finished_utc'],'artifacts':[pin(p) for p in E.iterdir() if p.is_file()]}
p=E/'source.bytes'
if r.returncode==0 and p.exists() and p.read_bytes().startswith(b'%PDF'):
 run('pdfinfo',['/opt/homebrew/bin/pdfinfo',str(p)])
 run('fulltext',['/opt/homebrew/bin/pdftotext','-layout',str(p),str(E/'fulltext.layout.txt')])
 summary['artifacts']=[pin(p) for p in E.iterdir() if p.is_file()]
(E/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='artifacts'},indent=2))
if p.exists():print(json.dumps(pin(p)))
if r.stderr:print(r.stderr.decode(errors='replace'),file=sys.stderr)
