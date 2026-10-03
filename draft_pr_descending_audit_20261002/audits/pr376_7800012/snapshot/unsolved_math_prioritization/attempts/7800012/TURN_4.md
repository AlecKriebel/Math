# Turn 4: an exact all-direction local minimum on the8 by8 torus

This turn proves, by a finite exact algebraic certificate, that the holonomy-optimized uniform-pi/2 configuration is a strict local minimum modulo gauge against **all** edge-phase perturbations on the8 by8 torus. The Hessian has63 gauge zero directions and65 strictly positive physical directions. This local result does not prove a global minimum, and it does not extrapolate to arbitrary lattice size.

## 1. The base matrix and its isolated occupied band

Use L=8, N=64, q=16. In a seam gauge let horizontal hopping be1 except−1 across the horizontal wrapping seam; let vertical hopping be i^x except for an additional−1 across the vertical wrapping seam. Every plaquette has flux pi/2 and both loop holonomies are−1, as required by Turn3.

Write r=sqrt3, a=1+r and b=r−1. The four eigenvalues are−a,−b,b,a, each with multiplicity16, and

    T⁴−8T²+4I=0.                                        (1.1)

The gap from the occupied−a band to the next band is2. The q-eigenvalue sum is therefore analytic in a neighborhood of the base phases: a sufficiently small operator-norm perturbation preserves the isolated occupied cluster, and its Riesz projection and trace are analytic. This is a statement about the entire band, so the multiplicity inside that band causes no differentiability problem.

Let P_0,P_1,P_2,P_3 be the four spectral projections in that order. As polynomials in T, their coefficients, from constant through cubic, are the following numerators divided by48:

    P_0: (12−8r, 18−10r, 2r, r−3)
    P_1: (12+8r, −18−10r, −2r, 3+r)
    P_2: (12+8r, 18+10r, −2r, −3−r)
    P_3: (12−8r, −18+10r, 2r, 3−r).                    (1.2)

The checker verifies(1.1) entrywise over Gaussian integers and verifies the eigenvalue, orthogonality and sum identities of(1.2) modulo that polynomial. It also checks the four projection traces16. Thus these are exact spectral projections, not approximate numerical eigenspaces.

## 2. First and second variations

There are128 oriented positive-direction edges, one horizontal and one vertical at each vertex. Write T(theta+h)_xy=T(theta)_xy exp(ih_e) on the chosen orientation and use the conjugate on the reverse edge. Let K_e be the Hermitian derivative matrix with entries

    (K_e)_xy=i T_xy,  (K_e)_yx=conjugate(i T_xy).

For every nearest-neighbor edge, the projection polynomial gives

    (P_0)_xy=−a T_xy/16.                                 (2.1)

It is also checked entrywise. Thus every first derivative Tr(P_0 K_e) vanishes. The direct second derivative contribution is(a/8) sum_e h_e².

Differentiating the isolated spectral projection, or solving its off-diagonal eigenbasis equations, gives the full real Hessian

    H_ef=(a/8) delta_ef
         −2 sum_(j=1)^3 Re Tr(P_0 K_e P_j K_f)/(lambda_j+a), (2.2)

where lambda_1=−b, lambda_2=b, lambda_3=a. To derive the denominator and sign, in an eigenbasis the derivative of the occupied projection between an occupied state u and an unoccupied state v is <v,T'u>/(−a−lambda_v). In Tr(P'T') the two conjugate off-diagonal terms give the factor2. The second derivative of T itself supplies the first term in(2.2).

All entries of13824H lie in Z[sqrt3]. In terms of the numerator matrices48P_j, the subtraction weights are6,2sqrt3,3(sqrt3−1), while the diagonal is1728(1+sqrt3). This normalization is used by hessian_certificate.py.

## 3. Exact translation and gauge reductions

The checker constructs the whole128 by128 matrix from(2.2), using exact integer arithmetic in Q(i,sqrt3), and verifies:

1. H is real symmetric.
2. In the positive-edge coordinates it is translation-invariant on the8 by8 torus, including across the gauge seams. Each2 by2 block depends only on vertex displacement.
3. HG=0, where (Gg)_e=g_head−g_tail is the vertex-gauge differential. These are precisely the expected63 independent gauge directions on a connected64-vertex graph.

A Fourier transform on the vertex torus decomposes H into64 Hermitian2 by2 blocks, indexed by(k_x,k_y) in{0,...,7}². At a nonzero frequency the Fourier gauge vector is

    (exp(2pi i k_x/8)−1, exp(2pi i k_y/8)−1),

which is nonzero and lies in the block kernel. Thus a positive trace makes that block rank1 and positive semidefinite. At frequency(0,0), direct summation gives the block

    [(7sqrt3−9)/144] I_2.                                (3.1)

Both entries are strictly positive.

## 4. A finite certificate for every nonzero frequency

The block traces are evaluated exactly in Q(sqrt2,sqrt3). TURN_4_CERTIFICATE.json lists all64 values as

    (A+B sqrt2+C sqrt3+D sqrt6)/27648,

with integer coefficients. Imaginary parts are verified to vanish. The file also records strict rational lower bounds for every trace. The bounds use the following adjacent rational endpoints, whose squares are checked against2,3,6 using integers:

    1.414213562373095 < sqrt2 < 1.414213562373096,
    1.732050807568877 < sqrt3 < 1.732050807568878,
    2.449489742783178 < sqrt6 < 2.449489742783179.

These decimals denote exact terminating rationals. A positive coefficient uses the lower endpoint and a negative coefficient the upper endpoint when bounding a trace below. No floating-point arithmetic enters the certificate.

In fact every trace is at least(7sqrt3−9)/72, twice the eigenvalue in(3.1); equality occurs at some modes. The checker verifies this difference exactly when zero and with the same strict rational interval test otherwise. Therefore the entire Hessian, on the Euclidean orthogonal complement of the gauge directions, has the explicit positive lower bound

    H >= kappa I,  kappa=(7sqrt3−9)/144>0.                (4.1)

The Fourier argument is a proof that this finite certificate implies positivity in every continuous phase direction. Merely checking a list of sample perturbations would not suffice.

## 5. Local minimality and its precise limit

Gauge transformations preserve the energy exactly. Fix a local linear slice transverse to their63-dimensional tangent space. Analyticity, vanishing first variation and the positive transverse Hessian give a strict local minimum on this slice by Taylor's theorem. Every sufficiently small perturbation is gauge-equivalent to a point on the slice, so the base configuration is a strict local minimum modulo gauge. Equivalently, the only zero quadratic directions are infinitesimal gauge transformations, while all physical directions have positive second variation.

This does not exclude a distant nonuniform configuration with lower energy, a different local basin, or an instability at a different lattice size. It is not a proof of the global8 by8 minimum or of the source's large-lattice conjecture.

## 6. Replay and proof boundary

Run `python verify_turn4.py` from this directory. It regenerates the full exact Hessian, all projection and symmetry checks, the gauge kernel and64 Fourier certificates, and compares the complete certificate with TURN_4_CERTIFICATE.json. Only Python's standard library is needed. The matrix file is not a rounded numerical artifact: its defining algorithm and every scalar positivity bound are exact and portable.
