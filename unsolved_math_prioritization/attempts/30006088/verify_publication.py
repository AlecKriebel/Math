#!/usr/bin/env python3
"""Validate the public-only two-loop SLE partial-results audit delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'AUDIT.md', 'BOOTSTRAP.py', 'CHECK_RUNS.json', 'CORRECTIONS.md', 'DEPENDENCIES.json', 'DEPENDENCY_RUNNER.py', 'HISTORICAL_ACCEPTANCE.json', 'HISTORICAL_PROVENANCE.json', 'MUTATION_TESTS.py', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PUBLICATION_MANIFEST.json', 'PUBLICATION_SCOPE.json', 'README.md', 'REPORT.md', 'REPORT_CORRECTIONS.patch', 'SOURCES.json', 'SOURCE_AUDIT.json', 'STATUS.json', 'VERIFICATION.md', 'audit_exact.mode0.reference.stderr', 'audit_exact.mode0.reference.stdout', 'audit_exact.mode1.reference.stderr', 'audit_exact.mode1.reference.stdout', 'audit_exact.mode2.reference.stderr', 'audit_exact.mode2.reference.stdout', 'audit_exact.py', 'check_exact.mode0.reference.stderr', 'check_exact.mode0.reference.stdout', 'check_exact.mode1.reference.stderr', 'check_exact.mode1.reference.stdout', 'check_exact.mode2.reference.stderr', 'check_exact.mode2.reference.stdout', 'check_exact.py', 'guard_checks.mode0.reference.stderr', 'guard_checks.mode0.reference.stdout', 'guard_checks.mode1.reference.stderr', 'guard_checks.mode1.reference.stdout', 'guard_checks.mode2.reference.stderr', 'guard_checks.mode2.reference.stdout', 'guard_checks.py', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'budget': 5, 'budget_exhausted': True, 'corrections': ['Probability Palm disintegration now requires sigma-finite intensity and standard Borel spaces.', 'Common finite-positive-mass restrictions and measurability stated.', 'ARS lambda range and modulus convention explicit.', 'Benoist-Hongler square-grid, Jordan-domain, + boundary-condition scope explicit.', 'Rare-event counterexample strengthened by Borel-Cantelli to eventual almost-sure emptiness.', 'Executable coverage wording corrected.'], 'decision': 'ACCEPTED_SIX_SCOPED_PROPOSITIONS_AND_CREDITED_ARS_CONSEQUENCES', 'disposition': 'SCOPED_PARTIAL_PROGRESS', 'excluded_stages': {'dataset_replay': 'NOT_RUN', 'formal_proof_assistant_verification': 'NOT_RUN', 'historical_audit_harness_replay': 'NOT_RUN', 'historical_patch_application': 'NOT_RUN', 'new_source_search': 'NOT_RUN', 'original_report_replay': 'NOT_RUN', 'source_body_replay': 'NOT_RUN'}, 'full_embedded_pair_comparison_proved': False, 'general_lattice_CLE_convergence_proved': False, 'graph_inputs': 82, 'independent_environment_check': 1, 'independent_exact_mathematical_checks': 42097, 'independent_numerical_diagnostics': 297, 'installed_dependency_trust': True, 'intentional_failure_controls_per_mode': 1, 'mathematical_acceptance': {'equations_7_9': 'Credited ARS formula and elementary consequences, exact stated parameter conventions.', 'proposition_3': 'Standard Borel, sigma-finite intensity; nested origin-surrounding outer-to-inner sector.', 'proposition_6': 'Finite matching plus factorial-moment uniform integrability; no model-specific hypothesis inferred.', 'propositions_1_2': 'Finite positive-fugacity vertex-disjoint cycle model only.', 'propositions_4_5': 'Ambient Mobius obstruction and finite-restriction conditional-law criterion only.'}, 'new_proof_turns': 0, 'novelty_claim': False, 'numerical_precision_decimal_digits': 70, 'original_exact_checks': {'finite_graph': 1482, 'rare_event': 60, 'symbolic': 6}, 'problem_id': 30006088, 'proof_turns': 5, 'python_modes': ['normal', '-O', '-OO'], 'schema': 1, 'semantic_mutants': 19, 'sixth_approach_added': False, 'worldwide_prior_resolution_claim': False}
EXPECTED_STATUS = {'accepted_results': ['Finite positive-fugacity vertex-disjoint cycle identities and low-fugacity expansion', 'Standard-Borel sigma-finite Palm reduction and restricted nested-sector resolvent', 'Ambient Mobius obstruction and conditional embedded-law criterion', 'Credited ARS transform and elementary descendant/endpoint consequences', 'Conditional finite-matching plus factorial-moment UI convergence criterion'], 'budget': 5, 'full_resolution_accepted': False, 'manuscript_status': 'Authored unrefereed scoped partial-results audit; no novelty or full-resolution claim.', 'new_proof_turns': 0, 'novelty_claimed': False, 'problem_id': 30006088, 'proof_turns': 5, 'publication_scope': 'Target-only authored current mathematics, audit, acceptance, safe checks and public verification metadata. No QUEUE changes.', 'remaining_gaps': ['Complete embedded-pair Radon-Nikodym comparison of cascade and same-realization CLE factorial measure', 'Identification of model annular factor and conditional embedded shape given modulus', 'Required model-specific full lattice-configuration convergence and pair-moment uniform integrability'], 'schema': 1, 'status': 'exhausted_partial'}
EXPECTED_REFERENCE = {'check_exact.py': {'0': {'stdout': {'bytes': 893, 'sha256': '1e2af647c8f3b3f9e50168876aabf2165a3fb5f9783ff0d2d8d89b16cdf6f448'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 893, 'sha256': '1e2af647c8f3b3f9e50168876aabf2165a3fb5f9783ff0d2d8d89b16cdf6f448'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 893, 'sha256': '1e2af647c8f3b3f9e50168876aabf2165a3fb5f9783ff0d2d8d89b16cdf6f448'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'audit_exact.py': {'0': {'stdout': {'bytes': 15267, 'sha256': 'dad00cb8b3d2db1bce9862c3a1d868dec5f1ee10f4dbfcf28a4fadf08e96c29f'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 15267, 'sha256': 'dad00cb8b3d2db1bce9862c3a1d868dec5f1ee10f4dbfcf28a4fadf08e96c29f'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 15267, 'sha256': 'dad00cb8b3d2db1bce9862c3a1d868dec5f1ee10f4dbfcf28a4fadf08e96c29f'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'guard_checks.py': {'0': {'stdout': {'bytes': 59517, 'sha256': '1509c7d9b74e77b9977a05077d33f202ff3e59fdb36ae9c992aafc03fbc851cc'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 59517, 'sha256': '6067feb29eeb513bddc04637c9e36de2c1db4cf3b6ae9ab6d6fdbfb66c92d2bd'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 59517, 'sha256': '0ac536e9e14f597155241e29ef592063a75c133b10ba518790781be441448144'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
SCRIPTS = ('check_exact.py','audit_exact.py','guard_checks.py')
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
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==30006088,'manifest problem')
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
 compare_typed(parse(stdout),parse(refout))
 need(stdout==refout and stderr==referr,'complete stdout/stderr byte equality')
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
  r=subprocess.run([sys.executable,'-I','-S','-B',*mode,*(['DEPENDENCY_RUNNER.py',script]+(['--require-readonly'] if script=='audit_exact.py' else []) if script!='guard_checks.py' else [script])],cwd=root,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=200)
  records.append(compare_output(script,r.returncode,r.stdout,r.stderr,initial[refname(script,'stdout')],initial[refname(script,'stderr')]))
 final=integrity(root,mp,bp);need(final==initial,'whole delivery changed')
 print(json.dumps(dict(schema=1,problem_id=30006088,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,whole_delivery_unchanged=True,before={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(initial.items())},after={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(final.items())},source_body_replay='NOT_RUN',original_report_replay='NOT_RUN',historical_audit_harness_replay='NOT_RUN',historical_patch_application='NOT_RUN',new_source_search='NOT_RUN',dataset_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',mathematics_scope='Six accepted scoped propositions plus credited ARS consequences; full embedded-pair comparison unresolved after 5/5 approaches. Exact checks and numerical diagnostics are distinct.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
