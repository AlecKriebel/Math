# Worst-case LLL approximation on coefficient ideal lattices

Problem 8800068 / AMR-087-0068. Authored research and verification package, 2026-10-20.

**Outcome: partial results only; the chosen general sharp exponential-rate target remains unresolved.** No novelty or exhaustive literature-status claim is made. These results do not solve every interpretation of the historical question.

## Target and essential qualifications

The chosen target asks for growing-dimensional, full-rank coefficient ideals in monic quotient rings, with exact classical (3/4,1/2)-LLL-reduced ordered bases whose first-vector/SVP ratio has exponential rate 1/2. See [SCOPE.md](SCOPE.md) and the exact quantifiers in [PROOF_ATTEMPT_1.md](PROOF_ATTEMPT_1.md). This is Euclidean coefficient geometry, not an adjustable canonical-embedding metric. Stationary reduced-input existence is distinct from HNF-start behavior. First-vector/SVP and Hermite measures are distinct.

## Reading map

- [SOURCE_GATE.md](SOURCE_GATE.md): the original historical-source recovery snapshot. Its pending gates reflect that stage; subsequent attempts explicitly choose a target. [SOURCES.md](SOURCES.md) lists public citations and retrieval metadata.
- [PROOF_ATTEMPT_1.md](PROOF_ATTEMPT_1.md): precise target, a general-lattice near-critical control, and the increasing-degree triangular ideal obstruction.
- [PROOF_ATTEMPT_2.md](PROOF_ATTEMPT_2.md): reversed-control obstruction, exact companion congruences, additive cyclic quotient characterization, and a checked irreducible quadratic example.
- [PROOF_ATTEMPT_3.md](PROOF_ATTEMPT_3.md): growing evaluation-kernel ideals, exact planted shortest vector, necessary scales and large-parameter recovery obstruction.
- [PROOF_ATTEMPT_4.md](PROOF_ATTEMPT_4.md): a preserved natural relation prefix prevents hiding the short vector in too small a trailing block. This is not a theorem about all prefixes or all reduced bases.
- [PROOF_ATTEMPT_5.md](PROOF_ATTEMPT_5.md): noncyclic-additive-quotient construction through dual-number evaluation, with an exactly characterized short vector and finite reduction tests.
- [CYCLIC.md](CYCLIC.md): shortest-orbit-span bounds, including the power-of-two negacyclic exponent-1/4 obstruction. Cyclic symmetry alone is insufficient.
- [CONSTRUCTION_ATTEMPT.md](CONSTRUCTION_ATTEMPT.md): cyclic congruence-family large-modulus recovery theorem and two restricted searches.
- [NEXT_ATTEMPT.md](NEXT_ATTEMPT.md): exact shortest norm and a genuine growing cyclic family with nonshortest reduced first vectors, but only constant loss sqrt(4/3), plus a coordinate-prefix limitation.
- [AUDIT.md](AUDIT.md): independent adversarial review, qualifications and finite checks. Read alongside the proofs rather than interpreting accepted restricted claims as acceptance of the general target.
- [REPRODUCIBILITY.md](REPRODUCIBILITY.md), [requirements.txt](requirements.txt), and computation/: scripts, saved results and replay logs.

## What is not established

No family meeting the general exponent-1/2 target is proved; no global impossibility theorem for arbitrary monic coefficient ideals is proved. The cyclic constant-loss examples are not exponential-loss examples. Repeated shortest-first outputs, missing finite-search hits, and failed restricted constructions do not prove absence of adversarial reduced bases. The package makes no worst-case HNF-output claim.

## Integrity and publication boundary

The manifest records SHA-256 and byte count for every payload file, excluding the manifest itself to avoid self-reference. Only authored arguments/code, generated results, public citations and source-verification metadata are included. Source PDFs, extracted source text, datasets and coordination material are not included.
