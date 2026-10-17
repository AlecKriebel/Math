# Quadratic width gaps in an exactly solvable staircase model

Shared final PASS5, row1778 /30005770. This comparison model shows why a harmonic finite-width gap cannot be inferred from staircase geometry, positivity of shuffle counts, or fixed-width growth equivalence alone. It does not determine the gap of the actual1324 kernel.

## 1. A genuine monotone staircase model

Consider the same descending staircase support, but require every cell to be decreasing. Let M_K be the permutation class griddable in its first K cells, and let m_(n,K) count labeled griddings with n points, including empty cells. Once the cell sizes n_1,...,n_K are fixed, every cell pattern is unique and each neighboring pair has an arbitrary binary interleaving. Different row and column interleavings reconstruct one gridded permutation. Hence

    m_(n,K)=sum_(n_1+...+n_K=n; n_j>=0)
                 product_(j=1)^(K-1) binom(n_j+n_(j+1),n_j). (1)

Every such permutation avoids123: an increasing pair cannot lie within one decreasing cell, and nonadjacent cells are in skew order. An increasing triple cannot be supported on three cells, since its first and third occupied cells would be nonadjacent. Conversely, every123-avoider has such a finite staircase gridding. One can obtain this by reflecting the established increasing staircase gridding of321-avoiders; an additional anti-diagonal reflection changes which of the first two directions is used, if required.

Thus the union of the M_K is Av(123), whose growth rate is4. The primary reference for existence of the monotone staircase gridding is Albert, Brignall, Ruskuc and Vatter, *Rationality For Subclasses of321-Avoiding Permutations*, Section2, especially the construction on PDF page4:
https://www.rbrignall.org.uk/papers/av321.pdf

A fixed n-point permutation has at most(n+1)^(K-1) choices for its K-1 horizontal and vertical dividing lines. Therefore the gridded and ungridded fixed-K growth rates coincide. We will compute that common rate directly from(1).

## 2. Exact fixed-width growth by entropy maximization

For nonnegative x,y write

    E(x,y)=(x+y)log(x+y)-x log x-y log y.

On the K-simplex let

    F_K(x)=sum_(j=1)^(K-1) E(x_j,x_(j+1)).                  (2)

The standard binomial entropy bound and the at most(n+1)^K size vectors show that the upper growth rate in(1) is at most exp(max F_K). For a fixed positive maximizing vector, rounded integer sizes and Stirling's formula give the matching lower bound; all rounding and factorial errors are O_K(log n). Thus

    lim_n m_(n,K)^(1/n)=exp(max F_K).                       (3)

Here is an exact maximizer. Set

    theta=pi/(K+2),    rho_K=2 cos(theta),
    u_j=sin(j theta) for0<=j<=K+2,
    Z=sum_(j=1)^K u_j u_(j+1),
    x_j=u_j u_(j+1)/Z,   x_0=x_(K+1)=0.                    (4)

All x_j for1<=j<=K are positive. The sine recurrence gives

    x_(j-1)+x_j=rho_K*u_j^2/Z,
    x_j+x_(j+1)=rho_K*u_(j+1)^2/Z.

Consequently every partial derivative of F_K at(4) is

    log[(x_(j-1)+x_j)(x_j+x_(j+1))/x_j^2]
       =log(rho_K^2).                                     (5)

At the two endpoints, the displayed derivative formula includes a zero contribution from E(0,x_1) or E(x_K,0), so it remains correct. It also covers K=1, when F_1=0 and rho_1=1.

Each E is concave, so F_K is concave on the simplex. Its constant gradient at(4) proves global maximality. Homogeneity gives Euler's identity F_K(x)=sum_j x_j partial_j F_K(x), hence the maximum is log(rho_K^2). Therefore the exact fixed-width growth is

    h_K=gr(M_K)=4 cos^2(pi/(K+2)).                          (6)

This is a special case of Bevan's general spectral-radius theorem for monotone grid classes. The elementary calculation above fixes the width convention and proves the needed case without appealing to an uninspected specialization. Primary reference: David Bevan, *Growth rates of permutation grid classes, tours on graphs, and the spectral radius*:
https://oro.open.ac.uk/38963/1/GrowthRatesRevision3.pdf

## 3. Its true gap is summable

Relative to the full union growth4, the actual gap in this model is

    d_K=log(4/h_K)=-2log cos(pi/(K+2)).                     (7)

It is strictly positive for every fixed K and decreases to zero. Taylor's formula at zero gives

    d_K=pi^2/(K+2)^2+O(K^(-4)),
    sum_(K>=1) d_K<infinity.                               (8)

In particular no positive c can satisfy d_K>=c/K for all large K, and the nonsummability hypothesis of the adaptive-window criterion fails for this perfectly concrete staircase model.

No probabilistic failure is claimed. A sufficient criterion can fail even when a desired weak limit holds. The present point is narrower: fixed-width positivity plus a path-shaped gridding and exact binary boundary entropy do not force a harmonic gap. A proof of such a gap for1324 would have to exploit its particular Catalan states and1324 interaction restrictions in a genuinely additional way.

## 4. Consequence for the present attempt

For actual1324 we have certified positive gaps, exact one- and two-ended local penalty recurrences, the fixed-width D/K equivalence, and small-width calibrations. None supplies a collective all-width lower bound whose sum diverges. The folded-path construction explored in the companion note loses a fixed positive entropy per point, despite low turnaround mass, so it does not give the hoped-for recoverable width comparison either.

The model above is not a substitute for an estimate on the actual g_K. In particular it does not prove those actual gaps summable, and must not be used to reject the conditional adaptive-window theorem. It supplies a rigorous obstruction to deriving the missing rate from generic staircase geometry alone.

## Source inspection

The author manuscript of Albert, Brignall, Ruskuc and Vatter was directly inspected at Section2, PDF pages4-6, for the gridding construction. Its introduction records the Catalan enumeration of Av(321), equivalently Av(123). Bevan's primary manuscript was inspected for the general spectral-radius statement. The exact count, variational calculation and resulting asymptotic used here are fully supplied above. No finite coefficient extrapolation is used, and no new primary source is claimed to settle1324.
