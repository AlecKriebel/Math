#!/usr/bin/env python3
"""Validate the public-only Coxeter partial-results audit delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['01_equivariant_quotients.md', '02_clique_overlap_rigidity.md', '03_direct_factor_reduction.md', '04_conjugator_cocycle_obstruction.md', '05_standard_representation_obstruction.md', 'ACCEPTANCE.json', 'ACCEPTANCE.md', 'BOOTSTRAP.py', 'CHECK_RUNS.json', 'CORRECTION_NOTE.md', 'HISTORICAL_ACCEPTANCE.json', 'HISTORICAL_PROVENANCE.json', 'INDEPENDENT_MATHEMATICAL_AUDIT.md', 'MUTATION_TESTS.py', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PUBLICATION_MANIFEST.json', 'README.md', 'SOURCE_AUDIT.md', 'STATUS.json', 'VERIFICATION.md', 'guard_checks.mode0.reference.stderr', 'guard_checks.mode0.reference.stdout', 'guard_checks.mode1.reference.stderr', 'guard_checks.mode1.reference.stdout', 'guard_checks.mode2.reference.stderr', 'guard_checks.mode2.reference.stdout', 'guard_checks.py', 'independent_source_check.json', 'independent_verify.mode0.reference.stderr', 'independent_verify.mode0.reference.stdout', 'independent_verify.mode1.reference.stderr', 'independent_verify.mode1.reference.stdout', 'independent_verify.mode2.reference.stderr', 'independent_verify.mode2.reference.stdout', 'independent_verify.py', 'source_manifest.json', 'verify_calculations_hardened.mode0.reference.stderr', 'verify_calculations_hardened.mode0.reference.stdout', 'verify_calculations_hardened.mode1.reference.stderr', 'verify_calculations_hardened.mode1.reference.stdout', 'verify_calculations_hardened.mode2.reference.stderr', 'verify_calculations_hardened.mode2.reference.stdout', 'verify_calculations_hardened.py', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'budget': 5, 'budget_exhausted': True, 'connected_cyclic_graphs': 626, 'dataset_replay': 'NOT_RUN', 'decision': 'ACCEPTED_FIVE_SCOPED_MATHEMATICAL_CLAIMS', 'formal_proof_assistant_verification': 'NOT_RUN', 'full_candidate': False, 'full_conjecture_counterexample': False, 'full_target_status': 'unresolved_exhausted', 'hardened_semantic_mutants': 3, 'historical_audit_harness_replay': 'NOT_RUN', 'historical_centerless_clique_assertion_used_as_input': False, 'historical_five_mode_replay': 'NOT_RUN', 'independent_baseline_checks': 6066, 'independent_semantic_mutants': 14, 'mathematical_claims': [{'decision': 'accepted_with_stated_hypotheses_and_gap', 'file': '01_equivariant_quotients.md'}, {'decision': 'accepted_with_stated_hypotheses_and_gap', 'file': '02_clique_overlap_rigidity.md'}, {'decision': 'accepted_with_stated_hypotheses_and_gap', 'file': '03_direct_factor_reduction.md'}, {'decision': 'accepted_with_stated_hypotheses_and_gap', 'file': '04_conjugator_cocycle_obstruction.md'}, {'decision': 'accepted_with_stated_hypotheses_and_gap', 'file': '05_standard_representation_obstruction.md'}], 'mathematical_correction_required': False, 'new_proof_turns': 0, 'new_source_search': 'NOT_RUN', 'novelty_certified': False, 'original_checker_delivered': False, 'portable_original_checker_replay': 'NOT_RUN', 'problem_id': 30004454, 'proof_turns': 5, 'schema': 1, 'sixth_approach_attempted': False, 'source_authority': 'Varghese published 2026 version, Conjecture 1.2 and stated corrected sufficient hypotheses', 'source_body_replay': 'NOT_RUN', 'verification_correction': 'Original 11 assert predicates replaced by explicit exceptions in unchanged hardened checker'}
EXPECTED_STATUS = {'accepted_results': ['Equivariant presentation quotient criteria', 'Finite-centralizer spanning-tree bound', 'Full factor-stabilizer surjective reduction', 'Retraction and unique-conjugator obstruction', 'Standard reflection representation obstruction'], 'budget': 5, 'full_conjecture_counterexample': False, 'full_resolution_accepted': False, 'manuscript_status': 'Authored unrefereed partial-results audit; no journal acceptance or originality claim.', 'new_proof_turns': 0, 'novelty_claimed': False, 'problem_id': 30004454, 'proof_turns': 5, 'publication_scope': 'Target-only authored proofs, audit, acceptance, safe checks and public verification metadata; no QUEUE changes.', 'remaining_gaps': ['No universal invariant infinite finite-Out quotient construction', 'Infinite clique-overlap centralizers defeat finite counting', 'Infinite irreducible groups with infinite outer automorphism groups remain', 'Unique conjugators need not give homomorphisms', 'Standard geometric implementation does not provide the desired abstract epimorphism'], 'schema': 1, 'status': 'exhausted_partial'}
EXPECTED_REFERENCE = {'verify_calculations_hardened.py': {'0': {'stdout': {'bytes': 86, 'sha256': '18fedf0aee0848985c6a09032ae004031722efd9912760c4e03f2ba57a9d56cd'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 86, 'sha256': '18fedf0aee0848985c6a09032ae004031722efd9912760c4e03f2ba57a9d56cd'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 86, 'sha256': '18fedf0aee0848985c6a09032ae004031722efd9912760c4e03f2ba57a9d56cd'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'independent_verify.py': {'0': {'stdout': {'bytes': 119, 'sha256': '877c3010e4465cbc40c96ac78168d3d33ff0c8070c8f7eb6745e576b96904a90'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 119, 'sha256': 'a844c2a4671e52ec6c4ed35d082d369059254959bb3d10712fb1aab4defa5f67'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 119, 'sha256': 'abb464fc298679301cc711c667208c8077bffdcec18773814e65c13f34c2c5fc'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'guard_checks.py': {'0': {'stdout': {'bytes': 30464, 'sha256': 'c74138fb2ec6cebe3a50ddacd14b03826f11a13379da7c68f2f400f316b08775'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 30464, 'sha256': '9aa4599472ea1942bce7c2caec848a04e6df0ba0191d4f8ffacb4dd4941c1cbc'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 30464, 'sha256': '19863ddbc1e6f3a4fffafc8c3bddf1edf9a48dd1b577156316ae81dc606f0c90'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
SCRIPTS = ('verify_calculations_hardened.py','independent_verify.py','guard_checks.py')
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
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==30004454,'manifest problem')
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
 if script!='verify_calculations_hardened.py':compare_typed(parse(stdout),parse(refout))
 need(stdout==refout and stderr==referr,'complete stdout/stderr byte equality')
 return dict(script=script,exit_code=exit_code,stdout=stdout.decode(),stderr=stderr.decode(),stdout_bytes=len(stdout),stdout_sha256=sha(stdout),stderr_bytes=len(stderr),stderr_sha256=sha(stderr),complete_output_comparison=True,recursive_exact_type_comparison=script!='verify_calculations_hardened.py',normalization='NONE')
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
 print(json.dumps(dict(schema=1,problem_id=30004454,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,whole_delivery_unchanged=True,before={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(initial.items())},after={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(final.items())},source_body_replay='NOT_RUN',portable_original_checker_replay='NOT_RUN',historical_audit_harness_replay='NOT_RUN',historical_five_mode_replay='NOT_RUN',new_source_search='NOT_RUN',dataset_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',mathematics_scope='Five accepted scoped Coxeter claims; full target unresolved after 5/5 approaches. Finite supporting checks only.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
