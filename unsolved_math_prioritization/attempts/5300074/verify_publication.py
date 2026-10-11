#!/usr/bin/env python3
"""Validate the public-only external-ray partial-results audit delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'BOOTSTRAP.py', 'CHECKS.md', 'CHECK_RUNS.json', 'HISTORICAL_ACCEPTANCE.json', 'HISTORICAL_PROVENANCE.json', 'INDEPENDENT_AUDIT.md', 'MUTATION_TESTS.py', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_NOTE.json', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PUBLICATION_MANIFEST.json', 'PUBLIC_SOURCE_MANIFEST.json', 'README.md', 'RESULT.md', 'RESULT.md.patch', 'SOURCE_VERIFICATION.json', 'STATUS.json', 'independent_exact_checks.py', 'run_checks.mode0.reference.stderr', 'run_checks.mode0.reference.stdout', 'run_checks.mode1.reference.stderr', 'run_checks.mode1.reference.stdout', 'run_checks.mode2.reference.stderr', 'run_checks.mode2.reference.stdout', 'run_checks.py', 'verify_exact.py', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'accepted_scope': ['Continuous generalized-ray rotation on the strictly repelling marked locus U_d', 'Density of the smooth-ray domain and uniqueness of any continuous extension', 'Connected-Julia neutral-boundary limit from the stated multiplier disk estimate', 'Exact quadratic obstruction to the multiplier-argument shortcut'], 'accepted_small_invariant_subsets': 238, 'analytic_proofs_machine_verified': False, 'budget': 5, 'budget_exhausted': True, 'dataset_replay': 'NOT_RUN', 'disposition': 'ACCEPTED_SCOPED_PARTIAL_AFTER_PROOF_CLARIFICATIONS', 'distinct_degree_angle_set_pairs': 150, 'enumerated_cases': 616, 'finite_rotation_formula_scope': 'cyclic-order-preserving permutation, not arbitrary finite forward-invariant set', 'formal_proof_assistant_verification': 'NOT_RUN', 'full_counterexample': False, 'full_prior_resolution_verified': False, 'full_solution': False, 'historical_original_report_replay': 'NOT_RUN', 'historical_patch_application': 'NOT_RUN', 'historical_receipt_replay': 'NOT_RUN', 'historical_replay': 'NOT_RUN', 'historical_runner_replay': 'NOT_RUN', 'new_proof_turns': 0, 'novelty_claimed': False, 'problem_id': 5300074, 'proof_turns': 5, 'rejected_small_nonrotation_subsets': 423, 'remaining_gaps': ['Disconnected-Julia neutral-boundary continuity, including singleton marked components and irrational rotations', 'Compatibility at every initially accessible indifferent marked point'], 'reviewed_result_sha256': 'b1cbc9b5b77060b8ba57faabcd7927d49df6579a1381ef6dea95b750a2790be1', 'schema': 1, 'sixth_approach_attempted': False, 'source_body_replay': 'NOT_RUN'}
EXPECTED_STATUS = {'accepted_results': ['Continuous generalized-ray rotation on the strictly repelling marked locus U_d', 'Density of the smooth-ray domain and uniqueness of any continuous extension', 'Connected-Julia neutral-boundary limit from the stated multiplier disk estimate', 'Exact quadratic obstruction to the multiplier-argument shortcut'], 'budget': 5, 'full_resolution_accepted': False, 'manuscript_status': 'Authored unrefereed partial-results audit; no journal acceptance or originality claim.', 'new_proof_turns': 0, 'problem_id': 5300074, 'proof_turns': 5, 'publication_scope': 'Target-only authored mathematics, correction patch, audits, acceptance, safe checks and public verification metadata; no QUEUE changes.', 'remaining_gaps': ['Disconnected-Julia neutral-boundary continuity, including singleton marked components and irrational rotations', 'Compatibility at every initially accessible indifferent marked point'], 'schema': 1, 'status': 'exhausted_partial'}
EXPECTED_REFERENCE = {'run_checks.py': {'0': {'stdout': {'bytes': 54243, 'sha256': 'd7ceedfca4bbc65d478962280d5462ffa0767741623090bc165a316acb196ad9'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 54243, 'sha256': 'a31f0094f8c80f0b6409e1557d5a03d4b3d7fac79fc075a660db79afbaaba49d'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 54243, 'sha256': '56aefbd75a3d500ba4f09087bf3f86b7181c7b32ac7fa4c0391e15da21a0938e'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
SCRIPTS = ('run_checks.py',)
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
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==5300074,'manifest problem')
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
 print(json.dumps(dict(schema=1,problem_id=5300074,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,whole_delivery_unchanged=True,before={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(initial.items())},after={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(final.items())},source_body_replay='NOT_RUN',original_report_replay='NOT_RUN',historical_patch_application='NOT_RUN',historical_runner_replay='NOT_RUN',standalone_unittest_main_entrypoint_replay='NOT_RUN',historical_replay='NOT_RUN',dataset_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',mathematics_scope='Repelling-locus continuity and smooth-domain density accepted; disconnected neutral boundary and accessible-indifferent compatibility unresolved. Finite checks only.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
