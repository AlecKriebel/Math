# Independent skeptical priority and implication audit

PR1216 / problem 30000921. Audit date: 17 October 2026. This is a research-audit artifact, not a paper, submission, publication, or novelty certificate.

## Verdict

**POSITIVE EARLIER GENERAL IMPLICATION FOUND.** The negative answer, each-fixed-polynomial dense counterexamples, the simultaneous-all-nonconstant-polynomials strengthening, and the classification of universally preserving polynomial multipliers all follow from an older random-series theorem plus elementary estimates. The simplest identifiable source is Miika Nikula, Theorem 1 of arXiv:1209.6209v1 (27 September 2012), subsequently published online on 8 October 2013 and in *Complex Analysis and Operator Theory* 8(7) (2014), 1455–1474, DOI [10.1007/s11785-013-0328-0](https://doi.org/10.1007/s11785-013-0328-0). A specialization of Bayart–Matheron, Proposition 3.3 in arXiv:1112.1289v1 (6 December 2011), supplies an even earlier route to the same Gaussian model.

I have not found a source explicitly printing the exact polynomial-multiplier corollary. That distinction does not erase the prior implication. The defensible framing is an elementary corollary or independent rediscovery and clarification of a consequence of established random hypercyclicity. Do not promote the basic answer or the stronger simultaneous conclusion as a new research discovery on the basis of this audit. This verdict is positive mathematical overlap, rather than an inference from unsuccessful searches.

## Scope and independence

The target is pointwise multiplication: whether `f in HC(D)` implies `p(z)f(z) in HC(D)` for every nonconstant polynomial p. It is enough for prior overlap to obtain a single nonconstant p and a single counterexample. Exact copying of the submitted specimen or the same proof mechanism is not required. The submitted proof and source manifest were read to determine this target. No sibling priority report, parent conclusion, or the separate new-annulus proof report was read before the independent positive finding was frozen in `POSITIVE_IMPLICATION_FREEZE.md` at 18:24:32 UTC. None has been read in preparing this final report either.

No contacts or outreach drafts were made. No Git/index, candidate, external-app, or publication mutations were performed. Source bodies and rendered source pages are held only in ignored `sources/` here. `SOURCE_RECEIPTS.json` records whole-file retrieval hashes; retrieval and inspection scopes are separate.

## A. Primary theorem and complete deduction

### A1. What Nikula actually proves

[Nikula's arXiv record](https://arxiv.org/abs/1209.6209) identifies v1 as submitted 27 September 2012 at 12:45:47 UTC. The complete [v1 PDF](https://arxiv.org/pdf/1209.6209v1), Theorem 1 on PDF pages 2–3, says that the exponential generating series with independent identically distributed complex coefficients is almost surely entire and frequently hypercyclic for differentiation if their law has support all of C and a mild logarithmic tail bound. Circular standard complex Gaussians meet these hypotheses. The source's proof occupies pages 6–10 and was read; the theorem pages were also rendered and visually checked. The published publisher record independently confirms the authorship, model, online date, issue date, and DOI. The local v1 PDF has a later TeX-generated date on page 1; the arXiv version history, rather than that compilation date, is the historical timestamp. The published full PDF was not obtained in this audit, so exact numbering is claimed for arXiv v1 only.

### A2. Gaussian bounds, with explicit probabilities

Let X_0,X_1,... be independent standard circular complex Gaussians, of density

    (1/pi) exp(-|z|^2).

Then

    P(|X_n|<r) = 1-exp(-r^2) <= r^2,
    P(|X_n|>R) = exp(-R^2).

Set alpha=3/4. Both series

    sum_{n>=1} P(|X_n|<n^-alpha),
    sum_{n>=1} P(|X_n|>log(n+e))

converge: the first is bounded by sum n^-3/2; the second has terms exp(-log(n+e)^2), bounded eventually by n^-2. First Borel–Cantelli therefore gives, on one probability-one event, an N such that

    n^-3/4 <= |X_n| <= log(n+e)   for every n>=N.                 (A.1)

Intersect this event with the probability-one conclusion of Nikula's theorem. Thus there exists (indeed almost surely there is) an entire frequently hypercyclic function

    f(z)=sum_{n>=0} X_n z^n/n!

with (A.1). This use of probability is an existence proof, not empirical simulation.

### A3. One event works for every polynomial

Take any nonconstant complex polynomial p(z)=sum_{j=0}^d p_j z^j, where d>=1 and p_d!=0. For n>=d, Leibniz gives

    (pf)^(n)(0)=sum_{j=0}^d p_j (n)_j X_{n-j},
    (n)_j=n!/(n-j)!.

For n large enough depending on N,d, the leading term has modulus at least

    |p_d| (n)_d (n-d)^-3/4 >= c_p n^(d-3/4),

where c_p>0. The sum of all lower-degree terms has modulus at most

    sum_{j<d} |p_j| (n)_j log(n-j+e)
      <= C_p n^(d-1) log(n+e).

Consequently

    |(pf)^(n)(0)|
      >= c_p n^(d-3/4)-C_p n^(d-1)log(n+e) -> infinity.          (A.2)

The ratio of the lower-term bound to the leading-term bound is O(log(n)/n^(1/4)), which tends to zero. For d=1 the leading power is n^(1/4), so the boundary case works as well. Nonreal coefficients and phases cause no problem because the reverse triangle inequality was used. The zeros and root multiplicities of p are irrelevant to this argument.

Crucially, (A.1) was established before p was chosen and implies (A.2) deterministically for every finite list of polynomial coefficients. There is **no uncountable intersection of probability-one events**. One f simultaneously defeats every nonconstant complex polynomial.

If a scalar sequence tends in modulus to infinity, each bounded disk contains only finitely many sequence values. Its range cannot be dense in C. Evaluation at zero is continuous and onto from H(C) to C; hence the derivative orbit of pf cannot be dense in H(C). Thus pf is not HC(D), for every such p. In particular p(z)=z already gives the historical negative answer.

### A4. Density and multiplier classification

For any polynomial q, sufficiently high derivatives of f+q equal those of f. Thus f+q is still frequently hypercyclic and has exactly the same eventual coefficient bounds. The preceding argument applies to every f+q. Since C[z] is dense in H(C), the translate f+C[z] is dense in H(C). Therefore a dense set of frequently hypercyclic functions simultaneously fails every nonconstant polynomial multiplier. This is stronger than each fixed p having dense counterexamples.

Every nonzero constant multiplier preserves HC(D) by scalar multiplication of the dense derivative orbit. The zero multiplier does not. Combining these facts with the counterexamples above yields exactly the nonzero constants as universally preserving polynomial multipliers.

### A5. Comparison with the proposed n^-1/2 annuli

A raw Gaussian realization does not have the eventual lower bound n^-1/2: its small-ball probabilities are asymptotic to 1/n and the independent events occur infinitely often. It would be a quantifier/error-of-bound mistake to attribute that exact bound directly to Gaussian samples.

If the exact eventual annuli are wanted, an elementary null-orbit correction obtains them. For n>=1 set b_n=X_n when |X_n|>=n^-1/2, and b_n=n^-1/2 otherwise. Put c_n=b_n-X_n, so |c_n|<=2n^-1/2. Define h(z)=sum c_n z^n/n!, with any finite choice at n=0. Then for each R,

    ||D^m h||_R <= exp(R) sup_{n>=m}|c_n| -> 0.

The function F=f+h remains frequently hypercyclic: visits of f to a sufficiently smaller disk-neighborhood of an arbitrary target have positive lower density, and the eventually small perturbation retains those visits. The eventual Gaussian upper bound survives the clipping, so

    n^-1/2 <= |F^(n)(0)| <= log(n+e)

eventually. Highest-degree dominance now has leading size n^(d-1/2) and lower size O(n^(d-1)log n), proving simultaneous escape again. Polynomial additions again give density. The exact annular existence conclusion is therefore also an elementary corollary of Nikula plus a standard null-orbit perturbation. This audit does not assert that either Nikula or Bayart–Matheron printed that clipping argument.

## B. Earlier Gaussian-measure theorem route

[Bayart–Matheron arXiv:1112.1289v1](https://arxiv.org/abs/1112.1289), posted 6 December 2011 at 14:35:24 UTC, Proposition 3.3 (PDF pp. 14–15), gives Gaussian mixing for an eigenfield E whose associated integral operator is gamma-radonifying, spanning, and has the required Fourier-decay property. The paper's initial context explicitly includes complex separable Fréchet spaces. The introduction on p.1 explains that ergodicity with full support implies almost-everywhere frequent hypercyclicity. This version's pp.37–39 discuss relevant weighted shifts and convolution operators; it does not contain the later explicit D-Gaussian remark.

Here is a checkable specialization, not a quotation of a theorem about polynomial products. Take X=H(C), T=D, the unit circle with Haar probability m, phi(lambda)=lambda, and

    E(lambda)(z)=exp(lambda*z),
    K_E u = integral_T u(lambda) exp(lambda*z) dm(lambda).

Then D E(lambda)=lambda E(lambda). Fourier basis vectors are taken by K_E to the monomials z^n/n! or zero. The associated Gaussian series is exactly sum g_n z^n/n!. It converges absolutely on every compact almost surely because the expected sum of its radius-R term norms equals E|g_0| exp(R)<infinity. This verifies the gamma-radonifying condition for this particular K_E. Every monomial belongs to its range, giving the spanning/full-support condition. For S=c_0, Fourier decay for all L^1(m) densities is the Riemann–Lebesgue lemma. Proposition 3.3 therefore makes D strongly mixing for this Gaussian series law, and the p.1 ergodicity implication gives almost-sure FHC(D). Section A2–A4 now applies unchanged.

This identifies an older general theorem from which the Gaussian instance can be derived, already in 2011. No claim is made that it is the earliest possible theorem. An author-hosted later 51-page version explicitly states the Gaussian D-hypercyclic model in Remark 2 after Proposition 8.1, p.41, and cites Nikula; the exact date of that author-hosted file is not certified, so it must not be backdated to the 2011 v1. The journal citation is *J. Reine Angew. Math.* 715 (2016), 75–123.

## C. Negative and nearby routes: exact limits

| Source/route | Actual checked mechanism | Why it does not itself give the requested negative answer |
|---|---|---|
| Costakis (2008), printed p.330 / PDF p.34 | Definition 4, Theorem 6, Question 5; contribution and references read on PDF pp.32–35 | Theorem 6 is positive for a residual family simultaneously under all nonzero polynomial multipliers. Question 5 asks the all-HC-vectors statement. Residual good and dense bad can coexist. |
| Costakis (2010), Theorem 1.7, PDF p.5 / printed p.207; proof in Section 6 pp.21–22 | Residual common HC vectors for n^b D^n for all real b | Existence/common genericity does not imply equality of all HC sets or universal pointwise multiplier preservation. This source was fully available and successfully retrieved. |
| Bernal–Conejero–Costakis–Seoane (2018), entire 12-page text read | Nonvanishing HC functions, hypercyclic multiplicative groups, and selected composition products | Selected products, powers P(f), differential operators P(D), and pointwise p(z)f(z) have different quantifiers/operations. No all-HC preservation or counterexample implication was located here. |
| Shkarin (2010), arXiv:1209.0984v1 posted 2012, targeted pp.1–4 and concluding material | Hypercyclic algebras and closed HC subspaces | Its p composed with f theorem is not a theorem about p(z)f. Its quoted p(T)x preservation result applies to p(D)f. |
| Bernal–Calderón–Prado, coefficient multipliers, targeted pp.1–6 | Diagonal/Hadamard coefficient multipliers and cyclicity of their sequences | These operators multiply coefficients without shifting them. Differentiation shifts exponential jets; pointwise multiplication convolves them. No exact preservation-set theorem was found in the checked scope. |
| Moothathu (2025), all 8-page text read | Fast approach to an orbital limit forces that limit to be HC, for Banach-space operators | It is neither a classification of pointwise multipliers nor a restriction on Gaussian small balls. |

Two seductive deductions were explicitly rejected. First, the fact that D^n(zf)=zD^n f+nD^(n-1)f does not mean HC(D) equals HC(nD^n); multiplying an orbit by unbounded scalars need not preserve density. Second, a general Gaussian measure with full support and mixing cannot automatically be assumed to have IID jets. Section B identifies a specific K_E and computes its series, so this assumption is verified rather than inferred.

## D. Search coverage and remaining gaps

`QUERY_LOG.md` records the actual queries, including exact-target, HC-preserving maps, weighted shifts, coefficient restrictions, common scaled derivative orbits, multiplier functions, growth, Gaussian series, and recent literature. Search results were used for discovery; mathematical support above comes from retrieved primary sources. Current searches surfaced 2024–2026 growth and differential-sequence work, and the 2025 fast-orbit paper was followed to its full text. Results about conjugate/adjoint multipliers, Fock-space weighted composition, and universal Taylor series were screened as different operator/space questions. No other project AI post was counted as independent earlier evidence.

The search is bounded. It is not a citation-index census, not an earliest-priority determination, and not proof that the exact corollary has never been printed. Earlier Banach-space Gaussian-measure work (Bayart–Grivaux 2006/2007, Rudnicki 1993, Flytzanis 1995) may yield an earlier underpinning; this audit does not promote those references without their needed hypotheses and specialization. The Rosenbloom 1962 trail encountered in random-growth literature was not converted into a claimed hypercyclicity theorem. These gaps do not affect the verified 2011/2012 implication.

## E. Recommendation for the project record

Retain the submitted proof as a valid self-contained argument if independently mathematically accepted, but revise any research-contribution framing to acknowledge the prior random-series implication. A suitable status is: **valid elementary negative answer; older general theorem implies the conclusion; exact explicit corollary priority undetermined; novelty not established.** The simultaneous-polynomial strengthening improves the submitted proof's statement but does not remove the overlap. No paper or publication action should be justified on novelty grounds by this audit.

## Freeze

This report was completed and frozen independently at 2026-10-17T18:28:01.292354+00:00. Its SHA-256 is recorded in `FREEZE.json`. Subsequent cross-family or adversarial comparison, if any, must be recorded separately rather than silently changing this frozen report.
