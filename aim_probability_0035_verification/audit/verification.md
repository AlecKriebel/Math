# Mathematical verification

## Verdict and exact scope

**The candidate is correct for the universal finite deterministic heat-bath
censoring question.** A single q=3 counterexample is sufficient to disprove a
claim covering all ferromagnetic Potts models. The parameters are finite:
activity λ=30 and inverse temperature β=log(30)>0, with zero external field
and uniform coupling. The graph is simple and connected. The initial
configuration is monochromatic, and the deleted opportunity is fixed before
any spin is sampled.

Holroyd's primary paper, *Some circumstances where extra updates can delay
mixing*, [arXiv:1101.4690](https://arxiv.org/pdf/1101.4690), defines the
deterministic conditional-update comparison on page 1 and poses the
ferromagnetic constant-start question on page 4. These are exactly the
dynamics used here. The UnsolvedMath endpoints were inaccessible during this audit. The original
[AIM problem list](http://aimpl.org/markovmixing/1/) was successfully retrieved
over plain HTTP: Problem 1.5, attributed to Yuval Peres, asks precisely the
q-state (in particular q=3), all-green, deterministic-censoring question. The
source audit records the retrieval hash, HTTPS certificate limitation, dataset
transcription, and independent corroboration from Holroyd.

## Probability model and arithmetic

For each vertex, cancellation of Gibbs factors not incident to that vertex
gives conditional probability λ^(number of same-color neighbors), divided by
the sum of these weights over the three colors. This justifies the supplied
H and J, including the factors 900/902 and 1/902. Both implementations preserve
total mass exactly, and all five update operators preserve the full Gibbs law.

Enumeration of all 243 configurations gives the following counts by number
of monochromatic edges:

| Edges | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Configurations | 18 | 66 | 90 | 42 | 24 | 0 | 3 |

Consequently the partition polynomial is
3λ⁶ + 24λ⁴ + 42λ³ + 90λ² + 66λ + 18, and Z(30)=2207656998.
The supplied transfer-matrix derivation is also valid: the two eigenvalues
are λ+2 and λ−1, and conditioning on A=B versus A≠B gives exactly the stated
two terms. Direct enumeration independently checks every coefficient.

## Written reduction

The common first six updates introduce, in order, colors x at C, y at E,
z at B, c at C, b at B, and a at A. Multiplying their six conditional
probabilities and summing x,z gives exactly R(a,b,c,y) in equation (1).
Summing the old B color u and E color y, with or without the intermediate
E update, gives F and Q in equations (2)–(3). The last E update gives the
common factor H(e;b,0) in equations (4)–(5).

D is never updated, so both laws are supported on D=0. This does not make
π a conditioned Gibbs law. The full stationary mass of that slice is 1/3 by
global color symmetry; its complementary mass is 2/3. On the slice, summing
over E gives exactly the unnormalized marginal in equation (6), and π has the
same final E conditional factor as both evolving laws. The verifier checks
these identities entry by entry, including every one of the 81 slice states.

To check equation (8), let d=Σ(π̄−X)₊ over the 27 triples. Since ΣX=1 and
Σπ̄=1/3, Σ(X−π̄)₊=2/3+d. The slice's absolute difference sum is 2/3+2d;
the complement adds 2/3. Dividing by two gives TV=2/3+d. Thus neither a
missing complementary contribution nor an accidental renormalization is
hidden in the reduction.

All 14 color-swap orbit representatives, including the differing `112` sign,
were recomputed exactly. None has zero difference. Both displayed
positive-part sums and both final fractions match:

```text
TV(μ,π) = 511715038479158504505751178946687363011
          / 766036711510586802141859485820665762204
TV(ν,π) = 9300189570967998685056395332640723
          / 13922371260779084768671794660693282
```

The denominator ratio is 55022. Exact subtraction yields the positive
fraction in the README. No floating-point value is used to establish a sign.

## Independent checks and attempted objections

The coordinator used neighbor counts, rational state propagation, and the
explicit marginal formulas. A separate agent used global Gibbs weights and
integer mass redistribution over coordinate fibres, constructing its verifier
before reading the coordinator or published implementations. A subsequent
cross-check compares every final probability, not merely the aggregate TV.

The independent implementation also checks detailed balance, update
idempotence, and every-step normalization. Both routes verify that each
individual update contracts its own chain's TV. The comparison between two
different chains can nevertheless reverse after a common suffix: full-minus-
censored TV is negative immediately after opportunity seven, negative after
eight, and positive after nine. There is no contradiction with Markov-kernel
contraction.

At λ=1 the same comparison gives equality. For q=2, λ=30 it has the expected
nonpositive sign. These are implementation controls for this graph and word,
not independent proofs of general censoring theorems. A vertex need not be
updated during every finite prefix in Holroyd's formulation; the finite words
could also be followed by a common fair schedule without changing the strict
inequality already obtained at opportunity nine.

No mathematical gap was found within the stated scope. This witness does
not prove a failure for every q≥3, random-scan schedules, regular lattices,
particular mixing-time thresholds, or schedules required to update every
vertex before observation. Minimality and practical speed-up are not claimed.
Priority is a separate matter and fails for a new-discovery publication.
