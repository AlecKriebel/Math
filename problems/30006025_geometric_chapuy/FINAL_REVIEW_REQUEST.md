# Full independent review request

Problem 30006025 / OWR-14298589-010, geometric Chapuy bijections. Five substantive author turns are frozen. Recommended original disposition: **unsolved 5/5**. No further author search is requested.

## Complete packet and binding

Read `SOURCE_GATE.md`, `FINAL_RESULT.md`, and all five `TURN_n.md` proofs, checkers, receipts, states and manifests. The final manifest binds all public files. Historical turn states correctly record their then-current status and are immutable. Sources and inspected pages remain in the sibling working directory's `sources/`, not in the public packet. Source hashes and additional reading scopes are in `SOURCE_HASHES.json` and the turn-2, turn-3 and turn-4 source addenda. The final WIP commit will be supplied separately after raw-byte readback.

## Exact source and bibliographic distinctions

- OWR 41/2024: `OWR_2024_41.pdf/.txt`, `printed2405.png`. Read Louf's complete contribution, printed 2404–2406, especially Question 4. The imported volume-identity language belongs to Question 6. The source leaves “nice/geometric” unspecified. The report is 2024, publication 14 February 2025.
- Chapuy 2010: `chapuy2010.pdf/.txt`, a dominant-subset fixed-genus result, not the later exact all-map CFF theorem.
- CFF 2013: `cff2013.pdf/.txt`, Theorem 5, signed odd cycles, rooting and 2^(n+1) copy multiplicity. No naive cyclic gluing is substituted for its bijection.
- Janson–Louf: `janson-louf2021.pdf/.txt`, graph scale √(12g/n), g=o(n), and Conjecture 1.5's polygon interpretation.
- Published Barazer–Giacchetto–Liu: `bgl2025.pdf/.txt`, intro, Sections 2 and 6. The known tree/Dirichlet sampler and moduli correspondence are credited. Face perimeter is **2∑edges**, and the source fixes it to **12g**. PDF includes a download footer and stays local-only.

## Highest-risk proof points

1. Turns 1–2: closure in PSL(2,R) only implies trace±2 in an SL lift, which is used only as a necessary condition. Audit the nonzero analytic constraint on the fixed-sum simplex, the transcendental barycenter trace, the maximal-exponent uniqueness, arbitrary finite pairing choices, and the countable versus uncountable angle-profile distinction. `delaygue2025.pdf/.txt`, `delaygue-page1.png`: only the classical Hermite–Lindemann and Lindemann–Weierstrass statements in the introduction are used.
2. Turn 3: smoothness of arbitrary valid cubic one-face side pairings; marked versus unmarked laws; clean dessin degree convention and index N=12g−6; the subgroup only gives a systole **lower bound**, not equality. `uniform-dessins2025.pdf/.txt` Section 2 and Lemma 1, and `philippe2008.pdf/.txt`, `philippe2686.png`, Corollary 5.2 at p=3, provide the credited inputs.
3. Turn 3 probability normalization: use **only the displayed** Mirzakhani–Petri theorem intensity (cosh t−1)/t matching the OWR source, not a nearby small-epsilon sentence or numerical expected-value approximation. Read `mirzakhani-petri.pdf/.txt`, `mp-page2.png`. Check μ[1/2,1]>3/16 and 1−exp(−μ)>3/19. This is a count-law comparison for this special model, not a universal geometry impossibility.
4. Turn 4: Izmestiev's Theorem 1 applies to an **intrinsic** topological disk with arbitrary positive boundary sector angles and no interior cone points. Audit the cut completion even when vertices/edges recur in the face word, bridges contribute twice, and a developing map need not be injective. Read `izmestiev2014.pdf/.txt`, `izmestiev-page1.png`, definitions and Theorem 1, Sections 1.1–1.4. The area 4π(g−1) uses a smooth closed curvature−1 surface. Check the exact genus-12 threshold and every deformation bound; no existence claim is made below it.
5. Turn 5: normalized exponential independence, the exact top-k Dirichlet mean, inclusion-exclusion control, adaptive location quantifiers and outer-probability version. Check all edge cases k=0, C=1, k=E, the harmonic/log bound, uniformity over rules, and Jensen's expected-stretch lower bound. Arbitrarily large sparse corrections are not excluded, nor are topology changes or other comparison notions.

## Replay

Run `python verify_turn1.py` through `python verify_turn5.py` in the packet directory and compare each stdout byte-for-byte with `TURN_n_CHECKS.json`. SymPy is required only for turn 1. The final replay receipt gives **15,618 exact assertions**. Source theorems must be reviewed independently; a checker pass alone is not a geometric or probabilistic proof.

Please preserve all frozen author bytes and keep review artifacts separate. Report any defect promptly. Bind the final verdict to the final manifest and verified WIP head. Parent retains disposition and publication approval.
