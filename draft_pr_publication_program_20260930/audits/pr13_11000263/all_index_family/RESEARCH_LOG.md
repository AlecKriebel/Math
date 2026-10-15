# Independent all-index algebra audit log

Target: PR 13 source snapshot `7a845f7e025a24affe1b712cf7ada648570f9c64`, record 11000263.
Scope: only the Burau algebra family, repaired index ranges, parameter changes, scalar twists, and dimension inference.
Independence boundary: read `AUDIT.md` and `SOURCES.md`, not historical `REVIEW.md`, `verdict.json`, or sibling audits. No canonical edits, Git mutations, or external outreach.

## 2026-10-01 13:32:03 UTC — initialization (15%)

Defined the success criterion: derive all-index images directly, verify every legal relation including the exceptional first row, and attempt to falsify the generic nonvanishing and specialization claims. Classification remains a hypothesis. Retrieved primary paper definitions; the preprint explicitly lists generators only through sigma_(n-1), while the terminal relation uses sigma_n. Published scan is being inspected independently. Temporary fulltexts and page renders remain in ignored `tmp/`.

## 2026-10-01 13:33:45 UTC — proof checkpoint (70%)

Visually inspected published p. 298, confirming the whole-word inverse and terminal sigma_n. Direct basis-vector propagation yields the advertised rank-one image for every index and kills every legal relation, with a separate calculation for R2. Both repaired quotients have nonzero X3 over Q(q), detected in Q(q,u) matrices. Recorded the legitimate specialization ring F[u,u^-1]; specialization of the entire field Q(q,u) would be invalid. At n=3, X4 is unavailable in A3 and available in C3. No sibling or historical verdict has been read.

## 2026-10-01 13:37:17 UTC — computational/adversarial checkpoint (90%)

Fresh standard-library sparse Laurent-polynomial implementation passed 426 exact symbolic assertions on 3–10 strands, including all legal rows, full-word inverses, both repairs, rank-one images, scalar twists, and u=q/q^2/q^3 controls. At q=2,u=3 both deliberate wrong-order and missing-constant R2 variants fail explicitly. Generic independent-u image is infinite-dimensional as an F-algebra because sigma_1 has eigenvalue -u and no nonzero F-polynomial can annihilate it; this is distinct from the finite-dimensional u=q^3 image. The latter does not bound any universal quotient by added relations. Drafting the independent report and machine-readable verdict.

## 2026-10-01 13:41:53 UTC — final audit checkpoint (100%)

Completed `REPORT.md`, `probe.py`, `probe_results.json`, and `verdict.json`. Verdict is PASS_CONDITIONAL_SCOPE: no fatal mathematical defect found in the witness for the two named repairs. Strongest verified claim: X3 is nonzero in both repairs for every n>=3 over Q(q). All-index proof, source defect, n=3 edge, base-change route, dependent twist values, and dimension inference are documented. Exact prior-art chronology and intended correction remain outside this family's evidence. This 100% refers to the assigned audit, not a novel solution of the literal defective problem. No canonical edits, Git mutations, or outreach occurred.
