# KOU-21.114 / UnsolvedMath 2623

**Outcome: unresolved after five substantive approaches. No solution or new theorem of novelty is claimed.**

The target, attributed to Luca Sabatini, asks whether the derived length is bounded by a single absolute constant among all finite groups G satisfying a(H)≤a(G) for every H≤G, where a(X)=|X/X'|. This is a uniform bound across all orders and primes. Nilpotency alone is not an answer.

## Identity and literature

The October 2026 editor-maintained 21st edition was checked at printed/PDF page 194. Problem 21.114 has neither a solved marker nor an unverified-AI-solution marker. Its annotation cites Lisi–Sabatini's reduction to direct products of weakly ab-maximal p-groups. The same question already appears as Question A in their 2024 paper, so the catalogue's proposed year 2026 is an issue date rather than its earliest identified appearance.

The original paper also constructs examples with arbitrarily large nilpotency class. Those examples are metabelian, so they do not refute a bound on derived length. Eberhard–Sabatini's 2025 paper resolves a different extremal-size question, Question C in the earlier paper, using class-two groups. It does not settle this target. The checked October 2026 source retains the target as open; literature search is not proof that no unindexed result exists.

## Main proved conclusions

- Quotient and direct-product closure are reconstructed. Any minimal counterexample to a proposed bound d has cyclic center and a unique minimal normal subgroup equal to its d-th derived subgroup, of order p.
- An elementary bound dl(P)≤ceil(log_2(a(a+1)+1)) follows when |P/P'|=p^a. It depends on a and gives no absolute bound.
- Cyclic holomorphs C_(p^n)⋊Syl_p(Aut(C_(p^n))) are weakly ab-maximal of class n and derived length exactly 2. A uniform proof includes p=2.
- A regular wreath product of two nontrivial finite p-groups is weakly ab-maximal precisely for C2 wr C2. The next iterated 2-wreath product has derived length 3 but its base violates the required inequality.
- UT_n(F_q) fails the inequality for every n≥4, using an explicit rectangular abelian subgroup.
- Direct-product padding, and specified central products along a commutator-center subgroup, cannot repair the offending wreath examples.

These are elementary reductions, reconstructions, and construction obstructions, not claimed resolutions of KOU-21.114 or claims of priority.

## Exact checks

Run:

    python3 verify_math.py
    python3 verify_manifest.py

The first command exactly recomputes CHECK_RESULTS.json without network access or third-party packages. It constructs 11 groups, checks all associativity triples, and exhaustively enumerates the subgroups of 9 groups. The two other cases use explicit disqualifying subgroup certificates rather than an exhaustive search. Negative controls distinguish strict from weak maximality, disprove subgroup inheritance, reject iterated wreath preservation, and distinguish nilpotency class from derived length.

## Files and release boundary

- PROOFS.md: arguments and precise open gap
- RESEARCH_LOG.md: the five approaches and why each stops
- SOURCE_VERIFICATION.json: public source/verification metadata, dates, hashes, and bounded repository-history checks
- verify_math.py and CHECK_RESULTS.json: portable exact finite controls
- LIMITATIONS.md: what was and was not established
- AUTHOR_MANIFEST.json and verify_manifest.py: deterministic safe-file integrity check

This author freeze contains no source PDFs, copied source extracts, dataset records, private coordination files, or raw account/repository responses. Independent audit is still required before publication. No remote write was made by this investigation.

## Primary references

- [October 2026 editor update](https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/)
- [Lisi–Sabatini, On groups with large verbal quotients, arXiv v4](https://arxiv.org/abs/2203.12021v4)
- [Eberhard–Sabatini, Probabilistic construction of some extremal p-groups, arXiv v2](https://arxiv.org/abs/2502.05821v2)
- [Published 2025 article metadata](https://wrap.warwick.ac.uk/id/eprint/191736/)

Exact retrieval scope and byte/hash verification are recorded in SOURCE_VERIFICATION.json.
