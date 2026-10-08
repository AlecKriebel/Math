#!/usr/bin/env python3
"""Validate the public-only grassmannian proof delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'ATTRIBUTION_FIX.patch', 'BOOTSTRAP.py', 'CHECK_RUNS.json', 'CORRECTION.md', 'INDEPENDENT_AUDIT.md', 'MUTATION_TESTS.py', 'PATCH_HISTORY.json', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PUBLICATION_MANIFEST.json', 'README.md', 'REPORT.md', 'SOURCE_AUDIT.json', 'SOURCE_METADATA.json', 'STATUS.json', 'check_math.py', 'independent_checks.py', 'run_independent.mode0.reference.stderr', 'run_independent.mode0.reference.stdout', 'run_independent.mode1.reference.stderr', 'run_independent.mode1.reference.stdout', 'run_independent.mode2.reference.stderr', 'run_independent.mode2.reference.stdout', 'run_independent.py', 'run_math.mode0.reference.stderr', 'run_math.mode0.reference.stdout', 'run_math.mode1.reference.stderr', 'run_math.mode1.reference.stdout', 'run_math.mode2.reference.stderr', 'run_math.mode2.reference.stdout', 'run_math.py', 'semantic_mutants.mode0.reference.stderr', 'semantic_mutants.mode0.reference.stdout', 'semantic_mutants.mode1.reference.stderr', 'semantic_mutants.mode1.reference.stdout', 'semantic_mutants.mode2.reference.stderr', 'semantic_mutants.mode2.reference.stdout', 'semantic_mutants.py', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'actual_Escobar_Harada_counterexample': False, 'arbitrary_prime_cone_classification': False, 'coherence_not_sufficient_for_SAGBI': 'Known hexagonal boundary: degree-two dimensions 174 versus 175', 'corrected_report_sha256': 'd6be3600406a3c8b111c16815601a7a477d73b2265b6d62c6dbba4e44d5b73b3', 'dataset_replay': 'NOT_RUN', 'decision': 'ACCEPTED_FIVE_SCOPED_PARTIAL_RESULTS', 'finite_check_scope': 'Exact regression and falsification evidence supporting the authored proofs; no formal proof-assistant or independent verification of all cited geometry', 'formal_proof_assistant_verification': 'NOT_RUN', 'global_mutation_comparison_solved': False, 'global_target': 'UNFINISHED', 'historical_patch_application': 'NOT_RUN', 'hn_formula_defect_version': 'arXiv:2107.04264v2 only', 'hn_published_formula_defect_claimed': False, 'label_preserving_additive_transport': 'Impossible for the prescribed B0 to B1 generator images', 'labeled_cone_nonadjacency': 'Accepted for B0 and B1 in the common fixed Plucker labeling', 'local_min_max_identities': 'Accepted on the entire real ambient vector space with integral piecewise-linear bijectivity', 'novelty_certified': False, 'original_report_replay': 'NOT_RUN', 'positive_block_SAGBI_source': 'Imported cited theorem, not established by finite Hilbert agreement', 'problem_id': 30005082, 'schema': 1, 'source_body_replay': 'NOT_RUN', 'source_hash_recheck': 'NOT_RUN', 'substantive_proof_approaches': 5, 'turns': '5/5', 'unadjusted_max_nonconvexity': 'Accepted for the specified Gr(3,6) rectangle coordinates'}
EXPECTED_STATUS = {'accepted_scope': 'Five partial boundary results after independent mathematical and source-scope audit', 'global_target': 'UNFINISHED', 'novelty_certified': False, 'problem_id': 30005082, 'queue_modified': False, 'schema': 1, 'status': 'exhausted', 'substantive_proof_approaches': 5, 'turns': '5/5', 'unqualified_original_solved': False}
EXPECTED_REFERENCE = {'run_math.py': {'0': {'stdout': {'bytes': 2033, 'sha256': '58b3fafe0f8ea79f6b3b5cd0b51ca8d5c4561c5bafab9f1d5121404aec145c61'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 2033, 'sha256': '5bc6d5d57887440272a04e6baa67a4218c13f00c1f26e7fdc92c2cfe29fb079b'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 2033, 'sha256': '67a35a8f1f95458024df13374bdf706127543ec6be88cb9a7a9a4110bdc84053'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'run_independent.py': {'0': {'stdout': {'bytes': 1708, 'sha256': 'ce3158db0dcdbbf01f0fd4bf9402a83e0a14cb604615e4664b6232004d8a17b4'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 1708, 'sha256': '51193b619091ec7479b6927a808cc1cdb0f388cd7b29452abe26db81864b2a22'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 1708, 'sha256': '5e1e7c83488028cfc7fda4e60677a6a0610828fd0c9b86ec270b1de4ce101d4a'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'semantic_mutants.py': {'0': {'stdout': {'bytes': 8606, 'sha256': '1ca953aa50e15b1aebf638b0297df2f579fa19c4b31c13429282f23ef6a1da91'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 8746, 'sha256': '37b6f9ac04c4f600d320ffdd5ba37decfc11334cbfd9fd4e8bc7fae1a2621256'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 8756, 'sha256': '862d155cb1f8dd13822019d4a503cb4ac9d0863ef5eed854ba0eb52e0a7b33c6'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
SCRIPTS = ('run_math.py','run_independent.py','semantic_mutants.py')
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
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==30005082,'manifest problem')
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
 print(json.dumps(dict(schema=1,problem_id=30005082,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,whole_delivery_unchanged=True,source_body_replay='NOT_RUN',source_hash_recheck='NOT_RUN',original_report_replay='NOT_RUN',historical_patch_application='NOT_RUN',dataset_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',mathematics_scope='Five accepted partial boundaries; global higher-Grassmannian comparison unfinished, exhausted 5/5. Finite checks are regression evidence only.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
