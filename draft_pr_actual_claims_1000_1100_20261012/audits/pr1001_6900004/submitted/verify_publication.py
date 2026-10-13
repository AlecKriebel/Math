#!/usr/bin/env python3
"""Validate the public-only tensegrity proof delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'ATTRIBUTION_CORRECTION.patch', 'AUDIT.md', 'BOOTSTRAP.py', 'CHECK_RUNS.json', 'MUTATION_TESTS.py', 'PATCH_HISTORY.json', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PUBLICATION_MANIFEST.json', 'README.md', 'REPORT.md', 'SOURCE_AUDIT.json', 'SOURCE_MANIFEST.json', 'STATUS.json', 'check_collision_witness.mode0.reference.stderr', 'check_collision_witness.mode0.reference.stdout', 'check_collision_witness.mode1.reference.stderr', 'check_collision_witness.mode1.reference.stdout', 'check_collision_witness.mode2.reference.stderr', 'check_collision_witness.mode2.reference.stdout', 'check_collision_witness.py', 'independent_kernel_check.mode0.reference.stderr', 'independent_kernel_check.mode0.reference.stdout', 'independent_kernel_check.mode1.reference.stderr', 'independent_kernel_check.mode1.reference.stdout', 'independent_kernel_check.mode2.reference.stderr', 'independent_kernel_check.mode2.reference.stdout', 'independent_kernel_check.py', 'semantic_mutants.mode0.reference.stderr', 'semantic_mutants.mode0.reference.stdout', 'semantic_mutants.mode1.reference.stderr', 'semantic_mutants.mode1.reference.stdout', 'semantic_mutants.mode2.reference.stderr', 'semantic_mutants.mode2.reference.stdout', 'semantic_mutants.py', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'abstract_adjacency_classification': False, 'ambient_homeomorphism_classification': False, 'collision_criterion_attribution': 'Panina, Section 3, Lemma 4, arXiv:1902.07212v4, p.8', 'collisions_retained': True, 'conclusion': 'Identical partitions if and only if identical edge sets', 'connected_components_required': True, 'coordinate_zero_sign_preserved': True, 'd_minimum': 1, 'dataset_replay': 'NOT_RUN', 'decision': 'ACCEPTED_LITERAL_PARTITION_THEOREM_WITH_ORIGINAL_INTERPRETATION_HOLD', 'finite_regression_scope': 'Exact formula and kernel regression evidence; not a replacement for the universal proof or an author-intent determination.', 'formal_proof_assistant_verification': 'NOT_RUN', 'full_configuration_space': True, 'generic_only_classification': False, 'historical_patch_application': 'NOT_RUN', 'mathematical_proof': 'ACCEPTED_AFTER_INDEPENDENT_AUDIT', 'n_minimum': 1, 'novelty_certified': False, 'original_report_replay': 'NOT_RUN', 'partition_equality': 'Literal equality of collections of subsets of the same (R^d)^n', 'problem_id': 6900004, 'schema': 1, 'simple_labeled_graphs': True, 'source_arithmetic_correction': 'K3 with exactly two coincident vertices has stress-fiber dimension 1, not 2; correction limited to Karpenkov Example 1.4 and Doray et al. Example 2.7.', 'source_body_replay': 'NOT_RUN', 'unqualified_original_problem_solved': False}
EXPECTED_STATUS = {'accepted_result': 'For every n >= 1 and d >= 1, two simple graphs on the same labeled vertex set induce identical full connected sign-equivalence partitions of (R^d)^n if and only if their edge sets are equal.', 'configuration_scope': 'Full Cartesian configuration space, including collisions and deficient affine span.', 'novelty_certified': False, 'original_problem_status': 'INTERPRETATION_HOLD', 'problem_id': 6900004, 'queue_modified': False, 'reason_for_hold': 'The source does not separately define cross-graph sameness; arbitrary ambient homeomorphisms and abstract adjacency equivalence are not classified.', 'schema': 1, 'status': 'candidate_result', 'substantive_proof_approaches': 1, 'turns': '1/5', 'unqualified_original_solved': False}
EXPECTED_REFERENCE = {'check_collision_witness.py': {'0': {'stdout': {'bytes': 4377, 'sha256': '7fc306ac2e32fe5b8c2b18cc5752e6ae7a92e3b62d3cb44a2f2120bbd95a3acd'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 4377, 'sha256': '54344f05fd36028752cd0da3452f1152732a6e9814cc12e7cbff3cb106ab72c8'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 4377, 'sha256': 'ceb47a573e34584cf5fb64c9bec95f5f05b5de44c7ecd5640695c0863e20ab6c'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'independent_kernel_check.py': {'0': {'stdout': {'bytes': 16602, 'sha256': '6a64281294b8c1686135a86617a5f962d28e8119242899ec2847e375b076c414'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 16602, 'sha256': 'fe0f8c3d016ceb841aa0e3562c28247c4b134862ac65a0706985e5599831fe23'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 16602, 'sha256': '6fdccae287bc537c00c785a29786b0500b2ab38f2955c076cd21f48e9657ce29'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'semantic_mutants.py': {'0': {'stdout': {'bytes': 5188, 'sha256': 'd32814e85a03d54e632d0fc6e8d422f70b74c3a89fabdec5f9259663614601eb'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 5272, 'sha256': '8e79d7dcb01452845dfb185550df2469241f272c3004285774a9e5bdb35a0a99'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 5278, 'sha256': 'b770fad63c636b85c47225355bff627b6bbc30239e942b8944044fe79b9ee428'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
SCRIPTS = ('check_collision_witness.py','independent_kernel_check.py','semantic_mutants.py')
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
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==6900004,'manifest problem')
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
 need(integrity(root,mp,bp)==initial,'whole delivery changed')
 print(json.dumps(dict(schema=1,problem_id=6900004,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,whole_delivery_unchanged=True,source_body_replay='NOT_RUN',original_report_replay='NOT_RUN',historical_patch_application='NOT_RUN',dataset_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',mathematics_scope='Accepted written literal-partition theorem; original interpretation hold. Finite checks are regression evidence only.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
