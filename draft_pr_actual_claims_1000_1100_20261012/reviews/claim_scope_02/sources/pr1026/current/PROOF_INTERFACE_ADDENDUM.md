# Clarifications and independent coefficient derivation

Target 30001576 / OWR-4427-011. Audit date: 9 October 2026.

This supplements the frozen `PARTIAL_RESULTS.md`; it does not replace or alter
that document. Its conclusions remain partial. No sixth proof route, global
solution, counterexample, or novelty claim is asserted.

## 1. Convergent heat expansion and coefficient classification

Use the original notation, including `a=x12`, `b=x13`, `c=x23`,
`x1j=x2j=x3j=yj`, `S=sum(beta_j*yj^2)`, and
`x_ab=tau_ab/(2*pi*i)`. The independent off-diagonal coordinate differentiates
the theta Fourier exponent by `2*pi*i*(n_a+epsilon_a/2)*(n_b+epsilon_b/2)`.
Applying `partial_za partial_zb` instead multiplies by `(2*pi*i)^2` times the
same product. This proves the off-diagonal heat normalization. For a diagonal
coordinate the Fourier exponent has half that factor, giving the denominator
`4*pi*i`. The coefficient normalization in the frozen packet is therefore
consistent in both cases.

At a fixed diagonal matrix the theta Fourier series and all derivatives
converge normally on a sufficiently small product neighborhood in the period
matrix and the z variables. Taylor expansion in off-diagonal coordinates is
therefore genuinely convergent. Repeated application of the heat equation
identifies it with the stated exponential differential operator. This use of
an exponential is a Taylor identity of holomorphic functions; it needs no
claim that a differential operator acts boundedly on all entire functions.

There is an especially short all-genus check of the surviving terms. After
the first three equations are solved, assign weight two to `a,b,c` and weight
one to each `y_j`. For a remaining output `j`, parity requires odd edge-degree
at vertices `1,2,3,j` and even edge-degree at any other vertex. Through weight
three, the only allowed graphs are:

- One internal edge joining two of `1,2,3`, and the edge joining the third
  vertex to `j`. These give `beta_j*y_j*(a+b+c)`.
- Three distinct edges from `j` to `1,2,3`. Their coefficient is
  `gamma_j*y_j^3`.
- One edge from `j` to one of `1,2,3`, and two edges from another even vertex
  `k` to the remaining two odd vertices. There are three choices, giving
  `3*beta_j*beta_k*y_j*y_k^2` for every `k != j`.

All edges in these graphs are distinct. In the ordered heat-operator
expansion the `3!` orderings cancel its `1/3!`; in the multiset expansion each
edge multiplicity factorial is one. This explains the coefficients without
using finite-genus extrapolation. Terms containing two internal edges have
weight at least five. An omitted term of ordinary degree at least four has
weight at least four, so cannot change the leading residual cubic.

The first three equations start as
`f1=c+alpha1*a*b+S+O(3)`, with the two analogous permutations. Their linear
Jacobian in `a,b,c` is invertible. The holomorphic implicit function theorem
with diagonal parameters gives `a=b=c=-S+O(||y||^3)`. Substitution leaves
`(gamma_j-3*beta_j^2)*y_j^3+O(||y||^4)`.

For a factorial-sensitive additional check, the *full* third jet of `f1` is

    c + alpha1*a*b + S
    + alpha2*alpha3*c^3/6
    + alpha1*alpha2*a^2*c/2 + alpha1*alpha3*b^2*c/2
    + S*(alpha1*(a+b) + (alpha1+alpha2+alpha3)*c/2).

The other first-coordinate formulas follow by permuting `1,2,3`. The
supplementary checker compares these terms as well, including the repeated
edge coefficients `1/6` and `1/2` absent from the original comparisons.

## 2. Uniform zero-set bound and dimension transfer

Fix the genus and a diagonal point where every residual coefficient is
nonzero. Shrink to a diagonal parameter polydisc whose compact closure lies
in that nonvanishing set and in the implicit-function neighborhood. There
is a positive lower bound `eta` on all coefficient moduli. Holomorphic Taylor
remainders on a slightly larger polydisc give one finite constant `K` such
that every residual remainder has modulus at most `K*r^4`, with
`r=max |y_j|`. These constants are local and may depend on the fixed genus;
no uniformity across all genera is required or asserted.

At a simultaneous zero with `r>0`, choosing `j` that attains the maximum
forces `eta*r^3 <= K*r^4`, impossible when `r` is sufficiently small. Thus
all `y_j=0`; the first three solved equations then force `a=b=c=0`.
The intersection with the slice has exactly diagonal support as a germ.

For each irreducible analytic germ `C` through the chosen point, intersecting
with the `r_Y=g(g-3)/2` linear slice equations reduces dimension by at most
`r_Y`. Consequently `dim C-r_Y <= dim(C intersect Y) <= g`. Combining this
with the height bound for the original g equations yields codimension g.
This remains valid even if `C` does not contain the full diagonal. It makes
no scheme-reducedness assertion. For `g>3`, Jacobian rank three is
incompatible with smoothness of this entire codimension-g gradient scheme
at the point; it does not determine whether its reduced support or its
individual branches are smooth.

For nonemptiness of the coefficient condition, `q=exp(pi*i*t)` gives
`theta00=1+2q+O(q^4)`, `theta00''=-8*pi^2*q+O(q^4)`, and
`theta00''''=32*pi^4*q+O(q^4)`. Division yields

    gamma-3*beta^2 = 32*pi^4*q - 256*pi^4*q^2 + O(q^3).

In particular the leading coefficient in the frozen proof is correct, and
independently choosing small nonzero q in every even factor supplies the
required nonempty open diagonal set.

## 3. Explicit boundary and spin dimension interfaces

In the rank-one induction, take a sufficiently fine level cover of the
partial toroidal compactification before using the boundary as a Cartier
divisor. For an irreducible component whose closure meets this boundary,
the local boundary equation is nonzero in the integral local ring of the
closure, because the component meets the interior. Its nonempty zero locus
therefore has pure codimension one. Finite descent then recovers the
coarse-moduli dimension statement. No assertion that an arbitrary boundary
divisor on a coarse quotient is Cartier is needed.

Put `h=g-1`. The dimension theorem for the relative singular locus is
Ciliberto–van der Geer, *The Moduli Space of Abelian Varieties and the
Singularities of the Theta Divisor*, arXiv:math/9911127v2, Theorem (2.4),
printed pp.6–7. It gives codimension `h+1` in the universal h-dimensional
family, so dimension `N_h-1`. Its fiberwise doubling image has no larger
dimension. The other boundary set, a relative theta divisor over `I_h`,
has dimension at most `(N_h-h)+(h-1)=N_h-1` under the inductive hypothesis.
Grushevsky–Salvati Manni, arXiv:0805.4148v1, Proposition 12 and Theorem 13,
provide the two boundary types and explicitly require rank-one boundary
access. This conditional induction is accepted, with that hypothesis.

Primary references:
- https://arxiv.org/abs/math/9911127v2
- https://arxiv.org/abs/0805.4148v1

For the curve-moduli import, Teixidor i Bigas, *Half-canonical series on
algebraic curves*, Theorem (2.17), supplies pure codimension three for the
odd, at-least-three-section locus in its stated genus range. The preprint's
notation is projective dimension `r`, so the relevant case is `r=2`, not
`r=3`. The institutional preprint was inspected at its printed p.24 (PDF
p.26); the published theorem is numbered (2.17), printed p.113. To avoid
any OCR ambiguity at the endpoint, use the theorem for `g>=6` and handle
`g=5` directly: Clifford equality makes this locus the hyperelliptic locus,
of dimension `2g-1=9=3g-6`. For `g<=4`, a theta characteristic of degree
`g-1` cannot have three sections by Clifford's bound. The finite choice of
spin characteristic and the quasi-finite Torelli map preserve dimension.
This justifies the stated ambient codimension and rules out this family's
being an excess-dimensional counterexample on its own.

Primary institutional source:
https://hdl.handle.net/2445/151640

None of these dimension interfaces gives the missing global specialization
or boundary-accessibility theorem.
