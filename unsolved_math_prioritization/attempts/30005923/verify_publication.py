#!/usr/bin/env python3
"""Validate the public-only row-ball fixed-parameter audit delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'ADDITIONAL_SOURCE_METADATA.json', 'AUDIT_PROVENANCE.json', 'AUDIT_REPORT.md', 'BOOTSTRAP.py', 'FIXED_G_PROOF.md', 'HISTORICAL_ACCEPTANCE.json', 'HISTORICAL_CALCULATION_RESULTS.json', 'HISTORICAL_CHECK_RESULTS.json', 'INDEPENDENT_AUDIT.md', 'MUTATION_TESTS.py', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PROOF_INTERFACE_ADDENDUM.md', 'PUBLICATION_MANIFEST.json', 'PUBLIC_SOURCE_METADATA.json', 'README.md', 'REFERENCE_CAPTURE.json', 'SCOPE_DISPOSITION.json', 'STATUS.json', 'VERIFICATION.md', 'guard_row_ball.mode0.reference.stderr', 'guard_row_ball.mode0.reference.stdout', 'guard_row_ball.mode1.reference.stderr', 'guard_row_ball.mode1.reference.stdout', 'guard_row_ball.mode2.reference.stderr', 'guard_row_ball.mode2.reference.stdout', 'guard_row_ball.py', 'verify_publication.py', 'verify_row_ball.mode0.reference.stderr', 'verify_row_ball.mode0.reference.stdout', 'verify_row_ball.mode1.reference.stderr', 'verify_row_ball.mode1.reference.stdout', 'verify_row_ball.mode2.reference.stderr', 'verify_row_ball.mode2.reference.stdout', 'verify_row_ball.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'companion': 'CREDITED_PRIOR_RESULT_WITH_EXPLICIT_REPAIRS', 'companion_id': 30005922, 'constant_uniform_in_g': False, 'dataset_replay': 'NOT_RUN', 'finite_tests_scope': 'Deterministic finite interfaces and scope/integrity checks; not a universal analytic proof or an all-g bound.', 'fixed_g_moment': 'ACCEPT_C(g,k,r,m)', 'formal_proof_assistant_verification': 'NOT_RUN', 'full_manuscript_accepted': False, 'historical_audit_verifier_replay': 'NOT_RUN', 'journal_acceptance_of_2607_25980_claimed': False, 'local_uniformity': 'FIXED_DIMENSION_PRODUCT_OPEN_ROW_BALLS', 'main_target': 'HOLD_VARIABLE_COUNT_UNIFORMITY', 'mathematical_patch_required': False, 'monotonicity_verified': False, 'new_research_turns': 0, 'novelty_claimed': False, 'optimal_constant_verified': False, 'original_verifier_replay': 'NOT_RUN', 'outer_domain': 'POINTWISE_STRICT_OUTER_SPECTRAL_RADIUS', 'problem_id': 30005923, 'proof_turns': 0, 'queue_changes': False, 'quotient_theorem_accepted': False, 'remote_ci': 'NOT_RUN', 'remote_readback': 'NOT_RUN', 'schema': 1, 'source_body_replay': 'NOT_RUN', 'source_documents_in_packet': False, 'unrestricted_mixed_word_theorem_accepted': False, 'verdict': 'ACCEPT_FIXED_PARAMETER_RECONSTRUCTION_WITH_DOCUMENTED_SCOPE'}
EXPECTED_STATUS = {'accepted_scope': 'Fixed-g positive moments; fixed-parameter covariance for strict outer spectral radius; fixed-dimensional product-row-ball local uniformity.', 'companion_disposition': 'CREDITED_PRIOR_RESULT_WITH_EXPLICIT_REPAIRS', 'companion_id': 30005922, 'disposition': 'HOLD_VARIABLE_COUNT_UNIFORMITY', 'full_manuscript_accepted': False, 'new_research_turns': 0, 'novelty_claimed': False, 'problem_id': 30005923, 'proof_turns': 0, 'schema': 1, 'seven_repairs': ['fixed-g pointwise ceiling', 'tail integration additive one', 'logarithm and reciprocal-determinant signs', 'joint holomorphic normal-family uniqueness', 'second determinant restored', 'unnormalized FK factor 2k', 'positive/inverse-word centering only'], 'unresolved_bridge': 'No verified bound on C(g,k,r,1) as g varies. Fixed-dimensional compactness and coefficient estimates retain fixed g.'}
EXPECTED_REFERENCE = {'verify_row_ball.py': {'0': {'stdout': {'bytes': 1540, 'sha256': '510e2e03e8f65047056e7efe8172d7d6b1bfbfefa74ef6682297257bfac6867a'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 1540, 'sha256': 'eec1ef03936739fc5008be58f5721a4ffb2c9e0996f8424ed95e17a0f9e492e8'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 1540, 'sha256': '5b8b765329045a3d4b6c7055e4172b32309b267f38799e677cd84b99b1d69e2e'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'guard_row_ball.py': {'0': {'stdout': {'bytes': 3331, 'sha256': '27450f4d48e8e69cce773e25df54c364d0e09e2f91fd31306b22fc3b4aa40d6d'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 3331, 'sha256': 'd84ad5d0ea16a75c3acee00cd704ebb2519460781a327dcffeba354d464d65f1'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 3331, 'sha256': '095a2073bfed00fec94e3a00009ba764c37f4dbd51a1df4887a8e9a0942a50ca'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
SCRIPTS = ('verify_row_ball.py','guard_row_ball.py')
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
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==30005923,'manifest problem')
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
 print(json.dumps(dict(schema=1,problem_id=30005923,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,whole_delivery_unchanged=True,before_sha256={n:sha(b) for n,b in sorted(initial.items())},after_sha256={n:sha(b) for n,b in sorted(final.items())},source_body_replay='NOT_RUN',original_verifier_replay='NOT_RUN',historical_patch_application='NOT_RUN',historical_audit_verifier_replay='NOT_RUN',dataset_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',mathematics_scope='Repaired fixed-g prior theorem and fixed-parameter companion covariance; variable-count-uniformity HOLD retained.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
