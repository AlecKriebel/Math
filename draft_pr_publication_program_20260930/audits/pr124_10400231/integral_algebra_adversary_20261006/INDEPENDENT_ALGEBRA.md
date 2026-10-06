# Independent integral-algebra argument (pre-comparison)

Established 2026-10-06 19:42:43 UTC, before reading the supplied attempt,
prior imported report, other reviews, or source conventions.

Let `R = Z[t,t^-1]`. If an `n x n` matrix `A` over `R` is an actual
presentation matrix and `D = det(A)`, then for every prime `p`

`ord_(t-1)(D mod p) >= dim_Fp coker(A(1) mod p)`.

Here the order of the zero polynomial is `+infinity`, and the determinant
of the `0 x 0` matrix is `1`. For a nonzero polynomial multiply by any
Laurent unit `t^k` to clear negative powers; the order does not change.

Proof: work over the discrete valuation ring `Fp[t]_(t-1)`, in which
Laurent powers of `t` are units. Lift invertible constant row and column
operations over `Fp` that reduce `A(1) mod p` to a matrix with its last
`r = dim coker(A(1) mod p)` rows zero. Those same constant operations
preserve the determinant up to a nonzero field unit. Every entry in
those `r` rows is divisible by `t-1`, so the determinant is divisible by
`(t-1)^r`. This proof uses a genuine determinant, not a gcd of minors.

If `coker A(1) = Z^b direct-sum T` with `T` finite, then the right side
is `b + dim_Fp(T tensor Fp)`. Thus it implies the weaker torsion-only
inequality. It also forces `D(1)=0` when `b>0`.

An often relevant different relation is `H = Z direct-sum coker A(1)`.
When `coker A(1)` is finite, the bound reads
`ord_(t-1)(D mod p) >= dim_Fp(T tensor Fp)` and `|D(1)| = |T|`.
The added free `Z` is external to this presentation.

This fails for an order defined only as the gcd of maximal minors.
For the rectangular presentation `[p, t-1]`, the module is
`R/(p,t-1)`, its gcd order is `1`, but its specialization is `Z/p`.
The Fitting ideal `(p,t-1)` is nonprincipal; its height-two support is
lost on replacing it by the gcd. This finite module is a pseudonull
obstruction, not a counterexample to the square-matrix result.

For `D_p = t + (p^3-2) + t^-1`,
`D_p(1)=p^3`, while `D_p mod p = t^-1(t-1)^2` for all primes,
including `p=2`. Thus its order is `2`, but the specified elementary
torsion `(Z/p)^3` has dimension `3`. No genuine square presentation
with determinant `D_p` can specialize to that torsion. There is also
no square matrix with determinant `D_p` and cokernel at `1` equal to
`Z direct-sum (Z/p)^3`, because the determinant would have to vanish
at `1`.

This polynomial does have genuine square presentations with different
specialization groups: `[D_p]` gives `Z/p^3`, and

```
[ p             t-1 ]
[ -(t-1)/t      p^2 ]
```

has determinant `D_p` and specializes to
`Z/p direct-sum Z/p^2`. These exhibit the unresolved integral lift
choice left by polynomial evaluation alone.

Multiplication by `+/-t^k` and inversion `t -> t^-1` do not change the
order at `1`. Multiplication or division by a factor `t-1` does change
it, so any reduced determinant must be tracked separately. Removing
integer content divisible by `p` likewise changes the mod-`p` object;
it is not multiplication by a unit of `R`. A scalar polynomial and a
finite group with matching cardinality do not establish a topological
realization or an integral presentation.
