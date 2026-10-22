"""Read-only public source/finite-diagnostic reproduction. Python 3.10+ stdlib."""
import hashlib,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent

def need(ok,why):
 if not ok:raise RuntimeError(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(entries,data):
 need(len(entries)==len({e['path'] for e in entries}),'duplicate inventory')
 need({e['path'] for e in entries}==set(data),'closed source membership')
 for e in entries:
  b=data[e['path']];need(len(b)==e['bytes'] and sha(b)==e['sha256'],'source bytes '+e['path'])
def main():
 m=json.loads((P/'PUBLIC_MANIFEST.json').read_text());data={str(p.relative_to(P)):p.read_bytes() for p in P.rglob('*') if p.is_file() and p!=P/'PUBLIC_MANIFEST.json'}
 need(all(not p.is_symlink() for p in P.rglob('*')),'symlink');verify(m['files'],data)
 expected=(P/'verification/expected_results.json').read_bytes();runs=[]
 for flags in ([],['-O'],['-OO']):
  b=subprocess.check_output([sys.executable,'-B',*flags,str(P/'verification/exact_controls.py')]);need(b==expected,'finite output drift');runs.append({'flags':flags,'sha256':sha(b)})
 controls=[];key=next(iter(data))
 for name,other in [('changed',dict(data,**{key:data[key]+b'x'})),('missing',{k:v for k,v in data.items() if k!=key}),('extra',dict(data,**{'UNEXPECTED':b'x'}))]:
  try:verify(m['files'],other)
  except RuntimeError:controls.append(name)
  else:raise RuntimeError('accepted inventory mutation '+name)
 build=json.loads((P/'BUILD_RECEIPT.json').read_text());need(sha((P/'main.tex').read_bytes())==build['source_sha256'],'TeX pin');need(sha((P/'paper.pdf').read_bytes())==build['pdf_sha256'],'PDF pin')
 deposit=json.loads((P/'zenodo-deposit.json').read_text());meta=json.loads((P/'zenodo-metadata.json').read_text());need(deposit['metadata']==meta,'metadata disagreement')
 need([e['name'] for e in deposit['files']]==['extremality-bit-complexity.pdf','extremality-bit-complexity-source-and-verification.zip'],'scientific file selection')
 print(json.dumps({'status':'PASS','read_only':True,'publication_performed':False,'files':len(data),'finite_diagnostic_runs':runs,'inventory_mutants_rejected':controls,'pdf_sha256':build['pdf_sha256'],'source_sha256':build['source_sha256'],'universal_proof':'main.tex/paper.pdf; finite checks do not establish complexity or implement AHT'},indent=2,sort_keys=True))
if __name__=='__main__':main()
