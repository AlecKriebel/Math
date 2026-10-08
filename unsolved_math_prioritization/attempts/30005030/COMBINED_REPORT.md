# Combined accepted report and required scope addendum

The two frozen originals below must be read together. See INDEPENDENT_ACCEPTANCE.md for the full audit. The report's historical verify.py instructions are superseded by the explicit portable and source-backed audit_verify.py modes described in README.md; the original wording is preserved unchanged.

## Frozen REPORT.md begins

# Temporal integrability cannot generally lower the fractional SDE uniqueness threshold

Problem 30005030, OWR-9790360-001. Source-scoped literature resolution, 7 October 2026.

## Conclusion

The proposed universal improvement is refuted by an existing 2026 preprint theorem, already for ordinary, spatially Hölder drifts in dimension two. This is a literature-based negative answer, not a new counterexample or an independently verified proof of that preprint. The precise reduction below is elementary and independently checked. It does not settle every dimension, Hurst parameter, endpoint, or solution notion.

## Original mathematical target

Galeati's contribution to OWR 9/2022, printed pages 469–471, asks whether increasing the temporal exponent beyond two permits improvement of the spatial threshold for additive fractional SDEs. Equation (2) gives the scaling boundary, while Theorem 1 supplies strong existence, pathwise uniqueness, and path-by-path uniqueness above the older boundary. The passage considers arbitrary dimension; ordinary fBm has H in (0,1), and the displayed theorem also discusses its integrated extension to noninteger H>1. The clean question is faithful. The separate question A on page 470 has a missing-looking term; the final question and Theorem 1 unambiguously specify the boundary used here. [OWR]

Write

A(H)=1-1/(2H),   S(H,q)=1-1/H+1/(Hq),

with 1/infinity=0. The proposed general criterion is alpha>S(H,q) for drifts in L^q([0,T];C^alpha(R^d;R^d)). For positive noninteger alpha, C^alpha means the bounded usual Hölder class; negative alpha requires a distributional convention.

## The decisive prior theorem

Hess-Childs and Rowan, Corollary 1.11, PDF page 5, give in dimension two, for H in (1/2,1) and 0<=alpha<A(H), a randomly constructed drift with uniformly bounded C^alpha norm and pathwise nonuniqueness from any fixed deterministic initial point. The drift randomness is independent of fBm; fixing a suitable realization yields a deterministic drift. The solutions satisfy the ordinary Carathéodory integral equation and the nonanticipation condition of Definition 1.14. Thus no distributional enhancement is involved. [HR]

For this argument fix one point, say x0=0, before selecting the realization. No simultaneous assertion over uncountably many initial points is needed.

## Reduction to the temporal question

Assume the cited theorem. Fix H in (1/2,1) and q in (2,infinity]. Then

A(H)-S(H,q)=(1/2-1/q)/H>0,   0<A(H)<1/2.

Set M=max(0,S(H,q)) and choose alpha=(M+A(H))/2. It follows, using only these inequalities, that

0<alpha<A(H)<1/2,   alpha>S(H,q).

Apply the prior theorem at this alpha and select a deterministic realization b giving nonuniqueness at x0=0. Since the time interval is [0,1],

||b||_(L^q_t C^alpha_x) <= ||b||_(L^infinity_t C^alpha_x)

for every finite q, and the infinity case is immediate. Thus b satisfies the proposed scaling condition and the required temporal assumption, but pathwise uniqueness fails. Failure of pathwise uniqueness also rules out path-by-path uniqueness: a path-by-path unique equation would force any two compatible stochastic solutions using the same noise and initial point to coincide.

A concrete parameter witness is

H=3/4, q=4, alpha=1/6;
S(H,q)=0 < 1/6 < A(H)=1/3.

The scaling exponent is 1-H-1/q+H*alpha=1/8>0. The drift supplied by the theorem therefore lies strictly inside the proposed scaling-subcritical region. This is an existence-based witness through the cited construction, not an explicit numerical formula for one selected drift.

For d>2, extend b to (b_1(t,x_1,x_2),b_2(t,x_1,x_2),0,...,0). Couple each nonunique two-dimensional solution with the same independent remaining fBm coordinates. The Hölder bound and nonanticipation are preserved, and distinct first coordinates still give distinct solutions. Dimension two alone already disproves a dimension-uniform assertion.

Consequently, for each H in (1/2,1) and each q>2, temporal L^q membership alone cannot replace A(H) by the lower scaling boundary S(H,q). Indeed the obstruction persists even with time-essentially-bounded Hölder norm.

## Nearby results and scope limits

Galeati–Gerencsér's published Theorem 1.4 assumes q in (1,2] and alpha>S(H,q), with alpha<1. Taking q=2 and using finite-time embedding covers larger q only above A(H). Their Theorem 1.5 is weak existence under alpha>max(1/2-1/(2H),S(H,q)) for ordinary fBm; it is not a strong uniqueness theorem. [GG]

Butkovsky–Mytnik establish weak uniqueness for autonomous distributional drifts when 0<H<1/2 and alpha>1/2-1/(2H). This is a distinct conclusion with different hypotheses. [BM]

Gu–Yu's 2026 Theorem 1.1 concerns Lebesgue-space drifts, with H<1/2, p>=2, Hq>=1 and 1/q+Hd/p<1-H. It cannot establish the full Hölder/Besov assertion: the embedding from L^p to negative Hölder regularity is one-way. [GY]

The present negative conclusion does not assert a result in dimension one, at alpha=A(H), for autonomous drifts, or for H>1. For 0<H<1/2, HR Section 1.4 explicitly leaves actual pathwise nonuniqueness open; its general explosive-separation theorem is not itself a nonuniqueness theorem at time zero. Its Brownian result, Theorem 1.3, separately supplies negative-regularity counterexamples in dimension two. [HR]

Pathwise nonuniqueness by itself does not imply absence of all strong solutions. That stronger conclusion for the non-Brownian counterexamples is not claimed here. Nor is weak uniqueness for those examples asserted.

## Verification and reproducibility

The original pages and decisive PDF page were visually inspected. The PDF, abstract record, and author publication list identify HR as a preprint; no peer-reviewed publication was verified. Its downloaded PDF is dated 28 April 2026, and arXiv records v1 submission on 26 April. The experimental HTML instead displays 24 August; the PDF's theorem and version are the frozen authority here. [HR, Author]

The prior-corpus semantic gate examined 15,458 problem records and 6,701 reports. It found no earlier report for this problem or semantic duplicate of the threshold question. Nearby records concerned density estimates, Lévy-area approximation, volatility, or unrelated mixing questions. Dataset hashes and source hashes are recorded separately; corpus contents and copied scholarly documents are excluded from this authored payload.

Run `python verify.py` to reproduce exact rational parameter checks and payload/source-manifest consistency checks. These validate the reduction and provenance; they do not verify the cited probabilistic construction. No simulation is offered as proof. Work stopped at the prior-result gate rather than fabricating five new approaches to a universally refuted criterion.

## Public references

- [OWR] L. Galeati, “Some recent advances on SDEs with fractional noise,” in OWR 9/2022, pp. 469–471. https://doi.org/10.4171/OWR/2022/9
- [HR] E. Hess-Childs and K. Rowan, “Sharp pathwise nonuniqueness for additive SDEs,” arXiv:2604.23883v1 (2026), especially Corollary 1.11, Definitions 1.1 and 1.14, Section 1.4. https://arxiv.org/abs/2604.23883v1
- [Author] K. Rowan, research list, inspected 7 October 2026. https://keeferrowan.github.io/
- [GG] L. Galeati and M. Gerencsér, “Solution theory of fractional SDEs in complete subcritical regimes,” Forum of Mathematics, Sigma 13 (2025), e12. https://doi.org/10.1017/fms.2024.136
- [BM] O. Butkovsky and L. Mytnik, “Weak uniqueness for singular stochastic equations,” arXiv:2405.13780v2 (2025). https://arxiv.org/abs/2405.13780v2
- [GY] J. Gu and Q. Yu, “Strong solutions to SDEs with singular drifts driven by fractional Brownian motions,” arXiv:2602.04303v2 (2026). https://arxiv.org/abs/2602.04303v2

## Frozen REPORT.md ends; required SCOPE_ADDENDUM.md begins

# Deterministic drift and solution class checks

This addendum supplements the frozen REPORT.md without replacing it. It clarifies the stochastic meaning of the counterexample and the narrower positive results. References use the report's labels.

## Deterministic selection preserves stochastic nonanticipation

The invoked result is HR Corollary 1.11(1), PDF page 5. Its quantifier is: for each deterministic initial point, for almost every drift realization, pathwise nonuniqueness holds for the SDE. Fixing the initial point before selecting a drift is therefore sufficient. We do not merely select from a statement of nonunique solutions for individual forcing paths.

The source's proof makes the order explicit. Theorem 2.5, page 14, converts explosive separation to stochastic nonuniqueness. Lemma 6.1, pages 24–25, establishes a full-measure set of drifts for a fixed initial point. The proof of Theorem 2.5, page 26, fixes one such drift and constructs a two-point process driven by (W,W). Lemma 6.2 preserves the weak-solution property under its weak limit. Its Appendix A proof, pages 29–30, specifically preserves the nonanticipation identity (A.1). These are inspected proof dependencies, not a certification of the full multiscale construction. [HR]

There is also an elementary way to check that the stated result provides a common compatible filtration. Fix the drift and take the weak solution furnished by Corollary 1.11(2). Disintegrate its joint law as

mu(dX,dW)=K(W,dX) P_H(dW).

By the nonanticipation condition, the projected conditional kernel K_t(W,·), governing X restricted to [0,t], is measurable with respect to the past W restricted to [0,t]. Equivalently, for each bounded Borel past functional f, the function W↦integral f(X)K(W,dX) depends only on that past.

Define the conditionally independent coupling

nu(dX1,dX2,dW)=K(W,dX1)K(W,dX2)P_H(dW).

Its two marginals are mu. Its joint past kernel is K_t⊗K_t, which remains measurable with respect to the past of W: first check products of bounded Borel test functions, then apply the monotone-class theorem. Thus the joint pair cannot reveal future noise; one may use the common canonical filtration generated by (X1,X2,W), with completion.

For any fixed epsilon>0, K_epsilon is non-Dirac for almost every W by the cited corollary. For a probability measure eta on a Polish path space,

(eta⊗eta){(x,x):x in the path space}=sum_a eta({a})^2,

where the sum is over atoms. This quantity is strictly below one whenever eta is not Dirac. Applying this to K_epsilon and integrating shows

nu(X1|_[0,epsilon] != X2|_[0,epsilon])>0.

Therefore pathwise uniqueness fails with a jointly compatible pair, rather than only with individually nonanticipating marginal solutions. This conditional-product argument is independent of how the prior paper builds its drift. It does not infer nonexistence of every possible strong solution.

## Precise restricted positive results

The BM reference in REPORT.md should be read with its regularity-class qualifier. Theorem 2.9 covers 0<H<=1/2, autonomous b in C^alpha, alpha>1/2-1/(2H), and weak uniqueness in V((1+H)/2). Here V(kappa) requires, for every m>=2, uniformly bounded L^m Hölder-kappa increments of X-B^H. Distributional solutions use smooth-drift approximation as in Definition 2.7.

For d=1, BM Theorem 2.12 also gives strong existence and pathwise uniqueness within that class if either

(1+alpha*H)(alpha+1/(2H))>1/2

or b is a nonnegative measure. No externally supplied enhancement is part of those hypotheses. [BM]

For example, H=1/4 and alpha=-11/10 have old boundary -1, weak boundary -3/2, and product (29/40)(9/10)=261/400>1/2. Thus the restricted autonomous one-dimensional theorem really does go below the older threshold. This does not contradict the dimension-two time-dependent counterexamples or establish the proposed universal temporal-integrability criterion.

## Classification discipline

The defensible disposition is: a source-verified preprint theorem refutes the dimension-uniform strong/pathwise-uniqueness criterion based solely on the scaling inequality. Do not state that every special case is settled, that HR has been independently proved here, or that its preprint has verified peer-reviewed status. The original broad question must retain these qualifiers when summarized.

## Required SCOPE_ADDENDUM.md ends
