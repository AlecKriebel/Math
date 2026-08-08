# Uniform-bundle bounded-gadget tangent formula

Let `H` be a fixed connected undirected weighted gadget on `s` vertices,
with dimensionless internal weighted degrees `d_i`.  Give its internal edges
physical weight `C/a` times their gadget weight, and join vertex `i` weakly
to every large-core vertex with common portal load `x_i>0`.  The overall
scale of the `x_i` cancels.

Write `h_U^+(i)` and `h_U^-(i)` for isolated-gadget fixation from singleton
`i` at fitness `r` and `1/r`, respectively, and put

\[
 \bar h_U^+={1\over s}\sum_i h_U^+(i),\quad
 S_0=\sum_i{x_i\over d_i},\quad
 S_B^-=\sum_i x_i h_B^-(i),\quad
 S_D^-=\sum_i{x_i h_D^-(i)\over d_i}.                  \tag{1}
\]

Direct summation of cross birth--target and death--parent events gives the
successful gate odds

\[
 Z_B={a(r-1)S_0\over S_B^-},\qquad
 Z_D={r(r-1)\sum_i x_i\over aS_D^-}.                   \tag{2}
\]

The normalized dilute satellite corrections are therefore

\[
 F_U=s\left\{{\bar h_U^+Z_U\over p(1+Z_U)}-1\right\},
 \qquad p=1-1/r.                                       \tag{3}
\]

With `lambda` hub pendants per satellite, the two tangent coefficients are

\[
 F_B+{\lambda\over r-1},\qquad F_D-\lambda.             \tag{4}
\]

Thus existence of `lambda>=0` is equivalent to

\[
 F_D>\max\{0,-(r-1)F_B\}.                              \tag{5}
\]

In particular, the separator

\[
                         F_D+(r-1)F_B                   \tag{6}
\]

must be positive.  Formula (2) specializes to the clique formulas in the
companion theorem.

## Exact finite catalogue

For uniform portal loads and all 142 connected unweighted unlabeled gadgets
on two through six vertices, `certify_unweighted_gadgets.py` solves the four
local subset chains exactly over `QQ`.  At `r=3/2`, after the positive scale
denominator in (6) is cleared, its numerator is a concave quadratic in `a`.
Exact coefficient and discriminant tests show:

> `K_2` is the unique gadget in this finite catalogue for which (6) can be
> positive at any common scale.

The certificate digest is printed by the verifier.  This is a precise
finite class theorem.  It neither proves a universal bounded-gadget theorem
nor excludes weighted or nonuniform-portal gadgets.

