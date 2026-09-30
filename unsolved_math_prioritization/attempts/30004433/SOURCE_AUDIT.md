# Source and prior-attempt audit, 2026-09-30

## Original target

The unsolvedmath page was requested first but could not be retrieved. The complete pinned record is preserved in `source_record.json`, from corpus revision `37e53eabe540fb458758e198be61634bd02ee008`. Its August 2026 assessment calls the problem open and cites only the OWR report. No entry for this exact problem number was present in the imported `research_results.json`.

The full official report was retrieved from EMS Press. The entire Berger contribution, printed pp. 625–627, was read, and pp. 625–626 were visually inspected. The published question really contains the two proposed end counts; these are not introduced by the dataset. The model is independent, undirected, translation-invariant on the integer lattice, with every displacement probability strictly between zero and one. The contribution focuses on dimension one and inverse-square decay for this problem. It does not define a nonstandard end notion or an incipient-cluster law.

The workshop occurred in February 2020; the report was published in 2021. Its preceding Theorem 3 discusses critical percolation, but its abbreviated wording does not specify every possible one-parameter family. The artifact therefore proves a parameter-independent conditional end theorem and separately supplies a precise nearest-neighbor-parameter family with positive critical density.

## Classical primary dependencies

All three complete primary journal-paper PDFs were obtained from the university-hosted percolation-paper collection linked in `source_manifest.json`. These are copies of the published papers, not generated summaries. Their title pages, pagination, statements and bibliographic identities agree with the primary publisher records and the original report's references.

- **Aizenman–Kesten–Newman 1987.** Read the introduction's distinction between actual critical clusters and incipient clusters, the full model setup and Proposition 1.1 on p. 507, and its proof reduction in Section 4, pp. 524–525. Visually checked p. 507. The theorem concerns independent translation-invariant irreducible long-range bond models. There is no exclusion of a critical parameter with positive percolation probability. The setup allows the exact source model. The proof reduction invokes earlier free-energy propositions; this package credits the established uniqueness theorem rather than claiming a new independent reproof of those propositions.
- **Newman–Schulman 1986.** Read the introduction and Theorem 1.2 on p. 549, and visually checked its statement. It fixes all probabilities at lengths greater than one and gives unoriented percolation when the nearest-neighbor and site probabilities are sufficiently close to one, provided the liminf of the inverse-square coefficient exceeds one. Setting every site present gives the bond case used here. The full renormalization proof is an imported classical dependency, not re-certified by our finite controls.
- **Aizenman–Newman 1986.** Read the full introductory setup, regularity definition, Proposition 1.1 and its coefficient definition on pp. 613–614, plus the two-parameter phase discussion. Visually checked pp. 613–614. Its coefficient is the limsup of $j^2p_j$, and its conclusion is $\beta\theta^2\ge1$ whenever $\theta>0$. All probabilities must be below one in the regular independent case. The artifact supplies the right-continuity argument at the chosen critical parameter; it does not assume left continuity or percolation at an arbitrary unspecified critical point. The deep renormalization theorem remains credited.

Springer's AKN metadata and the author's publicly indexed full-text upload were also checked. A Project Euclid download returned an HTML challenge, not a PDF; that response is retained separately as `akn-projecteuclid-response.html` in the local source cache and is not a mathematical source. The complete usable AKN PDF was subsequently obtained through the independent university collection. No access restriction was bypassed.

## Prior-work and duplicate gates

The selected queue row was rank 127, queued, 0/5. The exact target was absent from the local campaign state, assessment history, related-target groups and prior selected-path history. Exact all-state GitHub PR search for 30004433 returned no result, and the dedicated remote branch was absent before this work. A percolation-keyword PR search identified PR31, concerning the distinct vertical-fiber problem 10000043; its title and full body were read and do not attempt this end-count question. Corpus comparison did not identify a duplicate statement. This is a bounded evidence-based prior-work gate, not a claim that every historical binary file was searched.

No shared queue or generator was edited. There is one credited theorem-validation family and no fresh proof-search attempt. The recommended post-review classification is `already_solved`, 0/5, for the literal ordinary-end question. The mathematical content and source interpretation still require the separate reviewer before a PR.

## Current-literature and interpretation limits

Bounded searches included the exact paper titles, ordinary one-ended long-range clusters, the two-ended/infinitely-many-ended assertions, and the author's name. No published correction or clarification of this particular OWR question was located. This absence is not a novelty claim. The artifact explains its classical theorem dependencies directly, without inferring the intended alternative question. Results about hyperbolic graphs, dependent graphical models, incipient clusters, or long-range graph distances were not substituted for the given model.

The negative answer depends on the standard graph-end interpretation. It does not decide any reformulated question about a different law or different invariant. In particular it does not claim that an infinite critical cluster exists for every possible parameter family merely from its tail exponent.
