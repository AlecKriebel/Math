# Logarithmic sampling for strong involution centralizers

## Result and attribution

The asymptotic sampling question in Cheryl E. Praeger’s contribution, joint with John D. Dixon and Ákos Seress, *Finding strong involutions in finite classical groups in odd characteristic*, is resolved in its natural matrix-group setting: for each fixed desired confidence, logarithmically many independent uniform samples suffice to generate a subgroup containing the second derived subgroup of the given strong involution’s centralizer. The contribution appears on printed pages 2160–2161 of [Oberwolfach Report 37/2016](https://ems.press/content/serial-article-files/46642), [DOI 10.4171/OWR/2016/37](https://doi.org/10.4171/OWR/2016/37).

The linear and unitary conclusions are credited prior results of Dixon–Praeger–Seress and Glasby–Praeger–Roney-Dougal. The authored marginal proofs here supply the symplectic and orthogonal cases; an audited natural-group bridge and an independently sourced 192-class generation theorem complete their generation argument. The distinction between these contributions and the cited literature is essential. No claim of worldwide novelty or external peer review is made.

This reader includes the complete authored proofs, mathematical audits, source-boundary review, and finite certificates. Finite computations corroborate specified identities and expose specific false alternatives; they do not prove a theorem over unbounded dimensions or field orders.

## Main theorem

Let q be any odd prime power. Let G be one of the natural matrix groups

SL_n(q), SU_n(q), Sp_n(q), SO_n^ε(q), or Ω_n^ε(q),

where ε includes odd orthogonal dimension and both even-dimensional Witt types. Let t∈G be any fixed strong natural involution: both ±1 eigenspaces have dimensions in the closed interval [n/3,2n/3]. Natural unitary dimension means dimension over F_(q²). Quantification is over involutions actually belonging to G, so determinant, spinor, and dimension parity restrictions are respected.

There is an absolute integer N such that for each δ∈(0,1) there is a constant K_δ independent of q, n, t, and the admissible form type with the following property. For n≥N, take M≥K_δ log n independent uniform samples g_i in the actual ambient G. Define

z_i=inv(t t^(g_i)),   H=⟨z_1,…,z_M⟩,

where inv(y)=1 for odd |y| and inv(y)=y^(|y|/2) otherwise. Then

P(C_G(t)''≤H≤C_G(t))≥1−δ.

The full isometry family O_n^ε(q), as well as GL_n(q) and GU_n(q), is additionally covered. The prime power q is arbitrary and need not tend to infinity. The theorem uses a given t, not a randomly typical involution. Every z_i centralizes t because conjugation by t inverts t t^(g_i) and fixes its unique involution when its order is even.

The source’s named algorithmic reference explicitly uses SL, SU, Sp, SO, and Ω in their natural representations, and its complexity convention concerns sufficiently large dimensions with a separately prescribed failure probability. The exact source comparison is in the [scope acceptance](audits/SCOPE_ACCEPTANCE.md). Thus N is part of the theorem, not an omitted small-case assertion.

## Marginal estimates and exact sample bounds

The separately fixed + and − target eigenspaces have the following bounds. None is a simultaneous-success assertion.

- GL: n≥700 and marginal probability at least 0.0002/log n, by Dixon–Praeger–Seress, Theorem 1.1. The elementary transfer below gives SL.
- GU: n≥250 and marginal probability at least 0.0001/log n, by Glasby–Praeger–Roney-Dougal, Theorem 1. Uniform sampling satisfies their nearly-uniform hypothesis. The transfer below gives SU.
- Sp: n≥49152 and probability greater than 1/(40000 log n), by the [symplectic proof](proofs/SYMPLECTIC_MARGINAL_PROOF.md) and its [audit](audits/SYMPLECTIC_AUDIT.md).
- O, SO, Ω: n≥98304 and probability greater than 1/(5000000 log n), by the [orthogonal proof](proofs/ORTHOGONAL_MARGINAL_PROOF.md) and its [audit](audits/ORTHOGONAL_AUDIT.md).

Consequently the common marginal lower bound 1/(5000000 log n) holds across all listed families for n≥98304. For generation, the orthogonal construction imposes an additional square-discriminant condition retaining exactly half the counted mass; both component restrictions then lie in Ω. That refined bound is 1/(10000000 log n), proved in Section 3 of the [bridge](proofs/GENERATION_BRIDGE.md).

For the new Sp/O/SO/Ω part, let a=dim E_−(t), b=dim E_+(t), and let d₀ be the absolute dimension constant in the [192-class theorem](proofs/CLASS_GENERATION.md). Put

κ=1/40000 for Sp, and κ=1/10000000 for O/SO/Ω,

L=ceil(κ^(−1)log n·log(385/η)),  M=385L,  0<η<1.

For Sp require n≥max(49152,3d₀); for O/SO/Ω require n≥max(98304,3d₀). The probability of failure is at most

η+q^(−a)+q^(−b)+13q^(−2b²/9).

With η=1/20, success is greater than 0.9. Independent repetition r=ceil(log(1/δ)/log 10), retaining all outputs, gives failure at most δ. No certificate identifying which batch succeeded is required for this probabilistic containment theorem.

For GL/GU, Glasby–Praeger–Roney-Dougal Theorem 2 gives constants λ,n₁ such that at least λlog n independent nearly-uniform samples yield the required SL/SU product with probability greater than 0.9(1−q^(−n/3)−q^(−2n/3)). At a common sufficiently large threshold this is greater than 0.8 uniformly in q. Independent repetition gives the same asymptotic confidence dependence. The whole theorem therefore has a sample bound O(log n·(1+log(1/δ))). For fixed δ this is O(log n); for δ=n^(−A) the displayed bound is O((log n)²).

The overall dimension cutoff is absolute but unevaluated: the replacement proof uses a published absolute maximal-subgroup-count constant C, and the credited linear/unitary generation theorem supplies n₁. One may increase N to at least max(n₁,98304,3d₀). No numerical N is certified.

## Required transfer from full to special groups

Let D=GL(V), J=SL(V), or D=GU(V), J=SU(V), and suppose t∈J. Its eigenspace decomposition is V=A⊕B, perpendicular and nondegenerate in the unitary case. The centralizer in D is D(A)×D(B). Its determinant map is onto the determinant image of D: in GL scale one basis vector by any nonzero field scalar; in GU use an orthogonal basis and scale one vector by any scalar of norm one. Both eigenspaces are nonzero.

Since J is the determinant kernel, D=J C_D(t). Hence t^D=t^J. Uniform conjugation in either finite group gives the uniform distribution on this same class, with equal-sized fibers. Therefore the entire output matrix inv(t t^g), and every independent sequence of outputs, has exactly the same law under uniform D and uniform J sampling. This transfers both credited marginals and the even-output generation theorem. It does not presume that a uniform special-group sample is nearly uniform in the larger group.

Let L=SL(A)×SL(B), or SU(A)×SU(B). At the dimensions in use its factors are perfect. We have L≤C_J(t), while C_J(t)/L is abelian by the component determinant maps. Thus

L=L'≤C_J(t)'≤L,

so C_J(t)'=C_J(t)''=L. The same argument identifies the full GL/GU target. This proves the special-group scope rather than inferring it from a paper title.

## How the new proofs fit together

1. The symplectic graph chart uses self-adjoint K=F*F with characteristic polynomial f², with centralizer factors Sp(2,q^d). Its unconditional polynomial mass exceeds q^(−a)/2. A distinguished factor with uniquely largest order 2-part forces the desired negative dimension.
2. The orthogonal graph chart retains both discriminant constraints. Summing its self-adjoint trace-form classes yields |O(A)|/2 operators for each admissible squarefree f; unconditional mass exceeds q^(−a)/8. An exact character-series argument handles all four determinant sectors even at q=3.
3. The replacement theorem proves that 192 independent elements from any prescribed sequence of strong Sp or Ω classes generate the natural group with probability at least 1−q^(−e). Elementary counts rule out every invariant subspace. Burness’s inspected non-subspace fixed-point ratio and Liebeck–Pyber–Shalev’s inspected count of actual maximal subgroups rule out the rest. Perfectness lifts generation from the simple quotient.
4. The bridge splits samples into 192 A-blocks, 192 B-blocks, and one independent extra B-block. First-success selection preserves class-uniformity and independence. It proves C_G(t)'' is exactly the product of the two Sp or Ω factors. A simple-quotient Goursat argument and central-lift check show that a proper subdirect graph has at most two permitted B lifts after fixing the A component of the extra sample. The class-size estimate supplies the final error term.
5. The special-group transfer above joins these new results to the credited GL/GU results.

The [dependency map](DEPENDENCIES.md) identifies exact proof sections, mathematical audits, and published theorem boundaries. The [reader certificate](certificates/CONTROL_CERTIFICATE.md) contains fresh finite reconstructions and explicit false controls. The [source metadata](metadata/SOURCES.json) records public identifiers, hashes, sizes, inspected locations, and current dependency status.

## Historical conditional bridge

The full [original bridge](proofs/GENERATION_BRIDGE.md) and its [original mathematical audit](audits/GENERATION_BRIDGE_AUDIT.md) remain in this reader. They explicitly made the conclusion conditional on CR(Sp,Ω) because the original Praeger–Seress 2011 article had not been retrieved and the inspected restatement did not settle exact Ω scope. That retrieval history remains true.

The [replacement theorem](proofs/CLASS_GENERATION.md), its [independent audit](audits/CLASS_GENERATION_AUDIT.md), and the independent [subspace](proofs/SUBSPACE_LEMMA.md) and [non-subspace](proofs/NON_SUBSPACE_LEMMA.md) lemmas now supply precisely the class input actually used: the closed strong interval [e/3,2e/3] and c=192. They do not claim the broader provisional (1/4,3/4) theorem, and do not retroactively verify PS2011. The former source gate is bypassed as a dependency. The original conditional text is retained to make this replacement visible and auditable.

## Essential limitations and a counterexample

An all-dimensions marginal theorem is false. In Sp₄(q), let t be negative on one symplectic plane A and positive on its perpendicular plane. It is strong. Every inv(t t^g) centralizes t and restricts to an involution in Sp₂(q). In odd characteristic its eigenvalues are ±1; determinant one forces the restriction to be I or −I. A strong restriction on a plane would require one eigenvalue of each sign. Its probability is therefore zero. This refutes the unqualified all-dimensions marginal reading, while leaving the stated asymptotic generation theorem intact.

The [equal-negative-dimensions lemma](proofs/EQUAL_NEGATIVE_DIMENSIONS.md) supplies another genuine boundary: for products of conjugate involutions, the negative dimensions of inv(t t^g) inside the two t-eigenspaces agree. At some dimension ratios, simultaneous strong restrictions are impossible. Separate marginal guarantees are exactly what the bridge uses.

The result excludes characteristic two, projective involutions with order-four lifts, arbitrary similitudes or intermediate groups, and non-natural representations. No total field-operation, bit-operation, exact-order-computation, random-sampler implementation, or complete recognition complexity bound is asserted. A fixed universal multiplier of log n is not claimed to give vanishing failure. External novelty and peer-review status are not certified.
