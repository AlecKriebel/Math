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
