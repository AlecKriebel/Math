# Independent priority and duplication audit: cost versus first L²-Betti number

Checkpoint: 2026-10-06, 9:29 p.m. America/Los_Angeles (2026-10-07 04:29 UTC). Audit completion estimate: 95% for a bounded primary-source audit; a worldwide priority exclusion cannot be certified by searching. This audit makes no claim that family 259 is sound.

## Decision

The proposed conditional conclusion is an immediate consequence already effectively disclosed by OpenAI's family 259 manuscript, combined with Gaboriau's established 2002 results. I found no explicit Betti-number statement in family 259 itself. That omission does **not** establish novelty. The logical connection from failure of fixed price to failure of action-specific/relation cost–Betti equality was explicitly in the literature by 2018, before the present source.

A responsible follow-on must present the conclusion as a **conditional corollary/observation of OpenAI's claimed construction**, identify the unverified source input, and credit Gaboriau for the comparison and action invariance. It must not claim an independent new construction or resolution of the cost–Betti problem. This conclusion is an inference from the verified statements and publication records below.

## Exact mathematical scope and conditional deduction

Let Γ, its essentially free Bernoulli action on X, and its free height-extension actions on Y_M be precisely those in [OpenAI, Theorem 1.1](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-group-without-fixed-price-October-5-2026/build/introduction.tex). The source asserts, for η>0 and every integer M>100,

\[
C(R_{\Gamma\curvearrowright X})\ge1+\eta,
\qquad C(R_{\Gamma\curvearrowright Y_M})\le1+99/M.
\]

Gaboriau's Corollary 3.16 identifies β_n(R) with β_n(Γ) for a free probability-measure-preserving group action, without requiring ergodicity. Corollary 3.23 gives

\[
C(R)-1\ge\beta_1^{(2)}(R)-\beta_0^{(2)}(R).
\]

These are in [*Invariants ℓ² de relations d'équivalence et de groupes* (2002)](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/Cohom-L2-rel/Cohom-L2.pdf), Corollaries 3.16 and 3.23. The inspected April 2002 author PDF has them on printed pp. 25 and 26 (PDF pages 25 and 26). The journal reference is *Publ. Math. IHÉS* **95**, 93–150, [DOI 10.1007/s102400200002](https://doi.org/10.1007/s102400200002). Gaboriau's [FAQ](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/FAQ.pdf), p. 1, locates the comparison at journal p. 128 and the question at p. 129. The differing page numbers are different layouts, not different numbered results.

Γ is infinite, so β₀(Γ)=0. Thus the height-action upper bounds alone yield

\[
0\le\beta_1^{(2)}(\Gamma)
=\beta_1^{(2)}(R_{Y_M})
\le C(R_{Y_M})-1\le99/M.
\]

Taking M→∞ gives β₁(Γ)=0; hence β₁(R_X)=0. **Only if the source's positive Bernoulli cost lower bound is valid**, R_X has β₁(R_X)=0 and C(R_X)>1. No new comparison theorem is needed for this deduction. A standalone proof of the upper bound can establish the vanishing even if the source lower bound fails; it cannot establish a counterexample.

Define the group infimum cost explicitly by C_*(Γ)=inf{C(R_α): α free p.m.p.}. The same bounds give C_*(Γ)=1. Therefore this example, if valid, satisfies C_*(Γ)=1+β₁(Γ); it contradicts **action-specific/relation** equality only. It does not contradict equality for the infimum cost of a group. An unqualified phrase “cost of Γ” would be misleading here.

## Prior formulations and explicit implication

1. **Gaboriau 2002.** Immediately after Corollary 3.23 the author PDF asks whether C(R)−1=β₁(R)−β₀(R) always holds and records the absence of known strict examples. Short exact excerpt: “On ne connaît aucun exemple d’inégalité stricte.” The full formula and numbered theorem, rather than an extended quotation, identify the claim. The [Numdam journal record](https://www.numdam.org/item/PMIHES_2002__95__93_0/) reports Online First July 1, 2002, and online publication July 28, 2002. The author version is described by its [landing page](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/Cohom-L2-rel/Cohom-L2.html) as April 2002. These records establish priority by 2002; they do not prove the earliest date on which the question was orally posed.

2. **Gaboriau survey, 2002.** [*On Orbit Equivalence of Measure Preserving Actions*](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/Renc-Betti-L2/prepub-293.pdf), Theorem 7.1 and Question 6 on printed p. 17, state group-action invariance and the same equality question. The [author's publication page](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/Cambridge/Cambridge.html) identifies publication in *Rigidity in dynamics and geometry (Cambridge, 2000)*, pp. 167–186, Springer, 2002. “Cambridge, 2000” is the meeting context, not an established public posting date for the inspected PDF.

3. **Popa–Shlyakhtenko–Vaes 2018/2019.** [*Classification of regular subalgebras of the hyperfinite II₁ factor*](https://arxiv.org/abs/1811.06929), Remark 6.6, explicitly formulates fixed price for equivalence relations, proves its connection with the group question, and explains that a fixed-price counterexample supplies a cost–Betti counterexample because Betti numbers agree across the relevant extensions. Exact short clause: “would also provide a counterexample”. The arXiv v1 was submitted November 16, 2018, 17:24:26 UTC; v2 September 8, 2019, 12:34 UTC. I checked that the implication is present in both v1 (pp. 24–25) and v2 (p. 25). The source cites Gaboriau Corollary 3.16 and Sauer Theorem 5.5. The journal publication is [DOI 10.1016/j.matpur.2020.02.009](https://doi.org/10.1016/j.matpur.2020.02.009). Thus the present logical bridge is not novel.

4. **Gaboriau notes dated October 3, 2025.** [*Around the orbit equivalence theory, measure equivalence, cost and ℓ² Betti numbers*](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/ME-Cost-L2-Lectures/ME-Cost-L2-lectures.pdf), Theorem 2.64 and Question 2.65, pp. 22–23, explicitly distinguish group infimum-cost equality, individual free-action strictness, and relation equality. This distinction is essential for the proposed claim. The PDF date is a version date, not a independently timestamped upload date.

## Family 259 source, catalogue, and current-version evidence

The read-only clone is `/Users/alec/Desktop/math`, at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Family 259 has one manuscript in both `CONTENTS.md` (lines 6401–6410) and `overview.tex` (line 605). Both summarize two free actions with distinct costs and the height costs tending to one. No cost–Betti corollary is listed. Searches through all manuscript `.tex`, `.bib`, and `.md` files found no other explicit source for this exact conclusion. Adjacent cost/Betti citations in the nonuniqueness-percolation, unitarizability, and free-uniform-spanning-forest manuscripts do not state it; the latter's Lyons 2013 reference is background, not this counterexample.

The source bibliography cites Levitt 1995, Gaboriau 2000, Arzhantseva–Ol'shanskii 1996, Kapovich–Schupp 2002 v1, Khezeli 2026 v4, Slutsky 2026 v1, Bevilacqua–Bowen 2025 v1, and Greendlinger 1960. It does not cite Gaboriau's Betti paper or Popa–Shlyakhtenko–Vaes. This is a bibliographic omission, not evidence of an independent consequence.

Current primary public checks at the checkpoint:

- `git ls-remote` reports HEAD and main at the same pinned commit.
- [GitHub repository API](https://api.github.com/repos/openai/math) reports `created_at=2026-10-06T21:47:02Z`, `pushed_at=2026-10-06T22:01:11Z`. These correspond to October 6, 2:47:02 p.m. and 3:01:11 p.m. PDT.
- [Commit history API](https://api.github.com/repos/openai/math/commits?per_page=100) and the manuscript path history each return one commit, “Initial commit”, timestamp October 6, 21:58:50 UTC (2:58:50 p.m. PDT).
- Tags, releases, and repository issues each return an empty list at inspection.
- Downloaded main `introduction.tex`, `INPUTS.md`, manuscript PDF, and `CONTENTS.md` are byte-identical to the pinned clone.

Therefore the audit found no later revision, correction, withdrawal, or separate public corollary in these checked channels. This does not certify that no informal criticism or correction exists elsewhere. The source title-page date **October 5, 2026 is not proof of public disclosure on October 5**. The evidence supports a public repository release on October 6, with the current publicly accessible source observed by this audit. Git commit timestamps alone do not establish the exact initial time when the repository became public.

The [source INPUTS.md](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-group-without-fixed-price-October-5-2026/INPUTS.md) says: “The available source record does not establish that it was the final revision of that argument.” It calls the source intermediate and distinguishes the general fixed-price problem from the property-(T) fixed-price-one question. The repository README says unformalized claims may have issues and promises versioned corrections. These statements reinforce the need for independent validation, not acceptance of its claims.

## Current cited-work check and search limits

The current [Khezeli arXiv page](https://arxiv.org/abs/2509.08325) still gives v4, January 4, 2026, following first submission September 10, 2025. Its theorem is a positive fixed-price-one result for products of two infinite countable groups, not a strict cost–Betti example. [Bevilacqua–Bowen](https://arxiv.org/abs/2510.05459) still gives v1, submitted October 6, 2025, 23:45:20 UTC; it gives positive criteria. [Slutsky](https://arxiv.org/abs/2607.20273) still gives v1, July 22, 2026, 15:24:53 UTC; Introduction paragraph 3 calls general fixed price open, and Corollary 1.8 deduces vanishing β₁ from fixed price one. No newer arXiv versions were listed. None explicitly supplies the desired strict example.

Searches included the exact manuscript title with OpenAI/correction/Betti variants, cost–Betti strictness/counterexample formulations, and current 2025–2026 variants, followed by primary-paper checks. Secondary indexes were used only for discovery, not as authority. A later indexed secondary catalogue repeats family 259 but provides no independent result or earlier disclosure evidence. Search-engine absence is weak evidence and cannot exclude unindexed preprints, unpublished observations, or same-day parallel corollaries. No individual was contacted, and no comments, issues, messages, or other outreach were prepared or sent.

## Recommended attribution text

“Assuming the two cost bounds in OpenAI's *A group without fixed price* (manuscript dated October 5, 2026; public repository version `adc7f124...`, October 6, 2026), Gaboriau's Corollaries 3.16 and 3.23 imply that its Bernoulli orbit relation has vanishing first L²-Betti number and cost strictly greater than one. We record this conditional consequence and its precise scope. The underlying construction and cost estimates are due to OpenAI; the cost–Betti comparison and group-action invariance are due to Gaboriau. The general implication from failure of fixed price to a cost–Betti counterexample was already explicit in Popa–Shlyakhtenko–Vaes, Remark 6.6.”

Until the positive lower bound is independently validated, replace assertions of an actual counterexample with the conditional formulation above. If the source audit identifies a flaw, the useful deliverable is that verified flaw plus any retained independent theorem, not a conditional headline implying established resolution.

## Provenance artifacts

`local_source_manifest.json` records SHA-256 hashes for the 17 inspected local family/catalogue files. `web_source_manifest.json` records URLs, UTC retrieval times, byte lengths, SHA-256 hashes, and public response headers for fetched primary documents. `repository.json`, `commits.json`, `source_history.json`, `tags.json`, `releases.json`, and `github_issues.json` are read-only API snapshots. Cached PDF/full-text inspection copies are ignored by the adjacent `.gitignore`; they are not intended for republication.

Key source hashes:

| Source | SHA-256 |
|---|---|
| OpenAI family 259 PDF | `aa2ee4de0db26fc8aa62f95ec695e2ef11db6c9b326d2d354465aa50bee4c078` |
| OpenAI introduction.tex | `6cbfa027e1ddc3efc5dd435347c76c0003f67551749931cf21763e3282cfa1bc` |
| OpenAI INPUTS.md | `924b8b3fa74298a7f8943bbabfe15f99fe47d28c9853479f8e17661fefc453aa` |
| Gaboriau April 2002 author PDF | `6b00c6967d1fb1e5ff7080b76717cbdb6ed00c914bc951ffda823986d7be3a1a` |
| Gaboriau October 3, 2025 notes | `54a39877ba212a3d3bf35d10d38587bfe60d5a248970d37ed025ad866d8cdbbe` |
| Popa–Shlyakhtenko–Vaes arXiv v1 | `ee3ce3ec22323c8a8cdbd3cb2b79737528b841f7d6c11b14b6787de916929490` |
| Popa–Shlyakhtenko–Vaes arXiv v2 | `d734253d056bfbe95d4a5f11688264cceec8aa618136c785c84b570fded38550` |
