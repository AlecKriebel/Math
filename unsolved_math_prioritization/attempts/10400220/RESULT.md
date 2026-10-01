# Conway mutation and ordinary unknotting number: five-turn partial results

**Original target remains unsolved5/5. Independent review pending.** This is Ohtsuki Problem12.15, dataset10400220, with protected exact alias2662(b). The connected-sum question2662(a) is separate and untouched. No claimed solution, new exact small-knot unknotting number, or historical novelty is asserted.

## Exact source target and existing input

The source asks whether ordinary Conway mutants can have different ordinary unknotting numbers. Ordinary crossing changes, a four-punctured Conway sphere, and knots in S3 are retained. Genus-two mutation, generalized untwisting, equivariant unknotting of a strongly invertible knot, and slice genus are different questions.

Gordon–Luecke's complete theorem that u=1 is preserved by mutation is credited, as are classical double-cover crossing-surgery theory and the known Kim–Livingston four-genus disparities. The 2026 Kirby list still lists the general mutation problem; the bounded source search here is not a certificate of exhaustive literature coverage.

## Retained scoped statements

1. **Marked local distance (turn1).** Mutation acts on the graph of marked knot-and-sphere pairs with crossing balls disjoint from the sphere. Distance delta to the u=1 shell is invariant. For nontrivial K it is finite and u(K)-1<=delta. The difference between mutant unknotting numbers equals the difference of the localization defects. If u(K)=2 and a local change reaches u=1, its mutant also has u=2. This is a restricted equality theorem, not unrestricted localization.
2. **Four-genus candidate obstruction (turn2).** For the credited Kim–Livingston family, the exact genus-one Seifert form gives determinant9, zero ordinary signatures and the stated threefold-cover module. A proposed smaller-side upper certificate below the larger-side four-genus lower bound would also violate the separate nontrivial-summand lower-bound conjecture in this particular connected-sum family. That conjecture is not assumed true. Componentwise upper bounds cannot produce the proposed disparity, and the known four-genus differences do not determine u.
3. **Marked cover certificate (turn3).** Ordinary u(K)<=r is characterized by at most r simultaneous distance-two rational-tangle replacements, equivalently the specified equivariant strongly-inverted solid-torus surgery certificate from the standard unknot cover, ending in the full branched-cover pair. The primitive slope normalization is proved. A homeomorphism of the unmarked covers does not transfer the deck action and quotient certificate.
4. **Displayed resolution cube (turn4).** For a fixed displayed mutant pair, every crossing subset produces mutants. The exact Boolean functions for resulting u=0 and u=1 agree after crossing-label permutation. Thus all displayed unknotting subsets, their cardinality/weighted minima and the marked visible-diagram minimum agree. The latter can genuinely exceed ordinary u: the credited EM-knot examples have u=1 but no disjoint unknotting arc. Positive localization defects alone therefore do not produce mutant disparity.
5. **Concrete final candidate and certificate (turn5).** A source-pinned join of865 published mutant groups and the KnotInfo workbook finds no disjoint displayed intervals; its sole differing pair is11n76 listed3 versus11n78 listed[2,3]. The reference gap for the former prevents treating that cell as an independently verified lower bound. For the exact four-strand word assigned to11n78, a three-change, ten-move Artin/Markov certificate is fully proved and checked. The restricted two-change search failed; it is not a lower bound. A classical finite-type realization theorem implies that no universally valid lower bound depending only on a bounded-order Vassiliev class can exceed1, and no finite such upper bound exists. It does not preserve a mutant family or additional geometric constraints.

## Remaining original gap

There is no pair with rigorously certified different ordinary unknotting numbers and no proof of general equality. The unresolved step is a mutation-sensitive unrestricted lower bound coupled with an actual upper certificate, or a valid transfer theorem for optimal nonlocal crossing data. Neither unmarked-cover equivalence, a table interval, a fixed-diagram search, a slice-genus difference, nor a bounded collection of finite-type values supplies that step.

## Reproducibility

- Read SOURCE_GATE.md and all five TURN_N.md files. Historical turn snapshots remain unchanged.
- Run `python check_turn1.py`, `python check_turn2.py`, `python check_turn3.py`, `python check_turn4.py`, and `python check_braid_certificate.py`; compare stdout with the respective `turnN_checks.json`. These are finite exact controls, not general topology proofs.
- Run `python search_braid_certificates.py`; compare stdout with `turn5_search_receipt.json`. Its negative result is only for the explicitly stated move graph.
- The optional data screens take a directory of the pinned source files: `python screen_published_tables.py SOURCE_DIRECTORY` and `python screen_knotinfo_intervals.py SOURCE_DIRECTORY`. Compare with `turn4_candidate_screen.json` and `turn5_data_screen.json`. The latter requires the standard xlrd reader. Sources are identified and hashed in the source manifests; full PDFs, texts, workbook and table files are reading copies and not redistributed.
- The braid certificate states the actual word and all moves. Its topological upper bound concerns that closure; the tabulated knot identification is attributed to KnotInfo.

Five substantive turns are exhausted. Independent review, corrections and authorized publication do not add a sixth research turn. Proposed final queue status is unsolved5/5, with any alias row handled only after an explicit live check and authorization.
