# Extremal modular forms modulo p: credited prior resolution

Canonical target: **30000160 / OWR-782-001**. Duplicate: **30000161 / OWR-782-002**, covered by this same audit and [acceptance](ACCEPTANCE.md).

## Disposition

The intended, corrected level-one conjecture is resolved by Alper Ferudun's *Extremal Modular Forms Modulo p and a Conjecture of Bannai, Koike, Shinohara and Tagami*, version 1.0, dated 1 October 2026: [Zenodo DOI 10.5281/zenodo.23071924](https://doi.org/10.5281/zenodo.23071924), Theorem 1.2 and Corollary 1.3. It is an explicitly unrefereed, AI-assisted note. This is an independent audit of that prior argument, with zero new proof-search turns and no novelty, priority, or journal-peer-review claim.

The conjecture is credited to Bannai, Koike, Shinohara, and Tagami. The classical modular-form inputs are credited to Swinnerton-Dyer and Serre, and the Hasse-invariant interpretation to Deligne.

## Accepted conclusion

For a normalized level-one extremal form f_k with nonconstant reduction modulo p supported on exponents divisible by p, there is an integral extremal form f_(k′) satisfying

    f_k(q) ≡ f_(k′)(q^p) modulo p,
    k′ = w(f_k mod p)/p,  4 ≤ k′ ≤ k/p < k,
    k′ ≡ k modulo p−1.

The proof includes an actual modular root obtained with the full-space Hecke operator, minimal-weight filtration, the exceptional residue class 2 modulo 12, and the small-prime and constant cases. Iteration produces the maximal exponent and a smaller-weight extremal form at every intermediate exponent. Only the reduction is unique; neither the characteristic-zero lift nor its weight is claimed unique.

This covers both parts of the original corrected Conjecture 4, including the stronger extremal-form wording of duplicate 30000161. This one directory is the canonical account of both formulations.

## Source corrections and limits

The printed OWR Case (2) divisibility sign must be corrected to p divides a_i when p does not divide i. The [2006 journal abstract](https://www.mathnet.ru/eng/mmj245) independently supports this reading. Acceptance concerns this intended statement.

The separate OWR Theorem 3 is false as printed at k=12, p=13. Its missing exclusion is identified, but a complete repair of that auxiliary theorem is not asserted. No arbitrary-level extension, non-extremal starting-form theorem, characteristic-zero equality, or global literature-priority certification is claimed.

## Read the argument

- [AUDIT.md](AUDIT.md): complete mathematical proof audit, exact classical dependencies, source corrections, and inspection limits
- [ACCEPTANCE.md](ACCEPTANCE.md): accepted scope and attribution
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public scholarly-source identities and originating retrieval/inspection metadata
- [STATUS.json](STATUS.json): canonical and duplicate coverage, status, and zero proof-search turns
- [MANIFEST.json](MANIFEST.json): this edition's exact file inventory and identities
