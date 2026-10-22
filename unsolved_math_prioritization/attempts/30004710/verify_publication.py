#!/usr/bin/env python3
"""Validate the public-only odd-volume convention audit delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'AUDIT_PROVENANCE.json', 'BOOTSTRAP.py', 'CHECK_RESULTS.json', 'CHECK_RUNS.json', 'CORRECTION_NOTICE.md', 'GUARDED_TEST_RESULTS.json', 'MUTATION_TESTS.py', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PUBLICATION_MANIFEST.json', 'README.md', 'REPORT.md', 'SOURCE_MANIFEST.json', 'STATUS.json', 'VERIFICATION.md', 'guard_conventions.mode0.reference.stderr', 'guard_conventions.mode0.reference.stdout', 'guard_conventions.mode1.reference.stderr', 'guard_conventions.mode1.reference.stdout', 'guard_conventions.mode2.reference.stderr', 'guard_conventions.mode2.reference.stdout', 'guard_conventions.py', 'verify_conventions.mode0.reference.stderr', 'verify_conventions.mode0.reference.stdout', 'verify_conventions.mode1.reference.stderr', 'verify_conventions.mode1.reference.stdout', 'verify_conventions.mode2.reference.stderr', 'verify_conventions.mode2.reference.stdout', 'verify_conventions.py', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'MP_calibration_blocker_repaired': True, 'Q3m111_completed': '2*pi^4/3', 'Q3m111_correction': 'pi^4/9', 'Q53_completed': '73*pi^6/420', 'all_tail_factor': '2^(2G-h)', 'audit_report_accepted': True, 'author_endorsed_erratum_claimed': False, 'complete_resolution_accepted': False, 'dataset_replay': 'NOT_RUN', 'disposition': 'ACCEPTED_CONVENTION_AUDIT_WITH_RETAINED_OWR_APPLICATION_HOLD', 'finite_checks_scope': 'Exact bounded arithmetic and convention mapping; not a proof of all geometric dependencies or infinite graph families.', 'formal_proof_assistant_verification': 'NOT_RUN', 'historical_guard_harness_replay': 'NOT_RUN', 'historical_patch_application': 'NOT_RUN', 'new_proof_turns': 0, 'novelty_claimed': False, 'original_report_replay': 'NOT_RUN', 'problem_id': 30004710, 'proof_turns': 0, 'retained_holds': ['OWR_PRODUCT_NORMALIZATION', 'OWR_EXISTENCE_SCOPE'], 'schema': 1, 'source_body_replay': 'NOT_RUN', 'tail_factor': '2^(2a-1)', 'theorem_falsity_claimed': False}
EXPECTED_STATUS = {'audit_review': 'ACCEPTED_CURRENT_CONVENTION_AUDIT_WITH_RETAINED_OWR_HOLD', 'candidate_complete_resolution': False, 'corrected_MP_calibration': {'Q3m111_completed': '2*pi^4/3', 'Q3m111_correction': 'pi^4/9', 'Q53_completed': '73*pi^6/420', 'all_tail_factor': '2^(2G-h)', 'tail_factor': '2^(2a-1)'}, 'decision': 'HOLD_OWR_PRODUCT_NORMALIZATION_AND_EXISTENCE_SCOPE', 'independent_audit_completed': True, 'new_proof_turns': 0, 'next_required_step': 'Settle the OWR product normalization and stratum-existence scope explicitly, or adopt a clearly labeled corrected formulation. The accepted convention audit alone does not resolve the original application.', 'novel_mathematical_solution_claimed': False, 'prior_route': {'n_at_least_four': 'DGY Theorem 2.6 in its stated product normalization.', 'two_singularities': 'MP Theorems 1.1, 5.7 and 6.2 with the explicitly authored, table-compatible quadratic-power convention correction; imported geometric theorems remain credited.'}, 'problem_id': 30004710, 'proof_turns': 0, 'publication_scope': 'Target-only authored audit and public verification metadata; zero proof turns; no status promotion to a complete solution.', 'remaining_holds': [{'finding': 'All 19 OWR coefficients equal 2^h times DGY. Identification requires a stated product convention P_OWR=2^(-h)P_DGY after aligning single quadratic and completed volumes; the inspected OWR text does not supply it.', 'kind': 'OWR_PRODUCT_NORMALIZATION'}, {'finding': 'The all-displayed-strata-exist reading excludes the numerically compatible two-marking cases in the seven OWR families. The broader reading with empty corrections zero requires nonzero special-star terms. Neither reading is silently adopted.', 'kind': 'OWR_EXISTENCE_SCOPE'}], 'schema': 1, 'source_correction_status': 'Authored convention repair; not a verified author-issued erratum. MP p.5 pi exponent separately requires 6 instead of 4.', 'supersedes_original_MP_calibration_blocker': True, 'verification_status': 'PASS_CORRECTED_CONVENTION_AUDIT_WITH_OWR_SCOPE_HOLD'}
EXPECTED_REFERENCE = {'verify_conventions.py': {'0': {'stdout': {'bytes': 9835, 'sha256': '4b28f5f9b356dbfcc3b25782d54ad092409584d250fe2fa4b3e46cc8d0631616'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 9835, 'sha256': '4b28f5f9b356dbfcc3b25782d54ad092409584d250fe2fa4b3e46cc8d0631616'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 9835, 'sha256': '4b28f5f9b356dbfcc3b25782d54ad092409584d250fe2fa4b3e46cc8d0631616'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'guard_conventions.py': {'0': {'stdout': {'bytes': 3891, 'sha256': 'a2d93e40d8247f33202e17aeef0a9eba308e55f6097eeee283ce3d202ebb41ab'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 3891, 'sha256': 'f393114b24ee0520998ba1000eda4fc81f0cb5ed3bcae39e7419da1a777dd1da'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 3891, 'sha256': '32d521823b174a3e491ed0d38b46def5ef54379b786f011c97dc87e351d74581'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
SCRIPTS = ('verify_conventions.py','guard_conventions.py')
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
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==30004710,'manifest problem')
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
 need(snap['CHECK_RESULTS.json']==snap[refname('verify_conventions.py','stdout')],'accepted checker complete output identity')
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
 need(integrity(root,mp,bp)==initial,'whole delivery changed')
 print(json.dumps(dict(schema=1,problem_id=30004710,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,whole_delivery_unchanged=True,source_body_replay='NOT_RUN',original_report_replay='NOT_RUN',historical_patch_application='NOT_RUN',historical_guard_harness_replay='NOT_RUN',dataset_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',mathematics_scope='Accepted convention correction; OWR normalization and existence-scope hold. Finite arithmetic checks only.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
