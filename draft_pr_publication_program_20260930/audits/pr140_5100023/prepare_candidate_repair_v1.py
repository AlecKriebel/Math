"""Separate candidate repair; original capture and historical reviews remain intact."""
from pathlib import Path
import datetime,hashlib,json,os
A=Path(__file__).resolve().parent
F=A/'repaired_candidate_v1';F.mkdir(exist_ok=False)
proof=(A/'original/PROOF.md').read_text()
old="The source's introduction specifies a pair of confocal ellipses, rather than a hyperbolic caustic. Its N-periodic polygon is understood with N distinct successive vertices (least period N)."
new="The source's introduction specifies a pair of confocal ellipses, rather than a hyperbolic caustic. Here N explicitly denotes least period, with distinct successive vertices. The source does not formally define least period, but its Section 3.7 uses central inversion of opposite vertices of even orbits; that supports this primitive-period interpretation. We do not ascribe an arbitrary repeated-list interpretation to the source."
if proof.count(old)!=1:raise RuntimeError('exact scope patch preimage required')
proof=proof.replace(old,new)
author=(A/'original/verify.py').read_text()
if author.count(' assert p\n')!=1:raise RuntimeError('author predicate preimage')
author=author.replace(' assert p\n',' if not p:raise RuntimeError("Exact verification check failed")\n')
independent=(A/'original/independent_review/independent_checks.py').read_text()
if independent.count('    assert ok,name\n')!=1 or independent.count('    assert D!=0\n')!=1:raise RuntimeError('independent predicate preimage')
independent=independent.replace('    assert ok,name\n','    if not ok:raise RuntimeError(name)\n').replace('    assert D!=0\n','    if D==0:raise RuntimeError("Singular antipedal line system")\n')
(F/'PROOF.md').write_text(proof);(F/'verify.py').write_text(author);(F/'independent_checks.py').write_text(independent)
(F/'author_replay').mkdir();(F/'author_replay/PROOF.md').write_text(proof);(F/'author_replay/verify.py').write_text(author)
(F/'README.md').write_text('# Prospective corrected PR140 candidate\n\nThe theorem is explicitly for even least period and a nondegenerate confocal elliptical caustic. Source Section 3.7 supports the central-symmetry convention but does not formally define least period. Repeated odd lists are excluded; an exact boundary counterexample is retained in the algebraic family audit.\n\nValidation uses explicit exceptions in normal and optimized Python modes. The original seventeen source files and original historical reviews remain unchanged in ../original and ORIGINAL17_MANIFEST.json. This directory is a separate prospective repair, not a relabelled original review or a publication clearance. Priority has not been assessed.\n')
files=[]
for p in sorted(F.rglob('*')):
 if p.is_file():
  b=p.read_bytes();files.append({'path':str(p.relative_to(F)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(F/'PREPARATION.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'scope':'Period-convention wording and explicit verifier failures only; proof equations/mechanism unchanged','originals_modified':False,'files':files,'priority_clearance':False,'case_completion_estimate_percent':35},indent=2)+'\n')
print(json.dumps({'prepared':str(F),'files':len(files),'actual_PID':os.getpid(),'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
