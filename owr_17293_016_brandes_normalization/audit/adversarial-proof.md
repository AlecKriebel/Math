# Independent adversarial proof audit

Date: 2026-09-23 UTC. Scope: the candidate argument supplied in the task, audited independently by direct derivation. This note does not establish bibliographic priority or independently authenticate the original problem statement.

**Verdict:** the mathematical argument is correct for positive-definite real homogeneous polynomials of positive degree, provided the requested coefficients are the symmetric tensor coefficients in the ordered-index expansion. No unresolved logical gap was found. Its result is stronger than the weak inequality: the basis can be chosen so that every tensor coefficient is positive and every mixed coefficient satisfies the inequality strictly. The paper should explicitly state `m >= 1` and even `d >= 2`.

Completion estimate for this proof-verification subtask: **100%**. This is a mathematical audit, not a formal proof-assistant certificate and not an assessment of priority.

## Exact claim checked

Let `m >= 1`, let `d >= 2` be an integer, and let `A` be a real symmetric `d`-linear form on `R^m` with `psi(x)=A(x,...,x)>0` for every nonzero `x`. Then `d` is even. There is an invertible linear map `S` with columns `x_1,...,x_m` such that, for each ordered tuple `J=(j_1,...,j_d)`,

\[
0<A(x_{j_1},\ldots,x_{j_d})\le
\prod_{r=1}^d\psi(x_{j_r})^{1/d}.
\]

The inequality is strict when the tuple contains at least two distinct indices. This implies the stated absolute-value inequality.

## Independent derivation without logarithms

Choose a unit vector `v` minimizing `psi` on the auxiliary Euclidean unit sphere. Compactness and positive definiteness imply `c=psi(v)>0`. Replace `A` and `psi` by `A/c` and `psi/c`. This leaves the desired inequality invariant, and gives `psi(v)=1`.

For `u` perpendicular to `v`, differentiate the sphere curve `cos(s)v+sin(s)u` for unit `u`. Its first derivative at zero is zero and its second derivative is nonnegative. Thus

\[
A(v^{d-1},u)=0,\qquad
Q(u,u):=A(v^{d-2},u,u)\ge\frac{|u|^2}{d-1}.
\tag{A1}
\]

The second formula follows exactly from

\[
0\le d(d-1)A(v^{d-2},u,u)-d A(v^d).
\]

This establishes strict positivity of `Q` on `v^perp`; a strict minimum or a nondegenerate constrained minimum is not needed. The positive radial value itself supplies the lower bound, including when the restriction of `psi` to the sphere is constant.

Choose an orthonormal basis `u_1,...,u_{m-1}` of `v^perp`, set `w_i=u_i` for `i<m`, and set `w_m=0`. Put `x_i(epsilon)=v+epsilon w_i`. For every nonzero `epsilon` these vectors form a basis: tangent projection of any linear relation forces the first `m-1` coefficients to vanish; radial projection then forces the last coefficient to vanish.

Fix an ordered tuple `J`, and abbreviate `a_r=w_{j_r}`. Each `a_r` is tangent, so its linear term vanishes. Multilinearity gives

\[
N_J(\varepsilon):=A(v+\varepsilon a_1,\ldots,v+\varepsilon a_d)
=1+\varepsilon^2\sum_{r<s}Q(a_r,a_s)+O(\varepsilon^3),
\]

\[
P_J(\varepsilon):=\prod_{r=1}^d\psi(v+\varepsilon a_r)
=1+\binom d2\varepsilon^2\sum_r Q(a_r,a_r)+O(\varepsilon^3).
\]

Consequently the following polynomial has the indicated leading term:

\[
\begin{aligned}
F_J(\varepsilon)&:=P_J(\varepsilon)-N_J(\varepsilon)^d\\
&=\frac d2\varepsilon^2\sum_{r<s}
Q(a_r-a_s,a_r-a_s)+O(\varepsilon^3).
\end{aligned}
\tag{A2}
\]

The identity uses only symmetry and the fact that every diagonal term appears in exactly `d-1` unordered pairs. It independently confirms the sign and factor in the candidate's normalized logarithmic expansion.

If `J` is pure, `F_J` is identically zero. If `J` is mixed, at least one difference is nonzero and tangent, so (A1) makes the quadratic coefficient in (A2) strictly positive. Therefore `F_J(epsilon)>0` for all sufficiently small nonzero `epsilon`. There are only finitely many tuples, so a single positive `epsilon` works for all mixed tuples. Since `d` is even and `P_J>0`, `F_J>=0` is equivalent to `|N_J|<=P_J^(1/d)`. Continuity of the finitely many `N_J`, all equal to one at zero, also gives `N_J>0` after further shrinking `epsilon`.

This proves the entire asserted inequality, including its absolute value and simultaneous quantifier. No numerical evidence or unsupported auxiliary theorem is required.

## Check of the candidate's general Taylor identity

For arbitrary perturbations define `L(a)=A(v^(d-1),a)`, `Q(a,b)=A(v^(d-2),a,b)`, and `B=Q-L tensor L`. If `a=alpha v+u` with `u` tangent, then `L(a)=alpha` and `B(a,a)=Q(u,u)`. Hence `B` is positive semidefinite with kernel exactly `R v`.

The logarithm of the numerator has quadratic coefficient

\[
\sum_{r<s}Q(a_r,a_s)-\tfrac12\left(\sum_r L(a_r)\right)^2.
\]

The logarithm of the geometric-mean denominator has quadratic coefficient

\[
\tfrac{d-1}{2}\sum_r Q(a_r,a_r)-\tfrac d2\sum_rL(a_r)^2.
\]

Their difference is

\[
-\tfrac12\sum_{r<s}B(a_r-a_s,a_r-a_s).
\]

Thus the candidate's displayed key identity, including its factor `1/2`, is correct. Taking logarithms is justified in a neighborhood of zero because every quantity has value one at zero. A separate positive neighborhood for each tuple suffices, because the final family is finite.

## Falsification attempts and scope checks

- **Flat sphere minimum:** not a counterexample. For `psi(x)=|x|^d`, the constrained Hessian may vanish, but (A1) still gives `Q(u,u)=|u|^2/(d-1)>0`.
- **Quadratic degree:** `d=2` is covered without alteration. The result is also a special case of Cauchy–Schwarz for a positive-definite quadratic form. The logarithmic remainders remain legitimate even though the underlying polynomial has degree two.
- **One variable:** `m=1` has no mixed tuples, and the unique basis vector gives equality. The orthonormal tangent list is empty, and the independence argument still works.
- **Odd degree:** excluded by `psi(-x)=(-1)^d psi(x)` and positivity at both `x` and `-x`.
- **Degree zero:** a positive constant would satisfy a bare positivity definition, but the requested `1/d` inequality is undefined. State positive degree explicitly; this is a domain clarification, not a gap for the intended problem.
- **Semidefinite forms:** the proof does not establish this extension. The sphere minimum can be zero, and division by `c` as well as strict tangent coercivity then fail. No semidefinite claim should be inferred.
- **Conditioning:** the constructed basis approaches a singular matrix as `epsilon` tends to zero, but it is invertible for every nonzero `epsilon`. This is permitted by an unrestricted `GL_m(R)` change. The proof gives no uniform bound on the condition number.
- **Signs:** coefficients can be kept positive by continuity. Even without that extra fact, (A2) proves the absolute-value inequality because `d` is even.
- **Uniformity:** no compactness over infinitely many perturbations is asserted or needed. There are exactly `m^d` ordered tuples; taking a finite minimum of their admissible positive thresholds closes the quantifier correctly.
- **Scaling:** replacing `psi` by `psi/c` scales both sides of each desired inequality by `1/c`, so the normalization is harmless.
- **Coefficient convention:** for the expansion `psi(t)=sum_(j_1,...,j_d) n(j_1,...,j_d)t_(j_1)...t_(j_d)` with symmetric `n`, one has `n(j_1,...,j_d)=A(e_(j_1),...,e_(j_d))`. For the ordinary monomial expansion `psi(t)=sum_alpha c_alpha t^alpha`, the relation is `c_alpha=binomial(d,alpha)n_alpha`. Omitting this multinomial factor would change the claim and invalidate the identification. The source statement must therefore be checked against the symmetric ordered-index convention.
- **General local-maximum wording:** the proof establishes strict decay along each fixed genuinely mixed transverse configuration. That is exactly what is needed for the finite basis construction. Broader neighborhood assertions about arbitrary varying configurations should not be used without an additional argument.

## Optional explicit remainder certificate

In the chosen tangent construction, every two distinct `w_i` have squared distance at least one. A mixed tuple has at least `d-1` unequal unordered pairs. It follows from (A1) that the sum in (A2) is at least one, so the coefficient of `epsilon^2` in `F_J` is at least `d/2`.

Write the exact polynomial `F_J=sum_(k=2)^(d^2) f_(J,k) epsilon^k`, and set `M=max_J sum_(k=3)^(d^2)|f_(J,k)|` over mixed tuples. For `0<epsilon<=1`, the tail has absolute value at most `M epsilon^3`. If `M>0`, choosing `epsilon<=min(1,d/(4M))` guarantees `F_J(epsilon)>=d epsilon^2/4` for all mixed tuples. If `M=0`, any `0<epsilon<=1` suffices for these inequalities. This optional bound is finite and checkable once the normalized minimizer and tangent basis are specified; it is not necessary for the existence proof.

## Remaining work outside this audit

Authenticate the exact source problem and its allowed coordinate changes; complete a dated priority search; check consistency of final prose, source files, metadata, and any computational verifier. None of these bibliographic or publication tasks changes the verified mathematical derivation above.
