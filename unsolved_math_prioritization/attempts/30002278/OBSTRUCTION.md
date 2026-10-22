# Variable acoustic PML: obstruction to the displayed Lyapunov family

**Broad target unresolved; two approaches used.** We prove that the specific
parameterized functional displayed in the original report cannot be made
nonincreasing for all admissible smooth initial states under a certain smooth
nonnegative damping profile. This is an obstruction to that functional family,
not a proof of PDE instability or of nonexistence of every Lyapunov functional.
Separate adversarial review is pending. No historical novelty is claimed.

## 1. Primary formulation and the source-scope correction

The full relevant contribution is Manfred Kaltenbacher's *Stability Analysis of
Time-Domain PML*, joint with Barbara Kaltenbacher, printed pp.196–200 of
[OWR 03/2013](https://ems.press/journals/owr/articles/12331). The equations on
p.197 are

\[
 c^{-2}p_{tt}+\alpha p_t+\beta p+\gamma v-\Delta p-\nabla\cdot u=0,
 \quad u_t+Au+B\nabla p-C\nabla v=0,\quad v_t=p, \tag{1}
\]

where, writing \((\sigma_1,\sigma_2,\sigma_3)=(\sigma_x,\sigma_y,\sigma_z)\),

\[
 \alpha=c^{-2}\sum_i\sigma_i,\quad
 \beta=c^{-2}\sum_{i<j}\sigma_i\sigma_j,\quad
 \gamma=c^{-2}\sigma_1\sigma_2\sigma_3,
\]
\[
 A=\operatorname{diag}(\sigma_i),\quad
 B_{ii}=\sigma_i-\sum_{j\ne i}\sigma_j,\quad
 C_{ii}=\prod_{j\ne i}\sigma_j. \tag{2}
\]

The reduced model, rPML, sets C to zero. This changes the full three-dimensional
model in regions with multiple active profiles; it must not be silently substituted
for full PML. Our test is supported in a single active face, where C already
vanishes, so the distinction does not affect the local calculation.

The referenced [Kaltenbacher–Kaltenbacher–Sim paper](https://doi.org/10.1016/j.jcp.2012.10.016),
Section 3, uses homogeneous Dirichlet conditions on p and v on the outer bounded
domain. The stated stability theorem imposes zero initial auxiliary vector u,
without requiring all initial pressure data to be in the physical region. We use
smooth, compactly supported pressure data **inside a layer**, with p_t(0)=0 and
u(0)=v(0)=0. A more restrictive task allowing initial data only in the physical
region is not settled by this test. All states below are unforced and satisfy
the homogeneous boundary conditions for the short time needed.

On p.198 the report displays, with fixed space-dependent parameters δ and
nonnegative diagonal F,

\[
\begin{split}
 2\eta_{\delta,F}={}&\|c^{-1}p_t\|^2+\|\nabla p\|^2+\|F^{1/2}u\|^2
 +\|(\beta+\alpha\delta)^{1/2}p\|^2+\|(\gamma\delta)^{1/2}v\|^2\\
 &-\|C^{1/2}\nabla v\|^2+2\langle\gamma v,p\rangle
 +2\langle u,\nabla p\rangle+2\langle\delta c^{-2}p_t,p\rangle.
\end{split} \tag{3}
\]

It proposes 0≤δ≤c²α and pointwise algebraic matrix conditions, but then
explicitly flags the uncontrolled spatial-variation term. Thus the earlier
published stability assertion cannot simply be reused as a variable-profile
solution. The pinned record's “original statement” extracts a step of that
proposed argument, while its cleaned statement asks more broadly for a
nonincreasing functional uniformly controlling acoustic energy. We keep that
broader request unresolved rather than equating it with (3).

## 2. Approach 1: every allowed choice in (3) fails for one profile

Set c=1. Consider a rectangular face patch U where

\[
 \sigma_1=s(x)>0,\qquad\sigma_2=\sigma_3=0,
\]

with s smooth and depending on its own coordinate only. Then
\(\alpha=s,\beta=\gamma=0,A=\operatorname{diag}(s,0,0)\),
\(B=\operatorname{diag}(s,-s,-s)\), C=0. All initial data used in this section
have compact support in U, so coefficients and parameter choices outside U
contribute nothing to the derivative at time zero.

**Scoped proposition.** There is a smooth bounded nonnegative coordinate damping
profile, zero in an adjoining physical region, such that no bounded,
time-independent parameters δ,F in (3), satisfying the source's 0≤δ≤c²α and
F≥0, make (3) nonincreasing for every smooth compatible solution with zero
initial auxiliaries. The profile can be chosen monotone in its active face.
This statement concerns exactly family (3).

### 2.1 Zero-auxiliary initial derivative and necessity of δ=s

Let p(0)=f and p_t(0)=h be smooth compactly supported in U, and set u(0)=v(0)=0.
Equation (1) gives

\[
 p_{tt}(0)=\Delta f-sh,\qquad
 u_t(0)=(-sf_x,sf_y,sf_z).
\]

Differentiating (3) and integrating the term hΔf by parts gives

\[
 \eta'_{\delta,F}(0)=
 \int_U\big[(\delta-s)h^2-sf_x^2+sf_y^2+sf_z^2+\delta f\Delta f\big]. \tag{4}
\]

Every F term vanishes because u(0)=0. Formula (4) requires only bounded δ;
no derivative of δ is taken. The potentially troublesome terms sδfh cancel
exactly. For differentiable δ the final term can instead be integrated by parts,
exhibiting \(-\int f\nabla\delta\cdot\nabla f\).

The source already imposes δ≤s on U. If δ<s on a set of positive measure,
choose a real χ∈C_c^∞(U) for which
\(J=\int_U(s-\delta)\chi^2>0\). Such a χ exists by positivity and density.
Use h=0 and \(f_N=\chi\cos(Ny)\). In (4), the terms of order N² are

\[
 N^2\int_U\chi^2[s\sin^2(Ny)-\delta\cos^2(Ny)],
\]

and all other terms are O(N), since χ,s,δ are fixed and bounded on this compact
support. The Riemann–Lebesgue lemma for the integrable coefficient functions
therefore gives

\[
 \lim_{N\to\infty}N^{-2}\eta'_{\delta,F}(0)=\tfrac12J>0. \tag{5}
\]

Hence monotonicity for all such data forces δ=s almost everywhere on U. This
necessity does not assume any particular choice of F or the additional algebraic
matrix conditions. If the restriction δ≤s were dropped, setting f=0 in (4)
would first force it back, by arbitrary compactly supported h.

### 2.2 The forced value has a positive derivative

For δ=s, h=0, formula (4) becomes

\[
 \eta'_{s,F}(0)=-2\int_U s f_x^2-\int_U s'ff_x.
 \tag{6}
\]

Transverse derivative terms cancel. Where s(x)=x², an integration by parts gives

\[
 \eta'_{s,F}(0)=\int_U[f^2-2x^2f_x^2]. \tag{7}
\]

Choose ε=2⁻¹⁶ and first consider the scalar H₀¹(ε,1) test function

\[
 a_\varepsilon(x)=\frac{(1-x)(1-\varepsilon/x)}{\sqrt x}.
\]

Its endpoint traces vanish, and ε>0 keeps its derivatives finite on the closed
interval. Direct integration yields

\[
\begin{split}
 I_\varepsilon
 &=\int_\varepsilon^1(a_\varepsilon^2-2x^2(a_\varepsilon')^2)\,dx\\
 &=\tfrac72(\varepsilon^2-1)
   +(\tfrac12\varepsilon^2+6\varepsilon+\tfrac12)\log(1/\varepsilon).
\end{split} \tag{8}
\]

For ε=2⁻¹⁶, \(\log(1/\varepsilon)=16\log2\). The elementary positive series
\(\log2=2\sum_{j\ge0}[(2j+1)3^{2j+1}]^{-1}>2/3\) shows

\[
 I_\varepsilon>
 -\tfrac72+\tfrac12\,16\,\tfrac23=\tfrac{11}{6}>0. \tag{9}
\]

The quadratic form in (8) is continuous in H¹(ε,1). Since C_c^∞(ε,1) is dense
in H₀¹(ε,1), there exists a real a∈C_c^∞(ε,1) with the same quadratic form
strictly positive. Choose any nonzero real b∈C_c^∞ in the transverse face
rectangle, normalized by \(\int b^2=1\), and set f(x,y,z)=a(x)b(y,z).
Then (7) is strictly positive. These are smooth compactly supported data, not
a singular limiting state. Equations (5)–(9) prove the scoped proposition for
all allowed δ,F.

### 2.3 Profile, boundary conditions, and existence of the test solution

For example, choose a rectangular computational box containing
[−1,2]×[−1,1]², with an interface x=0 and an interior face patch containing
(ε,1)×supp(b). Take s(x)=0 for x≤0 and s(x)=x² for x≥ε/2 within that face.
A smooth nondecreasing transition is obtained by multiplying x² by a smooth
nondecreasing cutoff which is zero for x≤0 and one for x≥ε/2. Extend s smoothly
and boundedly outside the box when constructing a whole-space local solution.
Other face profiles may be zero, or may turn on near distant y,z boundaries;
they vanish on a neighborhood of the data support. Thus this is a legitimate
local part of a Cartesian layer with nonnegative coordinate-dependent damping.

For completeness, smooth short-time solutions are available without assuming
the disputed Lyapunov estimate. In the one-face region define

\[
 q=p_t+sp,\qquad r=\nabla p+u,\qquad w=u_1.
\]

The equations become

\[
 \begin{array}{ll}
 q_t=\nabla\cdot r,&p_t=q-sp,\\
 (r_1)_t=q_x-2sr_1+sw-s'p,&w_t=-sr_1,\\
 (r_2)_t=q_y,&(r_3)_t=q_z.
 \end{array} \tag{10}
\]

The q,r principal block is the usual symmetric first-order wave system; p,w
are ODE components. All remaining coefficients are smooth bounded multiplication
operators. The free wave evolution plus a bounded-perturbation Duhamel/Picard
construction gives a smooth local solution for smooth compact data, with finite
propagation speed. Start with q(0)=h+sf, r(0)=∇f, w(0)=0, p(0)=f. Defining
u=r−∇p recovers (1): the difference w−u₁ obeys
\((w-u_1)_t=-s(w-u_1)\) with zero initial value; the transverse equations give
\((u_2)_t=sp_y,(u_3)_t=sp_z\). Set \(v(t)=\int_0^t p(\tau)d\tau\).

Take time smaller than the positive distance of the initial support from the
edge of the face patch and from the outer boundary. Finite propagation then
keeps the solution inside that patch, so it also solves the full coefficients
extended outside, and p=v=0 near the outer boundary. This justifies the
Dirichlet compatibility and the computed positive right derivative of an actual
solution. No numerical unstable mode or long-time growth assumption is used.

## 3. Approach 2: established state augmentation leaves the same remainder

The natural local transformation in (10) suggests

\[
 H=\tfrac12\int(q^2+|r|^2+w^2).
\]

Its exact smooth-solution balance, with zero boundary flux, is

\[
 H'=-2\int s r_1^2-\int s'pr_1. \tag{11}
\]

To check (11), multiply (10) by q,r,w. The q,r derivative terms form the
boundary flux div(qr), and the terms swr₁ cancel. Only the displayed damping
and profile-gradient terms remain. In original variables H is precisely (3)
on this face with δ=s and F=diag(2,1,1). These parameters even saturate all the
report's pointwise algebraic matrix inequalities, yet (7) makes H increase for
the constructed data.

The profile-gradient issue is **known prior work**, not a new mechanism. In
[Baffet–Grote–Imperiale–Kachanovska (2019)](https://doi.org/10.1007/s10915-019-01089-9),
Theorem 2.2 proves a decreasing augmented energy for constant coefficients.
Their Remarks 2.1 and 2.3 explicitly retain the additional term involving the
gradients of the coefficient sum, pairwise products and triple product. On a
single active face that term is exactly the second term in (11). Their integrated
auxiliary variables, with zero initial auxiliaries as here, reduce to this same
face energy. Remark 2.4 similarly retains an interface contribution for a
piecewise-constant profile. The published theorem is not a general
variable-coefficient monotonicity result.
Their physical application also specifies zero initial data inside the layer.
The layer-supported test here is not a counterexample within that more restricted
initial-data class, nor a counterexample to their constant-coefficient theorem.

This attempted augmentation therefore does not resolve the remaining problem.
A Gronwall bound allowing exponential growth, or a semigroup well-posedness
estimate, is weaker than a nonincreasing functional uniformly controlling the
requested acoustic energy. Changing the PML equations by deleting additional
couplings is also a different problem.

## 4. Exact gap and disposition

The result is an explicit obstruction to choosing the **displayed** δ,F family,
for general initial states allowed in the cited energy formulation. It does not
prove any of the following:

- that solutions are unbounded or unstable
- that no differently weighted, derivative-dependent, nonlocal, or further
  augmented functional can be nonincreasing and coercive
- that the same initial increase is reachable when every initial pressure state
  is required to be supported only in the physical region
- that uniform long-time stability fails for the full variable-profile PML

The unfilled step is to construct such a more general coercive monotone
functional for the exact original equations and intended initial/boundary class,
or to prove a genuine dynamical obstruction that rules it out. No such step was
obtained. Thus the broad source target remains **unsolved**, with two approaches
recorded and no novelty claim.

The [exact standard-library checker](verify_obstruction.py) validates the energy
balance algebra, the initial derivative, the saturated algebraic inequalities,
and the rational-plus-logarithmic integral in (8), including a rigorous rational
positive lower bound. It does not replace the function-space, high-frequency or
local-existence arguments, and it does not infer PDE instability. Run
`python3 verify_obstruction.py` and compare [verification.json](verification.json).
