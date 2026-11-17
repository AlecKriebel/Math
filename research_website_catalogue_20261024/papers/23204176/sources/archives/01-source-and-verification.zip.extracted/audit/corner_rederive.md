# Independent corner and relative-extension audit

Checkpoint: 2026-10-07 04:40 UTC. Completion estimate: 100% of this narrow audit; this is not an estimate for the Hodge-conjecture program.

Audited upstream file, read-only: `/Users/alec/Desktop/math/preprints/The-rational-Hodge-conjecture-for-products-of-K3-surfaces-October-4-2026/build/manuscript/curvature.tex`, principally lines 230–472. No upstream edits, Git mutations, publication, or external individual contact occurred.

## Verdict and exact scope

**The narrowed relative construction passes this audit.** I found no counterexample to cut-order compatibility, preservation of a fixed ordinary child's output under external cyclic relabeling, retention of reciprocal switches when the external word is empty, the matching-surjectivity argument, or the finite collar/CF-extension mechanism. The current proof supplies more than the tree identity: its quasi-component paragraph supplies the neighborhood construction required before Proposition 14.5 can be used.

This is a validation of that construction relative to the stipulated collared, componentwise ordinary disk data, ordinary output submersivity, the cited immersed local chart/gluing theory, and the no-sphere hypothesis. It does not independently reprove the entire analytic gluing theory or verify the no-sphere hypothesis, the odd-degree hypothesis, or the rest of the manuscript. Those are upstream inputs, rather than new gaps discovered here.

In particular, there is **no additional unsupported lemma identified** merely because ChartsII states its results for boundary-rooted embedded disks. The source proofs expose their mechanism, and the manuscript identifies the changes needed for the mixed interior-rooted/ordinary system. The distinguished interior mark gives a type of component which is preserved under the exact partial-smoothing operations used in those proofs. Fixed-jump chart theory supplies the immersed local operators.

## Checkable tree and matching deductions

Let T be a disk tree and r its unique vertex carrying the distinguished interior mark. For every v != r, define its output to be the first edge on the unique path from v to r. This is a definition using the whole tree, independent of the order in which its edges are cut.

For a set S of cut edges, each component of T minus S contains either r or a unique flag toward r. Thus its root type is, respectively, interior-rooted or ordinary. Further cutting a second set S' gives exactly the components obtained by cutting S union S' at once. The output at every surviving ordinary vertex is the same flag in both descriptions. This proves the factor-label identity for an iterated normalized corner, rather than merely an abstract associativity assertion. For a chain r--a--b, both cut orders yield the factors P_r, Q_a, Q_b, where the output of Q_a is its flag toward r and that of Q_b its flag toward a. Forks behave in the same way, with sibling factor permutation.

The ribbon structure and the output flag give each ordinary child a unique linear input order, starting immediately after its output. A cyclic renumbering of *external* marks moves the global numbering seam; it does not move this child output or this local input order. This remains true when the child's external marks straddle the global numbering seam. Consequently, a fixed child's data need not be invariant under a transformation which reroots the child. This is the distinction the proof uses at curvature.tex:304–313 and 429–434. Decorations, including sector labels, are carried along with the relabeling.

An empty external word does not imply that every internal node is diagonal. A two-vertex type can have a root P with one internal flag labelled (p,q) and a child Q with reciprocal flag (q,p). These labels are internal and disappear after gluing. On the remaining arcs, source lifts can run from one preimage to the other and back, yielding a boundary lift with no external jump. This is an admissible combinatorial type; its presence does not assert that every such type has a holomorphic representative. It refutes the alleged *combinatorial* exclusion of switches by an empty external word. The current proof retains this type, at lines 249–255 and 453–460.

At a constant bivalent intermediate component, each open boundary arc has a constant lift to a preimage of the double value. It follows that either neither node switches or both do; exactly one switching node is impossible. Contracting the component preserves the surviving flag labels and the output path toward r. At reciprocal flags, contraction uses the same ordered dual cap-line pairing already used by gluing. This is an associativity statement about that fixed pairing, not a newly chosen sign. The concatenation T=T_1+...+T_j is independent of contraction order.

For the analytic matching assertion, write K_v for the augmented kernel of the linearized Cauchy--Riemann operator on a component. Component surjectivity first solves arbitrary componentwise inhomogeneous equations. The remaining diagonal edge errors lie in tangent spaces of L. Starting at r, choose a correction in K_v for every child v to prescribe its output evaluation and cancel its edge error toward its parent. Such a correction may alter evaluations at v's own child flags; cancel those subsequently by corrections on those children. Since T is a tree, this process never revisits an edge and terminates. Hence the full augmented operator, including all matching equations, is surjective. No joint surjectivity of all boundary evaluations on one component is needed. A reciprocal transverse switch has matching space a point and adds no tangent-space matching equation. This validates curvature.tex:333–349.

## Neighborhood construction, rather than tree equality alone

The following additional structure is necessary for the collar step:

1. Transported obstruction spaces defined for nearby ambient maps, with componentwise equality on each broken stratum.
2. Open/proper quasi-component index families, inherited from the fixed ordinary data and the lower interior-rooted problems.
3. Direct sums, surjectivity, and equivariance on a neighborhood; coordinate-change inclusions with coherent auxiliary forgetting.
4. Collared representatives of the product CF-perturbations, with agreement on iterated normalized boundaries.

The manuscript explicitly constructs this structure at lines 351–389, rather than trying to deduce it solely from lines 267–277. Its inherited index prescription agrees with ChartsII Condition 8.13: at a tree, take the union of the indices of its component problems. Whether a contracted subtree contains the interior mark determines its type. Thus the repeated inclusions in the proofs of Lemmas 8.19 and 8.20 remain the same; a subtree never acquires an ambiguous type or a changed ordinary output.

Lemma 8.19 gives openness of the inherited boundary family. Lemma 8.20 gives properness through degenerations. Definition 8.21 extends this family into a sufficiently small neighborhood while retaining the boundary prescription. Direct-sum and transversality conditions hold on the boundary by component support and the matching argument above, and persist on a smaller neighborhood. Additional compact-core choices cover the complement of that neighborhood and can be made transverse to the finite inherited family. This is exactly the neighborhood stage of the proof of Proposition 8.18, not an appeal to an unspecified relative theorem.

The semifiniteness needed here is the actual finite-cutoff setting of the manuscript. A positive nonconstant-energy lower bound and the arity/stability bounds imply finitely many relevant vertex and tree types. Choices under the finite stabilizers can be saturated, with invariant obstruction spaces and finite CF parameter representations. External cyclic relabeling preserves inherited ordinary indices because it preserves the ordinary output and local input order, as proved above.

ChartsII Theorem 5.3 then applies at the level of the componentwise construction: its proof identifies corner charts using the obstruction-space equality, not just the equality of the underlying stable-map factors. Remark 6.1 explicitly allows representatives to be chosen so that these identifications hold exactly for any finite collection of moduli problems. Therefore the finite relative argument has the representative-level coincidence required for AFOOO Remark 14.7.

The change in the root's condition removes boundary-output evaluation transversality; it does not require a new local differential operator. It also does not require interior-evaluation submersivity, because the target for virtual integration is a point. Auxiliary forgetting is performed in the admissible category. The manuscript's T-sum contraction rule is the mechanism for which AFOOO Section 14.3 gives admissible pullback compatibility. The stronger statement about forgetting on a full outer collar uses the source's bi-collared refinement; ordinary collaredness alone does not imply that refinement. Here no boundary-input forgetting is requested on a new root. The auxiliary-stabilization coordinate changes use the cited admissible chart construction. If a full outer-collar forgetful map is used, the standard bi-collared refinement must be retained from that construction. This is a known technical refinement in the cited proof, rather than a new relative-root lemma.

### Constant switching roots

The phrase “smooth nonconstant root” at curvature.tex:316 is not an exclusion of constant stable switching polygons: the proof retains them explicitly at lines 262–264 and 405–406, and invokes the ordinary fixed-jump local chart theory at lines 237–239 and 342–349.

A constant root carrying the interior mark and at least one boundary flag is already stable. It therefore need not be stabilized by new incidence marks transverse to a constant map. In a constant switching root the local Cauchy--Riemann operator is the same fixed-jump operator as in the cited immersed construction, with the interior-mark domain coordinate included. If an obstruction space is required, compact-core cokernel-killing sections can be chosen by unique continuation; this argument does not require the underlying map to be nonconstant. Since no boundary-output or interior-output submersion is requested on a root, there is no new evaluation condition. The one-input *diagonal* constant root is the separately identified regular space L. The unstable zero-input constant root is excluded and is not a missing endpoint of the construction.

Thus I found no additional unsupported constant-switch operator or neighborhood case.

## CF extension and source locators

AFOOO Proposition 14.5 does **not** extend raw boundary data. It requires a CF-perturbation already defined on a neighborhood of the compact prescribed set. The manuscript now first supplies an outer-collared corner neighborhood, then takes a smaller closed neighborhood as K. With f the map to a point, both weak and strong submersivity impose no additional evaluation requirement. The proposition returns a thickening and compatible CF data near K; this compatibility is sufficient to preserve the virtual integrations of the prescribed products. It should not be interpreted as asserting literal equality of every thickened chart with its original chart.

This is the same order of operations as the source proof. No use of Proposition 14.5 before its neighborhood hypothesis is supplied remains in the audited text.

Read source files:

- `AFOOO2606.12257v1.txt`: Proposition 14.5, lines 7363–7384; the explicit neighborhood/common-representative warning, 7410–7448; Remark 14.7 and Proposition 14.8, 7543–7591; the smaller-collar application of 14.5, 7593–7605.
- The same file: admissible T-sum pullback, 7684–7696; Definition 14.9/Proposition 14.10 and bi-collared construction, 7726–7785.
- The same file: Proposition 16.3's mixed parent/ordinary-bubble data, 8643–8718; no boundary-output submersivity required for the parent, Remark 16.4, 8740–8750; construction given the ordinary system, 8753–8758; fixed ordinary bubble data, Remark 16.5 and Remark 16.13, 8759–8764 and 8921–8931.
- The same file: Proposition 16.14, especially preservation of the ordinary CF factors, 8949–8965, and cyclic invariance, 8976–8981.
- `FOOOChartsII1808.06106v2.txt`: Theorems 5.3/5.4 and Remark 6.1, 790–831; actual corner-chart/bundle identification, 832–890; Conditions 8.12–8.15, 1970–2086; Proposition 8.17's properness-to-semicontinuity argument, 2088–2109; Lemmas 8.19/8.20, 2153–2221; Definition 8.21 and the neighborhood completion, 2222–2292.

[Akaho--Joyce, *Immersed Lagrangian Floer theory*](https://people.maths.ox.ac.uk/joyce/AkahoJoyce.pdf), Sections 4–5, supplies the immersed local boundary problems and capping orientations used here. In particular, Theorem 4.3 gives boundary factorization in Kuranishi spaces with diagonal and transverse sectors. This audit relies on that local analytic input and on AFOOO's corresponding immersed implementation; it does not identify a new constant-map obstruction to using it.

## Strongest verified result and remaining boundary of this audit

Given the ordinary geometric system specified in the manuscript and its imported local gluing/chart inputs, the finite mixed-root construction can carry its prescribed products through the neighborhood, outer-collar, and relative-CF stages without rerooting or changing an ordinary child operation. The combinatorial and linear matching claims above are independently checkable deductions. The analytic stage is a valid finite adaptation of the mechanisms in the cited proofs.

No falsifying example or distinct unfilled analytic lemma was found in this narrow scope. I have not promoted the resulting Stokes identity into a validation of the full curvature-removal argument or the overall Hodge claim.
