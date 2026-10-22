# Recorded verification and distribution limits

The submitted note and its independent internal audit were accepted as an
unconditional partial result. This summary reports their recorded checks;
it does not replace the full mathematical analysis in AUDIT.md.

- Main seed: all 144 divisor-plus-one candidates classified, with 131 composite
  exclusions and 13 deterministically proved primes.
- Older seed: all 68 candidates classified, with 59 composite exclusions and
  9 primes. Both complete fibers have nine elements.
- An independent checker importing no candidate code enumerated the entire
  prime-exponent box: 116736 tuples for D and 6912 for the older seed.
- The complete ordered certificate lists and all 212 displayed factor-table
  entries agreed. Proper factors and deterministic primality were checked.
- Totient-sieve comparison for 1≤a≤100 against n≤20000 was complete by
  φ(n)^2≥n/2, including a=1 and odd nontotients.
- Candidate and independent checks passed in normal, -O, and -OO modes.
  Eight malformed-certificate controls were rejected in each independent run.
  Optimization did not remove required checks.

These finite checks establish the claimed complete fibers and exact minimum;
they do not computationally prove the imported analytic-number-theory inputs.
The whole-fiber theorem and counting lemma were checked for exact attribution
and application, including all-preimage quantifiers, equal fixed seeds,
fixed-constant dependence, and injection of the counted convenient integers.

The excluded factor tables, JSON certificates, detailed outputs, and executable
checks are not attachments to this edition. The finite classifications remain
proof dependencies left for reconstruction by deterministic trial division
from the stated divisor formulas. The audit's preferred embedded-table
recommendation is not implemented under this edition's scope; its acceptance
also permits the accurate disclosure used here. No claim is made that every
computational dependency is distributed or that omitted code is unnecessary.

The resulting bound is 4580175615/2239889408>2.0448. Positive lower relative
density is proved above this fixed threshold among totients. Existence of a
relative-density limit, positive natural density among integers, uniformity
in the seed, novelty, a global computational record, and divergence are not
claimed. The least-preimage divergence problem remains unresolved by this work.
