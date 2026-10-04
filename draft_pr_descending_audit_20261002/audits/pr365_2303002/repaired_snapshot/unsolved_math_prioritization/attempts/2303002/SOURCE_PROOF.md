# Complete verification of the credited harmonic-path result

This is an exposition of the known affirmative result recorded in Hayman–Lingham Update3.2 and covered by Carleson(1976), not a novelty claim. The original target is a real-valued, nonconstant harmonic function on all of R^n, n>=3. We verify it without invoking the discontinuous-subharmonic part of Carleson's theorem or fine-potential/Brownian-motion machinery.

We use the ordinary maximum principle, the mean-value property and the Poisson formula for a ball. Every other step needed for the path is given below. A path means a continuous parametrized curve escaping every compact set; no prescribed ray or quantitative growth rate is claimed.

## 1. An elementary spherical-average fact

Let f be a bounded, nonnegative, continuous subharmonic function on R^n. Write M=sup f and let m_f(R) be its average over the sphere of radius R centered at0. Then

    lim_{R→infinity} m_f(R) = M.                     (1)

Indeed, fix x and take R>|x|. The harmonic Poisson extension H_R of the continuous boundary data f on that sphere majorizes f in the ball. Relative to normalized surface measure, its Poisson kernel is

    K_R(x,zeta) = R^(n−2)(R²−|x|²)/|x−zeta|^n.

For s=|x|/R<1, it obeys

    (1−s²)/(1+s)^n <= K_R(x,zeta) <= (1−s²)/(1−s)^n.

Both bounds tend to1 as R→infinity, uniformly over the sphere for the fixed x. Since f is nonnegative,

    f(x) <= H_R(x) <= [(1−s²)/(1−s)^n] m_f(R).

Thus liminf m_f(R)>=f(x). Taking the supremum over fixed x gives liminf>=M, while m_f(R)<=M. This proves(1). No claim that a bounded subharmonic function is constant is used.

## 2. Two disjoint bounded positive subharmonic pieces cannot coexist

Suppose f,g are nonnegative, continuous, bounded subharmonic functions on R^n, both nonzero, and f(x)g(x)=0 everywhere. Put M=sup f>0 and N=sup g>0. Disjoint positivity gives

    f/M + g/N <= 1

pointwise. Taking spherical averages and using(1) gives2<=1 in the limit, a contradiction.

## 3. A superlevel component can be pasted by zero

Let u be continuous subharmonic on R^n, let a be real, and let A be a component of the open set{u>a}. Define

    f_A(x)=u(x)−a for x in A, and0 otherwise.

Then f_A is continuous, nonnegative and subharmonic. Continuity follows because u=a on the finite boundary of A. For completeness, if a boundary point had u>a, a small ball in{u>a} meeting A would put that point in the same open component, a contradiction; continuity also rules out u<a at the boundary.

To check subharmonicity, take any ball and the harmonic extension H of boundary data f_A. Since boundary data are nonnegative, H>=0 in the ball. On each part of A inside the ball, u−a is subharmonic and is <=H on its boundary: this holds on the sphere by construction and on the boundary of A because f_A=0. The bounded-domain maximum principle gives f_A<=H there; outside A it follows from H>=0. This is the harmonic-comparison characterization of subharmonicity. No boundary regularity of A is required: u−a−H is continuous on the closure of each bounded piece, and a positive interior maximum would contradict the maximum principle.

Therefore, at any fixed level a, **at most one** component of{u>a} can have u bounded above. Two such components would produce nonzero bounded functions f_A,f_B with disjoint positivity, contrary to Section2.

## 4. Nested components on which the function remains unbounded

Assume now that u is continuous subharmonic and sup u=+infinity. At any level a, some component of{u>a} has u unbounded above. If there is only one component, it contains all sufficiently high values. If there are at least two, Section3 shows that at most one is bounded above.

More generally, suppose u is unbounded above on a component A of{u>a}, and let b>a. The components of{u>b} that meet A lie entirely inside A. If only one does so, that component contains all values above b from A and is unbounded above. If at least two do so, at least one is unbounded above by the same disjoint-component argument. Thus an unbounded-above child can always be chosen.

Inductively choose

    A_1 superset A_2 superset A_3 superset ...,

where A_j is a component of{u>j} and u is unbounded above on A_j. This selection does not make the invalid inference that a Euclidean-unbounded component must have unbounded function values. The latter property has been proved and maintained explicitly.

## 5. Polygonal concatenation and proper escape

Choose x_j in A_j. An open connected subset of R^n is polygonally connected: the set of points reachable from a fixed point by a finite polygonal path is both relatively open and relatively closed. Since x_j,x_(j+1) both lie in A_j, join them by a finite polygonal arc Q_j contained in A_j. Concatenating Q_j on successive parameter intervals[j,j+1] gives a continuous locally polygonal path gamma.

Every point on Q_j satisfies u>j, so u(gamma(t))→+infinity. It remains to verify genuine escape in space. For a compact set C, continuity gives a finite bound M_C=max_C u. Every Q_j with j>M_C misses C. Only finitely many earlier polygonal arcs remain, and their parameter intervals are bounded. Hence gamma eventually leaves every compact set, equivalently |gamma(t)|→infinity. The path is proper and locally finite. No monotonicity of u within each individual arc is required.

Sections1–5 prove the continuous-subharmonic special case of the credited theorem whenever the function is unbounded above.

## 6. Nonconstant entire harmonic functions are unbounded above

Suppose instead that an entire harmonic u were bounded above by M. Then h=M−u is nonnegative harmonic. Apply the ball Poisson formula to h, with the same kernel bounds as in Section1. The sphere average of h is exactly h(0), so for every fixed x,

    [(1−s²)/(1+s)^n] h(0) <= h(x)
        <= [(1−s²)/(1−s)^n] h(0).

Let R→infinity. This yields h(x)=h(0) for all x, even if h(0)=0. Thus u is constant. A nonconstant entire harmonic function therefore has sup u=+infinity. It is continuous and subharmonic, so Sections1–5 supply the required proper polygonal path. This proves the full original assertion for every n>=3.

## 7. Source scope and remaining exclusions

Hayman–Lingham's own Update3.2 explicitly credits Fuglede with the required asymptotic path and cites Carleson's polygonal strengthening. The proof above verifies only the continuous case needed for the harmonic question; it does not recertify Carleson's more technical treatment of discontinuous subharmonic functions. Its component method follows the classical argument, while the explicit spherical-average lemma avoids reliance on a thinness/Phragmén–Lindelöf criterion.

The bounded subharmonic example in the original question, max(−1,−r^(2−n)), has finite supremum0 and therefore does not satisfy Section4's unboundedness hypothesis. There is no contradiction. No claim is made that a straight ray suffices, that a prescribed growth rate holds, or that the original problem remains open.
