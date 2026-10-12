# Independent adversarial challenge: EP-1038 analytic reduction

Public edition dated 2026-10-12. This retains the complete substantive mathematical report, with transparent editorial changes to private references and review-status wording. Independently authored executable checkers, raw interval certificates, full numerical records, detailed diagnostic outputs, and source copies are not included. Hashes identify omitted evidence but do not provide executable public reproducibility. The work is AI-assisted and unrefereed, with no external human peer review or formal proof-assistant certification. The exact cubic contact example below is an authored mathematical example, not a published program-input record.

Date: 2026-10-12 UTC.

## Disposition

**No blocking analytic defect or counterexample found.** I accept the finite-polynomial analytic implication from the explicit reference/certificate assumptions listed below to the strict global lower bound and finite nonattainment. This is conditional analytic acceptance, not a new execution or acceptance of numerical certificates, not an independent reproving of Tao's upper-extremum theorem, and not a uniqueness theorem for arbitrary relaxed minimizers.

The original 1989 circle reference has a published correction. To avoid relying on an uninspected version, use the primary theorem of Michael Christ and Marina Iliopoulou, *Inequalities of Riesz-Sobolev type for compact connected Abelian groups*, Theorem 1.1 and equation (1.3): https://preprint.press.jhu.edu/ajm/sites/default/files/AJM-christ-iliop.pdf. The inequality used here has no admissibility restriction. Its later equality and stability theorems are unnecessary.

I did not execute the author's software, linked Lean, or any earlier numerical verifier. I independently derived and ran six floating-point diagnostics of the main-width support and endpoint-adjoint identities. They are explicitly not certificates. The mathematical justification below does not depend on their accuracy.

## Sources and independence

- Retained [Wang manuscript](https://multiscalar.ai/results/erdos-1038/paper.pdf), SHA256 `3a7e857b12e59f24af17f36a30030b0ad6368c2d59955ef58e643400917565ad`. I read Sections 2–9 from its extracted text, with emphasis on Sections 2–5 and 8.
- Inspected the earlier [draft PR 1310 packet](https://github.com/AlecKriebel/Math/pull/1310), its mathematical audit, public source metadata, and exact acceptance scope. That historical packet accepted a fixed-candidate upper construction and left the global numerical gates open. The later end-to-end acceptance is recorded separately in this edition.
- Modern circle source: retained PDF SHA256 `40bd076e6f40ce4b907520f095ffc853ba117e0ddb2999c50e4199bcaf1aeab3`; Theorem 1.1/equation (1.3) checked in retained text and the primary public PDF. Its bibliography explicitly records Baernstein's 1995 correction.
- Before completing this analysis, the only information obtained from the separate end-to-end review was source identification and the modern circle citation; its draft analysis was not read.

## Exact assumptions accepted at the interface

1. For the one-cut family, independently validated Certificate 6.1 supplies its branch classification, unique global minimizing parameter, exact minimum L, and the stated enclosing inequalities, in particular L < 2.
2. For each finite k ≥ 29/20, a reference has a in [1,2), nonnegative reference probability density, and simple main crossings x− < 0 < x+ < a with the stated derivative orientations.
3. The certified scalar bounds imply the right side of (5.4) is strictly positive for every pair of normalized block masses in the full covering rectangle. The numerical cover includes the small-mass limits and all k regimes; it is not a sampled check of selected blocks.
4. Any hardcoded affine comparison value is an upper bound for the exact L. The established one-sided candidate bridge suffices because the normalized deficit is decreasing in L, with derivative −1/(q R0). Containment of L in an unnecessarily tight two-sided hardcoded interval is not required.
5. The elementary small-k inequalities are available with their strict rational margins, and the positive-platform recovery argument is retained.
6. Standard Pringsheim's theorem and the cited modern circle rearrangement inequality are external mathematical inputs. No equality classification from the circle theorem is needed.

Subject to these assumptions, none of the analytic challenges below leaves a remaining gap.

## 1. Finite atomization, endpoint roots, and contacts

Finite polynomials are a materially smaller class than arbitrary root measures. Their strict-sublevel boundaries are zeros of f²−1; therefore there are finitely many, none is a root of f, and all have potential exactly zero. A repeated root must first be treated as one distinct location with its positive multiplicity mass. A root itself has potential −∞ and is always interior to a negative component, including roots at −1 or 1.

For a component without a root, the potential would be strictly concave with zero boundary values, hence nonnegative inside. Thus every negative component contains root mass. Its finite weighted barycenter is strictly inside the component. Outside the old negative set, the root-coordinate logarithm is concave on every component, so simultaneous collapse raises the potential there. This proves containment, including every isolated contact point. Inside each old component, the new potential has one pole and cannot create a second negative component without a pole. Old distinct components cannot merge because the separating nonnegative points survive.

An isolated zero between two negative intervals is not an open gap, but it is enough: it still separates the strict-sublevel components. In a finite root-free gap W'' < 0, so any zero maximum is nondegenerate. There is no hidden higher-order flat contact or finite zero plateau.

**Concrete contact stress case.** Put k=2 and d=3/2^(2/3). In shifted coordinates the monic cubic is x²(x−d). In original coordinates it is (x+1)²(x−(d−1)), whose roots lie in [-1,1]. Its contact point is 2d/3, where |f|=1 and W'=0. The main left endpoint is −d/3, so its exact main width is d. Its two negative components share exactly one boundary point. This is a genuine finite-polynomial contact example, not a continuous-measure abstraction; the manuscript's contact convention treats it correctly.

Coalescing root locations cause no missing case. Equal locations are merged before the distinct-cluster formulas are used. At positive separation all logarithms of distinct distances are finite, however large their magnitude. At the zero-separation limit the appropriate representation has fewer clusters. No proof step needs a uniform positive inter-cluster distance over all finite configurations.

## 2. Orientation and endpoint normalization

For mean m≤0 and −1<x<0, |x−t|≤1−xt followed by Jensen gives V(x)≤log(1−xm)≤0. Equality in the whole chain would force a point mass of mean zero, hence δ0, for which the first inequality is strict. Thus the interval is genuinely negative.

The cluster c in this component is leftmost: any smaller root in [-1,1], including a root at −1, connects to the already negative interval. Translation by −c−1 leaves all roots in [-1,−c]⊂[-1,1] and retains nonpositive mean. If the original right boundary r0 obeyed r0−c<1, all its residual-root distances would be ≤1 and the principal distance strictly <1, contradicting product one. Therefore the translated boundary β≥0.

AM–GM at β>0 forces A≥1/2. At β=0 its equality case forces all residual roots to 1; the mean then again forces A≥1/2. This separate equality case is essential and is present. A=1 is a one-cluster polynomial of width 2; otherwise k=A/(1−A) is finite and at least one, and every residual d_i lies in [1,2]. Reflection preserves length and produces no orientation asymmetry left over in the normalized problem.

The main component contains (0,1), so residual components begin at or beyond 1. After removal of a residual self-pole its background is finite and strictly concave throughout that component. Interpolating its two boundary values gives R_i≤s^(u/(s+u))u^(s/(s+u))≤(s+u)/2, with the correct reversed inequality after dividing by −q_i. Shared endpoint contacts do not affect the disjoint sum of lengths.

## 3. Supporting functional and topology changes

The strongest apparent concern is that the interpolation T_s=(1−s)T0+sT need not stay in a single topological class. That concern does not invalidate this proof: convexity is established for finite algebraic partial sums on all positive coordinates, not by differentiating the actual width along the entire path.

Each coefficient times R^n is a positive sum of inverse-coordinate monomials. For one monomial m=product d_j^(−γ_j), its directional Hessian is

    m [ (sum γ_j v_j/d_j)^2 + sum γ_j v_j²/d_j² ] ≥ 0.

Consequently each finite odd truncation is globally convex. The common equal-mass partitions exist because finite empirical masses are rational, even though their barycenter positions need not be. At a fixed truncation, coefficients and first variations involve only finitely many inverse moments and the logarithmic mean. Bounds T≥1 and |T−T0|≤1 justify passing the partition limit before summing the infinite series. No separation assumption for the finite reference approximants is needed.

For the actual strictly separated reference, W''<0 on (0,a), and W'(x+)>0 implies the inverse branch remains regular all the way to x+. Positive inverse-series coefficients and Pringsheim rule out a nearer complex singularity. Pick a closed z-disk strictly beyond R but below its first positive singularity; positivity gives |Φ(z)|≤Φ(|z|)<a there. This uniform support separation lets the analytic implicit-function theorem differentiate with respect to a small bounded material perturbation, including the discontinuous atomic velocity. Cauchy bounds then yield convergence of the differentiated series. This fills the functional-analytic justification rather than presuming an infinite-dimensional convexity theorem.

At an atomic target contact, the positive critical point is unique because (log Ψ)'=1/y−sum q_i/[k(d_i−y)] is strictly decreasing from +∞ to −∞. Its inverse has a square-root endpoint but a finite real limit. The Abel parameter λ<1 keeps all evaluations inside the inverse disk. Nonnegative odd coefficients give monotone convergence of the target width as λ↑1, while the separated reference and its first variation converge absolutely. The proof never differentiates the target width at contact.

## 4. Moving endpoints and adjoint correction

Let F=A v in the reference spatial coordinate. For an interior point of an atomic target block, differentiation is direct: on the same block the logarithmic distance acquires exactly log(1−s), while off-block reference distances stay bounded away from zero for that fixed point. Thus the material derivative exists away from finitely many block boundaries. The platform derivative cancels the v(d) terms and gives

    g(d)=PV integral F(e)/(e−d) de_I(e),
    Mdot=−sum_j σ_j integral F(d)/(d−x_j) de_I(d).

The PV may be taken symmetrically in the spatial coordinate. Changing to angle at an interior point changes the two cutoff lengths by a ratio tending to one, so it introduces no finite correction.

The difference of these two pairings is a real endpoint functional:

    Mdot−integral g dξ=−F(2) Gamma,
    Gamma=σ−/K−+σ+/K+>0.

Two exact independent checks make its sign and endpoint transparent. If F=1, its finite Hilbert transform is zero and Mdot=−Gamma. If F=d, its transform is one; writing R0=D−σ−−σ+ and using K_j/(a−x_j)=(2−x_j)/K_j gives Mdot−R0=−2 Gamma. These are precisely −F(2)Gamma, not a left-endpoint term or the opposite sign.

For atomic velocities, F is piecewise analytic in angle with finitely many interior jumps. Subtract those jumps; the remaining continuous part has cosine coefficients O(n^−2), since its piecewise analytic derivative has bounded variation. Its transformed Abel sums are bounded by C(1+|log distance-to-endpoints|). Each jump contributes a difference of two logarithms divided by sin θ. It is logarithmic at that jump, and numerator cancellation keeps it bounded at 0 and π. These bounds give uniform integrability against the bounded angular adjoint density. The limiting identity therefore survives jumps and support-boundary blocks. Point values at the finitely many jumps are irrelevant.

For a finite target, v(2)=d_N−2≤0. Therefore the endpoint correction is nonnegative and the required one-sided inequality follows. Omitting this correction would be false. The exact contact example above also served as a diagnostic check of this nonzero correction; the detailed diagnostic value is omitted.

If a nonnegative reference density happens to vanish at the lower endpoint, neither the actual F=A v nor this transform identity requires division by A there. The finite-cosine calculation is an identity for F, which extends to the actual piecewise analytic F by the estimates just given. In the reference families actually used away from the soft edge, the positivity certificate is stronger in any event.

## 5. Positivity and exact mass bookkeeping

The adjoint numerator vanishes at a and has strictly positive derivative because σ±, K± and d−x± are positive. Hence it is positive on (a,2], behaves as O(d−a) at a, and has only an integrable inverse-square-root singularity at 2. Thus ξ is finite with R0>0.

The reference CDF is continuous and strictly increasing away from a possible single zero of its density at a. Every nonempty target quantile interval therefore corresponds to a spatial/angular interval of positive length, and has adjoint mass r_i>0. No endpoint or quantile boundary carries an atom. Consequently sum r_i=R0 exactly. Assigning half-open blocks does not change any integral.

Absolute integrability of mixed log energies follows from the angular chord identity: the diagonal and endpoint terms are logarithms of sin((θ−φ)/2) and sin((θ+φ)/2), integrable over the compact square. A and B are bounded in angle. This also covers adjacent blocks sharing an endpoint.

For off-block pairs, monotone target order gives the same sign as reference order; applying log y≤y−1 to absolute ratios is legitimate. Same-block ratios contribute exactly −1. The radius expression has its unique minimum at R_i=q_i r_i/2. This gives exactly E_i−q_i r_i log(q_i r_i/2)−C r_i. Summation uses the exact mass R0, not a probability normalization of ξ.

## 6. Circle rearrangement under density caps

The relevant extension is f(θ)=1_J(|θ|)A(|θ|)/A(π) and g(θ)=1_J(|θ|)B(|θ|)/B(π), with ordinary angular measure. They lie in [0,1], have masses 2Q and 2R, and need not themselves be symmetric decreasing. The modern theorem permits arbitrary nonnegative measurable functions; apply it to min(log 2−log|e^(it)−1|,N). Monotone convergence removes the truncation.

After rearrangement, convolution of nonnegative symmetric decreasing circle functions is symmetric decreasing. This follows by layer cake and centered-arc overlaps, including arcs longer than half a circle; the overlap can have a plateau but never reverses monotonicity. The cap-one bathtub argument first replaces f by the centered arc of mass 2Q, then replaces g by the arc of mass 2R. No equality or strict-admissibility hypothesis is used. Thus large, unequal, or support-touching blocks are all covered.

The normalization is important. The four even-extension quadrants give two copies each of the difference and sum kernels. Therefore the normalized physical chord energy is the circle energy divided by 2QR, and the arc result is twice the normalized arc cross-energy, not once. The Fourier expansion gives

    A(Q,R)=−sum_{n≥1} sin(nQ) sin(nR)/(n³ Q R).

Its square completion is exact. With h(Q)=A(Q,Q)−log(Q/π), the integral formula and monotonicity of sin u/u show h decreases to h(π)=0. Restoring q=A(π)Q/π and r=B(π)R/π yields exactly log(2H/[A(π)B(π)])+h(Q)+h(R)+sum(sinc(nQ)−sinc(nR))²/n−π Ceff/[A(π)Q]. No factors of two, π, or total adjoint mass are missing.

## 7. Strictness, tiny blocks, and exhaustive k coverage

If each normalized deficit is >δ(k)>0 for the chosen reference, each finite block contributes >δ(k) q_i r_i>0. There are finitely many blocks and their masses are positive; summing proves J_k>L. Atomization containment then gives the same strict inequality for the original polynomial. No equality analysis of the rearrangement theorem is needed.

There is no degree-independent positive surplus, and none is needed. At a hard lower reference edge with A(a)>0, a very short lower block has q proportional to angular width, while r is proportional to its cube because B(θ)=O(θ²). Hence q r can be of fourth order in its size. A tiny lower-block diagnostic corroborated this behavior; its detailed input and numerical output are omitted. Arbitrarily small positive block surplus is compatible with finite nonattainment and with empirical sequences approaching L.

Every normalized finite configuration is either A=1 or has finite k≥1. The elementary case covers [1,29/20]. The calibrated affine range begins earlier, at 36/25, and reaches 21/10; the constant-edge range reaches 21/5. For the zero-platform family,

    k(q)=−log q/log(2/(1+q)²)−1.

The numerator controlling −k'(q) is exactly (1+q)log(2/(1+q)²)+2q log q, positive before the soft endpoint. Thus k decreases strictly with q and tends to infinity as q↓0. The certified overlap k(41542/10^6)<21/5 and the exact shared q endpoint 26631/10^6 close the remaining ranges. No finite k=∞ endpoint is needed. Discontinuous changes of chosen reference between ranges cause no issue, since this is an existential comparison separately for each k.

In the terminal family C=0, so Ceff=(L−M0)/R0≤0 follows from the independently established one-variable global minimum. Discarding its favorable contribution is therefore noncircular: Certificate 6.1 does not use the global finite-configuration lower bound.

## 8. Strict sublevels, zero plateaux, and what is not proved

For a finite nonconstant polynomial the level set |f|=1 is finite, so replacing < by ≤ changes no length. This cannot be asserted for the limiting continuous reference: its support interval is a positive-measure zero plateau. The recovery proof correctly first changes the principal mass upward to create a positive platform, keeps the density nonnegative, and proves the new zero set consists of two simple crossings. Weak convergence then yields L1 convergence of logarithmic potentials, and the zero-set-null sign lemma applies. Only afterward is the positive buffer sent to zero. Thus no unjustified strict/weak-sublevel interchange is used.

The combination of finite strict lower bound with this recovery gives finite nonattainment. It does **not** classify all continuous relaxed minimizers, force convergence of every near-minimizing sequence to one measure, or prove uniqueness modulo reflection among arbitrary measures. The proven parameter uniqueness is only within the specified one-cut family.

## Independent diagnostics

The separately authored diagnostic program uses only standard Python, SciPy quadrature, and SciPy root isolation; the program and its detailed outputs are omitted from this edition. It derives reference integrals from the angular primitives

    U(φ)=2/sqrt(2a) arctan(sqrt(2/a) tan(φ/2)),
    H_θ(φ)=log|sin((θ+φ)/2)/sin((θ−φ)/2)| / (r sin θ),

and computes g directly from off-block pole integrals, rather than calling the manuscript verifier or recycling its Hilbert-transform implementation.

Six fixtures cover the exact cubic contact; a target endpoint at 2 (zero correction); three discontinuous quantile blocks with top endpoint below 2; roots separated by only 10^−8; a tiny lower block; and a tiny upper block with another target atom below the reference support. The maximum observed endpoint-identity residual is below 1.8×10^−10; each tested supporting surplus is positive; block adjoint masses add to the independently integrated total to rounding error. The coalescing-root and other multi-atom fixtures test the support/adjoint identities, not necessarily the stronger one-cluster-per-residual-component premise needed for the radius lower bound. The output states this is diagnostic evidence, not a rigorous certificate.

## Final acceptance boundary

The mathematical reductions survive the targeted challenges. The deliverable should retain (i) the corrected/modern circle citation, (ii) the exact endpoint correction and one-sided top-endpoint sign, (iii) the separated-reference/contact-target distinction, (iv) the complete numerical gates and their one-sided L bridge, and (v) the positive-platform recovery. Removing any of these qualifications would overstate what was checked. There is no additional analytic blocker to the claimed finite-polynomial lower bound once those exact gates are satisfied.
