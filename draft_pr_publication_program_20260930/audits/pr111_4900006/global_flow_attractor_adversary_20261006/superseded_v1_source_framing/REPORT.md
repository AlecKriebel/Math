# Independent global-flow and exact-attractor adversarial audit of PR111

Immutable candidate: PR111, problem4900006 / AMR-048-0006, head `8a7270989d7064a4b97badecaa4b311db5e6d49f`, literal claimed_solved2/5. Completed 2026-10-06. This is an independent reconstruction of the supplied proof, not a new problem-solving attempt. No mathematical clearance was assumed. The original author verifier and original independent review were not read or used. Source pins and actual exact-control executions are included in this folder.

**Verdict:** No mathematical flaw was found in the counterexample to the literal unrestricted all-smooth-dissipative-system/global-attractor assertion. The exact global attractor, its complete trajectory classification, and the claimed Lyapunov spectra and strict comparisons are correct. This audit supplies no historical priority clearance, novelty clearance, or theorem about chaotic, generic, Lorenz-specific, transitive, or typical attractors.

## 1. Exact claim and falsification criteria

The supplied source statement asks whether, for every smooth dissipative dynamical system with a global attractor, the supremum of local Lyapunov dimension on the attractor is attained at an equilibrium or unstable periodic orbit. The complete prior report uses the same unrestricted quantifier. A valid counterexample must therefore have a globally defined forward flow, a genuine compact minimal global attractor attracting every bounded set, a precisely stated dimension convention, and strict comparison with every equilibrium and every periodic trajectory on that attractor. A locally attracting quasiperiodic torus by itself would fail this requirement. Unchecked aperiodicity, omission of heteroclinic trajectories, numerical exponents, or confusing different Kaplan–Yorke conventions would also fail it.

All these failure modes were attacked independently below. The source's broader historical attribution is not established merely because the literal mathematical statement is false.

## 2. Cartesian reconstruction and two-sided completeness

For one oscillator write z=x+iy, s=x²+y², and omega its real angular speed. The proposed field is

    x' = f(s)x - omega y,
    y' = f(s)y + omega x,
    f(s) = (-s²+5s-4)/(1+s²).

On R5 there are two such blocks with omega1=1, omega2=sqrt(2), plus w'=-100w. The denominator 1+(x²+y²)² is strictly positive everywhere. A reciprocal of a nonvanishing real-analytic function is real analytic locally, so every field component is real analytic throughout R5.

Direct polynomial certificates, valid for every s>=0, are

    f(s)+4 = (3s²+5s)/(1+s²) >= 0,
    3/2-f(s) = [(5/2)(s-1)²+3]/(1+s²) > 0.

For r>0, differentiation of x²+y² gives r'=r f(r²). Consequently |r'|<=4r. For any finite interval in either time direction, r is bounded by its initial radius times exp(4 times the interval length). The exact formula w(t)=w(0)exp(-100t) is finite for every finite positive or negative t. Angles grow linearly and do not create a spatial blowup. The usual local continuation theorem for a smooth field now yields existence for all real times: if a finite endpoint existed, these bounds would keep the entire trajectory in a compact ball, where the smooth field admits continuation. The zero-radius solution is handled in Cartesian coordinates and remains zero. This proves completeness in both directions, not merely bounded forward trajectories on the proposed attractor.

## 3. Strict ambient volume dissipation

The independently differentiated Cartesian Jacobian is

    f(s) I + 2 f'(s) [x;y][x,y] + omega J,
    J = [[0,-1],[1,0]],
    f'(s) = (5+6s-5s²)/(1+s²)².

Hence the single-block divergence is

    h(s)=2f(s)+2s f'(s)
        =2(-s⁴+s²+10s-4)/(1+s²)².

A direct positive-polynomial certificate avoids any numerical maximization:

    11-h(s) = [13s⁴+20(s-1/2)²+14]/(1+s²)² > 0.

The full divergence is h(s1)+h(s2)-100 < -78 at every point of R5. Thus the field is strictly volume contracting everywhere. Independently, its compact global attractor below provides the absorbing/global-attraction meaning of dissipative. The proof is safe under either of those common requirements. The added strongly contracting w-coordinate is a legitimate part of this explicitly five-dimensional system; the statement being falsified puts no bound on ambient dimension.

## 4. Complete radial portrait, including both time directions

The only nonnegative radial stationary values are 0,1,2. The exact signs are

    g(r)=r f(r²)<0 for 0<r<1,
    g(r)>0 for 1<r<2,
    g(r)<0 for r>2.

Uniqueness prevents any nonstationary scalar solution from crossing a stationary radius. The complete classification is:

| Initial radius | Forward limit | Backward limit | Bounded for all real time? |
| --- | --- | --- | --- |
| 0 | 0 | 0 | yes |
| 0<r<1 | 0 | 1 | yes |
| 1 | 1 | 1 | yes |
| 1<r<2 | 2 | 1 | yes |
| 2 | 2 | 2 | yes |
| r>2 | 2 | infinity | no |

For the nonconstant bounded cases the limit is forced by monotonicity: a finite limiting radius at which g does not vanish contradicts convergence. In the r>2 backward case, a finite limiting radius would have to be a stationary value at least r(0)>2, which does not exist. The infinity limit is approached only at infinite backward time by the completeness proof. The w trajectory is bounded for all real time exactly when w=0.

These observations also show that the proposed attractor consists exactly of all initial points on bounded complete trajectories. They exhaust interior, disk-boundary, coordinate-axis, and radial-separatrix cases; no assertion of hyperbolicity or recurrence is needed.

## 5. The exact minimal compact global attractor

Let D2 be the closed radius2 disk in C. Set A=D2×D2×{0}. It is compact, and the complete radial classification gives phi_t(A)=A for every real t. In particular, it is fully invariant, not just positively invariant.

To prove attraction uniformly on bounded sets, let B be any bounded initial set and choose R>=2 bounding both initial radii and W bounding |w|. Scalar uniqueness/order preservation gives r_i(t)<=r(t;R) for every initial point in B and t>=0. The comparison radius r(t;R) either equals2 or decreases to2. Since Euclidean distance to a closed disk is max(r-2,0),

    sup_{p in B} dist(phi_t(p),A)
      <= [2 max(r(t;R)-2,0)² + W² exp(-200t)]^(1/2) -> 0.

This explicitly proves the required uniform attraction, with no exchange of a pointwise limit and a supremum over initial conditions.

For minimality, let K be any closed set attracting every bounded set. In particular K attracts the bounded set A. Full invariance gives phi_t(A)=A, so the nonnegative number sup_{a in A}dist(a,K) must tend to0 while remaining constant. It therefore equals0; closedness of K implies A is contained in K. Thus A is the minimal closed global attracting set. A smaller union of the four periodic circles and origin fails: all complete bounded connecting trajectories must belong to the global attractor. A single outer torus fails even more directly because it does not attract the origin. These were explicit adversarial alternatives, not implicit assumptions.

## 6. Exhaustion of equilibria and periodic trajectories

An equilibrium must have w=0. Any nonzero complex coordinate has angular speed omega!=0, so cannot be stationary. Thus (0,0,0) is the only equilibrium in the entire ambient space.

A periodic trajectory must have w=0 because exp(-100T)!=1 for every positive T. Every radius must be constant: a scalar autonomous radial solution lying strictly between stationary radii is strictly monotone and cannot repeat. Any nonzero constant radius is1 or2. If both complex coordinates are nonzero, periodicity would require T=2pi m and sqrt(2)T=2pi n for positive integers m,n, giving sqrt(2)=n/m. The elementary irrationality of sqrt(2) rules this out. If just the first complex coordinate is nonzero, each radius1 or2 gives one periodic circle with period2pi. If just the second is nonzero, those radii give the other two periodic circles with period2pi/sqrt(2). There are exactly four nontrivial periodic orbits; all lie in A.

At radius1 the transverse radial rate is3, so the two such circles are unstable. At radius2 the radial rate is-24/17, the inactive complex block has two rates-4, and the w rate is-100; the two such circles are orbitally stable. This classification confirms the source's words in the full five-dimensional ambient system, not just in a two-dimensional oscillator restriction.

## 7. Direct singular-value derivation on every stratum

For a nonzero oscillator radius, use orthonormal radial and angular frames at the initial and current points. Subtracting omega J from the Cartesian variational equation cancels the rotation exactly, leaving a diagonal matrix with instantaneous diagonal entries

    g'(r)=f(r²)+2r² f'(r²),  f(r²).

There is no angular/radial shear, because the angular velocity is constant independent of radius. Therefore the derivative block is related by orthogonal left and right factors to

    diag(exp(integral_0^t g'(r(tau)) d tau),
         exp(integral_0^t f(r(tau)²) d tau)).

Both entries are strictly positive and are exactly the block's singular values before sorting. This derivation remains valid for every finite time on a nonzero trajectory; a radius approaching zero never reaches zero in finite time. At radius0 the Cartesian derivative is exp(-4t) times a rotation, giving two singular values exp(-4t).

The needed endpoint values, derived from the rational expression, are

    f(0)=-4, g'(0)=-4, g'(1)=3, g'(2)=-24/17,
    f(1)=f(4)=0.

If the radius tends to a stationary value, the respective integrands converge to these constants. Their time averages converge to the same constants by the elementary Cesaro argument. This proves the singular-value exponents directly, without invoking a one-dimensional linearization theorem, Oseledets regularity, an ergodic measure, or numerical estimation. It yields:

| Type | Exact initial-radius set inside A | Exponent pair |
| --- | --- | --- |
| O | 0<=r<1 | (-4,-4) |
| U | r=1 | (3,0) |
| S | 1<r<=2 | (0,-24/17) |

A nonstationary trajectory tending to the origin really has two negative exponents; an automatic zero flow exponent would be an error here. Its flow vector itself decays exponentially, so no nonzero recurrent flow direction forces a zero exponent.

The full derivative is block diagonal. Its five singular values are the union of the two block singular-value pairs and exp(-100t). Sorting the logarithmic rates preserves convergence (sorting is a continuous operation on a finite real list). The local spectrum at every point of A is therefore the sorted union of the two corresponding exact pairs and -100. This justifies not only individual exponents but all leading exterior-power exponent sums.

## 8. The strict dimension comparison

Under the point-dependent Kaplan–Yorke index, with zero partial sums admitted, exact rational calculation gives:

| Types | Pointwise Kaplan–Yorke dimension | Fixed-global-index4 expression |
| --- | --- | --- |
| OO | 0 | 96/25 |
| OU | 11/4 | 79/20 |
| OS | 1 | 332/85 |
| UU | 203/50 | 203/50 |
| US | 6827/1700 | 6827/1700 |
| SS | 2 | 1688/425 |

Each type pair is realized in A. The largest pointwise value is203/50, and the UU type occurs exactly on T={|z1|=|z2|=1,w=0}. The equilibrium has typeOO. All four periodic circles have typeOU orOS. Both periodic dimensions11/4 and1, and the equilibrium dimension0, are strictly smaller than203/50. Every orbit on T is nonperiodic by the irrational-frequency argument.

For the separate fixed-global-index convention, the exact maxima of the sums of the leading k local exponents for k=1,...,5 are (3,6,6,6,-94). The first strictly negative global sum is therefore the fifth, giving global index4. The smallest local exponent is always-100, so the formula is4+M4/100. The independently computed third column above again has its unique maximum atUU. Its equilibrium and periodic values are strictly smaller. No pointwise-index values are relabeled as fixed-index values.

For the finite-time singular-value convention, T, the equilibrium, and the four periodic circles have exact exponential singular values for every positive t, so their finite-time dimensions are constant in t and equal their pointwise values above. Thus sup_A dim_L(t,p)>=203/50 at every positive t, while every equilibrium and every periodic circle has value at most11/4. Taking infimum over t preserves that strict comparison. The original proof carefully asserts only this lower bound; equality of inf_t sup_A with the pointwise asymptotic supremum is not needed and was not assumed. Interior transient finite-time dimensions have not been silently excluded from the supremum.

## 9. Independent exact controls and limits of this audit

`verify_independently.py` is new standard-library code, using explicit exceptions rather than Python assert. It performs polynomial identity checks for f', growth, and strict divergence; independently differentiates the Cartesian field with exact two-variable automatic differentiation; checks absence of corotating shear and both exact eigendirections; checks limiting rates and radial sign controls; enumerates all six exact spectra/dimension values and global partial-sum maxima; and tests six mechanism/scope alterations. Its final source-bound runs passed4076 checks both normally (actual PID7624) and with Python optimization (actual PID7625). The controls distinguish the crucial irrational-frequency condition, strong w-contraction, zero exponents, radial instability, full disk-product attractor, and equilibrium spectrum. They are finite evidence complementing the analytic proof above, not a substitute for all-real/all-time deductions.

After completing the independent reconstruction, I also read the entire root-repaired `../repaired_diagnostics_v1/COUNTEREXAMPLE.md` (SHA256 `4943f2c38effe24e0aa049242f035091df100c1089612cd2ae4c585abc161ddb`). Its field and mathematical mechanism are unchanged. Its Section6 explicitly adopts the nonnegative-partial-sum finite-time convention already used in this audit, distinguishes that convention's neutral values from the printed strict-positive source index, and refrains from asserting an exact finite-time supremum or infimum. These qualifications correctly preserve the strict mathematical comparison. I accept that repaired mathematical body, subject to the separate primary-source/priority audit; I did not independently retrieve or verify the external primary publications for their wording in this task.

No original candidate file, inherited verifier, original review, global repository file, queue, cache, service record, Git index/ref, or external communication was modified. All audit work stays in this dedicated folder. Mathematical verification is100% complete for the supplied unrestricted candidate; priority and historical-source scope remain a separate pending gate. No mathematical repair is required. A publication must retain the present distinction between the literal unrestricted assertion and narrower historical conjectures, and must not infer historical novelty from this mathematical audit.
