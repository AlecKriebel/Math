# An older Banach-lattice mechanism for the full measurable-fiber assertion

Status: narrowed route independently verified 2026-10-01 13:34 UTC; audit complete. This is a mathematical priority certificate for an equivalent mechanism, not a claim that the old authors explicitly stated the present composition-operator corollary.

## Primary theorem inputs and their inspected scope

**K20:** A. K. Kitover and M. Orhon, *Spectrum of Weighted Composition Operators Part VI: Essential spectra of d-endomorphisms of Banach C(K)-modules*, arXiv:2009.09303v2, version dated 2020-12-19. Official version-pinned full text: <https://arxiv.org/html/2009.09303v2>.

1. Section 2.2, Definition 2.3: a Kaplansky module is a faithful isometric Banach `C(K)` module with `K` extremally disconnected, for which the annihilator of each vector is a band. Proposition 2.5 supplies weak-operator closure of the multiplier algebra.
2. Only the one-direction inclusion `sigma_ap(C) subset sigma_ap(S)` for the concrete coordinate shift is needed. Theorem 5.4 states it, and the disjoint-orbit construction in proof 5.2, case (3a), supplies a mechanism for it. The narrowed certificate independently checks this direction. It does **not** rely on full spectrum equality or on reverse approximate-spectrum transfer; a broader source-proof issue is recorded below.
3. Theorem 2.26 states the following result and attributes it to [Kitover 2011, Theorem 3.29]. For aperiodic `phi` on compact Stonean `K`, and `lambda` in `sigma(C)`, `lambda I-C` bounded below is equivalent to closed invariant sets `E,F` and a **clopen** wandering set `Q`, whose iterates, `E`, and `F` are pairwise disjoint and cover `K`. Spectrum on `E` is strictly inside `|lambda|`; spectrum on `F` strictly outside it. Crucially the **global** positive-tail accumulation set of `phi^j Q` lies in `E`, and the global negative-tail accumulation lies in `F`.
4. For historical context, proof 5.2, displayed (24), prints the older clopen spectral-gap split credited to Kitover 2011 Theorem 3.10. The narrowed certificate proves this resolvent case independently with Riesz projections and multiplier invariance, so the original proof access limit is not a premise.

**Excluded broader proof issue:** K20 proof 5.2, equation (33), writes `tilde T^n P_1=T^n P_1 U^(-2n)` for `tilde T=wU^-1`. In general the left side uses products along negative iterates while the right side uses products along positive iterates, so the displayed identity is algebraically false without an additional argument. The certificate does not treat the entire old proof as independently validated. Its needed one-direction construction precedes this issue and avoids it; the old central global-tail statement is independent of this step.

**K11 provenance:** *Spectrum of weighted composition operators: part 1. Weighted composition operators on C(K) and uniform algebras*, Positivity 15 (2011), 639–659, DOI <https://doi.org/10.1007/s11117-010-0106-4>. Publisher metadata dates online publication to 2010-12-08. The publisher preview was inspected; the original theorem proofs are subscription-restricted and were **not** retrieved. Thus our inspected certificate uses K20's exact printed primary-author statement and attribution, not a claim to have read K11's original proof or compared both versions literally. K20's arXiv version header dates the evidence; its internal dynamically rendered `Date: August 24, 2026` is not treated as the version date.

**Shadowing input:** the finite-average bounded-forcing argument below proves directly that `I-B*` is bounded below. It needs no inaccessible source. For historical context, Dragičević–Pituk's 2026 spectral characterization is explicitly restated as Theorem 1 in Pituk's primary arXiv:2608.19499v1 (2026-08-19); the original publisher PDF was inaccessible and its proof is not claimed inspected.

## Exact setup and complexification

Let `Omega=W x Z`, with product measure `m=nu x counting`. No atomicity or separability of `W` is assumed. The candidate's isometry sends the original composition operator to

`(Bg)(w,n)=a_n(w) g(w,n+1)`, where `a_n=(rho_n/rho_{n+1})^(1/p)>0`.

Bounded invertibility says `0<c<=a_n<=C<infinity` almost everywhere. Its dual on `L^q(Omega)` (`1/p+1/q=1`, and `q=infinity` at `p=1`) is

`(Sh)(w,n)=a_{n-1}(w) h(w,n-1)`.

Write `s(w,n)=(w,n-1)`, `b(w,n)=a_{n-1}(w)`, so `S=M_b U`, where `Uh=h o s` is a positive invertible isometry. Thus `sigma(U)` is contained in the unit circle, since both forward and inverse powers have norm 1. Work over the complex scalars to apply K20. In the real case, real shadowing complexifies: split any complex pseudotrajectory into its real and imaginary parts, shadow the two parts separately, and add the shadowing vectors. At most a factor 2 is lost in the error bound. The final band projections are real indicators, so the splitting restricts back to real `L^p`.

## The Stone representation satisfies every transfer hypothesis

Since `m` is sigma-finite, its measure algebra is complete. Let `K` be its Stone space. The unital algebra `L^infinity(Omega,m)` is isometrically `C(K)`; `K` is Stonean. Multipliers act faithfully and isometrically on every nonzero `L^q`, including `q=infinity`: a nonzero essential level set contains a positive finite-measure subset on which its multiplier norm can be tested. A vector's annihilator consists exactly of multipliers supported outside its essential support, hence is the projection band generated by that complement. This is the Kaplansky property; K20 Proposition 2.5 also supplies the required weak-operator closure. The coordinate shift and its inverse preserve disjointness and intertwine multipliers, so `U` is a module d-isomorphism.

The induced Stone homeomorphism `phi` is characterized by `U M_f U^-1=M_(f o s)`, i.e. it extends the action `s`. It has **no periodic Stone points**, not merely no periodic points of the original measure space. Indeed, for any positive integer `r`, use the finite clopen partition induced by the coordinate residues `n mod (r+1)`. The map `phi^r` cyclically sends each partition member to a different one, since `r` is nonzero modulo `r+1`. Every Stone point belongs to exactly one member. A `phi^r` fixed point would therefore belong to two disjoint members, a contradiction.

For `q=infinity`, `S` already is the central weighted composition operator on `C(K)`. For finite `q`, only the one-direction approximate-spectrum transfer, independently checked below, is needed for the central operator

`Cf=b(f o phi)` on `C(K)`.

## The minimal transfer, proved directly for the concrete shift

Only `sigma_ap(C) subset sigma_ap(S)` at 1 is required. This can be proved without any imported central point criterion or the flagged equation (33).

Suppose unit `f_m in L^infinity(Omega)=C(K)` satisfies `||Sf_m-f_m||_infinity <= epsilon_m`, where `epsilon_m=m^-3`. Since the essential supremum is 1, some coordinate `n_m` and positive finite-measure set `A_m subset W` satisfy `|f_m(w,n_m)|>=1/2` on `A_m`. Put `r_m=1-m^-1/2` for `m>=2`, and define

`chi_m(w,n)=1_(A_m)(w) r_m^|n-n_m|` if `|n-n_m|<=m`, and 0 otherwise.

The vector `h_m=chi_m f_m` belongs to every finite `L^q`, and `||h_m||_q >= (1/2) nu(A_m)^(1/q)`. Write `s(w,n)=(w,n-1)`. The exact identity is

`Sh_m-h_m=(chi_m o s-chi_m)f_m+(chi_m o s)(Sf_m-f_m)`.

Away from the two endpoints of the cutoff, the modulus of `chi_m o s-chi_m` is at most `(1-r_m)/r_m` times `chi_m`. Thus this part has norm at most that factor times `||h_m||_q`. At the two endpoints the norm is at most `2 r_m^m nu(A_m)^(1/q)`, because `||f_m||_infinity=1`. The approximation-error term has norm at most `epsilon_m (2m+1)^(1/q) nu(A_m)^(1/q)`. Consequently

`||Sh_m-h_m||_q / ||h_m||_q <= (1-r_m)/r_m + 4r_m^m + 2m^-3(2m+1)^(1/q) -> 0`.

For `q=infinity`, transfer is the identity of the spaces; the same estimate is also valid with essential maximum norms. Hence `1 in sigma_ap(C)` implies `1 in sigma_ap(S)`. This proves exactly the needed contrapositive without claiming any reverse inclusion or full-spectrum equality. The geometric cutoff even works at `q=1`, though the actual finite dual exponents here are `q>1`.

## Shadowing gives the required bounded-below central difference operator

Shadowing and linear scaling give a constant `K` such that every bounded forcing `b_j` has a bounded solution of `y_(j+1)-B y_j=b_j` with `sup_j ||y_j||<=K sup_j ||b_j||`. To see this directly, construct a pseudotrajectory for the scaled forcing recursively in both integer directions, shadow it, and subtract the exact orbit; bounded invertibility permits the backward recursion.

There is a short finite-average consequence. Fix any dual `u`, choose a unit `v` with `Re u(v)>=||u||-delta`, and use the forcing `b_j=v` for `1<=j<=N`, zero elsewhere. A bounded solution gives, after summing the dual identity,

`N Re u(v) <= 2K||u|| + NK||(I-B*)u||`.

Divide by `N`, let `N->infinity`, then `delta->0`. Thus `||u||<=K||(I-S)u||` for `S=B*`. In particular 1 is outside `sigma_ap(S)`, and the concrete transfer proves 1 is outside `sigma_ap(C)`. Equivalently `I-C` is bounded below. This step requires neither adjoint uniform expansivity nor the inaccessible Dragičević–Pituk proof.

## Constructing a one-step clopen split from the old global-tail theorem

First suppose `1` belongs to `sigma(C)`. Apply K20 Theorem 2.26 with `lambda=1`, obtaining `E,F,Q`. Put `Q_j=phi^j Q` and

`V=E union (union_(j>=0) Q_j)`,

`V^c=F union (union_(j<0) Q_j)`.

Both sets are closed. For example if a point outside `V` were in its closure, it lies outside the closed set `E` and each of the finitely many `Q_0,...,Q_(N-1)`. It would therefore lie in `closure(union_(j>=N) Q_j)` for every `N`, hence in `E` by the positive-tail condition, a contradiction. The same argument using the negative-tail condition proves `V^c` closed. Thus `V` is **clopen**, and

`phi(V) subset V`, `phi^-1(V^c) subset V^c`.

This is a split invariant under one step, with no measurable selection, no fiberwise uniformity inference, and no passage to a power. Every clopen set of `K` is a measurable projection in the original complete measure algebra, so it gives a measurable indicator band on `L^p(Omega)`.

## Uniform exponential product bounds, directly from the global tails

Let `b_k(x)=product_(i=0)^(k-1) b(phi^i x)` and `c_k(x)=product_(i=1)^k b(phi^-i x)^-1`. Both are continuous positive functions. On `E`, `||C_E^k||=sup_E b_k`, so `r(C_E)<1` yields some `d>=1` and `alpha<1` with `sup_E b_d<alpha`. Choose `alpha<alpha'<1`; continuity yields an open neighborhood `H` of `E` with `b_d<alpha'` throughout `H`.

The nested compact sets `A_N=closure(union_(j>=N) Q_j)` have intersection contained in `E`. Compactness therefore gives an integer `J` with `A_J subset H`: otherwise their nonempty closed intersections with the compact complement of `H` would have a common point. Since `phi^t(V)=E union (union_(j>=t) Q_j)`, every `phi^t(V)` lies in `H` for `t>=J`. Let `L=max(1,||b||_infinity,||b^-1||_infinity)`. For `k=J+td+r` with `0<=r<d`, products from `V` satisfy

`sup_V b_k <= L^(J+d) (alpha')^t`.

Increasing a fixed prefactor covers `k<J` and gives `sup_V b_k <= C_s beta_s^k` with `beta_s=(alpha')^(1/d)<1`.

Apply the identical argument to the inverse central operator on `F`, the map `phi^-1`, the weight `b^-1 o phi^-1`, and the global negative-tail condition. Since `r(C_F^-1)<1`, this gives

`sup_(V^c) c_k <= C_u beta_u^k`, with `beta_u<1`.

Empty `E` or `F` cause no gap. If, for example, `E` is empty and `Q` nonempty, the nested nonempty compact positive-tail sets would have nonempty intersection, contradicting its inclusion in empty `E`. Thus the corresponding transition set is absent and the corresponding band is zero; pure contraction or pure expansion cases are permitted.

If `1` is outside `sigma(C)`, multiplication by `exp(i theta n)` conjugates the coordinate operator to a unimodular multiple of itself. Hence its spectrum is rotation invariant and the whole unit circle is outside it. The Riesz stable and unstable spaces give a clopen invariant split directly: for every multiplier `h`, the identity `C^k(hf)=(h o phi^k)C^k f` preserves forward exponential decay, while the analogous inverse identity preserves backward exponential decay. Both Riesz spaces are therefore invariant under all multipliers, so their projection `P_s` commutes with them. On `C(K)`, `P_s f=f P_s 1`; writing `e=P_s 1` gives `P_s=M_e`, `e^2=e`, and a clopen set `V={e=1}`. Since `P_s` commutes with `C` and `b>0`, `e o phi=e`. The Riesz restrictions have spectral radii `r(C|V)<1` and `r(C^-1|V^c)<1`, giving the same product estimates immediately. This check does not rely on full spectrum transfer or the uninspected original proof of Kitover 2011 Theorem 3.10. It includes cases when all spectrum lies inside or outside the unit circle.

## Orientation and transfer back to the primal operator

This is the essential orientation check. For central `C`, the support of `Cf` is `phi^-1(supp f)`. For the primal `B`, the support moves by **phi**: a vector at coordinate `n` is sent to coordinate `n-1`. These directions are opposite.

On original measurable coordinates,

`b_k(w,n)=(rho_(n-k)(w)/rho_n(w))^(1/p)`;

`c_k(w,n)=(rho_(n+k)(w)/rho_n(w))^(1/p)`.

Changing the summation index in the `L^p` norm gives, for a vector supported in `V`,

`||B^k g||_p^p = integral_Omega b_k(w,n)^p |g(w,n)|^p dm`,

and for a vector supported in `V^c`,

`||B^-k g||_p^p = integral_Omega c_k(w,n)^p |g(w,n)|^p dm`.

Thus the old central product bounds are exactly the needed **primal** norm bounds. Moreover `phi(V) subset V` gives `B L^p(V) subset L^p(V)`, and `phi^-1(V^c) subset V^c` gives `B^-1 L^p(V^c) subset L^p(V^c)`. We obtain the complementary closed bands

`L^p(Omega)=L^p(V) direct_sum L^p(V^c)`

with uniform forward and backward exponential contraction. This is generalized hyperbolicity. The standard convergent Green series for this split proves shadowing and was already established in the linear-dynamics literature; the candidate also supplies it directly.

## The displayed density-drop condition is also an old-mechanism corollary

The complementary bands give constants `C>=1`, `0<alpha<1` for which `||B^k|M||<=C alpha^k` and `||B^-k|N||<=C alpha^k` for every `k>=0`, after taking the maximum of the two constants and rates. Choose a common positive integer `d` sufficiently large that `C alpha^d<1`, and put `eta=(C alpha^d)^p<1`.

The exact primal norm identities imply, almost everywhere on the corresponding support bands,

`rho_(n-d)(w)/rho_n(w)<=eta` on `M`,

`rho_(n+d)(w)/rho_n(w)<=eta` on `N`.

For example a positive-measure portion of the stable support where the first ratio exceeded the operator bound would, by taking a finite-measure indicator there, contradict `||B^d|M||<=C alpha^d`. Since the two supports cover `Omega` modulo null sets, we obtain

`min(rho_(n-d)(w),rho_(n+d)(w))<=eta rho_n(w)`

for all integer `n` outside one common `nu`-null subset of `W`; the common set is obtained by the countable union of the coordinate exceptional sets. Thus this displayed density condition also follows from the older complementary support-band mechanism. This is a derived formula corollary, not a claim that an older paper printed the literal formula in this notation. Novelty cannot be certified solely by its display format.

## Priority implication and exact remaining validation

The difficult measurable uniform splitting is therefore supplied by old scalar central-spectrum/lattice results: the global clopen transition theorem stated in K20 and attributed there to K11, plus an independently checked concrete one-direction approximate-spectrum transfer. The latter is consistent with the earlier disjoint-orbit mechanism in K20, but needs no blanket validation of the broader theorem. The candidate density-drop and finite-intersection proof is a different elementary implementation, but a different formula format does not establish a novel theorem.

This certificate preserves two distinctions: (i) it is a derived corollary of older mechanisms, rather than an assertion that the exact no-bounded-distortion composition statement was printed before; (ii) original K11 and Dragičević–Pituk proof access remains incomplete, and the broader K20 proof has a recorded algebra issue; the exact global-tail statement, direct one-direction transfer, finite-average necessary condition, and Riesz resolvent case are checkable. The independent adversarial check in `kitover_translation_falsifier/FALSIFIER.md` passes the narrowed translation. The imported scalar theorem is not independently reproved; this explicit source boundary remains.
