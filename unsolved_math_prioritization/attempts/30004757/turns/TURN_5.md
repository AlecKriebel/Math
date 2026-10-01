# Author research turn 5: a global collision limit with half-ball cones

Date: 2026-10-01. Final substantive author turn, 5/5. **The full source target remains unresolved.** This turn proves a source-type family limit, not the finite-separation cone classification. The partial result below awaits independent review. No novelty claim.

## The partial theorem

Let n=3 or 4 and R>0. There is a family of entire convex source-type solutions u_δ, with atoms at ±δe_n, smooth off the joining segment, and affine on that segment, such that:

1. Their quadratic and additive asymptotic normalization at infinity is fixed independently of δ.
2. The two atom sizes tend to ω_n R^n/2.
3. Their two subgradient bodies converge in Hausdorff distance to the two closed half-balls of radius R.
4. The potentials converge uniformly to the one-atom radial solution whose tangent body is the full ball of radius R.

Consequently, forming an individual tangent cone and then colliding atoms does not give the same cone as first merging the atoms. An additional isotropic rescaling and additive adjustment makes both individual atom weights exactly ω_n R^n/2 while retaining the same limiting statement and the fixed asymptotic normalization.

## 1. Radial barriers with the same asymptotic constant

Put

    W_R(r)=∫_0^r (t^n−R^n)_+^(1/n) dt.

This is convex, vanishes on the closed ball of radius R, and solves

    M_{W_R}=1_{|x|>R} dx.

For n>2 it has the expansion

    W_R(r)=r²/2+c_n R²+O(r^(2−n)),
    c_n=lim_{r→∞}[W_1(r)−r²/2]<0.

Finiteness follows because its radial derivative differs from r by O(r^(1−n)); negativity follows directly from the integral and W_1(1)=0. Write c_R=c_nR².

Choose M>0 so that

    |c_n|·2RM ≥ R+2,

and then choose δ0>0 small enough that Mδ0≤1 and

    δ0 ≤ W_R(R+2)/(R+2).

For 0<δ≤δ0 let R_δ=R+Mδ and define

    B_δ(r)=W_{R_δ}(r)+c_R−c_{R_δ}.

The difference B_δ−W_R has nonpositive radial derivative and tends to zero at infinity. Therefore

    0≤B_δ−W_R≤c_R−c_{R_δ}=O(δ).                (5.1)

The two radial functions have exactly the same constant c_R in their quadratic asymptote. Also B_δ≥δ|x_n| globally. For r≤R+2 its additive constant is at least δ(R+2), while for r≥R+2 one uses W_R(r)/r≥W_R(R+2)/(R+2), a consequence of convexity and W_R(0)=0. Finally M_{B_δ}≤dx.

## 2. Global two-plane obstacle solutions

On a large ball B_L, L>R+2, solve the convex obstacle problem with obstacle δ|x_n|, measure dx, and boundary data W_R(L). Mooney's Proposition 2.1 applies; the strict boundary-obstacle inequality can be ensured by taking L larger if necessary. Call the solution v_{δ,L}.

The zero-obstacle solution with that boundary value is W_R. Obstacle ordering and the supersolution B_δ give

    W_R≤v_{δ,L}≤B_δ.                            (5.2)

For the upper comparison one uses the equivalent Perron class with boundary values at least the prescribed boundary data, explicitly allowed by Mooney Remark 2.2. Thus B_δ need not have identical boundary values.

As L increases, these solutions are monotone on common subdomains: the larger-domain solution has boundary values at least W_R on the smaller ball. They are locally uniformly bounded by (5.2). Their locally uniform limit v_δ is an entire convex solution of the obstacle problem

    v_δ≥δ|x_n|,  M_{v_δ}≤dx,
    M_{v_δ}=dx on {v_δ>δ|x_n|}.

The last assertion follows from weak continuity of MA measures on compact sets where the limiting obstacle gap is positive. The boundary data and obstacle are invariant under axial rotations and reflection in x_n=0, so v_δ has those symmetries.

The barriers (5.2) imply both a fixed asymptotic normalization

    v_δ(x)=|x|²/2+c_R+O_δ(|x|^(2−n))

and the global bound

    0≤v_δ−W_R≤Cδ.                              (5.3)

No varying additive constant is hidden in the normalization.

## 3. Contact-body convergence

Set

    K_δ^+={v_δ=δx_n},  K_δ^-={v_δ=−δx_n}.

These are closed convex sets in their respective closed half-spaces. They are uniformly bounded: on the total contact set, W_R(|x|)≤δ|x_n|≤δ|x|, which confines it to B_{R+ε} once δ is sufficiently small, for every fixed ε>0.

For the opposite inclusion, fix a point q in the open upper half of B_R and a ball B_s(q) compactly contained there. The function f_δ=v_δ−δx_n is nonnegative, solves the ordinary zero-obstacle equation on that ball, and is at most Cδ. A small positive quadratic function centered at q has determinant at most one, dominates f_δ on the ball boundary for δ small, and vanishes at q. The local Perron comparison therefore gives f_δ(q)=0. The argument is uniform on compact subsets of the open upper half-ball. Reflection gives the corresponding lower statement.

Every point of a closed half-ball can be approximated by its open-half interior. Combining these inner contacts with the outer bound gives

    K_δ^+ → {x:|x|≤R, x_n≥0},
    K_δ^- → {x:|x|≤R, x_n≤0}                    (5.4)

in Hausdorff distance. Continuity of the volume of convex bodies gives

    |K_δ^±|→ω_nR^n/2.                           (5.5)

There is also an actual common facet for all sufficiently small δ, rather than merely a limiting one. Fix a point of {x_n=0} strictly inside B_R. On a small ball about it, (5.3) makes v_δ uniformly small. Use a fixed small multiple of Mooney's barrier w_{n,1} from his equation (3). It has MA measure at most one, dominates a fixed positive multiple of |x_n|, is positive on the unit sphere, and vanishes at the origin. After a quadratic rescaling, it dominates both δ|x_n| and the boundary values of v_δ for δ small. Perron comparison forces contact at the chosen point. Uniformity on compact subdisks shows, for example, that K_δ^+∩K_δ^- contains the disk of radius R/2 for all sufficiently small δ.

The restriction n>2 is used here: w_{n,1} is available because 1<n/2. Each K_δ^± also has full-dimensional interior by the preceding open-half-ball argument. Convexity then shows the union contains neighborhoods of interior points of the shared disk.

## 4. Return to the actual atomic equation

Let u_δ=v_δ*. The quadratic lower growth makes this Legendre transform finite everywhere. The hypotheses used in the proof of Mooney Lemma 4.2 hold: compact contact set, full-dimensional contacts in the two affine chambers, a shared facet with interior points of the total contact set, and quadratic growth. For n=3,4 that proof gives

    ∂v_δ=∂(δ|x_n|) on the contact set.

Mooney's Proposition 4.1 argument therefore yields

    M_{u_δ}=dx+a_δ^+δ_{δe_n}+a_δ^-δ_{−δe_n},
    a_δ^±=|K_δ^±|>0,

and u_δ is smooth away from the segment joining the two atoms. It is zero on the segment. At its interior points the subgradient contains the shared (n−1)-dimensional disk, so it really is a singular affine segment, not merely a potential location for one. Symmetry gives a_δ^+=a_δ^-.

These are genuine members of the source's real, entire, singular polyhedral-obstacle family. The argument uses the cited construction and its barriers; it is not an independent claim to have invented that family.

Legendre transforming (5.3) gives

    U_R−Cδ≤u_δ≤U_R,  U_R=W_R*.

Thus u_δ→U_R uniformly on R^n. The function U_R is the standard one-atom solution from turn4, with atom size ω_nR^n and tangent cone R|x|. Transforming the radial asymptotic bounds also gives the fixed normalization

    u_δ(x)=|x|²/2−c_R+O_δ(|x|^(2−n)).

## 5. The limiting individual cones are explicit

The tangent cone at +δe_n is the support function of K_δ^+. Hausdorff convergence (5.4) gives locally uniform convergence of these support functions to

    H_+(x)=R|x|   if x_n≥0,
           R|x'|  if x_n≤0.                     (5.6)

The formula is elementary: for x_n≥0 the full-ball maximizer lies in the upper half-ball; for x_n≤0 the best point has last coordinate zero. The other cone has the reflected formula.

This differs from the full-ball cone R|x| of the merged potential. In particular, at −e_n the individual upper cone is zero for every δ, whereas the merged cone has value R. The order of these two limiting operations matters.

There is a higher-regularity consequence away from the inward ray. Near the direction e_1, restrict (5.6) to x=e_1+t e_n. The limit equals R for t≤0 and R sqrt(1+t²) for t≥0. Its second derivative is zero from the left and R from the right. Therefore the family of individual cones cannot be relatively compact in C² on such a neighborhood. In particular no uniform C^{2,β} bound, β>0, can hold there across this collision regime. A uniform bound on second derivatives alone is **not** ruled out by this argument; the distinction is important.

## 6. Optional fixed-atom-weight normalization

Let a=ω_nR^n/2 and s_δ=(a/a_δ^+)^(1/n)→1. Set

    u_hat_δ(x)=s_δ² u_δ(x/s_δ)+(s_δ²−1)c_R.

Then its two atom weights are exactly a, at ±s_δδe_n. The continuous MA density remains one, and its quadratic/additive asymptote is again |x|²/2−c_R. Its tangent bodies are s_δK_δ^± and still converge to the two half-balls. The potentials converge locally uniformly to U_R. The added constant changes the level of the affine segment, which has no effect on the PDE or tangent cones.

Thus the phenomenon is not an artifact of varying atomic weights or changing the quadratic asymptote.

## 7. Full-target stopping condition

This proves a precise collision limit and a nonuniform-regularity obstruction. It does not classify the cone for any fixed positive separation, prove its smoothness away from the inward ray, establish the Hessian transition, or settle the general polyhedral/Y-shaped case. The original target is therefore **unresolved after five substantive author turns**.

The strongest remaining step is a quantitative local theorem selecting the actual finite-separation crease profile, together with control of the additional chamber-bridging exposed segments and interface rims in a general graph. The formal coefficients and model solutions in earlier turns do not substitute for that theorem. Further mathematical search under this five-turn attempt is stopped. Independent review may verify or reject the saved partial results, but must not be used as extra author search turns.
