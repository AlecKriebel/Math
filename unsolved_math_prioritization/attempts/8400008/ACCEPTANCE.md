# Fresh acceptance of the restricted O7b findings

## Determination

Accepted on 9 October 2026 after a fresh complete independent AI mathematical audit of the four reconstructed reports and a separate full reading of that audit. The audit completed at 2026-10-09T22:17:35.681135+00:00. No must-fix mathematical defect was found under the stated hypotheses.

This accepts the two reports' restricted mathematical findings. It does not accept either explored direction as a solution of O7b. The original target remains unresolved after two approaches, 2/5 turns, with no new substantive approach or turn consumed by reconstruction, auditing, or packaging.

## Exact reviewed reports

- reports/MODEL_AND_STATUS.md: 3,381 bytes; SHA-256 93214cb26eca4bf52ed8a116f67cbbee8c03a35a10526c17e3c8d6e85bd525a1.
- reports/SOURCE_VERIFICATION.md: 3,259 bytes; SHA-256 76c23317c3b9283dcc0ecb72602881863f6d6ac9e77debf2757e7aa1ea155f7a.
- reports/TURN1_RECONSTRUCTED.md: 9,221 bytes; SHA-256 906baa8b7c6c5f960c2f89e13aaebce7705458a679e93e5664237871c403cb4d.
- reports/TURN2_CANDIDATE.md: 11,602 bytes; SHA-256 7d57ffaed0175c46b807c251c8615eaa0749b339f1f6580a4ad5c55a722b2468.

These four files are distributed byte-for-byte under the same reports/ names. Their historical status language is intentionally unchanged. Turn 1's lost historical acceptance is not authenticated. Turn 2's previous “unaccepted” label is superseded by this fresh restricted acceptance; no old hash is treated as certifying reconstructed bytes.

The full original mathematical audit was 22,414 bytes, SHA-256 ae3ede846303bf4eed3f87a7f57e878a261a6486f64b9e770be2a11c073a0066. The distributed AUDIT.md is 23,176 bytes, SHA-256 a27b1301422ad15c63ee2e96fbb259ce2569239b95f62f1e33bde7dfba6fbed9. It retains all mathematical reasoning and the full supplementary-check discussion. The complete editorial changes are described in PROVENANCE.md: an edition note, replacement of the omitted auxiliary inventory's identity by an omission statement, and replacement of the omitted checker's local path by a descriptive phrase. No theorem, proof, counterexample, qualification, count, or audit verdict was removed or changed.

## Accepted scope

Turn 1 establishes deterministic gcd-layer support projection for positive squarefree n, exact simulation of the same virtual C7 transcript on each random tape with actual queries coprime to n, computable joint valuation blocks, and invariance only under the listed operations with every initialized integer included as a tag. Its root bound requires nonzero normalized polynomials fixed before fresh independent uniform samples, a pathwise degree budget, and separate treatment of coefficient-split successes. The success-without-split bound additionally requires a proved success-implies-hit premise within the specified restricted scheme. Conditioning on a future no-split event is not licensed.

Turn 2 establishes the exact sign probability 1-2^(1-k) conditional on sign-blind acquisition of a nonempty relation from independent uniform units modulo an odd squarefree n with k>=2 prime factors. If acquisition succeeds with probability rho, the total proper-factor probability is rho*(1-2^(1-k)). Neither uniform sampling with worst-case bounded tapes nor polynomial acquisition follows from that conditional calculation.

The fixed-batch theorem computes a polynomial-size basis of the entire binary square-product dependency space of an explicit positive-integer batch, using gcd-free refinement, perfect-square tests, and binary linear algebra. It does not enumerate all dependencies or guarantee a nonzero dependency in a sampled batch. The equality of the m_i and s_i dependency spaces removes no adaptive oracle-dependent batch construction.

The transporter theorem assumes odd squarefree n, s>0, equal nonzero norms K, n dividing K, and gcd(2srr',n)=1. With B=xr'-x'r and the primitive positive denominator c of the specified transporter, its conclusion is exactly

    gcd(c,n) = n/gcd(B,n).

The full c need not divide n and need not equal the right side. A proper factor occurs exactly for a mixed local sign pattern. The second representation is supplied, not constructed within the target complexity bounds. K=0 and nonunit cases are excluded for the reasons and counterexamples retained in the proof and audit.

## General integer-exponent convention

The explicit sign theorem uses a nonempty subset, so its square relation is an integer one with exponents 0 or 1. For the report's short integer-exponent extension, take integer exponents e_i with at least one odd e_i and require

    product_i s_i^e_i = h^2 in the positive rationals.

For negative exponents, interpret all products in the rational unit group whose denominators are coprime to n; reduce a rational a/b modulo n as a times the inverse of b. Since each s_i and r_i is a unit modulo n, a rational square root h of that product has numerator and denominator coprime to n. Thus Y=h*product_i r_i^e_i is a well-defined unit, while X=product_i x_i^e_i is evaluated in the modular unit group. The same sign argument applies because an odd exponent retains one independent sign vector. An all-even relation has no such guarantee. No assertion is made that a negative-exponent product is necessarily an integer square.

This is the explicit interpretation already adopted by the audit; it is not a new research result or an enlargement of the accepted subset theorem.

## Attribution, evidence, and remaining gap

Dixon's classical congruence-of-squares method, established gcd-free/coprime-basis work, valuation arguments, and elementary root estimates receive prior credit. The distinct-exponent result in arXiv:2412.12558v4 is a credited prior theorem outside the squarefree-composite input class. No novelty or historical priority is claimed. SOURCE_PROVENANCE.json states the actual inspection depth and retrieval limits; no raw source PDF bytes, sizes, or hashes were acquired or asserted for this edition.

The proofs and audit reasoning establish the accepted restricted statements. The audit's finite-check discussion records supplementary error detection, not a universal proof or the missing relation-acquisition theorem. No executable or separate computational output accompanies the edition.

Still absent are polynomial-bounded relation or representation acquisition; complete worst-case sampling, arithmetic, query, and tape accounting; and correct complete factorization of every positive input with at least half of allowed tapes successful. The original historical problem text was not recovered or independently inspected; the model is the stipulated target, not an authenticated quotation. This is not human peer review or formal verification, and it records no merge, release, or archival publication.
