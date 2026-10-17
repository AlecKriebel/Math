# Primary-source adversarial audit of the Nikula implication

## Verdict

**PASS as a corollary of the authenticated Theorem 1.** No gap was found in the proposed Gaussian implication or in the radial-clipping strengthening. The resulting scope is stronger than ordinary hypercyclicity:

1. For IID standard complex Gaussian jets, almost surely f is frequently hypercyclic for D and, simultaneously for every nonconstant complex polynomial p, |(pf)^(n)(0)| tends to infinity.
2. Such frequently hypercyclic simultaneous counterexamples form a dense subset of H(C).
3. For every M>=0, frequently hypercyclic functions are dense relative to the exact annular space X_M defined by eventual bounds (n+1)^(-1/2) <= |f^(n)(0)| <= log(n+e). Every function in that space has the same all-polynomial escape property. In particular the union of the relative frequently hypercyclic classes is dense in H(C).

There is an essential distinction: the raw Gaussian jets almost surely violate the exact exponent-1/2 lower bound infinitely often. Radial clipping, followed by an orbit-stability argument, is necessary for the exact annular conclusion. Applying Nikula's IID theorem directly to the clipped non-IID coefficients would be invalid; the argument below does not do that.

This is a candidate-aware adversarial audit of a supplied implication, not a novelty assessment. Nikula's theorem is an authenticated external theorem input, not a theorem reproved here. All probabilistic estimates and subsequent deterministic implications below are independently checked.

## 1. Primary authentication and exact input boundary

The only external mathematical source read was Miika Nikula, *Frequent hypercyclicity of random entire functions for the differentiation operator*, [arXiv:1209.6209v1](https://arxiv.org/abs/1209.6209v1), obtained from its [version-specific primary PDF](https://arxiv.org/pdf/1209.6209v1).

The complete theorem was visually inspected on PDF/printed pages 2–3 after local rendering, and cross-checked against text extraction. Downloaded PDF: `sources/nikula_1209.6209v1.pdf`, 180409 bytes, SHA-256 `b24a6e7469325963d5bc343aca141b2e40b7d578c41e56023e6f984ed4c27e2b`. `SOURCE_RECORD.json` binds the source and access details. Source bodies, extracted text and rendered page images stay in ignored `sources/`.

The version-specific archive record gives submission on 2012-09-27 at 12:45:47 UTC, and the PDF margin identifies v1/27 September 2012. The served PDF also prints an internal date of August 2, 2018 and has November 17, 2018 creation metadata. These distinct observations are recorded without inferring their cause. This audit does not assert that the presently served PDF bytes existed in 2012, or infer when the corollary itself was first noticed.

No sibling priority reports, other research shards, later literature, unversioned later Nikula source, Git/index operations, publication, or outside contacts were used. The earlier annular review was not edited. Its prior conclusion was not substituted for primary theorem authentication.

## 2. The authenticated external input and Gaussian assumptions

Theorem 1 assumes a complex law supported on all of C and a beta>0 with

\[
\limsup_{r\to\infty}(\log r)^{1+\beta}\mathbb P(|X|\ge r)<\infty.
\]

For independent copies X_n of that law, it concludes that sum X_n z^n/n! is almost surely entire and frequently hypercyclic for differentiation on H(C). No centering or moment condition beyond its displayed tail hypothesis is required by that theorem. [Primary theorem, pp. 2–3](https://arxiv.org/pdf/1209.6209v1).

Fix the convention that a standard complex Gaussian has density pi^(-1)exp(-|z|^2) with respect to planar area. Its law has full support C, and

\[
\mathbb P(|X|<t)=1-e^{-t^2},\qquad
\mathbb P(|X|>t)=e^{-t^2}\quad(t\ge0).
\]

Thus the theorem's logarithmic tail expression tends to zero for every beta>0. It applies to the IID Gaussian sequence and provides an event E_FHC of probability one on which

\[
f(z)=\sum_{n\ge0}X_n\frac{z^n}{n!}
\]

is entire and frequently hypercyclic. Frequent hypercyclicity here means that visits to every nonempty open set have positive lower natural density.

## 3. The single coefficient event, including the sharp failed boundary

For n>=1,

\[
\mathbb P(|X_n|<n^{-3/4})
=1-e^{-n^{-3/2}}\le n^{-3/2}.
\]

This is summable. Also

\[
\mathbb P(|X_n|>\log(n+e))
=\exp[-(\log(n+e))^2],
\]

which is summable: once log(n+e)>=2, it is at most (n+e)^(-2). The first Borel–Cantelli lemma gives a probability-one event E_bounds on which, for some finite random N>=1,

\[
n^{-3/4}\le |X_n|\le\log(n+e)
\quad\text{for every }n\ge N.
\]

Independence is not needed for these two summable-event conclusions. Intersecting E_bounds with E_FHC still gives probability one. No polynomial was mentioned in defining this event.

In contrast, with ell_n=(n+1)^(-1/2),

\[
\mathbb P(|X_n|<\ell_n)=1-e^{-1/(n+1)}\sim\frac1{n+1}.
\]

These failure events are independent and their probabilities have divergent sum. The second Borel–Cantelli lemma therefore gives infinitely many failures almost surely. In particular the raw Gaussian entire function almost surely belongs to none of the exact annular spaces X_M. Replacing the 3/4 bound by the exact 1/2 bound before clipping is a concrete false inference.

More generally any lower exponent alpha with 1/2<alpha<1 works for the raw argument: the small-ball probabilities are summable, while n^(1-alpha) dominates log n. The boundary alpha=1/2 fails in exactly the way just described.

## 4. One event deterministically controls every polynomial

Work on any one realization satisfying E_bounds. Let p(z)=sum_(j=0)^d c_j z^j be an arbitrary nonconstant complex polynomial, d>=1 and c_d nonzero. For n>=N+d,

\[
(pf)^{(n)}(0)=\sum_{j=0}^{d}c_j(n)_jX_{n-j}.
\]

This identity uses derivative-normalized jets; the j! in p^(j)(0) cancels the j! in the binomial coefficient. For n>=2d, the leading term obeys

\[
|c_d(n)_dX_{n-d}|
\ge |c_d|2^{-d}n^{d-3/4}.
\]

Writing C=sum_(j<d)|c_j|, all lower terms together have modulus at most

\[
C n^{d-1}\log(n+e).
\]

The ratio of this error bound to the leading lower bound is at most

\[
\frac{2^dC}{|c_d|}\frac{\log(n+e)}{n^{1/4}}\longrightarrow0.
\]

The reverse triangle inequality gives escape to infinity. This includes d=1, where n^(1/4) eventually dominates the logarithmic lower term. Complex phases, zeros of p, zero lower coefficients and arbitrarily large fixed coefficients cause no exception. If C=0 the error is simply absent.

Since p was arbitrary after fixing the realization, the implication is E_bounds => “for every nonconstant complex p, escape holds.” It is not a probability-one claim for one p followed by an uncountable intersection. Thresholds may depend on p and N; uniformity over all polynomials is not claimed.

Scalar escape excludes density of the derivative orbit. Its tail avoids the unit disk; an open subdisk avoiding the finitely many earlier scalar values still remains. Continuous evaluation at zero would send a dense entire-function orbit to a dense subset of C, so pf is not hypercyclic. This explicitly handles the full orbit including n=0 and every finite prefix.

## 5. Ambient density: two independently checkable arguments

The simplest route requires one realization f in E_FHC intersect E_bounds. For any polynomial Q, f+Q has exactly the same derivative orbit as f after order deg(Q). Thus it remains frequently hypercyclic: deleting finitely many times does not change positive lower density. For any fixed polynomial p, p(f+Q)=pf+pQ, so its high derivative values equal those of pf. All polynomial-product escape conclusions persist. The translate f+C[z] is dense in H(C), because polynomials are dense. This proves the asserted ambient density without an additional support theorem.

The raw Gaussian law also has full support on H(C). To check this directly on a disk of radius R, approximate an arbitrary target by a polynomial and choose a finite Gaussian coefficient block close to its jets. That event has positive probability. Independently, the remaining tail has arbitrarily small expected R-disk majorant, because E|X| is finite and sum R^n/n! converges. Markov's inequality makes a sufficiently small tail event have positive probability. Independence of the head and tail gives a positive-probability compact-open neighborhood. Intersecting it with the probability-one good event gives the same density conclusion.

## 6. Exact radial clipping and a null derivative orbit

Fix any M>=0. Put ell_n=(n+1)^(-1/2) and u_n=log(n+e). Leave Y_n=X_n for n<M. For n>=M define, for X_n nonzero,

\[
Y_n=\min\{u_n,\max\{\ell_n,|X_n|\}\}\frac{X_n}{|X_n|}.
\]

At X_n=0 define Y_n=ell_n on the positive real axis. This is a measurable definition everywhere; Gaussian zero events have probability zero. At n=0 the two radii coincide at 1, and clipping produces a unit-circle coefficient. This finite boundary case causes no problem.

Define F_M(z)=sum Y_n z^n/n!. It is entire for every realization with finite prefix, by the deterministic upper bound u_n after M. It belongs to X_M by construction. Let c_n=Y_n-X_n and e_M=F_M-f. Upper clipping occurs at only finitely many n almost surely, by the upper Borel–Cantelli estimate. At every sufficiently large n the only possible modification is lower clipping, of magnitude at most ell_n. Therefore

\[
c_n\longrightarrow0\quad\text{almost surely}.
\]

No claim that only finitely many lower clippings occur is made; almost surely infinitely many do occur. Since a null scalar sequence is bounded, its exponential generating series e_M is entire. For every R>=0,

\[
\|D^n e_M\|_R
\le\sum_{k\ge0}|c_{n+k}|\frac{R^k}{k!}
\le e^R\sup_{m\ge n}|c_m|\longrightarrow0.
\]

All exceptional early coefficients, including the altered n=0 coefficient when M=0, disappear under sufficiently high differentiation or are encompassed by the same tail supremum.

The required stability lemma is elementary. If f is frequently hypercyclic and D^n e ->0 locally uniformly, then f+e is frequently hypercyclic. Given a nonempty open target U, choose a disk-norm ball around some h contained in U and a smaller concentric ball V. The visit set {n:D^n f in V} has positive lower density. For all sufficiently large n the perturbation D^n e is smaller than the margin between V and U, so those visits remain in U. Removing finitely many times preserves positive lower density. Applying this lemma proves F_M frequently hypercyclic almost surely.

This step applies Nikula's theorem only to the original IID Gaussian sequence. The clipped Y_n are independent but generally not identically distributed, and their marginal supports are annuli rather than C; direct application of Theorem 1 to them would fail its hypotheses.

## 7. Full support of the clipped law and relative density

For each n>=M, the support of Y_n is the entire closed annulus

\[
A_n=\{w:\ell_n\le|w|\le u_n\}.
\]

Every relative neighborhood of an interior point has a positive-area preimage on which clipping is the identity. A neighborhood of an inner or outer boundary point contains an angular sector; radial clipping from respectively smaller or larger Gaussian radii gives it positive probability. If ell_n=u_n, the same angular argument gives full support on the resulting circle. For n<M the support remains C. Independence is preserved by coordinatewise measurable clipping.

There is a homeomorphism

\[
\mathbb C^M\times\prod_{n\ge M}A_n\longrightarrow X_M,
\qquad (a_n)\longmapsto\sum a_nz^n/n!.
\]

The common upper bound u_n makes every tail uniformly small on a fixed disk; the finitely many initial coordinates then control compact-open approximation. The inverse consists of continuous jet evaluations. A nonempty relative open set in X_M consequently contains a finite-coordinate product cylinder. Each of its coordinate events has positive probability, so independence makes the cylinder probability positive. This proves that the law of F_M has full support exactly X_M.

The almost-sure frequent hypercyclicity event intersects every such positive-probability neighborhood. Hence X_M intersect FHC(D) is dense relative to X_M for every M. The same conclusion can also be obtained from one such F_M by changing finitely many coefficients to arbitrary admissible annular values: the modification is polynomial, so frequent hypercyclicity survives, and finite-coordinate cylinders form the relative topology.

For f in X_M, the deterministic polynomial argument improves its leading lower bound to order n^(d-1/2), with error order n^(d-1)log n; the ratio is O_p(log n/sqrt(n)). Thus every nonconstant polynomial product still escapes. Finally, polynomials plus sufficiently high baseline tails ell_n z^n/n! approximate every entire target and belong to appropriate X_M. Relative density then makes the union over M of X_M intersect FHC(D) dense in H(C).

## 8. Exact scope and gaps

No repair is needed for the stated implication when the steps are ordered as above. The necessary qualifications are:

- Start n^(-3/4) estimates at n>=1 and allow finite random prefix exceptions.
- Use independence for the divergent lower-bound failure argument, not for the summable BC1 estimates.
- Do not assert that the raw Gaussian sequence eventually satisfies the exact exponent-1/2 lower bound.
- Apply Nikula before clipping, then prove frequent-hypercyclicity stability by the null derivative orbit.
- Treat full relative support through finite cylinders and the bounded-tail topology.
- Derive all-polynomial escape deterministically from one coefficient event; no uncountable probability intersection occurs.

The exact remaining mathematical gap in these corollaries is **none identified, conditional on the authenticated external Theorem 1**. That theorem was not independently reproved, and no later corroboration or later-priority source was consulted. The archive date and the served PDF's later internal/creation dates are separately recorded rather than conflated. No novelty or historical first-discovery inference is made.
