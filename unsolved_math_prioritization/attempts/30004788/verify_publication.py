#!/usr/bin/env python3
"""Validate the public-only Iwahori partial-analysis delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'AUDIT.md', 'BOOTSTRAP.py', 'CHECK_RUNS.json', 'CORRECTIONS.patch', 'MUTATION_TESTS.py', 'PARTIAL_ANALYSIS.md', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PUBLICATION_MANIFEST.json', 'README.md', 'SOURCE_AUDIT.json', 'SOURCE_METADATA.json', 'STATUS.json', 'VALIDATION.md', 'check_exact.mode0.reference.stderr', 'check_exact.mode0.reference.stdout', 'check_exact.mode1.reference.stderr', 'check_exact.mode1.reference.stdout', 'check_exact.mode2.reference.stderr', 'check_exact.mode2.reference.stdout', 'check_exact.py', 'independent_exact.mode0.reference.stderr', 'independent_exact.mode0.reference.stdout', 'independent_exact.mode1.reference.stderr', 'independent_exact.mode1.reference.stdout', 'independent_exact.mode2.reference.stderr', 'independent_exact.mode2.reference.stdout', 'independent_exact.py', 'semantic_case.py', 'semantic_mutants.mode0.reference.stderr', 'semantic_mutants.mode0.reference.stdout', 'semantic_mutants.mode1.reference.stderr', 'semantic_mutants.mode1.reference.stdout', 'semantic_mutants.mode2.reference.stderr', 'semantic_mutants.mode2.reference.stdout', 'semantic_mutants.py', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'baselines_passed': 6, 'correction_patch': 'CORRECTIONS.patch', 'dataset_replay': 'NOT_RUN', 'date_utc': '2026-10-08', 'evidence_scope': 'Publication edition: derivative and independent exact checks only; final full-delivery evidence externally pinned.', 'formal_proof_assistant_verification': 'NOT_RUN', 'full_problem_solved': False, 'general_hecke_module_model_proved': False, 'historical_patch_application': 'NOT_RUN', 'mathematical_scope': ['Published negative dependence example with quotient/block normalization checks', 'Known rank-one regular model', 'Self-contained Jordan and Fitting-ideal obstruction', 'Six field-independent flag cases supported by full affine equations and finite F2,F3,F5 enumeration', 'Conditional lattice lemma under explicit unproved-in-application hypotheses', 'Limits of compact data and singular Steinberg resolutions'], 'new_p_adic_branching_theorem_claimed': False, 'not_established': ['Full general H_n module presentation', 'All parameter-dependent extensions and boundary gluing', 'Actual central annihilator or uniform lattice denominator for the p-adic module', 'General Steinberg products and singular differential maps', 'Complete independent audit of Chan quotient-branching proof', 'Worldwide absence of prior work'], 'novelty_certified': False, 'original_archive_replay': 'NOT_RUN', 'original_report_replay': 'NOT_RUN', 'parameter_independence': 'FALSE_IN_RANK_TWO_BY_APPLICATION_OF_PRASAD_1993', 'problem_id': 30004788, 'schema': 1, 'semantic_mutations_rejected': 33, 'source_bodies_included': False, 'source_body_replay': 'NOT_RUN', 'status': 'ACCEPTED_CORRECTED_PARTIAL_ONLY', 'steinberg_product_extension_completed': False}
EXPECTED_STATUS = {'accepted_disposition': 'ACCEPTED_CORRECTED_PARTIAL_ONLY', 'full_problem_solved': False, 'missing_deliverable': 'General restricted Iwahori Hecke-module model, parameter-dependent extensions, and compatible Steinberg products', 'novelty_certified': False, 'parameter_independence': 'False already in rank two by a credited application of Prasad 1993', 'problem_id': 30004788, 'proof_search_budget_exhausted': True, 'queue_modified': False, 'schema': 1, 'status': 'PARTIAL_UNRESOLVED_BUDGET_EXHAUSTED', 'turns': '5/5'}
EXPECTED_REFERENCE = {'check_exact.py': {'0': {'stdout': {'bytes': 154, 'sha256': 'dd60937f7f2ba900e32861522d7082aa8a74439db1944dcfba7f947182cce580'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 154, 'sha256': 'dd60937f7f2ba900e32861522d7082aa8a74439db1944dcfba7f947182cce580'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 154, 'sha256': 'dd60937f7f2ba900e32861522d7082aa8a74439db1944dcfba7f947182cce580'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'independent_exact.py': {'0': {'stdout': {'bytes': 1895, 'sha256': 'e5825c84c7f1b19afdf635837c187eb3fd5b2d1702af5539a0dd7ce83c432549'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 1895, 'sha256': 'e5825c84c7f1b19afdf635837c187eb3fd5b2d1702af5539a0dd7ce83c432549'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 1895, 'sha256': 'e5825c84c7f1b19afdf635837c187eb3fd5b2d1702af5539a0dd7ce83c432549'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'semantic_mutants.py': {'0': {'stdout': {'bytes': 6030, 'sha256': '7189af3be3ccfbf79d35ed68ab016c5cc8b6b2e8eaa67ed5ffbc905e28ff82cd'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 6096, 'sha256': 'd2d7b6cdc1f82beba36ecf342cee62622b10a52cb0f3095285b06bfdd420a68c'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 6107, 'sha256': '23e832c0a07d42372cb187d3e5faa862a28408c77d5f31a628ffb78ca7921b99'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
SCRIPTS = ('check_exact.py','independent_exact.py','semantic_mutants.py')
MAX_BYTES=2000000
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def same(a,b):
 if type(a) is not type(b):return False
 if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
 if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def compare_typed(a,b):need(same(a,b),'recursive exact JSON types and values')
def unique(pairs):
 result={}
 for k,v in pairs:need(k not in result,'duplicate JSON key');result[k]=v
 return result
def nonfinite(token):raise ValueError('nonfinite JSON')
def number(token):
 x=float(token);need(math.isfinite(x),'overflow JSON');return x
def parse(raw):return json.loads(raw,object_pairs_hook=unique,parse_constant=nonfinite,parse_float=number)
def keys(x,wanted):need(type(x) is dict and set(x)==set(wanted),'object schema')
def integer(x):need(type(x) is int and 0<=x<=MAX_BYTES,'bounded exact integer')
def digest(x):need(type(x) is str and re.fullmatch('[0-9a-f]{64}',x) is not None,'SHA-256')
def ordinary(path):
 for p in path.parents:need(stat.S_ISDIR(p.lstat().st_mode),'linked ancestor')
 st=path.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1 and st.st_size<=MAX_BYTES,'ordinary bounded single-link file')
 with os.fdopen(os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)),'rb') as f:
  fs=os.fstat(f.fileno());need((st.st_dev,st.st_ino,st.st_size)==(fs.st_dev,fs.st_ino,fs.st_size),'replaced file');raw=f.read(MAX_BYTES+1)
 need(len(raw)==st.st_size,'changed size');return raw
def inventory(root):
 for p in (root,*root.parents):need(stat.S_ISDIR(p.lstat().st_mode),'linked root or ancestor')
 entries=list(os.scandir(root));need({e.name for e in entries}==FILES,'exact flat inventory')
 need(all(stat.S_ISREG(e.stat(follow_symlinks=False).st_mode) for e in entries),'linked or special member')
def validate_manifest(m,snapshot):
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==30004788,'manifest problem')
 need(type(m['files']) is list and len(m['files'])==len(PAYLOAD),'manifest inventory length');seen=set()
 for row in m['files']:
  keys(row,['path','bytes','sha256']);n=row['path'];need(type(n) is str and n in PAYLOAD and n not in seen,'manifest path');seen.add(n)
  integer(row['bytes']);digest(row['sha256']);need(same(row,dict(path=n,bytes=len(snapshot[n]),sha256=sha(snapshot[n]))),'manifest member binding')
 need(seen==PAYLOAD,'complete manifest')
def validate_acceptance(a):compare_typed(a,EXPECTED_ACCEPTANCE)
def validate_status(a):compare_typed(a,EXPECTED_STATUS)
def refname(script,kind):return script[:-3]+'.mode'+str(sys.flags.optimize)+'.reference.'+kind
def compare_output(script,exit_code,stdout,stderr,refout,referr):
 need(script in SCRIPTS,'known script');need(type(exit_code) is int and exit_code==0,'exact successful exit');need(all(type(x) is bytes for x in (stdout,stderr,refout,referr)),'output bytes')
 for kind,raw in [('stdout',refout),('stderr',referr)]:need(same(dict(bytes=len(raw),sha256=sha(raw)),EXPECTED_REFERENCE[script][str(sys.flags.optimize)][kind]),'mode-specific reference identity')
 compare_typed(parse(stdout),parse(refout));need(stdout==refout and stderr==referr,'complete stdout/stderr byte equality')
 return dict(script=script,exit_code=exit_code,stdout=stdout.decode(),stderr=stderr.decode(),stdout_bytes=len(stdout),stdout_sha256=sha(stdout),stderr_bytes=len(stderr),stderr_sha256=sha(stderr),complete_output_comparison=True,recursive_exact_type_comparison=True,normalization='NONE')
def integrity(root,mp,bp):
 digest(mp);digest(bp);inventory(root);snap={n:ordinary(root/n) for n in FILES}
 need(sha(snap['PUBLICATION_MANIFEST.json'])==mp,'external manifest pin');need(sha(snap['BOOTSTRAP.py'])==bp,'external bootstrap pin')
 validate_manifest(parse(snap['PUBLICATION_MANIFEST.json']),snap)
 parsed={n:parse(raw) for n,raw in snap.items() if n.endswith('.json')}
 validate_acceptance(parsed['ACCEPTANCE.json']);validate_status(parsed['STATUS.json'])
 for n in FILES:
  if n.endswith('.py'):need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(snap[n]))),'assertion-free delivery code')
 for n in SCRIPTS:compare_output(n,0,snap[refname(n,'stdout')],snap[refname(n,'stderr')],snap[refname(n,'stdout')],snap[refname(n,'stderr')])
 return snap
def readonly(root):
 rows=[]
 for p,label,d in [(root,'.',True)]+[(root/n,n,False) for n in sorted(FILES)]:
  need((p.stat().st_mode&0o777)==(0o555 if d else 0o444) and not os.access(p,os.W_OK),'read-only permissions')
  try:fd=os.open(p/'FORBIDDEN_CREATE' if d else p,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if d else os.O_APPEND),0o600)
  except PermissionError as e:need(e.errno==13,'physical denial errno');rows.append(dict(path=label,operation='create' if d else 'append_open',errno=13,denied=True))
  else:os.close(fd);raise ValueError('physical write unexpectedly allowed')
 return rows
def main():
 need(len(sys.argv)==4,'manifest pin, bootstrap pin, packet required');mp,bp,rs=sys.argv[1:];root=Path(os.path.abspath(rs))
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'isolated no-site no-bytecode')
 initial=integrity(root,mp,bp);probes=readonly(root);mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];records=[]
 for script in SCRIPTS:
  r=subprocess.run([sys.executable,'-I','-S','-B',*mode,script],cwd=root,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=200)
  records.append(compare_output(script,r.returncode,r.stdout,r.stderr,initial[refname(script,'stdout')],initial[refname(script,'stderr')]))
 final=integrity(root,mp,bp);need(final==initial,'whole delivery changed')
 pins_before={n:dict(bytes=len(raw),sha256=sha(raw)) for n,raw in sorted(initial.items())};pins_after={n:dict(bytes=len(raw),sha256=sha(raw)) for n,raw in sorted(final.items())}
 print(json.dumps(dict(schema=1,problem_id=30004788,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,file_pins_before=pins_before,file_pins_after=pins_after,whole_delivery_unchanged=True,source_body_replay='NOT_RUN',original_report_replay='NOT_RUN',original_archive_replay='NOT_RUN',historical_patch_application='NOT_RUN',dataset_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',mathematics_scope='Corrected partial-only analysis; full p-adic module model unresolved. Bounded regression evidence only.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
