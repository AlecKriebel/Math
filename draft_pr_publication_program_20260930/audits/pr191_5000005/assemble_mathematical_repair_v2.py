"""Assemble explicit two-formulation proof while preserving every original byte."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent
def require(x,msg):
 if not x:raise RuntimeError(msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=A/'global_affine_geometry_adversary/GEOMETRIC_REDUCTION.md';negative=A/'literal_type_source_adversary/ANALYTIC_CERTIFICATE.md'
require(digest(source)=='c229ba7e8f33b311d8dba01eefd2ae6d794041636db2cc22d83234fd98169f0b','Clean geometry input drift')
require(digest(negative)=='a2f75ea7da4fa7279e1be57908689b7f9358601da8463f4a15f8f762e4fca13c','Literal obstruction input drift')
stamp=datetime.datetime.now(datetime.UTC).isoformat();cert=negative.read_text();start=cert.index('## 1. Geometric calibration');end=cert.index('## 4. Audit certificate')
header='''# Parallel short trajectories: literal obstruction and a parity-selected signed law

Current mathematical repair v2. This is a reviewable proof artifact, not a declaration of publication readiness or historical novelty. Original PR191 head a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe, effort2/5, and all16 original files remain preserved unchanged under original_submission/files/. The original candidate is not overwritten by this assembly.

There are two explicitly different conclusions. First, the immutable imported global conjunction, including its bare A0 iff beta−alpha=2pi/n condition, is false for every n>=5. Second, the parity-selected type K_PS defined below obeys the all-admissible signed law, with first-vertex existence, for every n>=3. This proves a supported completion of the source convention and its generic-sector law, rather than turning the inconsistent conjunction into a positive theorem. The literal direct-diagonal counterexamples are outside/on the boundary of the source's preceding open fundamental sectors. No counterexample to that restricted generic conjecture is asserted.

Fuchs's published title is Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra, Arnold Mathematical Journal7(2021),493–517, DOI10.1007/s40598-020-00170-8; it appeared online7January2021. The immutable upstream target's differing title and2020 metadata are retained as historical imported metadata. The actual full source body, Figures8/9 and parity paragraph are the mathematical provenance. No author-authenticated erratum or uniquely forced source intent is claimed.

The following source-calibration/counterexample derivation was independently written by the literal/type adversarial family before any sibling report or old opinion. The clean all-direction proof was written by the independent geometric family; its common-label construction credits the submitted candidate. Root independently checked both, including the direct double-surface shear and finite-length descent. Classical polygon surfaces/shears and affine geometry are not claimed as new. The original Veech body is not a load-bearing unread import in the direct proof. Priority is a subsequent separate audit, and no present openness, firstness, awareness or independent chronology is certified here. AI tools were used extensively; this work is unrefereed and has not undergone conventional human peer review.

## Part I. Exact target and convention repair

'''
text=header+cert[start:end]+'\n\n## Part II. All-direction proof of the explicit parity-selected law\n\n'+source.read_text()
target=A/'CURRENT_PROOF_V2.md'
with target.open('x') as f:f.write(text)
target.chmod(0o444)
manifest=json.loads((A/'ORIGINAL_FILE_MANIFEST.json').read_text())
for x in manifest['files']:
 p=A/'original_submission/files'/x['path'];require(p.is_file() and not p.is_symlink() and digest(p)==x['sha256'] and (p.stat().st_mode&0o777)==0o444,'Original artifact drift')
receipt={'UTC':stamp,'status':'EXPLICIT_TWO_FORMULATION_REPAIR_ASSEMBLED_FINAL_GEOMETRY_FAMILY_AUTHENTICATION_PENDING','original_candidate_SHA256':'6d406380552758f7b4292759d62c12cbf2fe7f4c03e358086d6fac938ed10260','current_proof':{'path':target.name,'bytes':target.stat().st_size,'SHA256':digest(target),'actual_mode':'0444'},'inputs':[{'path':str(source.relative_to(A)),'SHA256':digest(source)},{'path':str(negative.relative_to(A)),'SHA256':digest(negative)}],'repairs':['Explicit negative literal target and distinct positive K_PS theorem; no scope conflation','Distinguish generic open source sector from global all-admissible extension','Admit source endpoint representative k=N congruent0 before modular reduction','Direct cylinder/shear/descent replaces unread original cusp-chain dependence','Exact source title/online-publication metadata corrected with imported metadata retained'],'original16_files_all_unchanged_and_actual0444':True,'mathematical_clearance':False,'priority_clearance':False,'publication_ready':False,'remote_or_PR_disposition_performed':False}
with (A/'ROOT_MATHEMATICAL_REPAIR_01.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
(A/'ROOT_MATHEMATICAL_REPAIR_01.json').chmod(0o444);print(json.dumps(receipt))
