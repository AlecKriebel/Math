# Symmetric orbit quotient spectrality: an alternative proof

Problem 30005476 / OWR-12697711-010.

## Prior proof announcement and status

This is a complete alternative proof of a previously announced result.
Kummer–Riener’s final 2025 article, printed page 42, announces a proof by
Nicolà Schnieper using the Shift Theorem; its bibliography identifies his
2024 University of Bern master’s thesis, *Orbit closures and G-irreducibility*.
The thesis was not retrieved or independently verified. This edition claims
neither first resolution nor worldwide novelty.

Review and distribution status: AI-assisted and unrefereed. Acceptance means an
internal AI mathematical audit, not external human peer review or formal
proof-assistant certification. This is a prose edition, not a computational
reproduction package. No claim of first resolution or worldwide novelty is made.

## Exact theorem and argument

For every finite positive n and algebraically closed field K, let
S=K[x_ij : i in N, 1 <= j <= n] and let G=union_m Sym(m) act by finite-support
permutations of the first index. The space KQ(Spec(S)/G) is spectral, using
all ordinary prime ideals, the topological orbit quotient, and then the
Kolmogorov quotient. The original problem assumes K uncountable, but the proof
only needs algebraic closedness and covers every characteristic.

The proof descends each radical G-prime ideal to a countable algebraically
closed field, constructs a prime with the required G-core by a countable
multiplicative-set argument, and ascends that prime by scalar extension.
This proves sobriety. Equivariant Noetherianity then gives quasi-compactness
and an intersection-stable basis of quasi-compact opens. Every G-stable closed
subset is consequently a finite union of orbit closures.

The ordinary prime spectrum is essential. Neither rational points alone,
Spec(S^G), a GIT quotient, nor full-permutation point orbits replace this target.

## Proof, audit, and source scope

PROOF.md contains the complete proof, and AUDIT.md retains the complete
mathematical audit with its boundary checks and import register. The only
specialized import is Hillar–Sullivant equivariant Noetherianity, Theorem 1.1
and Corollary 3.5. Its relevant statements and finite-support applicability
were directly inspected; the foundational Gröbner/Higman proof was not
reaudited. Standard algebraic results are named in the proof and audit.

SOURCES.json records public source identifiers, versions, byte counts, hashes,
and the actual retrieval/inspection scope. It does not distribute source bodies.
The source announcement was checked in the final 2025 article, not inferred
from the older version’s continuing conjecture label.

## Eight-file prose edition

- PROOF.md: complete mathematical proof, with publication-facing editorial changes
- AUDIT.md: complete mathematical audit and limitations
- ACCEPTANCE.md and ACCEPTANCE.json: bounded internal acceptance and exact identities
- SOURCES.json: public bibliographic and verification metadata
- VERIFICATION.json: integrity and retained-evidence scope
- MANIFEST.json: exact membership and seven non-self hashes
- README.md: theorem, credit, scope, and distribution guide

No copied source documents, dataset contents, executable code, raw computation
outputs, private sources, or private coordination material are distributed.
Exact byte identities establish integrity, not mathematical correctness.
