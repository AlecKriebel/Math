# Meager-ideal equalities at regular uncountable cardinals

Problem 30003417 / OWR-15216-023. Investigation date: 2026-10-05.

## Outcome

**No resolution.** Neither universal equality has been proved or refuted here. No independence theorem or novelty claim is made. Five approach families recover known min–max tools, elementary special cases, and explicit obstacles, but do not close the central gap. The strongest retained conclusions are proved in `RETAINED_PROOFS.md`.

The exact two remaining questions are whether, for every regular uncountable κ with 2^{<κ}=κ,

bκ≤cov(Mκ),          non(Mκ)≤dκ.

These are equivalent, respectively, to the two original equalities, not a weakening of them.

## Exact target and conventions

The primary source is Jörg Brendle's contribution *Generalized cardinal invariants*, printed pages 561–563 of the 2017 Oberwolfach set-theory workshop report. The definitions on page 561 and the conjecture on page 562 were inspected in the complete PDF; page 562 was also visually inspected. [Primary report](https://publications.mfo.de/bitstream/handle/mfo/3575/OWR_2017_11.pdf?isAllowed=y&sequence=1)

The question asks for add(Mκ)=bκ and dκ=cof(Mκ), simultaneously, for regular uncountable κ satisfying 2^{<κ}=κ. Here:

- The space is 2^κ with basic cylinders determined by initial segments of length below κ.
- Meager means a union of at most κ nowhere dense sets. It does not mean merely a countable union, unless κ=ω, which is excluded from the conjecture.
- The comparison defining cof is ordinary inclusion of sets in the ideal.
- bκ and dκ use eventual domination modulo a bounded subset of κ, equivalently modulo fewer than κ coordinates because κ is regular.
- Strong inaccessibility, weak compactness, supercompactness, 2^κ=κ^+, and successorhood are not assumptions of the full question.

The adjacent suggestion about bκ=non(Mκ) and cov(Mκ)=dκ at successor cardinals is a different, stronger pair and is not silently substituted for this target. The two min–max formulas are already known. Proving them is useful verification, but is not a solution.

## Later literature and its actual scope

### Established comparisons

Brendle's *The higher Cichoń diagram in the degenerate case*, arXiv v2 dated 2022-02-02, proves add(Mκ)≤bκ and dκ≤cof(Mκ) without restricting to strongly inaccessible κ. Corollary 3 gives add(Mκ)=min{bκ,cov(Mκ)}; under 2^{<κ}=κ it also gives cof(Mκ)=max{dκ,non(Mκ)}. These formulas leave exactly the two inequalities stated above. Its counterexamples to the cofinality min–max formula occur outside the target arithmetic and do not refute the conjecture. [Inspected version](https://arxiv.org/pdf/1907.03111v2)

The article is published in *Tsukuba Journal of Mathematics* 46(2), 255–269 (2022). Some later bibliographies print volume 42; the publisher's volume page gives 46. [Publisher volume](https://program.math.tsukuba.ac.jp/publications/tsukuba-journal-of-mathematics/3943/?lang=en)

The BBFM manuscript's Question 84 explicitly asks about consistency of add(Mκ)<bκ and dκ<cof(Mκ), even for strongly inaccessible or supercompact κ. Its translation-envelope result is Proposition 30. [Institutional manuscript](https://eprints.whiterose.ac.uk/id/eprint/118463/1/cichon-large%28revised%29.pdf)

### Recent status and preservation obstacles

Tristan van der Vlugt's January 2024 dissertation lists both exact strict inequalities as open in Question 2.6.1(3)–(4), with their equivalent non/cov forms. This is positive evidence of unresolved status at that date, not a claim that no later work can exist. [Dissertation record and PDF](https://ediss.sub.uni-hamburg.de/handle/ediss/10850)

His 2025 survey *The Horizontal Direction* identifies cov(Mκ)<dκ for supercompact κ as the known horizontal separation, discusses a subsequent correction to its iteration, and explains the remaining difficulties with random, Laver/Mathias, Miller, and eventually-different methods. Question 4.8 concerns bounding preservation; Question 4.21 isolates a small-cofinality filter-completeness obstacle. The survey mentions progress through private communication toward a possible random-forcing construction, but does not provide a completed countermodel for either target equality. We do not upgrade that mention into a theorem. [Survey](https://arxiv.org/html/2503.04471v1), [published volume listing](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/2315.html)

The consistency of cov(Mκ)<dκ alone does not imply cov(Mκ)<bκ: bκ can be the smaller value. Thus that established separation does not answer either part of this problem.

### Compactness models do not prove universality

Honzik and Stejskalová's revised 2025 manuscript has a supercompact κ and a weakly compact λ>κ in the ground model, with μ≥λ, cf(μ)>κ, μ^κ=μ, and regular κ<κ*<μ. Theorems 4.1–4.2 produce extensions in which bκ,dκ and all four meager-ideal invariants have common value κ*, with 2^κ=μ and additional compactness properties. This supports the equalities in specific models; it does not prove them for every κ satisfying the original hypotheses. The precise iteration proof is imported from the literature, not independently reconstructed here. [Revised v2](https://arxiv.org/html/2308.13478v2)

An older author-hosted PDF includes additional DSS assertions absent from v2. It was not used as the controlling theorem statement. The v2 introduction expressly marks that additional assertion as unknown at uncountable κ. The meager-equality pattern relevant here remains in v2.

### Scope checks through 2026

The June 2026 revision of Hayashi and van der Vlugt's *Topology and category for singular product spaces* concerns singular-cardinal spaces and distinguishes several topologies. It does not turn a result about those spaces into a resolution for regular κ. Its introduction was checked for the relevant scope and citations. [2026 manuscript](https://arxiv.org/html/2605.09582v2)

A 2026 paper called *Cardinal invariants of a meager ideal* studies ordinary category in completely metrizable spaces, including κ^ω. The exponent and topology differ from the present κ^κ/2^κ bounded-topology problem. It was excluded as a purported solution on that basis. [Publisher abstract](https://doi.org/10.1016/j.topol.2025.109516)

Targeted searches for the conjectured equalities, higher category, and 2025–2026 developments found no verified later proof or countermodel. This is a bounded literature search, not an exhaustive proof of openness. No authors were contacted.

## Five approach families

### 1. Direct fusion and cardinal collapse

Recursion through at most κ nowhere dense sets establishes the generalized Baire bound κ^+≤add(Mκ). Combining this with cofinal coding proves both equalities when 2^κ=κ^+, the first whenever bκ=κ^+, and the second whenever dκ=2^κ. The recursion cannot simply be continued through an arbitrary μ with κ<μ<bκ: stems can already reach length κ. These are special cases, not a universal proof.

### 2. Translation and a common escape point

Explicit meager envelopes E(x,f) absorb small families once a point x outside suitable meager translates has been chosen. This proves the known additivity lower bound and cofinality upper bound. The exact obstruction is the surviving cov/non parameter. Selecting that point for every family of size below bκ, or selecting a nonmeager parameter set of size at most dκ, would assume the missing result.

### 3. Nowhere-dense tree coding

A tree constructed from g∈κ^κ yields a closed nowhere dense set N_g. A family of at most κ functions associated to each meager set detects when N_g escapes it. This recovers add(Mκ)≤bκ and dκ≤cof(Mκ), including successor κ. The direction is the already-known direction; no inversion of the comparison is obtained. All details retained are in Section 3 of the proof file.

### 4. Topological transfer and representation checks

An explicit unary-block homeomorphism transfers κ^κ to a dense comeager subspace of 2^κ. This justifies transferring topological category invariants and gives bκ≤non(Mκ), cov(Mκ)≤dκ. It does not transfer an inaccessible-only chopped-function representation to a successor cardinal. The 2025 survey's Question 2.3 explicitly preserves this distinction. This approach yields the exact reformulation but no missing inequality.

### 5. Forcing and small-cofinality preservation

Known Cohen/compactness models and the corrected horizontal-separation literature were checked for a countermodel. None inspected separates cov(Mκ) below bκ or non(Mκ) above dκ in the required regime. An explicit increasing sequence of uniform <κ-complete filters has a union that is not countably complete; its proof rejects an automatic limit-preservation shortcut. It does not prove that a carefully designed forcing construction is impossible.

## Prior work and provenance

The pinned public dataset revision is 37e53eabe540fb458758e198be61634bd02ee008. Both complete source files were retrieved and their SHA-256 hashes and byte counts independently matched against the repository manifest. Problem 30003417 occurs uniquely at zero-based list index 12201. Its exact statement and review hashes were recomputed and match the selected repository descriptor.

The separate research-results dictionary has no OWR-15216-023 key; the numeric ID is absent from that file's bytes. Therefore no separate upstream proof attempt for this target was available to audit. The problem's embedded literature triage was inspected and its scholarly pointers checked; it is not treated as a proof.

At repository commit 73300d9223ca6175983c78cb2370f99ffdd4b59c, the attempts directory has 62 entries and no 30003417 entry. Exact-ID and topic code/PR/commit searches, plus an exact-ID branch search, found no prior attempt. The related-target-groups file contains no group for this target. The queued 0/5 row was inspected, but is not the basis for the no-prior-attempt finding. Deleted branches, unindexed artifacts, and other unpublished working trees were not exhaustively searched.

## Completion and disposition

Source recovery and this bounded attempt are complete. A fresh independent audit remains required. Toward a new full resolution, the completion estimate is 0%: the central universal inequalities remain open in this work, and all affirmative equality cases retained are already-known or immediate special cases.

After independent review, the appropriate campaign disposition is an exhausted five-approach attempt with no resolution, retaining these proofs and the exact gap. Do not mark it solved, already solved, or proved independent. No remote write, publication, or queue mutation was performed in this investigation.
