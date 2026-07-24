# July 2026 literature audit for the H(668) program

## Status

Ramos, Hulak, and de Queiroz,
[Multiplier obstructions for Legendre pairs of length
333](https://arxiv.org/abs/2607.20765), submitted 22 July 2026, materially
changes attribution for the multiplier lanes but does not close the active
order-three program.

Their theorem concerns pairs fixed by a common subgroup
`H <= (Z/333Z)^*`, without the prescribed length-37 compression used in
several local models here.  It proves:

```text
30 subgroups survive the necessary reduction modulo 3;
21 of those 30 are impossible;
all 19 subgroups of order at least 9 are impossible;
the nine unresolved subgroups have orders 1,2,3,3,3,3,6,6,6.
```

The result uses exact compression, row-sum certificates, value-set
enumeration, direct pseudo-Boolean bounds, and checked DRAT proofs.  It is not
a timeout report and it leaves unrestricted `LP(333)` and `H(668)` open.

A second 2026 source is directly relevant:
Kotsireas, Gallardo-Cava, Gómez, and Gómez-Pérez,
[On the search of binary Legendre pairs of length
`p q^2`](https://doi.org/10.1016/j.jsc.2026.102606).  Its proposed
`q^2`-uncompression starts from

```text
A(p,q) = [1, q chi],
B(p,q) = [1,-q chi],
```

where `chi` is the quadratic character modulo `p`.  At `(p,q)=(37,3)`,
this is exactly the prescribed length-37 compression underlying the local
`LP(333)` program.  The paper verifies its conjectured uncompression only
at smaller parameters; it does not construct `LP(333)`, classify the local
order-three Eisenstein profiles, or close `H(668)`.

## Exact correspondence

| Local lane | Paper ID and subgroup | Public status | Consequence here |
|---|---|---|---|
| column-only `h=18` | ID20, `<10,28>` | impossible | local fixed-compression proof is subsumed |
| quartic `h=9` | ID12, `<10,46>` | impossible analytically | local fixed-compression proof is subsumed |
| sextic `h=6` | ID8, `<10,64>` | impossible | local fixed-compression proof is subsumed |
| column-only `h=3` | ID3, `<10>` | open | five-orbit program remains active |
| `<112>` | ID2 | open | only the prescribed fixed-compression branch is closed locally |
| `<121>` | ID4 | open | coupled 1,296-word boundary remains |
| `<211>` | ID5 | open | coupled 1,296-word boundary remains |

The public full-family conclusions for IDs 20, 12, and 8 are strictly
stronger than `LP333_MULTIPLIER_ROW_SUM.md`.  That local theorem is retained
as a compact independent proof and as the front end of ID3, not as headline
novelty.

The paper does not contain the following deeper ID3 results:

- the 1,756-word fixed-compression row-sum catalog;
- the 22 Eisenstein shards or primitive-nine labelled lift;
- the characteristic-37 and `F_729` decompositions;
- prime-167 exactness and the spectral-unit theorem;
- the exact shell exclusions `n_9=6,5,4,3`;
- the five exact `n_9=2` profile orbits;
- the quadratic second-placement-digit pencil and ramified row-collapse
  theorem.

These remain potentially novel but are restricted results within a
non-necessary fixed-compression branch.

## `q^2`-uncompression overlap

The fixed compression itself must now be attributed to the
`p q^2` paper.  It is not a local discovery.  The additional restriction by
the open order-three common multiplier `<10>` is also not a necessary
condition for an uncompression of that seed.

Within that restricted lane, the checked sources do not contain:

- the explicit dense-shell `h=0` profile with shell `(0,18,6)`;
- its exact all-37-lag Eisenstein certificate and 12-element formal orbit;
- the half-turn splitting `36=21+15`;
- the twelve even quadrics and six odd bilinear equations;
- the complete 35-family nonidentity global fiber-twist exclusion; or
- the ternary `[27,15,4]` antisymmetric code and complete exclusion of its
  three projective minimum directions.

These are plausible new internal results about one open `p=37,q=3`
uncompression branch.  They are not yet a complete uncompression theorem,
an `LP(333)`, or an `H(668)`.

## Search consequence

The five minimal proper fixed common-multiplier supergroups of ID3 are paper
IDs

```text
8, 11, 12, 13, 14.
```

All five are publicly excluded.  Therefore any exact pair in the `<10>`
lane has fixed common-multiplier stabilizer exactly `<10>`.  A structured
search must break every proper supergroup; imposing another common
multiplier cannot produce a solution.  Additional useful structure would
have to be asymmetric between the channels, translation-twisted, or
unrelated to common multiplier invariance.

## Companion-release overlap

The paper's
[proof-artifact repository](https://github.com/Arthur742Ramos/hadamard-668-multiplier-obstructions)
contains two additional relevant notes.

Its
[mod-64 report](https://raw.githubusercontent.com/Arthur742Ramos/hadamard-668-multiplier-obstructions/main/mod64/report.md)
already states the basic exact-lift equivalence between Eliahou's special
form and `BS(84,83)`, proves a raw-distance lower bound of 64, and gives a
solver-backed distance-17 bound for a 128-modular lift.  The basic
Eliahou-to-base-sequence translation is therefore prior.  The local
adjacent-42 distance bound 80 is still a strict improvement; the companion
source does not contain the local special-distance-41 boundary, anti-fold
reduction, rank-21 lift, or certified anti-fold case.

Its
[fixed-field compression note](https://raw.githubusercontent.com/Arthur742Ramos/hadamard-668-multiplier-obstructions/main/compression_theorem/theorem_note.md)
publishes general totally real and quadratic fixed-field obstructions.  It
does not reach the ID3 profile algebra or prime-167 exactness theorem, but
generic novelty claims for fixed-field compression must be avoided.

The April 2026 paper
[Determining the group that sends each Legendre pair to an equivalent
Legendre pair](https://arxiv.org/abs/2604.22423) must also be cited before
claiming priority for formal equivalence groups or lex-leader machinery.

The March 2026
[Ulam Frontier-HAD report](https://www.ulam.ai/research/frontier-had.pdf)
already uses `9 x 37` compression, multiplier-orbit search, SAT/SMT, and
decompression.  Those generic ingredients are prior.  No order-three
Eisenstein profile, half-turn algebra, or profile-specific fiber-twist
census was located there.

## Priority verdict

The five-orbit classification, the new `h=0` profile, and their
second-digit algebra are not superseded by the checked 2026 papers.  Their
honest scope is now sharper:

```text
new-looking exact structure inside the p=37,q=3 q^2-uncompression
and public open subgroup ID3,
not a classification of the complete ID3 family,
not an unrestricted Legendre-pair result,
and not an H(668) construction.
```

The isolated `h=0` profile and its half-turn family are not recommended as
a standalone paper.  Their strongest current role is as sections of a
complete order-three profile-classification paper.  A stronger publication
threshold is a complete `h=0` orbit census, extension of the structured
theorems across every resulting orbit, or a row-margin-compatible lift
through two consecutive higher digits.

No external contact was made during this audit.
