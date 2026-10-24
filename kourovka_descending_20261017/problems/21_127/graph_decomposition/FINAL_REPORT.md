# Graph-decomposition family: research outcome

2026-10-24 UTC. **Unsolved. Estimated completion toward the original general RAAG rationality target: 7%. Publication gate closed.** No claim that these partial observations are new to the literature; no complete priority audit has been performed on them.

The independent route tested torus graph-of-groups splittings, in particular the first non-cograph tree P4. Its middle edge directions are central but noncommensurable, and that condition survives induced finite covers. The exact hypotheses of Chen's rationality theorem and Susse's common-amalgam theorem do not allow a direct application. Homologically collapsing the directions also violates the relevant scl-isometric-embedding theorem.

The strongest checkable partial is the **coordinate transport lemma**: once polygon blocks and paired turns are fixed, integer winding assignments making designated pieces disks exist exactly when every all-designated coordinate component has zero total charge. Its proof is integral spanning-tree flow, not numerical evidence. The minimum possible number of non-disks equals a finite hitting-set number.

A concrete P4 family has sixteen blocks and eight bad coordinate components, with minimum hitting number four. Its best relative surface objective is exactly 2 **within that fixed family**. The naïve count treating every locally potential block as a disk instead gives 0. A positive-density obstruction persists in every graph cover and rewiring that retains the unchanged block shapes; general annular covers can change shapes and are outside that counting statement.

For the two explicit exterior elements, both in the commutator subgroup, the actual homogeneous **chain** value is only bounded:

    1 <= scl_G(g1+g2) <= 2.

The lower bound follows from retraction to a single nontrivial free commutator counted twice. The upper bound follows from explicit cyclic covers of a six-holed sphere and capping its four inner torus loops. These bounds neither prove an exact scl value nor answer elementwise rationality. In particular the fixed-family lower bound is never promoted to a lower bound on the infimum over all surfaces.

Essential artifacts:

- `COORDINATE_TRANSPORT.md`: exact transport and transversal proofs, fixed-data scope.
- `P4_PROMOTION_OBSTRUCTION.md`: complete normal-block construction, unchanged-block-cover obstruction, and explicit cover/cap upper bound.
- `FREE_RETRACT_BOUND.md`: direct commutator identities and chain lower bound.
- `BLOCKED_REDUCTIONS.md`: additional failed mechanisms and precise obstructions.
- `check_transport.py`, `transport_certificate.json`: standard-library exact reconstruction and finite certificates.
- `free_turn_probe.py`, `free_turn_probe.json`: optional exact Fraction LP check for a single free commutator; unnecessary for the established direct proof.
- `SOURCE_MANIFEST.json`, `RESEARCH_LOG.md`: source custody, source-access limitations, timestamps, and nonmonotone estimate.

The remaining gap is a theorem controlling all possible polygon types, winding component structures, and pairings for an arbitrary fixed input word, or a different exact scl mechanism. An uncontrolled infimum of rational finite optimization values does not imply rationality. No complete positive or negative resolution was obtained; preserve these partials and require a new mechanism before reopening a blocked reduction.
