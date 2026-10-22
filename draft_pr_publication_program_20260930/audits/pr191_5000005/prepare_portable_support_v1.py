"""Build an explicit own-authored verification payload; never redistribute primary bodies."""
from pathlib import Path
import ast,datetime,hashlib,json
A=Path(__file__).resolve().parent;D=A/'verification_support_v1'
if D.exists():raise RuntimeError('Refuse overwriting existing support generation')
D.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
def copy(src,rel):
 if not src.is_file() or src.is_symlink():raise RuntimeError('Nonregular input '+str(src))
 f=D/rel;f.parent.mkdir(parents=True,exist_ok=True)
 with f.open('xb') as w:w.write(src.read_bytes())
for x in json.loads((A/'ORIGINAL_FILE_MANIFEST.json').read_text())['files']:
 rel='original_submission/files/'+x['path'];src=A/rel
 if sha(src.read_bytes())!=x['sha256']:raise RuntimeError('Original source drift')
 copy(src,rel)
families=[('literal_type_source_adversary','PUBLIC_ALLOWLIST.json','files'),('exact_reproduction_adversary','PUBLICATION_ALLOWLIST.json','files'),('global_affine_geometry_adversary','PUBLIC_SAFE_ALLOWLIST.json','public_safe_authored_files'),('classical_priority_audit','PUBLIC_ALLOWLIST.json','files'),('contemporary_priority_audit','PUBLIC_ALLOWLIST.json','allowlist')]
for family,allow,key in families:
 for x in json.loads((A/family/allow).read_text())[key]:
  name=x if isinstance(x,str) else x.get('file',x.get('path'))
  if Path(name).is_absolute() or '..' in Path(name).parts or any(z in Path(name).parts for z in ['private','private_source','private_inputs','outputs','results']):raise RuntimeError('Private path selected')
  src=A/family/name
  if isinstance(x,dict) and sha(src.read_bytes())!=x['sha256']:raise RuntimeError('Allowed body drift')
  copy(src,'reviews/'+family+'/'+name)
for name in ['CURRENT_PROOF_V3.md','ROOT_MATHEMATICAL_GATE.json','ROOT_PRIORITY_GATE_01.json','ROOT_EXACT_UPSTREAM_TARGET_01.json','ORIGINAL_FILE_MANIFEST.json','ROOT_TWO_MATH_FAMILY_AUTHENTICATION_01.json','ROOT_GEOMETRY_FAMILY_AUTHENTICATION_01.json','ROOT_PRIORITY_FAMILY_AUTHENTICATION_01.json','ROOT_PRIMARY_SOURCE_CUSTODY_01.json','ROOT_PRIMARY_SOURCE_CUSTODY_02.json','ROOT_COMPLETE_PAGE_SOURCE_INSPECTION_01.json','ROOT_PRIMARY_SCOPE_ASSESSMENT_01.md','ROOT_PRIMARY_SCOPE_SEAL_01.json','ROOT_PRIMARY_SCOPE_ASSESSMENT_02.md','ROOT_ANALYTIC_REPRODUCTION_01.md','ROOT_ANALYTIC_CHECKPOINT_SEAL_01.json']:
 copy(A/name,'audit/'+name)
copy(A/'CURRENT_PROOF_V2.md','history/CURRENT_PROOF_V2.md')
copy(A/'ROOT_MATHEMATICAL_REPAIR_01.json','history/ROOT_MATHEMATICAL_REPAIR_01.json')
for name in ['reflection_geometry.py','pentagon_geometry.py','octagon_geometry.py']:copy(A/'exact_reproduction_adversary/checks'/name,'checks/'+name)
copy(A/'global_affine_geometry_adversary/geometry_checker.py','checks/geometry_checker.py')
original=A/'literal_type_source_adversary/independent_exact_checks.py';raw=original.read_bytes();tree=ast.parse(raw);count=sum(isinstance(x,ast.Assert) for x in ast.walk(tree))
if not count:raise RuntimeError('Expected historical supplementary assertions not found')
class Harden(ast.NodeTransformer):
 def visit_Assert(self,node):
  args=[] if node.msg is None else [node.msg]
  return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=args,keywords=[]),cause=None)],orelse=[]),node)
fixed=ast.fix_missing_locations(Harden().visit(tree))
if any(isinstance(x,ast.Assert) for x in ast.walk(fixed)):raise RuntimeError('Unsafe assertion survived transformation')
text='# Explicit if/raise hardening of the preserved independent supplementary checker.\n# Original source and ordinary baseline remain under reviews/literal_type_source_adversary/.\n'+ast.unparse(fixed)+'\n'
(D/'checks/literal_type_hardened.py').write_text(text)
copy(A/'literal_type_source_adversary/EXACT_CHECKS_OUTPUT.json','reference_results/literal_original_ordinary.json')
copy(A/'portable_verify_all_v1.py','verify_all.py')
hard={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'SUPPLEMENTARY_LITERAL_CHECKER_HARDENED_EXPLICIT_IF_RAISE','preserved_original_source_SHA256':sha(raw),'hardened_source_SHA256':sha(text.encode()),'converted_assertions':count,'method':'AST Assert(test,msg) becomes if not test: raise AssertionError(msg), preserving lazy message evaluation. No mathematical test removed.','original_authored_checker_and_family_ordinary_report_preserved_unchanged':True,'historical_literal_checker_optimized_execution_claimed':False,'portable_ordinary_optimized_semantic_equality_and_injected_false_guards_required':True}
(D/'ASSERTION_HARDENING.json').write_text(json.dumps(hard,indent=2)+'\n')
readme='''# Parallel short trajectories: verification and provenance

This is a credited mathematical verification/exposition package for the accompanying research note. The unrestricted imported bare-A0/global-rule conjunction is false. The explicit segment-parity-selected law is proved for all n>=3, actual admissible angles, evenell for evenn, including first-vertex existence. The source preceding open fundamental sectors and the global import are distinguished. This package does not certify novelty, historical firstness, either author's awareness, or independent simultaneous discovery.

Ferudun, version1.0 of9October2026, DOI10.5281/zenodo.23267641, Definition1.1/Remark1.2/TheoremB already supplies the nontrivial theorem, parity/diagonal qualification and existence. Its double-surface angular/reflection and cylinder/descent mechanisms substantially overlap ours. Veech and the other classical inputs are credited in the note and source ledger. The triangle and the full-affine common-shift formulation are not advertised as new.

Run from a clean extracted directory using Python3.10 or later, standard library only:

    python3 -E -S -B -P verify_all.py

The runner hashes every payload, checks the exact manifest inventory, copies executable inputs into temporary folders, and runs ordinary and optimized execution. It reproduces3,276,822 original author controls and441,920 old independent controls, reruns independent exact first-hit geometry for n=3,4,5,6,8 (1,280 transformed pairs;1,628 terminated trace invocations with repetitions), runs the supplementary exact source/model controls and geometry sanity checks, and injects12 deliberately false guard conditions. An expected nonzero exit is required in every negative test, in both modes. It writes no verification output into the extracted payload. Geometry-checker floating-point comparisons are sanity checks with explicit tolerances, not interval proofs.

The literal/type family's historical supplemental checker uses ordinary Python assertions; its original source and ordinary record are preserved. checks/literal_type_hardened.py replaces every such assertion by explicit if/raise, and its scientific JSON must equal the authenticated ordinary baseline. ASSERTION_HARDENING.json records both source hashes and the count. The original author and old independent programs already used explicit guards. Historical originals are copied before running their adjacent output writes. Finite controls supplement, rather than prove, the universal analytic theorem.

CURRENT_PROOF_V3 and the two mathematical/priority gates are dated audit-assembly records. Earlier candidate/review opinions, the protected original16-file snapshot and the preterminal v2 assembly are retained as history; they do not override the current precise proof, convention repairs and credited priority conclusion. The source and priority ledgers specify actual body hashes, versions and pages read, with explicit unread/version-history gaps. They are not claims to have read every cited page or every earlier work. No original external paper bodies, page images, OCR/extracted text, downloaded external source archives or credentials are included.

Five independent source-first families supplied the mathematical/reproduction and priority audits. Their early-seal timing-label corrections and limitations are retained. These are AI audit evidence, not human refereeing. Extensive AI assistance was used for derivation, reconstruction, literature search, drafting and checking; no conventional human peer review is claimed. Compilation and complete-package review/publication acceptance records in the repository supersede dated assembly-time pending flags only after those steps actually succeed. File protection modes in historical receipts describe the recorded local audit state; distribution integrity is checked by hashes.
'''
(D/'README.md').write_text(readme)
rows=[]
for p in sorted(D.rglob('*')):
 if p.is_file():
  b=p.read_bytes();rows.append({'path':str(p.relative_to(D)),'bytes':len(b),'sha256':sha(b)})
(D/'MANIFEST.json').write_text(json.dumps({'status':'PORTABLE_SCIENTIFIC_INPUT_MANIFEST_ASSEMBLY_STAGE','files':rows,'scope':'Payload hashes only; final paper/metadata and package assembly will add their own explicitly declared copies before freeze.'},indent=2)+'\n')
receipt={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'support_folder':D.name,'payload_files_excluding_manifest':len(rows),'literal_checker_hardening':hard,'all_primary_bodies_excluded':True,'publication_ready':False}
(A/'ROOT_PORTABLE_SUPPORT_ASSEMBLY_01.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
