# Positive partial twists can destroy parity permanently

AIM problem 2.1, *Categorified Hecke algebras, link homology, and Hilbert schemes*: problem 20000079 / AIM-ALGEBRAIC_GEOMETRY-0079, rank 1265. Accepted partial result, substantive attempt 1 of 5. Novelty is unconfirmed.

## Established result

Over C, in the raw Hogancamp–Mellit Rouquier/Hochschild-cohomology convention, write s=σ1 and r=σ2 in B3, and set

γ = r s r² s² r²,       γ_k = γ s^(2k),       k≥0.

The [complete mathematical report](MATHEMATICAL_REPORT.md) and [independent mathematical audit](MATHEMATICAL_AUDIT.md) establish:

1. HHH(γ) is even in Rouquier homological degree, because γ is explicitly conjugate to the positive (3,4) torus braid.
2. For every k≥1, HHH(γ_k) has both Rouquier parities. Every positive power of this fixed proper two-strand full twist destroys parity of γ, and continuing that same twisting never repairs it.
3. Every ordinary unreduced Euler series in the family is coefficientwise nonnegative in the q-expansion at zero. Ordinary unreduced Euler sign coherence therefore does not suffice for parity, even for positive three-strand knot braids.

The complete proof retains the invariant-coordinate Koszul/Künneth factorization, both six-basis coefficient tables and trace substitutions, the polynomial Hecke recurrence for every k, the signed reduced coefficients, and the all-k unreduced nonnegativity decomposition. The tables are authored symbolic proof, not supplemental checker output.

For U=(1+a)/(1−q), the explicitly defined reflection reduction gives χ(γ_k)=U P_k. The Hecke identity yields

P_(k+2)=(1+q²)P_(k+1)−q²P_k,
[a²]P_k=q³Σ_(j=0)^(2k)(−q)^j.

Thus a²q³ and a²q⁴ have coefficients +1 and −1 for every k≥1. The proved T-even invariant-coordinate tensor factor transfers both parities to ordinary unreduced HHH. The independent audit retains its authored two-matrix/character argument and all mathematical scope checks.

There is also a single-step parity-preservation counterexample for L=sr²s and, by Garside conjugation, the conventional Jucys–Murphy braid rs²r. The all-k theorem concerns powers of s²; it makes no all-power claim for either Jucys–Murphy operation.

## Scope and credit

This is a proper FT2 inside B3. It is not the central FT3=(sr)³. No eventual-central-twisting theorem or general parity characterization is established. The family is not pure, so it does not refute the adjacent pure-Coxeter/nested-initial-full-twist question 20000081. No algebraic-link claim is made, and conjecture 20000080 is not refuted. Distinct raw Euler polynomials are not by themselves asserted to prove distinct normalized knot types.

Hogancamp–Mellit supply the positive-torus parity theorem and grading conventions. The first mixed example is the known positive knot 10_139, identified in the 2026 preliminary K3 problem volume. Turner supplies adjacent-family terminology. Exact public citations, source-file identities and recorded retrieval/inspection limits appear in [SOURCE_METADATA.json](SOURCE_METADATA.json).

## Review and distribution

This AI-assisted, unrefereed proof-and-audit edition makes no historical novelty, priority, current-openness, external human peer-review, journal-acceptance or formal proof-assistant certification claim. Acceptance rests on the written mathematics. Edition preparation claims no fresh scholarly retrieval, source-file rehash, source inspection or literature search.

[STATUS.json](STATUS.json) records partial attempt 1/5. [MANIFEST.json](MANIFEST.json) lists exactly six distributed files and hashes the other five; the pull-request body independently pins the manifest. These identities establish packaging integrity, not mathematical correctness.

Programs, checker outputs and receipts, fixtures, datasets, copied third-party source bodies, source-derived images and private coordination/version identities are excluded. Excluded computational material is not recast as prose. This addition-only edition leaves QUEUE.md and unrelated entries unchanged, adds no substantive proof turn and does not reset attempt accounting.
