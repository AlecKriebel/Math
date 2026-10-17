# Sharpness families for the embedded local criteria

Authored exact examples, 2026-10-16. Coordinates are [X0:X1:U:V], with pi_1=[X1:U:V] and pi_2=[X0:U:V]. These examples supplement `EMBEDDED_SMOOTHNESS_CRITERION.md`; all displayed expressions have integer coefficients and are exact.

## A. Arbitrarily high baseline contact can coexist with smoothness

For every integer k>=2, let W_k be parametrized by

    [s:t] |-> [s^(k+1) : s^(k+1)+s^k t : s t^k : t^(k+1)].

There are no common zeros of these sections. On s!=0, put z=t/s; then the map is

    [1 : 1+z : z^k : z^(k+1)].

The coordinate X1/X0=1+z proves injectivity and immersion on this chart. The unique parameter point s=0 maps to [0:0:0:1], which is not reached from s!=0. Near it, U/V=s/t is a local parameter, proving immersion there as well. Therefore W_k is a smooth embedded rational curve. Its degree is k+1 because the parametrization is injective and the displayed base-point-free line bundle is O_P1(k+1).

W_k avoids both camera centers. Its only baseline point is [1:1:0:0], reached at t=0. The transverse coordinates U/X0 and V/X0 vanish to orders k and k+1, so W_k is tangent to the baseline to order k.

The two image curves have equations

    C1: A V^k - U^(k+1) - U^k V = 0,
    C2: A V^k - U^(k+1) = 0.

These equations are irreducible: each is primitive and linear in A over C[U,V], with its coefficient V^k relatively prime to its remaining term. Both curves have degree k+1, and both have a singular branch of multiplicity k at their epipole [1:0:0]. Their normalization epipolar maps have degree 1. At z=0, local representatives are

    image 1: [1+z : z^k : z^(k+1)],
    image 2: [1   : z^k : z^(k+1)].

Thus k1=k2=k, but rho=1+z has nonzero derivative. This is the second, genuinely necessary option in the interior-baseline immersion criterion. The world curve is smooth even though both selected image branches are singular; the off-baseline obstruction does not apply here.

For k=2 this is a linear transform of the twisted cubic. For k=3 it is a smooth rational quartic. Higher k gives the same phenomenon in every degree at least 3.

## B. The same transverse orders can give a cusp

Replace X1 in the preceding parametrization by X0:

    [s:t] |-> [s^(k+1) : s^(k+1) : s t^k : t^(k+1)].

The image is the integral plane curve

    X1=X0,   X0 V^k=U^(k+1).

Both camera images are C2 from family A. Its normalization has epipolar degree 1, but at t=0 its local map is

    [1 : 1 : z^k : z^(k+1)].

Here k1=k2=k and rho=1 is constant. The derivative vanishes and the world branch has multiplicity k. Families A and B have the same pair of epipole multiplicities and the same cover ramification indices; the ratio jet distinguishes their embedded smoothness.

## C. Center multiplicity is exactly the order difference

For integers b>a>=1, consider

    [s:t] |-> [s^(b+1) : s^(a+1)t^(b-a) : s t^b : t^(b+1)].

This is a base-point-free map, generically injective because [U:V]=[s:t] away from t=0. Its image is an integral curve of degree b+1. The two image curves are

    C1: A V^a=U^(a+1),
    C2: A V^b=U^(b+1).

Indeed, the first projected triple has a common homogeneous factor t^(b-a), which is canceled; the second has no common factor. Both epipolar normalization covers have degree 1. Near t=0 the normalized world map is

    [1 : z^(b-a) : z^b : z^(b+1)].

It lands at O1 and has multiplicity b-a there. It is smooth at O1 exactly when b-a=1; in that case its tangent is the baseline. Away from O1 the epipolar parameter gives local immersion, including at s=0 where U/V=s/t is a local parameter. There are no self-identifications. Consequently this entire world curve is smooth if and only if b-a=1.

The projection degree identities are exact:

    degree(W)=b+1=degree(C1)+(b-a)=degree(C2)+0.

Thus the same family realizes every positive center branch multiplicity, and the order-difference smoothness threshold cannot be weakened.

## D. Multiple immersed branches still fail embedded smoothness

The companion exact-fixture report supplies the family

    [s:t] |-> [s^3+lambda t^3 : s^3+t^3 : s^2t : st^2].

For lambda!=1 this is an invertible linear transform of the twisted cubic (the linear transform on s^3,t^3 has determinant 1-lambda). In particular lambda=2 gives a smooth curve with both image curves nodal cubics. Its two epipole branches map to the distinct baseline points [1:1:0:0] and [lambda:1:0:0].

For lambda=1 the first two coordinates agree, and these two normalization points both map to [1:1:0:0]. Each local branch is immersive, but their collision produces a nodal plane cubic. This isolates the separation condition from the derivative condition. The detailed exact certification belongs to the companion fixture report.

## Audit status

The independent review is recorded in ../audit/INDEPENDENT_AUDIT.md. The elementary calculations here are additional transparent witnesses, not a substitute for the principal local criterion proof or the companion global classification.
