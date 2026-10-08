#!/usr/bin/env python3
"""Validate the public-only extremal partial-results audit delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'AUDIT_REPORT.md', 'BOOTSTRAP.py', 'CHECK_RUNS.json', 'CLAIM_AND_SCOPE.md', 'CORRECTIONS.md', 'EXACT_AUDIT_RESULTS.json', 'HISTORICAL_ACCEPTANCE.json', 'HISTORICAL_REPRODUCIBILITY.json', 'MUTATION_TESTS.py', 'ORIGINAL_EXACT_RESULTS.json', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PUBLICATION_MANIFEST.json', 'README.md', 'RESULT.json', 'RESULT.md', 'REVIEWED_INPUTS.json', 'ROUTE_1_MASS_AND_RADIAL.md', 'ROUTE_2_STABLE_POTENTIAL_OBSTRUCTION.md', 'ROUTE_3_DIFFERENTIAL_BOOTSTRAP.md', 'ROUTE_4_BLOWUP_AND_ENTIRE_SOLUTION.md', 'ROUTE_5_NONLINEAR_REALIZATION.md', 'ROUTE_LEDGER.md', 'SOURCE_AUDIT.md', 'SOURCE_METADATA.json', 'SOURCE_VERIFICATION.json', 'STATUS.json', 'VERIFICATION.md', 'audit_exact.mode0.reference.stderr', 'audit_exact.mode0.reference.stdout', 'audit_exact.mode1.reference.stderr', 'audit_exact.mode1.reference.stdout', 'audit_exact.mode2.reference.stderr', 'audit_exact.mode2.reference.stdout', 'audit_exact.py', 'check_exact.mode0.reference.stderr', 'check_exact.mode0.reference.stdout', 'check_exact.mode1.reference.stderr', 'check_exact.mode1.reference.stdout', 'check_exact.mode2.reference.stderr', 'check_exact.mode2.reference.stdout', 'check_exact.py', 'guard_checks.mode0.reference.stderr', 'guard_checks.mode0.reference.stdout', 'guard_checks.mode1.reference.stderr', 'guard_checks.mode1.reference.stdout', 'guard_checks.mode2.reference.stderr', 'guard_checks.mode2.reference.stdout', 'guard_checks.py', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'additional_proof_search_routes': 0, 'all_five_route_arguments_independently_reviewed': True, 'authored_mathematics_unchanged': True, 'counterexample_to_full_target': False, 'disposition': 'accepted_as_scoped_unresolved_partial_report', 'full_target_proved': False, 'independent_exact_checks_per_mode': 41, 'mathematical_corrections_required': False, 'mathematical_prose_certification': 'Independent mathematical audit tied to externally pinned reviewed bytes; not automatic proof certification', 'novelty_claimed': False, 'numerical_evidence': False, 'optimization_modes': ['normal', 'O', 'OO'], 'original_exact_checks_per_mode': 23, 'original_integrity_verifier_included': False, 'original_integrity_verifier_replay': 'NOT_RUN', 'problem_id': 30005996, 'remaining_gap': 'Derive spatial nonconcentration from the full extremal problem, or construct a compatible source-admissible positive zero-Dirichlet extremal counterexample.', 'schema': 1, 'source_body_free': True, 'source_hypotheses_checked': True, 'substantive_route_limit': 5, 'substantive_routes_used': 5}
EXPECTED_STATUS = {'counterexample_to_full_target': False, 'entire_profile_dimension_minimum': 10, 'entire_stable_profile_counterexample_to_full_target': False, 'ff_v2_scope': 'Averaged bounds and a pointwise lower conclusion; no target pointwise upper theorem', 'formal_proof_assistant_verification': 'NOT_RUN', 'full_target_proved': False, 'new_routes': 0, 'new_source_search': 'NOT_RUN', 'novelty_claimed': False, 'problem_id': 30005996, 'route_limit': 5, 'routes_used': 5, 'schema': 1, 'source_body_replay': 'NOT_RUN', 'source_class': 'Differentiable positive increasing convex f with f(0)>0, finite integral of 1/f, and superlinear growth; finite positive lambda*; isolated interior singularity', 'stable_potential_counterexample_to_full_target': False, 'status': 'UNRESOLVED'}
EXPECTED_REFERENCE = {'check_exact.py': {'0': {'stdout': {'bytes': 2972, 'sha256': 'd3acadfcbf2196bae14fb2f07ed6f5a2a2a7d921887c4fb1807380e2d93f7f0d'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 2972, 'sha256': 'd3acadfcbf2196bae14fb2f07ed6f5a2a2a7d921887c4fb1807380e2d93f7f0d'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 2972, 'sha256': 'd3acadfcbf2196bae14fb2f07ed6f5a2a2a7d921887c4fb1807380e2d93f7f0d'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'audit_exact.py': {'0': {'stdout': {'bytes': 4930, 'sha256': 'a4a86eb7ea751db4825db17c88208781181eb75cf45f9cdc7ccacfd1006739cf'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 4930, 'sha256': 'a4a86eb7ea751db4825db17c88208781181eb75cf45f9cdc7ccacfd1006739cf'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 4930, 'sha256': 'a4a86eb7ea751db4825db17c88208781181eb75cf45f9cdc7ccacfd1006739cf'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'guard_checks.py': {'0': {'stdout': {'bytes': 75305, 'sha256': 'f8243ad0eda97eecbfdedbfb248cf84710f3d0866c0b0a160462250710a58837'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 75305, 'sha256': '21b69c9cc62d7deca72f974e220e780f840d86f2957e1203f2758a360b2b77b4'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 75305, 'sha256': '834ed26ce0933621bee45018c6bb1c44be75bff6288183824182c703ad9f9a7c'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
SCRIPTS = ('check_exact.py','audit_exact.py','guard_checks.py')
LAUNCHER = "import os,sys,sysconfig;from pathlib import Path;\nif os.getuid()!=1000 or os.geteuid()!=1000:raise RuntimeError('UID/EUID 1000 required')\nsys.path.append(sysconfig.get_path('purelib'));import sympy,mpmath\nif sympy.__version__!='1.14.0' or mpmath.__version__!='1.3.0':raise RuntimeError('tested dependency versions required')\nn=sys.argv[1];sys.argv=sys.argv[1:];exec(compile(Path(n).read_bytes(),n,'exec'),{'__name__':'__main__','__file__':str(Path(n).resolve())})"
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
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==30005996,'manifest problem')
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
 need(snap['ORIGINAL_EXACT_RESULTS.json']==snap[refname('check_exact.py','stdout')],'accepted corrected checker output identity')
 need(snap['EXACT_AUDIT_RESULTS.json']==snap[refname('audit_exact.py','stdout')],'accepted independent checker output identity')
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
  r=subprocess.run([sys.executable,'-I','-S','-B',*mode,'-c',LAUNCHER,script],cwd=root,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=200)
  records.append(compare_output(script,r.returncode,r.stdout,r.stderr,initial[refname(script,'stdout')],initial[refname(script,'stderr')]))
 final=integrity(root,mp,bp);need(final==initial,'whole delivery changed')
 print(json.dumps(dict(schema=1,problem_id=30005996,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,whole_delivery_unchanged=True,before={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(initial.items())},after={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(final.items())},source_body_replay='NOT_RUN',original_integrity_verifier_replay='NOT_RUN',historical_audit_harness_replay='NOT_RUN',new_source_search='NOT_RUN',dataset_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',mathematics_scope='Five accepted scoped partial results; full extremal pointwise upper target unresolved. Finite arithmetic checks only.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
