# PR1142 priority and duplicate adversary report

Checkpoint: 2026-10-21 UTC. Scoped audit complete: **100%**. Recommendation: **skip as an already fully answered target; do not prepare or create a new publication record for this claimed full resolution.** This is a positive prior-result finding, independent of the unsuccessful duplicate searches.

## Claim and provenance

The reviewed candidate is the 10,412-byte `PROOF.md` at immutable PR head `c29139d2c2a98f1a0284d0dc794c88f51c680a0c`, SHA256 `c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658`. Its claim is that for each fixed integer m>=2, connected bounded smooth Euclidean domains with exactly two boundary components make

    lambda_k(boundary Omega) * area(boundary Omega)^(2/m)
    ---------------------------------------------------
             I(Omega)^(1+2/m) + k^(2/m)

unbounded, counting all zeros and multiplicities from index 1. This disproves the dimension-only additive bound in Colbois's 2012 question.

The fresh OWR source was read through the whole Colbois contribution, printed 2034-2036, and the relevant problem-session item at 2064. The former asks about I^(1+2/m); the latter prints I. Both concern the intrinsic boundary Laplacian. The problem-session heading says Dirichlet, but the equation and cited hypersurface theorem specify the boundary spectrum. Neither formulation requires the boundary to be connected. The earlier result below defeats both powers.

The audit located and read the existing October 17 PR1142 priority decision before freshly reading the decisive literature. This audit therefore does **not** claim a blind discovery of the literature lead. It independently retrieved primary files and checked their statements, proofs, and the target implication. Earlier audit pass labels and scripts were not treated as mathematical premises and were not executed.

## Positive earlier full resolution

Luc Petiard's institutional thesis, *Isoperimetric inequalities for Laplace and Steklov problems on Riemannian manifolds*, DOI [10.35662/unine-thesis-2749](https://doi.org/10.35662/unine-thesis-2749), supplies the decisive result. Theorem 2.1.2, printed 24 / PDF 36, applies in every dimension m>=2 to connected smooth compact hypersurfaces embedded in R^(m+1). The complete relevant Chapter 2 was freshly read, including the dimension-two branch, disconnected model, and tubular attachment. [Institutional record](https://libra.unine.ch/handle/20.500.14713/31635).

The institutional issue year is 2019. The PDF records defense on February 5, 2019, and approval on March 5, 2019. Current repository accession/availability is September 12, 2025; it is not confused with publication in 2019. All these dates precede the PR's recorded creation on October 10, 2026. The 2017 arXiv article [1706.09189v1](https://arxiv.org/abs/1706.09189v1), Theorem 2, already states a stronger continuous-function nonseparation result for m>=3. That article alone does not cover m=2.

The following are this audit's deductions from the thesis theorem. Write p=2/m and a=1+p, and call the source's zero-based eigenvalues mu_j. The theorem says that, for every C>0, there are a finite J and a threshold j0 such that every sufficiently large j admits a connected hypersurface Sigma with

    I(Sigma)<=J,              mu_j(Sigma)*|Sigma|^p > 2C*j^p.

The exact order of quantifiers matters: J may depend on C, and j is chosen after J. A connected compact embedded Euclidean hypersurface bounds a bounded connected smooth domain D. Thus it already belongs to the original target class, with connected boundary. Its one-based eigenvalue lambda_(j+1) equals mu_j. Because p<=1 and j>=1,

    (j+1)^p <= 2*j^p.

Given finite positive proposed constants A,B, choose C=B+1 and then j beyond the source threshold and with A*J^a < 2*j^p. The source lower bound exceeds A*I(D)^a+B*(j+1)^p. Hence the exact original additive claim was fully resolved earlier. Replacing a by 1 gives the problem-session variant too. No unproved uniform ceiling in C is needed.

## Even the exactly-two-boundary restriction is a prior corollary

The following elementary bridge removes a possible scope escape. Fix a source domain D as above. Take an interior point x and remove a closed ball of radius r, small enough that its closure lies in D. The new domain D_r is bounded, smooth, and connected, and its boundary is the disjoint union of Sigma and a round m-sphere S_r. Connectivity follows by detouring through a spherical annulus contained in D whenever a path passes through the removed ball; m+1>=3 suffices. There are exactly two boundary components.

Choose r with m/r^2>mu_j(Sigma). The small sphere contributes exactly one eigenvalue below that finite spectral window, its zero. Thus, including the original zero,

    lambda_(j+2)(boundary D_r) = mu_j(Sigma).

Its area is |Sigma|+rho_m*r^m and its volume is |D|-omega_(m+1)*r^(m+1), so I(D_r)->I(D). Choose r still smaller to make I(D_r)<=K:=J+1. The normalized numerator increases because the area increases. Set C=2t in the source theorem and select j large enough that j^p>=K^a. Then

    I(D_r)^a+(j+2)^p <= K^a+3*j^p <=4*j^p,

where (j+2)<=3j and 3^p<=3. The resulting quotient is >C/2=t. Choosing t->infinity establishes the candidate's full quotient-divergence conclusion within exactly two boundary components as a consequence of the earlier theorem. This bridge does not claim that Petiard printed this puncture formulation.

## Mechanism and adversarial checks

Petiard's prior construction already uses the high first-positive normalized spectrum from Colbois-Dryden-El Soufi, a sphere, disjoint-union spectral bookkeeping, and a thin connection with control of spectrum and enclosed volume. The candidate localizes the high-gap component inside a fixed outer sphere by Nash-Kuiper and smoothing, and replaces sphere Weyl asymptotics with exact mode counts. These are differences of presentation and geometric specialization; they do not make the full negative target unresolved.

The fresh CDE source [0909.5346v1](https://arxiv.org/abs/0909.5346v1), Theorem 1.4 and complete Section 5, explicitly treats embedded hypersurfaces, dimension two with varying genus, higher dimensions with fixed smooth structure, and C1-to-smooth approximation. The precise Nash-Kuiper statement in De Lellis-Szekelyhidi, Theorem 1.2, explicitly preserves embeddings when the starting short map is an embedding. These classical methods need full credit.

CEG [1007.0826v2](https://arxiv.org/abs/1007.0826v2), Theorem 1.1, is the multiplicative bound, not the desired additive theorem. Example 3.1 uses a different ambient manifold; its two zero modes do confirm that disconnected boundary is included in that convention. Example 3.2 uses compact ambient manifolds and does not independently settle the bounded Euclidean target. Neither example was misclassified as the decisive prior answer.

The thesis's gluing argument explicitly includes the extra Dirichlet spectrum of the limiting interval. The interval is chosen short enough that its first eigenvalue lies above the finite spectral window before its thickness tends to zero. This avoids silently discarding tube modes. Its final equality on printed 28 incorrectly identifies x^(m/2)+1 with (x+1)^(m/2) in general. The immediately preceding bound already proves a finite ceiling independent of j; alternatively, for m>=2 the equality can be replaced by an inequality in the required direction. This does not invalidate the theorem. The absolute-value bars in Proposition 2.3.1 are present in the PDF despite their omission by text extraction. The relevant theorem and proof pages were inspected visually.

Two independent primary acknowledgments reinforce the scope. Colbois's 2017 survey, Remark 49, writes the same I^(1+2/m) additive question and attributes its negative answer to Petiard. Colbois-Provenzano's 2021 journal article, [DOI 10.1112/jlms.12493](https://doi.org/10.1112/jlms.12493), Appendix A, Remark 4 (printed 2145), records nonseparation for p=2 and cites the 2019 thesis as reference 37. This is not reliance on a bare thesis abstract or on an absence of matching titles.

## Existing work and external duplicate checks

The actual existing folder is `draft_pr_actual_claims_1100_1200_20261017/audits/pr1142_30002112`. Its `ROOT_PRIORITY_DECISION.md` and `SKIP_PR_UNCHANGED.json` record the same earlier full resolution and explicitly record no paper, deposit, tracker row, or PR mutation. No publication/preprint-named file was present in this target folder during this audit. It is prior audit work to resume; it is not a newly found unpublished package that should be deposited. The current candidate is the same immutable head listed in that skip receipt.

The parent supplied a fresh October 21 23:47:06 UTC ledger search over 181 rows with no exact or semantic target match. That result is pinned privately here, but this agent did not independently authenticate to the ledger or recertify private provider drafts. A fresh public check found the EulerSolve alias URL returned actual HTTP 404, while the full public papers index returned HTTP 200. All 374 heading titles were scanned, as were title/abstract contexts for spectral and hypersurface leads. The nearby Laplace, Robin, and Dirichlet entries are about different questions. No exact ID, alias, or semantic target record was identified. Initial web-tool alias failures were not called 404; the direct HTTP retrieval supplies the actual status.

Fresh public Zenodo metadata searches for the exact problem ID, alias, the additive-boundary phrase, and isoperimetric+Kriebel returned zero results. A small-cavity query returned two unrelated records. Initial size-100 requests failed because unauthenticated requests permit at most 25 results; the corrected size-25 requests succeeded. These bounded public searches are not evidence that no private draft or differently worded record exists. They provide no reason to create a new record because the positive literature result already controls the decision.

## Limits and deliverables

This is a scoped priority classification, not an exhaustive earliest-world-priority certificate, a claim of copying, or a fresh proof of all external geometric analysis inputs. The original Anné, Colbois-Dodziuk, Nash, Kuiper, and Hirsch works were not all independently reproved or read in full here. No material target gap remains between the decisive prior theorem and the proposed conclusion. The specialized fixed-outer-sphere presentation may be of expository interest, but a claim of new full resolution is unsupported.

All captures, third-party text/renders, and recovered source bodies are under ignored `private/`. Public files contain authored analysis, query/read-scope/version metadata, hashes, and an offline verifier. The verifier checks custody and the finite exact algebraic/index checks described in its output; it does not certify external theorem truth. It was run normally, with Python optimization, and in isolated mode from a fresh copied folder. No original/captured script was executed. No external person was contacted and no provider, Zenodo, PR, GWS, Git, index, or refs state was mutated.
