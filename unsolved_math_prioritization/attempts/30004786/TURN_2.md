# Author turn 2: transport of weak invariant functionals

**A rigorous obstruction to a formal proof from the weak two-functional identity alone. It is not a counterexample to an automorphic L-function conjecture.**

This turn tests whether the actual OWR premise supplies the theta inversion used in turn1. The weakness is structural: in a two-space formulation, an invariant functional can be transported through an invertible equivariant Fourier operator. The resulting identity carries no prescribed theta or boundary normalization.

## 1. Algebraic transport lemma

Let a group H act linearly on vector spaces V and W. Suppose an invertible linear map F:V→W satisfies

F R_a = R_(a^-1) F for every a in H.

Given any nonzero H-invariant linear functional ell on V, define ell_dual=ell composed with F^-1 on W. Then ell_dual is nonzero and H-invariant, and

ell(phi)=ell_dual(F phi)

for every phi in V. Indeed F^-1 R_a=R_(a^-1) F^-1, so invariance follows immediately. This construction is formal and proves no Mellin continuation or asymptotic behavior of a theta sum.

The lemma treats the two functionals as independently chosen, as the displayed weak existential statement does. If a stronger formulation identifies them in a self-dual situation, imposes a canonical family across representations or additive characters, prescribes a distributional support, or normalizes them on a theta subspace, those are extra compatibility conditions. This lemma does not remove such conditions or declare them automatic.

## 2. Fourier covariance in the source normalization

The source's local Mellin transform has exponent s-1/2. With R_a phi(x)=phi(ax), change of variables gives

Z_v(s,R_a phi,chi)=chi(a)^-1 |a|_v^(-s+1/2) Z_v(s,phi,chi).

Use the local functional equation for F_v and compare the Mellin transforms of F_v R_a phi and R_(a^-1) F_v phi. At dual parameter1-s and character chi^-1, the latter translation contributes exactly the same factor chi(a)^-1 |a|_v^(1/2-s). Local Mellin uniqueness, supplied by the cited source theory, therefore gives

F_v R_a=R_(a^-1) F_v.

Tensoring gives the same identity on the adelic Schwartz spaces. It is compatible with, rather than a replacement for, the source's inverse F_(dual pi,psi^-1). In particular it holds on the subgroup k× needed by the OWR invariant-functional statement.

## 3. A nonzero invariant functional already exists in the right half-plane

Under the local and uniform-growth assumptions fixed in turn1, choose a real s0 sufficiently large that the global zeta integral converges absolutely on the prescribed Schwartz space. The local growth estimates and absolute Euler-product bound used in the source's Section5 provide such a right half-plane; no continuation or functional equation is used here.

Define

ell_(s0)(phi)=integral_(A×) phi(x)|x|_A^(s0-1/2) d×x.

For a in k×, the product formula |a|_A=1 makes ell_(s0)(R_a phi)=ell_(s0)(phi). This is an invariant linear functional.

It is nonzero. At exceptional finite places take compactly supported unit functions, and at Archimedean places take nonnegative nonzero compactly supported smooth functions. At almost all finite places take the basic functions. At a sufficiently large real s0 the exceptional Mellin factors are nonzero, and the absolutely convergent unramified Euler product is nonzero. Thus the resulting global evaluation does not vanish.

Transporting ell_(s0) through the inverse Fourier operator now gives a second nonzero k×-invariant functional on the dual Schwartz space satisfying the weak identity. This construction uses only right-half-plane integrals, the product formula, and the local invertible Fourier theory. It does not use a globally automorphic transfer or an analytic continuation of the Euler product.

### Domain and continuity boundary

The displayed construction is defined on the source's algebraic restricted tensor-product Schwartz space, whose elements are finite sums of pure restricted tensors. A fixed sufficiently positive s0 is available from the uniform source growth estimates; no arbitrary completion of that space is used. On this domain the evaluation has the explicit bound

|ell_(s0)(phi)| ≤ p_(s0)(phi), where p_(s0)(phi)=integral_(A×)|phi(x)||x|_A^(s0-1/2)d×x.

Thus it is continuous for this weighted-integral seminorm, and the transported functional is continuous for the pullback seminorm p_(s0)(F^-1 eta). The bare OWR statement does not explicitly demand continuity in a specified alternative completed topology or a prescribed distribution class. No such stronger topological assertion is silently claimed here. If canonical continuous extensions on a particular completion were intended, their compatibility and theta normalization would still require a separate argument.

## 4. Why this is not genuine theta inversion

For any idele x, the orbit of the constructed functional is

ell_(s0)(R_x phi)=|x|_A^(-s0+1/2) ell_(s0)(phi).

This has a single fixed power-law behavior in the norm variable whenever ell_(s0)(phi)≠0. It is generally not the actual theta sum, whose large-norm decay for these source spaces was established in turn1. The equality of transported functionals therefore cannot be substituted into the Mellin integral of Theta without an additional identification.

This also makes the missing normalization visible rather than merely asserting that some estimates are absent. The weak identity admits functionals with orbit behavior unrelated to theta summation. The refinement in the published Conjecture7.4 supplies precisely extra information on a restricted test-function subspace; deriving or assuming that information is a substantive change of premise.

## 5. Logical scope of the obstruction

The transport lemma and the explicit convergent evaluation show that the bare two-functional identity, considered in isolation, is not the analytic theta-inversion input needed in turn1. They do not prove that the automorphic L-function fails continuation, and they do not furnish a counterexample satisfying every global automorphic hypothesis. The original expected implication might be true for reasons using that additional global structure, or with the intended canonical/refined meaning of Poisson summation.

Accordingly this is a formulation and proof-route obstruction, not a false claim that the Langlands conjecture has been refuted or proved. Two substantive author turns are complete; the weak-premise source target remains unresolved. Completion estimate30%. Next: work out precisely what the published refinement actually supplies, including Fourier/translation stability of its two-place subspace, without importing an unstated canonical boundary expansion.
