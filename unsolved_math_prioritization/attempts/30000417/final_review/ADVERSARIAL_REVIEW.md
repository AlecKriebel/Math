# Independent full review: 30000417 path list labeling

**Verdict: PASS for every scoped result; original floor conjecture remains unsolved5/5.** No mandatory mathematical revision. One implementation-complexity qualification is recorded below, additively, without changing frozen author files.

Bound author freeze: FINAL_FROZEN_MANIFEST.json SHA256 `b61d78498a62f1892c2932c9b98532b1bc8535f1994da35dc561d63c3e515739`;53files, remote commit `6b043cbbaec41b4cf1a6c5727046b277ecc83a75`, branch dot/math-30000417, folder unsolved_math_prioritization/attempts/30000417. All raw Git blobs match. This is an independent AI-assisted mathematical/computational audit, not human peer review or novelty certification.

## Exact source and credit

The complete Kohl contribution, [official OWR7/2006](https://ems.press/content/serial-article-files/46037?nt=1), printed414–417, was read; printed416 was visually inspected. Definition1 uses arbitrary natural-number lists and separation d at graph distances1 and2 when s=d. Theorem6 supplies n≥3 and the lower bound; Conjecture2 has **floor**, not the catalog's ceiling. The d=1,n=4 discrepancy refutes only the transcription. The adjacent all-trees question is separate.

[Kohl's2006 dissertation](https://webdoc.sub.gwdg.de/ebook/dissts/Freiberg/Kohl2006.pdf), printed100–102, retains the path conjecture and explicitly gives common-global-extremum and interval-list sufficient cases in Theorems4.14–4.15. Those methods and the weighted ordinary-path lemma are correctly credited. The full2005TCS article was not independently retrieved; its attribution is supported by the same-author dissertation and the original report, with that access limitation retained. No current-search absence is a proof of novelty or continuing literature openness.

## Turns1–2: finite reduction and deficit method

Gap compression preserves the exact predicate |a−b|≥d: either an intervening gap is already≥d and retains size d, or all relevant gaps are unchanged. It is injective, preserves lists/intersections and gives the finite bound1+d(nk−1). This is distinct from one-way rank expansion. The reachable-pair recurrence checks precisely the two new distance constraints, so empty terminal relation and predecessor recovery have the stated meanings. Fixed-parameter termination is proved, not claimed practical for all instances.

The known n=3 and d=1 boundary proofs are sound, including equality thresholds and the n=2/d=0 qualifications. The weighted path lemma correctly bounds integers simultaneously close to all preceding feasible labels by max(0,2d−|S|), and its strict total deficit<2d is essential. Removing one modulo-three class from a squared path leaves an ordinary path, with endpoint geometry checked. A common extremal anchor removes at most d integers per retained list; floor/ceiling conversion and q(ceil(3d/n)−1)<2d hold strictly. No hypothesis creating a common label from arbitrary lists is smuggled into the argument.

## Turns3 and5: all-length machine theorem

The rank map is used only in the safe direction: a labeling on consecutive ranks expands to the original integer labels. It is not a feasibility equivalence, and no bound on arbitrary union size follows from it.

The machine state is the exact reachable relation of the last two labels. Initial states cover every ordered pair of six-element lists. For an old row b containing preceding labels S, the next row c contains b exactly when |b−c|≥2 and S has some a with |a−c|≥2. I inspected both implementations and independently exhaustively compared every nine-label single-row contribution with the literal set-pair relation. Taking unions over rows and masking the next list is exact. Dropping duplicate successor states does not drop any possible input transition.

The Python proof replay has no cap and processes every added state. Its complete nine-label closure contains4,087,257 states and covers343,329,588 list-input transitions, with no empty state. The compiled packed C++ implementation was independently rerun to its CLOSED outcome, below its exploratory cap, and produced44,959,827 state bytes with SHA256
`1e684d75b22798311196274b81cbaae77fe4154a5b691998ddabfc3a6819f791`.
This equals the Python full sorted-state digest. The serialization is81-bit states in11little-endian bytes, numeric ascending order. The eight-label and smaller closures also replay exactly. Their induction genuinely covers every path length: depth43 is a maximum shortest-state prefix statistic, not a bound on n.

The complete result is therefore: **all path lengths, d=2, six-element lists, union size at most nine**. The explicit impossible five-list P6 instance is one below the target and extends to longer paths, proving sharpness only within this stated restricted family. The d=3 eight-list P13 obstruction is likewise below the source's nine-list target. Neither is an original-conjecture counterexample. The nonempty state with too few robust rows defeats only a proposed stronger invariant.

The ten-label cyclic-six-list construction has a complete cooccurrence graph. Hence any single global map preserving six distinct images on every list must be injective. Its explicit valid labeling passes. This blocks precisely that palette-recoding shortcut, not vertex-dependent recodings, other proof techniques, or the source conjecture.

## Turn4: variable anchors and method limitation

Anchor vertices have no mutual constraints in the original squared path. Every remaining vertex sees one anchor or two consecutive anchors, so grouping unary/pair deficits counts every residual vertex exactly once. The Bellman recurrence minimizes that exact sufficient cost and reconstructs an optimum. Local-minimum hypotheses ensure all removed labels lie in at most d consecutive integer positions even when two anchor labels differ. The same strict deficit arithmetic proves the stated unrestricted-palette family; the reflected local-maximum case follows.

The42-vertex certificate has a valid direct labeling, and a separately implemented factor-by-last-anchor dynamic program confirms optimum4 in all three residue classes. Thus the strict<4 sufficient criterion is genuinely incomplete even after optimal anchor choice. No minimality or original infeasibility claim is made.

**Implementation qualification:** the theoretical O(nk³) comparison bound is attained with local incidence precomputed from the modulo-three geometry. The supplied Python anchor_solver.py instead scans all anchors for each retained vertex and uses list membership scans, adding an O(n²) preprocessing overhead. Its recurrence and correctness are unaffected. Its O(nk) score/predecessor storage bound remains valid. This distinction is recorded here rather than silently changing the frozen implementation or claiming its literal runtime is O(nk³) for fixed k and arbitrarily large n.

## Evidence and final disposition

All198 historical/final manifest bindings, both primary PDF hashes and53remote raw blobs match. The five author stdout receipts replay byte-for-byte, including365,597 finite assertions in turns1,2,4 and the complete closure/witness records in turns3,5. Separate reviewer controls pass98,448 assertions:4,608 local transition-mask comparisons,91,475 weighted-list families, geometry checks,972 independent brute anchor optimizations, and the large direct-labeling/4–4–4 certificate audit.

The written proofs establish the meaning of these computations; counts and hashes alone would not establish an all-length theorem. No raw PDFs, imported datasets, large state binaries or private coordination are part of this review bundle. No sixth author search was conducted.

Recommended publication disposition: **unsolved5/5**, with the source's floor correction, all-length bounded-union theorem, unrestricted-palette sufficient families and exact method barriers prominent. No unrestricted n,d/palette resolution, novelty, CI success, merge or release is claimed.
