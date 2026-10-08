#!/usr/bin/env python3
"""Validate the public-only kk-application proof delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'APPLICATION_CLARIFICATIONS.patch', 'BOOTSTRAP.py', 'CHECK_RUNS.json', 'INDEPENDENT_AUDIT.md', 'MUTATION_TESTS.py', 'PATCH_HISTORY.json', 'PREPARATION_CONTROLS_O.json', 'PREPARATION_CONTROLS_O.stderr', 'PREPARATION_CONTROLS_OO.json', 'PREPARATION_CONTROLS_OO.stderr', 'PREPARATION_CONTROLS_normal.json', 'PREPARATION_CONTROLS_normal.stderr', 'PREPARATION_RECEIPT.json', 'PREPARATION_STAGE.json', 'PROOF_APPLICATION.md', 'PUBLICATION_MANIFEST.json', 'README.md', 'SOURCE_AUDIT.json', 'SOURCE_METADATA.json', 'STATUS.json', 'check_algebra.py', 'independent_checks.py', 'run_independent.mode0.reference.stderr', 'run_independent.mode0.reference.stdout', 'run_independent.mode1.reference.stderr', 'run_independent.mode1.reference.stdout', 'run_independent.mode2.reference.stderr', 'run_independent.mode2.reference.stdout', 'run_independent.py', 'run_math.mode0.reference.stderr', 'run_math.mode0.reference.stdout', 'run_math.mode1.reference.stderr', 'run_math.mode1.reference.stdout', 'run_math.mode2.reference.stderr', 'run_math.mode2.reference.stdout', 'run_math.py', 'semantic_mutants.mode0.reference.stderr', 'semantic_mutants.mode0.reference.stdout', 'semantic_mutants.mode1.reference.stderr', 'semantic_mutants.mode1.reference.stdout', 'semantic_mutants.mode2.reference.stderr', 'semantic_mutants.mode2.reference.stdout', 'semantic_mutants.py', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'accepted_scope': ['Ordinary absorbing maps with separable domain and stable sigma-unital ideal, with proper path starting at 1.', 'Transfer to any ambient extension via its canonical multiplier action, including nonessential extensions.', 'Unitally absorbing maps with separable unital domain and separable stable ideal, with proper path and no initial-unitary-1 claim.'], 'audit_publication_context': 'Independent mathematical scope unchanged; private packaging history omitted.', 'clarifications_applied': True, 'current_proof_sha256': '4280f45db7aed2cff62691f9a83804b77f4112f6206eddcd5922f635d63cc2a3', 'formal_proof_assistant_verification': 'NOT_RUN', 'full_literal_owr_acceptance': False, 'independent_mathematical_acceptance': True, 'mandatory_application_corrections': [], 'mathematical_credit': 'Gábor Szabó, with credited prior imports', 'new_proof_search_turns': 0, 'optional_clarifications': ['Write the two-sided strict-tail estimates explicitly.', 'State the adjoint path reversing the reconstructed conjugacy orientation.', 'Make first-block preservation and corona injectivity explicit in the unital bridge.'], 'optional_patched_proof_sha256': '4280f45db7aed2cff62691f9a83804b77f4112f6206eddcd5922f635d63cc2a3', 'original_proof_sha256': '5cc505923e1b5c969d8f2cb5124287605610af9142d56925abcb17789c3ac910', 'portable_historical_patch_application': 'NOT_RUN', 'portable_source_body_replay': 'NOT_RUN', 'primary_printed_repairs_confirmed': ['s1* s1* must be s1 s1* in Szabo v1/v2 Theorem 2.8 proof.', 'The overlap estimate uses quotient equality; a contraction lift need not be a unitary upstairs.', 'Hua stable homotopy commutes modulo the coefficient ideal before quotienting; the auxiliary representation is absorbed unitally.'], 'private_coordination_included': False, 'problem_id': 30005199, 'recommended_disposition': 'HOLD_EXACT_RELATIVE_ABSORPTION_CONVENTION_WITH_VERIFIED_STANDARD_PRIOR_RESOLUTION', 'schema': 1, 'source_bodies_included': False, 'verification_boundary': ['Mathematical audit uses identified established analytic and KK-theoretic imports, not a derivation from axioms.', 'Finite semantic tests do not certify infinite-dimensional analytic statements.', 'Live manuscript/journal status is outside this local-PDF review.', 'Other equivariant or refined-group applications in the cited papers are not separately accepted.']}
EXPECTED_STATUS = {'full_literal_owr_accepted': False, 'mathematical_credit': 'Gábor Szabó, with credited prior imports', 'new_proof_search_turns': 0, 'ordinary_path_starts_at_one': True, 'problem_id': 30005199, 'schema': 1, 'standard_application_accepted': True, 'status': 'HOLD_EXACT_RELATIVE_ABSORPTION_CONVENTION_WITH_VERIFIED_STANDARD_PRIOR_RESOLUTION', 'unital_ideal_must_be_separable': True, 'unital_path_starts_at_one_claimed': False}
EXPECTED_REFERENCE = {'run_math.py': {'0': {'stdout': {'bytes': 1148, 'sha256': '4fb19e8b71fa3b75b8f8946f37e231783307b42f3275f51f9d7e20a4bcedc5fa'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 1148, 'sha256': '3362b7626ce21689bf1c34a4936608e79da0b7c926627c6789c7c632d81d9b10'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 1148, 'sha256': 'd1bad3825c9dc18b284aa5555dcb9f486b3c6ad979d233d3046035e6a93b8d99'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'run_independent.py': {'0': {'stdout': {'bytes': 1991, 'sha256': 'aca8cd2c06f246d2e23c1279bbd74f2895c9430cefc9f15b4d6bb5d3fe4a53d4'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 1991, 'sha256': '143a8dcc7ede47025245f48809f8583213a32480c49f738fbb3b071f43455d93'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 1991, 'sha256': 'ff9051d26f70b781cade42b689c6d1289479d9b4b3414f8791a89ee6fc32def7'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}, 'semantic_mutants.py': {'0': {'stdout': {'bytes': 65911, 'sha256': 'ad2d1a9aaebbd003b487cde455f7ac76ede22ce19b505e83c7a5f410af8b3eb6'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 66079, 'sha256': 'c32cf90907b1369e73871f46ee124506ac0f9064166e0cdabd341008436ad608'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 66091, 'sha256': '40b0155747ec126006262c5f4bcb366adf68034ec96b306ed5bdf679b3a4a6c5'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
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
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==30005199,'manifest problem')
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
 after=integrity(root,mp,bp);need(after==initial,'whole delivery changed')
 print(json.dumps(dict(schema=1,problem_id=30005199,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,whole_delivery_unchanged=True,whole_delivery_hashes_before={n:dict(bytes=len(raw),sha256=sha(raw)) for n,raw in initial.items()},whole_delivery_hashes_after={n:dict(bytes=len(raw),sha256=sha(raw)) for n,raw in after.items()},source_body_replay='NOT_RUN',source_hash_recheck='NOT_RUN',original_application_replay='NOT_RUN',original_full_packet_replay='NOT_RUN',historical_patch_application='NOT_RUN',dataset_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',mathematics_scope='Credited standard stable ordinary-absorption application accepted; separate separable-ideal unital proper path without initial-1 claim; exact OWR convention hold; zero turns. Finite checks are regression evidence only.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
