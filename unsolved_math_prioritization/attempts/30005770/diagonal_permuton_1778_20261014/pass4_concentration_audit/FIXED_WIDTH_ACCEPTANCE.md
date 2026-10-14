# Independent acceptance of fixed-width growth calibration and small-window comparison

Shared PASS4, 14 October 2026.

## Verdict and pins

**Accepted:**

- `pass4_window_gaps/FIXED_WIDTH_CALIBRATION.md`, 7149 bytes, SHA-256 `f831a975f8757858a6ad2a875d135011068047f49154ec426c66e262e5e3705c`.
- `pass4_adaptive_profiles/SMALL_WINDOW_TRUE_GAPS.md`, 3190 bytes, SHA-256 `997f5b9f8f5bc95a6459e7fb8a8154e648572e45dc8588d06e5a63398a791b13`.

The fixed-width guard comparison, exact g_1 and g_2, fixed-k rescaling of the credited domino construction, and the true-gap singleton/two-cell comparisons are valid. These results do not settle the true gap sequence at all widths.

## 1. Guarding labeled unrestricted paths

The unrestricted count h_(n,K) is correctly a count of labeled state paths and edge words, with empty states allowed. It is not identified with a count of ungridded permutations. A canonical path with at most K cells injects into this space by terminal zero-padding.

Applying the same state transformation P(A)=12 skew-sum A at every position and the symmetric guard to every edge gives compatible normalized state patterns. The two incident edge words act on different coordinate orders; the accepted exact kernel reconstruction supplies a unique canonical permutation. Its total added size is2K, not four times the number of edges, because the same two guard points in a state participate in its incident edge records.

The output's canonical states and normalized edge words recover the original states and edges by the specified deletions, including empty states. Thus h_(n,K)<=b_(n+2K,K) is genuinely injective. For each fixed K the constant shift leaves the exponential limsup unchanged. No growing-K conclusion follows.

## 2. Small-width growth

One canonical cell is exactly Av(213), so g_1=4. For two unrestricted cells, summing over their split and internal patterns gives exactly the credited domino enumeration, including empty cells. The exact formula has exponential growth27/4. The guard sandwich therefore gives g_2=27/4 without a finite-data extrapolation.

The separate asymmetric three-point guard also gives the stated sharper size shift for two cells. Its smaller constant is not needed for the growth equality.

## 3. Fixed-width source adaptation and arithmetic

I directly inspected the retained primary source's Theorem9 proof on PDF pages13–14, including its exact product count. The displayed construction has k dominoes and k connectors in3k cells. The local component/interleaving restrictions are independent of setting the size scale equal to k. Keeping k fixed while replacing that scale by m preserves the count

    B_(14m)^k C_(8m,7m)^k binom(21m,14m)^(2k-1).

The records are gridded paths. Guarding them, rather than identifying their ungridded originals, avoids an unproved multiplicity division and adds only6k points at fixed k.

The source's balanced-domino growth gives the contribution28k log(27/4) per m. Its component formula gives9log9-8log8 for each connector, while the interleaving contribution is7log(27/4) per edge. The total numerator is exactly

    36k log(81/8)-7log(27/4).

Dividing by36k and letting m tend to infinity proves the displayed lower bound on g_(3k). A subsequence lower bound suffices because g is defined as a limsup. The fixed guard overhead vanishes in that limit.

Monotonicity in K and the credited lambda<=27/2 give the stated upper bound on the true logarithmic gap with constant term log(4/3). That constant does not tend to zero. It cannot be used to conclude summability, nonsummability, or adaptive-window success or failure at every width.

Primary source: Bevan, Brignall, Elvey Price and Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, Theorem2, Proposition7, Theorem8 and the Theorem9 proof. Retained PDF:627368 bytes, SHA-256 `1264749e17f01005277e8acf1a7782e6c4e448fe1733ac6fbb29ec8bd125f26d`; https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf . The exact enumeration and balanced growth statements were also checked directly in the extracted source text. These are credited inputs, not new enumeration claims.

## 4. Actual optimal one- and two-cell gaps still lose on the mountains

Let H=e(1,1/2). The source calibration gives delta_1<=log(27/8) and delta_2<=log2. In the canonical ratio-half mountain, a central singleton has boundary entropy ratio2H. Every other singleton has an inward neighbor of twice its mass, which alone gives at least2H. Since2H=log(27/4), the singleton score is negative even for the true delta_1, with a margin at least log2.

A center-containing two-cell window has masses a,a/2 and outer neighbors a/2,a/4. Its ratio is exactly H. A one-sided two-cell window has an inward neighbor2a and mass3a/2, giving ratio at least4H/3>H even when the outer neighbor is absent. Since H>log2, all such windows also have negative score with the true delta_2.

These statements hold in the finite canonical mountains once their parameter exceeds the fixed window cap. They upgrade only widths one and two; no comparison with the true delta_K for every K>=3 is established. The deterministic examples still have no asserted positive uniform probability.
