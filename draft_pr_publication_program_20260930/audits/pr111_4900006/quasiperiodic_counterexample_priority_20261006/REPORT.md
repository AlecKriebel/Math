# PR111 independent priority audit: quasiperiodic and product constructions

## Judgment

The proposed first resolution of the unrestricted imported question is not cleared for novelty. Its manifold-permitting wording already has a routine classical negative specialization: decay in one real coordinate times an irrational linear flow on a two-torus. This has a compact global attractor and no equilibrium or periodic trajectory at all. The explicit calculation and the ambient/intrinsic convention distinction are recorded in `ZELIK_PRODUCT_SPECIALIZATION.md`.

The bounded search did not locate a prior primary theorem or example matching the stronger complete PR111 result: a real-analytic vector field on all R5, strict volume contraction everywhere, a compact minimal global attractor for the entire phase, actual equilibrium and periodic competitors of strictly lower dimension, and an exact aperiodic maximizing locus under two separately stated asymptotic conventions. This is a search finding, not proof of novelty or an exhaustive claim. None of the sources below supplies that full conjunction by the stated theorem alone.

PR111 therefore contains checkable added mathematical content beyond the elementary manifold product. However, novelty of the formula or exact certificate is weaker than a new decisive resolution of a meaningful open conjecture. The product mechanism is familiar and the literal imported question is too broad to support a first-disproof claim. A narrowly framed explicit Euclidean example could be useful; this family does not decide publication value, PR status, closure, merge, or release.

## Authenticated object and audit boundaries

Reviewed original PR head: `8a7270989d7064a4b97badecaa4b311db5e6d49f`. Imported problem: AMR-048-0006, source 4900006. Read the authenticated source statement and prior report, the actual root mathematical gate, and verified v2 diagnostic `repaired_diagnostics_v2/COUNTEREXAMPLE.md`, SHA256 `0e2e4e1484193c304cb2394142e24460c89a50f6ab3bb58ad838624cabb9035f`. The exact source asks whether the supremum of local Lyapunov dimension on the global attractor of a smooth dissipative system is attained at an equilibrium or an unstable periodic orbit. It states no chaos, genericity, Lorenz, or Euclidean-only hypothesis. Historical interpretations remain separate.

The verified field on C × C × R is

    z1' = [f(|z1|²) + i] z1,
    z2' = [f(|z2|²) + i sqrt(2)] z2,
    w' = -100 w,
    f(s) = -(s-1)(s-4)/(1+s²).

Its global attractor is two radius-2 closed disks times {0}. Only the origin and four periodic circles are equilibria/periodic trajectories. Both the pointwise Kaplan–Yorke maximum and the separately defined fixed-global-j maximum are 203/50, attained precisely on the radius-1 × radius-1 irrational saddle torus. This family inherits the mathematical gate; it does not issue a new independent full proof audit. It does not promote a finite-time equality, chaos, transitivity, genericity, or a refutation of a narrower historical conjecture.

The priority search started independently from the other new priority families. Initial mechanism leads were obtained before comparison. Later, the root requested an exact Zelik specialization and an adversarial check of Turaev–Zelik; the historical family independently confirmed the manifold/ambient distinction. No other family's report was used as evidence of a prior theorem. Only the actual primary bodies listed in `SOURCE_TABLE.json` support the source conclusions. No outside individual was contacted. No Git, PR, service, or publication mutation was made by this family.

## Most serious priority concern: classical torus products

Zelik's author-hosted preprint treats decoupled cascade products, torus translations with zero external exponents, and global attractors relative to a chosen product phase. Relevant author-version locations are Examples 3.1–3.3, printed pp. 10–12. The related published paper has a different title and numbering; its 2008 publisher metadata is confirmed, while its publisher PDF was not retrieved. The author body is undated. These version/access distinctions are retained rather than silently treating author p. 10 as published p. 980. [Author body](https://sergey-zelik.co.uk/publications/dlyap.pdf), [publisher record](https://doi.org/10.3934/cpaa.2008.7.971).

The reviewer specialization x'=-x, theta'=(1,sqrt(2)) on R × T2 is completely explicit. It attracts every bounded subset to {0} × T2; the global attractor is minimal; intrinsic divergence is -1; ordered intrinsic spectrum is (0,0,-1); all local dimensions equal 2; no equilibrium or periodic orbit exists. This is a direct elementary specialization of a classical framework, not an assertion that the author published this exact Eden-refutation example. Gelfert's 2003 primary paper independently authenticates the intrinsic Riemannian manifold tangent convention, pp. 553–555. [Gelfert primary body](https://ems.press/content/serial-article-files/35401).

Parker–Goluskin v2 explicitly allows embedded manifold phases on p. 2 and uses ambient Rn derivatives on pp. 5–7. The embedded product B=R × S1 × S1 in R5, with explicit extension F=(-x,2 pi i z1,2 pi i sqrt(2)z2), has a global attractor relative to B and ambient spectrum (0,0,0,0,-1), giving dimension 4, not intrinsic dimension 2. It supplies the same absence-of-competitors objection within that explicitly permitted phase setting. The extension has no compact global attractor on all R5, since arbitrary radii are preserved. Thus the weaker phase-relative example must not be identified with PR111's stronger entire-space result. [Exact Parker–Goluskin version](https://arxiv.org/pdf/2510.14870v2).

## Turaev–Zelik 2002 does not yet yield the full strict comparison

The WIAS 777 primary preprint is dated 2002 and was read at the introduction, the relevant bifurcation theorem/corollaries, Theorem 4.1, Remark 4.3 (printed p. 34), and Appendix B (pp. 38–40). It constructs high-dimensional quasiperiodic minimal tori in damped hyperbolic equations, with dimension of the same asymptotic order as the global Lyapunov dimension. Corollary 3.1 also constructs periodic orbits with many unstable directions. [Actual primary body](https://www.wias-berlin.de/preprint/777/wias_preprints_777.pdf).

Adversarially, neither order-of-growth bounds nor a high-dimensional minimal torus imply that every equilibrium and periodic orbit has lower local Lyapunov dimension. The source's bounds on equilibrium instability indices count positive eigenvalues; they are not bounds on equilibrium Kaplan–Yorke dimension. Its introduction explicitly relates the local Lyapunov dimension of the relevant equilibrium to the large bifurcating dimensions. Remark 3.2 compares a periodic unstable manifold dimension to an integer part of Lyapunov dimension; it does not exclude that periodic orbit as a maximizer. Remark 4.3 supplies a torus of comparable order, not an exact torus maximum or a strict comparison against all competitors. These are the exact missing implications. Deriving them would require new spectrum/global optimization arguments absent from the source; this audit does not assume those arguments or initiate a new proof search.

The paper is substantive prior work on quasiperiodic minimal sets and attractor dimension. It should be credited if PR111 is retained. It cannot be labeled an authenticated previous full negative resolution of this exact maximizer question merely because it contains large irrational tori.

## Aperiodic maximizing cocycles are relevant but have a different target

Bousch–Mairesse's May 2001 author preprint, Section 4, gives an explicit matrix-family counterexample to a finite-word spectral maximizer assertion. Its irrational Sturmian maximizer is aperiodic. The corresponding journal paper is JAMS 15 (2002), 77–111, DOI 10.1090/S0894-0347-01-00378-2. This is a multiplicative matrix cocycle over symbolic sequences; it is not by itself the derivative cocycle of an autonomous dissipative flow or a global-attractor Lyapunov-dimension maximization example. Turning it into the latter requires additional realization and attractor/spectrum control that the source does not supply. [Author primary body](https://www.imo.universite-paris-saclay.fr/~thierry.bousch/preprints/artetris.pdf).

Bochi's arXiv v3 (23 April 2018), Section 3, reviews these nonperiodic cocycle maximizers and contrasts them with periodic-optimization results requiring specific regularity/base dynamics or genericity. Those generic statements do not apply automatically to an irrational torus flow. Nor do they support unrestricted equilibrium/periodic maximization for every dissipative autonomous flow. [Exact primary exposition](https://arxiv.org/pdf/1712.01612v3).

The familiar existence of aperiodic Lyapunov maximizers makes a broad first-ever maximizer-disproof narrative particularly unsafe. It does not authenticate a prior proof of PR111's full Euclidean theorem.

## Modern dimension theory does not remove these gaps

Anikushin's arXiv v10 (14 October 2025), Section 3, Remark 3.9, and Appendix A were read at the relevant definitions and complete ergodic variational argument. Maximization over ergodic measures permits aperiodic measures; it does not force a periodic or equilibrium support. The text places periodic optimization in a generic context and describes the Eden conjecture for particular systems. Its finite-equilibrium example illustrates a distinction among uniform/local dimension constructions, not a torus counterexample. [Exact v10 primary body](https://arxiv.org/pdf/2304.05713v10).

General variational principles and dimension bounds do not imply that the old conjecture is universally true, universally open, or already refuted in the exact entire-R5 sense. The root's separate source audit, including the historical thesis access gap, remains necessary. This family has not read Eden's original thesis or the full Kaplan–Mallet-Paret–Yorke 1984 torus paper and makes no theorem-content claim about either.

## Claim-by-claim priority comparison

| Content | Prior evidence in this family | Exact boundary |
|---|---|---|
| Irrational product torus with no periodic trajectories | Classical torus/cascade framework, explicit reviewer specialization | Already elementary on manifold phase; does not establish a new open-problem resolution |
| Local/uniform dimension from a merged product spectrum | Zelik direct-product calculation; explicit constant derivative here | Standard mechanism, not a new general theorem |
| Smooth manifold global attractor with aperiodic-only maximizers | Exact elementary specialization above | Negative answer to literal imported wording; exact example is our deduction, not an authenticated author-labeled Eden refutation |
| Embedded-manifold version with ambient tangent exponents | Explicit smooth extension and Parker–Goluskin's permitted phase scope | Global only relative to the chosen embedded phase; ambient normal spectrum is fixed explicitly |
| High-dimensional quasiperiodic minimal sets in genuine dissipative PDE global attractors | Turaev–Zelik 2002 | Comparable dimension order does not prove exact global maximization or strict superiority to every equilibrium/periodic orbit |
| Nonperiodic largest Lyapunov exponent for a matrix cocycle | Bousch–Mairesse 2001/2002 | Not automatically autonomous-flow derivative or Lyapunov-dimension/global-attractor target |
| Entire-R5 analytic strict-volume-contracting field with all stated comparisons | PR111 mathematical gate | No exact matching previous full theorem located in bounded search; no absolute novelty clearance |

## Remaining concerns and contribution assessment

1. **Framing is a substantive concern.** A title/abstract claiming the first negative resolution of the unrestricted question, or the historical Eden conjecture without its original hypotheses, would overstate what this audit supports. The manifold product gives a direct scope objection. The historical thesis remains unread in this family.
2. **The Euclidean enhancement is real, but discovery value is unproved.** It adds a complete explicit system, genuine entire-space attraction, existing lower competitors, exact rational values, two carefully separated conventions, and a reusable verification certificate. Its independent originality as a research contribution has not been established merely by failing to locate the same formula. The underlying product/radial/irrational mechanism is routine.
3. **Access/version gaps remain visible.** The undated Zelik author version is read; its publisher body is unavailable. Hunt's author abstract was only a lead, not a full-text exclusion. The historical torus-paper lead and Eden thesis were not read. No negative claim about those unseen bodies is made.
4. **Search assurance is bounded.** The phrase/mechanism searches included English variants and selected French/Russian terms; indexed secondary pages were used only to find originals. They returned much unrelated Murray Eden growth literature, which was excluded. Search terms, source locations, body hashes, and access gaps are retained in the machine artifacts. The audit cannot certify that no prior construction exists.

Recommendation to the root: treat this as a priority/framing finding against a novel decisive resolution of the broad imported question. Preserve the stronger verified theorem and its exact certificate while deciding whether it merits a modest explicit-construction contribution. Do not close a PR as beyond repair or publish/merge solely from this family's bounded finding. The root must combine independent families and apply the user's stated solved/already-solved/unsolved process.
