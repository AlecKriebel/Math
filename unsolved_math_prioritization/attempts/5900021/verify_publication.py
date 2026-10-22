#!/usr/bin/env python3
"""Validate the public-only equal-pressure foam scoped partial-results audit delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'BOOTSTRAP.py', 'CHECK_RUNS.json', 'HISTORICAL_ACCEPTANCE.json', 'MUTATION_TESTS.py', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PUBLICATION_MANIFEST.json', 'PUBLICATION_SCOPE.json', 'README.md', 'STATUS.json', 'audit/AUDIT.md', 'audit/AUDIT_PINS.json', 'audit/CORRECTION.patch', 'audit/ORIGINAL_PINS.json', 'audit/README.md', 'audit/SOURCE_VERIFICATION.json', 'audit/check_independent.py', 'audit_check_independent.mode0.reference.stderr', 'audit_check_independent.mode0.reference.stdout', 'audit_check_independent.mode1.reference.stderr', 'audit_check_independent.mode1.reference.stdout', 'audit_check_independent.mode2.reference.stderr', 'audit_check_independent.mode2.reference.stdout', 'current/CLAIMS.json', 'current/PAYLOAD_PINS.json', 'current/README.md', 'current/RESULTS.md', 'current/SOURCE_MANIFEST.json', 'current/STATUS.json', 'current/VALIDATION.json', 'current/verify.py', 'current_verify.mode0.reference.stderr', 'current_verify.mode0.reference.stdout', 'current_verify.mode1.reference.stderr', 'current_verify.mode1.reference.stdout', 'current_verify.mode2.reference.stderr', 'current_verify.mode2.reference.stdout', 'guard_checks.mode0.reference.stderr', 'guard_checks.mode0.reference.stdout', 'guard_checks.mode1.reference.stderr', 'guard_checks.mode1.reference.stdout', 'guard_checks.mode2.reference.stderr', 'guard_checks.mode2.reference.stdout', 'guard_checks.py', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'approaches_exhausted': '5/5', 'decision': 'ACCEPTED_SCOPED_PARTIAL_WITH_CLARIFICATIONS', 'dodecahedral_occurrence': 'unresolved', 'excluded_stages': {'dataset_replay': 'NOT_RUN', 'formal_proof_assistant_verification': 'NOT_RUN', 'historical_audit_harness_replay': 'NOT_RUN', 'historical_patch_application': 'NOT_RUN', 'new_source_search': 'NOT_RUN', 'original_report_replay': 'NOT_RUN', 'source_body_replay': 'NOT_RUN'}, 'finite_combinatorial_types': 'unresolved', 'full_target_resolved': False, 'geometry_algebra_mutants': 10, 'hypothesis_status_guards': 6, 'independent_checks_with_readonly': 227, 'limits': 'Finite exact and scope checks support but do not machine-prove analytic theorems, PDE existence, classification or global realization.', 'mathematical_scope': {'N9': 'arithmetic count threshold only, not a realized periodic quotient', 'borders': 'intervals', 'cell_closure': 'ball', 'closed_faces': 'disks', 'compact_stationarity': 'compactly supported finite-area boundaryless regular Plateau film with minimal interfaces', 'edge_curvature_bound': 'norm-one conormal-pair bound; each edge counted once', 'finite_types': 'conditional on uniform per-cell Q+T bound, not proved', 'local_junction': 'truncated planar annulus plus two catenoid annuli; no completed minimal disks or global foam', 'regularity': 'finite facewise Gauss-Bonnet curvature terms', 'vertex_valence': 3}, 'new_proof_turns': 0, 'novelty_claimed': False, 'original_checks': 56, 'original_input_negative_controls': 7, 'problem_id': 5900021, 'schema': 1, 'semantic_mutants': 16, 'source_scope': 'SM96 and S98 author PDFs historically retrieved and inspected; Kusner ResearchGate HTML preview provenance unverified, no inspected Kusner PDF claimed.', 'tetrahedral_occurrence': 'unresolved', 'two_faced_continuation': 'unresolved'}
EXPECTED_STATUS = {'approaches_exhausted': '5/5', 'dodecahedral_occurrence': 'unresolved', 'finite_combinatorial_types': 'unresolved', 'full_target_resolved': False, 'global_foam_constructed': False, 'manuscript_status': 'Authored unrefereed scoped partial-results audit; no full-resolution or novelty claim.', 'new_proof_turns': 0, 'novelty_claimed': False, 'problem_id': 5900021, 'publication_scope': 'Target-only current mathematics, full authored audit, authored correction patch, acceptance, safe checks and public verification metadata; no QUEUE changes.', 'schema': 1, 'sixth_approach_added': False, 'status': 'exhausted_partial', 'tetrahedral_occurrence': 'unresolved', 'two_faced_continuation': 'unresolved'}
EXPECTED_REFERENCE = {'current/verify.py': {'0': {'stdout': {'bytes': 9835, 'sha256': '905abb8495e4722091a0c10d860c29e5a51f328b401ff16b75ac29aa99ccf638'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 9835, 'sha256': '905abb8495e4722091a0c10d860c29e5a51f328b401ff16b75ac29aa99ccf638'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 9835, 'sha256': '905abb8495e4722091a0c10d860c29e5a51f328b401ff16b75ac29aa99ccf638'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'audit/check_independent.py': {'0': {'stdout': {'bytes': 19305, 'sha256': 'a9619c058faaec7de18b7a8c408e1cfb936cba695c2c58d7da6410b30b4068d7'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 19305, 'sha256': 'a9619c058faaec7de18b7a8c408e1cfb936cba695c2c58d7da6410b30b4068d7'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 19305, 'sha256': 'a9619c058faaec7de18b7a8c408e1cfb936cba695c2c58d7da6410b30b4068d7'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'guard_checks.py': {'0': {'stdout': {'bytes': 7619, 'sha256': 'd603c9c8aaa7a29c0cb748addb8c3453ceac31446dc5ef4c3c43e24122eec34a'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 7619, 'sha256': '6032d7659f0c44c2c56e6aa6628cb8b39f6bff4085ba58687a462a54b0e08e8b'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 7619, 'sha256': 'af4b2225c4627327e420d02cbb64757d917b947baa00ad23ecf411a16ca1ba2a'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
SCRIPTS = ('current/verify.py','audit/check_independent.py','guard_checks.py')
DIRS = {'current','audit'}
EXPECTED_CLAIMS = {'angles': {'cos_alpha': '-1/3', 'cos_theta': '1/3', 'delta_pi_coefficient': -1, 'delta_theta_coefficient': 3}, 'circle_junction': {'a_squared': '3/4', 'all_z_ode_identity': True, 'complete_bounded_cell': False, 'inward_conormals_r_z': [['1', '0'], ['-1/2', 'sqrt(3)/2'], ['-1/2', '-sqrt(3)/2']], 'minimal_ode': 'r*r_second-r_first**2=1', 'r_at_zero': 1, 'region_integrals_pi': [2, -1, -1], 'rprime_at_zero_sign': -1, 'rprime_at_zero_squared': '1/3', 'sheet_geodesic_curvatures': ['-1', '1/2', '1/2']}, 'compact_stationarity': {'boundaryless_required': True, 'compact_support_required': True, 'divergence_dimension': 2, 'excludes_infinite_foam': False}, 'conditional_finite_types': {'bound_proved': False, 'uniform_Q_plus_T_bound_required': True}, 'display': {'D12': '1.5406586457', 'D13': '0.4380874488', 'D14': '-0.6644837480', 'D4': '10.3612282206', 'average_threshold': '13.3973325714376', 'density_cap': '0.1116602359750'}, 'incidence': {'E_F_coefficient': 3, 'E_constant': -6, 'V_F_coefficient': 2, 'V_constant': -4}, 'schema': 1, 'scope': {'approaches_exhausted': '5/5', 'borders': 'intervals', 'cell_closure': 'ball', 'closed_faces': 'disks', 'finite_curvature_terms': True, 'full_target_resolved': False, 'general_nonsimple_coverage': False, 'global_construction': False, 'two_faced_continuation_resolved': False, 'vertex_valence': 3}, 'stellar': {'count_pass_is_realization': False, 'full_decoration_average': '62/7', 'full_decoration_insertions_per_cell': 6, 'new_cells': 1, 'new_total_face_count': 8, 'single_insertion_first_count_pass': 9, 'starting_faces_per_cell': 14}, 'target_id': 5900021, 'transport': {'Q_coefficient': 1, 'V_delta_coefficient': -1, 'edge_conormal_sum_norm_squared': 1, 'global_cellwise_sign_status': 'No global sign theorem is decided.', 'local_equations_force_nonpositive_cell_transport': False, 'pi_coefficient': 4}}
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
 seen=set();dirs=set()
 def walk(base):
  for e in os.scandir(base):
   n=str(Path(e.path).relative_to(root));kind=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(kind):
    need(n in DIRS,'unexpected directory');dirs.add(n);walk(Path(e.path))
   else:need(stat.S_ISREG(kind),'linked or special member');seen.add(n)
 walk(root);need(seen==FILES and dirs==DIRS,'exact recursive inventory')
def validate_manifest(m,snapshot):
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==5900021,'manifest problem')
 need(type(m['files']) is list and len(m['files'])==len(PAYLOAD),'manifest inventory length');seen=set()
 for row in m['files']:
  keys(row,['path','bytes','sha256']);n=row['path'];need(type(n) is str and n in PAYLOAD and n not in seen,'manifest path');seen.add(n)
  integer(row['bytes']);digest(row['sha256']);need(same(row,dict(path=n,bytes=len(snapshot[n]),sha256=sha(snapshot[n]))),'manifest member binding')
 need(seen==PAYLOAD,'complete manifest')
def validate_acceptance(a):compare_typed(a,EXPECTED_ACCEPTANCE)
def validate_status(a):compare_typed(a,EXPECTED_STATUS)
def refname(script,kind):return script[:-3].replace('/','_')+'.mode'+str(sys.flags.optimize)+'.reference.'+kind
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
 validate_acceptance(parsed['ACCEPTANCE.json']);validate_status(parsed['STATUS.json']);compare_typed(parsed['current/CLAIMS.json'],EXPECTED_CLAIMS)
 for n in FILES:
  if n.endswith('.py'):need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(snap[n]))),'assertion-free delivery code')
 for n in SCRIPTS:compare_output(n,0,snap[refname(n,'stdout')],snap[refname(n,'stderr')],snap[refname(n,'stdout')],snap[refname(n,'stderr')])
 return snap
def readonly(root):
 rows=[]
 for p,label,d in [(root,'.',True)]+[(root/n,n,True) for n in sorted(DIRS)]+[(root/n,n,False) for n in sorted(FILES)]:
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
  r=subprocess.run([sys.executable,'-I','-S','-B',*mode,script,*(['--require-readonly'] if script=='audit/check_independent.py' else [])],cwd=root,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=200)
  records.append(compare_output(script,r.returncode,r.stdout,r.stderr,initial[refname(script,'stdout')],initial[refname(script,'stderr')]))
 final=integrity(root,mp,bp);need(final==initial,'whole delivery changed')
 print(json.dumps(dict(schema=1,problem_id=5900021,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,whole_delivery_unchanged=True,before={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(initial.items())},after={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(final.items())},source_body_replay='NOT_RUN',original_report_replay='NOT_RUN',historical_audit_harness_replay='NOT_RUN',historical_patch_application='NOT_RUN',new_source_search='NOT_RUN',dataset_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',mathematics_scope='Scoped simple-cell curvature analysis; full global foam questions unresolved after 5/5 approaches. Geometry/algebra mutations and scope guards are distinct.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
