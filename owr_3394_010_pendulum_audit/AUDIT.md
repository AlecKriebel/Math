# Verification of the normalized damped-pendulum candidate

## Decision and scope

**Mathematics: affirmative, using the published Angeli–Praly theorem.** The
candidate's calculations are correct, and its conclusion has the quantifiers
asked for in the 2009 problem. Add a fixed positive margin when converting the
limsup estimate to eventual confinement. This is a minor rigor clarification,
not an obstruction to the conclusion.

**Priority: fails for a new resolution.** The imported paper explicitly solves
this pendulum problem, using the same Lyapunov-function mechanism. Its 2010
conference version also treats the problem. The supplied candidate itself
acknowledges this prior work. This audit does not establish a new theorem or an
independent proof of the imported general theorem.

## Exact claim and original source

On the standard product cylinder \(M=S^1\times\mathbb R\), consider

\[
\dot\theta=\omega,\qquad \dot\omega=-\sin\theta-\omega+d(t).
\]

Write \(r(x)=\sqrt{\operatorname{dist}_{S^1}(\theta,0)^2+\omega^2}\).
The target is

\[
\exists\gamma\in\mathcal K\quad\forall d\in L^\infty([0,\infty))
\quad\exists B_d\subset M:\quad\mu(B_d)=0,\qquad
x_0\notin B_d\Longrightarrow\limsup_{t\to\infty}r(x(t))
\le\gamma(\|d\|_\infty).
\]

Inputs are Lebesgue measurable and fixed independently of the initial state;
the exceptional set may depend on the whole input. The gain is continuous,
zero at zero, and strictly increasing. The original report p. 671, equations
(4)–(5), gives these quantifiers and exactly this normalized differential
equation. It does not ask for a common exceptional set for all inputs or a
uniform transient ISS estimate. See [SOURCES.md](SOURCES.md).

## Direct checks

Let \(w=\omega\), \(s=\sin\theta\), \(c=\cos\theta\), and

\[
H=\tfrac12w^2+1-c,\qquad V=H+\tfrac12ws.
\]

The following exact identities are convenient certificates:

\[
V-\tfrac12H=\tfrac14(w+s)^2+\tfrac14(1-c)^2,
\qquad
\tfrac32H-V=\tfrac14(w-s)^2+\tfrac14(1-c)^2.
\]

Thus \(H/2\le V\le3H/2\). Both are nonnegative and proper: the angle
factor is compact, and bounded sublevels bound \(|w|\). They are smooth,
including across a choice of angular coordinate cut.

For the unforced vector field, direct differentiation gives

\[
-\dot V=\tfrac14(w^2+s^2)+\tfrac14(w+s)^2+
\tfrac12(1-c)w^2\ge\tfrac14(w^2+s^2).
\]

It is strictly positive away from the two equilibria \((0,0)\) and
\((\pi,0)\). In particular, the energy \(H\) alone would not supply this
strictness; the cross term is doing necessary work.

The state Jacobian is

\[
\begin{pmatrix}0&1\\-\cos\theta&-1\end{pmatrix}.
\]

At the downward equilibrium the eigenvalues are
\((-1\pm i\sqrt3)/2\), so it is locally exponentially asymptotically
stable. At the upright equilibrium they are \((-1\pm\sqrt5)/2\), giving
one strictly positive and one negative eigenvalue. The latter equilibrium is
an isolated hyperbolic saddle. The asymptotically stable set is exactly
\(E_s=\{(0,0)\}\).

For forced solutions, almost everywhere,

\[
\dot H=-w^2+wd,\qquad
-\tfrac12H+1+\tfrac12d^2-\dot H
=\tfrac12(w-d)^2+\tfrac14w^2+\tfrac12(1+c)\ge0.
\]

With \(D=\|d\|_\infty\), scalar comparison yields

\[
H(t)\le e^{-t/2}H(0)+(2+D^2)(1-e^{-t/2}).
\]

The smooth lifted vector field on \(\mathbb R^2\) is globally Lipschitz
in the state and has at most linear growth for bounded input. Standard
Carathéodory existence and uniqueness therefore apply. The displayed bound
prevents finite-time escape. The same argument using the input's bound on
each finite interval handles locally essentially bounded inputs.

To check the published *eventual-confinement* hypothesis, choose a time after
which \(e^{-t/2}H(0)\le1\). Then \(H(t)\le3+D^2\) for all later times,
and therefore

\[
r(x(t))\le\sqrt{\pi^2+6+2D^2}
\le\sqrt{\pi^2+6}+\sqrt2D.
\]

This is an eventual bound of the required constant-plus-class-K form, with
constants independent of the input and initial state. Merely writing a
limsup bound with no margin would not by itself show eventual confinement
inside the closed ball of that same radius. The candidate's original
limsup estimate \(\sqrt{\pi^2+4+2D^2}\) is nevertheless correct.

## Imported step and exceptional sets

Angeli–Praly Proposition 2 combines assumptions A0–A2, finitely many stable
equilibria, and ultimate boundedness to give almost-global ISS. Here A0 holds
because the cylinder is smooth, connected, orientable, and boundaryless, with
input space \(\mathbb R\) closed and a smooth jointly Lipschitz vector
field. The strict proper function and saddle classification establish A1–A2;
the preceding estimates establish the remaining hypotheses. Their Definition
1 has the required input-dependent null set. A half-line input may be extended
by zero to negative times without changing its norm. Hence the claimed
class-K asymptotic gain follows. If necessary, adding the identity function
to a nondecreasing gain makes it strictly increasing.

The essential imported fact is robustness of the saddle's thin exceptional
set under small time-dependent forcing. The energy estimates alone do not
prove this. The candidate's null-set discussion is an explanation of that
theorem, not a substitute proof. It applies the local result only to
sufficiently small inputs; larger inputs are handled by ultimate boundedness
and enlargement of the gain.

For clarity, globalization causes no additional gap here. For \(D\le1\),
the energy bound brings any compact set of initial states uniformly into
\(H\le4\). Such a set lies inside the proper sublevel \(V\le7\), whose
boundary contains neither equilibrium. Proposition 1 applies there for
sufficiently small inputs. The finite-time flow is a diffeomorphism, with
Jacobian determinant \(e^{-(t-t_0)}\); its inverse preserves null sets
locally. Taking inverse images at entry times and then a countable union
over a compact exhaustion preserves zero area. The uniform entry statement
here follows from the explicit bound, rather than from pointwise convergence
alone.

One can also make gain stitching continuous explicitly. Let \(\beta\) be
the small-input class-K gain and choose \(\delta>0\) below its amplitude
threshold and below 1. With \(C=\sqrt{\pi^2+6}\), the function

\[
G(u)=\beta(u)+(C+\sqrt2u)\min\{1,u/\delta\}
\]

is continuous, strictly increasing (or can be made so by adding \(u\)),
vanishes at zero, dominates the small-input gain when \(u\le\delta\),
and dominates the global limiting bound when \(u\ge\delta\).

## Boundary checks and verification limits

- **Zero input:** the upright equilibrium and its stable manifold must be
  excluded; otherwise a gain vanishing at zero is impossible.
- **Small constant input:** equilibria move. This is compatible with a gain
  tending to zero and an input-dependent exceptional set.
- **Large or switching inputs:** the energy estimate uses only an essential
  bound and an almost-everywhere differential inequality, not input continuity.
- **State space:** the angle is modulo \(2\pi\). No claim is made about an
  unwrapped angle on \(\mathbb R\), which can rotate without bound. Standard
  chordal and geodesic distances on the circle are comparable, so their product
  metrics only change the gain by a constant factor.
- **Quantifiers:** changing the input to state feedback, requiring a universal
  exceptional set, or demanding a full transient estimate is outside this claim.
- **Computer verification:** `verification/verify.py` checks exact rational
  polynomial identities, with a deliberately false identity as a negative
  control. It does not certify the imported theorem, source chronology,
  measure theory, or all trajectories by numerical sampling.

No mathematical obstruction to this citation-dependent proof was found.
This is not a formal proof-assistant certification or a new derivation of the
general Angeli–Praly theorem. The independent reviews document additional
adversarial checks and the exact scope of acceptance.

## Priority and publication decision

The direct antecedent is Angeli–Praly's *Stability Robustness in the Presence
of Exponentially Unstable Isolated Equilibria*. The journal paper identifies
the 2009 Oberwolfach problem and applies its theorem to the pendulum; the
conference version appeared in CDC 2010. The journal front matter states
online publication on December 6, 2010, with the July 2011 issue date.

This is sufficient to reject a new-resolution priority claim; no exhaustive
claim about the earliest private discovery is needed or made. The normalized
coefficient choice and explicit algebra checks do not establish a separate
novel contribution.

Accordingly, the condition for the requested resolution paper, GitHub Pages
site, and Zenodo upload package fails. Only this verification record is
prepared and committed. No release, DOI deposit, or outreach is performed.
