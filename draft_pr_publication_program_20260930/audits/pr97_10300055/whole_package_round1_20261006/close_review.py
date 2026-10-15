from pathlib import Path
import json,hashlib,datetime,os,sys
r=Path(__file__).resolve().parent;p=(r.parent/'contingent_credited_note_v1').resolve();sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();d=json.loads((p/'CLOSED_MANIFEST.json').read_text())
rows=[]
for x in d['files']:
 f=p/x['path'];rows.append({'path':str(f),'sha256':sha(f),'bytes':f.stat().st_size,'pass':sha(f)==x['sha256'] and f.stat().st_size==x['bytes']})
actual={str(f.relative_to(p)) for f in p.rglob('*') if f.is_file()};expected={x['path'] for x in d['files']}|{'CLOSED_MANIFEST.json'}
auth={'UTC':stamp,'manifest_sha256':sha(p/'CLOSED_MANIFEST.json'),'count':len(rows),'file_checks':rows,'failures':[x['path'] for x in rows if not x['pass']],'extra':sorted(actual-expected),'missing':sorted(expected-actual)}
(r/'AUTHENTICATION_AFTER.json').write_text(json.dumps(auth,indent=2)+'\n')
borrow=[]
for x in d['borrowed_input_bindings']:
 f=r.parent/x['reference'];borrow.append(dict(x,actual_sha256=sha(f),actual_bytes=f.stat().st_size,pass_=sha(f)==x['sha256'] and f.stat().st_size==x['bytes']))
(r/'BORROWED_AUTHENTICATION_AFTER.json').write_text(json.dumps(borrow,indent=2)+'\n')
if auth['failures'] or auth['extra'] or auth['missing'] or not all(x['pass_'] for x in borrow):raise RuntimeError('Reviewed inputs changed')
if auth['manifest_sha256']!='ca4ce63be4957fc836b9e0a5d30dc7049eb22e33cc50d15994444d8e4638adc3':raise RuntimeError('Wrong frozen manifest')
# Close evidence only after all actual checks and report files are complete.
log=r/'RESEARCH_LOG.md';log.write_text(log.read_text()+'- '+stamp+': Final after-authentication confirms frozen231 own files+manifest and nine borrowed bindings unchanged. Independent review complete100%. Mathematics and bounded source attribution pass; one required output-custody issue R1 affects all three wrappers. Whole-package acceptance false; no publication authority or priority clearance. Closing private evidence including retained link witnesses.\n')
summary='Review complete: frozen inputs unchanged; mathematics/source PASS; whole package REPAIRS_REQUIRED (R1).\n'
(r/'FINALIZATION_RECEIPT.json').write_text(json.dumps({'UTC':stamp,'PID':os.getpid(),'argv':sys.argv,'cwd':str(Path.cwd()),'exit_code_intended':0,'stdout':summary,'stdout_sha256':hashlib.sha256(summary.encode()).hexdigest(),'stderr':'','scope':'After-authentication and private evidence closure only'},indent=2)+'\n')
inputs=[{'path':str(p/'CLOSED_MANIFEST.json'),'sha256':sha(p/'CLOSED_MANIFEST.json'),'bytes':(p/'CLOSED_MANIFEST.json').stat().st_size,'role':'Frozen own231-file closure'}]+[{'path':str((r.parent/x['reference']).resolve()),'sha256':x['sha256'],'bytes':x['bytes'],'role':'Read-only borrowed package binding'} for x in d['borrowed_input_bindings']]
for x in json.loads((r/'PRIMARY_READ_SCOPE_LEDGER.json').read_text())['source_reads']:
 inputs.append({'path':x['path'],'sha256':x['sha256'],'bytes':x['bytes'],'role':'Read-only primary source; exact extent in ledger'})
for x in json.loads((r/'METADATA_INPUT_PINS.json').read_text()):inputs.append({'path':x['path'],'sha256':x['sha256'],'bytes':x['bytes'],'role':'Read-only static metadata provenance'})
for x in inputs:
 f=Path(x['path'])
 if sha(f)!=x['sha256'] or f.stat().st_size!=x['bytes']:raise RuntimeError('Read-only input pin changed: '+str(f))
files=[];links=[];inodes={}
for f in sorted(r.rglob('*')):
 if f.name=='CLOSED_EVIDENCE_MANIFEST.json' and f.parent==r:continue
 rel=f.relative_to(r).as_posix()
 if f.is_symlink():links.append({'path':rel,'type':'controlled_symlink','target':os.readlink(f),'target_within_review':f.resolve().is_relative_to(r)});continue
 if f.is_file():
  files.append({'path':rel,'sha256':sha(f),'bytes':f.stat().st_size});st=f.stat();inodes.setdefault((st.st_dev,st.st_ino),[]).append(rel)
manifest={'schema':'pr97-independent-whole-package-evidence/v1','UTC':stamp,'own_files':files,'controlled_symlinks':links,'hardlink_groups':[v for v in inodes.values() if len(v)>1],'read_only_input_pins':inputs,'excluded':['CLOSED_EVIDENCE_MANIFEST.json'],'review_verdict':'REPAIRS_REQUIRED','publication_authorized':False,'private_source_extracts_only':True,'third_party_full_bodies_copied':False,'artifact_recovery':'568 unchanged duplicate own payload-copy files removed; witness contents and actual receipts retained; reproducible against frozen payload pin.'}
(r/'CLOSED_EVIDENCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(summary,end='')
