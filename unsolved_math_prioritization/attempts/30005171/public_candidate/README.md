# Smooth limits of prime-degree plane curves

Problem 30005171 / OWR-11101913-005, rank 948.

Status: unresolved after five substantive approaches. No proof or counterexample to the full conjecture is claimed. No novelty or priority claim. This authored packet is awaiting independent mathematical review.

- manuscript.tex and manuscript.pdf: complete partial-result manuscript, with exact assumptions, five approaches, and remaining gaps
- ATTEMPTS.md: concise approach ledger
- SELF_REVIEW.md: scope checks and author self-review
- verify_math.py: dependency-free exact arithmetic replay
- checks_result.json: recorded replay output, including all twelve degree-11 semigroup witness sets
- SOURCES.json: public scholarly metadata and inspection history only
- MANIFEST.json: byte counts and SHA-256 for the package files, excluding itself

Run: python3 verify_math.py
Optional: python3 -O verify_math.py

The strongest narrowly scoped computation excludes rational unicuspidal degree-11 plane curves with log canonical threshold at least 3/11. The manuscript gives a mathematical exhaustion proof before checking the twelve possible cusp signatures. It does not eliminate reducible or nonreduced divisors, curves on singular Manetti surfaces, or all degree-11 smooth limits.

All mathematical assertions depend only on the stated sources and the proofs in the manuscript. The source PDFs, copied text, retained corpus records, and coordination files are not part of this authored candidate. This packet itself performs no repository or queue changes.
