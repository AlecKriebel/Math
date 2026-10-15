# Independent primary-source and target-scope audit

Date: 2026-10-01 UTC (2026-09-30 America/Los_Angeles). Candidate: immutable PR12 head `19dfaccb52a7640eec79af28a778b4f22f93479a`; `PROOF.md` SHA-256 `f38ae2dd97bb2aeb8f1e97da0f4133b84b6d43d803e2b38df2c91acc56817a8e`.

**Verdict: the exact curated target and the candidate's cited primary-source roles match. No material scope narrowing or unsupported cited theorem was found. Reference 6 has verified primary bibliographic metadata but an uninspected full text. Full priority certification is deferred and is not implied by this verdict.** The candidate's self-contained mathematical proof is being tested by separate independent families; this report does not substitute for those proof audits.

## 1. Method and evidence boundary

This audit started from the immutable candidate, the pinned source record, and six downloaded primary PDFs. The preserved `SOURCE_AUDIT.md` and historical mathematical review were not used as evidence. Relevant definitions, theorem statements, and full proofs were independently read in the primary texts. All four official OWR target pages and eight key cited-statement pages were rendered and visually inspected. The original publisher EMS PDF was independently downloaded; its bytes exactly equal the cached OWR PDF. All six inspected PDF hashes equal both the current retrieval manifest and historical `source_provenance.json`. See `audit_manifest.json` for hashes and inspection locations.

Official arXiv abstract pages were checked for current versions, and publisher/Crossref metadata was checked for DOI identities. Raw documents, metadata responses, and page renderings remain under ignored `tmp/root_primary/` or `tmp/primary_scope/`; this report does not redistribute the full texts. No external individual was contacted.

## 2. Exact target and standing hypotheses

The official report is *Mini-Workshop: New Horizons in Linear Dynamics, Universality, and the Invariant Subspace Problem*, Oberwolfach Reports **21** (2024), no. 2, pp. 1069-1096, report no. 19/2024, DOI [10.4171/OWR/2024/19](https://doi.org/10.4171/OWR/2024/19). [EMS's official record](https://ems.press/journals/owr/articles/14298367) identifies publication on 25 November 2024. The inspected contribution is Martina Maiuriello, *Preserved dynamics: visualizing the connection between composition operators and weighted shifts*, joint work with Emma D'Aniello and Udayan B. Darji, printed pp. 1078-1081 (PDF pages 10-13).

Open Problem (1) is entirely on printed p. 1080 and asks two distinct questions: whether the earlier shadowing characterization survives removal of bounded distortion, and whether generalized hyperbolicity remains equivalent to shadowing. Printed p. 1081 begins Open Problem (2), on structural stability under bounded distortion, followed by the contribution's references. The candidate makes no claim to solve that structural-stability problem.

The curated `statement` and `clean_statement` for 30005897 select only the generalized-hyperbolicity/shadowing equivalence. Its longer `original_statement` preserves both sentences of Open Problem (1), plus an extraction artifact from the p. 1081 header. The candidate addresses the selected equivalence with its theorem, discusses the other sentence separately, and expressly credits its negative answer as prior art. It therefore does not replace a bundled target with an easier special case. For maximum clarity the opening target line could name the selected second sentence and call the first sentence an accompanying already-resolved question; this is an editorial improvement, not a mathematical gap.

The source's standing assumptions, on pp. 1079-1080, are:

- A sigma-finite measure space and a bijective bimeasurable transformation `f`.
- `mu(f^-1 A) <= c mu(A)` for all measurable `A`, and the same condition for `f^-1`. These are exactly the candidate's two inequalities (1.1), with independently allowed constants.
- Composition on `L^p`, `1 <= p < infinity`, giving a bounded invertible operator.
- Dissipativity **in the source's finite-wandering-set sense**: the disjoint union of all `f^n W` is `X`, with `0 < mu(W) < infinity`.
- Two-sided shadowing, indexed over all integers.
- Generalized hyperbolicity by closed complementary subspaces, forward invariance of `M`, backward invariance of `N`, and spectra of the two restricted operators inside the open unit disk.

The candidate reproduces each of these assumptions. Its interpretation of the orbit partition modulo null sets is harmless: both measure-change inequalities preserve null sets in both directions; restricting to the invariant full-measure union yields the same `L^p` operator. The introductory general-operator notation on p. 1078 assumes a separable Banach space; the candidate's absence of a separability restriction enlarges its theorem and cannot narrow the source target. Its real-space extension similarly enlarges the complex-spectrum presentation. The finite positive measure assumption on `W` is explicit in the source, although a general Hopf dissipative part need not admit a finite wandering set. The candidate appropriately says “in the source's sense” and should retain this qualification in any broader summary.

The report uses the spectral formulation of generalized hyperbolicity, exactly as candidate (1.3). This is an important convention: one-step proper contraction in the original norm is stronger than spectral radius below one. The 2020 preprint underlying reference 1 initially words the definition using proper contractions but its main proof obtains exponential/spectral decay. The candidate states its 2024 convention explicitly. Strict contractions on the two bands can also be obtained in an equivalent norm: choose `alpha` strictly between their spectral radii and one, define the stable norm as `sup_k alpha^-k ||T^k m||`, the unstable norm analogously with `T^-k`, and combine them using the direct-sum projections. Thus no hidden original-norm hypothesis is being introduced.

## 3. Independent verification of all seven reference roles

### [1] D'Aniello-Darji-Maiuriello, 2021

Inspected the open preprint [arXiv:2009.11526v1](https://arxiv.org/abs/2009.11526v1), including composition/dissipativity definitions (pp. 9-10), Corollaries SC/GH (pp. 13-14), the supporting SS/SN main-theorem proofs (pp. 22-29), and Problem 5.0.1 (pp. 29-30). Corollary GH states exactly the shadowing/generalized-hyperbolicity equivalence for dissipative systems **with bounded distortion**. Corollary SC characterizes shadowing using the aggregate sequence `mu(f^k W)` through HC/HD/GH. Problem 5.0.1 explicitly separates removal of bounded distortion for equivalence from removal for that characterization.

The candidate's attribution is accurate. Publisher metadata independently confirms the published title, authors, Journal of Differential Equations **298** (2021), 68-94, and [DOI 10.1016/j.jde.2021.06.038](https://doi.org/10.1016/j.jde.2021.06.038). Current arXiv history lists only v1, submitted 24 September 2020; “2021” is correctly the publication year, not a claim about the arXiv submission date.

### [2] Official OWR contribution, 2024

The contribution, printed page range, report DOI, source assumptions, definition conventions, and both sentences of Open Problem (1) all match. The author entry “M. Maiuriello” is correct for the contribution; recording its joint-work attribution would be optional bibliographic enrichment. The report DOI identifies the complete report, whose listed organizers/authors are Grivaux, Grosse-Erdmann, Matheron, and Peris, not a separately DOI-registered contribution.

### [7] Carvalho-Darji-Varandas, 2024

Inspected the author-institution PDF [CDV-arxiv-2024.pdf](https://www.cmup.pt/sites/default/files/2024-09/CDV-arxiv-2024.pdf), whose title page identifies [arXiv:2407.20890v1](https://arxiv.org/abs/2407.20890v1). Theorem 2.4 (p. 4), under Definition 2.3's dissipative composition hypotheses, gives a conjugacy to the identity shift on the sequence space with norm

`||psi||^p = sum_n integral_W |psi_n|^p d(mu f^n)/dmu dmu`.

Its full proof on pp. 18-19 constructs `Gamma(phi)_n = phi o f^n` on `W`, proves the norm identity and onto property, and verifies the shift intertwining. The candidate's normalized realization is obtained by multiplying each coordinate by the p-th root of this density; attribution of the unnormalized realization to prior work is accurate and essential.

Corollary 2.16 (p. 8) requires **finite-dimensional** Banach fiber `X` and a basis with **S-bounded projections** (Definition 2.9, p. 6). Theorem 2.10 (p. 7) reduces such shifts to a finite product of scalar shifts, which explains the shadowing/generalized-hyperbolicity equivalence. This is not an unrestricted infinite-dimensional measurable-fiber theorem. In fact p. 8 gives an infinite-dimensional example illustrating failure of the naive componentwise-shadowing implication, and Question 5.1 (p. 27) leaves general shift equivalence open. The candidate correctly distinguishes uniform operator estimates from separate fiberwise assertions.

The current official arXiv history lists only v1, submitted 30 July 2024. The institutional title-page manuscript date is 31 July 2024; this one-day internal dating difference does not contradict the correctly cited arXiv submission date.

### [3] Bernardes-D'Aniello-Maiuriello, July 2026

Inspected [arXiv:2607.15831v1](https://arxiv.org/abs/2607.15831v1), Section 5's standing assumptions and Theorem 6.1/Example 6.2, including the complete obstruction proof on pp. 17-18. Example 6.2 is exactly a two-orbit dissipative system with `W={a_0,b_0}` and masses `mu(f^n W)=2^n`. Its b-orbit mass is one for every positive index. Hence HC holds with limiting rate `1/2`, yet the accumulated pseudotrajectory error at `b_j` equals `j delta`, making a shadowing orbit impossible.

The example lies within the candidate's bounded-invertible setting: consecutive point masses obey `mu(f A) <= 3 mu(A)` and `mu(f^-1 A) <= mu(A)` for all measurable `A` (all point masses are positive). Its wandering set has mass one. Bounded distortion fails, since the b-orbit fraction of level mass tends to zero. On the b-fiber, the candidate's normalized density equals two at every positive coordinate; for any fixed `d`, taking `n>d` makes both neighboring densities equal `rho_n`, so (1.5) fails for every `eta<1`. The candidate's negative-answer credit and description of this obstruction are correct.

Theorem 6.1 is a restatement of the earlier aggregate HC/HD/GH criterion under bounded distortion; the candidate does not mistake it for a new unrestricted positive equivalence theorem. Official arXiv history lists only v1, submitted 17 July 2026.

### [4] Pituk, August 2026

Inspected [arXiv:2608.19499v1](https://arxiv.org/abs/2608.19499v1), Theorems A-C and their scope on pp. 2-4, Theorem A's full construction on pp. 11-14, and Theorem B's full proof on pp. 14-15. Theorem B covers **all bounded invertible operators on separable complex Hilbert spaces**. The paper expressly leaves removal of separability open. The proof uses local constancy of kernel Hilbert dimension and a right-resolvent existence result whose stated hypothesis is separability. Therefore the candidate correctly credits its separable complex `p=2` equivalence case as prior art, while its specific support-band construction and density criterion are not thereby attributed to Pituk.

Theorem A's counterexample is constructed on `X=Y direct_sum_1 Y`, where `Y=(ell^infinity/c_0) direct_sum_1 ell^1(N,ell^infinity)`, using the nonexistence of a bounded right inverse of the quotient map. Its operator has coupled block form `T(x,y)=(y,x-3Sy)`. It is not presented as a dissipative composition operator. The candidate does not assert any stronger exclusion than that the construction has not been identified as belonging to the target class. Official arXiv history lists only v1, submitted 19 August 2026.

### [5] Messaoudi-Tofanin Neto-Saavedra-Tsokanos, August 2026

Inspected [arXiv:2608.17021v1](https://arxiv.org/abs/2608.17021v1), definitions distinguishing pseudo-hyperbolicity from generalized hyperbolicity (pp. 3-4), Theorem 3.5 (p. 6), Theorem 3.9 (p. 7), and the full counterexample proof (pp. 14-15). Theorem 3.9 gives, for every `1<p<infinity`, `p != 2`, an invertible operator on `ell^p(N)` with shadowing that is not pseudo-hyperbolic and consequently not generalized hyperbolic. It uses a non-complemented closed subspace, a quotient map, and a coupled operator `(u,v) -> (v,u+alpha A v)`, transferred by an arbitrary Banach-space isomorphism. No dissipative composition representation is claimed.

Theorem 3.5 gives shadowing equivalence with **pseudo-hyperbolicity** under complemented unimodular eigenspaces, including Hilbert spaces. It does not settle generalized hyperbolicity there; Pituk explicitly discusses this distinction in his Theorem B footnote. The candidate correctly treats this work as a general Banach-space counterexample and does not conflate its weaker positive Hilbert theorem with Theorem B. Official arXiv history lists only v1, submitted 17 August 2026.

### [6] Dragičević-Pituk, 2026

The primary [AMS earlyview metadata](https://pubs.ams.org/journals/tran/earlyview) and the publisher-deposited [Crossref DOI record](https://api.crossref.org/works/10.1090/tran/9879) independently confirm title, authors, Transactions of the American Mathematical Society, and [DOI 10.1090/tran/9879](https://doi.org/10.1090/tran/9879). Crossref gives publication date 8 July 2026. Current AMS metadata lists it as earlyview/preprint without volume, issue, or pages, and records receipt on 18 November 2025 and revision on 26 April 2026. The candidate's deliberately incomplete volume/page bibliography is therefore appropriate.

The actual PDF URL identified in publisher metadata is `https://www.ams.org/journals/tran/earlyview/tran9879/tran9879.pdf`; this audit's request redirects to AMS login. Other current publisher routes return HTML rather than PDF. Consequently its full text and proofs remain uninspected. Pituk [4, p. 2, Theorem 1] independently quotes [6, Theorem 2.2]'s characterization of shadowing by avoidance of the unit circle by the surjective spectrum; Messaoudi et al. [5, Theorem 2.3] also quote it. Those are inspected primary authors' attributions, not inspection of [6] itself.

The candidate labels [6] as a consistency/literature comparison and explicitly says none of its uninspected proof is used as a premise. Its actual necessary dual estimate is proved directly in Lemma 2.1. There is therefore no missing mathematical premise from this inaccessible citation. There remains a full-text gap for exact comparative priority of that estimate; it must not be presented as independently new, and the candidate does not do so. The reference's historical access note may be retained, or updated to say publisher metadata has now been independently checked while full text remains unavailable.

## 4. Pinned-record provenance and duplicates

`pinned_cache_checks.json` independently records:

- `problems.json` has 15,458 records and SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`, equal to the pinned dataset manifest at revision `37e53eabe540fb458758e198be61634bd02ee008`.
- Exactly one record has numeric ID 30005897 and exactly one record has code `OWR-14298367-003`; the full parsed record equals the preserved `source_record.json`.
- Its canonical UTF-8 sorted-key JSON SHA-256 is `4c38f4ab152d7996b1e7d0c3f8a00c0fa6013120846d97c2f1f29f57c29fcefb`, matching `source_provenance.json`.
- `research_results.json` has SHA-256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`, also matching its pinned manifest; it contains no report under this code, confirming `report_present:false`.
- There is no match for 30005897 in `review_v2/related_target_groups.json`. The only other records from the same report are 30005898 (weighted-shift supercyclicity converse) and 30005899 (Gamma-supercyclicity); neither duplicates this equivalence target.
- All six inspected PDFs match the source provenance hashes. The two historical CDV filenames are correctly aliases of the identical institutional PDF, not two independent pieces of evidence.

The record's August 2026 “open” assessment is historical triage, not a current mathematical certificate. The candidate correctly retains an unconfirmed-priority warning, credits the current special cases and negative aggregate answer, and does not rely on that stale status to establish novelty.

## 5. Repairs, remaining gap, and promotion boundary

No mandatory source-scope repair emerged. Recommended small presentation improvements are to identify the curated second sentence in the opening target line, retain the finite-wandering-set qualification wherever “dissipative” is summarized, and optionally update reference 6's bibliographic verification note with the current AMS/Crossref check.

The strongest verified source conclusion is that the candidate addresses the original selected question with the source's exact analytic assumptions and convention, and accurately distinguishes all inspected cited prior results. Its full `1<=p<infinity` theorem is not already supplied by any of the inspected cited theorems. This does **not** establish global priority: the full [6] text is inaccessible, and a systematic broader primary-literature search is still required after the proof audit passes. The support-band/density criterion's comparative originality also remains to be investigated. No novelty conclusion is promoted here.
