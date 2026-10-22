# Verification summary: final two-parent triangle insertion

The accompanying authored proof establishes two-root block gluing and explicit two-connected, nonplanar, incidence-dimension-three families with unbounded degree at both roots. It does not resolve the general conjecture.

## Exact checks

- Nine geometric fixtures supply 5759 complete nonempty-subfamily certificates. These include the two-half-plane source model, three shared-pair block fans, three block/ear families, and two actual recursive insertions across newly introduced pair-edges.
- Every feasible certificate is checked against the original rational inequalities. Every direct infeasibility certificate has nonnegative multipliers, zero weighted normal, and a strictly negative weighted right side. Larger nonfaces name a contained direct infeasibility certificate. A separate replay verifies these identities without invoking elimination.
- All declared hyperedges have strict rational common witnesses. Maximal faces, coverage, looplessness and linearity are explicitly compared. The source model's minimum witness slack is 9/500000.
- A separate complete incidence-order checker accepts the independent searched eight-vertex certificate and the uniform constructions. The largest pure block test has 803 incidence elements, 644006 ordered pairs and exactly 1202 strict incidences. Mixed block/ear orders are checked independently as well. The full universal proofs are in the report.
- Recursive insertions use actual rational private side crossings, scales 1/8 and 1/4096, exact separation from every other old triangle, and exact agreement with the two local root half-planes. The old coordinate lists are unchanged at each insertion. These extra recursive fixtures carry no incidence-dimension assertion.

## Determinism and adversarial controls

The three exact checkers run with normal Python, -O and -OO, each under hash seeds 1,77,999. All 27 runs pass; outputs are byte-identical for each checker across modes and seeds. Every verification gate is an explicit exception.

Eight genuine mutations are rejected in each Python mode, for 24 required rejections: negative thickening; reversed root half-plane; colliding scale bands; loss of the segment endpoint; missing reverse block order; missing root-last order; disabled geometry gates; and a negative certificate multiplier. Each failure must match the intended diagnostic. Timeouts, import errors and unrelated exceptions do not count.

Closed point and line intersections, inconsistent parallel inequalities, inconsistent zero-normal constraints and an unconstrained plane are controlled separately. The positive certificates and universal proofs are not inferred from solver search outcomes.

## Fixed mathematical artifacts

- Full authored report: 26874 bytes; SHA-256 fb21fcf28c33fa396067ca455a45a6e8ba77eedb623f1bddd261e6fb7c6f79e4.
- Complete exact geometric certificates are retained separately; the distributed exact examples give the complete authored coordinates, whole edges, witnesses and recursive insertions.
- Complete exact incidence-order verification records are retained separately; the distributed finite certificates contain complete orders and every vertex-criterion witness.

Private source programs, raw inputs and recovery material remain separate from this public mathematical report. The complete payload is preserved in both a full recovery archive and a content-addressed byte store. Fresh restorations are compared file-by-file and byte-for-byte, and the exact verification and mutation harnesses are rerun from restored copies. The external preservation receipt records the resulting inventory, hashes and replay outcomes.
