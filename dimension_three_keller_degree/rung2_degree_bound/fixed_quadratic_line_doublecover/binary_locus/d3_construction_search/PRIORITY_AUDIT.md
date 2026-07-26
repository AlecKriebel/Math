# Priority audit for the `D3-BB-21` and `D3-BS-N2-Z` exclusions

**Audit time (UTC):** 2026-07-26T09:07:14Z

**Claim being audited:** within the frozen binary fixed-quadratic
line-double-cover taxonomy, the single normal form
\[
h=pq,\qquad R=p^2q
\]
cannot be the leading data of a quartic Keller counterexample over
\(\mathbb C\).

## Current-listing sweep

The Friday 24 July 2026 new listings in `math.AG`, `math.AC`, `math.CO`,
and `math.NT` were checked for Jacobian, Keller, polynomial-automorphism,
quartic, and degree-bound work.  The current relevant papers found were:

- Z. Jelonek, [*On mappings with Jacobian
  one*](https://arxiv.org/abs/2607.20597), which proves closedness and a
  component dichotomy in the bounded-degree Keller parameter space.  It
  does not classify quartic leading forms or state this family exclusion.
- T. Shaska, [*Graded Keller maps and the Jacobian
  Conjecture*](https://arxiv.org/abs/2607.20210), which studies equivariant
  maps by weight signature.  It does not contain the present
  Hilbert--Burch/contact descent.
- P. Migus, [*Generic degrees of real polynomial Keller maps with
  non-dense image*](https://arxiv.org/abs/2607.21572), which concerns
  generic degree and real-image density, not total-degree-four leading
  strata.

The older closest computational classification located was M. de Bondt,
[*Computations of Keller maps over fields with
\(\tfrac16\)*](https://arxiv.org/abs/1609.09753).  Its quartic
dimension-three theorem treats maps \(x+H\) with \(H\) homogeneous.  The
present family retains arbitrary cubic and quadratic lower parts and an
arbitrary invertible linear part, so the scopes are different.

## Forum and exact-expression sweep

MathOverflow's active Jacobian-conjecture threads, Terence Tao's July
2026 digestion post, the Secret Blogging Seminar, and publicly indexed
X/Twitter material were searched.  Exact searches included

```text
"p^3 q" "p q^3" Jacobian Keller map
"12a^2-8ak+3k^2" Jacobian
"p^2 q r^2" Keller map determinant
"D3-BB-21" Keller
quartic Keller map dimension 3
```

No checked source states the complete \(E_7\) parameterization, the
\(E_6\) conic
\[
12a^2-8ak+3k^2=0,
\]
or the lower-independent obstruction
\[
[p^2qr^2]E_5=\frac25ak(8a-k)
\]
for this normal form.

## Priority verdict and limitations

No exact prior-art collision was located.  This is source-specific
negative evidence, not a guarantee of worldwide priority.  The family
identifier is internal to the frozen taxonomy, and the theorem closes
only one of its 26 fine families.  It closes no one of the fourteen
global quartic rows and leaves the universal dimension-three
total-degree floor at four.

## `D3-BS-N2-Z` delta

At 2026-07-26T09:43:34Z the same current listings and public sources were
compared with the second full-family descent
\[
h=p^2,\qquad R=p^2q.
\]
Exact searches included the internal ID, the leading pair
\((p^4,p^2q^2)\), the ladder
\(c=0,\ b+k=0,\ a^2b=0,\ bu_2+6au_3=0\), and the decisive
\([q^2r]E_3=12d^3\).  No checked source states this exclusion or its
two-chart descent.

The work is AI-assisted and not peer reviewed.  The exact SymPy,
PARI/GP, and dependency-free replays establish facts about the encoded
determinant systems; they do not substitute for specialist mathematical
review.
