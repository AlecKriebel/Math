from pathlib import Path
import json,hashlib,subprocess,sys,datetime,zipfile,stat
O=Path(__file__).resolve().parent;A=O.parent;P=A/'publication_package_v1';PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
def H(b):return hashlib.sha256(b).hexdigest()
def require(ok,m):
 if not ok:raise ValueError(m)
def row(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':H(b)}
def run(label,argv,cwd=None):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(argv,cwd=cwd,capture_output=True)
 out=O/(label+'.stdout');err=O/(label+'.stderr');out.write_bytes(r.stdout);err.write_bytes(r.stderr)
 rec={'UTC':start,'argv':argv,'cwd':str(cwd or O),'exit':r.returncode,'stdout':row(out),'stderr':row(err)};(O/(label+'.receipt.json')).write_text(json.dumps(rec,indent=2));return rec
bound=json.loads((A/'ROOT_WHOLE_REVIEW_INPUT_01.json').read_text());m=P/'FINAL_REVIEW_PACKET_MANIFEST.json';require(H(m.read_bytes())==bound['package_manifest_SHA256'],'packet manifest mismatch')
checks=[]
for n,x in bound['other_exact_inputs'].items():
 b=(A/n).read_bytes();require(len(b)==x['bytes'] and H(b)==x['sha256'],n);checks.append(row(A/n))
for n,x in json.loads(m.read_text())['payloads'].items():
 b=(P/n).read_bytes();require(len(b)==x['bytes'] and H(b)==x['sha256'],n);checks.append(row(P/n))
vm=json.loads((P/'verification/MANIFEST.json').read_text())['files'];observed={p.relative_to(P/'verification').as_posix() for p in (P/'verification').rglob('*') if p.is_file()};require(observed==set(vm)|{'MANIFEST.json'},'verification exact membership')
for n,x in vm.items():
 b=(P/'verification'/n).read_bytes();require(len(b)==x['bytes'] and H(b)==x['sha256'],'verification '+n)
with zipfile.ZipFile(P/'verification-package.zip') as z:
 require(len(z.namelist())==len(set(z.namelist()))==146,'duplicate/count ZIP');require(z.testzip() is None,'CRC')
 require(set(z.namelist())==observed,'zip membership')
 for n in z.namelist():
  require(not Path(n).is_absolute() and '..' not in Path(n).parts,'unsafe path');require(z.read(n)==(P/'verification'/n).read_bytes(),'zip bytes '+n)
nm=json.loads((A/'integration_preparation/CURRENT_TEMPLATE.json').read_text());N=A/'integration_preparation'/nm['current_template'];ns={p.relative_to(N).as_posix() for p in N.rglob('*') if p.is_file()};require(ns==set(nm['files']) and len(ns)==49,'native membership')
for n,x in nm['files'].items():
 b=(N/n).read_bytes();require(len(b)==x['bytes'] and H(b)==x['sha256'],'native '+n)
om=json.loads((P/'verification/provenance/ORIGINAL_FILE_MANIFEST.json').read_text());(O/'ORIGINAL_MANIFEST_SCHEMA.json').write_text(json.dumps(om,indent=2))
# Original manifest schema inspected separately below. Compare preserved 22 files in ZIP and native.
hist={p.relative_to(N/'historical_original').as_posix():p for p in (N/'historical_original').rglob('*') if p.is_file()};require(len(hist)==22,'original count')
for n,f in hist.items():require(f.read_bytes()==(P/'verification/historical_original/unsolved_math_prioritization/attempts/5000007'/n).read_bytes(),'native/ZIP historical '+n)
require((N/'PROOF_V2.md').read_bytes()==(A/'CURRENT_PROOF.md').read_bytes()==(P/'verification/CURRENT_PROOF.md').read_bytes(),'current proof consistency')
require((P/'dodecahedron_endpoint.tex').read_bytes()==(P/'verification/manuscript/dodecahedron_endpoint.tex').read_bytes(),'tex consistency')
require((P/'dodecahedron_endpoint.pdf').read_bytes()==(P/'verification/manuscript/dodecahedron_endpoint.pdf').read_bytes(),'pdf consistency')
(O/'INTEGRITY_RESULTS.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bound_inputs':checks,'verification_payloads':len(vm),'ZIP_entries':146,'native_files':49,'native_original_files':22,'all_checks':'PASS'},indent=2))
receipts=[]
for name in ['check_certificate.py','check_half_turn.py','test_reconstruction.py','check_pinned_coordinates.py','run_verification.py']:
 for opt in [False,True]:
  folder=P/'verification/current';driver='import sys,runpy;sys.path.insert(0,'+repr(str(folder))+');sys.argv=['+repr(name)+'];runpy.run_path('+repr(str(folder/name))+',run_name="__main__")';argv=[PY,'-E','-S','-B','-P']+(['-O'] if opt else [])+['-c',driver];r=run(name.removesuffix('.py')+('_optimized' if opt else '_normal'),argv,O);receipts.append(r);require(r['exit']==0,'execution '+name)
receipts.append(run('manifest',[PY,'-E','-S','-B','-P',str(P/'verification/check_manifest.py')],O))
# Build only in our folder; no input/editor mutation.
receipts.append(run('tectonic',['/opt/homebrew/bin/tectonic','--only-cached','--outdir',str(O),str(P/'dodecahedron_endpoint.tex')],O))
receipts.append(run('pdfinfo',['/opt/homebrew/bin/pdfinfo',str(P/'dodecahedron_endpoint.pdf')],O))
receipts.append(run('render',['/opt/homebrew/bin/pdftoppm','-scale-to','1300','-png',str(P/'dodecahedron_endpoint.pdf'),str(O/'paper')],O))
receipts.append(run('figures',['/opt/homebrew/bin/pdftoppm','-f','10','-l','11','-scale-to','1500','-png',str(A/'root_primary_sources_private/fuchs2021.pdf'),str(O/'fuchsfig')],O))
(O/'ACTUAL_RUN_INDEX.json').write_text(json.dumps(receipts,indent=2));print(json.dumps({'runs':len(receipts),'exits':[r['exit'] for r in receipts],'integrity':'PASS'},indent=2))
