# Calibration: the same mountains defeat the true one- and two-cell gaps

Shared PASS4, row 1778 / 30005770, 14 October 2026. This supplements, and does not change, the frozen all-width certificate obstruction.

The independently authored FIXED_WIDTH_CALIBRATION.md in the PASS4 gap lane proves

    g_1=4,     g_2=27/4,

using the accepted exact canonical guard and the credited domino enumeration. It also records the primary upper bound lambda<=27/2. Consequently the actual logarithmic gaps satisfy

    delta_1=log(lambda/g_1)<=log(27/8),
    delta_2=log(lambda/g_2)<=log2.                           (1)

These are upper bounds on the true gaps, unlike the lower certificate V_K in the main obstruction note.

Let H=H(1/2)=e(1,1/2)=(3/2)log3-log2. Take the actual canonical mountain with cell sizes

    2,4,...,2^m,2^(m-1),...,4,2.

Fix B>=1 and m>B, and use the mass M and exact two-boundary entropy E of a window. Common normalization cancels from E/M.

## One cell

For a central singleton, both neighbors have half its mass, so E/M=2H. A noncentral singleton has its inward neighbor of twice its mass, which alone contributes E/M>=e(1,2)=2H, including at a staircase endpoint. Thus every singleton satisfies

    E/M>=2H=log(27/4)>=delta_1+log2.                        (2)

There is therefore a positive margin against the true one-cell loss everywhere, not only against the frontier certificate.

## Two cells

For a two-cell window containing the center, the two masses are a and a/2, and the outside neighbors have masses a/2 and a/4. They are all present because m>B>=2. Hence

    E/M=[aH+(a/2)H]/(a+a/2)=H.                             (3)

For a two-cell window on one side, let its inward endpoint have mass a. The other endpoint has mass a/2, its outside inward neighbor has mass2a, and M=3a/2. Even when its outer endpoint is at the end of the staircase,

    E/M>=e(a,2a)/(3a/2)=(4/3)H>H.                          (4)

Together, every two-cell window satisfies

    E/M>=H>log2>=delta_2,
    H-log2=(1/2)log(27/16)>0.                              (5)

For B=1, no width-two statement is needed.

## Combined obstruction and its boundary

The main note proves E/M>V_K for all windows of width K<=B. Equations(2)-(5) show that this remains true if the available loss is strengthened to the actual optimal delta_K for K=1,2, while retaining V_K for K>=3. Thus the exact small-width calibrations do not rescue the bounded adaptive-window route based on the currently supplied rates.

No comparison E/M>delta_K is proved for every K>=3. In particular, the main note's distinction between the certificate and the true gap remains essential, and the divergence criterion in ADAPTIVE_WINDOW_ENTROPY.md remains unresolved. There is still no uniform-probability counterexample.

## Input pin

PASS4 gap lane, FIXED_WIDTH_CALIBRATION.md: SHA-256 f831a975f8757858a6ad2a875d135011068047f49154ec426c66e262e5e3705c. Primary source for the domino growth and lambda upper bound: Bevan, Brignall, Elvey Price and Pantone, Theorems2 and8, https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf . The supplementary inequalities above are proved directly and require no new source retrieval.
