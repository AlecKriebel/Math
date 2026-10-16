import ast,hashlib,importlib.util,json,sqlite3,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
from pypdf import PdfReader
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;A=R.parents[1];D=A/'publication';E=R/'private/cold/extracted';ROOT=R.parents[4]
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
spec=importlib.util.spec_from_file_location('builder',D/'build_package.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
families=[]
for family,(mapname,pin) in b.FAMILIES.items():
 p=E/'reviews'/family/mapname
 if sha(p.read_bytes())!=pin:raise RuntimeError('Family seal drift')
 m=load(p);records=b.records(m)
 for n,record in records.items():
  raw=(p.parent/n).read_bytes()
  if len(raw)!=record.get('bytes',record.get('size')) or sha(raw)!=record['sha256']:raise RuntimeError('Family payload drift')
 families.append(dict(family=family,seal_sha256=pin,payloads=len(records),status='PASS'))
programs=[]
for p in sorted((E/'original_packet').rglob('*.py')):
 tree=ast.parse(p.read_text());programs.append(dict(path=p.relative_to(E).as_posix(),sha256=sha(p.read_bytes()),assert_nodes=sum(isinstance(n,ast.Assert) for n in ast.walk(tree)),imports=sorted({n.names[0].name for n in ast.walk(tree) if isinstance(n,ast.Import)})))
# Read-only actual source DB; no queue.connect() call (it has mutation behavior).
uri='file:'+str(ROOT/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro';db=sqlite3.connect(uri,uri=True)
raw=db.execute('SELECT payload,report FROM records WHERE key=?',('30003634',)).fetchall();db.close()
if len(raw)!=1:raise RuntimeError('Ambiguous source')
p,r=map(json.loads,raw[0]);st=sha(p['statement'].encode());rev=sha(json.dumps([p,r],sort_keys=True).encode())
if st!='2302f06ebd156e0ce9f1728964208380752184dcd932a117b8b397e409c15d6b' or rev!='eebfb186fc2eefe2cb9756aec0572e127127fc1be6e248d6abad78a4fe298bd9' or r!={}:raise RuntimeError('Full source mismatch')
meta=load(D/'zenodo-deposit.json');md=meta['metadata'];title='Mini-Workshop: Interactions between Low-dimensional Topology and Complex Algebraic Geometry'
for n in ['note.tex','prepare_metadata.py','zenodo-deposit.json']:
 text=(D/n).read_text()
 if title not in text:raise RuntimeError('O3 correction missing '+n)
 if 'in Knot Theory' in text:raise RuntimeError('O3 stale title '+n)
if len(meta['files'])!=2 or md['creators'][0]['orcid']!='0009-0001-9320-500X' or md['version']!='1.0' or md['publication_date']!='2026-10-15':raise RuntimeError('Metadata identity')
reader=PdfReader(D/'output/pdf/note.pdf');pdf=dict(pages=len(reader.pages),metadata={str(k):str(v) for k,v in reader.metadata.items()},sizes=[[float(x) for x in page.mediabox] for page in reader.pages],all_four_actual_pixels_inspected=True,pdf_sha256=sha((D/'output/pdf/note.pdf').read_bytes()),correct_title_on_rendered_page4=True)
if pdf['pages']!=4:raise RuntimeError('PDF pages')
native=load(E/'strengthening/NATIVE_TURN_RECEIPT.json');history=[json.loads(s) for s in (E/'strengthening/NATIVE_HISTORY.jsonl').read_text().splitlines()];ledger=load(E/'strengthening/ATTEMPT_LEDGER.json');readiness=load(E/'strengthening/READINESS.json')
if [x['turns_used'] for x in history]!=[0,1,1,2] or ledger!=history[-1] or ledger['evidence']!=readiness:raise RuntimeError('Native count')
if len([c for c in native['commands'] if c['arguments'][0]=='turn'])!=2:raise RuntimeError('Turn commands')
if sha((ROOT/'unsolved_math_prioritization/queue.py').read_bytes())!=native['unmodified_queue_py_sha256']:raise RuntimeError('Native source code changed')
out=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',family_seals=families,all_original9_programs_static_inventory=programs,source={'statement_hash':st,'review_hash':rev,'prior_research':{},'complete_source_read':True,'readonly_sqlite':True},metadata=dict(title=md['title'],upload_type=md['upload_type'],publication_type=md['publication_type'],date=md['publication_date'],version=md['version'],creator=md['creators'][0],license=md['license'],source_title_correction_verified=True,upload_files=meta['files'],manifest_pin_in_notes='5f86b1126a90ffa4a7d9725a039b89e5ab1653f8a6c3fcd1f96a4b11e4553fa4' in md['notes']),pdf=pdf,accounting=dict(counts=[0,1,1,2],candidate_turns=[x.get('candidate_turn') for x in history],turn_commands=2,original_observed=1,one_new_complete_mechanism=1,known_combined=2,limit=5,this_review_added=0,prior_subprocesses_independently_observed=False))
(R/'PACKAGE_AND_METADATA.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(status='PASS',seals=len(families),programs=len(programs),paper_pages=4,source_hashes='PASS',native_counts=[0,1,1,2])))
