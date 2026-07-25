# Provisional literature and priority audit

Date: 25 July 2026 PDT

This is a broad public-source audit, not an exhaustive MathSciNet/Zentralblatt
or expert review.  Every novelty statement below is provisional.

## Current problem status

Epoch AI still lists order 668 as the smallest Hadamard order for which no
matrix is known:

<https://epoch.ai/frontiermath/open-problems/hadamard>

The standard strongly-regular-graph table still marks
`srg(333,166,82,83)` with `?`, rather than a construction or
nonexistence result:

<https://aeb.win.tue.nl/graphs/srg/srgtab301-350.html>

Thus a symmetric conference matrix of order 334 would still be decisive:
its conference graph would settle that open parameter set, and conference
doubling would give `H(668)`.

## What is already standard

The general use of orbit matrices for strongly regular graphs with a
prime-order automorphism is established in:

- M. Behbahani and C. Lam, “Strongly regular graphs with non-trivial
  automorphisms,” *Discrete Mathematics* 311 (2011), 132–144,
  <https://doi.org/10.1016/j.disc.2010.10.005>.

The description of a graph with a semiregular cyclic automorphism by a
matrix of cyclic connection sets is standard `m`-Cayley or
multicirculant theory.  A directly relevant survey is:

- L. Martínez, “Strongly regular m-Cayley circulant graphs and digraphs,”
  *Ars Mathematica Contemporanea* 8 (2015), 195–213,
  <https://www.dlib.si/details/URN:NBN:SI:doc-TCR0ZT1K?language=eng>.

Accordingly, neither the nine-circulant-block setup nor the generic
zero-frequency orbit equations are priority claims.

The identity expressing `z^18` as a scalar multiple of the quadratic
character word in `F_37[C37]` is also classical finite-field/group-algebra
material in substance.  Its use in the present formal completion may be
problem-specific, but the identity alone should not be advertised as new.

## The dangerous Mathon near-match

Mathon’s title, “Symmetric conference matrices of order `p q^2 + 1`,”
looks at first as if it settles this problem because

```text
333 = 37 * 3^2.
```

It does not.  In Mathon’s main theorem the same integer `t` determines

```text
q = 4t - 1,  p = 4t + 1,
```

so `p=q+2`; `p` must also be the order of a pseudo-cyclic graph.  The
pair `(p,q)=(37,3)` is outside that construction.  See Theorem 4.1 and
the setup immediately before it:

- R. Mathon, “Symmetric conference matrices of order \(pq^2+1\),”
  *Canadian Journal of Mathematics* 30 (1978), 321–331,
  <https://doi.org/10.4153/CJM-1978-029-1>.

This false near-match was checked explicitly because missing it would
invalidate the entire priority assessment.

The similarly obvious attempt to combine normalized conference cores of
sizes 9 and 37 by the standard zero-filling tensor correction also fails:
its square retains
`28*(I9 tensor J37-J9 tensor I37)`.  The local verifier checks this
identity.  No source located in this audit supplied a different mixed
order-10/order-38 product that removes the defect.

## July 2026 multiplier paper

The paper submitted on 22 July 2026 proves obstructions for Legendre pairs
of length 333 fixed by a common multiplier subgroup.  It excludes every
common subgroup of order at least nine and several smaller cases, while
explicitly leaving unrestricted existence open:

- A. F. Ramos, D. B. Hulak, and R. J. G. B. de Queiroz,
  “Multiplier obstructions for Legendre pairs of length 333,”
  <https://arxiv.org/abs/2607.20765>.

That paper overlaps and supersedes priority claims in several older local
multiplier lanes.  It does not analyze a conference graph with a
semiregular `C37` action on nine vertex orbits, so it does not subsume this
new route.

## Provisional priority boundary

Targeted searches found no published occurrence of all of the following
specific items:

- the complete 625-class integral nine-orbit quotient census for
  `srg(333,166,82,83)`, including its three parity types;
- the quotient-specific `6/3` diagonal incidence law;
- the rank-16 characteristic-37 first-moment calculation;
- the exact characteristic-two unitary-projection and
  characteristic-three Hermitian-square-zero relaxation censuses;
- the trace-corrected full formal completion for every admissible first
  moment;
- the explicit exact-margin characteristic-two supports for both parity
  types and their exact small-switch gates;
- the constant-generator no-go results through rank three; or
- the `20+20` first-nonconstant normal form and its pure-rank-two and
  common-two-plane exclusions.

This is evidence for possible novelty, not proof of novelty.  The
conference, regular-two-graph, association-scheme, and `m`-Cayley
literatures are large, and some sources are not publicly searchable.

## Publication verdict at this checkpoint

The earlier paper threshold of an exhaustive nine-orbit quotient
classification has now been met: the exact census has 625 permutation
classes, its parity layer has only three types, and the trace, finite-field,
support, and constant-rank-three consequences are mechanically certified
and independently replayed.  Bundled together, this is now a plausible
focused computational-combinatorics note rather than merely a private
checkpoint.

It is still not a Wikipedia-level discovery, because it neither constructs
nor excludes the conference graph or `H(668)`.  A paper claim also remains
conditional on a broader expert literature audit and human review of the
orderly-enumeration proof.  The strongest next thresholds are:

1. an exact conference graph, hence `H(668)`;
2. a general theorem for conference `m`-Cayley graphs that contains the
   trace and finite-field phenomena; or
3. a modulo-four or integral-support obstruction that reduces the two
   unitary parity types to a genuinely feasible exact census.

The construction gate itself is now negative: exact-margin supports exist
modulo two for both parity types, but the best retained next-digit carry is
`672/1503`, and the smallest exact switch families are empty.  The package
has strengthened as a scoped paper while weakening as evidence of imminent
construction.

Retain all novelty language as provisional, but preserve the quotient
classification as a paper project even if the construction lane later
closes.
