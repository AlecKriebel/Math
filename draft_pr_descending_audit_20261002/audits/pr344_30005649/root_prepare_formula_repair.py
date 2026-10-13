#!/usr/bin/env python3
"""Prepare (without installing) the B2 public supplement repair after independent reproduction."""
from pathlib import Path
import ast,datetime,hashlib,json,difflib
A=Path(__file__).resolve().parent;H=A/'preprint';OUT=A/'root_preprint_private/formula_repair_preparation_001'
assert not OUT.exists();OUT.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
input_names=['qss-self-duality-note.tex','qss-self-duality-note.pdf','qss-self-duality-verification.zip','zenodo-deposit.json','build_supplement.py','verify_supplement.py']
inputs={name:sha((H/name).read_bytes()) for name in input_names}
original=(H/'build_supplement.py').read_bytes()
assert sha(original)=='5e26dd86f2091264756686c1bcdb18f688d4eec2b5d921540c5437545873490a'
s=original.decode()
def replace(old,new):
 global s
 assert s.count(old)==1,old
 s=s.replace(old,new)
replace('def derive_control(name,edits):',"def derive_control(name,edits,scope='Only runtime provenance output and included-document references; mathematical code/assertions/input data unchanged.'):")
replace("scope='Only runtime provenance output and included-document references; mathematical code/assertions/input data unchanged.')\n# Preserve",'scope=scope)\n# Preserve')
replace("    ('report.md','manuscript.tex',2)])",'''    ('report.md','manuscript.tex',2),
    ('rank(join(transpose(f2),transpose(v2)),k)',
     'rank(join(transpose(twist(twist(v2,k.sigma),k.sigma)),transpose(twist(twist(f2,k.tau),k.tau))),k)',1),
    ('def main():',(HERE/'intrinsic_formula_regressions.txt').read_text()+'def main():',1),
    ('    result={"status":"pass",',
     '    dense_kernel_controls=check_dense_kernel_formulas(f,v)\\n    result={"dense_kernel_formula_controls":dense_kernel_controls,"status":"pass",',1)],
    scope='Runtime provenance/document-reference repair B1, plus mathematical helper correction B2: opposite squared Frobenius twists and actual-kernel/minimal/dense basis regression checks over F125, F343 and generic-formula-only F32. Historical original control and input data preserved; public mathematical code/assertions are intentionally corrected and extended.')''')
replace("add('manuscript.tex',HERE/'qss-self-duality-note.tex')","add('CONTROL_FORMULA_CORRECTION.md',HERE/'CONTROL_FORMULA_CORRECTION.md')\nadd('manuscript.tex',HERE/'qss-self-duality-note.tex')")
replace('control_derivations=control_derivations,raw_primary_source_bodies_included=False))',"control_derivations=control_derivations,mathematical_control_correction='CONTROL_FORMULA_CORRECTION.md',historical_audit_control_acceptance_qualified_for_generic_formula=True,raw_primary_source_bodies_included=False))")
replace('unchanged, and all mathematical code, assertions and input data are preserved.', '''unchanged. The corrected public intrinsic derivative also repairs a generic
semilinear dual-kernel formula: opposite squared Frobenius twists are essential.
CONTROL_FORMULA_CORRECTION.md derives the formula and its exact counterexample.
New actual-kernel/minimal/dense controls cover F125, F343 and a Frobenius-order-five
F32 sample. The latter checks only generic linear algebra and does not extend
the group-scheme theorem beyond p>3. Its public mathematical code and assertions
are intentionally corrected/extended, with original input data preserved.''')
ast.parse(s)
(OUT/'build_supplement.py').write_text(s)
(OUT/'builder.diff').write_text(''.join(difflib.unified_diff(original.decode().splitlines(True),s.splitlines(True),fromfile='v03/build_supplement.py',tofile='prepared_v04/build_supplement.py')))
rec=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PUBLIC_FORMULA_REPAIR_PREPARED_NOT_INSTALLED',original_builder_sha256=sha(original),prepared_builder_sha256=sha(s.encode()),fragment_sha256=sha((H/'intrinsic_formula_regressions.txt').read_bytes()),derivation_sha256=sha((H/'CONTROL_FORMULA_CORRECTION.md').read_bytes()),current_six_inputs_unchanged=True,requires_completed_second_historical_adverse_review=True,requires_new_third_full_review=True)
(OUT/'PREPARATION.json').write_text(json.dumps(rec,indent=2)+'\n')
assert {name:sha((H/name).read_bytes()) for name in input_names}==inputs
print(json.dumps(rec,indent=2))
