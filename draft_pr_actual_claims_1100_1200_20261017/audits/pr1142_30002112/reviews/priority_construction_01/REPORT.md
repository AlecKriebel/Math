# Construction-family priority audit: PR1142 / 30002112

Final checkpoint: 2026-10-17 23:26:20 UTC. Completion estimate: 100% of this assigned priority audit; receipt and containment verification completed. This percentage measures the audit, not the probability of mathematical novelty.

## Independent decision

**Earlier complete target resolution found. Recommend SKIP under the user's stated rule.** This decision was reached from primary bodies before reading any older audit, root report, or concurrent review; those reports remain unread. It does not rest on the age of generic ingredients.

Luc Pétiard's 2017 preprint explicitly disproves the additive isoperimetric/Weyl bound for every hypersurface dimension at least three. His 2019 doctoral thesis explicitly extends the result to dimension two. Both concern the intrinsic Laplace spectrum of smooth Euclidean hypersurfaces. The connected-hypersurface result is stronger in boundary connectivity than the candidate's two-component cavity example. A different elementary proof can remain useful exposition, but the full original question was already recorded as answered negatively.

This is a bounded positive identification of an earlier full result. It is not a global firstness certificate, a claim about influence or copying, or a conclusion about who first knew the result privately. The supplied PR date is 10 October 2026; all decisive sources precede it by years.

## Claim audited

The target is Colbois's question on printed page 2036 of Oberwolfach Report 33/2012, following Theorem 3 on page 2035. For each fixed m >= 2 it asks for dimension-only constants A_m,B_m in

    lambda_k(partial Omega) |partial Omega|^(2/m)
       <= A_m I(Omega)^(1+2/m) + B_m k^(2/m),
    I(Omega)=|partial Omega|/|Omega|^(m/(m+1)).

The domains are bounded smooth connected Euclidean domains; their boundaries need not be connected. All zero eigenvalues and multiplicities are retained, with the candidate's numbering starting at one. The read-only candidate is `../../inputs/PROOF.md`, 10,412 bytes, SHA-256 `c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658`.

## Decisive primary evidence

1. **Luc Pétiard, Counter-example to a Kröger type spectral inequality, arXiv:1706.09189v1.** The primary submission history lists only v1, submitted 28 June 2017 at 09:53:24 UTC. All six pages were read. Theorem 2 on page 2 explicitly negates a bound with *any continuous function* of the isoperimetric ratio plus a dimension-only coefficient times k^(2/n), for n >= 3, using connected smooth hypersurfaces in R^(n+1). A prescribed hypersurface diffeomorphism type is permitted. Section 2 proves the disconnected version (Theorem 3): fix the area of a component whose first positive eigenvalue exceeds a chosen sphere eigenvalue, take its disjoint union with the unit sphere, retain the two zero modes, and bound the ratio uniformly in k. Section 3 joins the components through a thin tube and controls the spectrum and enclosed volume. This is an explicitly recorded full negative consequence, not merely an ingredient. [Primary version and history](https://arxiv.org/abs/1706.09189v1).

2. **Luc Pétiard, Isoperimetric inequalities for Laplace and Steklov problems on Riemannian manifolds, doctoral thesis, Université de Neuchâtel, 2019.** Relevant introduction and the complete printed pages 23–29 were read. Theorem 2.1.2 explicitly covers every n >= 2: for each C>0 there are J,j0 such that every j>=j0 admits a connected hypersurface with I<=J and normalized j-th eigenvalue greater than 2C j^(2/n). Section 2.2 includes the two-dimensional variable-topology input; Section 2.3 connects the sphere and high-gap component. Equation (2.1.3) expressly formulates the broader continuous-function additive bound being disproved. The title page records defense on 5 February 2019; the imprimatur is dated 5 March 2019. The institutional item lists issue year 2019, DOI `10.35662/unine-thesis-2749`, and present-system accession/availability on 12 September 2025. Thus I do not claim that the present repository URL was online in 2019. [Institutional item](https://libra.unine.ch/handle/20.500.14713/31635), [primary PDF](https://libra.unine.ch/server/api/core/bitstreams/cb35ac23-61a8-402a-9fdb-a1eb4d47c041/content).

## Exact implication for this target

Here is an independently written check of the index and quantifier bridge. Let p=2/m. Use the thesis's quantitative theorem and fix putative target constants A,B. Choose C such that 2C>2^p B. It supplies a finite J and examples at all sufficiently large source indices j satisfying

    I <= J,    lambda_j |Sigma|^p > 2C j^p.

The source indexes from zero, whereas the candidate indexes from one. Therefore the target index is k=j+1 and its eigenvalue is exactly the source eigenvalue lambda_j. For j>=1, (j+1)^p<=2^p j^p. Choose j further so that

    A J^(1+p) < (2C-2^p B) j^p.

Then

    lambda_k |Sigma|^p > A I^(1+p) + B k^p.

A smooth compact connected embedded Euclidean hypersurface bounds a bounded connected smooth complementary component; hence these are valid domains in the target class. No change of ambient metric, no different spectral operator, and no disconnected-domain loophole is used.

The stronger unbounded-quotient formulation in the candidate is also not a surviving target distinction. For each integer N choose C large compared with N, use the associated finite J, then choose j large enough that J^(1+p)<=j^p. The displayed theorem and k=j+1 make the quotient by I^(1+p)+k^p arbitrarily large. Taking one example for each N gives divergence by a diagonal choice. This is a direct logical consequence of the already recorded quantitative statement.

## Ingredient and construction separation

| Source/family | Mechanism actually checked | Classification relative to full target |
|---|---|---|
| Colbois–Dryden–El Soufi, arXiv:0909.5346v1, Theorem 1.4 and entire Section 5 | Large normalized first positive eigenvalue; Kuiper embedding followed by smooth approximation and spectral comparison; variable surface topology in dimension two, fixed smooth type in higher dimensions | Earlier established ingredient. The theorem and proof do not explicitly prescribe an arbitrary containing ball and exact area together, and do not record this additive-boundary counterexample. |
| De Lellis–Székelyhidi, author's PDF, Theorem 1.2 and adjacent discussion | Arbitrarily close C^0 approximation of a short embedding by a C^1 isometric embedding, preserving embedding; discusses crumpling into a small region | Precise localization ingredient. Combining it with the previous row and smoothing gives the candidate lemma, but this audit does not label that combined lemma historically new. |
| Colbois–El Soufi–Girouard, arXiv:1007.0826v2, introduction and Examples 3.1–3.2 in full | Multiplicative Euclidean estimate. Example 3.1 uses products with hyperbolic manifolds and two boundary components; Example 3.2 removes a small ball in a compact ambient manifold | Related explicit counterexamples with different ambient hypotheses. Neither example is a Euclidean negative answer to the target. |
| Pétiard 2017 paper | High-gap component with fixed area plus round sphere, exact multiset spectrum/zero shift, uniformly controlled isoperimetric ratio; thin-tube connection | Earlier complete Euclidean negative result for m>=3. |
| Pétiard 2019 thesis | Same construction with two-dimensional high-gap input explicitly included | Earlier complete Euclidean negative result for every m>=2. |
| Colbois–Girouard, arXiv:2108.03101v2, selected introductory results and remarks | Steklov bounds using packing/growth/distortion and intrinsic injectivity data; Laplace consequences through cylinders | Related spectral geometry, not used as the decisive target hit. |

The candidate's exact prescribed-area, prescribed-gap, prescribed-small-ball lemma was not located as a standalone statement in the checked CDE, CEG, Pétiard, or Nash–Kuiper passages. The candidate's cavity placement also differs from Pétiard's external union followed by tube attachment. Those are distinctions of presentation/construction, not a missing earlier full consequence. The prior paper already records the high-gap-plus-sphere spectral mechanism and the full negative additive conclusion. No unsupported equivalence claim is substituted for the target.

For CDE, the verified arXiv history has only v1, dated 29 September 2009 at 13:56:51 UTC. The freshly downloaded version is byte-identical to the supplied private PDF. The official journal landing page reports first publication on 22 December 2009, with the 2010 issue citation. For CEG, the verified history is v1 on 6 July 2010 at 07:56:53 UTC and v2 on 2 October 2011 at 16:46:02 UTC. The exact-v2 download is byte-identical to the supplied private PDF. Its first-page typeset date says May 25, 2022, while its arXiv version stamp/history says 2011; the historical version assertion uses arXiv history, not that typeset date. I do not infer a 2022 revision from the latter.

## Adversarial checks and limits

The strongest possible scope mismatch was checked: the 2017 theorem really says m>=3, so it alone does not settle m=2. The thesis body supplies that missing dimension explicitly. The source's zero-based index was shifted explicitly above. Its connected hypersurface statement is within, rather than outside, the permitted boundary class. The normalized quantity is intrinsic induced Laplace–Beltrami spectrum. No Steklov, interior Neumann/Dirichlet, or arbitrary compact-ambient result was counted as a full Euclidean hit.

Pétiard's tube step cites Anné. This audit read the full paper's tube argument and the thesis's expanded statement, but did not independently reconstruct Anné's proof. Small typographical problems in the paper's prose do not erase the explicitly recorded full theorem. The absolute-value bars in the thesis's Proposition 2.3.1 are present in the PDF but omitted by the pdftotext extraction; this is an extraction limitation, not missing notation in the thesis. This precise correction follows narrow parent feedback after the independent core audit was sealed; I did not independently inspect the reported page image. The primary article's Proposition 7 states absolute differences; its proof discusses area as well as enclosed-volume convergence, which are the quantities required by the normalized conclusion. A fresh mathematical audit of every tubing estimate is separate from this positive priority identification.

CDE's journal full-body URL was unavailable through the web tool; its official abstract/date record and full arXiv proof were available. CEG's current journal HTML returned HTTP 405; full arXiv v2 was available. Hassannezhad's 2011 journal body returned HTTP 403; only official abstract/bibliographic material and its role as cited in the read sources were checked. Therefore I do not independently classify every theorem in that journal body. Colbois–Girouard 2023 v2 was selectively read, not read in its entirety. Other search hits were leads only unless explicitly marked as body reads in the receipt. No negative conclusion about the whole literature is made.

No older audit, tracker, root/concurrent report, or other shard was read. After the core audit was sealed, narrow parent feedback about the PDF-versus-text extraction discrepancy was received and incorporated as described above; it did not supply the initial prior-full classification. No external individual was contacted. No subagent was spawned. No paper, PR, tracker, release, or Zenodo record was altered. No commit or push was performed. Only this assigned review folder was written; `git check-ignore` was used solely to verify required containment.

## Public-artifact policy

Third-party PDFs, extracted text, HTML, repository JSON, and retained raw web-tool returns are confined to ignored `sources/private/`. Public artifacts contain authored analysis and factual bibliography/query/version/digest metadata. The source manifest records byte identities and reading limits; it does not reproduce source excerpts or source headings. The manifest excludes itself to avoid circular self-pinning; its own external SHA-256 will be supplied to the coordinating parent after finalization.

Post-core accuracy repair: 2026-10-17 23:27:11 UTC. Completion estimate remains 100%; the priority verdict is unchanged. The former report and receipt remain byte-preserved in an ignored private historical directory.
