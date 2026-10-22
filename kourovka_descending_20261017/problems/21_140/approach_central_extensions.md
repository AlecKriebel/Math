# 21.140: central extensions preserve a copy of Thompson's F

Status at 2026-10-17 21:27:48 UTC: **locally verified partial theorem, pending parent-level adversarial review; no novelty claim**. Estimated completion of this narrow central-extension obstruction: **95%**. Estimated completion of Kourovka 21.140 itself: **5%**; this is a restriction on possible constructions, not a solution.

## Exact claim and scope

**Proposition.** There is an injective homomorphism `j:F→F` such that `H₂(j;Z)=0`. Consequently, for every central extension

`1 → A → E → F → 1`

with arbitrary kernel A, the group E contains a subgroup isomorphic to F. More generally, if a group G contains F, every central extension of G contains F.

Here F is the group of orientation-preserving, dyadic, piecewise linear homeomorphisms of [0,1] with slopes powers of 2. Products mean `(gh)(x)=g(h(x))`. The kernel of a central extension is automatically abelian. No finite generation, countability, divisibility, or torsion restriction is imposed on A.

This does **not** prove that an arbitrary extension of a group containing F contains F. It does not settle 21.140 or claim any novelty. It rules out a proposed F-avoidance mechanism using only a central kernel.

## Imported theorem, and what is derived here

The sole imported non-elementary homological fact is

`H₁(F;Z) ≅ Z²` and `H₂(F;Z) ≅ Z²`,

with the abelianization given by the two endpoint log-slopes. These facts are stated and explained in Kenneth S. Brown, *The homology of Richard Thompson's group F*, arXiv:math/0411347 (2004), introduction and §§1.4–1.5:

- https://arxiv.org/html/math/0411347
- Author-hosted source: https://pi.math.cornell.edu/~kbrown/papers/homology.pdf
- Local copy: `central_extensions/brown_homology_2004.pdf`.

The integer cocycle below is the displayed discrete Godbillon–Vey cocycle in Louis Funar and Vlad Sergiescu, *Central extensions of the Ptolemy-Thompson group and quantized Teichmüller theory*, arXiv:0802.2996v2, §4.2, Lemma 4.1 (published J. Topology 3 (2010), 29–62; DOI 10.1112/jtopol/jtp033):

- https://arxiv.org/html/0802.2996v2
- Local copy: `central_extensions/funar_sergiescu_0802.2996v2.html`.

A short direct verification of the cocycle identity is included below, so no normalization or basis claim concerning this cocycle is imported. In particular, the proof does not require any theorem about the cohomology of F′.

## 1. A circle cocycle with an explicit convention

Identify 0 and 1 to form the oriented circle. For g∈F let

`b_g(x)=log₂(g′_r(x))`,  `Δb_g(x)=log₂(g′_r(x))−log₂(g′_l(x))`.

At the circle point 0, the left derivative is the derivative at `1−`; it is not set to 1. All b-functions are integer-valued right-continuous step functions with finitely many jumps.

For two such step functions define

`P(u,v)=Σ_{x∈S¹} (u(x)Δv(x)−v(x)Δu(x))`.

Only finitely many terms are nonzero. P is bilinear, alternating, and invariant under simultaneous precomposition by any orientation-preserving circle homeomorphism h:

`P(u∘h,v∘h)=P(u,v)`.

Indeed `Δ(u∘h)(x)=Δu(h(x))`, and h bijects the finite sets of discontinuities. The chain rule gives `b_{gh}=b_g∘h+b_h`. Put

`C(g,h)=P(b_h,b_{gh})=P(b_h,b_g∘h)`.

Expanding by this chain rule and using the invariance of P gives

`C(g,h)−C(fg,h)+C(f,gh)−C(f,g)=0`.

Thus C is an integer 2-cocycle, independently of the cited identification with a Godbillon–Vey class. Written as determinants, it is

`C(g,h)=Σ_x det [[b_h(x),b_{gh}(x)],[Δb_h(x),Δb_{gh}(x)]]`.

## 2. C and the endpoint cup class span rational H²

Define homomorphisms

`λ(g)=log₂g′(0+)`,  `ρ(g)=log₂g′(1−)`.

Let B denote the cup-product 2-cocycle `B(g,h)=λ(g)ρ(h)`. We give two commuting-pair bar cycles on which B and C have an invertible evaluation matrix. For commuting f,g, the normalized bar chain `[f|g]−[g|f]` is a 2-cycle, since its boundary is `[g]−[fg]+[f]−([f]−[gf]+[g])=0`.

Let a be the standard F element

```
a(x)=x/2       for 0≤x≤1/2,
a(x)=x−1/4     for 1/2≤x≤3/4,
a(x)=2x−1      for 3/4≤x≤1.
```

For a dyadic interval I=[s,t] whose length is a power of 2, write `a_I` for the affine rescaling of a to I, extended by the identity outside I. The rescaling is an element of F.

First take `f=a_[0,1/4]`, `g=a_[3/4,1]`. They commute, and for `z_end=[f|g]−[g|f]` we have

`⟨B,z_end⟩=(-1)(1)−(0)(0)=−1`.

The value of C on this cycle is −2; this value is not needed for independence but is recorded to make the circle endpoint contribution explicit.

Second take `p=a_[1/4,1/2]`, `q=a_[1/2,3/4]`. They commute because they preserve their respective intervals and are identity outside; the shared endpoint is fixed by both. Both have λ=ρ=0. For `z_int=[p|q]−[q|p]`, we have `⟨B,z_int⟩=0`.

Only the common endpoint x=1/2 can contribute to `⟨C,z_int⟩`. At that point

`b_p=0, Δb_p=−1`,  `b_q=−1, Δb_q=−1`,

and, because p and q have disjoint support interiors,

`b_{pq}=−1, Δb_{pq}=−2`.

Thus the determinant is 1 for C(p,q) and −1 for C(q,p), giving

`⟨C,z_int⟩=2`.

At any other point, either both maps are locally identity or only one of them has a nontrivial derivative or jump. Then the determinant defining each of C(p,q), C(q,p) is zero. In particular, both maps are identity near the circle point 0.

The evaluation matrix is therefore

```
                z_end    z_int
B                 −1        0
C                 −2        2
```

with determinant −2. Hence [B] and [C] are linearly independent over Q. Since Brown's theorem gives `dim_Q H²(F;Q)=2`, these two classes span rational H². This avoids any integral-normalization claim.

## 3. Reflection changes the sign exactly

Let r(x)=1−x and `R(g)=rgr`. The map R is an automorphism of F, although r itself reverses orientation. Let y=r(x). One-sided derivatives interchange:

`b_{R(g)}(x)=b_g(y)−Δb_g(y)`,  `Δb_{R(g)}(x)=−Δb_g(y)`.

Also `R(g)R(h)=R(gh)`. Each determinant defining `C(R(g),R(h))` is therefore obtained from the determinant for C(g,h) by replacing its first row u with `u−v` and its second row v with `−v`. Its value is `−det(u,v)`. The bijection x↔r(x) gives the cochain identity

`C(R(g),R(h))=−C(g,h)`.

This argument includes endpoints: r acts on the circle, and the convention for left derivative at 0 was fixed above.

## 4. A mirrored pair of separated interior clones

Let `I=[1/8,3/8]`. For f∈F define k(f) as its affine clone on I, extended by the identity. This is an injective homomorphism F→F. Its reflected interval is `r(I)=[5/8,7/8]`, separated from I by an open interval. Define

`j(f)=k(f) R(k(f))`.

The two factors commute, because their support closures lie in the separated intervals I and r(I). Consequently j is a homomorphism. Its restriction to I is k(f), so it is injective. Both factors are identity near 0 and 1, so `λ(j(f))=ρ(j(f))=0` and `j*B=0` as a 2-cochain.

The determinant defining C is local. For maps supported in I and r(I), each point has a neighborhood meeting at most one of those closed intervals. On the neighborhood of I, all right/left derivative data of `j(g),j(h),j(gh)` agree with those of `k(g),k(h),k(gh)`. The analogous statement holds on r(I), while every term outside these neighborhoods is zero. Thus

`C(j(g),j(h)) = C(k(g),k(h)) + C(R(k(g)),R(k(h))) = 0`.

The interval endpoints cause no cross-terms because there is a positive gap between the closed intervals. It is not necessary to identify `C(k(g),k(h))` with C(g,h); cloning may alter endpoint terms, and the argument makes no such assumption.

Thus `j*[B]=j*[C]=0`. Since these classes span rational H², the induced map on rational H² is zero, and hence the map on rational H₂ is zero. Brown's theorem gives torsion-free `H₂(F;Z)=Z²`, so the integral map `H₂(j;Z)` is zero as well. Equivalently, for any integral homology class z, [B] and [C] annihilate j_*z; their rational independence forces `j_*z⊗1=0`, and torsion-freeness forces `j_*z=0`.

## 5. Arbitrary central kernels

For an arbitrary abelian group A with trivial F action, the universal coefficient theorem gives a natural exact sequence

`0 → Ext¹_Z(H₁(F;Z),A) → H²(F;A) → Hom_Z(H₂(F;Z),A) → 0`.

Because `H₁(F;Z)=Z²` is free, the Ext term vanishes for every A. The evaluation arrow is therefore a natural isomorphism. Pullback by j corresponds under that isomorphism to precomposition by `H₂(j;Z)=0`. It follows that

`j*:H²(F;A)→H²(F;A)` is zero for every A.

A central extension with kernel A represents a class e∈H²(F;A). Its pullback along j has class j*e=0 and therefore splits. Composing a splitting with the map from the pullback group to E gives a homomorphism `s:F→E` satisfying `πs=j`. Since j is injective, s is injective. This proves the proposition.

For a central extension of an ambient group G containing a subgroup F₀≅F, restrict the extension to `π⁻¹(F₀)`. This is a central extension of F₀ by the same kernel, so the proposition supplies the required F subgroup.

## Validation and limitations

`central_extensions/verify_pl_gv.py` implements all maps as rational piecewise linear maps using `fractions.Fraction`, with no floating-point arithmetic. The recorded run in `central_extensions/verification_results.json` checks the two witness evaluations and 300 seeded random instances each of the cocycle, reflection, separated-clone additivity, mirrored zero, and homomorphism identities on 57 sample maps. These finite computations support, and do not replace, the universal proofs above. The sole deep imported theorem remains Brown's integral homology calculation.

A convention discrepancy in Funar–Sergiescu's displayed Lemma 4.1 computation is quarantined in `central_extensions/source_convention_note.md`; the argument here does not depend on that computation, on their cycle normalization, or on any claimed basis for H².

Remaining audit tasks: independently inspect the full proof, especially naturality for arbitrary coefficient A and the boundary-safe local additivity argument; check whether this central-extension preservation result is already in the literature before making any novelty claim. No outreach was prepared or initiated. No release, commit, push, or publication was performed by this subagent.
