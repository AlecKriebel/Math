# Exact-byte hostile audit of the workload-only physical-time Foster lemma

**Independent proof replay, 2026-08-12 PDT.**  The immutable target of this
audit is

~~~text
research_notes/proof_first_levelset_h_alone_physical_time_foster_lemma.md
SHA-256 8cf2a8d41f0fab64bf34b6608fa7cf6b0f1b385a30f4a01afeb10c7732851b2a
388 lines / 15,175 bytes
~~~

The verdict is **STRICT PASS for the conditional theorem stated there**.
The target correctly proves that the single workload $H$, together with
the stated low-death occupation macro, gives finite mean physical hitting of
a finite set and positive recurrence of every closed irreducible class.  It
does not claim to prove the occupation macro.  Section 7 of the target is an
exact reduction of that remaining analytic obligation, not its discharge.

## 1. Exact stopped workload identity

The level-set hypotheses give, pathwise at every finite stopping time,

\[
 H(X_\tau)-H(x)=s\left(B_\tau-
                   \sum_{u\in D}N_{u,\tau}\right).       \tag{1.1}
\]

This omits no physical increment.  Upper reactions preserve $H$, lower
unary transfers preserve it, every $0\to u$ label raises it by $s$, and
every $u\to0$ label lowers it by $s$.  Parallel labels are correctly
aggregated in the counting processes.

The target's compensation argument for an arbitrary almost surely finite
stopping time with finite mean is sound.  A literal localization is obtained
by stopping simultaneously at deterministic time $m$, at the $m$-th
jump, and on a finite population sublevel.  For the constant birth clock,
monotone convergence gives

\[
                     \mathbb E B_\tau=\beta\mathbb E\tau. \tag{1.2}
\]

Nonnegativity of $H(X_\tau)$ in (1.1) gives the pathwise domination

\[
       \sum_{u\in D}N_{u,\tau}\le H(x)/s+B_\tau.          \tag{1.3}
\]

Thus the death count is integrable before its compensator is invoked.
Applying the same increasing localization then proves

\[
 \mathbb E\sum_{u\in D}N_{u,\tau}
 =\mathbb E\int_0^\tau\sum_{u\in D}\delta_uX_u(t)\,dt.  \tag{1.4}
\]

Also $H(X_\tau)\le H(x)+sB_\tau$, so endpoint integrability follows from
finite mean duration.  Therefore equations (2.3)--(2.7) of the target do not
use Dynkin's formula circularly: all terms are integrable before the final
identity is taken.  The occupation inequality (2.8), the count ledger (2.9),
and the macro drift (2.2) are exactly equivalent.

## 2. Pointwise complement and the absence of an embedded margin

If $x\notin{\cal D}_k$, at least one direct-death coordinate is at least
$k$, and hence

\[
 {\cal L}H(x)\le s\beta-s\delta_*k=-c_k.                \tag{2.1}
\]

For the next off-diagonal jump time $T_1$, with total changing rate
$q(x)>0$,

\[
 \mathbb E_x[H(X_{T_1})-H(x)+\eta_0T_1]
 ={\mathcal LH(x)+\eta_0\over q(x)}\le0.                \tag{2.2}
\]

The division by $q(x)$ is correct.  No uniform embedded-jump decrement is
asserted or needed.  This is precisely the point at which a reaction-count
Foster proof would fail when $q(x)\to\infty$, while the physical-time proof
remains valid.

In a nontrivial irreducible class $q(x)>0$ at every state.  A singleton
class is already recurrent and, after $C_R$ is chosen nonempty, creates no
exception to the tiling.

## 3. Episode tiling and nonexplosion

The recursive episode rule is adapted and state selected.  The state space
is countable, so selecting one certified macro for each state is measurable.
Every nonterminal episode contains at least one actual off-diagonal jump;
zero-time chart or algebraic classifications are explicitly folded into the
next physical rule.  Conditional summation of the macro inequality and
(2.2) therefore gives

\[
 \mathbb EH(X_{S_{n\wedge N}})+
 \eta_0\mathbb ES_{n\wedge N}\le H(x).                 \tag{3.1}
\]

There is no hidden uniform-integrability step in this induction.  At each
stage the next endpoint workload and episode duration are nonnegative and
their conditional sum is bounded by the integrable current workload.

Monotone convergence yields

\[
               \eta_0\mathbb ES_\infty\le H(x).         \tag{3.2}
\]

On the event $N=\infty$, the positive-duration episode rule contains
infinitely many distinct physical jumps.  Nonexplosion forces their times,
and hence the episode endpoints, to tend to infinity.  Equation (3.2)
therefore implies $N<\infty$ almost surely and

\[
                       \mathbb ES_N\le H(x)/\eta_0.      \tag{3.3}
\]

The target's binary-network nonexplosion argument is also sufficient.
Quadratic sources cannot increase total molecule count, while all
population-increasing channels have constant or linear propensity and
bounded jumps.  A linear population Lyapunov localization prevents
finite-time escape.  On each population sublevel there are finitely many states
and a finite maximum total rate, so arbitrarily many population-preserving
quadratic jumps cannot accumulate there.

## 4. From a finite set to positive recurrence

The last step in Theorem 5.1 is valid and is stronger than merely producing
an invariant measure.  Fix $o\in C_R$.  For each of the finitely many
states $c\in C_R$, irreducibility supplies a finite physical population
path to $o$.  The union of its prescribed states and all first competing
endpoints is finite.  Consequently:

* the success probability of a prescribed attempt has a uniform positive
  lower bound $p$;
* an attempt has a uniform finite mean duration; and
* every failed endpoint has a finite mean return to $C_R$ by (3.3), with
  a uniform bound because the endpoint set is finite.

Strong-Markov restarts therefore make the attempt count geometrically
dominated and give finite mean hit of $o$.  From $o$, the first ordinary
jump has finite mean holding time and one of finitely many endpoints; the
same bound gives finite mean return to (o).  This is the standard physical-
time definition of positive recurrence for the irreducible class.  No
stationary law of an unrelated embedded chain is substituted.

## 5. Fixed-class reductions and symbolic kernel scope

The invariant exception in Section 6 is exact.  In the common-catalyst
support every upper source contains $Y$.  If $Y=0$ and $Y$ is absent
from the lower unary support, then $Y$ is a full-network invariant and the
upper linkage is inactive on that fixed class.  Coordinates absent from the
remaining lower support are fixed as well.  After this fixed-class
projection, the active network is an open strongly connected unary linkage.
Killing its one-particle graph on first hit of zero gives a transient
subgenerator $Q$; $v=(-Q)^{-1}{\bf1}>0$ yields a linear Foster function
with generator equal to constant immigration minus total active population.

The homogeneous symbolic trichotomy in Section 7 is exhaustive without an
orientation list.  On a dormant pure-$X$ ray, $2X\notin T$.  Rank two
forces a carrier.  Up to interchanging $Y,Z$, the alternatives are:

1. both $XY,XZ$, giving the killed two-carrier kernel;
2. only $XY$, with $2Z$, giving the two-minimum dyadic kernel; or
3. only $XY$, without $2Z$, which forces
   $T=\{XY,YZ,2Y\}$, the common-$Y$-catalyst kernel.

For $h=(1,1,2)$, the quadratic shell is collinear and rank two forces
$C$ plus at least two of $2A,A+B,2B$, giving exactly the four supports
displayed in (7.2).  These are valid reductions of the macro problem.  The
target correctly does **not** infer the occupation estimate from this
support classification.

## 6. Verdict boundary

The following implication is fully proved at the frozen bytes:

\[
 \boxed{\text{occupation macro }{\bf M}(k,R,\eta)
        \quad\Longrightarrow\quad
        \text{classwise positive recurrence}.}
\]

What remains outside the target theorem is equally precise: prove the
macro, or equivalently (2.8)/(2.9), on the low-direct-death region for the
three homogeneous kernels and the four anisotropic supports.  Qualitative
death accessibility, a first hit of a service coordinate, or a bounded
prescribed reaction word would not meet that hypothesis.  Accordingly this
audit is a **STRICT PASS of the conditional workload-only Foster theorem**,
not a recurrence certificate for the 336 family by itself.

## 7. Reproduction and render

The target hash, line count, byte count, and absence of hidden control bytes
were independently replayed.  Pandoc/MathJax conversion and a
LaTeX/Tectonic letter-paper render both complete without an overfull box or
missing-glyph warning.  The resulting target and audit PDFs were inspected
page by page; equations, lists, and the boxed verdict render cleanly.
