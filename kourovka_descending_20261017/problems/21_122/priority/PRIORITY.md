# 21.122: preliminary priority audit

As of 2026-10-24 UTC. Preparation complete; discovery estimate 0%.

**Recommendation:** `provisionally_eligible_no_complete_resolution_located`.
No authenticated complete solution or counterexample to the exact arbitrary-word,
arbitrary-profinite-group **value-set** dichotomy was located. This is a bounded
literature-search finding, not proof of mathematical openness. No top-level status
is set here, no original mathematics is claimed, and no publication is prepared.

## Official source check

The current main Notebook gives P. Shumyatsky's question on page 197 with no added
solution comment; its cited 2020 paper settles important words. The fresh official
updates have no occurrence of 21.122. Exact scope, source hashes, and the update
PDF's date anomaly are in SOURCE_CONTRACT.md. Neither unstarred status nor absence
of an update is sufficient to establish openness.

## Authenticated primary results and exact remaining scope

The following theorem statements and relevant proof passages were read in full
primary texts, not inferred solely from abstracts. The raw files, versions, access
times and hashes are in SOURCE_MANIFEST.json. Set notation differs by source.

| Primary source | Verified result pertinent to 21.122 | Restriction or remaining gap |
|---|---|---|
| E. Detomi, B. Klopsch, P. Shumyatsky, *Strong conciseness in profinite groups*, J. London Math. Soc. (2) **102** (2020), 977–993; [DOI](https://doi.org/10.1112/jlms.12342); [arXiv v2, 25 March 2020](https://arxiv.org/abs/1907.01344v2) | Theorem 1.1: every multilinear (outer) commutator word is strongly concise in every profinite group. Theorem 1.2: every word is strongly concise in nilpotent profinite groups. | Neither all ordinary words on arbitrary profinite groups nor the weaker full set dichotomy is proved. |
| E. Detomi, *A note on strong conciseness in virtually nilpotent profinite groups*, Arch. Math. **120** (2023), 115–121, online 27 November 2022; [publisher](https://doi.org/10.1007/s00013-022-01808-z) | Theorem 1.1: every word is strongly concise in every virtually nilpotent profinite group. | Virtually nilpotent remains a group-class restriction; finite generation is not needed for this theorem. |
| E. I. Khukhro, P. Shumyatsky, *Strong conciseness of Engel words in profinite groups*, Math. Nachr. **296** (2023), 2404–2416; [arXiv v1, 25 August 2021](https://arxiv.org/abs/2108.11789v1) | Theorem 1.1: every n-Engel word is strongly concise in finitely generated profinite groups. Theorem 1.2: in an arbitrary profinite group with fewer than continuum n-Engel values, there is a **finite normal subgroup** \(N\) such that \(G/N\) is locally nilpotent. | The strong-conciseness statement retains finite generation; the arbitrary-group quotient conclusion is **locally** nilpotent. Neither restriction can silently be removed. |
| P. Shumyatsky, *On profinite groups admitting a word with only few values*; [arXiv v2, 22 February 2024](https://arxiv.org/html/2401.15707v2) | Theorem 1.1: for every word and every profinite group, \(|G_w|<\mathfrak c\) implies \(w(w(G))\) is finite. Proposition 3.1: every word is strongly concise on FC-generated profinite groups, namely groups with dense FC-centre. | The universal conclusion is an **iterated verbal subgroup**, not finiteness of the original value set. The proof makes \(w(G)\), not necessarily \(G\), FC-generated. Applying Proposition 3.1 directly to the original \(G\) would add a hypothesis. |
| I. de las Heras, A. Zozaya, *Strong conciseness and equationally Noetherian groups*, Ann. Mat. Pura Appl. **205** (2026), 749–758, online 18 November 2025; [DOI](https://doi.org/10.1007/s10231-025-01622-8); [arXiv v1, 11 February 2025](https://arxiv.org/html/2502.07427v1) | Version-of-record Theorem 1.1: the exact **set** conclusion holds if \(G\) has a dense equationally Noetherian subgroup. Corollary 1.2: all words strongly concise on profinite linear groups. Corollary 1.3: the same for pro-C completions of residually C linear groups. Theorem 1.4: the same if \(G\) has a dense virtually abelian-by-polycyclic subgroup. | The dense-subgroup or linearity/completion hypotheses are essential to the statements. The article does not assert that every profinite group has such a subgroup. |
| A. Zozaya, *Strong conciseness in profinite metabelian groups*; [arXiv v1, 3 August 2026](https://arxiv.org/html/2608.02237v1) | Theorem 1.1: every word is strongly concise in every profinite metabelian group. Theorem 2.8 proves the set implication for groups \(G=AB\), with \(A\) a normal abelian subgroup and \(B\) an abelian subgroup; no trivial-intersection assumption is stated. | The metabelian hypothesis is retained. Proposition 4.1 is about polynomial maps; Example 4.3 explicitly shows word maps need not be polynomial, even in the metabelian setting. It supplies no all-word-map shortcut on arbitrary groups. |

Additional precise partials in the original cited paper are Corollary 1.3 (words
whose countably generated free relatively free quotient is nilpotent), Corollary
1.4 (\(x^2,x^3,x^6,[x,y,y]\) and the listed further simple commutators), and Theorem
1.7 (weakly rational words or words implying virtual nilpotency, **with the further
hypothesis that the verbal subgroup is generated by finitely many word values**).
The last hypothesis is Conjecture 1.5 in general; treating it as proved would be
circular. Conjecture 1.6 asks for an open subgroup satisfying the word law and is
also not available as a universal theorem.

Detomi's 2023 Corollary 1.2 gives finiteness of an iterated verbal subgroup for
virtually soluble profinite groups, where the iteration count is the nilpotent
series length of the specified open soluble subgroup. It does not claim the
original set dichotomy in that full class. The later universal iterated result
above is broader in this respect.

The 2026 version of record of de las Heras–Zozaya was freshly downloaded from the
authors' [institutional repository](https://academica-e.unavarra.es/server/api/core/bitstreams/eb9ebdbb-3243-4cf1-b5c5-e5f3ad96cf5e/content).
Its Theorem 1.1, proof on printed page 755, and Theorem 1.4 were checked against the
preprint: the subgroup hypotheses remain. Corollary 1.5(ii) concerns virtually
abelian-by-**topologically finitely generated nilpotent** profinite groups. The
paper's open questions about stronger conciseness are not by themselves a status
certificate for the weaker Notebook question.

## Independent challenge and search limits

A separately tasked source reviewer attempted to find a complete prior solution,
including weaker set-only and equivalent-cardinality formulations, without
authoring new mathematics. Its frozen report is independent_status/AUDIT.md; the
exact query list and failed direct database access are preserved in
independent_status/SEARCH_SCOPE.json. It independently found no complete solution.
It also checked the current corrected version of Conte–Petschick,
[*Conciseness of first-order formulae*](https://doi.org/10.1007/s00605-025-02127-5),
Monatsh. Math. **209** (2026), 215–240, as a possible general definability shortcut.
The compact-group results there concern negative formulae, not the ordinary
existential positive word-value formula, and do not assert the target dichotomy.

A direct historical weaker-open-status lead is Matteo Pintonello's December 2023
PhD thesis *On Conciseness and Profinite RAAGs*, introduction page 2. A primary-source
search-index paragraph explicitly separates the small-value-set-finite question
from ordinary conciseness and calls the former open. Fresh full PDF recovery
failed (404; university record reset/503). The lead is corroboration only, not an
authenticated current full-text status certificate; links and failures are in the
independent report. No unpublished theorem was inferred from this excerpt.

Searches covered exact problem number, finite/continuum and countable-word-value
forms, strong conciseness, related terminology, arXiv, current publisher records,
the cited paper's references, and the 2024–2026 follow-up bibliographies. Direct
MathSciNet and zbMATH access was unavailable, and domain-limited web searches did
not yield a complete-resolution primary record. No claim of exhaustive database
coverage is made. Source absence is not proof of openness. QUEUE.md, PR numbers,
PR statuses, and unrelated agents' work were not used for selection.

## Handoff condition

Parent source audit and selection remain required before original research on
21.122. Any future candidate proof must face a fresh full-priority audit, including
the weaker **set** conclusion, and independent mathematical falsification. This
package neither promotes a result to `solved_verified` nor provides grounds for
publication as an original solution.
