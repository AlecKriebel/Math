# Proof 37  Explicit neighborhoods of the symmetric zero two five slice

Included dependencies: [Symmetric extreme bounds on zero two five](36_k5_symmetric_slice.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

Let 4<p<6, q=p/2, and A,B,C>=0. Set

    M=(A+C)/2,   S=A+B+C.

When S>0, the full real coefficient box bounded by (A,B,C) on {0,2,5} has the all-positive vertex as a norm maximizer if

    |A-C| <= (q)_5 M^5 B^5 / (6p S^9).                           (1)

Here (q)_5=q(q-1)(q-2)(q-3)(q-4)>0. This is a sufficient condition, not a necessary one. For fixed 4<p<6 and M,B>0, it includes an open neighborhood of A=C, and therefore includes unequal-extreme coefficient bounds within the strict triangle region. The neighborhood is quantitatively narrow; no unrestricted theorem is asserted. S=0 is trivial.

## Proof

Write D(A,B,C) for the positive-minus-middle-negative pth norm-power gap. The quantitative integral bound in the symmetric-slice proof gives

    D(M,B,M) >= [(q)_5 (4MB)^5/(480pi)]
                 * integral_0^1 v^6(B+2Mv)^(p-10)/sqrt(1-v^2) dv.

Since p-10<0 and B+2Mv<=S, while

    integral_0^1 v^6/sqrt(1-v^2) dv=5pi/32,

we obtain

    D(M,B,M) >= (q)_5 M^5B^5 S^(p-10)/3.                         (2)

For positive M,B, put delta=(A-C)/2 and interpolate

    P_(sigma,t)(z)=M+t delta + sigma Bz^2 + (M-t delta)z^5,
    sigma in {+1,-1},  0<=t<=1.

The extreme coefficients remain nonnegative, so |P_(sigma,t)|<=S. Also

    |dP_(sigma,t)/dt|=|delta(1-z^5)|<=2|delta|.

Because p>1, the derivative of |P|^p, including at P=0, obeys

    |d |P_(sigma,t)|^p/dt| <= 2p|delta| S^(p-1).

Integrating in t and z for the two signs gives

    |D(A,B,C)-D(M,B,M)| <= 4p|delta|S^(p-1)
                           =2p|A-C|S^(p-1).                    (3)

Equations (1)--(3) show D(A,B,C)>=0. Zero-coordinate cases satisfying (1) are immediate or follow by continuity. The global-sign and z -> -z symmetries reduce every real sign vertex to the two norms defining D; convexity then proves the entire real coefficient-box assertion.
