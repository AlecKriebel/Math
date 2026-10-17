**Integrated reader status.** Accepted replacement class-generation theorem. It discharges the precise input used by the retained bridge with c=192. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# A verified replacement for the balanced-involution class-generation input

13 October 2026. This is an authored mathematical deduction from two inspected primary-source theorems, with an elementary treatment of all subspace obstructions. It does not require the uninspected Praeger–Seress 2011 article or a correction to its later summaries.

## 1. Exact theorem needed by the Bray bridge

There is an absolute integer d₀ such that the following holds for every odd prime power q.

Let V be an e-dimensional nondegenerate symplectic or quadratic space, e≥d₀, and set

- J=Sp(V) in the symplectic case; or
- J=Ω(V) in the orthogonal case, including odd dimension and both even-dimensional form types.

Prescribe any sequence C₁,…,C₁₉₂ of J-conjugacy classes of natural involutions x for which both eigenspaces have dimensions in the closed interval [e/3,2e/3]. Independently choose xᵢ uniformly in Cᵢ. Then

  P(⟨x₁,…,x₁₉₂⟩=J) ≥ 1−q^(−e).                              (1)

These are genuine order-two matrices in J. No assertion about arbitrary projective involutions with order-four lifts is made. The classes need not be equal. All constants are uniform in q, e, the form type, and the prescribed class sequence.

This theorem is slightly narrower in balance range than CR in Section 2 of the accepted generation bridge, and exactly sufficient there: every selected component is strong in this closed sense. Replace that section's CR by (1), and take its c to be 192. No endpoint convention is imported from the old source.

## 2. The two published inputs and their precise scope

**Non-subspace fixed-point ratios.** Burness, *Fixed point ratios in actions of finite classical groups, I*, Theorem 1 and Corollary 1, gives, for a simple classical group S in a faithful coset action on S/M with M maximal and non-subspace,

  fpr(y,S/M) < |y^S|^(−1/2+1/e+ι)

for prime-order y. For PSpₑ(q), PΩₑ^±(q), and Ωₑ(q) in the present range, 0≤ι≤1/(e−2). His dimension parameter is the natural dimension here. Definition 1 says that a subspace maximal subgroup, in these odd-characteristic families, stabilizes a proper nonzero totally singular or nondegenerate subspace. The characteristic-two alternatives do not apply. Theorem, exceptions, and definitions were read and rendered in the author manuscript, pp.2–3. [Author PDF](https://seis.bristol.ac.uk/~tb13602/docs/fpr1.pdf); [DOI](https://doi.org/10.1016/j.jalgebra.2006.05.024).

**Number of maximal subgroups.** Liebeck–Pyber–Shalev, *On a conjecture of G. E. Wall*, Theorem 1.1, bounds the number of actual maximal subgroups of a finite almost simple group G with Lie-type socle of rank r by C r^(−2/3)|G|, for an absolute C. In this application G=S is simple, giving the bound C r^(−2/3)|S|. The statement was read and rendered on author-manuscript p.2. [Author PDF](https://www.ma.imperial.ac.uk/~mwl/WALL.PDF).

These two inputs explicitly have the projective/simple orthogonal scope needed below. The natural groups' perfectness and simplicity modulo center at our dimensions are the already-inspected classical-group facts used by the accepted bridge (Taylor, Theorems 8.7–8.8 and 11.45–11.48). Neither a generalized-Fitting convention nor an assertion that SO itself is generated is used.

## 3. Elementary counts for subspaces

Put D=Sp(V) or O(V). The following estimates hold uniformly for q≥3. Zero-dimensional component spaces in a product contribute one.

### 3.1 Nondegenerate subspaces

For any prescribed existing isometry type of nondegenerate k-space W in an e-space, with 0<k<e, orbit–stabilizer gives

  N(e,k,type)=|D(V)|/(|D(W)|·|D(W⊥)|).

For Sp, write |Sp_d(q)|=q^(d(d+1)/2)ψ_(d/2), where 7/8≤ψ≤1. For O in positive dimension d, write |O_d(q)|=q^(d(d−1)/2)η_d, where 7/6≤η_d≤8/3. These follow directly from the usual order products; ∏_{j≥1}(1−q^(−2j))≥1−Σ_{j≥1}q^(−2j)≥7/8. The orthogonal products are 2ψ in odd dimension and 2(1−εq^(−d/2))ψ in even dimension.

Consequently each existing nondegenerate-subspace type satisfies the convenient common bounds

  (21/128)q^(k(e−k)) ≤ N(e,k,type) ≤ 2q^(k(e−k)).             (2)

There is at most one type for Sp and at most two for O. Formula (2), with its loose constants, also bounds the count one when k=0 or k=e and the type is possible.

### 3.2 Totally singular subspaces

Let T(e,k) count all totally singular k-spaces, and only consider k for which such spaces exist. In the symplectic case this means totally isotropic spaces. Define

  Fσ(e,k)=ke−(3k²+σk)/2,
  σ=−1 for Sp, and σ=+1 for O.

Then

  (1/2)q^Fσ(e,k) ≤ T(e,k) ≤ 8q^Fσ(e,k).                    (3)

Here is a direct product proof. Let N_d be the number of nonzero singular vectors in a nondegenerate residual d-space. Counting ordered bases of a singular k-space successively, then dividing by the number of ordered bases of a k-space, gives

  T(e,k)=∏_{j=0}^{k−1} N_(e−2j)/(q^(k−j)−1).

Indeed, after j singular basis vectors have been chosen, a nonzero singular vector in the residual quotient lifts to q^j eligible vectors, while the corresponding factor in |GL_k(q)| contributes q^j(q^(k−j)−1). The q^j factors cancel. The residual quadratic form is obtained by removing j hyperbolic planes, so the even-dimensional sign remains fixed.

The singular-vector counts are

  N_d=q^d−1                                      (Sp),
  N_d=q^(d−1)−1                                  (O, d odd),
  N_(2m)=(q^(m−1)+ε)(q^m−ε)                      (O, sign ε).

Extracting the leading powers gives exactly Fσ. The denominator's normalized product is ∏_{h=1}^k(1−q^(−h)), strictly greater than or equal to 1/2 and at most one. The normalized numerator is at least 7/8 for Sp and odd O, and at least 1/2 for even O: its negative factors have distinct positive exponents. Its positive factors are bounded by

  ∏_{h=0}^∞(1+q^(−h)) ≤ 2exp(1/(q−1)) < 4.

Thus numerator/denominator lies between 1/2 and 8, proving (3). Products are empty for k=0. A zero factor corresponds to an impossible k and is never used as a positive denominator.

## 4. Excluding every invariant subspace

Let x be any one of the prescribed strong involutions. Write V=A⊥B for its eigenspaces, with dimensions a,b≥e/3. Since q is odd, an x-invariant W splits as W=(W∩A)⊕(W∩B). Put i=dim(W∩A), j=dim(W∩B), and k=i+j.

If W is nondegenerate, both summands are nondegenerate. For each i, there are at most two types in each eigenspace. Applying the upper bound (2) in A and B and summing gives at most

  16(k+1) q^max[i(a−i)+j(b−j)]

x-invariant nondegenerate k-spaces. The dimension loss relative to k(e−k) is

  Δ=ib+ja−2ij ≥ ek/3−k²/2 ≥ ek/12,                        (4)

provided k≤e/2. Dividing by the lower bound in (2) proves that the proportion fixed in any D-orbit of a fixed nondegenerate type is at most

  100(k+1)q^(−ek/12).

If W is totally singular, both summands are totally singular, with i≤a/2 and j≤b/2. From (3), there are at most

  64(k+1)q^max[Fσ(a,i)+Fσ(b,j)]

invariant totally singular k-spaces. The loss relative to Fσ(e,k) is

  Δ=ib+ja−3ij.

Since ib+ja≥4ij, one has Δ≥(ib+ja)/4≥ek/12. Division by (3) yields the common bound

  P(x fixes a specified W) ≤128(k+1)q^(−ek/12).             (5)

The probability in (5) is for x uniformly chosen in any strong J-class. In Sp it is immediately the D-orbit fixed-point ratio. In Ω, each such J-class is also a full O-class. To verify this, the centralizer O(A)×O(B) contains reflections with square and nonsquare spinor norm, because a nondegenerate space of dimension at least three contains a hyperbolic plane and represents every nonzero scalar. Their determinant/spinor pairs generate O/Ω. Thus O=Ω C_O(x), and the two classes coincide. Uniform J-class sampling therefore gives exactly the full-O orbit ratio for any fixed W, even when the action on subspaces has more than one Ω-orbit. No nonsplitting assertion about subspace orbits is required.

There are at most 12q^(ek) relevant k-spaces in total, by (2) and (3). A nonzero proper degenerate invariant subspace has a nonzero totally singular invariant radical; a nondegenerate invariant subspace of dimension exceeding e/2 may be replaced by its orthogonal complement. Thus a reducible group fixes one of the subspaces counted for 1≤k≤⌊e/2⌋.

For 192 independent representatives from arbitrary prescribed strong classes, (5), independence, and the union bound give

  P(⟨x₁,…,x₁₉₂⟩ is reducible)
  ≤12Σ_{k=1}^{⌊e/2⌋} q^(ek)[128(k+1)q^(−ek/12)]^192.       (6)

For e≥384, k+1≤2^k implies

  128(k+1)≤256^k≤3^(8k)≤q^(ek/48).

Hence (6) is at most

  12Σ_{k≥1}q^(−11ek) <13q^(−11e) <(1/2)q^(−e).            (7)

This is uniform in the entire class sequence. In particular, every subspace maximal subgroup is excluded except with probability (7).

## 5. Excluding all non-subspace maximal subgroups

Put S=J/Z(J). For e≥384 it is nonabelian simple and |Z(J)|≤2. A strong x is noncentral, so its image x̄ has order two. The natural class-size computation in the accepted bridge, or the order ratios in Section 3.1, gives

  |x^J|≥(21/128)q^(ab),

where ab≥2e²/9. In Sp the stronger factor 7/8 is available. The class projection x^J→x̄^S is surjective with equal fibers of size at most two. Therefore

  |x̄^S|≥(21/256)q^(2e²/9)≥q^(e²/5)                       (8)

for e≥16. This accounts explicitly for both possible central lifts.

For e≥16, 1/e+1/(e−2)≤1/6. Applying Burness's theorem to the faithful transitive action S/M for each non-subspace maximal M, and then (8), gives

  |x̄^S∩M|/|x̄^S| ≤ q^(−e²/15).

Projecting independent uniform natural-class samples produces independent uniform projective-class samples. Thus the probability all 192 images lie in a specified M is at most q^(−192e²/15).

The number of actual maximal subgroups is at most C|S|<Cq^(e²), using the second published input and S as a quotient of a subgroup of GL_e(q). A union bound yields

  P(all images lie in some non-subspace maximal M)
  ≤ Cq^(−59e²/5).                                          (9)

Choose, for example, the absolute threshold

  d₀=ceil(max{384, sqrt(log₃(2max{1,C}))}).

For e≥d₀, C≤q^(e²)/2, so (9) is at most (1/2)q^(−54e²/5)≤(1/2)q^(−e). A numerical value of the published absolute C, and thus of this d₀, is not asserted.

## 6. Generation in the natural group

If the projective image of K=⟨x₁,…,x₁₉₂⟩ is proper in S, it lies in a maximal subgroup. By Burness's exact definition, that maximal is either subspace or non-subspace. The first event implies a natural invariant subspace and is covered by (7); the second is covered by (9). Their sum is at most q^(−e).

If the image is all S, then KZ(J)=J. Since J is perfect and Z(J) is central,

  J=(KZ(J))'=K'≤K.

Therefore K=J. This proves (1) with no loss of probability, and handles the central covering group rather than merely its simple quotient.

## 7. Substitution into the accepted Bray reduction

For the natural ambient groups G=Sp(V), O(V), SO(V), or Ω(V), with odd q and a strong involution t, all sampling and direct-product arguments already audited in the generation bridge remain unchanged. Its selected component classes satisfy exactly the hypotheses of (1). With a=dim E₋(t), b=dim E₊(t), take

  κ=1/40000 for Sp,
  κ=1/10000000 for O, SO, Ω,
  L=ceil(κ^(−1)log n · log(385/η)),
  M=385L,

where 0<η<1. Require n≥max(49152,3d₀) for Sp and n≥max(98304,3d₀) for the orthogonal families. The same proof now gives, without the old source qualification,

  P(⟨inv(tt^(g₁)),…,inv(tt^(g_M))⟩≥C_G(t)'')
  ≥1−η−q^(−a)−q^(−b)−13q^(−2b²/9).

Here the gᵢ are independent uniform samples in the exact ambient matrix group G, and inv(y)=1 for odd order and y^(|y|/2) otherwise. The accepted bridge proves C_G(t)''=Sp(A)×Sp(B) or Ω(A)×Ω(B), and uses an additional independent output to exclude a proper subdirect product. Surjective projections alone are not being treated as product containment.

For fixed η=1/20 the success probability exceeds 0.9 at these thresholds. Repeating independently ceil(log(1/δ)/log 10) times and retaining all outputs gives confidence at least 1−δ with O(log n·(1+log(1/δ))) samples. For fixed confidence this is O(log n). This is a sample-count theorem, not a bound on field operations, bit complexity, exact-order computation, or uniform-sampler implementation. No numerical overall dimension cutoff is claimed because C above was not numerically specified.

## 8. Scope and documentary boundary

This result closes the generation input needed by the existing large-dimensional natural Sp/O/SO/Ω reduction. It does not resolve low-dimensional exceptional groups, arbitrary intermediate or similitude groups, projective involutions without natural order-two lifts, or non-natural representations. It does not claim to retrieve, repair, or verify the exact original PS2011 theorem.

The later Dixon–Praeger–Seress author manuscript, *Strong involutions in finite special linear groups of odd characteristic*, pp.2–4, was also inspected. Its explicit SO wording cannot be used literally: balanced classes contained in Ω cannot generate all SO. That source is neither an input nor a premise of this proof.

All source PDFs, extracted text, and page renders remain private inspection evidence. The public-safe work consists of this authored deduction, its mathematical audit, and verified public source metadata. Byte hashes establish source identity, not mathematical validity.
