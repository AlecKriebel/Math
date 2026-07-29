# Lemma dependency ledger

This file records logical dependence rather than chronology.

## Primary spectrum theorem

The complete spectrum theorem will require both:

1. **Necessity:** an obstruction for every arbitrary matrix-class solution in
   the excluded dimensions.
2. **Sufficiency:** exact constructions in every claimed allowed dimension.

Known \(d=4\) plus spectator stabilization already proves sufficiency for
\(4\mathbb N\).

## Audited structural chain

The first implications are now proved for every arbitrary solution:

```text
(YB-P) + rank(P)=d²/2
        |
        +--> abstract two-projection block theorem [PROVED]
        |
        +--> scalar partial traces [PROVED via no-opposite-spectrum theorem]
        |
        +--> all-level Markov trace with eta=1/2 [PROVED]
                       |
                       +--> faithful Jones--Wenzl quotient representation [PROVED]
                                      |
                                      +--> exact central multiplicities [PROVED]
                                                     |
                                                     +--> only 2 | d
```

Thus a possible extra factor of two cannot arise from central ranks,
simple-block multiplicities, or Bratteli inclusion recurrences.  It must
arise from strict tensor locality/coherence, or else a \(d\equiv2\pmod4\)
construction exists.

The first genuinely local divisibility chain is:

```text
scalar partial traces + spectator-sector restriction
        |
        +--> half ranks and overlap trace D/4 on D = r d²
                       |
                       +--> common-one/common-zero ranks D/8
                                      |
                                      +--> 8 | r d²
                                                     |
                                                     +--> d = 2 mod 4
                                                          forbids odd-rank
                                                          leg projections
```

This proves \(4\mid d\) for every solution controlled on either leg, but
does not yet cover the branch where both one-leg commutants have only
even-rank projections. A global spectrum theorem now requires either:

1. proving that every exceptional solution has an odd-rank leg-commutant
   projection; or
2. obtaining a different invariant that also excludes scalar/even-block
   commutants; or
3. constructing a noncontrolled \(d\equiv2\pmod4\) solution.

## Candidate construction chain

```text
structured numerical or finite search at d=6
        |
        +--> exact algebraic recognition
        |
        +--> independent exact verifier
        |
        +--> extension mechanism
        |
        +--> spectrum sufficiency theorem
```

No numerical candidate enters a theorem until exact recognition and exact
verification are complete.
