# Source-first baseline, sealed before candidate mathematics

Scope: frozen PR 370, problem 30004811, head `567c2e493854b32d0cd325ad96e4c5b69c9c1e1b`, base `efd29c05204703acca9a0860812f54b94fae54b1`. The reviewer read only the routing SOURCE_MANIFEST and fetched the seven specified PDFs before this baseline. No SOURCE_GATE, candidate proof, checker, generated checks, status, final result, prior review, queue, or root/sibling findings was read before sealing. Raw PDFs and extracted texts are private and ignored. All fetched PDF bytes match the supplied manifest hashes.

## Exact target and success criterion

The OWR 40/2021 contribution of Jeffrey Jauregui, printed pp. 2255–2258, proposes the capacity–volume mass

\[
m_{CV}(M,g)=\sup_{\{K_j\}}\limsup_j\bigl[(3|K_j|_g/(4\pi))^{1/3}-\operatorname{cap}_g(K_j)\bigr].
\]

The normalized capacity is `(4π)^(-1)` times the Dirichlet energy of functions vanishing on K and tending to 1 at infinity. Thus a Euclidean ball of radius r has capacity r. The OWR prose on capacity omits this prefactor in one sentence, but its inequality, ball normalization, mass formula, and the credited Jauregui paper make the intended convention unambiguous.

The precise original conjecture is supplied by Jauregui's paper, Definition 9 and the paragraph after Corollary 8: smooth connected one-ended AF 3-manifolds, possibly with smooth compact boundary, with decay through two derivatives `O_2(r^{-τ})`, `τ>1/2`, integrable scalar curvature, globally nonnegative scalar curvature, and boundary empty or minimal. No topology restriction, connected-boundary requirement, or outermost requirement appears there. The desired equality is `mCV=mADM`, over all compact exhaustions, including disconnected, irregular, non-ball, off-center, and badly shaped sets. The OWR sentence about general AF metrics inherits this scalar-curvature/boundary context; equality without the global curvature/boundary hypotheses is not justified.

Success requires a universal upper bound, plus the already established lower bound. A coordinate-ball calculation alone cannot establish the supremum upper bound. A code sample or numerical sweep cannot replace the quantified proof.

## Independently checked source coverage

* Jauregui, arXiv 2002.08941, retrieved 31-page version: Definition 4 has both cubic-deficit and radius-deficit definitions; Lemma 10 proves equality after restricting to efficient exhaustions; Lemma 12 supplies arbitrary-compact smoothing. Theorem 5 gives `mCV≥mADM` assuming scalar curvature nonnegative outside a compact set. Theorem 6 supplies the ball upper bound. Theorem 7 supplies the general upper bound under harmonic flatness and nonnegative ADM mass.
* Benatti–Fogagnolo–Mazzieri, arXiv 2305.01453v2, printed pp. 3–4, Theorem 1.3: `miso^(p)=miso=mADM` for `1<p≤2`, C1 AF decay `τ>1/2`, nonnegative scalar curvature, smooth compact minimal possibly empty boundary, and `H2(M,∂M;Z)=0`. Using only this theorem directly leaves a topology gap in the original claim.
* The same BFM paper, printed pp. 20–21, Theorems 5.5 and 5.6: sharp asymptotic isocapacitary comparison and `miso^(p)≤miso` require only C0 AF with compact possibly empty boundary. At p=2 this upper comparison has no H2 assumption. The proof's multiplicative error step uses a nonnegative comparison mass, a defect explicitly identified in the later Benatti paper; the AF setting supplies that sign via JLU. Consequently this route can cover the original target without extending Theorem 1.3's topology scope.
* Jauregui–Lee, arXiv 1602.00732, Theorem 3 establishes the isoperimetric/ADM identity; the relevant boundary convention is empty or minimal, as also made explicit by Jauregui Theorem 2 and JLU Theorem 6. Theorem 17 is a quantitative bound for outward minimizing allowable C1,1 regions, and requires no interior compact minimal surfaces. It cannot directly be applied to arbitrary source domains without the hull and exterior reductions. Proposition 37's statement assumes the alternative large-perimeter mass is positive; blindly dropping that condition would be a citation error.
* JLU, arXiv 2408.08871, Definition 1, Theorems 6 and 7: on a one-ended C0 AF end the isoperimetric mass is nonnegative, irrespective of scalar curvature; equality with ADM has the global nonnegative scalar curvature and minimal/empty boundary assumptions. Negative Schwarzschild ends expose the danger of extending the equality to arbitrary AF geometry.
* BFM Penrose, arXiv 2212.10215, Theorem 1.4 supplies the isoperimetric/ADM equality in the C1 optimal regime without the extra H2 condition. Lemma 2.11 explains an exterior/topology reduction when it is needed. Its boundary may have several components. This is supporting context, not permission to erase hypotheses in a separately quoted theorem.
* Benatti, arXiv 2511.11155v2 (24 December 2025), Proposition 3.1: upper comparison for strongly p-nonparabolic manifolds; Lemma 3.3 states the required sharp inequality for every region containing a fixed compact set. Theorem 1.2's complete equivalence additionally assumes orientability, absence of other compact minimal surfaces, and a positive Euclidean isoperimetric constant. That theorem is stronger in asymptotic scope but is not literally the original target. Its introduction's phrase about p in `(1,3)` overstates what BFM23 Theorem 1.3 actually states, namely `(1,2]`. At p=2 the overstatement has no effect.

## Independent mechanism available before seeing the candidate

Let `μ=miso(M,g)<∞` on a C0 AF end. JLU gives `μ≥0`. For every `m>μ`, the definition itself yields a compact core C such that every suitable region E containing C satisfies

\[
|E|\le |\partial E|^{3/2}/(6\sqrt\pi)+(m/2)|\partial E|.
\]

Proof: otherwise choose a violating E containing each core of an exhaustion, producing an exhaustion with quasilocal isoperimetric mass above m. If a nested exhaustion convention is required, recursively include the previous selected E in the next core. This avoids any need to cite a large-volume/large-perimeter version of the mass.

Define ρ(v)>0 by `v=(4π/3)ρ³+2πmρ²`, and `a(v)=4πρ(v)²`. The right side of the perimeter inequality is strictly increasing for positive area since m>0, hence every containing region has area at least a(v). The coarea/Cauchy–Schwarz capacity comparison, for a smooth compact K containing C, gives

\[
\operatorname{cap}(K)\ge \bigl[4\pi\int_{|K|}^{\infty}a(v)^{-2}\,dv\bigr]^{-1}.
\]

This follows by coarea on a capacitary potential, applying `A(t)²≤(4π cap(K))V'(t)`, and integrating in volume, or by variational coarea for smooth cutoffs followed by approximation. A fully rigorous candidate must justify critical levels, possible bounded complementary components, and arbitrary compact smoothing; silently presuming regular level sets at all t is insufficient.

Direct integration, using `dv=4πρ(ρ+m)dρ`, yields

\[
4\pi\int_{|K|}^{\infty}a(v)^{-2}\,dv=1/\rho+m/(2\rho^2),\qquad
\operatorname{cap}(K)\ge\rho/(1+m/(2\rho))\ge\rho-m/2.
\]

Meanwhile `(3|K|/(4π))^(1/3)=(ρ³+(3m/2)ρ²)^(1/3)≤ρ+m/2`, by cubing for m≥0. Thus the radius deficit is at most m for every sufficiently containing K. Smoothing (Jauregui Lemma 12), then limsup and supremum, then m decreasing to μ, gives `mCV≤miso` universally. Jauregui's lower theorem and the isoperimetric/ADM identity close the original equality. The μ=0 case is handled by taking arbitrary positive m and sending m to zero, so no division by ADM mass is necessary. Euclidean balls verify the normalization and limiting equality.

This reconstruction proves the available route is not inherently blocked by the H2 condition. It does not prejudge whether the candidate has actually executed that route correctly.

## Boundary cases to challenge after opening candidate mathematics

Empty/multiple minimal boundaries; nonoutermost boundaries and interior minimal surfaces; τ just above 1/2; zero ADM mass; nonsmooth/disconnected compact domains; nonnested exhaustion convention; bounded cavities or zero-gradient plateaux of potentials; finite versus infinite mass; source original versus C0 or C1 modifications; p=2 constants; nonorientable literal scope; arbitrary AF ends with negative ADM mass; all seals/manifests generated from the pinned head.

At this checkpoint the independent audit is 25% complete. The source target is identified and a universal route is reconstructed; candidate mathematical and implementation assessment remain unopened.
