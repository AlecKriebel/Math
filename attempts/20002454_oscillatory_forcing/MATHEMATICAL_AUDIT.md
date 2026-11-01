# Oscillatory forcing: a branch-stable scheme and observation obstruction

Row 1901; ID 20002454; AIM-PDES-0066. Authored scoped audit, 2026-10-21.
Status: partial progress only. No novelty or full workshop-resolution claim.

## Scope and sources

The original AIM contribution A.1, printed page 3, asks broadly for numerical
approximation of u_t + (f(u))_x = epsilon^{-1} h(x/epsilon). It specifies
continuous, mean-zero, one-periodic h; C1 coercive f; and u f'(u)>0, interpreted
for u != 0 since the literal inequality at zero is impossible. It does not
specify a convergence norm or a uniform-in-epsilon numerical objective.
Source: https://aimath.org/WWN/balancelaws/balancelaws.pdf .

We specialize to the unit torus, N=epsilon^{-1} a positive integer, and
H'=h, min H=0. Then F_N(x,u)=f(u)-H(Nx), with a MINUS sign. Working on the real
line does not require integer N; a torus specialization must not be imposed on
the original question. Write f0=f(0) and A=max H. The flux assumptions imply
strictly decreasing/increasing inverse branches phi_-/phi_+ on [f0,infinity).

Prior literature already establishes corrector theory under additional
hypotheses and well-balanced stationary-average reconstruction. In particular:

- Amadori, On the homogenization of conservation laws with resonant oscillatory
  source, Asymptotic Analysis 46 (2006), 53-79,
  https://doi.org/10.3233/ASY-2006-727 .
- Amadori, Homogenization of conservation laws with oscillatory source and
  non-oscillatory data,
  https://people.disim.univaq.it/~amadori/PDF/proc_amadori.pdf . Its Theorem 2
  recalls prepared-data correctors with a unique potential minimum and local
  convexity near zero; Theorem 3 treats nonoscillatory locally BV bounded data
  with C2 strictly convex flux and C2 potential with a unique minimum. Its
  Proposition 1 gives microperiodic stationary profiles, uniquely determined
  by their mean under the unique-minimum condition. Our multiple-microcell
  torus does not satisfy that unique-minimum condition on the whole torus.
- Gomez-Bueno, Castro Diaz, Pares and Russo, Collocation Methods for High-Order
  Well-Balanced Methods for Systems of Balance Laws, Mathematics 9 (2021), 1799,
  https://doi.org/10.3390/math9151799 ; author copy
  https://arxiv.org/abs/2505.02055 . The 2025 upload is not a 2025 journal result.
- Amadori and Gosse, Transient L1 error estimates for well-balanced schemes on
  non-resonant scalar balance laws, JDE 255 (2013), 469-502,
  https://doi.org/10.1016/j.jde.2013.04.016 . Nonresonant estimates are not
  blanket resonance estimates.

The proof and computations below are independently checkable specializations,
not a claim of priority over these works. No copied source document or dataset
content is part of this authored packet.

## Approach 1: close the branch-domain and stability gap

Fix one branch sigma, constants f0<Cmin<Cmax, and any periodic mesh of
intervals I_i of lengths d_i>0. Subscripts are cyclic. Put

 E_i(C) = d_i^{-1} integral_{I_i} phi_sigma(C+H(Nx)) dx,
 U_C(x) = phi_sigma(C+H(Nx)).

All integrals and inversions in Theorem 1 are exact. Let

 L = max {|f'(phi_sigma(q))| : Cmin <= q <= Cmax+A}.

Continuity, the strict gap, and compactness give 0<L<infinity. Each E_i is C1,
strictly increasing on the positive branch and strictly decreasing on the
negative branch, and

 E_i'(C) = average_{I_i} 1/f'(phi_sigma(C+H(Nx))),
 |E_i'(C)| >= 1/L.

There is no cancellation in the derivative average because its sign is fixed.
Consequently |(E_i^{-1})'| <= L, independently of N and the mesh phase.
Define the domain D_i=E_i([Cmin,Cmax]), ordered as an interval in u.

**Theorem 1.** For u_i^n in D_i, set C_i^n=E_i^{-1}(u_i^n). With
0<dt and dt L <= min_i d_i, the explicit updates

 positive branch: u_i^{n+1}=u_i^n-(dt/d_i)(C_i^n-C_{i-1}^n),
 negative branch: u_i^{n+1}=u_i^n-(dt/d_i)(C_{i+1}^n-C_i^n)

have all the following properties for all n:

(a) They remain in the product domain D, so every subsequent inverse exists.
(b) They are order preserving and conserve sum_i d_i u_i.
(c) Every grid equilibrium u_i=E_i(k), Cmin<=k<=Cmax, is preserved exactly.
(d) For two solutions of the same scheme, sum_i d_i |u_i^n-v_i^n| is
nonincreasing.
(e) They satisfy the adapted discrete entropy inequality, for every fixed k
in [Cmin,Cmax],

 |u_i^{n+1}-E_i(k)| <= |u_i^n-E_i(k)|
                       -(dt/d_i)(Q_{i+1/2}^n-Q_{i-1/2}^n),

where Q_{i+1/2}=|C_i-k| on the positive branch, and
Q_{i+1/2}=-|C_{i+1}-k| on the negative branch.

Proof. On the positive branch the update has derivatives
1-(dt/d_i)/E_i'(C_i)>=0 and (dt/d_i)/E_{i-1}'(C_{i-1})>=0.
On the negative branch they are 1+(dt/d_i)/E_i'(C_i)>=0 and
-(dt/d_i)/E_{i+1}'(C_{i+1})>=0. All other derivatives vanish. Thus the update T
is order preserving on the rectangular domain D. Its upper and lower corner
vectors are equilibria (with Cmax/Cmin interchanged on the negative branch).
Comparing against these vectors proves invariance. Flux telescoping proves
conservation, and equal C_i proves equilibrium preservation.

For contraction take coordinatewise w=max(u,v) and z=min(u,v), which belong
to D. Monotonicity gives |T_i(u)-T_i(v)|<=T_i(w)-T_i(z). Summing with weights
d_i and using conservation proves (d).

For (e) use w=max(u,e), z=min(u,e), e_i=E_i(k), and T(e)=e.
The same componentwise bound gives |T_i(u)-e_i|<=T_i(w)-T_i(z).
In the positive case C_i(w)=max(C_i,k), C_i(z)=min(C_i,k); their difference is
|C_i-k|. In the negative case the difference is -|C_i-k| because the inverse
is decreasing. Substitution into the respective conservative updates proves
the displayed inequality. This is an adapted stationary-profile entropy, not
an unstated proof of all constant-state Kruzkov inequalities. QED.

The scheme is exact-average upwind flux on a fixed sign branch: because f is
increasing on the positive branch, the physical upwind interface flux is
f(phi_+(C_i+H(Nx_interface)))-H(Nx_interface)=C_i. On the negative branch it
is C_{i+1}. This does not use global convexity of f. The CFL depends on the
chosen bounded branch band, but NOT on N. The scheme is not defined for
arbitrary initial averages outside D, nor for mixed-branch transients.

## Approach 2: a genuinely uniform, but narrowly prepared, transient bound

Let R_N[u](x)=phi_sigma(C_i+H(Nx)) for x in I_i. This is a reconstruction, not
the piecewise constant grid state. For k in the same branch band, monotonicity
ensures that the sign of R_N[u](x)-U_k(x) is constant on each cell. Hence

 ||R_N[u]-U_k||_L1 = sum_i d_i |u_i-E_i(k)|.                 (1)

**Theorem 2.** Let u_N(t) be a bounded Kruzkov entropy solution of the original
balance law on the torus, initial data u_N^0, and assume its exact initial cell
averages belong to D. Initialize Theorem 1 with those exact averages. For every
step n, with t_n=n dt,

 ||R_N[u^n]-u_N(t_n)||_L1 <= 2 ||u_N^0-U_k||_L1.           (2)

Proof. Same-source scalar entropy solutions are L1 contractive on the torus;
the additive smooth-in-space source cancels in the doubling-of-variables
comparison. For continuous h this follows also by smooth-source approximation;
for fixed N the source is bounded and continuous, and the flux is C1 and
Lipschitz on the bounded states under consideration. U_k is a stationary
classical entropy solution. Thus ||u_N(t)-U_k||_1<=||u_N^0-U_k||_1. Theorem 1(d),
(1), and |average(v)|<=average(|v|) give the same bound for R_N[u^n]. The triangle
inequality proves (2). QED.

Thus families with initial L1 distance eta_N from a single strict-gap
micro-equilibrium have all-time reconstruction error <=2 eta_N, with no N in
the constant and no requirement d_i << 1/N. This is a useful prepared-data
stability result, NOT a consistency rate in d_i or dt for fixed nonzero
perturbations. It does not establish uniform accuracy for general O(1)
macroscopic prepared profiles, arbitrary transients, or resonance crossings.
At eta_N=0 it reduces to exact well balancing.

## Approach 3: complete critical BV classification in the quadratic example

Take f(u)=u^2/2, H(y)=1-cos(2 pi y), and N in the positive integers. A bounded
stationary weak solution has u^2/2-H(Nx)=C a.e. For C=0 write
 a_N(x)=2|sin(pi N x)|.

**Theorem 3.** Up to equality almost everywhere, all BV stationary entropy
solutions with C=0 are parameterized by theta=(theta_0,...,theta_{N-1}) in
[0,1]^N. On the microcell k/N<x<(k+1)/N, write y=Nx-k and set

 U_theta(x)= +2 sin(pi y) for 0<y<theta_k,
             -2 sin(pi y) for theta_k<y<1.

Endpoint values and jump-point values are immaterial. In particular these
solutions form a continuum, not merely 2^N states. Their microcell integrals
and total means are

 integral_{k/N}^{(k+1)/N} U_theta = -4 cos(pi theta_k)/(pi N),
 integral_T U_theta = -(4/(pi N)) sum_k cos(pi theta_k).     (3)

Proof. On any compact subinterval of an open microcell, a_N is bounded away
from zero. Thus s=U/a_N is BV there and takes only the values +/-1. A one-
dimensional BV two-valued function has finitely many switches on each such
compact subinterval. Every switch has equal-flux traces. For a stationary
jump from +a to -a, Kruzkov entropy production at a constant state r between
-a and a equals 2(f(r)-f(a))<=0; an upward switch has the opposite positive
production for r=0 and is forbidden. Thus only downward switches occur.
There cannot be two downward switches without an intervening upward switch;
local compact classification and exhaustion give at most one switch in the
whole open microcell, including pure signs as endpoint parameters. At
microcell endpoints a_N=0, so both traces are zero and there is no entropy
jump. Conversely each displayed profile is BV, solves the stationary flux
identity, and has only entropy-admissible downward shocks. On its smooth
pieces the balance-law entropy equality holds (also distributionally through
continuous zero joins); the preceding jump calculation gives the entropy
inequality everywhere. Elementary integration proves (3). QED.

The theta_k in {0,1} subfamily is exactly the previously constructed 2^N
Lipschitz sign family. For even N it has binomial(N,N/2) mean-zero members,
but this counts only that discrete subfamily. A single microcell's average
uniquely determines its theta_k; this agrees with the primary-source
unique-minimum microperiodic classification. Arbitrary microcell choices on
the larger torus are not necessarily one-microperiodic.

## Approach 4: an observation-specific lower bound, not a universal claim

**Theorem 4.** Let N be even and choose the mesh with N/2 cells
I_j=[2j/N,(2j+2)/N]. There are two stationary Lipschitz entropy profiles U and
V=-U such that every mesh cell average of both is zero, yet

 ||U-V||_L1(T)=8/pi.

For every deterministic reconstruction or simulation output W that depends
only on these initial cell averages, the known PDE, this mesh and time, at
least one of the two stationary inputs has L1 error at least 4/pi, at every
time at which the same W is used for the indistinguishable inputs.

Proof. Take alternating signs +,-,+,-,... in the Lipschitz subfamily and
reverse all signs for V. Every pair of microcells has zero signed integral.
Since |U|=a_N, ||U-V||_1=2 integral_T a_N=8/pi. The data supplied to the
algorithm are identical, so its output W is identical for both inputs.
Triangle inequality gives max(||W-U||_1,||W-V||_1)>=4/pi. QED.

More generally the same pair is indistinguishable on aligned cells containing
an even number of microcells. No claim is made for arbitrary meshes. The
bound concerns recovery of the microscopic L1 state, not accuracy of coarse
cell averages (which can be exactly correct), weak limits, or supplied
branch/phase information. It does not prove that a particular data structure
must store one bit per microcell. The maximum statement is pointwise in time;
it does not assert a single worst-case input for all times simultaneously.

## Approach 5: quadrature control and its underresolution obstruction

Theorems 1-2 separate exact analysis from practical integration. A positive
normalized quadrature map

 Q_i(C)=sum_r w_ir phi_sigma(C+H(N x_ir)), w_ir>=0, sum_r w_ir=1,

has the same derivative sign and |Q_i'|>=1/L on the branch band. Replacing E
by Q therefore retains Theorem 1 with D_i replaced by Q_i([Cmin,Cmax]), including
exact preservation of its OWN quadrature equilibria. It does not automatically
preserve the exact PDE cell averages.

Suppose |Q_i(C)-E_i(C)|<=delta_i throughout the band, fix k in it, and assume
the exact equilibrium inputs E_i(k) lie in the Q-domain. The recovered
constants c_i=Q_i^{-1}(E_i(k)) satisfy |c_i-k|<=L delta_i, by the inverse
Lipschitz estimate and Q_i(k)-E_i(k). One step applied to these exact PDE
averages therefore has weighted stationarity defect

 sum_i d_i |u_i^1-E_i(k)| <= 2 dt L sum_i delta_i.          (4)

Indeed each residual is dt times a difference of neighboring c_i, and cyclic
summation gives at most twice the sum of |c_i-k|. Repeated use of contraction
against this fixed reference gives <=2 t_n L sum_i delta_i for n steps, PROVIDED
the exact reference belongs to the Q-domain; iterates stay there by Theorem 1.
This is a defect estimate, not a claim of a useful uniform quadrature rate.

Fixed unresolved samples do not give vanishing delta_i uniformly in N. For
one torus cell, integer N, positive branch and any C>0, endpoint quadrature at
x=0 gives Q(C)=sqrt(2C), whereas

 E(C)=integral_0^1 sqrt(2(C+1-cos(2 pi y))) dy > sqrt(2C).

The positive discrepancy is independent of N. In this one-cell example the
update still vanishes by periodic conservation, so it diagnoses inaccurate
reconstruction/averages, NOT a nonzero update. With phase-dependent quadrature
errors on multiple cells, (4) quantifies the possible failure of exact balance.
Phase-aware integration, complete-period precomputation plus partial-period
integrals, or a proved quadrature bound is necessary before asserting numerical
preservation of the true micro-equilibrium.

## Five-approach outcome and remaining boundary

1. Exact branch upwinding closes domain, monotonicity, CFL and contraction gaps.
2. PDE contraction gives an N-uniform but narrowly near-equilibrium bound.
3. Entropy-shock classification corrects the finite critical-equilibrium count.
4. A specified mesh and observation map give a sharp two-input lower bound.
5. Positive quadrature preserves a modified family; explicit aliasing and a
   residual bound delimit claims about true exact averages.

None supplies a general epsilon-uniform transient convergence theorem through
resonance. The original broad workshop objective is not given a solved/unsolved
binary by these results. Suitable next work would require a specified target
norm and data class, a representation carrying necessary microscopic data,
and separate consistency/entropy/convergence analysis. We do not claim global
novelty; the main contribution here is a rigorous, reproducible scoped audit.
