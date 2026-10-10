# Two final bounded checks on finite-p selection

Problem 30002288 / OWR-12336-004. Supplement to the unchanged author freeze,
SHA-256 ba1f6ed2632036cb0e0efa1ce62e1c3824bb8c14e34e036e15c66402ec73d1d2.
Date: 2026-10-06. Independent audit is pending. No publication is performed.

The original freeze records three mathematical approaches. The following two
checks complete the bounded five-approach investigation. Neither closes the
second question. The compound outcome remains PARTIAL_CANDIDATE.

## 4. Leading-order variational asymptotics do not select a profile

Let U be any finite weighted maximum from PROOF.md, normalized by max U=1.
It is globally alpha-Hoelder, compactly supported in the closure of the bounded
open set Omega, and its exact Hoelder seminorm is K=R^(-alpha). Define

    g(x,y)=|U(y)-U(x)|/|y-x|^alpha, for x != y.

The exact quotient used here is

    Q_p(U) = (integral_{R^n x R^n} |U(y)-U(x)|^p
                        / |y-x|^(alpha*p) dx dy)
             / (integral_{R^n} |U(x)|^p dx).

Both integrals use ordinary Lebesgue measure; there is no additional
|x-y|^(-n) factor in the product-space measure. Equivalently the Gagliardo
kernel exponent n+s_p*p equals alpha*p for s_p=alpha-n/p.

Choose p_0>max{1,n/alpha}. We claim g belongs to L^(p_0)(R^n x R^n). On pairs of distance
at most 1, g<=K and any pair with nonzero g has at least one coordinate in the
bounded support of U. The relevant set of pairs consequently has finite
2n-dimensional volume. On pairs of distance greater than 1, the bound
`g<=2/|x-y|^alpha` and the fact that at least one coordinate lies in that support
reduce integrability to the radial integral of `r^(n-1-alpha*p_0)` for r>1.
It is finite. Thus g is in both L^(p_0) and L-infinity. The global bound
on all nearby pairs includes pairs crossing the boundary, so no separate
boundary singularity is omitted. The diagonal itself has product measure zero.

At the alpha=1 endpoint the same calculation is literal: U is globally
Lipschitz, p_0>max{1,n}, the near-pair integrand is bounded by K^p_0, and
the far radial exponent is n-1-p_0<-1. For finite p>max{1,n},
s_p=1-n/p still lies strictly between zero and one. No passage to a local
W^(1,p) energy and no alpha-limit is being taken.

The standard elementary L^p-norm limit, valid for a function in
L^(p_0) intersect L-infinity even on an infinite-measure space, gives
`||g||_p -> ||g||_infinity=K`. One proof bounds the upper limit by
`||g||_p <= ||g||_infinity^(1-p_0/p)||g||_(p_0)^(p_0/p)` and bounds the lower
limit using any positive-measure superlevel set below the essential supremum.
Here essential and pointwise suprema agree: g is continuous off the diagonal,
and the exact extremal pair in PROOF.md has distinct coordinates.
Likewise `||U||_p -> 1`. It follows that

    Q_p(U)^(1/p) = ||g||_p/||U||_p -> R^(-alpha).

These U are admissible for each sufficiently large p with
`s_p=alpha-n/p in (0,1)`. To see the zero-boundary closure condition rather than
assuming it, put `U_epsilon=(U-epsilon)_+`. Its support is compactly contained
in Omega since U is continuous and zero outside Omega. The error
`U-U_epsilon=min(U,epsilon)` tends pointwise to zero; its difference quotient
is bounded by g because truncation is 1-Lipschitz. Dominated convergence proves
convergence in the relevant fractional Sobolev norm. Mollification of each
compactly supported U_epsilon then gives smooth compactly supported
approximants in Omega.

Using the established eigenvalue limit in Lindgren--Lindqvist, Proposition 20,
we therefore have

    Q_p(U)^(1/p)/lambda_p^(1/p) -> 1

for every one of these candidates, including those excluded as actual
subsequential p-limits by the rectangle reflection argument. This is strictly
a root-level statement. It does not establish `Q_p(U)/lambda_p -> 1`, nor does
it show convergence of minimizers to U. It proves that this leading-order
comparison cannot decide between the weighted profiles and the maximal one.
A quantitative subleading estimate would be needed to use this route for the
general selection question; none is established here.

## 5. Concave approximations do not supply the missing diagonal limit

The primary later source already listed and hash-verified in SOURCES.json,
da Silva--Rossi--Salort, arXiv:1704.01875v1,
https://arxiv.org/abs/1704.01875, was additionally checked at printed page 4.
Theorem 1.3 concerns the local infinity-Laplacian and a concave exponent tending
to one. The subsequent explicitly labeled conjecture concerns convergence of
ordinary local p-ground states to that maximal solution. Thus even within that
source's local setting, the former theorem is not asserted to prove the latter
limit. Section 4's suggestion of extensions to fractional kernels does not
remove either the operator difference or the distinct order of limits.

Consequently that result cannot be transferred as a proof of the present
whole-space fractional eigenfunction selection. No interchange of the two
limits is established in this investigation. No claim is made about the
current global literature status of either the local or fractional conjecture.

## Closing scope

The explicit continuum counterexample to unweighted representation stands
unchanged, pending independent audit. No proof or counterexample for general
maximal selection by the finite-p family has been obtained. All five bounded
approaches are now concluded. No sixth mathematical approach is undertaken.
