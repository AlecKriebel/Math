#!/usr/bin/env python3
"""Validate the public-only arithmetic K(pi,1) credited prior-resolution audit delivery. Use the fixed external bootstrap."""
import ast,hashlib,json,math,os,re,stat,subprocess,sys
from pathlib import Path
FILES = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'BOOTSTRAP.py', 'CHECK_RUNS.json', 'MUTATION_TESTS.py', 'PUBLICATION_MANIFEST.json', 'PUBLICATION_SCOPE.json', 'README.md', 'STATUS.json', 'document_checks.mode0.reference.stderr', 'document_checks.mode0.reference.stdout', 'document_checks.mode1.reference.stderr', 'document_checks.mode1.reference.stdout', 'document_checks.mode2.reference.stderr', 'document_checks.mode2.reference.stdout', 'document_checks.py', 'first_audit/AUTHORED_PACKET_MANIFEST.json', 'first_audit/NESTED_DEPENDENCY_LEDGER.md', 'first_audit/PRIOR_RESOLUTION_AUDIT.md', 'first_audit/SOURCE_VERIFICATION_METADATA.json', 'second_audit/INDEPENDENT_ACCEPTANCE_REPORT.md', 'second_audit/INDEPENDENT_PACKET_MANIFEST.json', 'second_audit/INDEPENDENT_VERIFICATION_METADATA.json', 'second_audit/LOCAL_CONDITION_CLARIFICATION.md', 'verify_publication.py'])
PAYLOAD = FILES - {'BOOTSTRAP.py','PUBLICATION_MANIFEST.json'}
EXPECTED_ACCEPTANCE = {'accepted_input_bytes_preserved': True, 'catalogue_disposition': 'SOURCE_SCOPE', 'credit': ['Alexander Schmidt', 'John Labute', 'Jan Minac'], 'decision': 'ACCEPTED_CREDITED_PRIOR_RESOLUTION_WITH_SOURCE_SCOPE', 'essential_authored_corrections_included': True, 'excluded_stages': {'computational_mathematical_proof_certification': 'NOT_RUN', 'cryptographic_pdf_signature_verification': 'NOT_RUN', 'dataset_replay': 'NOT_RUN', 'excluded_material_replay': 'NOT_RUN', 'formal_proof_assistant_verification': 'NOT_RUN', 'full_foundational_proof_replay': 'NOT_RUN', 'historical_inspection_replay': 'NOT_RUN', 'historical_retrieval_replay': 'NOT_RUN', 'new_source_search': 'NOT_RUN', 'publisher_pdf_comparison': 'NOT_RUN', 'source_body_replay': 'NOT_RUN'}, 'mathematical_proof_computationally_certified': False, 'mathematical_scope': {'catalogue': 'SOURCE_SCOPE: literal catalogue omits the original real-place convention; no unrestricted real-field p=2 theorem or residual-open classification.', 'characteristic_two': 'Both off-diagonal cup directions checked through Lemma 5.2; square vanishing uses splitting in k(i) and N(q_a)=1 mod 4; graded commutativity alone is insufficient.', 'duality': 'First local products of (I) and (II) are T-indexed; designated S factors remain S.', 'exact_target': 'OWR-1586-003: number field k, prime p odd OR k totally imaginary; every finite tame S and prescribed Dirichlet-density-one D admit finite A subset D minus (S union S_p) with Spec(O_k) minus (S union A) K(pi,1) for p.', 'foundations': 'Checked imported interfaces; arithmetic duality, class field theory, PBW, etale homotopy and other listed foundations are not independently reproved.', 'local_kummer': 'At p-adic J factors use C_v=O_v^* k_v^{*p}/k_v^{*p}, not ordinary unramified H^1(k_v,mu_p); its annihilator is unramified F_p characters.', 'odd_branch': 'psi_a evaluates at Frob(q_a), not p_a; old H^1 dimension at least two and degree-one prime descent explicit.', 'pdf_headers': 'Historical pdf_signature_valid denotes PDF-header detection only; no cryptographic digital-signature verification. Hash agreement does not establish historical network provenance.', 'restrictions': 'No class-number or cyclotomic exclusion; S may be empty and need not lie in D; no uniform bound on A.', 'roots_branch': 'Restore I_a in cyclic field F_a, Frobenius kernel, and chi_a space; n>=3 and kernel dimension p^n-2-n>0; psi_a chosen in old U.', 'source_versions': 'Inspected English/German author manuscripts and Labute-Minac author/arXiv versions are distinguished; no publisher-PDF identity claimed.'}, 'new_proof_search_turns': 0, 'novelty_claimed': False, 'original_owr_target_resolved': True, 'problem_id': 30000779, 'schema': 1, 'source_problem': 'OWR-1586-003', 'unrestricted_real_field_p2_disposition': 'NOT_ASSERTED'}
EXPECTED_STATUS = {'literal_catalogue_scope_repair_required': True, 'manuscript_status': 'Authored application/correction audits of credited published prior mathematics; not an author-issued or publisher-issued erratum. Imported-foundation boundary retained.', 'new_proof_search_turns': 0, 'novelty_claimed': False, 'original_owr_target_resolved': True, 'problem_id': 30000779, 'schema': 1, 'status': 'credited_prior_resolution_SOURCE_SCOPE', 'unrestricted_real_field_p2_open_asserted': False, 'unrestricted_real_field_p2_result_asserted': False}
EXPECTED_REFERENCE = {'document_checks.py': {'0': {'stdout': {'bytes': 2189, 'sha256': '57de11a109119aed53f696a763079d8e6e7e902e97b7dd0f3d96925981a6162f'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '1': {'stdout': {'bytes': 2189, 'sha256': 'a29ed9d64912f062f7303d04a76dae164a7c268e30084b28144949c84f33e65a'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}, '2': {'stdout': {'bytes': 2189, 'sha256': 'e625e4cf59c32b8ef7d36dbbacc0311dcd53a40c2ae5e2316d3cbe3119a0c355'}, 'stderr': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}}}}
SCRIPTS = ('document_checks.py',)
DIRS = {'first_audit','second_audit'}

EXPECTED_OUTPUT = {'document_checks.py': {'0': {'document_byte_check_count': 8, 'document_byte_checks': [{'bytes': 1101, 'document': 'first_audit/AUTHORED_PACKET_MANIFEST.json', 'preserved': True, 'sha256': '50f1655a716d9e58d005a3713fde29eba0da993e17abba43e038ee651a6fc5ec'}, {'bytes': 24620, 'document': 'first_audit/NESTED_DEPENDENCY_LEDGER.md', 'preserved': True, 'sha256': '07178f08bda91f33ffbf335da7af8d2244f5439f98f22f61e552aa6aafde1bf9'}, {'bytes': 34057, 'document': 'first_audit/PRIOR_RESOLUTION_AUDIT.md', 'preserved': True, 'sha256': '7a7cd9dc4c547e20739d5f96d35150f63f03b5fbc0fd1247e6056bce9b256ee4'}, {'bytes': 12008, 'document': 'first_audit/SOURCE_VERIFICATION_METADATA.json', 'preserved': True, 'sha256': '69df13349746856d34d4eb57970e5f618eb01c8f2d2e3d1346e21f7619389e6d'}, {'bytes': 28468, 'document': 'second_audit/INDEPENDENT_ACCEPTANCE_REPORT.md', 'preserved': True, 'sha256': 'dbd08a7f4b7f973f0a28c774b1030c0a87b20f4a3815221fd7bae04b0345acf5'}, {'bytes': 1071, 'document': 'second_audit/INDEPENDENT_PACKET_MANIFEST.json', 'preserved': True, 'sha256': '66934f764a75ab0730d4b2a0783153d54f2a9035284029e7157262bf807402f7'}, {'bytes': 12066, 'document': 'second_audit/INDEPENDENT_VERIFICATION_METADATA.json', 'preserved': True, 'sha256': '08e2b53460e7f862f39efd99eb0a6abbea162f386f03c2d7ba892a6f86f287a8'}, {'bytes': 3888, 'document': 'second_audit/LOCAL_CONDITION_CLARIFICATION.md', 'preserved': True, 'sha256': '438ca99e22f3975958eeb491b63a4f9610c35fb0b5aa46e61f97f4616d46d833'}], 'euid': 1000, 'mathematical_proof_checks': 'NOT_RUN', 'problem_id': 30000779, 'python_optimize': 0, 'schema': 1, 'scope_declaration_control_count': 2, 'scope_declaration_controls': [{'identity': 'exact acceptance declaration', 'passed': True}, {'identity': 'exact status declaration', 'passed': True}], 'source_theorem_computationally_certified': False, 'status': 'passed', 'uid': 1000}, '1': {'document_byte_check_count': 8, 'document_byte_checks': [{'bytes': 1101, 'document': 'first_audit/AUTHORED_PACKET_MANIFEST.json', 'preserved': True, 'sha256': '50f1655a716d9e58d005a3713fde29eba0da993e17abba43e038ee651a6fc5ec'}, {'bytes': 24620, 'document': 'first_audit/NESTED_DEPENDENCY_LEDGER.md', 'preserved': True, 'sha256': '07178f08bda91f33ffbf335da7af8d2244f5439f98f22f61e552aa6aafde1bf9'}, {'bytes': 34057, 'document': 'first_audit/PRIOR_RESOLUTION_AUDIT.md', 'preserved': True, 'sha256': '7a7cd9dc4c547e20739d5f96d35150f63f03b5fbc0fd1247e6056bce9b256ee4'}, {'bytes': 12008, 'document': 'first_audit/SOURCE_VERIFICATION_METADATA.json', 'preserved': True, 'sha256': '69df13349746856d34d4eb57970e5f618eb01c8f2d2e3d1346e21f7619389e6d'}, {'bytes': 28468, 'document': 'second_audit/INDEPENDENT_ACCEPTANCE_REPORT.md', 'preserved': True, 'sha256': 'dbd08a7f4b7f973f0a28c774b1030c0a87b20f4a3815221fd7bae04b0345acf5'}, {'bytes': 1071, 'document': 'second_audit/INDEPENDENT_PACKET_MANIFEST.json', 'preserved': True, 'sha256': '66934f764a75ab0730d4b2a0783153d54f2a9035284029e7157262bf807402f7'}, {'bytes': 12066, 'document': 'second_audit/INDEPENDENT_VERIFICATION_METADATA.json', 'preserved': True, 'sha256': '08e2b53460e7f862f39efd99eb0a6abbea162f386f03c2d7ba892a6f86f287a8'}, {'bytes': 3888, 'document': 'second_audit/LOCAL_CONDITION_CLARIFICATION.md', 'preserved': True, 'sha256': '438ca99e22f3975958eeb491b63a4f9610c35fb0b5aa46e61f97f4616d46d833'}], 'euid': 1000, 'mathematical_proof_checks': 'NOT_RUN', 'problem_id': 30000779, 'python_optimize': 1, 'schema': 1, 'scope_declaration_control_count': 2, 'scope_declaration_controls': [{'identity': 'exact acceptance declaration', 'passed': True}, {'identity': 'exact status declaration', 'passed': True}], 'source_theorem_computationally_certified': False, 'status': 'passed', 'uid': 1000}, '2': {'document_byte_check_count': 8, 'document_byte_checks': [{'bytes': 1101, 'document': 'first_audit/AUTHORED_PACKET_MANIFEST.json', 'preserved': True, 'sha256': '50f1655a716d9e58d005a3713fde29eba0da993e17abba43e038ee651a6fc5ec'}, {'bytes': 24620, 'document': 'first_audit/NESTED_DEPENDENCY_LEDGER.md', 'preserved': True, 'sha256': '07178f08bda91f33ffbf335da7af8d2244f5439f98f22f61e552aa6aafde1bf9'}, {'bytes': 34057, 'document': 'first_audit/PRIOR_RESOLUTION_AUDIT.md', 'preserved': True, 'sha256': '7a7cd9dc4c547e20739d5f96d35150f63f03b5fbc0fd1247e6056bce9b256ee4'}, {'bytes': 12008, 'document': 'first_audit/SOURCE_VERIFICATION_METADATA.json', 'preserved': True, 'sha256': '69df13349746856d34d4eb57970e5f618eb01c8f2d2e3d1346e21f7619389e6d'}, {'bytes': 28468, 'document': 'second_audit/INDEPENDENT_ACCEPTANCE_REPORT.md', 'preserved': True, 'sha256': 'dbd08a7f4b7f973f0a28c774b1030c0a87b20f4a3815221fd7bae04b0345acf5'}, {'bytes': 1071, 'document': 'second_audit/INDEPENDENT_PACKET_MANIFEST.json', 'preserved': True, 'sha256': '66934f764a75ab0730d4b2a0783153d54f2a9035284029e7157262bf807402f7'}, {'bytes': 12066, 'document': 'second_audit/INDEPENDENT_VERIFICATION_METADATA.json', 'preserved': True, 'sha256': '08e2b53460e7f862f39efd99eb0a6abbea162f386f03c2d7ba892a6f86f287a8'}, {'bytes': 3888, 'document': 'second_audit/LOCAL_CONDITION_CLARIFICATION.md', 'preserved': True, 'sha256': '438ca99e22f3975958eeb491b63a4f9610c35fb0b5aa46e61f97f4616d46d833'}], 'euid': 1000, 'mathematical_proof_checks': 'NOT_RUN', 'problem_id': 30000779, 'python_optimize': 2, 'schema': 1, 'scope_declaration_control_count': 2, 'scope_declaration_controls': [{'identity': 'exact acceptance declaration', 'passed': True}, {'identity': 'exact status declaration', 'passed': True}], 'source_theorem_computationally_certified': False, 'status': 'passed', 'uid': 1000}}}
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
def parse(raw):
 try:return json.loads(raw,object_pairs_hook=unique,parse_constant=nonfinite,parse_float=number)
 except json.JSONDecodeError:raise ValueError('malformed or trailing JSON')
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
 keys(m,['schema','problem_id','files']);need(type(m['schema']) is int and m['schema']==1,'manifest schema');need(type(m['problem_id']) is int and m['problem_id']==30000779,'manifest problem')
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
 compare_typed(parse(refout),EXPECTED_OUTPUT[script][str(sys.flags.optimize)])
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
 for p,label,d in [(root,'.',True)]+[(root/n,n,True) for n in sorted(DIRS)]+[(root/n,n,False) for n in sorted(FILES)]:
  need((p.stat().st_mode&0o777)==(0o555 if d else 0o444) and not os.access(p,os.W_OK),'read-only permissions')
  try:fd=os.open(p/'FORBIDDEN_CREATE' if d else p,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if d else os.O_APPEND),0o600)
  except PermissionError as e:need(e.errno==13,'physical denial errno');rows.append(dict(path=label,operation='create' if d else 'append_open',errno=13,denied=True))
  else:os.close(fd);raise ValueError('physical write unexpectedly allowed')
 try:os.unlink(root/'ACCEPTANCE.md')
 except PermissionError as e:need(e.errno==13,'physical unlink denial');rows.append(dict(path='ACCEPTANCE.md',operation='unlink',errno=13,denied=True))
 else:raise ValueError('physical unlink unexpectedly allowed')
 return rows
def main():
 need(len(sys.argv)==4,'manifest pin, bootstrap pin, packet required');mp,bp,rs=sys.argv[1:];root=Path(os.path.abspath(rs))
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'isolated no-site no-bytecode')
 initial=integrity(root,mp,bp);probes=readonly(root);mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];records=[]
 for script in SCRIPTS:
  r=subprocess.run([sys.executable,'-I','-S','-B',*mode,script],cwd=root,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=600)
  records.append(compare_output(script,r.returncode,r.stdout,r.stderr,initial[refname(script,'stdout')],initial[refname(script,'stderr')]))
 final=integrity(root,mp,bp);need(final==initial,'whole delivery changed')
 print(json.dumps(dict(schema=1,problem_id=30000779,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,manifest_sha256=mp,bootstrap_sha256=bp,physical_denials=probes,replays=records,whole_delivery_unchanged=True,before={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(initial.items())},after={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(final.items())},source_body_replay='NOT_RUN',historical_retrieval_replay='NOT_RUN',historical_inspection_replay='NOT_RUN',excluded_material_replay='NOT_RUN',new_source_search='NOT_RUN',dataset_replay='NOT_RUN',full_foundational_proof_replay='NOT_RUN',formal_proof_assistant_verification='NOT_RUN',computational_mathematical_proof_certification='NOT_RUN',publisher_pdf_comparison='NOT_RUN',cryptographic_pdf_signature_verification='NOT_RUN',mathematics_scope='Document preservation and declared source scope only; no mathematical proof certification. Exact OWR prior resolution credited; catalogue SOURCE_SCOPE qualification retained.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):print('REJECT: strict publication validation failed',file=sys.stderr);sys.exit(1)
