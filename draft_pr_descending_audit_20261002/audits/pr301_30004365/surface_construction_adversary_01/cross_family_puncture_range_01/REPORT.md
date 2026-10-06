# Cross-family falsification: A(3,5) versus A(4,4)

UTC 2026-10-05T11:37:12Z. Witness-check completion estimate 100%. This report follows the completed independent surface audit, whose prior reports, code, results, logs and manifest have not been edited. Only now was the classification family's PRINTED_RANGE_COUNTEREXAMPLE.md read.

**Result: the witness is independently verified. No numerical or topological disagreement found.** The two algebras satisfy the literal printed genus-zero APS7.4 comparison with winding equality only on original boundaries, while their full puncture winding multisets disagree. The submitted candidate's full peripheral key distinguishes them correctly.

## Separate computations

verify_witness.py constructs both quivers directly: arrow indices0…m-1 are u_i, m…m+n-1 are v_j, and m+n is the bridge z. Relations contain the two full cycle relation sets, with no bridge relation. It imports the already frozen surface_fixture_audit.py, whose mechanism was derived before consulting the classification witness. It calls the full exact lozenge quotient/link/dual-cut checker and its previously derived collar-sector formulas. It separately enumerates the monomial path basis from arrows and relations; dimension is not inferred from the classification family's formula.

| Exact quantity | A(3,5) | A(4,4) |
|---|---|---|
| Original quiver vertices/arrows | 8 / 9 | 8 / 9 |
| Nonzero paths by length0,1,2,3 | 8,9,2,1 | 8,9,2,1 |
| Dimension over fixed k | 20 | 20 |
| Longer paths | none | none |
| Filled lozenge surface g,b,black punctures | 0,1,2 | 0,1,2 |
| White/black marks on original boundary | 7 / 7 | 7 / 7 |
| White interior punctures | 0 | 0 |
| Compact puncture-truncated core Euler characteristic | -1 | -1 |
| Boundary dual-arc endpoint occurrences | 8 | 8 |
| Original-boundary winding | 6 | 6 |
| Puncture dual valencies | 3,5 | 4,4 |
| Puncture winding multiset | -5,-3 | -4,-4 |
| Full peripheral (n,w) key | (0,-5),(0,-3),(7,6) | (0,-4),(0,-4),(7,6) |
| AG pairs (n,n-w) | (0,3),(0,5),(7,1) | (0,4),(0,4),(7,1) |

All corner links are circles or intervals. Red-side cutting yields seven disks, each with one white boundary occurrence, for each algebra. The detailed lozenge arrows, side pairings, quotient data, and every nonzero monomial basis path are in RESULTS.json. Peripheral windings use the frozen independent derivation w(boundary)=2m_white-d=14-8=6 and w(puncture)=-dual-valency. Their sums are -2, agreeing with the compact core formula 4-2(1+2)-4·0.

## Source logic and exact consequence

The APS final primary body was already read independently: Theorem6.1 printed p19 requires preservation of winding for every simple closed curve by an orientation-preserving marked-surface homeomorphism; the proof and Remark6.2 run through pp19–21. Such a homeomorphism permutes puncture loops, so these unequal puncture winding multisets obstruct derived equivalence. APS7.4 printed p24 restricts winding equality in item(2) to j=1,…,b, with no genus-zero handle condition. Its literal conditions therefore identify this pair incorrectly. The proof printed pp26–27 uses equality on all c in B, exhibiting the missing puncture requirement directly.

The workshop's printed p163 Theorem3.3 lists only genus, puncture number, and boundary marked counts in genus zero, which also coincide here. Hence its completeness summary fails on the same pair, although the literal computation request in Problem3.4 remains well-defined.

**Mandatory additive correction for any complete-invariant proof:** explain the truncated printed statement and justify sufficiency using a correct criterion that includes every puncture peripheral winding. The candidate already returns those values, so this witness requests a source/proof repair rather than a change to its output key. My prior surface/topology PASS remains valid within its stated scope; a blanket invocation of printed APS7.4 as sufficient needs this correction.

## Execution evidence and limits

The actual run captures/cross_family_witness contains exact native argv/cwd/request, actual process PID/start time, finish/elapsed time, full stdout/stderr and the executed source snapshot. It exited0 in0.039s; stderr is empty. The imported checker is captured as imported_surface_fixture_audit.py.gz with SHA256 5b67ea0c252b89fab95be30d538c509750e57f06d6c5b96a25db1769e36c030c, matching the prior frozen artifact manifest. An additional preservation run verifies every prior manifest file is unchanged.

The computations verify finite quiver/path, surface/corner, and peripheral sector data. Non-derived-equivalence uses the accepted APS6.1 theorem; this is not a direct categorical computation. This follow-up does not independently audit LP's general sufficiency theorem, determine novelty, or establish a full production invariant implementation. No external communication, Git, shared controls, or publication was performed.
