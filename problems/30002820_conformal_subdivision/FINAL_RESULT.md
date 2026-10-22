# Final author result: 30002820 / OWR-13498-010

**Five substantive author turns completed. Recommended disposition: unsolved, 5/5, with a source-interpretation hold. Independent full review is pending.** A complete non-isometric conformal refinement theorem is proved under the printed output-metric definition. The intended unrestricted metric-compatible subdivision problem is not claimed solved.

## Source and interpretation

Ulrich Bauer, Problem 6, “Subdivision of discrete conformal structures”, *Discrete Differential Geometry*, OWR 13/2015, printed pp.721–722: https://ems.press/content/serial-article-files/46561 . Report citation: Oberwolfach Reports 12(2015), no.1, 661–729; DOI https://doi.org/10.4171/OWR/2015/13 . The publisher records submission 1 March 2015 and publication 4 December 2015. Rote's primary reproduction is https://page.mi.fu-berlin.de/rote/Kram/OWR-DDG15-problems.pdf , pp.3–4.

The printed map takes a complex with a metric to a subdivision equipped with another metric, and gives barycentric subdivision as an example. It does not explicitly require that the new face metric induce the original one. The surrounding geometric context makes that compatibility interpretation plausible, but no authoritative clarification was recovered. We therefore retain the uncertainty rather than claim a broad solution through an unstated convention. All comparisons here use the vertex/edge correspondence inherited from the indexed input triangulation.

The turn-1 gate's warning about vacuous constant-output constructions remains relevant. The turn-4 theorem is stronger and substantive: it is a proper, metric-dependent refinement preserving old edge totals and extending old conformal factors. Even those properties do not imply face isometry. Its positive theorem and the unresolved intended problem must both remain visible.

## Complete positive output-metric theorem (turn 4)

For a finite triangulated surface with nondegenerate Euclidean triangle metrics, there is an explicit proper, conformally equivariant output-metric refinement, in five rounds, with one new vertex on every old edge and four child triangles per old face. A fixed combinatorial choice/coloring is allowed; full relabelling invariance is not asserted. The construction also extends to locally finite countable triangulations with fixed combinatorial choices.

For an edge ij, select an incident triangle ijk by a metric-independent rule. Set t=l_ik/(l_ik+l_jk), split its length into t l_ij and (1−t)l_ij, and give every new diagonal to an incident opposite vertex q length

    l′_mq=(1−t)l_iq+t l_jq.

The strict triangle inequalities are proved in TURN_4.md. Under mu_uv=a_u a_v l_uv, retain every old factor and put

    D=a_i t+a_j(1−t),       a_m=a_i a_j/D,
    t_mu=a_i t/D,           1−t_mu=a_j(1−t)/D.

These identities prove every new edge equation mu′_uv=a_u a_v l′_uv. In particular both old edge totals and all old vertex factors are preserved exactly. The conflict graph of old edges sharing a face has maximum degree four; a fixed five-coloring makes each round commute and gives a complete whole-surface pass. No convergence theorem for iterated passes is claimed.

This is necessarily non-isometric in each affected face. With a=l_jq, b=l_iq, c=l_ij and h=(1−t)b+ta, the actual induced diagonal h_E obeys

    h²−h_E²=t(1−t)[c²−(a−b)²]>0.

The fixed underlying combinatorial subdivision can be realized at fixed barycentric points with the new output metric, or at input-dependent edge fractions t. Both preserve total edge length; only the latter preserves the old edge metric pointwise. Neither preserves the old face interior metric.

## Scoped negative results and scope control

1. TURN_1.md: induced midpoint 1-to-4 refinements of two metrics on a connected triangulated surface are conformally equivalent exactly when the original metrics differ by a global homothety. Disconnected surfaces allow componentwise homotheties.
2. TURN_2.md: every proper metric-independent fixed-barycentric refinement with induced Euclidean lengths fails to preserve all discrete conformal equivalences. The proof uses nonconstant adjacent-face cross ratios and arbitrarily small valid vertex rescalings.
3. TURN_3.md: no medial 1-to-4 metric rule with fixed boundary fractions works universally, even allowing arbitrary inner edge lengths. This concerns that particular medial topology; the positive turn-4 pattern generally differs.
4. TURN_5.md: no induced one-center-per-face stellar rule works universally, even with arbitrary global/discontinuous metric dependence, on an intrinsic tetrahedral boundary sphere. Retained old edges force old factors; a quantitative thin-face inequality then gives a valid counter-input depending on the reference output. No extrinsic tetrahedron embedding is assumed.
5. TURN_5.md also gives a deliberately limited positive isometric construction: split one chosen edge of a single triangular disk at its angle-bisector foot. The output's unique interior-edge cross ratio is always one. This does not glue into an arbitrary surface scheme.

These obstructions do not cover every metric-dependent induced subdivision with arbitrary topology. Failure of the stated classes must never be generalized into universal nonexistence.

## Evidence and remaining work

All five exact rational/squared-length receipts replay byte-for-byte: 176,654 author assertions. The final receipt verifies every historical manifest entry. The proofs establish the universal statements; the tests supply bounded reproducibility controls. The five-turn author budget is exhausted, and no sixth search is planned.

The standard vertex-scaling, cross-ratio and Möbius framework is credited to Luo (2004) and Bobenko–Pinkall–Springborn, https://arxiv.org/abs/1005.2698 . Canonical Möbius Subdivision (Vaxman–Müller–Weber, 2018), https://doi.org/10.1145/3272127.3275007 , concerns global Möbius equivariance and explicitly leaves preservation of arbitrary discrete conformal equivalence as future work. No historical novelty is claimed for the supplied deductions or construction. Raw source PDFs, source screenshots, imported records and retrieval logs are excluded from public artifacts.

The requested final independent audit must assess all five proofs, their exact hypotheses, the primary-source interpretation and the disposition. No full-target solved label is recommended without an established intended metric convention and a proof meeting it.
