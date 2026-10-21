# Independent adversarial review: central extensions and Thompson's F

Checkpoint: 2026-10-17 21:32 UTC. Reviewer: fresh adversarial subagent, independent of the candidate author. Bounded proof-audit completion estimate: **100%**. The narrow central-extension claim is **accepted conditional on the cited standard homology theorem**. Estimated completion of Kourovka 21.140 itself remains **5%**; no full solution, originality, priority, or publication claim is made.

## Claim reviewed and verdict

The candidate constructs a monomorphism `j:F→F` with `H₂(j;Z)=0`, then concludes that every central extension of a group containing an abstract copy of F also contains an abstract copy of F, with no restriction on the central kernel.

**Verdict: I found no mathematical gap in this narrow claim.** In particular, the determinant −2 in the witness matrix is used only for a rational span, not as an integral-basis claim. The subsequent passage through torsion-free integral H₂ and the natural universal coefficient evaluation map is sufficient for arbitrary abelian coefficients, including 2-torsion, other torsion, divisible, and noncountable groups.

This review accepts the central-extension obstruction only. It does not validate arbitrary extensions or exclude extensions with general noncentral kernels. The outer-automorphism corollary discussed below is a separate, conditional consequence.

## Sources checked directly

1. [Kenneth S. Brown, *The Homology of Richard Thompson's Group F*](https://arxiv.org/html/math/0411347), introduction and §§1.4–1.5: the integral homology is free abelian of rank 2 in each positive degree; the endpoint logarithmic slopes give the abelianization. These are the homological facts actually needed. Section 1.5 also records simplicity of F′, used only for the separate outer-automorphism corollary below.
2. [Funar–Sergiescu, arXiv:0802.2996v2, §4.2, Lemma 4.1](https://arxiv.org/html/0802.2996v2): the displayed determinant formula agrees with the candidate's formula. I do **not** import the source's asserted pairing with its η cycle or its normalization of the discrete Godbillon–Vey class. The source-convention discrepancy is reproduced below and remains quarantined.
3. [Hatcher, *Algebraic Topology*, §3.1, Theorem 3.2 and the naturality discussion, printed pp. 195–196](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf): the cohomology universal coefficient sequence for a free abelian chain complex applies to any abelian coefficient group; its evaluation map is natural even though a general splitting is not. No general splitting is selected in the candidate.

The universal proof below also establishes the cocycle identity directly, so identifying this cocycle with a named cohomology class is unnecessary.

## Universal checks, independent of the numerical output

### Cocycle identity and the circle point

Use the right-continuous integer step function `b_g=log₂(g′_r)` on the circle, with the left derivative at 0 taken from `1−`. For orientation-preserving h, precomposition transports both right values and jumps: `Δ(u∘h)(x)=Δu(h(x))`. Therefore the bilinear alternating form

`P(u,v)=Σ(u Δv−v Δu)`

is invariant under simultaneous precomposition by h. The one-sided chain rule gives `b_gh=b_g∘h+b_h`, including at 0. Hence

`C(g,h)=P(b_h,b_g∘h)`.

Expansion of the candidate's cocycle differential leaves precisely

`P(b_g∘h,b_f∘gh)−P(b_g,b_f∘g)=0`.

No differentiability at a breakpoint is assumed: the right and left chain rules are applied separately. The circle point 0 is a genuine jump location, not a deleted endpoint.

At that point the determinant contribution is

`C₀(g,h)=λ(g)ρ(h)−λ(h)ρ(g)`.

This formula agrees with the candidate's convention note. Deleting the circle point changes the cocycle, and is not silently interchangeable with the circle convention.

### Two witness cycles

The candidate's commuting maps have disjoint support interiors and preserve their intervals, so they commute even when their support closures meet at a fixed endpoint. Their bar chains `[f|g]−[g|f]` are actual cycles.

For the separated endpoint witnesses, the only nonzero determinant term is at the circle point 0. Directly, `C(f,g)=−1`, `C(g,f)=1`, and the cup pairing is −1.

For the adjacent interior witnesses p and q, the only nonzero term is at `x=1/2`. The right values and jumps are `(b_p,Δb_p)=(0,−1)`, `(b_q,Δb_q)=(−1,−1)`, and `(b_pq,Δb_pq)=(−1,−2)`. The two determinants are 1 and −1. Both endpoint characters vanish. Thus the evaluation matrix is exactly

```
          endpoint cycle   interior cycle
cup             −1               0
C               −2               2
```

Its determinant −2 proves rational independence. Since rational H² has dimension 2 by Brown's integral homology calculation and the universal coefficient theorem, these classes form a rational basis. No assertion of an integral basis is justified by this matrix, and none is needed.

### Reflection sign

For `R(g)=rgr`, `r(x)=1−x`, reflection interchanges the one-sided derivatives. If `y=r(x)`, then

`b_Rg(x)=b_g(y)−Δb_g(y)`, `Δb_Rg(x)=−Δb_g(y)`.

For each determinant the pair of rows `(u,v)` becomes `(u−v,−v)`, whose determinant is `−det(u,v)`. Reindexing the finite sum by r is a bijection of circle points. Thus `C(Rg,Rh)=−C(g,h)` exactly as a cochain identity. At 0 this uses the same circle convention; there is no exceptional unaccounted term.

### Cloning and support boundaries

The affine clone on `[1/8,3/8]` lies in F: its breakpoints and images stay dyadic, and affine conjugation preserves all slopes. Restriction to that interval recovers the original map, so cloning is injective. Its reflected clone is supported in `[5/8,7/8]`. The positive gap makes all cross-factor commutators trivial.

Consequently `j(f)=k(f)R(k(f))` is an injective homomorphism. It is identity near both global endpoints, so the endpoint cup cocycle pulls back to zero. At a point of either clone interval, including its boundary, the other clone is identity on an open neighborhood. All left/right derivative data there therefore agree with the appropriate single clone. Outside the two intervals all data are zero. The determinant sum splits locally into two summands and reflection cancels them.

This is a direct cochain-locality argument. It does not discard an `H₁⊗H₁` Künneth term. Indeed an interior clone can alter the original circle cocycle by endpoint terms; the proof correctly never assumes `C(kf,kg)=C(f,g)`.

### Integral homology and arbitrary kernels

The preceding identities give `j*[cup]=j*[C]=0`. Rational duality then gives `H₂(j;Q)=0`. Naturality of rationalization gives `H₂(j;Z)⊗Q=0`; every value of the integral map is therefore torsion in the target. Brown's target `H₂(F;Z)=Z²` is torsion-free, so the integral map itself is zero. The target's torsion-freeness is the necessary ingredient here.

For an arbitrary abelian A, centrality gives the trivial F action. Since `H₁(F;Z)=Z²`, `Ext¹(H₁(F;Z),A)=0`. The **evaluation map itself**, not a chosen universal coefficient splitting, is a natural isomorphism

`H²(F;A) → Hom(H₂(F;Z),A)`.

Naturality makes `j*` correspond to precomposition by the zero integral H₂ map, hence `j*=0` for this A. A separate subagent audited this coefficient step without reading the candidate and reached the same conclusion.

For completeness the splitting implication can be seen directly. Choose lifts `t(x)` of elements of F and write `t(x)t(y)=e(x,y)t(xy)` with additive central kernel A. Vanishing of the pulled-back class gives a cochain u with `e(jf,jg)=u(f)+u(g)−u(fg)`. Then `s(f)=−u(f)t(jf)` is a homomorphism into E and `πs=j`. Thus `ker(s)⊂ker(j)=1`. This proves an embedded F without claiming that the original extension splits over all of F. Restricting an ambient group's extension to its given F subgroup proves the ambient assertion.

## Exact computations and independent negative control

The candidate's command `python3 central_extensions/verify_pl_gv.py` completed successfully and reproduced the recorded JSON exactly: 300 checks of each stated identity, the witness matrix above, and source-cycle alternating values 0 and −2.

The separate [independent checker](central_adversary01_check.py) imports no candidate code. It represents a map as a word of elementary PL atoms and evaluates derivatives by the chain rule; it does not construct composed vertex graphs. It evaluates `P(b_h,b_g∘h)` directly rather than the candidate's determinant involving a composed map. All arithmetic uses rational fractions. Its [recorded output](central_adversary01_results.json) includes:

- The endpoint witness's sole nonzero terms at 0, equal to −1 and 1.
- The interior witness's sole nonzero terms at 1/2, equal to 1 and −1.
- 140 seeded instances each of the cocycle, reflection, local additivity, mirrored vanishing, homomorphism, and reflected one-sided derivative identities on 27 sample entries.
- A negative control: duplicating two separated clones **without** reflection gives alternating pairing 4 on the interior witness, so merely placing copies in disjoint intervals does not falsely pass cancellation.
- Independent source-cycle alternating values 0 and −2 with the circle convention, matching the quarantine note. These values are not used to establish the claim.

These finite checks are corroboration; the universal deductions above are the proof. I found no inconsistency between the code, written argument, and stated scope.

## Additional root-proposed outer-automorphism corollary

The following implication is valid using the accepted central theorem and the standard simplicity of F′:

> If `1→N→E→Q→1`, Q contains F, and `Out(N)` contains no F, then E contains F.

Restrict Q to F and let `θ:F→Out(N)` be the induced outer conjugation action. The restriction to simple F′ has either trivial kernel or all of F′ as kernel. The injective alternative would embed F′ in `Out(N)`, and an interior clone embeds F in F′, contradicting the hypothesis. Thus `θ(F′)=1`.

For every `f∈F′`, choose a lift e. Its conjugation on N is inner, so for some `n∈N` the element `n⁻¹e` centralizes N and still maps to f. Therefore `D=C_E(N)∩π⁻¹(F′)` maps onto F′. Its kernel is exactly `N∩C_E(N)=Z(N)`. That kernel is central in D because every element of D centralizes all of N. Pulling back to an interior clone `F₀⊂F′` gives a central extension of F₀, to which the preceding theorem applies. There is no circular use of the conclusion for general N.

The advertised special cases are valid. Finite N has finite `Out(N)`. For finitely generated abelian N, `Out(N)=Aut(N)` is residually finite: the actions on the finite characteristic quotients `N/mN` separate distinct automorphisms because `∩_{m≥1}mN=0`. A residually finite group cannot contain F, since the infinite simple F′ has no nontrivial finite quotient and hence is not residually finite. This covers the zero-rank and torsion cases as well.

## Audit history, limitations, and snapshot

- 21:30 UTC checkpoint: the candidate replay and independent algebra checks passed; bounded audit estimate 70%, full 21.140 estimate 5%.
- 21:31 UTC checkpoint: the independent word implementation and negative control passed; bounded audit estimate 90%, full problem estimate 5%.
- 21:32 UTC checkpoint: arbitrary coefficients, injectivity after splitting, and the separate outer-action argument accepted; bounded audit estimate 100%, full problem estimate 5%.

No novelty search was attempted. No individual was contacted, no outreach was prepared, and no Git, PR, queue, commit, push, or publication operation was performed by this reviewer. The Funar–Sergiescu normalization discrepancy remains unresolved and is not promoted as a correction to that paper.

Reviewed candidate SHA-256 values:

```
95baa08c84c37938994d939da23d050c0692257ac15bd2525f0532a2d27463fe  approach_central_extensions.md
5b49b6a7de2eca23752f47ae3035f62dd6484ad79054f7af36ce7872fb178d75  central_extensions/verify_pl_gv.py
9b825ae293ad0b669d8b7f5a0fac95457ef6e1a1fef93402b18e3ac2105e1950  central_extensions/verification_results.json
7aaa75302d859f5d30f2e375cd52062fe0f18c2bc9b18670739ec1b3f18e2130  central_extensions/source_convention_note.md
```
