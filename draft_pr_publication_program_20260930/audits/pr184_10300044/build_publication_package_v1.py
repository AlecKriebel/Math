"""Build the explicit own-authored supplemental payload; never walk private trees."""
from pathlib import Path
import hashlib,json,zipfile,datetime,shutil
A=Path(__file__).resolve().parent
P=A/'publication_package_v1'
S=P/'supplement'
S.mkdir(exist_ok=True)
def digest(b):return hashlib.sha256(b).hexdigest()
def emit(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=True)+'\n')
selected=set()
def add(folder,names):
 for n in names:selected.add(str(Path(folder)/n))
add('literal_source_adversary',json.loads((A/'literal_source_adversary/PUBLIC_SAFE_ALLOWLIST.json').read_text())['case_relative_files'] if False else [str(Path(x).relative_to('literal_source_adversary')) for x in json.loads((A/'literal_source_adversary/PUBLIC_SAFE_ALLOWLIST.json').read_text())['case_relative_files']])
add('global_taut_geometry_adversary',json.loads((A/'global_taut_geometry_adversary/FINAL_SEAL.json').read_text())['public_own_allowlist'])
add('gv_algebra_reproduction_adversary',json.loads((A/'gv_algebra_reproduction_adversary/SAFE_OWN_ALLOWLIST.json').read_text())['files'])
add('priority_target_history',[x['path'] for x in json.loads((A/'priority_target_history/PUBLIC_AUTHORED_ALLOWLIST.json').read_text())['exact_public_authored_files']])
add('priority_suspension_literature',json.loads((A/'priority_suspension_literature/AUTHORED_SAFE_ALLOWLIST.json').read_text())['files'])
add('priority_suspension_literature',['ADDENDUM_90_PERCENT_SCOPE.md','ADDENDUM_HASHSEAL.json'])
add('priority_volume_obstructions',json.loads((A/'priority_volume_obstructions/SAFE_PUBLIC_OWN_ALLOWLIST.json').read_text())['paths'])
selected.update(['ROOT_INITIAL_SOURCE_TARGET_HYPOTHESIS.md','ROOT_FIRST_CANDIDATE_ASSESSMENT.md','ROOT_FIRST_CANDIDATE_ASSESSMENT_SHA_SEAL.json','ROOT_MATHEMATICAL_AUDIT_01.md','ROOT_MATHEMATICAL_CLEARANCE_01.json','ROOT_PRIMARY_BODY_READ_LEDGER_01.json','ROOT_PRIORITY_DISPOSITION_01.md','ROOT_PRIORITY_SEARCH_PRIMARY_CHECKPOINT_01.md','ROOT_PRIORITY_FINAL_SEAL_AUTHENTICATION_01.json','ROOT_FIRST_FAMILY_SEAL_AUTHENTICATION.json','ROOT_FIRST_FAMILY_SEAL_AUTHENTICATION_02.json','ROOT_PRIORITY_INITIAL_SEAL_AUTHENTICATION_01.json','ROOT_PRIORITY_INITIAL_SEAL_AUTHENTICATION_02.json',
'root_reproduction_01/ROOT_REPLAY_AND_NEGATIVE_CONTROLS.json','root_reviewer_reproduction_01/ROOT_REVIEWER_EXECUTION.json','root_repaired_replays_01/ROOT_REPAIRED_REPLAY_ACCEPTANCE.json','root_repaired_symbolic_replays_01/ROOT_SYMBOLIC_REPAIRED_EXECUTION.json','root_repaired_symbolic_negative_01/ROOT_SYMBOLIC_NEGATIVE_ACCEPTANCE.json','root_distinct_family_replays_01/ROOT_DISTINCT_FAMILY_REPLAYS.json',
'repaired_verification/README.md','repaired_verification/verify_forms.py','repaired_verification/independent_symbolic_checks.py','repaired_verification/REPAIR_PROVENANCE.json','repaired_verification/REPAIR_ACCEPTANCE.json'])
for name in sorted(selected):
 rel=Path(name)
 if rel.is_absolute() or '..' in rel.parts or any('private' in x.lower() for x in rel.parts):raise RuntimeError(name)
 src=A/rel
 if not src.is_file() or src.is_symlink():raise RuntimeError(name)
 dst=S/'audit_history'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(src.read_bytes())
for source,name in [('repaired_verification/verify_forms.py','verify_forms.py'),('repaired_verification/independent_symbolic_checks.py','independent_symbolic_checks.py'),('gv_algebra_reproduction_adversary/independent_integrable_controls.py','independent_integrable_controls.py'),('gv_algebra_reproduction_adversary/finite_sampling_counterexample.py','finite_sampling_counterexample.py')]:
 dst=S/'controls'/name;dst.parent.mkdir(exist_ok=True);dst.write_bytes((A/source).read_bytes())
(S/'requirements-symbolic.txt').write_text('sympy==1.14.0\n')
(S/'README.md').write_text('''# Verification and audit supplement

This accompanies Alec Kriebel, *Unbounded Godbillon--Vey numbers on a fixed hyperbolic manifold*, 13 October 2026. It documents a complete mathematical negative answer to the literal Question 10.6 of Calegari, arXiv:math/0209081v1 (2002), rather than a certified historically first solution. The theorem fixes one closed hyperbolic manifold, one a>0 and one all-leaf embedded positive transversal, and gives ordinary GV=Na for every finite positive integer N. Compact leaves are allowed; no minimal-foliation result is claimed.

## Reproduce the local controls

After extracting this ZIP, use Python 3.11 or later. From this directory run:

```
python3 controls/verify_forms.py
python3 -O controls/verify_forms.py
python3 controls/independent_integrable_controls.py
python3 -O controls/independent_integrable_controls.py
python3 controls/finite_sampling_counterexample.py
python3 -O controls/finite_sampling_counterexample.py
```

These six runs need only the standard library. The polynomial checker performs 2660 checks across 120 distinct pairs, 360 pair/compression cases and 50 potentials. The independently implemented rational Taylor-jet checker performs 58 checks on actual integrable local forms, including compression. The grid counterexample shows that 343 sampled positive denominators do not prove positivity between samples. It does not falsify the paper's theorem or its specific local diagnostic. Arbitrary input pairs in the polynomial checker need not define integrable forms.

The separate symbolic implementation requires SymPy 1.14.0 (requirements-symbolic.txt). In an environment with that package run:

```
python3 controls/independent_symbolic_checks.py
python3 -O controls/independent_symbolic_checks.py
```

It performs 1640 symbolic/local controls. All guards in these current scripts use explicit errors, so optimization does not remove them. Actual baseline and negative-control receipts are in audit_history/root_repaired* and the algebra family receipts. Deliberate false guards, wrong densities and missing compression Jacobians failed as recorded in both modes. The original authors' 2660 and 1641 checkers used assertions removed by optimization; their case families also repeated. Historical output proof digests were not proof authentication. The current scripts label that digest informational and do not read or certify the paper. Audit logs retain original failures as history, not current acceptance criteria.

## What establishes the theorem

The proof uses the classical nonzero compact-support suspension input with its actual GV compatibility, a relative smooth interval trivialization, a disk-fixed representative of a pseudo-Anosov mapping class, mapping-torus hyperbolization, product-collar gluing, all-leaf transversal verification and oriented integration. The finite controls cannot realize the required global holonomy representation, certify a hyperbolic metric, or replace the universal leaf or topological arguments. The paper and mathematical audit supply those arguments using the stated classical theorems. No claim of formal proof-assistant verification is made.

## Priority and source access

The nonzero block is credited to classical Mather--Thurston/Tsuboi theory, interval-bundle replacement to the classical operation documented by Gabai, and hyperbolization to Thurston. Three separately initialized priority families and root primary-body checks found no authenticated earlier explicit full consequence in the inspected corpus. This is a bounded search, not a firstness or guaranteed novelty certificate. Final 2003 target-chapter wording was not compared. Relevant Tsuboi 1984 and 1985, Mather--Moussu--Tsuboi 1981, Gabai 1999, and Walczak 2013 full bodies remain unread in the relevant checks. Detailed source versions, read depths, failed access routes, scope differences and family coverage percentages are retained in audit_history/priority_* and ROOT_PRIORITY_DISPOSITION_01.md. Public abstracts, keyword scans and metadata checks are not represented as full-body reads.

## Reading the archive

audit_history preserves dated scientific snapshots, including preliminary percentages, prepublication status language and corrected mode/timestamp diagnostics. Later final reports and additive corrections supersede intermediate findings; earlier files were not silently rewritten. The six scientific/priority families are separate from the subsequent whole-publication-package review sequence. Snapshot paths in receipts describe the original execution environment; runnable controls above are self-contained and require no such paths. Source URLs and bibliographic metadata are retained, but primary-source PDFs, copied source bodies, downloads, rendered source pages, private environments and mutation working copies are excluded. Only explicit authored-safe file lists were copied. In particular the target-history family's excluded custody controls are absent.

SHA256SUMS.json describes every supplemental payload file except itself. It is a corruption check relative to that supplied manifest, not an independent trust anchor or mathematical certificate. The outer reviewed packet manifest binds the exact PDF, source, ZIP and deposit specification outside the ZIP.

AI tools were used extensively in development, drafting, sourcing, reproduction and adversarial review. The preprint is unrefereed and has not undergone conventional human peer review. Own-authored material is distributed under CC BY 4.0; no third-party full text is redistributed.
''')
entries=[]
for f in sorted(S.rglob('*')):
 if f.is_file() and f.name!='SHA256SUMS.json':entries.append({'path':str(f.relative_to(S)),'bytes':f.stat().st_size,'sha256':digest(f.read_bytes())})
emit(S/'SHA256SUMS.json',{'schema':'pr184.supplement.hashes.v1','self_excluded':True,'files':entries})
with zipfile.ZipFile(P/'verification-package.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for f in sorted(S.rglob('*')):
  if f.is_file():
   info=zipfile.ZipInfo(str(f.relative_to(S)),(2026,10,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,f.read_bytes())
metadata={'title':'Unbounded Godbillon-Vey numbers on a fixed hyperbolic manifold','upload_type':'publication','publication_type':'preprint','description':"<p>Classical compact-support suspension theory gives a foliated surface-times-interval block with product endpoint collars and nonzero ordinary Godbillon-Vey integral. Placing finite stacks in one fixed pseudo-Anosov mapping torus yields smooth cooriented taut foliations with GV=Na, a&gt;0, and the same embedded positive closed transversal meeting every leaf. This gives a negative answer to the literal unrestricted volume-bound Question 10.6 in Calegari's arXiv:math/0209081v1 (2002). Compact leaves are permitted; no minimal-foliation variant is claimed.</p><p>This is a credited consequence of classical Mather-Thurston/Tsuboi suspension theory, interval-bundle replacement documented by Gabai, and Thurston hyperbolization. A bounded primary-source audit did not authenticate an earlier explicit full consequence, but historical firstness, guaranteed novelty and present-day open status are not established. Relevant full texts remain unread, and the final 2003 target chapter was not compared. Version and access limits are documented in the supplement.</p><p>The deposit includes the research note, standalone LaTeX source, repaired exact-rational and symbolic local controls with actual ordinary/optimized reproduction, independent mathematical audits, and bounded priority ledgers. Finite controls do not replace the global existence proof. AI tools were used extensively in development, drafting, source checking, reproduction and adversarial review. This preprint is unrefereed and has not undergone conventional human peer review.</p>",'creators':[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'publication_date':'2026-10-13','version':'1.0','access_right':'open','license':'cc-by-4.0','language':'eng','keywords':['Godbillon-Vey invariant','taut foliations','hyperbolic 3-manifolds','Calegari Question 10.6','compact-support suspension','mapping tori','interval-bundle replacement'],'related_identifiers':[{'identifier':'https://github.com/AlecKriebel/Math/pull/184','relation':'isDerivedFrom','scheme':'url'},{'identifier':'https://arxiv.org/abs/math/0209081v1','relation':'references','scheme':'url'},{'identifier':'10.5802/aif.828','relation':'references','scheme':'doi'},{'identifier':'10.5802/aif.1289','relation':'references','scheme':'doi'},{'identifier':'10.1090/S0002-9947-1988-0930079-9','relation':'references','scheme':'doi'},{'identifier':'https://arxiv.org/abs/math/9801045v1','relation':'references','scheme':'url'}],'notes':'Negative answer to the literal 2002 manuscript formulation using credited classical ingredients. Historical priority remains unresolved after a bounded audit with explicit unread-source gaps. No certified firstness, guaranteed novelty, current-open-status or minimal-foliation claim. AI-assisted; unrefereed; no conventional human peer review.'}
emit(P/'zenodo-deposit.json',{'metadata':metadata,'files':[{'path':x} for x in ['taut_godbillon_vey.pdf','taut_godbillon_vey.tex','verification-package.zip']]})
(P/'README.md').write_text('''# PR184 research-note publication candidate

The three intended uploaded files are taut_godbillon_vey.pdf, its standalone .tex source, and verification-package.zip. zenodo-deposit.json supplies the exact intended metadata to the repository's top-level Zenodo upload kit. No deposit has yet been created by this build. The full package still requires successive fresh independent adversarial reviews and explicit clearance. Mathematical validity and historical priority are distinct: this is a qualified credited classical-consequence note, with priority unresolved. The manuscript and supplement state the exact question version, access gaps, computational limits, AI use and unrefereed status.

The ZIP contains README reproduction commands, standard-library and SymPy controls, a payload hash manifest and explicitly allowlisted own-authored scientific/priority audit history. It contains no primary-source PDFs or full-text copies. Internal prepublication status and dated interim findings are historical snapshots, not final release declarations. The outer REVIEW_PACKET_MANIFEST.json binds exact candidate bytes; it is not a mathematical or independent trust certificate. Build and visual-review intermediates are outside the three-file deposit.
''')
outer=['taut_godbillon_vey.pdf','taut_godbillon_vey.tex','verification-package.zip','zenodo-deposit.json','README.md']
emit(P/'REVIEW_PACKET_MANIFEST.json',{'schema':'pr184.whole-publication-candidate.v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_head':'fbd6561971368a0867df83453454427863d7f910','historical_priority':'unresolved','publication_ready':False,'files':[{'path':x,'bytes':(P/x).stat().st_size,'sha256':digest((P/x).read_bytes())} for x in outer],'supplement_payload_files_excluding_manifest':len(entries)})
print(json.dumps({'files':len(entries),'zip_bytes':(P/'verification-package.zip').stat().st_size,'packet_manifest_sha256':digest((P/'REVIEW_PACKET_MANIFEST.json').read_bytes())}))
