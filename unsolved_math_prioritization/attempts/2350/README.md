# Erdős 864: three audited partial results

Problem 2350 / EP-864; queue row 1741. Edition: 12 October 2026 UTC.

**Original interval conjecture: UNSOLVED by this work.** The proposed leading upper constant is 2/√3. This packet supplies no unrestricted leading-constant improvement beyond √2, no integer counterexample, and no novelty or priority claim. It is an AI-assisted, unrefereed mathematical manuscript with two independent internal AI audits. Acceptance is not external human peer review, journal acceptance, or proof-assistant certification.

The exact target is a set A⊆{1,…,N} with at most one integer having more than one unordered representation a+b with a,b∈A and a≤b. Equal summands are included. The conjectural 2/√3 upper constant must not be confused with the existing reflected-Sidon lower construction.

## Complete proofs and audits

1. [Reflected-core weighted inequality](WEIGHTED_PROOF.md). For the reflected core C=A∩(T−A), k=|C|, m=|A|, and u=m−k, the exact sliding-window bound is

   W²≤(L+h)(Q+h−1)/h,

   where W=u+k/√2, Q=u+k/2, L is A's diameter, and h≥1 is an integer. It yields m−(1−1/√2)k≤√N+(3/2)N^(1/4), restricted-family and location-sensitive bounds, and u=o(√N) conditionally near the existing √2 constant. The entire proof, including exact difference structure, midpoint bookkeeping, energy, and the symmetric residual, is retained.

2. [Exact continuum relaxation and stability](CONTINUUM_BARRIER.md). The midpoint-free symmetric case gives two necessary convolution dominations D/P. Their relaxed maximum mass on [0,1] is exactly 1, uniquely attained by uniform Lebesgue measure. For a feasible density of mass c, ∫(f−c)²≤1−c². The relaxed optimum corresponds to √2 in the original normalization; it is not an integer construction. The complete finite-to-continuum argument, L² regularity proof, uniform witness, uniqueness, stability, and support-length corollary are retained.

3. [Finite-group supersaturation and exact carries](MODULAR_CARRY_PROOF.md). A nonempty strong Sidon set of cardinality k in a finite abelian group of order q that avoids B+B+B satisfies (3k²−k)/2≤q−1. For every translate, the exact ordered-coincidence identity is

   R(t)=k²−∑_{u∈H}r_t(u)+(k−1)r_t(0),

   with h=|H|=q−1−k(k−1), giving R(t)≥k²−2h. An injective integer lift partitions R(0) by carries; for representatives in [1,L] with L≤q, integer triple avoidance requires C₁+C₂≥k²−2h. Nonzero carries are permitted and are not a contradiction. The complete finite-group proofs and restricted construction consequences are retained.

[The first independent audit](AUDIT_WEIGHTED_CONTINUUM.md) covers results 1–2. [The second independent audit](AUDIT_MODULAR_CARRIES.md) covers result 3, with [its required lift clarifications](LIFT_CLARIFICATIONS.md). The two required modular clarifications are incorporated in the controlling proof. Both complete substantive audit bodies are retained; editorial notices are clearly separated.

The proofs use different local symbols: k is the full core size in the weighted proof and the positive-radius or modular cardinality in the other proofs; L is either diameter or positive-radius horizon. Each proof defines its own notation. A midpoint-free core has twice as many points as positive radii.

## Edition and verification

[Acceptance](ACCEPTANCE.md), [edition map](EDITION_MAP.md), [original input pins](INPUT_PINS.json), [source metadata](SOURCE_METADATA.json), [verification summary](VERIFICATION.json), and [scope review](SCOPE_REVIEW.md) state exactly what is retained and what was checked. [MANIFEST.json](MANIFEST.json) binds every other public member by SHA-256 and byte count; its own digest is pinned in the separate external seal and intended draft description.

Only authored proofs, complete substantive mathematical audits, acceptance, and aggregate public verification/citation metadata are distributed. Executable checkers, detailed computational outputs, source documents/text/images, dataset contents, exact search corpora, and private coordination material are excluded. No mathematical claim depends on an omitted numerical certificate: the universal arguments are written out. Finite checks support implementation diagnostics, not formal certification or asymptotic extrapolation.

The historical source-title error in the continuum input is corrected transparently to “Some of my Forgotten Problems in Number Theory.” The original input digest remains pinned. No other mathematical change is introduced beyond the two required modular lift/coset clarifications.
