# Independent Cartesian, exterior-growth and dimension audit of PR111

**Mathematical verdict:** the supplied product flow is a complete counterexample to the literal unrestricted global-attractor maximizer assertion under its explicitly specified pointwise nonnegative-partial-sum convention and the separately specified fixed-global-index convention. All six unordered (nine ordered) asymptotic type combinations and the maximum 203/50 are correct. This audit does not establish novelty or resolve a chaotic, generic, transitive, Lorenz-specific or original-thesis formulation.

The original candidate is preserved at `../original_head_authentication_20261006/original_attempt/COUNTEREXAMPLE.md`, SHA256 `a9ea8220014aed7c082c995023a3bc7cdd10014544a85376d99267d908323266`. I derived the Cartesian variational matrix, exterior growth and dimensions before reading the inherited independent review. I subsequently compared that review; its main calculations agree with mine. The source-sign concern raised during the present audit is treated below, separately from the correct mathematical argument.

## 1. Cartesian variational equation and its actual singular values

For one oscillator write X=(x,y), s=|X|^2, J=[[0,-1],[1,0]], and V(X)=f(s)X+omega JX. Direct Cartesian differentiation gives

    DV(X)=f(s)I+2f'(s)XX^T+omega J.

For r0>0 choose the initial orthonormal frame Q0=(e_r(theta0),e_theta(theta0)). Its time-dependent counterpart is Q(t)=R(theta0+omega t). Since angular speed is constant and independent of radius, Q'=omega JQ. If a variational vector is Q(t)eta, its equation becomes

    eta'=diag(g'(r(t)), f(r(t)^2))eta,
    g'(r)=f(r^2)+2r^2f'(r^2).

The cancellation of omega J is exact. In particular the Cartesian fundamental matrix is

    B(t)=Q(t) diag(a(t), b(t)) Q0^T,
    a(t)=exp(integral_0^t g'(r(u)) du)>0,
    b(t)=exp(integral_0^t f(r(u)^2) du)=r(t)/r0>0.

Its two singular values are exactly a(t),b(t), sorted. These are Euclidean singular values of the Cartesian derivative, not eigenvalues of an instantaneous nonnormal Jacobian. For a nonstationary radius g(r0)!=0, a(t)=g(r(t))/g(r0), with positive ratio because the scalar solution stays in the same sign interval. At a stationary positive radius the exponential formula remains valid; the ratio formula is not used. At the origin polar coordinates are excluded: DV(0)=-4I+omega J gives B(t)=exp(-4t)R(omega t), with both singular values exp(-4t).

These formulas also identify the possible source of a hidden shear: radial dependence of angular speed would create an off-diagonal entry after rotation. It is absent in the stated vector field. The frame at the input is fixed once the initial point is fixed; the frame at the output is orthogonal for every time. No time-dependent choice of an initial maximizing direction has been smuggled into a Lyapunov limit.

## 2. Every radial case, including heteroclinic and zero cases

The scalar signs are negative on (0,1), positive on (1,2), and negative on (2,infinity), with zeros 0,1,2. Scalar uniqueness prevents crossing. A bounded monotone radial solution has a limit, and a limit strictly within one of those nonzero-sign intervals is impossible. Consequently every radius in (0,1) tends to 0 and every radius in (1,2] tends to 2; a radius at 1 remains 1. These cover the radius-two disk. The extra coordinate always contributes exp(-100t).

The exact quotient-rule computations are

    f'(s)=(5+6s-5s^2)/(1+s^2)^2,
    g'(r)=(-s^4-5s^3+7s^2+15s-4)/(1+s^2)^2, s=r^2,
    f(0)=-4, g'(0)=-4, f(1)=0, g'(1)=3,
    f(4)=0, g'(2)=-24/17.

Because f and g' are continuous, the logarithms of a(t) and b(t), divided by t, converge by the elementary Cesaro-average argument whenever r(t) converges. This gives:

| Initial radius | Radial rate | Angular rate | Sorted type |
|---|---:|---:|---|
| 0 | -4 | -4 | O=(-4,-4) |
| 0<r0<1 | -4 | -4 | O=(-4,-4) |
| 1 | 3 | 0 | U=(3,0) |
| 1<r0<2 | -24/17 | 0 | S=(0,-24/17) |
| 2 | -24/17 | 0 | S=(0,-24/17) |

No ergodic theorem, numerical asymptotic extrapolation or unverified multidimensional linearization is needed. A connecting orbit tending to an equilibrium can have no zero exponent; the usual zero flow-direction exponent requires additional recurrence/nonvanishing conditions. Thus assigning a spurious zero to the nonstationary inner-radius O case would be an error. Local spectra are discontinuous at r=1, which is consistent with arbitrarily long unstable transients nearby and does not obstruct this exhaustive classification.

The full five-dimensional fundamental matrix has the form Q(t)diag(a1,b1,a2,b2,exp(-100t))Q0^T with block-orthogonal Q(t),Q0. The five individual diagonal growth rates exist, so sorting commutes with their finite-dimensional limiting operation: the sorted logarithmic singular-value rates are the sorted union of the two oscillator types and -100. This does not interchange a spatial supremum with a time limit.

## 3. Fixed direction before limsup and all exterior orders

For any k, induced output/input frame changes on the exterior space are orthogonal. In the fixed initial coordinate-wedge basis a fixed initial k-vector has coefficients c_I indexed by k-element subsets I of {1,...,5}. Its squared evolved norm is exactly

    sum_I |c_I|^2 product_(i in I) d_i(t)^2,

where d_i are the five positive diagonal factors above. Each product has limiting logarithmic rate sum_(i in I) lambda_i. The finite sum therefore has norm-growth rate equal to the maximum of these sums over its nonzero coefficients. Maximizing over fixed initial k-vectors gives max_I sum_(i in I)lambda_i, attained by a fixed coordinate blade. This equals the sum of the k largest lambda_i.

Accordingly the initial-direction supremum outside the time limsup in [Parker-Goluskin Definition2.2](https://arxiv.org/html/2510.14870v2) agrees exactly with the singular-value calculation for this particular system. The agreement follows from the displayed explicit solution, rather than an assertion of universal equivalence of competing Lyapunov definitions. It also covers nondecomposable initial exterior vectors and every k=1,...,5.

## 4. Exhaustive dimensions and maximizer

Use j=max{m:sum_(i<=m)lambda_i>=0}, include m=0, and define d=j+sum_(i<=j)lambda_i/(-lambda_(j+1)), or d=5 if j=5. All denominators used below are strictly negative rates. All nine ordered products were independently enumerated; reversing oscillator order does not affect either column:

| Types | Sorted spectrum | Pointwise d | Fixed j=4 expression |
|---|---|---:|---:|
| OO | -4,-4,-4,-4,-100 | 0 | 96/25 |
| OU or UO | 3,0,-4,-4,-100 | 11/4 | 79/20 |
| OS or SO | 0,-24/17,-4,-4,-100 | 1 | 332/85 |
| UU | 3,3,0,0,-100 | 203/50 | 203/50 |
| US or SU | 3,0,0,-24/17,-100 | 6827/1700 | 6827/1700 |
| SS | 0,0,-24/17,-24/17,-100 | 2 | 1688/425 |

The leading partial-sum suprema are (3,6,6,6,-94). Under [Parker-Goluskin Definition2.3](https://arxiv.org/html/2510.14870v2), the first globally negative next partial sum is the fifth, so j=4. Since lambda5=-100 everywhere, its pointwise expression is D4=4+M4/100. These expressions are not the pointwise KY dimensions at low-growth trajectories.

Both columns attain their maximum 203/50 exactly at type UU, i.e. |z1|=|z2|=1 and w=0. The next-largest value is 6827/1700, below it by exactly 3/68. The fixed-index gaps at OO,OU,OS are respectively 11/50,11/100,131/850; the pointwise equilibrium/unstable/stable-periodic values are 0,11/4,1.

The only equilibrium is the origin because nonzero complex coordinates rotate at nonzero angular speed. A periodic scalar radius must be constant, hence 0,1 or2. If both oscillators are active, a positive common period would require both T/(2pi) and sqrt(2)T/(2pi) to be integers, forcing sqrt(2) rational. Thus there are exactly four periodic circles: one active oscillator, radius1 or2, the other at0 and w=0. Radius1 gives a Floquet radial multiplier exp(3T)>1 and is unstable. Radius2 gives exp(-24T/17)<1; all other transverse multiplier moduli are exp(-4T),exp(-4T),exp(-100T)<1, so those circles are orbitally asymptotically stable. The flow-direction multiplier is1. Every UU torus orbit is aperiodic. No equilibrium or periodic orbit can attain either maximum.

The intended compact set really is the global attractor, rather than a deliberately enlarged invariant set: the disk-product is invariant in both time directions, scalar comparison uniformly attracts every bounded set into it, and w decays uniformly. Any closed set attracting that compact invariant disk-product must contain it. The elementary bounds on f preclude finite-time escape in either direction. A direct polynomial certificate gives each oscillator divergence <=11: after denominator clearing, 11(1+s^2)^2-(2f+2sf')(1+s^2)^2=13s^4+20(s-1/2)^2+14>0. The total divergence is therefore <=-78. No dissipativity or global-attraction exception undermines the dimension example.

## 5. Finite-time statement, zero convention, and independent source inspection

At the origin, each listed periodic circle, and every UU torus point, singular values are exact exponentials for every positive time. Their nonnegative-index finite-time KY values are therefore exactly the corresponding entries above. The torus alone gives sup_A d(t,x)>=203/50 for every t>0, and hence inf_(t>0) sup_A d(t,x)>=203/50. Its equilibrium and periodic competitors have constant strictly smaller values. This proves the required obstruction without evaluating the entire time-infimum and without commuting that operation with pointwise limits.

The finite-time table must not be applied to all heteroclinic points. A strict exact control is s=3/4 in both oscillators. There f=-13/25 and g'=2243/625. At t approaching0 from above, the full finite-time rates approach the eigenvalues of the symmetric Cartesian Jacobian: two copies of (2243/625,-13/25) and -100. The first four sum to 3836/625>0. Thus the local finite-time KY limit is 63459/15625=4.061376, exceeding 203/50 by 43/31250. Continuity implies the strict excess also occurs for sufficiently small positive times. This corroborates the candidate's refusal to claim equality for the finite-time spatial supremum at every time; it does not determine the infimum over all times.

I separately recovered the actual [Kuznetsov-Mokaev 2018 PDF](https://arxiv.org/pdf/1807.00235), 1,749,196 bytes, SHA256 `ed0ca54b5839cad99c88295b5b1a77bdeb6b7563bb8d2c7ccd412160bee7c168`. Full page1 and a 300dpi crop of the index definition were visually inspected. **Its equation(5) clearly uses a nonnegative partial sum, with the equality bar present.** Consequently OS=1 and SS=2 are consistent with that printed convention; the origin uses the candidate's explicitly stated dimension0 extension. The source's separate strange-attractor/typical-system scope is not thereby removed. A temporary root repair asserting that this printed inequality was strict would introduce a source error and must not be promoted.

## 6. Independent controls and evidence limits

`independent_checks.py` uses only the standard library and has no assert statements. Normal PID6833 and optimized PID6834 each completed515 explicit guards, including exact polynomial identities, all31 nonempty coordinate-wedge subsets for each of nine ordered types, all dimensions and strict comparisons, exact orthogonal Cartesian Gram/compound controls for every exterior order, and12 mathematical mutants rejected. Its54 independent Cartesian ODE-plus-variational integrations cover origin, stationary circles, both heteroclinic families, near-separatrix radii, both angular speeds and three positive times. Maximum relative matrix discrepancy is 2.7295626345345703e-12. These finite floating controls supplement the analytic proof; they do not establish every-point limits by sampling.

The exact normal/optimized receipts are `CHECKS_NORMAL.json` and `CHECKS_OPTIMIZED.json`. No original file, Git ref/index, remote service, native acceptance source or assessment was mutated. Primary PDF/rendered pixels are private inspection material and are excluded from a distributable verification package. This audit is an independent AI mathematical review, not human peer review or a novelty certificate.
