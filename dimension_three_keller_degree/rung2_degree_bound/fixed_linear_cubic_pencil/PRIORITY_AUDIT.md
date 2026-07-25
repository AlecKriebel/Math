# Priority audit: horizontal fixed-linear cubic pencils

**Searched:** 2026-07-25T06:03:00Z.

This is a source-specific overlap check, not a guarantee of worldwide
priority.  No outreach or external communication was performed.

## Claim searched

The candidate new statement is the exclusion of the horizontal part of
the quartic leading-form row
\[
H_4=h(p,q,0),\qquad
(e,a,b,\delta,\nu)=(1,3,1,1,1),
\]
where \(h\) is linear, \((p,q)\) is a minimal primitive cubic pencil, and
\(h\) is not a component of any pencil member.  The mechanism is the
degree-zero first integral
\[
G^4/(hp)^d\in\mathbb C(p/q)
\]
and its incompatible valuation along \(h=0\) for \(d=2,3\).

## Queries and sources checked

Exact and combined searches included:

- `"h(p,q,0)" Jacobian`;
- `"fixed linear" "cubic pencil" Jacobian conjecture quartic`;
- `"R^4" "Q^d" pencil Jacobian`;
- `"primitive pencil" "Jacobian conjecture" ternary cubic`;
- `"degree four" "Keller map" "cubic pencil"`;
- `"quartic Keller" "fixed divisor"`;
- `"relative algebraically closed" "Jacobian conjecture"`;
- the exact tuple `"(1,3,1,1,1)" Keller map`;
- `"fixed-linear cubic-pencil"` and
  `"horizontal fixed linear" Keller`.

The searches covered arXiv and general scholarly indexing.  Separate exact
searches were also run against MathOverflow, Secret Blogging Seminar,
Terry Tao's blog, and public indexed X/Twitter results.

## Closest checked sources

1. Michiel de Bondt,
   [*Rational maps \(H\) for which \(K(tH)\) has transcendence degree
   \(2\) over \(K\)*](https://arxiv.org/abs/1501.06046) (2015).
   Theorem 2.7 supplies the homogeneous minimal-pair factorization and
   relative-algebraic-closure framework used by the project taxonomy.
   It does not state the fixed-linear valuation obstruction, extract the
   \(E_8/E_7\) normal components, or exclude this quartic Keller row.

2. Nguyen Van Chau,
   [*Pencil of irreducible rational curves and Plane Jacobian
   conjecture*](https://arxiv.org/abs/0905.3939) (2009).
   This concerns plane maps whose entire pencil consists of irreducible
   rational curves.  It does not address a ternary quartic leading map,
   a fixed divisor \(h\), or the two normal homogeneous components here.

3. T. Shaska,
   [*Graded Keller maps and the Jacobian
   Conjecture*](https://arxiv.org/abs/2607.20210) (2026).
   This analyzes equivariant Keller maps through a weighted quotient and
   a fibre cubic.  Inspection found no classification by the ordinary
   leading homogeneous form \(h(p,q,0)\), no horizontal/vertical cubic
   pencil split, and no \(E_8/E_7\) divisor theorem of the present form.

Searches for Jacobian-derivation kernels returned literature on
two-variable Jacobian derivations, but not the three-variable
two-Hamiltonian derivation
\(\operatorname{Jac}(hp,hq,-)\) or the fixed-divisor valuation used here.

## Result

No checked source states the theorem in
`WORKING_HORIZONTAL_FIXED_LINEAR_CUBIC_PENCIL.md`, its degree-zero
scaling descent, the valuation equation
\[
4v_h(G)=d,
\]
or the sharp vertical exceptions
\[
(h,p,q,G_2)=(z,zx^2,x^3+y^3,zx),
\qquad
(h,p,q,G_3)=(z,z^3,x^3+y^3,z^3).
\]

This is only negative evidence from the named sources and queries.  The
theorem passed independent hostile audit at 2026-07-25T06:15:00Z but
remains unreviewed.  The vertical locus remains open beyond the two top
determinant identities.
