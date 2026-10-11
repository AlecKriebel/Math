# Independent adversarial audit of the central-spectrum translation

Checkpoint: 2026-10-01 13:29:59 UTC. Assigned falsification audit: **100% complete**. No counterexample to the narrowed mathematical implication was found. The broader old source proof contains an algebraic failure, recorded below; the implication needed here has an independent proof that avoids it.

Final checkpoint: 2026-10-01 13:34:49 UTC, **100% complete**. Added the exact equation (33) countercheck and independently validated the parent-proposed direct coordinate cutoff transfer.

## Scope and independence

Exact target: a bounded invertible dissipative scalar composition operator on real or complex `L^p`, `1 <= p < infinity`, on a sigma-finite measure space with a finite positive-measure wandering generator, has generalized hyperbolicity if it has two-sided shadowing, without bounded distortion. The proposed deduction goes through an invertible positive weighted bilateral shift on `Omega = W x Z` and a central weighted composition operator on the Stone space of its measure algebra.

I inspected only the target translation and primary cached Kitover sources for the substantive splitting audit, and no sibling priority-family verdicts. Before the interruption, the original task permitted consulting the candidate proof; I read its setup and necessary dual lemma, but not its support-band splitting. The resumed audit below independently derives the needed necessary dual estimate and central transfer, without invoking that candidate lemma. I made no external individual communication and no Git or canonical-source edits.

Primary inspected source: [Kitover–Orhon, arXiv:2009.09303v2](https://arxiv.org/html/2009.09303v2), including Definition 2.3, Proposition 2.5, Theorem 2.26, Section 5 assumptions (20)–(22), and the proofs of Theorems 5.2 and 5.4. The cached PDF text confirms the relevant Theorem 2.26 statement and its global tail closures; this is not merely an HTML transcription interpretation. The PDF has the version header `19 Dec 2020` and internal date `Tuesday 22nd December, 2020`; the HTML's dynamically rendered 2026 internal date does not date the theorem evidence.

## Verdict and exact remaining external input

**The narrowed mathematical translation passes.** Its sufficient chain is:

1. Shadowing implies `I - B*` is bounded below, by the direct argument below.
2. For the normalized product shift, `sigma_ap(C) subset sigma_ap(S)`, where `S=B*`, by the independent finite-tower argument below. Thus `I-C` is bounded below.
3. If `1 in sigma(C)`, the scalar Theorem 2.26 global-tail decomposition produces a clopen one-step split and uniform product bounds.
4. If `1 notin sigma(C)`, the coordinate gauge and ordinary Riesz projections produce a clopen invariant split directly.
5. The support directions and change of summation index turn those central products into contraction estimates for the primal `B` on complementary measurable bands.

The only non-elementary scalar decomposition still imported is K20 Theorem 2.26, which explicitly attributes its statement to Kitover 2011 Theorem 3.29. This audit verifies the exact printed statement and the deduction from it, **not** the inaccessible original K11 proof. It does not independently reprove that scalar global-tail theorem. That source-access boundary is the remaining gap in an entirely self-contained certificate; it is not a failed hypothesis match or a transferred version of the composition-operator problem.

The result is a presently checkable derived corollary of older machinery. This does **not** establish that the exact no-bounded-distortion composition-operator corollary was printed before. Without K11's original text, prefer “K20 states and attributes this theorem to K11” to “reproduces exactly” as a literal-text provenance claim.

## Genuine failure in the broader old proof

K20 proof 5.2 defines `tilde T = w U^{-1}`. Its equation (33) identifies `tilde T^n P1` with `T^n P1 U^{-2n}` via a common `w_n`. In general,

`T^n = [product_(i=0)^(n-1) (w o phi^i)] U^n`,

`tilde T^n = [product_(i=0)^(n-1) (w o phi^{-i})] U^{-n}`.

Already at `n=2`, the central factors are `w(w o phi)` and `w(w o phi^{-1})`, which need not agree. Multiplication by an invariant spectral projection does not generally repair this equality. For an exact countercheck, use `Omega={stable,unstable} x Z`, `phi(n)=n-1`, and the coordinate-shift isometry. On the stable component let `w(n)` have values `1/4,1/2,3/4` at residues `0,1,2 mod 3`, respectively; on the unstable component let `w=2`. Take `r=1` and the stable spectral projection `P1`. At coordinate zero on the stable component, `w(w o phi)=3/16`, whereas `w(w o phi^{-1})=1/8`. Thus the claimed operator equality fails even with a genuine interior spectral gap and all the relevant product-shift hypotheses.

Consequently this audit does not promote full equality of spectra or full two-sided approximate-spectrum equality on the strength of a blanket claim that those old proofs were checked without issue. The weaker inclusion actually needed here has the following proof, independent of equation (33), K11 Lemma 3.25, and the reverse inclusion in K20 Theorem 5.4.

## Direct shadowing necessary estimate

Let `A` be any bounded invertible operator with two-sided shadowing. Scaling the shadowing accuracy and tolerance shows that every bounded forcing `b_j` admits a bounded solution

`y_(j+1) - A y_j = b_j`,  `sup_j ||y_j|| <= K sup_j ||b_j||`,

with one fixed finite `K`. Indeed recursively construct a two-sided pseudotrajectory after scaling the forcing into the shadowing tolerance, and subtract an exact orbit that shadows it; invertibility permits the recursion in both directions.

For `u in E*`, choose a unit-ball vector `v` with `Re u(v) >= ||u|| - epsilon`, and use forcing `b_j=v` for `1<=j<=N`, zero otherwise. Summing its equation gives

`N Re u(v) = Re u(y_(N+1)-y_1) + Re sum_(j=1)^N [(I-A*)u](y_j)`.

Hence

`N (||u||-epsilon) <= 2K ||u|| + NK ||(I-A*)u||`.

Divide by `N`, let `N -> infinity`, then `epsilon -> 0`. This proves

`||u|| <= K ||(I-A*)u||`.

Thus `1 notin sigma_ap(A*)` directly. No norm attainment, reflexivity, separability, or recent general shadowing characterization is used.

## Independent proof of the minimal central transfer

Let `S=M_b U` on scalar `L^q(Omega)`, `1<=q<=infinity`, where `U h=h o s` is the coordinate-shift isometry, `b` is positive with a positive uniform lower bound, and `C f=b(f o phi)` is its central operator on `C(K)`. Write

`b_j(x)=product_(i=0)^(j-1) b(phi^i x)`.

Suppose `1 in sigma_ap(C)`. Fix `m>=4`. Choose `f=f_m in C(K)` with `||f||=1` and `||Cf-f||` so small that

`||C^j f-f|| <= 1/2` for every integer `j` with `|j|<=m+1`.

This follows by finite telescoping: for positive `j`, use `sum_(i=0)^(j-1) C^i(Cf-f)`; for `j=-l`, use `-sum_(i=1)^l C^{-i}(Cf-f)`. This only uses fixed finitely many bounded powers for each `m`.

Pick `k=k_m` where `|f(k)|=1`. Since `|f|<=1`, the positive and negative powers imply, for `1<=j<=m+1`,

`b_j(k) >= 1/2`,  `b_j(phi^{-j}k) <= 2`.

The negative-power formula is `C^{-j}f(k) = f(phi^{-j}k)/b_j(phi^{-j}k)`. By continuity choose a nonempty clopen neighborhood `O` of `k` on which all these finite inequalities weaken to

`b_j(x) >= 1/4`,  `b_j(phi^{-j}x) <= 4`.

Because `phi` has no periodic points, shrink `O` so that `phi^j O`, `|j|<=m+1`, are pairwise disjoint. Choose `u=u_m` supported on the measurable projection `O` with `||u||_q=1`. For finite `q` such a vector exists by taking a positive finite-measure subset; for `q=infinity` use its indicator.

The vectors `S^j u`, `|j|<=m+1`, have disjoint supports `phi^{-j}O`. On `phi^{-j}O`, the multiplier in `S^j` is bounded above by four. On `phi^j O`, the multiplier in `S^{-j}` is the reciprocal of `b_j` evaluated on `O`, also bounded above by four. Since `U` and its inverse are isometries,

`||S^j u||_q <= 4` for all `|j|<=m+1`.

Put `t=1-1/sqrt(m)` and

`y_m = sum_(j=-m)^m t^|j| S^j u`.

Disjointness gives `||y_m||_q>=1`, including the supremum norm at `q=infinity`. The interior coefficients of `(S-I)y_m` are `t^|j-1|-t^|j|`, whose absolute values are at most `[(1-t)/t]t^|j|`. The scalar `L^q` disjoint-support norm, also for `q=infinity`, therefore bounds the interior error by `[(1-t)/t]||y_m||_q`. Its two boundary terms are `t^m S^{m+1}u` and `-t^m S^{-m}u`, with combined norm at most `8t^m`. Consequently

`||(S-I)y_m||_q / ||y_m||_q <= (1-t)/t + 8t^m -> 0`.

This proves the required implication `1 in sigma_ap(C) => 1 in sigma_ap(S)`. No single common Stone point for all `m`, infinite measurable selection, Fatou theorem, or old scalar orbit criterion is needed. A phase conjugation gives the corresponding statement at other nonzero spectral parameters if desired; only the parameter one is used here.

### Additional direct cutoff proof, independently checked

After the preceding proof was completed, the parent proposed an even shorter coordinate cutoff argument. I independently checked its signs, both boundaries, and the endpoint norms. It avoids Stone aperiodicity altogether for the transfer step.

Represent a central approximate vector as `f in L^infinity(Omega)` with `||f||_infinity=1` and `||Sf-f||_infinity<=epsilon`. Some coordinate `n0` has a positive finite-measure subset `E` on which `|f(w,n0)|>=1/2`: use the positive-measure essential level set and the countable coordinate partition, then sigma-finiteness. Put `r=1-m^{-1/2}`, and define

`chi(w,n)=1_E(w) r^{|n-n0|}` for `|n-n0|<=m`, zero otherwise; `h=chi f`.

The exact identity is

`Sh-h = (chi o s-chi)f + (chi o s)(Sf-f)`.

On the interior `n0-m+1 <= n <= n0+m`, the first coefficient is bounded in absolute value by `[(1-r)/r]chi`. At the two exterior boundaries `n=n0-m` and `n=n0+m+1`, the coefficients are respectively `-r^m` and `+r^m`. Thus those two terms have combined norm at most `2r^m nu(E)^{1/q}`. Also

`||h||_q >= (1/2)nu(E)^{1/q}`.

The error term is supported on `2m+1` coordinates and has norm at most `epsilon(2m+1)^{1/q}nu(E)^{1/q}`. With the usual supremum-norm interpretation at `q=infinity`,

`||(S-I)h||_q / ||h||_q <= (1-r)/r + 4r^m + 2epsilon(2m+1)^{1/q}`.

Choose `epsilon=m^{-3}`. The bound tends to zero for every `1<=q<=infinity`. This establishes the same minimal inclusion using only the concrete countable product-coordinate shift and bounded weights, without invertibility or a Stone-space orbit criterion in the transfer step.

## All-p module hypotheses and Stone aperiodicity

The sigma-finite measure algebra is a complete Boolean algebra: essential suprema of arbitrary families can be obtained separately on a countable finite-measure exhaustion, then combined. Completion of the underlying pointwise sigma-algebra is not required; all assertions are modulo null sets. Its Stone space `K` is extremally disconnected, and `L^infinity(Omega)` is isometrically the unital algebra `C(K)`.

For every scalar `L^q`, the multiplier representation is faithful and isometric. To test the norm of a multiplier, use a positive finite-measure portion of an essential level set (or an indicator at `q=infinity`). The annihilator of `h` is exactly the projection band of multipliers supported outside `{h!=0}`. Thus the Kaplansky definition and Proposition 2.5's weak-operator closure condition are satisfied, without atomicity or separability. The coordinate shift and its inverse intertwine multipliers and preserve disjointness. All finite towers in the proof are represented by nonzero measure-algebra projections; no Stone singleton is assumed to carry positive measure.

For every `r>=1`, partition the coordinates by `n mod(r+1)`. These give a finite clopen partition of `K`; `phi^r` moves each part to a different part because `r` is nonzero modulo `r+1`. A fixed point of `phi^r` is impossible. This rules out periodic Stone points, including those outside the original measurable coordinate points.

At `p=1`, the Banach dual is scalar `L^infinity` because the product measure is sigma-finite, and `S` is already the central operator; no approximate-spectrum transfer theorem is necessary. In the real case, shadowing complexifies by shadowing real and imaginary parts with half the requested accuracy. Positive real indicator projections and real contraction estimates then restrict the final splitting to real `L^p`. There is no reflexivity assumption.

## Spectral case: global tails really yield uniform bounds

K20 Theorem 2.26 states exactly the following relevant conditions at `lambda=1`: closed invariant `E,F`, clopen wandering `Q`, a disjoint cover by `E,F,Q_j=phi^jQ`, spectrum strictly inside one on `E` and strictly outside one on `F`, and

`intersection_N closure(union_(j>=N) Q_j) subset E`,

`intersection_N closure(union_(j>=N) Q_{-j}) subset F`.

These are **global** tail statements, not merely individual-orbit accumulation statements. They imply that `V=E union union_(j>=0)Q_j` and its complement `F union union_(j<0)Q_j` are both closed: a hypothetical exterior limit point avoids the closed invariant part and every finite initial collection of clopen tower pieces, so lies in every global tail closure, contradicting that it is exterior. Thus `V` is clopen, `phi(V) subset V`, and `phi^{-1}(V^c) subset V^c`.

Let `d>=1` satisfy `sup_E b_d < alpha < 1`, obtained from the spectral radius of `C_E`. Choose `alpha<alpha'<1` and an open neighborhood `H` of `E` where `b_d<alpha'`. The decreasing compact global tail closures `A_N` have intersection in `E`; compactness gives one **global** `J` with `A_J subset H`. Indeed otherwise the decreasing compact sets `A_N intersect(K\H)` would have a common point. Every `phi^t(V)` is in `H` for `t>=J`. With `L=max(1,||b||,||b^{-1}||)` and `k=J+td+r`, `0<=r<d`, the cocycle product identity gives

`sup_V b_k <= L^(J+d) (alpha')^t`.

This is `C_s beta_s^k` after changing a constant, with `beta_s=(alpha')^(1/d)<1`. Apply the same argument to `C_F^{-1}` and `phi^{-1}` to obtain

`sup_(V^c) product_(i=1)^k b(phi^{-i}x)^{-1} <= C_u beta_u^k`, `beta_u<1`.

If either invariant limiting set is empty, nonempty `Q` would contradict compactness of the corresponding decreasing nonempty tail closures; hence `Q` is empty in that case. Zero stable or unstable bands and purely contracting or expanding cases are allowed. This verification uses precisely the uniformity delivered by the scalar theorem, with no bounded-distortion condition.

## Resolvent case: a direct clopen split

For `D_theta h(w,n)=exp(i n theta)h(w,n)`,

`D_theta^{-1} S D_theta = exp(-i theta) S`.

The same conjugation holds in the central algebra. Hence `sigma(C)` is rotation invariant by a direct coordinate gauge, without invoking K20 Theorem 2.15 or checking its separate Fatou hypotheses. If `1 notin sigma(C)`, the entire unit circle misses the spectrum.

Use ordinary Riesz projections `P_s,P_u` for the portions of `sigma(C)` inside and outside the unit circle. The stable subspace has uniformly decaying forward powers and the unstable subspace uniformly decaying inverse powers. Both subspaces are invariant under every multiplier `h`: the identity

`C^n(hf)=(h o phi^n) C^n f`

preserves the forward decay bound, and its negative-power version preserves backward decay. The spectral characterization of the two subspaces then gives their multiplier invariance. Equivalently, apply the decaying inverse powers on the unstable component to a purported forward-decaying vector to show that component is zero, and vice versa.

Because both complementary subspaces are multiplier invariant, `P_s` commutes with every multiplier. On `C(K)` this gives `P_s h=h(P_s 1)` for every `h`. Thus `P_s=M_e` with continuous `e=P_s1`; idempotence gives `e^2=e`, so `V={e=1}` is clopen. Commutation with `C` and positivity/invertibility of `b` imply `e o phi=e`, hence `V` is invariant. Spectral-radius bounds on the restrictions immediately give the same uniform product bounds as above. Empty spectral pieces are harmless. This independently verifies the exact mechanism attributed to K11 Theorem 3.10 and printed at K20 equation (24).

## Primal direction and measurable realization

On the product coordinates, `phi` represents `s(w,n)=(w,n-1)`, `b(w,n)=a_(n-1)(w)`, and `a_n=(rho_n/rho_(n+1))^(1/p)`. The central operator moves supports by `phi^{-1}`, whereas the primal `B g(w,n)=a_n g(w,n+1)` moves supports by `phi`. The opposite directions are essential and are handled correctly in the translation.

The two central products are

`b_k(w,n)=(rho_(n-k)(w)/rho_n(w))^(1/p)`,

`c_k(w,n)=(rho_(n+k)(w)/rho_n(w))^(1/p)`.

Changing the summation index yields the exact identities

`||B^k g||_p^p = integral b_k^p |g|^p dm`,

`||B^{-k} g||_p^p = integral c_k^p |g|^p dm`.

Consequently the clopen central product bounds give primal forward contraction on `L^p(V)` and inverse contraction on `L^p(V^c)`. The inclusions of supports give `B L^p(V) subset L^p(V)` and `B^{-1} L^p(V^c) subset L^p(V^c)`. Every Stone clopen is a measurable indicator modulo null sets; those almost-everywhere inclusions suffice for the invariant closed bands. Complementary indicator projections give the direct sum. This is exactly generalized hyperbolicity in the spectral-radius convention, for all stated `p` and both scalar fields.

## Required wording changes before promoting the certificate

- Replace the blanket reliance on full K20 spectral equalities with the independently checked one-direction inclusion actually needed.
- Record the equation (33) failure rather than calling the whole older proof validated.
- Use the direct gauge in the resolvent case; it avoids a needless implicit Fatou-hypothesis discussion.
- Keep the scalar Theorem 2.26 imported-source boundary and the distinction between an old general mechanism and an exact earlier printed composition-operator statement explicit.

Subject to those changes, I find no missing `p=1`, real-scalar, nonseparable, measurable-uniformity, clopen-closure, empty-band, or primal-orientation condition that blocks the deduction.
