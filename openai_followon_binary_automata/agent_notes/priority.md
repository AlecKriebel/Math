# Priority and attribution audit: fixed binary automata

Audit checkpoint 2026-10-06, 21:16 America/Los_Angeles. This is a literature and scope audit, not certification of either upstream exponential theorem. Research-resolution estimate for this delegated audit: 85%; publication-readiness estimate: 0%. Root researchers are auditing the upstream mathematics separately. No external individual was contacted. The upstream checkout was read only, and no Git operations changed it.

## Findings that materially affect the manuscript

1. Adjacency-matrix alphabet reduction for one-way liveness is explicitly discussed by Kapoutsis in ICALP 2011 and the expanded Information and Computation 2013 paper. It is established machinery, and cannot be called our invention.
2. The inspected older exponential lower bound restricts deterministic machines to few reversals. It is not an unrestricted 2DFA lower bound. Before the OpenAI release, the latest inspected unrestricted lower-bound theorem was quadratic, including the exact liveness bound h(h+1)/4 from Adeogun–Kapoutsis v2.
3. The only public exact-target result found in the OpenAI corpus concerns growing alphabets. The two family-129 papers expressly disclaim a fixed-alphabet theorem. Thus a valid binary transfer of their exponential theorems would be a consequence of their breakthrough, using established reduction machinery. It must not be presented as an independent proof of the base conjecture.
4. A public machine-mathematics record, TheoremDB R816, describes stronger coding machinery than the initial triage: a delimiter source with at most 9h binary states and a macro pullback with at most 2s+2 states. That record imports only the quadratic liveness theorem and expressly leaves the core question open. It is a relevant antecedent, but is self-reported and currently lacks identifiable author provenance; its arXiv link is not evidence that the new encoding occurs in that arXiv paper.
5. Rejecting *every* nonmultiple block length is a material convention. The root compiler agent's h³ fooling-set argument is independently checked below. Therefore the informal older O(h²) source remark cannot be silently imported for the strict language E_h(OWL_h). The remark does not specify malformed-word behavior or supply a compiler, so alleging an error in the older work would overstate this audit.

## Inspected primary sources and precise scope

### Sakoda and Sipser, 1978

[STOC paper DOI](https://doi.org/10.1145/800133.804357); [Berkeley technical-report record](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1978/28933.html); [scanned report](https://digicoll.lib.berkeley.edu/record/133106/files/ERL-m-78-34.pdf).

The report is May 1978, UCB/ERL M78/34; the publisher gives 1 May 1978 for the proceedings paper. Sections 2.1–2.3 define relational graph alphabets and the complete language families C_n and B_n. Theorem 2.2 characterizes polynomial 2NFA-to-2DFA conversion through C_n. Theorem 2.3 makes B_n complete for 1NFA-to-2DFA conversion. Section 1 explicitly conjectures that B_n needs more than polynomially many deterministic two-way states. Their automata start on the first input symbol with a set of initial states and accept upon reaching the right endmarker in a final state; moves are left/right and partial transitions are permitted. Hence their state counts are not automatically identical to the new note's endmarked start convention. The checked text does not supply the proposed fixed-block binary compiler. Attribution belongs to Sakoda and Sipser for the original liveness family and succinctness question, even though the exponential input is attributed to OpenAI.

### Kapoutsis, ICALP 2011 and Information and Computation 2013

[2011 author-hosted PDF](https://www.andrew.cmu.edu/user/cak/reads/2011-ICALP/main.pdf); [2011 publisher DOI](https://doi.org/10.1007/978-3-642-22012-8_15); [2013 author-hosted PDF](https://www.andrew.cmu.edu/user/cak/reads/2013-IAC/main.pdf); [2013 publisher DOI](https://doi.org/10.1016/j.ic.2012.11.001).

The ICALP paper's Section 5 already describes encoding relation symbols by h²-bit words. Its source-size statement concerns 2NFAs. The expanded journal paper's Section 8, printed p. 29 of the author manuscript, says the binary witness needs O(h²) states on a zero-reversal 2NFA and retains its exponential few-reversal 2DFA lower bound. Its formal Theorem 1 restricts the target to o(input length) reversals, and Theorem 3 demonstrates exponential savings when that restriction is removed. Section 2.2 defines OWL_h over relation words, and its promise-problem framework explicitly allows unspecified behavior outside a promise. The binary paragraph contains no transition rules or malformed-word language definition. Thus the old paragraph certifies the *idea* and restricted-target application, but not the exact strict binary-language source bound needed here. The 2011 proceedings publication establishes a verifiable earlier disclosure of adjacency-bit reduction; this audit does not claim it is the earliest possible use in all literature.

### Adeogun and Kapoutsis, arXiv:2602.24279v2

[versioned primary text](https://arxiv.org/html/2602.24279v2); [submission-history page](https://arxiv.org/abs/2602.24279).

Version 1 was submitted 2026-02-27 18:50:33 UTC; v2 was revised 2026-07-06 09:45:39 UTC. Theorem 1, Section 4.4, states that every unrestricted 2DFA solving OWL_h has at least h(h+1)/4 states for h≥1. The paper's introduction separates this from exponential results for restricted target models. Its 2DFA convention uses left/right moves, total transitions, start at the left endmarker, and acceptance after exiting the right endmarker in an accepting state; nonaccepting loops are permitted. The result is an external comparator, not the pivotal exponential dependency. Its source liveness family is again over a relation alphabet. The exact source statement and published dates can be cited, but the theorem should not be described as providing an exponential lower bound or a newly resolved fixed-alphabet question.

### Adeogun and Kapoutsis, arXiv:2609.13793v2

[versioned primary text](https://arxiv.org/html/2609.13793v2); [submission-history page](https://arxiv.org/abs/2609.13793v2).

Version 1 was submitted 2026-09-12 08:12:11 UTC; v2 was revised 2026-09-15 13:44:55 UTC. Theorem 2.1 caps the number of transitions in a sequence of separated, smooth properties connected by their suffix-of-choice condition at binomial(h+1,2). Theorem 5.1 proves the connectivity-property special case. These are limitations of their property-chain mechanism. They neither provide a polynomial unrestricted simulator nor forbid a different exponential lower-bound mechanism. The upstream manuscript cites this work; a follow-on must not treat it as a refutation of every prospective exponential liveness theorem merely from the word “limitation.”

### Guillon, Prigioniero and Taheri, STACS 2026

[published primary PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol364-stacs2026/LIPIcs.STACS.2026.48/LIPIcs.STACS.2026.48.pdf); [publisher record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2026.48); [earlier arXiv disclosure](https://arxiv.org/abs/2507.11209).

The arXiv version was submitted 2025-07-15; the publisher records 2026-02-25. Table 1, pp. 48:2–48:3, identifies same-model 2NFA complementation as open, with an exponential upper bound from eliminating two-wayness. Theorem 4.1 gives a polynomial conversion of arbitrary 2NFAs into self-verifying 2NFAs with common guess, equivalently a restricted 1-limited automaton; this is a stronger target model with an annotation/rewrite phase. It does not imply polynomial 2NFA-to-2NFA complementation. Their size model counts description symbols and generally holds the input alphabet constant. This is the newest checked published comparator for the complementation question. Do not misrepresent the polynomial title as resolving the same-model target.

### Pighizzini, 2012 survey

[versioned primary PDF](https://arxiv.org/pdf/1208.2755v1); [publication record](https://arxiv.org/abs/1208.2755).

Submitted 2012-08-14, EPTCS 90, pp. 3–20, DOI 10.4204/EPTCS.90.1. Section 6 carefully distinguishes short-input automaton simulation, unary simulation, L versus NL, and NL versus L/poly. Theorem 6.1 gives an equivalence between polynomial unary 2NFA determinization and NL⊆L/poly. The discussion makes clear why a general family of hard regular languages does not by itself furnish a uniform L≠NL proof. The follow-on should state only its automaton state bounds; no complexity-class separation is obtained from the fixed-binary reduction alone.

## Other public evidence: coding antecedent with incomplete provenance

[TheoremDB R816](https://www.theoremdb.org/records/R816/) was accessible during this audit. Its own locator says a reduction was written/audited 2026-07-28, which is a self-reported work date, not independently established publication priority. The record describes row separators and a matrix terminator over four symbols, a 3h-state NFA with its own behavior on noncanonical words, and a uniform two-bit decoder with ≤9h states. A deterministic macro simulator hardwires each coded block's internal behavior, retaining only target state and entry side, for ≤2s+2 states. The claimed consequence is quadratic, imported from Adeogun–Kapoutsis. Its metadata identifies no author, and its verification link points to the base theorem rather than an independently published encoding proof. This page is a public antecedent worth recording, but not a mathematical dependency. If any route adopts its exact mechanism, state that this machinery was already publicly described and independently prove the needed version. No evidence of an exponential fixed-binary conclusion appears in this record.

## OpenAI family 129: corpus duplication and public-disclosure evidence

Pinned input: adc7f1241b42e322a6451854ab7e4b4c146bf78a. Both supplied manuscript READMEs identify OpenAI as author and supply manuscript-specific BibTeX, which should be preserved in the preprint. The manuscripts are internally dated 2026-09-25. Those dates are not public-disclosure evidence.

Read-only local search across preprint TeX/Markdown/BibTeX for Sakoda–Sipser, one-way liveness, and nondeterministic complementation found only these two family-129 manuscripts. Their introduction/separation sections expressly limit the results to growing alphabets. `lean/docs/129.md` does so as well. No complete fixed-binary theorem, compiler, or strict block-language result was located in the corpus. This is a search finding, not proof of absence or novelty.

On 2026-10-06 21:13 PDT the GitHub repository API reported:

```json
{
  "repository": "https://github.com/openai/math",
  "created_at": "2026-10-06T21:47:02Z",
  "pushed_at": "2026-10-06T22:01:11Z",
  "current_commit": "adc7f1241b42e322a6451854ab7e4b4c146bf78a",
  "commit_author_date": "2026-10-06T21:58:50Z",
  "commit_message": "Initial commit"
}
```

Endpoints: [repository metadata](https://api.github.com/repos/openai/math), [commit list](https://api.github.com/repos/openai/math/commits?per_page=5), [pinned commit](https://github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a). The API returned one commit. Therefore the earliest *verified public availability evidence located by this audit* is the 2026-10-06 repository release. Repository creation is not proof that files were already public then; push time is metadata, not a claim of globally earliest disclosure. No later correction was present in the checked current branch at this checkpoint. Recheck before publication.

## Independent check of strict-block cubic source-state obstruction

This deduction is ours for this project and uses no exponential theorem. Let L=h² and E be the length-L adjacency encoding. Define B_h=E(OWL_h), with every binary word whose length is not divisible by L rejected. Let I be the identity relation and e_pp the singleton diagonal relation, for 1≤p≤h. For each p and 0≤t<L set

    x_(p,t)=E(e_pp) prefix_t(E(I)),
    y_(p,t)=suffix_(L−t)(E(I)) E(e_pp).

The diagonal concatenation encodes e_pp I e_pp=e_pp and is accepted. A cross with different cut positions t≠u has length 3L+t−u, which is not divisible by L because 0<|t−u|<L; it is rejected by the strict convention. A cross with equal positions and distinct vertices p≠q encodes e_pp I e_qq=0 and is rejected. Thus these hL=h³ pairs form a fooling set with *all* off-diagonal crosses rejected. In any accepting NFA run for a diagonal concatenation, record the state at the prefix/suffix split. Equal states for two different pairs would splice the prefix of one run with the suffix of another and accept a rejected cross. Consequently every ordinary 1NFA for this strict binary language needs ≥h³ states. The proof permits multiple initial states and epsilon transitions. For endmarked no-left machines that may make stay moves, contract the finite stay closure at each boundary into an ordinary NFA, without adding states, before applying the splice argument.

The proposed O(h³) compiler would therefore be order-optimal for this exact language. The argument also works for any common-length injective coding of the relation alphabet; its role is to quantify the cost of strict alignment, not to give a new unrestricted two-way lower bound. Searches for “one-way liveness” together with “h^3” or “cubic” located no primary account of this particular obstruction. That limited negative search does not establish priority. A manuscript may present the proof as an auxiliary observation without a “first” claim. The older O(h²) remark and delimiter encoding cannot be substituted into strict-block source counts because their off-promise behavior is unspecified/different.

## Recommended claim and attribution boundary

If the upstream dependencies pass mathematical audit, title and abstract should describe a fixed-binary *consequence* of the newly released relation-alphabet lower bounds, with explicitly quantified polynomial loss and a total-language convention. Explain that the lower-bound engine is inherited from OpenAI, the liveness family from Sakoda–Sipser, and alphabet reduction is established machinery. The self-contained contribution can be the explicit checked compiler/pullback, complete boundary semantics, and strict-block order-optimal source expansion. Do not state priority beyond what the inspected evidence warrants. If an upstream gap is found, the same reduction yields only a conditional implication; priority auditing cannot repair that gap.

Do not claim 2^Ω(n) without a separately verified linear-state total-language construction and pullback. Do not infer L≠NL. Do not conflate target-state conventions or the complementation universe: pulling back the binary complement uses only canonical encodings, but the binary complement is taken in all of {0,1}*.

## Search record and reproducible fingerprints

Searches were performed on 2026-10-06 PDT through web search, arXiv versioned full texts, publisher/author pages, and the read-only local corpus. Query groups included Sakoda–Sipser binary alphabet encoding; fixed-alphabet two-way automata reductions; complementing 2NFAs over binary alphabets; one-way liveness exponential 2026; exact titles of both OpenAI manuscripts; and cubic/h³ one-way liveness. Nonprimary search results were used as leads only, except the explicitly identified public R816 antecedent, which was evaluated as its own self-reported original record. A failed search is not proof of novelty.

PDF bytes fetched transiently for SHA-256; third-party PDFs were not added to the publication package:

| Source | PDF bytes | SHA-256 |
| --- | ---: | --- |
| Kapoutsis 2013 author manuscript | 531539 | `2e5af94acb6c0a610c2c62277cb9b835ae17e594ba1feff9e17e1d7b1dc4e889` |
| Adeogun–Kapoutsis 2602.24279v2 | 865128 | `d107f0c5dd108fb8a44353e1b113e99ca76d985e6cf8eca2ae6deab445ae8ab4` |
| Adeogun–Kapoutsis 2609.13793v2 | 417533 | `ca1614b5899b7fc4fd981d9bc8fa762548aa195120a1023d6515741a62a64885` |
| Guillon–Prigioniero–Taheri STACS 2026 | 1200764 | `840deb7c0d0ce965b4ff1fc8a6b80fdd5d8d81c040e5a10488e1d44686be73e8` |
| Pighizzini 1208.2755v1 | 239164 | `020286a6d99b9f842a7725e46f155ebffd871843b7ad4446943fd3b0b6e6c9c6` |

The Berkeley mirror returned an empty body during direct hash fetching; that is *not* a validated PDF/hash and is deliberately excluded. Its text was inspected through the web reader. A later direct-fetch attempt encountered a transient disk-capacity failure before any file was written; no unrelated files were deleted. The 2011 conference PDF was inspected through the web reader, but has no direct-byte hash at this checkpoint.
