# Turn 4: logarithmic bounded-Lipschitz convergence for the uncut superlinear scheme

Substantive author turn **4/5**. We now return to the exact unmodified LT recursion with g(v)=v_+^(5/4), using the same white noise as the exact solution. All numerical values are finite and nonnegative for any fixed mesh, by the algebraic argument in turn 1; this does not assert finite higher moments.

Let h=1/N, τ=T/M, and assume **balanced refinement**

                         c h²<=τ<=γh²                             (38)

with fixed 0<c<=γ<infinity. Let I_{h,τ}U be the continuous piecewise bilinear interpolation of the grid values, with zero spatial boundary and the sampled initial profile at time0. For every 0<q<1/2 there is C such that, for all sufficiently small h,

 d_BL(Law(I_{h,τ}U),Law(u)) <= C [log(e/h)]^(−q),                  (39)

where the laws are on C([0,T]×[0,1]) with supremum norm, and d_BL takes the supremum over functions F with |F|<=1 and Lipschitz constant at most1. The same coupling converges uniformly on space-time in probability. This is a positive rate for **bounded** Lipschitz path tests, not a quarter-order strong theorem, a rate for every unbounded observable, or an optimal weak order.

## 1. Couple the exact and numerical cutoff systems

Use the cap g_R(v)=min(v_+,R)^(5/4), with its exact solution u^R and its LT values U^R, all on the same Brownian sheet and with the same initial data. Set

 D_R=max_{m,n}|U^R_{m,n}−u^R(t_m,x_n)|.

Take p=64 and alpha=1/2−3/64=29/64. By turn 2, for R>=1 and (25/16)Nτ sqrt(R)<=1,

                         ||D_R||_p <=C0 exp(C1 R)h^alpha.          (40)

The constants are independent of R and the mesh, under (38).

Define the good event

 G_R={sup_{t,x}u(t,x)<=R/2} ∩ {D_R<=R/2}.                         (41)

On its first component the exact solution never reaches the cap, so u^R=u throughout [0,T]. On G_R, every numerical cutoff grid value is at most R. Induction on the recursion therefore gives U^R=U at every grid point: the coefficients g_R and g agree at every frozen input value encountered.

An intermediate geometric-Brownian substep can exceed R even when its two grid endpoints do not. This does not invalidate the induction: the LT substep uses f evaluated at the **old grid state**, not g evaluated continuously along the substep. Thus identical frozen grid inputs and identical increments produce identical next steps. No unproved bound on all intermediate substep excursions is used.

The exact exit tail of turn 3 and Markov's inequality give

 P(G_R^c)<= C_q R^(−q) + C R^(−p)exp(p C1 R)h^(alpha p).           (42)

Constants absorb the replacement of R by R/2 in the exact tail.

## 2. Continuous interpolation costs only a polynomial cutoff factor

Bilinear interpolation is a contraction from the grid supremum norm to the continuous supremum norm. Hence

 ||I U^R−I(u^R|grid)||_infinity<=D_R.                              (43)

For the exact cutoff solution, the parabolic chaining estimate in turn 3 can be used with a=3/8 and p=64. Its Hölder seminorm K_R, for metric |x−y|+sqrt(|t−s|), satisfies

                             E K_R<=C R^(5/4),                    (44)

with an additional constant for the fixed smooth initial data absorbed for R>=1. Convexity of the interpolation weights and (38) imply

 Z_R:=||I(u^R|grid)−u^R||_infinity <=C K_R h^(3/8),
 E Z_R<=C R^(5/4)h^(3/8).                                       (45)

All four grid vertices of a mesh rectangle are at parabolic distance O_γ(h) from a point inside it. This is a statement about the specified bilinear interpolation, not the original discontinuous heat-kick/stochastic-substep interpolation.

On G_R, (43)–(45) and equality of the cutoff and uncut objects give

                   ||I U−u||_infinity<=D_R+Z_R.                   (46)

Outside G_R we use boundedness of the test function, not a nonexistent uniform moment bound for the uncut scheme.

## 3. Choose the cutoff after tracking every constant

Write ell_h=log(e/h). Set R_h=R0+eta ell_h, with R0 large enough for the exact exit estimate and eta>0 small enough that C1 eta<=alpha/2. For example choose eta=alpha/[2(1+C1)]. Then

 exp(C1 R_h)h^alpha <=C h^(alpha/2).

Also h sqrt(R_h)→0. Since Nτ<=γh under (38), the frozen-variance condition in (40) holds for all sufficiently small h. It is checked rather than assumed at the growing cutoff.

From (40)–(45),

 E D_{R_h}<=C h^(alpha/2),
 E Z_{R_h}<=C ell_h^(5/4)h^(3/8),
 P(G_{R_h}^c)<=C_q ell_h^(−q)+C ell_h^(−p)h^(alpha p/2).           (47)

These constants may depend on q,c,γ,T,u0, but not on the mesh. No rate is hidden in an uncontrolled cutoff-dependent constant.

For any allowed F,

 |E F(IU)−E F(u)|
 <=E(D_{R_h}+Z_{R_h})+2P(G_{R_h}^c)
 <=C_q ell_h^(−q).

The first inequality uses the Lipschitz property on G_{R_h} and |F|<=1 on its complement. The polynomial powers of h in (47) are eventually smaller than the displayed logarithmic power. Taking the supremum gives (39).

For any fixed epsilon>0, (46) also gives

 P{||IU−u||_infinity>epsilon}
 <=P(G_{R_h}^c)+epsilon^(−1)E(D_{R_h}+Z_{R_h}) ->0.                (48)

Thus convergence in probability is proved under the same coupling, not merely convergence in distribution after changing the driving noise.

## 4. Scope relative to the source and prior work

The source equation is the one-dimensional space-time-white-noise model; the update is its frozen-coefficient geometric-Brownian LT scheme, not Ulander's different LTE exact-simulation method. The proof uses the specific exponent5/4, its quantified exact exit tail, and balanced time-space refinement. The arbitrary one-sided condition τ<=γh² alone is not promoted to the grid-maximum bound used here.

A logarithmic bounded-test rate does not imply convergence of first moments or mean-square errors. Very rare values of an uncut nonnegative scheme can retain mass in expectation despite convergence in probability. No result for every globally Lipschitz but unbounded test, no higher smooth-test weak order and no sharpness claim is made. The remaining mean-square and test-class distinctions must still be investigated in the final author turn. Original unresolved4/5.
