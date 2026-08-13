# An exact fitness-dependent diffuse support identity

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## Status

**PROVED EXACT IDENTITY.**  For every finite adjoint diffuse kernel and every
fitness `r>1`, the leaf-annihilating response score admits the square
decomposition

\[
 \boxed{
 T_r={r(r-1)\over4}K_r
      +{r\over r-1}E_p\!\left[
       h\left\{{u\over h}-{r-1\over2}A\right\}^{\!2}\right] .} \tag{1}
\]

Here `T_r` is dB cost minus `(r-1)` times Bd gain, and

\[
 K_r={4\over r-1}E_p\!\left[{t x^2\over q}\right]
       -E_p(hA^2),
 \qquad A=Px-{x\over h}.                                  \tag{2}
\]

At `r=2`, (1) is exactly the previously proved ground-energy decomposition
of `1-beta-sigma`.  Formula (1) does **not** assert `K_r>=0`.  That sign is
open even at `r=2`, and the identity applies only to the exact diffuse
adjoint normal form below.  It is not a universal one-fitness separator for
arbitrary finite graphs; the stored weak-cut `K_2--K_20` trace refutes that
globalization at `R_hyb`.

## 1. Adjoint endpoint setup

Let `P` be finite, row stochastic, and self-adjoint in `L^2(pi)`.  Let
`a>0`, normalized by `E_pi a=1`, and put

\[
 p=\pi a,\qquad R=D_a^{-1}PD_a,\qquad t={Pa\over a}.       \tag{3}
\]

The two positive endpoint survival vectors at fitness `r>1` obey

\[
 t b=r(1-b)Pb,\qquad s=r(1-s)Rs.                          \tag{4}
\]

Write

\[
 p_0={r-1\over r},\qquad q=1-b,\quad h=1-s,
 \qquad x=b-p_0={1\over r}-q,
 \quad u=s-p_0={1\over r}-h.                              \tag{5}
\]

All expectations below are under `p`.  The measure is normalized because
`E_pi a=1`, and adjointness gives

\[
 E_p(Pf)=E_p(tf),\qquad E_p(fRg)=E_p(gPf).                 \tag{6}
\]

## 2. Exact endpoint deficits

Define

\[
 B_r={r\over r-1}E_p\!\left[{t x^2\over q}\right]
     ={r^2\over r-1}E_p\!\left[{t x^2\over1-rx}\right],  \tag{7}
\]

\[
 D_r={r\over r-1}E_p\!\left[{u^2\over h}\right]
     ={r^2\over r-1}E_p\!\left[{u^2\over1-ru}\right].   \tag{8}
\]

Both are nonnegative.  From the Bd equation,

\[
 0=E_p\!\left[tb\left({1\over rq}-1\right)\right]
   =E_p\!\left[{tbx\over q}\right].                      \tag{9}
\]

The scalar identity

\[
                         {bx\over q}=(r-1)x+{r x^2\over q} \tag{10}
\]

therefore yields

\[
                              E_p(tx)=-B_r.                 \tag{11}
\]

Similarly, the dB equation and `E_p(Rs)=E_p s` give

\[
 0=E_p\!\left[s\left({1\over rh}-1\right)\right]
   =E_p\!\left[{su\over h}\right],                        \tag{12}
\]

and

\[
                         {su\over h}=(r-1)u+{r u^2\over h}
 \quad\Longrightarrow\quad E_pu=-D_r.                     \tag{13}
\]

Thus `D_r=p_0-E_p s` is the exact dB cost.

## 3. Cross-energy and Bd gain

Let

\[
 \mathcal E(a,b)=\langle a,(I-P)b\rangle_\pi
                 =E_p[(1-t)x].                            \tag{14}
\]

Combining (11) and (14) gives

\[
                         E_p b-p_0=\mathcal E(a,b)-B_r.     \tag{15}
\]

The centered dB equation is equivalent to

\[
                    1-t={r\over r-1}\left(Ru-{u\over h}\right). \tag{16}
\]

Consequently, by (6),

\[
 \boxed{
 \mathcal E(a,b)={r\over r-1}E_p(uA),
 \qquad A=Px-{x\over h}.}                                 \tag{17}
\]

## 4. Completion of the square

Define the support deficit

\[
\begin{aligned}
 T_r
  &:=(p_0-E_p s)-(r-1)(E_pb-p_0)\\
  &=(r-1)E_pq-E_ps.                                       \tag{18}
\end{aligned}
\]

Equivalently, if

\[
 G_B(r)=E_pb-p_0,\qquad G_D(r)=E_ps-p_0,                   \tag{19}
\]

are the Bd and dB gains, then

\[
                 T_r=-\{G_D(r)+(r-1)G_B(r)\}.              \tag{20}
\]

Substituting (7)--(8), (15), and (17) into (18) gives

\[
 T_r=rE_p\!\left[{t x^2\over q}\right]
      +{r\over r-1}E_p\!\left({u^2\over h}\right)
      -rE_p(uA).                                           \tag{21}
\]

Completing the square in `u` proves (1)--(2).  The nonlocal label `Px` can
also be eliminated pointwise using (4):

\[
 Px={t(1-q)\over rq}-p_0,
 \qquad
 A={t(1-q)\over rq}-p_0-{1/r-q\over h}.                   \tag{22}
\]

Thus `K_r` is an exact constrained scalar inequality in `(t,q,h)` once the
two endpoint ground equations are retained.

The scalar deficit functions in (7)--(8) are convex on their physical
domains.  For example,

\[
 {d^2\over dz^2}\left\{{r^2\over r-1}{z^2\over1-rz}\right\}
 ={2r^2\over(r-1)(1-rz)^3}>0.                              \tag{23}
\]

This identifies the natural entropy curvature for any attempted
fitness-integrated proof of `K_r>=0`.

## 5. Boundary check: deterministic two-cycle

For the deterministic two-cycle and temperature ratio `kappa>0`, the Bd
extinction probabilities are

\[
 q_1={\kappa r+1\over r(\kappa+r)},\qquad
 q_2={\kappa+r\over r(\kappa r+1)},                        \tag{24}
\]

and the dB survival vector is `(s_1,s_2)=(b_2,b_1)`.  Under the normalized
measure `p=(1,kappa)/(1+kappa)`, direct reduction gives

\[
 \boxed{
 T_r={(\kappa-1)^2(r-1)\over
              r(\kappa+r)(\kappa r+1)}\geq0.}              \tag{25}
\]

Equality occurs only in the isothermal mode `kappa=1` (apart from the
neutral boundary `r=1`).  This is a sharp hostile check of all signs and
normalizations in (1).

## 6. Exact bridge to the pair--leaf threshold algebra

For a dilute strong `K_2` pair of internal scale `sigma`, the leading Bd
and dB responses are

\[
 b_2(r,\sigma)={2(\sigma-1)\over1+\sigma(r^2-1)},\qquad
 d_2(r,\sigma)={2\{r(2-r)-\sigma\}\over\sigma+2r(r-1)}.   \tag{26}
\]

An ordinary leaf has response `(1/(r-1),-1)`, so the same support in
(20) annihilates every leaf.  For the pair,

\[
 \mathcal S_r:=d_2+(r-1)b_2
 ={-2rF_r(\sigma)\over
       \{2r(r-1)+\sigma\}\{1+\sigma(r^2-1)\}},            \tag{27}
\]

where

\[
 F_r(\sigma)=(r-1)\sigma^2
 +(r^3-4r^2+3r+1)\sigma+r(2r-3).                           \tag{28}
\]

Since `T_r=-S_r`, its pair value is

\[
 T_r^{(2)}={2rF_r(\sigma)\over
       \{2r(r-1)+\sigma\}\{1+\sigma(r^2-1)\}}.            \tag{29}
\]

The exact square-minus-sextic identity is

\[
 4(r-1)F_r(\sigma)
 =\{2(r-1)\sigma+r^3-4r^2+3r+1\}^2-P(r),                  \tag{30}
\]

\[
 P(r)=r^6-8r^5+22r^4-30r^3+21r^2-6r+1.                  \tag{31}
\]

At `R=R_hyb`, where `P(R)=0`, the optimizer

\[
 \sigma_*={-R^3+4R^2-3R-1\over2(R-1)}                    \tag{32}
\]

makes both terms on the right of (30) vanish.  Equations (27)--(30) show
that (1) is the exact diffuse analogue of the pair--leaf tangent support,
while also explaining why a universal affine globalization is too strong.

## 7. The first fitness-integrated obstruction

The positive denominator-clearing multiplier forced by (29) is

\[
 W(r,\sigma)=
 {\{2r(r-1)+\sigma\}\{1+\sigma(r^2-1)\}\over2r}>0,       \tag{33}
\]

and it gives simply

\[
                         W(r,\sigma)T_r^{(2)}=F_r(\sigma). \tag{34}
\]

For any finite signed measure `nu` on a fitness interval, put

\[
 I_\nu(\sigma)=\int F_r(\sigma)\,d\nu(r)
              =A_\nu\sigma^2+B_\nu\sigma+C_\nu,           \tag{35}
\]

where

\[
 A_\nu=\int(r-1)d\nu,
 \quad B_\nu=\int(r^3-4r^2+3r+1)d\nu,
 \quad C_\nu=\int r(2r-3)d\nu.                            \tag{36}
\]

An integrated charge tangent to the optimized pair at `sigma_*` must obey

\[
                  B_\nu=-2A_\nu\sigma_*,
 \qquad C_\nu=A_\nu\sigma_*^2.                            \tag{37}
\]

These are the exact two moment constraints on any proposed cross-fitness
weight.  They expose an immediate positivity obstruction.  The proved
hybrid monotonicity `L(r,sigma_*)<lambda_*<U(r,sigma_*)` gives

\[
                         F_r(\sigma_*)<0
       \qquad(1<r<R_hyb).                                  \tag{38}
\]

Therefore every nonzero nonnegative measure supported in
`[r_0,R_hyb)` satisfies

\[
                         I_\nu(\sigma_*)<0,                 \tag{39}
\]

and cannot satisfy the tangency conditions (37).  Adding a nonnegative
atom at `R_hyb` does not help, because both `F_R(sigma_*)` and its
`sigma`-derivative vanish there.

Hence a genuinely cross-fitness cancellation based on (34) must use at
least one of the following ingredients:

1. a signed fitness weight;
2. a nonlinear charge, such as a negative-part penalty that detects failure
   of Bd or dB amplification at another fitness;
3. a separate boundary/derivative observable not contained in `T_r` alone.

This is not a failure of the threshold hypothesis.  It is forced by the
known hybrid construction, which has both gains positive for every fixed
`r<R_hyb` and reaches the tangent only at the endpoint.  In particular, no
positive weighted integral of the one-fitness support deficits can by
itself be the matching upper theorem.

## 8. Scope and next proof target

Within the diffuse adjoint class, `K_r>=0` would imply `T_r>=0` by (1),
ruling out simultaneous positive leading gains at that fitness.  The
stored non-diffuse constructions necessarily evade that sign.  Across the
full graph class, the exact endpoint theorem still required is the
nonlinear disjunction

\[
 \min\left\{{\rho_{Bd}(G,R)\over\rho_{Bd}(K_n,R)},
             {\rho_{dB}(G,R)\over\rho_{dB}(K_n,R)}\right\}\leq1. \tag{40}
\]

The weak-cut tangent refutation and (39) together show that neither a
single affine support nor a positive integral of those supports can prove
(40).  The minimal remaining cross-fitness route must explicitly remember
which coordinate fails away from the endpoint, rather than compressing the
two response curves into `T_r` before integration.

## 9. Exact neutral-boundary charge in the diffuse class

There is one coordinate-wise cross-fitness fact that can be proved exactly
inside the adjoint diffuse class.  Assume throughout this section that:

- the type space is finite and fixed;
- `P` is irreducible, row stochastic, and self-adjoint in `L^2(pi)`, with
  `pi_i>0`;
- `a_i>0` and `E_pi a=1`, with `R,t,p` defined by (3).

For each sufficiently small `epsilon=r-1>0`, the two irreducible concave
endpoint maps in (4) have a unique nonzero positive fixed point.  Those
fixed points form analytic one-sided branches after division by `epsilon`,
and

\[
 b_r=\epsilon c_Ba+O(\epsilon^2),\qquad
 s_r=\epsilon {c_D\over a}+O(\epsilon^2),                  \tag{41}
\]

where

\[
 c_B={E_\pi(t a^2)\over E_\pi(t a^3)},\qquad
 c_D={1\over E_\pi(1/a)}.                                  \tag{42}
\]

Here and below `a` retains the normalization `E_pi a=1`.  To derive the
first coefficient, insert

\[
                         b_r=\epsilon c a+\epsilon^2d+o(\epsilon^2)
\]

into the Bd equation.  The order-`epsilon^2` equation is

\[
 (D_t-P)d=c\,at-c^2a^2t.                                  \tag{43}
\]

The exact ground-state identity

\[
 \langle f,(D_t-P)f\rangle_\pi
 ={1\over2}\sum_{i,j}\pi_iP_{ij}a_ia_j
       \left({f_i\over a_i}-{f_j\over a_j}\right)^2       \tag{43a}
\]

makes `D_t-P` positive semidefinite with kernel `span{a}`.  Its solvability
condition against `a` is therefore

\[
 cE_\pi(t a^2)-c^2E_\pi(t a^3)=0,                         \tag{44}
\]

which gives `c=c_B`.  For the second endpoint, `R(1/a)=1/a`.
Inserting

\[
                         s_r=\epsilon {c\over a}+\epsilon^2e
                              +o(\epsilon^2)
\]

gives

\[
                         (I-R)e={c\over a}-{c^2\over a^2}. \tag{45}
\]

The invariant left measure of `R` is `p=pi a`; its solvability condition
is

\[
                         c-c^2E_\pi(1/a)=0,                \tag{46}
\]

proving the second formula in (42).

For completeness, the expansion and its error are rigorous, rather than
formal.  Set `b=epsilon y` and divide the Bd equation by `epsilon`.  The
resulting analytic map is

\[
 \Phi_B(\epsilon,y)=D_ty-(1+\epsilon)Py
       +\epsilon(1+\epsilon)y\mathbin\odot Py.             \tag{46a}
\]

At `epsilon=0`, its zero set is the Perron line `y=ca`.  Projecting onto
`a^perp` and using the inverse of `D_t-P` there solves the complementary
coordinate analytically as a function of `(epsilon,c)`.  The remaining
scalar equation has a removable factor `epsilon`; at `epsilon=0` it is

\[
                         -cE_\pi(ta^2)+c^2E_\pi(ta^3)=0,   \tag{46b}
\]

whose positive root is simple.  The analytic implicit-function theorem
therefore gives the first expansion in (41).  The same argument for
`s=epsilon y`, projecting along the left invariant measure `p` of `R`, has
reduced scalar equation

\[
                         -c+c^2E_\pi(1/a)=0,               \tag{46c}
\]

and proves the second expansion.  Irreducibility makes both Perron kernels
one-dimensional and identifies these local positive branches with the
unique nonzero fixed points of the endpoint maps.

In particular, for every fixed datum `(P,pi,a)` there are constants
`epsilon_0>0` and `C<infinity` such that the two remainders in (41) are at
most `C epsilon^2` in `l^infinity` for `0<epsilon<epsilon_0`.  The constants
are uniform on any compact family of fixed-dimensional data on which
`min_i(pi_i,a_i,t_i)` and the two complementary Perron spectral gaps stay
bounded away from zero.  No such uniformity is claimed for a sequence whose
type number diverges, whose temperature becomes singular, or whose
spectral gap collapses.  Those are precisely the regimes in which a
nonuniform neutral boundary layer can survive.

Since `E_p(1/a)=1`, the dB average satisfies

\[
 \left.{d\over dr}\right|_{1+}\{E_ps_r-p_0(r)\}
       ={1\over E_\pi(1/a)}-1\leq0,                        \tag{47}
\]

with equality if and only if `a` is constant, by strict convexity of
`z -> 1/z` and `E_pi a=1`.  Equivalently,

\[
 \boxed{
 \lim_{r\downarrow1}{T_r\over r-1}
 =1-{1\over E_\pi(1/a)}\geq0,}                            \tag{48}
\]

again with strict inequality outside the isothermal mode.

Thus every non-isothermal diffuse adjoint mechanism is already dB
suppressing at the neutral boundary.  This supplies an exact example of
the extra coordinate-wise observable demanded by Section 7.  It also
formalizes why the pair--leaf lower construction, which has both leading
gains positive at every fixed interior fitness, must retain a genuinely
non-diffuse boundary layer: it cannot converge uniformly to this
independent diffuse endpoint branch as `r` approaches one.

For a full-class matching upper theorem, the smallest visible disjunctive
target is consequently not a sign condition on `T` alone.  In response
coordinates it has the form

\[
 \boxed{
 \min\{G_B'(1+),\ G_D'(1+),\
       G_D(R_hyb)+(R_hyb-1)G_B(R_hyb)\}\leq0.}             \tag{49}
\]

The stored weak-cut tangent witness is admitted because its Bd neutral
derivative is negative; the optimized pair--leaf sequence is admitted
because its endpoint support is zero.  Equation (49) is recorded as a
target, not as a proved full-graph theorem.  For nonuniform asymptotic
sequences, a fixed interior fitness `r_0>1` may be needed in place of the
derivative, because the known construction has a singular neutral boundary
layer.

## 10. What an atomic scale decomposition would have to retain

The tempting next claim, that every finite non-diffuse module also has
nonpositive dB weak gain, is false.  The exact five-vertex path with edge
weights

\[
                             5,\ 1,\ 1,\ 5                 \tag{50}
\]

has dB weak coefficient

\[
 c_{dB}={1397\over4655}={3\over10}+{1\over9310},           \tag{51}
\]

strictly above the complete five-vertex value `3/10`.  Its Bd coefficient
is below the complete value, so it is a one-coordinate atom, not a weak
simultaneous amplifier.  The exact neutral genealogy calculation is stored
in `notes/weak_selection_independent.md`.

The same paired sign appears in the singular pair trace.  Formally taking
the neutral limit of (26) gives

\[
 b_2(1,\sigma)=2(\sigma-1),\qquad
 d_2(1,\sigma)={2(1-\sigma)\over\sigma}
              =-{b_2(1,\sigma)\over\sigma}.               \tag{52}
\]

This is a trace boundary-layer response, not the fixed-finite-graph weak
derivative, so the two limits must not be interchanged.  It nevertheless
shows exactly why a scalar dB sign is unavailable at the module level:
dB-positive pair atoms exist, but they carry a Bd-negative charge.  Leaves
carry the opposite singular role.

Consequently a scale-by-scale compactness induction cannot assign only a
dB scalar to each atom.  Its smallest viable state is the two-coordinate
weak response vector, together with portal/trace boundary data.  A precise
target is:

> For a graph sequence with a separated module partition, the two neutral
> genealogy coefficients decompose, up to a uniform `o(1)` error, into the
> sum of rooted finite-module response vectors and the response vector of
> the inter-module trace chain; every boundary flux and uniform-start weight
> is retained.  The closed cone generated jointly by the module and trace
> vectors avoids the open positive quadrant unless the next interaction
> scale is non-diffuse.

The neutral meeting-time equations do admit an exact first-exit
decomposition, but the resulting boundary term couples the exit vertices
of different modules.  Therefore additivity of the two weak coefficients
does not follow merely by summing standalone module coefficients.  Proving
uniform control of that coupled boundary term is the first genuine compactness
lemma needed for the proposed induction.

This diagnosis is already decisive for route selection: the scalar atomic
statement is exactly refuted by (50)--(51), while a paired module-cone
statement remains plausible and is strictly weaker than the still-open
assertion that no arbitrary finite weighted graph is a weak simultaneous
amplifier.

## 11. Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
lower_global_tradeoff/verify_r_dependent_diffuse_support_identity.py
```

The replay verifies all rational identities in Sections 2--7, the
two-cycle factorization, the pair score, and the square-minus-sextic
completion.
