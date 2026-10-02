# Source and prior-attempt gate: 2594 / KOU-21.85

Gate completed 2026-10-02. Initial substantive author count: 0/5.

## Pinned exact source

The target asks whether flexible permutation stability implies permutation stability. The definitions immediately preceding it in Problems 21.83–21.84 are essential: G is finitely generated; f_n:G→Sym(n) is asymptotically multiplicative in normalized Hamming distance, pointwise for every fixed pair g,h. Ordinary repair is a sequence of genuine actions on the same n points. Flexible repair is a sequence of genuine actions on m_n≥n points, with disagreement on the old n points tending to zero and (m_n−n)/n→0. The latter condition is part of the definition and cannot be dropped.

Primary current source: Khukhro–Mazurov, *The Kourovka Notebook*, 21st edition, arXiv:1401.0300v47, revised 30 September 2026, printed p. 189. Complete PDF downloaded and p. 189 visually inspected. PDF SHA-256: `a93b2d27c3f6dcba3103450a2e56ca083377a7431bec04fbc75bff025f145e76`.

- https://arxiv.org/abs/1401.0300v47
- https://arxiv.org/pdf/1401.0300v47
- Editors' October update: https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/
- Current official PDF: https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf

Problem 21.85 has neither a solved mark nor an AI-proposal mark in the current edition. The October update-only file contains no entry for 21.85. These observations do not prove that no unindexed solution exists.

The requested https://www.unsolvedmath.com/problems/2594 could not be retrieved. Its exact pinned fallback record was read from the repository's authorized dataset revision `37e53eabe540fb458758e198be61634bd02ee008`; prior research result is null. The direct alglog PDF route returned a certificate-expiration error, which was not bypassed. The independently accessible official WordPress/arXiv editions supplied the source.

## Prior gate

Live exact-ID PR, branch, and commit searches returned no prior attempt. Alias PR searches for `21.85` and `permutation` found no overlapping mathematical effort; a `stability` search returned only unrelated targets. Default-branch code search for flexible permutation returned no results. An all-ref local commit-message search across 425 available refs for 2594, 21.85, flexible stability, and permutation stability returned no hits. Live state has no 2594 entry; catalog/QUEUE report queued 0/5. Catalog statement hash is `2d92866e18429d8f542dd2123c570170e07449c592106e9fe49c1a65b16981ae`, review hash `c697be3fbe6b1fcc6456e9176b94a17ad25efef7b46de8cd7cf979d1abe299aa`.

The already exhausted target 2579 is skipped. Nearby metabelian stability (21.83), SL_n(Z) flexible stability (21.84), and general soficity (21.86) are not silently absorbed into this assignment.

## Verified primary literature boundaries

Adrian Ioana, *Stability for product groups and property (τ)*, J. Funct. Anal. 279 (2020), 108729, arXiv:1909.00282, Lemma 3.2(1), proves the desired implication for amenable groups. The complete author preprint was downloaded; its definitions and the full proof of Lemma 3.2 were read. That argument uses large almost-invariant subsets of a challenge, flexibly repairs a slightly smaller restriction, and fills the unused points trivially. Its amenable conclusion is credited, not claimed anew. Lemma 3.2(2) equates flexible and very flexible stability for property-(τ) groups; it does not prove their flexible stability. Theorem A's product examples are not even very flexibly stable and therefore cannot supply a counterexample to the present implication. Preprint PDF SHA-256: `7ca32d8dcb7277fb58addd9296ab0e0caecc11aa374f5132b7835598cd9d829d`.

- https://arxiv.org/abs/1909.00282
- https://arxiv.org/pdf/1909.00282

Lubotzky–Salomon, *Z² is flexibly stable in the operator norm*, arXiv:2607.17578v1, July 2026, gives a separation in a different metric category. Its primary introduction was read and expressly distinguishes permutation stability; it still lists ordinary permutation stability of surface groups as open. No unitary-matrix counterexample is transferred to permutations. The existing flexible stability of surface groups is credited there to Lazarovich–Levit–Minsky, JEMS 27 (2025), 1739–1768.

- https://arxiv.org/html/2607.17578v1

A new author turn must therefore address exact same-cardinality repair in the permutation setting, not repeat the known amenable result or the operator-norm separation. Raw source files remain local-only.

Further primary mechanism check before the first proof freeze: Becker–Chapman, *Stability of approximate group actions: uniform and probabilistic*, JEMS 25 (2023), 3599–3632, DOI 10.4171/JEMS/1267, full PDF https://ems.press/content/serial-article-files/32932 was retrieved. Its Theorem 1.1 and introductory comparison distinguish uniform stability from the pointwise source notion. One-point compression is a credited classical instability device, not a new construction. PDF SHA-256: `420606d4ee0f054c8c58702c285712a1caa6764ab2bbe8e5bce408ed7b0d9bad`. The downloaded Ioana file identifies itself as arXiv:1909.00282v1 (31 August 2019); the publication citation above identifies the later journal article, while the checked proof text is this pinned preprint.
