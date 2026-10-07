# Mass normalization and the species-pair cancellation

Prepared 2026-10-06 (America/Los_Angeles). This document proves the normalization,
energy/constraint identities and pointwise species-pair cancellation. It then
gives a **conditional transfer argument** for the occupation, selection and
simultaneous bootstrap: that part depends on the validity of the corresponding
upstream analytic estimates, which this note does not certify in full.

Completion estimate at this checkpoint: mathematical core 18%; publication
package 2%. These percentages concern the original full project, not this
algebraic subtask.

## 1. Precise physical and normalized systems

Use units with light speed and the rationalized Maxwell constants equal to one.
The physical momentum is denoted by `p`, rather than velocity. For fixed
`a=1,...,N`, let `m_a>0`, `e_a` be real, and `F_a(t,x,p)>=0`. Define

\[
 p_a^0=\sqrt{m_a^2+|p|^2},\qquad \widehat p_a=p/p_a^0.
\]

The system under consideration is

\[
 \partial_tF_a+\widehat p_a\cdot\nabla_xF_a
 +e_a(E+\widehat p_a\times B)\cdot\nabla_pF_a=0,
\]
\[
 E_t-\nabla\times B=-j,\quad B_t+\nabla\times E=0,
 \quad\nabla\cdot E=\rho,\quad\nabla\cdot B=0,
\]
\[
 (\rho,j)=\sum_a e_a\int(1,\widehat p_a)F_a\,dp.
\]

The normalized momentum and number density are

\[
 v=p/m_a,\qquad q(v)=\sqrt{1+|v|^2},\qquad u(v)=v/q(v),
 \quad f_a(t,x,v)=m_a^3F_a(t,x,m_av),\quad \lambda_a=e_a/m_a.
\]

The full phase change `(x,v)->(x,p)` has derivative `diag(I_3,m_a I_3)`
and determinant `m_a^3`. Thus `dp=m_a^3 dv`,
`F_a dp=f_a dv`, and no mass factor remains in particle number or Maxwell
charge/current. Multiplying the physical Vlasov equation by `m_a^3` gives

\[
 \partial_tf_a+u(v)\cdot\nabla_xf_a
 +\lambda_a(E+u(v)\times B)\cdot\nabla_vf_a=0,
 \qquad (\rho,j)=\sum_a e_a\int(1,u)f_a\,dv.\tag{1}
\]

In particular, replacing `f_a` merely by `F_a(t,x,m_a v)` without the
Jacobian factor would change the Maxwell sources and the conserved energy.
The common velocity law comes from the normalized momentum, whereas the
physical acceleration remains charge dependent.

The exact proposed regularity class is initially
`F_{a,0} in C_c^infinity(R^6), F_{a,0}>=0` and
`E_0,B_0 in C_b^infinity(R^3) intersect L^2(R^3)`, with the two Maxwell
constraints. Here every spatial derivative in `C_b^infinity` is bounded.
Whether this is the minimal sufficient class is a separate question; the
algebra below needs only enough regularity, integrability and support for
the displayed operations. On a compact classical interval, compact momentum
support and the field regularity justify all momentum integrations.

## 2. Transport, constraints and positive energy

For each species, the normalized characteristic flow solves

\[
 Y_a'=u(V_a),\qquad V_a'=\lambda_a(E+u(V_a)\times B).
\]

The phase divergence is zero because
`div_v(u cross B)=B dot curl_v u=0`, and `u=grad_v q`.
The scalar `lambda_a` does not change that calculation. Consequently the flow
preserves `dx dv`, transports `f_{a,0}`, and preserves particle number and the
`L^infinity` norm of each species.

Integrating (1) in momentum yields

\[
 \partial_t\int f_a\,dv+\nabla_x\cdot\int u f_a\,dv=0.
\]

Multiplying by `e_a` and summing gives `rho_t+div j=0`. Maxwell's equations
then give

\[
 \partial_t(\nabla\cdot E-\rho)=0,\qquad
 \partial_t\nabla\cdot B=0.\tag{2}
\]

The correct total energy density and flux are

\[
 \mathcal U=(|E|^2+|B|^2)/2+\sum_a m_a\int qf_a\,dv,
 \qquad \mathcal S=E\times B+\sum_a m_a\int quf_a\,dv.
\]

Multiplication of (1) by `m_a q` gives the work term
`m_a lambda_a E dot int u f_a = e_a E dot int u f_a`.
Summing exactly matches `E dot j`, which cancels the Maxwell work. Hence

\[
 \partial_t\mathcal U+\nabla\cdot\mathcal S=0,
 \qquad |\mathcal S|\le\mathcal U.\tag{3}
\]

The latter inequality uses `|u|<1` and **positive masses and densities**, not
the signs of the charges. Under the stated finite-energy hypotheses, spatial
cutoffs and (3) give conserved energy `H_0=int U(0,x) dx`.

For a backward cone `y=x-(t-s)n`, `r=t-s`, define
`d_a=1-n dot u_a` and
`G=|E+n cross B|+|n dot B|` at its source point. The exact cone flux is

\[
 \int_0^t\!\int_{S^2}\!r^2\left[
 \tfrac12(|E+n\times B|^2+|n\cdot B|^2)
 +\sum_a m_a\int qd_a f_a\,dv\right]dn\,ds
 =\int_{|y-x|<t}\mathcal U(0,y)\,dy.\tag{4}
\]

It follows that `int r^2 G^2 <=4H_0` and, for every species separately,
`int r^2 q d_a f_a <=H_0/m_a` (the weaker bound `4H_0/m_a` also suffices).
Likewise `int q f_a dx dv <=H_0/m_a`. There is no signed cancellation in
these bounds, so attractive species do not destroy the energy budget.

No neutrality condition is introduced here. Nonzero total charge is
compatible with finite field energy in three dimensions: a Coulomb tail has
size proportional to `r^{-2}`. That compatibility does not itself prove the
global theorem.

## 3. Retarded fields and exact source/receiver coefficients

Maxwell is linear in its charge and current sources. Its zero-data wave
potentials are

\[
 (\Phi,\mathcal A)(t,x)=\frac1{4\pi}\sum_b e_b
 \int_{|x-y|<t}\!\int\frac{f_b(t-|x-y|,y,v)}{|x-y|}(1,u(v))\,dv\,dy.
\]

For each source species `b`, fixed-time phase volume preservation gives the
retarded label Jacobian `dz_b=d_b dy dv`, where
`d_b=1-n dot u_b`. This follows from the rank-one determinant
`det(I-(u_b,V_b') tensor (n,0))=1-n dot u_b`. In particular, the acceleration
coefficient `lambda_b` does **not** enter this Jacobian.

Write `b_b=u_b'` (this `b_b` is an acceleration vector, not a species index).
The actual source acceleration is

\[
 b_b=\frac{\lambda_b}{q_b}(I-u_b\otimes u_b)(E+u_b\times B).\tag{5}
\]

Differentiating the retarded potentials gives, for this species, the
electric kernel and its magnetic cross product

\[
 \mathscr K_b=\frac{n-u_b}{r^2q_b^2d_b^3}
 +\frac{(n-u_b)(n\cdot b_b)-d_b b_b}{r d_b^3},
 \qquad n\times\mathscr K_b.\tag{6}
\]

The overall coefficient in the fields is `e_b/(4pi)`. Initial-cone boundary
terms carry the same `e_b`. The homogeneous wave terms carry no species
factor until a receiver is chosen.

For a receiving species `a`, write `alpha=u(V_a)`, `K_a=V_a'`,
`q_X=q(V_a)`, `D=1-n dot alpha`, `Q=D I+n tensor alpha`. Since
`h+alpha cross (n cross h)=Qh`, its force representation is

\[
 K_a=K_a^{\rm data}+\frac1{4\pi}\sum_b c_{ab}
 \int(T_b+S_b)\,dy\,dv,\qquad c_{ab}=\lambda_a e_b,\tag{7}
\]
\[
 T_b=\frac{f_bQ(n-u_b)}{r^2q_b^2d_b^2},\qquad
 S_b=\frac{f_bQ((n-u_b)(n\cdot b_b)-d_b b_b)}{r d_b^2}.
\]

Thus the physical transport coefficient is `e_a e_b/m_a`, and the
source-acceleration coefficient after substituting (5) is
`e_a e_b^2/(m_a m_b)`. Confusing the first with
`lambda_a lambda_b` loses a factor `m_b`; replacing the second by the first
loses the source charge/mass factor and its sign. Neither simplification is
valid in general.

## 4. Pairwise signed cancellation: proved without equal accelerations

Fix a receiver species `a` and source species `b`. Along their retarded
branch let

\[
 t=s+r,\quad rn=X_a(t)-Y_b(s),\quad
 d=1-n\cdot u_b,\quad D=1-n\cdot\alpha,
 \quad \varepsilon=1-\alpha\cdot u_b.
\]

A prime is a full derivative in `s` on this branch. Elementary
differentiation gives

\[
 t'=d/D,\quad r'=d/D-1,\quad
 rn'=N_0=(d/D)(\alpha-n)+n-u_b,\quad n\cdot N_0=0.\tag{8}
\]

Combining the retarded label Jacobian with `t'=d/D` gives
`ds f_{b,0} dz_b = D dt f_b dy dv`. Put

\[
 H=Q/D,\quad g=(u_b-n)/d,\quad k=u_b-\varepsilon n/D.
\]

Then `Hg=k/d`. The unweighted pair kernel in `ds f_{b,0} dz_b` measure is

\[
 \mathcal K_{ab}=-\frac H r\,\partial_s^{(u_b)}g
 -\frac{Hg}{r^2q_b^2d}.\tag{9}
\]

The entire physical pair contribution is multiplied by `c_ab/(4pi)`.
There is an exact identity

\[
 \boxed{\quad\mathcal K_{ab}
 =-\left(\frac{k}{rd}\right)'
 +\frac{\varepsilon}{r^2D^2}
       \left(\frac{n}{q_X^2D}-\alpha\right)
 +\frac{n(\alpha_t\cdot k)}{rD^2}.\quad}\tag{10}
\]

**Proof.** Apply the product rule to the first term of (9). For a variation
`A` of `alpha`, holding the source and cone direction fixed,
`partial_alpha k[A]=n(A dot k)/D`. Since `alpha'=alpha_t d/D`, this
is the last term of (10). The remaining geometric terms, multiplied by
`r^2 d^2`, are

\[
 rd(k)'_n+k(N_0\cdot u_b-dr'-q_b^{-2}).
\]

Using (8) and `|u_b|^2=1-q_b^{-2}` gives

\[
 N_0\cdot u_b-dr'-q_b^{-2}=-\varepsilon d/D,
 \quad rd(k)'_n=-\frac{\varepsilon d}{D}
          \left(N_0+\frac{n(N_0\cdot\alpha)}D\right).
\]

Finally `|alpha|^2=1-q_X^{-2}` gives

\[
 N_0+\frac{n(N_0\cdot\alpha)}D+k
 =\frac dD\left(\alpha-\frac{n}{q_X^2D}\right).
\]

Substitution proves the middle term, including its sign. The terms
containing the arbitrary vector `u_b'` are exactly the differentiated
primitive terms. No equality of `lambda_a` and `lambda_b` has been used.
The proof is valid for any strictly timelike smooth source and receiver
trajectories with the common normalized velocity law. Multiplying (10) by
the fixed scalar `c_ab`, of either sign, is legitimate. ∎

For an independent cleared-denominator check of the same identity see
`verify_pair_identity.py`. It uses exact integer polynomial arithmetic in
six generic velocity components and does not use numerical tolerances.
This is a check of (10), not a formalization of the global PDE theorem.

In `dt dy dv` measure the geometric and receiver remainders are respectively

\[
 c_{ab}\frac{f_b\varepsilon}{r^2D}
       \left(\frac{n}{q_X^2D}-\alpha\right),\qquad
 c_{ab}\frac{f_bn(\alpha_t\cdot k)}{rD}.\tag{11}
\]

The original source coefficient `lambda_b` remains in the source
derivatives of smooth cutoffs, through (5). It is absent from the two bulk
remainders (11). Therefore the cancellation does not silently erase charge
signs: the differentiated primitive uses the actual signed source motion,
and `c_ab` multiplies every term consistently.

## 5. Uniform species-dependent bounds, conditional bootstrap

Assume a compact classical interval and a common dyadic `P` larger than
`1024 max_{a,z,t} q(V_a(t,z))`. Write `L=log(2+P)`, `S(w)=P^2 L/w`.
The simultaneous bootstrap is the statement, for **every species** and
every supported receiver/eligible range interval,

\[
 |V_a(t_2)-V_a(t_1)|\le MP\sqrt{t_2-t_1}
                 +A(t_2-t_1)S(w).\tag{12}
\]

All species share the field. Nothing here invokes a separate one-species
existence theorem for each species. Instead (12) gives the source and
receiver stability needed for each pair, and the resulting force estimates
are summed in (7) before improving (12).

In the narrow sector `q_b~p`, `q_X~w`, `d~theta^2`, `D~phi^2`,
`theta<=16 kappa phi`, the geometric identities give
`|k|<=C theta/phi`, `|P_X k|<=C theta`,
`|P_X n|<=C phi`. Here `P_X` is orthogonal projection perpendicular to
the nonzero receiver momentum. From (5),

\[
 |u_b'|\le C|\lambda_b|p^{-1}(G+\theta^2|B|),\quad
 |n\cdot u_b'|\le C|\lambda_b|p^{-1}\theta(G+\theta^2|B|),
 \quad |q_b'|\le C|\lambda_b|(G+\theta|B|).\tag{13}
\]

The receiver identity is exactly
`alpha_t=(I-alpha tensor alpha)K_a/q_X`, even if `lambda_a=0`.
It introduces **no additional lambda_a** and requires no division by it.
Consequently the absolute bulk bounds from (11) are

\[
 C|c_{ab}|f_b/r^2,\qquad
 C|c_{ab}|f_b\theta|K_a|/(wr\phi^2),\tag{14}
\]

and their perpendicular projections gain a factor `phi`. Source-cutoff
errors have bounds

\[
 C|c_{ab}\lambda_b|\left(
        \frac{f_b\phi G}{rp\theta^2}
       +\frac{f_b\phi|B|}{rp}\right),\tag{15}
\]

spatial-cutoff errors have `C|c_ab| f_b phi/(r^2 theta)`,
receiver-cutoff errors have the second bound in (14), and time-weight
errors have `C|c_ab| |psi_t| f_b theta/(r phi)`. The common physical
multiplier must be factored out before summing cutoff derivatives.
The identity `sum beta_j=1` is specieswise; different pair prefactors
must never be canceled against one another.

For each source `b`, define its occupation measure exactly with its own
nonnegative density, flow and initial labels:

\[
 \mathsf M_b=\int dt\,ds\,dn\ r^2D\int_{\mathrm{bin}}f_b\,dv
            =\int f_{b,0}(z_b)\,dz_b\int_{\mathrm{hits}}ds.
\]

Both changes of variables are independent of acceleration coefficients.
The pointwise bin density is `<=C ||f_b0||_infinity p^3 nu^2`, where
`nu=theta` in the narrow sector and `nu=min(theta,sigma)` otherwise.
Using (4), the crude bounds are
`M_b<=C_b max(I,h)/p` and `M_b<=C_b I phi^2/theta^2`.

To obtain stable cells from (12), set `m=min(p,w)`, use the same tolerance
`omega` as upstream, and choose one fixed `C_1` covering every species:

\[
 \lambda=\left[C_1\frac Pm
     \left(\frac M\omega+\sqrt{\frac{AL}{\omega}}\right)\right]^{-2}.
\]

The stopping-time proof uses (12) directly on the source species and
receiver species. It gives `|Delta V|<=epsilon_0 m omega`,
`|Delta u|<=epsilon_0 omega`, and comparable `q` on the common cell.
It never estimates the actual acceleration to obtain this stability, so
different or oppositely signed `lambda_a,lambda_b` do not change its time
scale. In an actual bin the relative velocity is bounded below by
`c omega`; the same-time projected separation is monotone on a stable
cell. Its hit range has size `C h(phi+omega)`. This bounds label residence
by `C h k_1`, and (4) bounds label mass by `C_b/p`.

This proves, under (12), the stable-cell bound

\[
 \mathsf M_b\le C_b\frac{hk_1}{p}
       \max(1,I/\lambda,h/\lambda).\tag{16}
\]

For the narrow-sector joint budget, replace `q f` in the two indicators
of upstream occupation.tex by `q f_b`, keeping the same receiver.
Finite overlap and (4) give `sum_{p,phi} E^{(b)}_{p phi}<=C_b`.
The averaging-over-cells proof yields
`M_b<=C_b h k_1/p [1+(I/lambda) E^{(b)}_{p phi}]` outside the stated deficit
exception. There is no total signed density or signed energy budget.

The direction-change and enhanced occupation argument transfers
**provided its upstream direct-force and weighted-kernel estimates are
correct**: the receiver force is the full sum (7); every pair term has
one of the bounds (13)--(15), and finitely many fixed prefactors can be
absorbed into constants independent of `M,A,P`. The direction count is
`C(M,A,datum,masses,charges,N) L^6/delta`. Applying it separately to source
and receiver trajectories gives the same intermediate-angle occupation
bound

\[
 \mathsf M_b\le C_b\frac hp\phi^{-29/25}
      \max(1,I/I_m^0,h/I_m^0),\qquad I_m^0=(m/P)^2,\tag{17}
\]

in the exact upstream window. Its constant can be made independent of
`M,A` by increasing `P_*(M,A,datum,masses,charges,N)` as in that argument.
Equation (17) is not independently proved here beyond that transparent
transfer of dependencies.

At a fixed receiver time the two absolute bounds for a receiver coefficient
from one pair are

\[
 C_{ab}^{\rm data}\,U,\qquad
 U=\frac1w\min\{h^2(p\theta)^3,(p\theta h\phi^2)^{-1}\}.\tag{18}
\]

The constant contains `|c_ab|`, `||f_b0||_infinity` or `H_0/m_b` as
appropriate. If the pair has zero prefactor it vanishes. The exact pure
selection inequalities can use the same representative `M_*` and
`W=(P theta)^(-epsilon) phi^epsilon h^epsilon` as upstream, because
`M_b<=C_b M_*`. Every extra species factor is a fixed exterior constant.
If the upstream exponent lemma is correct, its conclusion
`U<=w^(-1/2)W` therefore applies without changing an exponent. Summing
over bins and the finite species set gives
`sum_selected C_ab^data U<=C_a w^(-1/2)`.

The corresponding full absolute-force estimate is

\[
 \int_J|K_a|\,dt\le C\sqrt w\{P\sqrt I+(M+\sqrt A)I S(w)\}.
\]

Multiplication removes the same `sqrt(w)` loss, rather than requiring a
small charge. The resulting weighted signed bound has one common constant
`C_eta` after taking the maximum over all receivers/species. Restoring
the endpoint ramps of (12) yields

\[
 |\Delta V_a|\le(C_\eta+2M\sqrt\eta)P\sqrt I
 +[C_\eta(M+\sqrt A)+2A\eta]I S(w).
\]

Choose `eta`, then common `M`, then common `A`, and finally the common
threshold `P_0`, exactly in that order. The strict improvement holds
simultaneously, conditional on the inherited analytic estimates.
The compact-interval continuity argument uses the maximum of the force
bounds over finitely many compact initial supports.

Finally define `Q(t)=max_{a,z in supp f_a0} q(V_a(t,z))`. The finite disjoint
union of initial supports is compact, so `Q` is continuous. The first
momentum-doubling proof uses the common `M,A,P_0`, even when the label
achieving each doubling belongs to a different species. It gives the same
divergent harmonic lower bound on elapsed times. For fixed positive masses,
bounded physical momenta and bounded normalized momenta are equivalent.
Thus a verified simultaneous signed estimate plus an established exact
multispecies continuation theorem would imply the core theorem. Those
two dependencies remain to be certified before an unconditional claim.

## 6. Boundary and degeneracy checks

| Case | Exact outcome |
|---|---|
| Equal masses one, charges +1/-1 | `lambda_+=1, lambda_-=-1`; the transport matrix `(c_ab)` is `[[1,-1],[-1,1]]`. In the source-acceleration matrix `c_ab lambda_b`, the rows are `[1,1]` and `[-1,-1]`. (10) holds with each actual signed source derivative. |
| Zero receiver charge | `lambda_a=0`, `K_a=0` and every `c_ab=0`; the receiver is free transport. No division by charge occurs. |
| Zero source charge | `e_b=lambda_b=0`; the species produces no Maxwell field and every pair contribution from it is zero. Its particles are passive and its momentum support is constant. |
| Identical masses and charges | Equal force laws give identical flows. Replacing the two initial densities by their sum gives the identical physical system and the same positive energy/constraints. |
| One species, mass/charge one | All formulas reduce exactly to the upstream normalization; this verifies reduction but does not certify its global proof. |
| Charge reversal of every species | `E,B` reversed with charges gives the same characteristic forces; `rho,j` reverse and `c_ab` is unchanged. Energy is unchanged. |
| Extreme fixed mass ratio | The common velocity geometry remains exact. Constants may grow through `max |e_a|/m_a`, `H_0/min m_a`, normalized initial support and pair coefficients. No uniformity as a mass tends to zero is claimed. |
| Empty species | Its initial-label integrals vanish. If every species is empty, Maxwell is vacuum and the kinetic problem is empty. |
| Nonneutral total charge | Neither (2), (3), (4), (10) nor the conditional transfer imposes neutrality. The chosen initial class already admits the Coulomb tail. |

## 7. Exact proved scope and remaining gap

**Verified here:** normalization with Jacobian; all signed charge/mass factors;
specieswise phase-volume preservation; propagation of constraints; positive
local energy and cone flux; retarded label Jacobians; the exact signed
source/receiver identity (10); source and receiver majorants; stable-cell
occupation under a simultaneous signed bootstrap; all stated degenerate
checks. The central identity is checked by an independent exact polynomial
certificate in addition to its displayed proof.

**Conditional only:** improved direction occupation, final selected-bin
coefficient summation and closure, insofar as they use the upstream analytic
proof. They do not encounter a new mass/charge mismatch. A false upstream
estimate would invalidate the transferred estimate and block the full
theorem. This note has not reproduced the full upstream analytic audit,
the exact multispecies local/continuation theorem or a priority audit.
No claim of a full solution, publication readiness, formal verification
of the PDE theorem, or novelty follows from this note alone.
