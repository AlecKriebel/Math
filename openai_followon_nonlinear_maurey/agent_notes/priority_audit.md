# Independent priority and attribution audit

Audit checkpoint: 2026-10-06 22:17 America/Los_Angeles (2026-10-07 05:17 UTC). Agent: independent priority auditor. Audit completion estimate: 95%; the remaining 5% is locating the full Mendel–Naor 2026 preprint, not an inference that it does not exist. Mathematical resolution/package completion percentages belong to the lead research log; this audit is not mathematical certification of the upstream manuscript.

## Verdict requiring a publication gate

**The earlier triage did not catch decisive September 2026 prior art. Novelty of the proposed endpoint theorem is not cleared.** The real-L1 metric-Markov-cotype-two conclusion and the `O(sqrt(q))` Lq-to-L1 consequence were publicly announced before the OpenAI repository existed. The proposed full Markov-type-two-source, arbitrary-real-L1-target statement is a standard consequence of that announced conclusion and established extension/retraction machinery. It is not defensible to advertise either the original Ball endpoint or the `O(sqrt(q))` consequence as a new solution from this project.

The important distinction is between an earlier **public theorem announcement** and an available **full proof**. The former is verified. The latter has not yet been located for Mendel–Naor 2026. Failure to locate it does not restore priority. An independently checkable adaptation of a later proof may still be useful as a verification/scope note, but its genuinely new mathematical statement, if any, must be identified separately. I presently find none in the original core target.

No individuals were contacted. The upstream clone was only read. All network access was public read-only literature/repository access. No git mutation or publication was performed by this agent.

## Exact target compared

The target is existence of one universal C such that, for every metric X with finite M2(X), every countably additive nonnegative measure space (Omega,Sigma,mu), every S subset X and Lipschitz `f:S -> L1(mu;R)`, an extension to X has Lipschitz constant at most `C M2(X) Lip(f)`. No sigma-finiteness or separability is assumed, and the image must be in the original target rather than its bidual. This is stronger in scope than the Hilbert-to-ell1 corollary written in family 332, but the comparison must include known implications rather than only literal statement matching.

## Decisive current primary sources

### Assaf Naor, De-Höldering factorization

Primary records: [arXiv abstract/version history](https://arxiv.org/abs/2609.07564), [v1 full text](https://arxiv.org/html/2609.07564v1), [v2 full text](https://arxiv.org/html/2609.07564v2).

Verified versions are v1, 2026-09-07 14:43:48 UTC, and v2, 2026-09-10 15:15:29 UTC. The author's Lp convention is Lebesgue measure on [0,1]; separability and completeness are used for convenience, with separability said to be droppable. Corollary 7 compares extension moduli into Lp and Lq by a power q/p. Corollary 8 proves an endpoint estimate `e(Lq,L1) <= C sqrt(q log q)` for finite q>=2. Remark 9 discusses L1 metric Markov cotype two as still open in the body. Crucially, **v2's added-in-proof paragraph supersedes that status**: it attributes an affirmative cotype-two answer and `e(Lq,L1) <= C sqrt(q)` to forthcoming work with Manor Mendel. The reference is **M. Mendel and A. Naor, Metric invariants from de-Höldering factorization, 2026, Preprint**. This paragraph is absent in v1. Both versions already establish Hilbert-to-L1 extension.

The full papers were retrieved as PDFs, separately hashed and converted to local text. Saved evidence is in `agent_notes/priority_sources/naor_deholder_v{1,2}.pdf`, `.txt`, and `.receipt.json`; v2 HTML is saved as well. These third-party PDFs are research evidence and should not be bundled into a Zenodo payload without an affirmative redistribution basis.

### Cheng–Wang–Xiang citation is real and materially relevant, but different

[arXiv:2609.08749v2](https://arxiv.org/abs/2609.08749v2), by Qingjin Cheng, Yue Wang and Bo Xiang, is *Sharp Metric Cotype Inequalities for L1 via Nonlinear Cut Smoothing*. v1 was submitted 2026-09-08 13:44:44 UTC; v2, 2026-09-09 14:04:55 UTC. The dates/author names/identifier in family 332's bibliography match the primary record. It proves sharp torus metric-cotype inequalities, not metric Markov cotype. The exact Theorem 1.1 has a term proportional to `m n^{(1/p-1/2)_+}` plus one proportional to `n^{1/p}`. Its finite L1 cut representation and cubic nonlinear smoothing are explicit in Section 2. No Markov-cotype or Lipschitz-extension theorem occurs in the inspected full text. This is not a direct duplicate of the core theorem, but any claim that this project invents finite L1 cuts or the cubic smoothing mechanism would be wrong.

### Established transfer and full extension

[Mendel–Naor 2013 primary manuscript](https://web.math.princeton.edu/~naor/homepage%20files/cat0-extension.pdf), *Spectral calculus and Lipschitz extension for barycentric metric spaces*, Definition 1.1/1.2, Theorem 1.11, and printed pp.8–10 supply the exact transfer. Theorem 1.11 is finite-domain extension with universal-multiple bound `Gamma M_p(X) N_p(Y)`. The discussion following it gives full extension through an ultrapower and a bidual retraction. Corollary 1.13 states the dual-target special case. Theorem 1.14 gives a closed subspace of ell1 failing all finite metric Markov cotypes; Question 1.15 asks about ell1 itself. Thus subspaces cannot be included casually.

[Harmand–Werner–Werner, Chapter IV](https://page.mi.fu-berlin.de/werner99/mbuch/buch4.pdf), Example IV.1.1(a), printed p.158, states L1(mu) spaces are L-summands in their biduals and gives both an AL-space argument and a measure representation argument. This supplies a norm-one projection. It does not say all L1(mu) spaces are dual spaces.

[Naor–Peres–Schramm–Sheffield primary manuscript](https://web.math.princeton.edu/~naor/homepage%20files/Mtype.pdf), Theorem 2.3, states `M2(Lp) <= 4 sqrt(p-1)` for 2<=p<infinity. Theorem 2.4 treats uniformly smooth/convex sources/targets with the older `sqrt((p-1)/(q-1))` estimate. Open-problem item 5 records the previously unknown L1 endpoint. This historical wording must be dated: it is no longer current after Naor September 2026.

## Why the proposed scope does not evade the earlier announcement

The following is this audit's independently checked deduction, rather than a claim that every detail is literally printed in the September announcement.

1. Suppose the announced result supplies `N2(L1[0,1]) <= K`. For every m, normalized indicators of m disjoint equal-length intervals give a linear isometric copy of ell1^m in that L1. Conditional averaging over those intervals gives a norm-one linear projection onto it. Applying the projection to any cotype witnesses fixes the original input tuple and decreases both costs, so `N2(ell1^m) <= K`. Weighted finite ell1 is linearly isometric to ell1^m by coordinate rescaling.
2. A finite tuple in any real L1(mu) has an exact finite cut model in some weighted ell1^m, together with the contractive ambient reconstruction T stipulated in the original request. Applying the finite-dimensional cotype inequality in that cut model and then T proves `N2(L1(mu)) <= K`. This finite-tuple argument needs only finite min/max, integrability, and finite sums, and does not need a product measure or sigma-finiteness. The old finite cut theory plus reconstruction does the transfer; one can also use common simple-function approximation and a bidual projection.
3. Every Banach space has W2 barycenter constant one. Combining the previous line with Mendel–Naor Theorem 1.11 gives finite extensions at `C0 K M2(X)`. Since L1(mu) has a norm-one bidual projection, the established full-extension passage returns the map to the original L1 target without further loss. The conclusion is precisely the core target for arbitrary S and X.

Therefore the full target already follows from a cotype result publicly announced by September 10. Calling the broader quantifiers a new solution would mistake an established reduction for an unresolved problem. The direct min/max ambient construction is a clean explicit adaptation, but its novelty is not established merely because one later manuscript writes only ell1.

The existing Naor v1 proof alone gives finiteness of L1-valued extension for every Markov-type-two X after combining its Corollary 7 with the known Hilbert-target extension estimate. It incurs a power loss (and optimization can reduce it); it does not itself certify a linear M2 bound. The v2 cotype announcement is what closes that quantitative gap by the preceding deduction. The lead must not compare only against v1/Corollary 8 while omitting the added-in-proof disclosure.

## Family 332 and companion audit

The pinned input is commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Both `overview.tex` and `CONTENTS.md` list **one** manuscript for family 332: *Metric Markov Cotype Two of ell1*. No catalogued companion is present. A repository-wide text search for metric Markov cotype and nonlinear Maurey found no other matching central argument; extraneous references to Maurey or extension in other families are not companions.

I read the complete `build/main.tex`, `build/references.bib`, manuscript README, main repository README, the matching catalogue entries, and downloaded current upstream main TeX for byte comparison. The source states `N2(ell1(R)) <= 12 sqrt(21)` (squared constant 3024), a complex ell1 bound with sqrt(2) distortion, and full-subset real-Hilbert-to-ell1 extension. Its proof of the extension corollary already explicitly states general Markov-type-two/dual-Banach-target machinery. It provides finite min/max cuts, the contractive reconstruction, a cubic/quartic-potential martingale argument, stopped geometric walk and Cesaro comparison. It attributes cubic cut smoothing to Cheng–Wang–Xiang, and the transfer to Ball and Mendel–Naor.

The upstream introduction says its Hilbert extension resolves Ball's problem for that target. The September Naor paper means that statement cannot be used as independent current-priority clearance for a follow-on. I found no applicable `lean/docs/332.md`; the filename `Canonical332.lean` is in mutually unbiased mixed semantics and is unrelated. This audit does not claim a Lean verification of family 332 or the follow-on theorem.

Preserve the exact manuscript-specific BibTeX from family 332's README, including OpenAI as supplied author. The follow-on author's metadata must not silently absorb the upstream cotype proof as original work. Also cite the September Naor result/announcement and both older transfer authors. Any useful independently reconstructed proof should expressly describe its dependence on the OpenAI manuscript and the earlier public theorem announcement.

## Public disclosure and later-correction evidence

The October 5 printed manuscript date is **not** public priority evidence. GitHub's public API currently reports that repository `openai/math` was created 2026-10-06 21:47:02 UTC, its sole commit is `adc7f124...` with commit time 2026-10-06 21:58:50 UTC, and its pushed-at timestamp is 2026-10-06 22:01:11 UTC. The official [OpenAI announcement](https://openai.com/index/sharing-ai-progress-in-mathematics/) is dated October 6, 2026. These establish an October 6 public release, not a precise first-public-access instant and not priority before September 10. Commit metadata is not itself a visibility log.

Read-only network checks on 2026-10-06 22:11–22:14 PDT found current main still equal to the pinned commit. File-specific commit history contains only that initial commit. Current family-332 main TeX is byte-identical to pinned input; no later correction was found at that check. Receipts save the relevant URLs, HTTP metadata, retrieval UTC, byte sizes and hashes in `priority_sources`. Later changes must be checked again before publication; this record is time-specific.

## Remaining exact gap and permissible framing

The remaining literature gap is the full public proof/version/location of Mendel–Naor 2026 and whether it contains the exact full quantifiers explicitly. It is **not** a verified gap in the announced quantitative theorem or its known consequence. A locator agent independently searches the primary author/arXiv chains. Do not contact the authors; the project's independent-research policy forbids outreach.

The independent locator has now completed its assigned searches: all 99 exact-Assaf-Naor arXiv entries, all 33 Mendel math entries and 51 broader archive entries, both primary author pages, linked public CVs, and exact/variant title and citation queries. Full MN26 proof remains unlocated. See `agent_notes/mn26_locator.md`; its conclusion independently agrees that the announced cotype statement and standard scope transfer prevent promotion of novelty.

Recommended disposition: keep the mathematical proof and scope verification as research artifacts; withhold any novelty-advertised endpoint-solution deposit until the lead identifies a genuinely new in-scope theorem or clearly distinguishes an independently reconstructed verification/exposition note from a new result. An explicit numerical constant inherited from family 332 and a routine arbitrary-measure adaptation are insufficient on their own to establish the original research contribution requested.

Storage note: when the shared disk ran out of space, I deleted only redundant downloads that this agent had created (Mendel–Naor 2013, HWW IV, NPSS and Cheng PDF/text copies), retaining their URL/status/hash receipts and the critical Naor version files/HTML. Nothing in the upstream clone or another agent's files was removed.

## Remaining upstream-bibliography references

[Naor–Young, Foliated corona decompositions, author-hosted manuscript](https://web.math.princeton.edu/~naor/homepage%20files/foliatedCorona.pdf), introduction surrounding Theorem 1.12 (manuscript pp.10–11), supplies historical discussion of the extension problem and separates it from Lipschitz factorization through Hilbert space. Its negative factorization theorem does not contradict the proposed extension statement. Its problem-status language predates the September 2026 announcement and must not be presented as current novelty evidence.

Ball's original 1992 paper and Deza–Laurent's 1997 book are correctly cited in upstream references; DOI landing-page access in this audit failed. I did not retrieve their original complete texts, and do not claim that I did. The exact current quantitative dependency is instead Mendel–Naor's primary 2013 theorem; the finite cut representation is supplied self-contained in the inspected OpenAI source and earlier Cheng–Wang–Xiang primary manuscript. Thus these two access limits do not reopen the novelty question. Ball remains the original attribution for the Markov extension program, and Deza–Laurent is established prior cut-metric background, not an original contribution of the follow-on.
