# Proof 11  Balanced and circular prescribed coefficient boxes

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Circuit obstructions and positive uncentered blocks](01_circuit_obstructions.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Theorem

Let `c,A_j,B_j>=0`, `1<=j<=n`, and suppose that for every pair either `A_j=B_j` or `A_j B_j=0`. For all real `d,a_j,b_j` with `|d|<=c`, `|a_j|<=A_j`, `|b_j|<=B_j`, and for every `p>=2`,

`E |d+sum_j(a_j Z_j+b_j conjugate(Z_j))|^p <= E |c+sum_j(A_j Z_j+B_j conjugate(Z_j))|^p`,

where the `Z_j` are independent uniform unit complex variables.

Thus all-balanced pairs are positive, and arbitrary independent one-sided circle summands may also be present. Unequal actual coefficients are allowed beneath the stated balanced majorants.

## A radial convexity lemma

Let `Phi:C->R` be smooth, radial and bisubharmonic (`Delta^2 Phi>=0`). Write `Phi(z)=psi(|z|^2)`. Then `psi''(s)>=0` for `s>=0`.

For `s>0`, direct radial differentiation gives

`Delta^2 Phi(sqrt(s)) = 16 (s^2 psi''(s))''`.

Smooth radiality at zero implies that `s^2 psi''(s)` and its first derivative vanish at zero. Two integrations therefore give

`psi''(s) = (16 s^2)^(-1) integral_0^s (s-t) Delta^2 Phi(sqrt(t)) dt >=0`.

The same conclusion holds for a continuous radial bisubharmonic function after convolution with nonnegative smooth radial mollifiers and passage to the locally uniform limit. Convexity of `s -> Phi(sqrt(s))` passes to that limit.

In particular, if `Y` is any bounded rotationally invariant complex random variable independent of the other variables and `p>2`, then

`Phi(z)=E |z+Y|^p`

is radial, continuous and bisubharmonic, because as a planar distribution

`Delta^2 |z|^p = p^2(p-2)^2 |z|^(p-4)>=0`,

with locally integrable right-hand side and no atom at zero. This distributional identity and positive-mollification argument are the same credited planar bisubharmonic calculus used in the earlier circuit and block results. Hence `Phi(z)=psi(|z|^2)` with `psi` convex. For `p=2`, `psi(s)=s+E|Y|^2` directly.

## The elementary alignment step

For arbitrary real numbers `h,v`, convexity gives

`[psi((h+v)^2)+psi((h-v)^2)]/2 >= psi(h^2+v^2)`.

Indeed, the average of the two arguments on the left is `h^2+v^2`.

If `H,V` are independent real variables and `V` is symmetric, integration gives

`E Phi(H+V) >= E Phi(H+iV)`.

No convexity or symmetry assumption on the distribution of `H` is needed.

## Proof of the theorem

First restrict every real coefficient to a sign vertex of its prescribed coefficient box. The center sign can be made positive by an overall sign. Each one-sided pair contributes a rotationally invariant independent circle variable regardless of its sign. Their sum is the variable `Y` above.

A balanced pair with common endpoint magnitude `A_j` is, after harmless changes of its independent circle angle, either the real variable `2 A_j cos(theta_j)` if its endpoint signs agree or the imaginary variable `i 2 A_j cos(theta_j)` if the signs disagree.

Let `H` be the constant `c` plus the sum of all real balanced-pair variables, and let `V` be the sum of all imaginary balanced-pair variables before multiplication by `i`. They are independent, and `V` is symmetric. The sign pattern has moment `E Phi(H+iV)`. The all-positive majorant has moment `E Phi(H+V)`. The elementary alignment step proves the comparison.

Finally, for `p>=1` the power moment is convex in the finite vector of real coefficients. Every coefficient vector in the prescribed box is a convex combination of its sign vertices, and the same all-positive majorant bounds every vertex. This proves the stated full box inequality.

## Attribution

The planar circle/disk and bisubharmonic framework is credited to Albert Baernstein II and Robert C. Culverhouse, *Majorization of sequences, sharp vector Khinchin inequalities, and bisubharmonic functions*, Studia Mathematica 152 (2002), 231–248, https://doi.org/10.4064/sm152-3-3, primary PDF https://www.impan.pl/shop/publication/transaction/download/product/90752. The coefficient-restricted alignment application above is supplied explicitly, without a novelty claim.
