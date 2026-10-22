"""Local packet custody only. No network, Git, provider or repository action."""
from pathlib import Path
import json,hashlib,datetime,sys
P=Path(__file__).resolve().parent
M=P/'MANIFEST.json'
def fail(s):raise RuntimeError(s)
def rows():
 out=[]
 for f in sorted(P.rglob('*')):
  if f.is_symlink():fail('symlink in closed packet')
  if not f.is_file() or f==M:continue
  b=f.read_bytes();out.append({'path':str(f.relative_to(P)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 return out
if '--verify-only' not in sys.argv:
 if M.exists():fail('closed manifest exists; never overwrite')
 proposal=json.loads((P/'QUALIFIED_ROW_PROPOSAL.json').read_text())
 if len(proposal['cells'])!=4 or any(type(x)is not str for x in proposal['cells']):fail('row literal schema')
 if proposal['cells'][1]!='' or proposal['cells'][2]!='':fail('blank B/C schema')
 if proposal['pr_url'] not in proposal['cells'][3]:fail('PR URL omitted')
 if proposal['publication_ready'] or proposal['append_ready']:fail('readiness must remain false')
 manifest={'schema':1,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Independent read-only PR1292 full original/prior review; private raw ledger data stays private','excluded_exact_relative_paths':['MANIFEST.json'],'files':rows()}
 with M.open('x') as h:h.write(json.dumps(manifest,indent=2)+'\n')
j=json.loads(M.read_text());actual=rows()
if actual!=j['files']:fail('closed packet content/inventory drift')
if not any(x['path']=='pinned_pr/MANIFEST.json' for x in actual):fail('nested manifest accidentally omitted')
allocated=sum(f.stat().st_blocks*512 for f in P.rglob('*') if f.is_file())
if allocated>12*1024*1024:fail('12MiB allocation budget exceeded')
if any(f.name=='CASE' for f in P.rglob('*')):fail('unexpected action CASE')
print(json.dumps({'status':'PASS','manifest_sha256':hashlib.sha256(M.read_bytes()).hexdigest(),'members':len(actual),'member_bytes':sum(x['bytes'] for x in actual),'allocated_bytes':allocated,'max_allocated_bytes':12*1024*1024,'report_sha256':hashlib.sha256((P/'REPORT.md').read_bytes()).hexdigest(),'proposal_sha256':hashlib.sha256((P/'QUALIFIED_ROW_PROPOSAL.json').read_bytes()).hexdigest(),'publication_ready':False,'append_ready':False,'external_writes':0},indent=2))
