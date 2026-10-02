# Turn 5: self-certifying finite-window Palm sampling

Substantive author turn **5/5**. This final turn supplies an adaptive local algorithm which returns the exact infinite-process Palm face and clique scores, almost surely after inspecting finitely many Poisson points. The number of inspected points has every fixed finite moment. It also gives elementary confidence intervals for the simplex-typical fraction from independent runs. This is a mathematical ideal-real-arithmetic algorithm; a production simulator, numerical fraction, bit-complexity estimate, and dimension trend are not claimed.

## 1. A completely specified finite direction family

Fix d>=1 and set m=4d. Use every nonzero integer vector q in {−m,...,m}^d as a cone axis, normalized to q/|q|. Repeated directions may be retained. There are

                    H=(8d+1)^d−1

vectors. Give every cone half-angle π/6. These cones cover the sphere. Indeed, for a unit vector u, round each coordinate of mu to its nearest integer to obtain q. Then |q/m−u|<=sqrt(d)/(2m)<=1/8, q is nonzero, and

 |q/|q|−u| <= 2|q/m−u| <=1/4.

This chord bound is smaller than that for angle π/6. The cones again have volume at least v r^d inside a radius-r ball, with v=κ_d/8^d, because each contains B(rq/(2|q|),r/8). This explicitly constructible cover replaces the smaller existential net of turn 3. Its larger size worsens constants but changes no conclusion.

Membership of a nonzero displacement z in the cone of q can be tested without evaluating a trigonometric function:

 z·q>0,        4(z·q)^2 >= 3|q|²|z|².                              (31)

Together with |z|²<=r² this is a finite algebraic shield test. Almost surely none of the random tests encounters an unprescribed geometric degeneracy; boundary equalities may in any case be included.

## 2. Adaptive algorithm and exactness

Generate a unit-rate Poisson process successively in the nested balls B(0,2^j), j=0,1,..., by generating independent Poisson processes in the newly exposed annuli. Add a point at 0 once, without counting it as a Poisson point. At level j, put L=2^j and perform these finite tests:

1. For the origin and for every currently observed point x in B(0,L/4), test whether every cone in the family contains another observed point at distance at most L/8 from x.
2. If any test fails, expose the next annulus.
3. If all tests succeed, construct the finite Delaunay complex and its graph for the observed points plus 0. Return the two scores S_D and S_F: the number of Delaunay k-faces containing 0 and the number of flag k-simplices containing 0. Stop.

All queried shield neighborhoods lie in B(0,3L/8), so the success event is determined entirely by the observed data. It is exactly the simultaneous-shield event used in turn 3 for this direction family. That proof shows that all finite and infinite Voronoi cells needed by the origin's faces and cliques coincide. Pairwise intersections therefore give the same clique score, and the common intersection of the cells of every candidate vertex set gives the same Delaunay-face score. The output is thus

             (S_D,S_F)=(C^D_k(0),C^F_k(0))                         (32)

for the single infinite Poisson process coupled by the annular construction. Selecting the first successful level does not bias these scores: every successful level returns exactly the same infinite-process quantities. Success is **not assumed monotone** as L increases, and no optional-stopping identity is being invoked.

## 3. Termination and point-cost moments

Let J be the first successful level, and define

 q_L=min{1,H[1+κ_d(L/4)^d]exp(−v(L/8)^d)}.

The same Mecke union bound as before gives

                 P(J>j) <= q_{2^j}.                              (33)

This is true without independence between levels, since J>j implies failure at level j. The right-hand side tends to zero, so J is finite almost surely. In fact its tail decays exponentially in 2^{jd}, up to a polynomial prefactor.

Let N_* be the total number of Poisson points exposed before stopping. In the nested construction this is N(B(0,2^J)); no point is counted twice. For any integer r>=1, put μ_j=κ_d 2^{jd}. Then

 E N_*^r <= B_r(1+μ_0)^r
        + sqrt(B_{2r}) Σ_{j>=1}(1+μ_j)^r sqrt(q_{2^{j−1}}) < infinity.   (34)

To prove it, bound the contribution of J=0 by E N(B(0,1))^r. For j>=1, apply Cauchy–Schwarz to N(B(0,2^j))^r 1{J=j}, use {J=j}⊂{J>j−1}, and use the Poisson moment bound. Exponential decay in 2^{(j−1)d} beats every polynomial in 2^{jd}. Equation (34) controls point count, not arithmetic operation count or the precision needed for geometric predicates.

No distribution of a “uniform simplex from the infinite process” is sampled by this algorithm. It samples an unconditioned **point-Palm score**. Division by k+1 is still required to get simplex intensities, and the ratio of the expected scores gives the desired fraction. Averaging per-run ratios would generally give a different quantity and is not proposed.

## 4. Confidence intervals without a boundary-bias term

Let D_* be the constant D in turn 3 equation (18), with M replaced by H. The same proof gives E S_F²<=D_*, and 0<=S_D<=S_F. For independent algorithm runs indexed i=1,...,n, put

 A_i=S_{D,i}/(k+1), B_i=S_{F,i}/(k+1),
 Abar=(1/n)Σ_i A_i, Bbar=(1/n)Σ_i B_i.

Then E A_i=a_{d,k}, E B_i=b_{d,k}, and both second moments are at most D_*/(k+1)². For confidence parameter 0<δ<1 define

                   e_n=sqrt(2D_*/[(k+1)² n δ]).                    (35)

Chebyshev's inequality and a union bound show that, with probability at least 1−δ, both means are within e_n of their expectations. On that event, if Bbar>e_n, the interval

 [ max{0,(Abar−e_n)/(Bbar+e_n)},
   min{1,(Abar+e_n)/(Bbar−e_n)} ]                                 (36)

contains theta_{d,k}=a_{d,k}/b_{d,k}. If Bbar<=e_n, use [0,1]. The interval is ordered because 0<=Abar<=Bbar. These are fixed-n intervals, not an anytime-valid sequential confidence sequence; repeated data-dependent stopping is not justified by (35).

Alternatively, when the numerator a is treated as a known credited intensity, only the B_i mean need be estimated. A one-mean Chebyshev interval and the deterministic lower bound b>=a give the corresponding ratio bounds. Formula (36) avoids needing any numerical integration of the known numerator.

The series defining D_* has a straightforward certifiable numerical tail if needed. For its j-th summand t_j=(1+A2^{jd})^{2k}exp(−c2^{jd}), A=κ_d2^{2d}, c=v/2,

 t_{j+1}/t_j <= 2^{2kd}exp(−c(2^d−1)2^{jd}).                      (37)

Once this bound is at most 1/2, every later ratio is at most 1/2, and the tail from the next term is at most twice that term. Elementary enclosures of κ_d and exp make a rigorous upper bound available. None is numerically evaluated here; the supplied finite controls check algebra and geometry, not Monte Carlo outcomes.

## 5. Final mathematical disposition

The five-turn attempt proves finite intensity-independent simplex fractions with an L1 window interpretation; strictly missing flag faces in every 2<=k<=d; the strict planar interval 2/3<theta_{2,2}<1; controlled finite integrals; and a self-certifying exact Palm sampler with finite point-cost moments. All use the stated homogeneous model and simplex-typical convention, and the corrected cone aperture.

The exact planar fraction, useful numerical estimates in higher dimensions, and the source's proposed dimensional likelihood behavior remain unresolved. The finite-dimensional integral representation and ideal sampler are partial methods, not an evaluated solution or a claimed new literature result. The author budget is exhausted at five substantive turns. No sixth author search is part of this packet.
