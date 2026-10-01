# Complete independent real / orthogonal-family audit of original PR25

**Family verdict: PASS for the original conservative source-only package. The stronger external square real theorem is independently reconstructible and passes this family's mathematical audit.** The reconstructed strongest result is

\[
\alpha_{\mathbb R}(N+1)-\alpha_{\mathbb R}(N)>\frac1{160N^2}
\quad\text{for every integer }N\ge1,
\]

with independent real N(0,1) entries and alpha_R(N)=N^(-3/2) E Tr sqrt(XX^T). This is validation of Hutnik's result, not a new solution, novelty claim, publication, or campaign attempt. Parent owns the combined adversarial gate and any current dated candidate repair. The original record's unsolved/source-hold outcome and 0/5 budget remain its accurate historical outcome.

The exact original head is `aa99d4a36eff79cbb7aae55ce3ffe4a0eb31af95`. All16 frozen attempt files match both their manifest and that Git head. Original SOURCE_AUDIT SHA256 is `99ae40a387e00e5d2c46ed8db4e479170092b2484cf237f83629ba5e1201ec8e`. No original/canonical, shared queue, branch, Git, PR, publication, or installation mutation was performed. This family wrote only inside `real_family/`; raw sources and replay scripts live in its ignored `tmp/`.

## Independence and sealed criterion

Before reading original historical detailed reports or any submitted checking script, I read the complete Bandeira2013 target, full MIT2015 handout, actual Hutnik real v2 square proof chain (Proposition2.2, Theorem2.5, coefficient lemmas, Proposition3.4, AppendixA.1), actual Livan--Vivo underlying density/scaling, and all AP material needed for its upper-bound proof (kernel, moment recurrence, generating function, singularity analysis, asymptotic constant, full Section4 proof). The hypothesis/quantifier/normalization map was sealed at 2026-10-01T20:56:01Z. The saved seal hashes `SEALED_RECONSTRUCTION.md` to `70a117a04a7d9e0548c27bf3d3bc85f110607374796227ce2ccb0bac37da907b`.

The criterion required every integer dimension, both parities, small dimensions, all signs/scales, analytic interchanges, and the complete decrement-bound dependency, not an extrapolation from finite dimensions. Historical review and scripts were read only after sealing. No sibling detailed report or script was used. The family mechanism is direct joint-law skew-matrix derivation plus positive-series/differential reconstruction of the imported bound.

## Actual proof dependencies and their resolution

The full reconstruction is in `DERIVATION.md`, and is intended to be checked equation by equation.

1. **LOE identity and scale — closed independently.** The raw real joint law uses weight x^((lambda-1)/2)e^(-x/2), while standard complex variance-one LUE uses x^lambda e^-x. The direct skew form B and polynomial operator Df=xf'+((lambda+1)/2-x/2)f satisfy B D=-2 diag(Gamma(j+lambda+1)/j!). This yields the finite inverse for even N and the explicitly bordered inverse for odd N. Differentiating the finite de Bruijn Pfaffian gives the one-point density. Its exact psi recurrence and Gamma duplication reproduce Hutnik Phi1/Phi2 and every normalization factor. This does not rely on an arXiv assertion being correct simply because it is printed. Livan--Vivo Eq16 separately agrees after the x=2y Jacobian. In particular odd N has the indispensable phi_(N-1)/v_(N-1) border; N1 reduces to the elementary chi-square/Gamma density.
2. **Abel completion — closed.** The parity Beta integral and Laguerre generating function reproduce the incomplete-Gamma term. Integrated fixed monomials have an explicit majorant proportional to (1-z^2)^(omega-1), omega=(lambda+1)/2>=1/2. Termwise integration at zeta<1 is justified by a Cauchy coefficient bound and an integrable exponential tail. At the boundary the ordinary diagonal tail decays as m^(-omega-3/2), at least m^-2. Thus the sign and adjacent-dimension arguments operate on absolutely convergent sums. They do not hide an unproved rearrangement at shape zero.
3. **Connection signs and coefficients — closed.** The shifted Laguerre norm makes Q a finite convolution of sqrt(1-z) coefficients. Absolute Fourier convergence proves kappa_d=1/[pi(d^2-1/4)] and a positive Beta/Tonelli computation proves theta_d=1/[pi(2d+1)]. Explicit finite products prove E>=0 and E decreases with the first index. The completed index is N-1+2u for both parity choices. Coefficient ratios are below one for every u, at lambda0 and N>=3; their universal proof uses the exact shape derivative and a telescoping ratio at shape1, not a finite set of u values.
4. **AP universal decrement upper bound — closed by reconstruction.** Positive Laguerre connection coefficients yield H(z)=sqrt(pi)/2 z(1-z)^(-5/2)2F1(-1/2,-1/2;1;z). Conjugating the hypergeometric ODE gives the moment recurrence for every n, without importing the Carlson-continuation theorem as an unexplained premise. The logarithmic continuation formula, analytic Delta-domain remainder and standard transfer theorem determine the needed E_n limit. The coefficientwise q estimate and independent alpha_C auxiliary upper bound prove decreasing E_n; then its limit gives Delta_n>0 and alpha_C above its limit. Only afterward does the first positive q coefficient yield the strict upper bound by telescoping. This dependency order is noncircular, and uses no withdrawn2016 Lemma1.
5. **Reserve and small dimensions — closed.** For N>=3 one positive diagonal dominates 1/[8pi N(N+1)], and subtraction of the certified AP bound gives the displayed pointwise reserve. The harmonic inequality is an induction starting at N4; all constants are non-asymptotic. The coefficient-ratio polynomial at N=t+3 has all positive coefficients. Direct joint-law half-moments and rational interval enclosures close N1,2,3 independently of the asserted Appendix integrals.

The standard mathematical inputs remaining explicit are Gamma/Beta and Laguerre identities, finite determinant/Pfaffian expansion, the hypergeometric continuation/ODE, and the standard Delta-domain coefficient transfer theorem; they have been applied within their stated domains. They are not renamed versions of the target inequality. This audit is ordinary analytic verification, not machine formalization. No central unsupported dependency was identified in the square route after the supplied reconstruction. The broader rectangularity-transition theorems and quantitative shape asymptotics are outside this square theorem certification.

## Falsifiable controls and reproduced receipts

`controls.py` uses Python standard-library exact fractions. Its direct real moment route starts with the MONOMIAL joint-density determinant and de Bruijn differentiation. Polar integration x=s^2,y=t^2 computes skew entries and moment variations exactly, then rational matrix inversion gives the moments. A separate route integrates the printed one-point formula, including incomplete-Gamma integrals. They agree exactly for N1..8, both parities. This tests a genuinely independent density premise, not two calls to the same formula.

The first values are

\[
Y_1=\sqrt{2/\pi},\quad
Y_2=\sqrt\pi(2-\sqrt2/2),\quad
Y_3=3\sqrt\pi/2+2\sqrt{2/\pi},\quad
Y_4=\sqrt\pi(153/32-3\sqrt2/4).
\]

The code constructs a rigorous rational pi enclosure by Machin's alternating arctangent formula and bounds radicals with integer square roots. The resulting rational intervals prove the reserve in dimensions N1..7. Floating decimals in `CONTROL_RESULTS.json` are explicitly illustrative; no floating value decides a pass. It also checks the independent AP positive-convolution recurrence through n40 and relevant coefficient bounds. The final run has **689 executed exact assertions, 201 distinct assertion names**; 552 executions concern repeated angular cancellation while moments are recomputed. This count is reported transparently and is not a numerical-universality argument.

The original author script, its historical identical review copy, and the historical independent script were copied unchanged into ignored tmp and replayed. Their 383,383,53 passes and produced receipts exactly match the frozen receipts, including scopes and false real-proof-certified flags. `PACKAGE_CHECKS.json` and `INTEGRITY_RESULTS.json` record exact receipt equality and all16 original-head file matches. Two early local harness mistakes were detected by the independent exact controls and corrected before issuing the final receipt; neither was a source defect.

## Source, historical, and budget handling

Fresh [Hutnik real v2](https://arxiv.org/pdf/2608.12151v2), [AP v1](https://arxiv.org/pdf/2609.07802v1), and [MIT original handout](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-of-data-science-fall-2015/a9963e8f7bd9c10b4d48df8115f63116_MIT18_S096F15_Open1.2.pdf) bytes match the original provenance SHA256 values. `SOURCE_RECEIPTS.json` supplies these and freshly fetched official metadata/withdrawal pages. Hutnik v2 revision dates, AP7September submission versus9September PDF front-matter date, and Baslingker--Dan27August submission agree with the recorded distinctions. The official [1606.00494v3 notice](https://arxiv.org/abs/1606.00494v3) names Abreu, marks6March2023 withdrawal, and explains the incorrect Lemma1/hypergeometric substitution. Current source pages show no withdrawal or journal-reference field for the four2026 preprints; that observation does not assert human review.

The full target in [Bandeira2013](https://afonsobandeira.wordpress.com/2013/11/01/a-conjecture-on-the-singular-values-of-a-gaussian-matrix/) and MIT uses exactly square size, entry scaling1/sqrt(N), and opposite real/complex directions for every N. Shape zero is the square case. Fixed positive integer shape changes the number of columns with N; noninteger shape is not a Gaussian matrix of noninteger dimension. No rectangular assertion replaces the original problem.

The preserved imported `prior_report.json` contains wrong attribution and invalid old claims, followed by its withdrawal correction. This package labels it historical and explicitly rejects its false inference; it does not reuse the malformed integral or invalid bounds. The original status/hold, false new-discovery flag, 0/5 budget and qualified finite controls are mutually consistent. Git history shows audit addition at94641588 on2026-09-30 04:49UTC and the queue-only head ataa99 on04:54UTC. The historical attempt's null PR and queue-modified=false fields precede the coordinator's queue update and are not current live-state records.

One provenance limit remains historical rather than mathematical: the16 files do not contain raw receipts for the reported04:36UTC all-state PR query. The old `source_revision`37e53 predates the queue/related-group paths, so it cannot replay that negative search baseline. Exact Git history does support that the selected attempt directory was first added at94641588, but this family does not claim to independently prove every past global-search negative. This limit is not a theorem dependency or grounds to reject the carefully qualified source-only package.

## Findings and disposition

No fatal source-proof gap, counterexample, normalization error, incorrect strictness, or failed original control was found. There is one minor source indexing omission: AP Lemma6 is printed for q_j with j>=2, while Section4 needs q1 too. Its displayed proof is valid for every0<t<1 and covers q1 at t1/2, so no new lemma or unbounded search is needed. The minimal repair is to state j>=1 or explicitly note the t1/2 case in the audit; the original candidate need not be edited solely for this external paper wording.

**Strongest verified result:** the universal square real strict reserve, with the complete reconstructed dependency chain above and separately checked finite exceptions. **Exact remaining mathematical gap for that result:** none identified at ordinary analytic-proof standard; separate cross-family adversarial scrutiny and the parent's fresh gate remain process requirements before promoting a combined assessment. No computer-formal proof or certification of the broader rectangularity results is claimed.

**Original source-audit disposition:** acceptable as the source-only unsolved partial it actually was. Preserve its historical validation hold and 0/5 budget; add any stronger current certification as a new dated assessment only after the parent-owned gate. Validation adds0 central proof-search attempts and gives0 novelty/solved-discovery credit. No GitHub release, publication, installation, or contact with an outside individual was performed or proposed.
