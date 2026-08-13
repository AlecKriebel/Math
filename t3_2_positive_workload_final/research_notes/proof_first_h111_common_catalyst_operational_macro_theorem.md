# The homogeneous common-catalyst operational macro theorem

**Proof-first standalone theorem, 2026-08-12 PDT.**  This note proves the
remaining stopped workload macro for the exceptional homogeneous level-set
kernel

\[
 T=\{X+Y,Y+Z,2Y\},\qquad R=\{0,Y,Z\}.                 \tag{1.1}
\]

Both supports carry arbitrary fixed strongly connected labelled directed
graphs and arbitrary fixed positive rate constants.  Every clock remains
active.  The proof does not enumerate orientations, rates, reaction
histories, or population boxes.

The key point is that activation is charged by its **expected complete
birth/death ledger**.  Individual lower deaths are never declared failed
attempts, and the theorem makes no false pathwise assertion that a local
death count has already repaid births from earlier attempts.

## 1. Statement and exact ledger

Work in any closed irreducible population class of the binary stochastic
mass-action chain.  Put

\[
                             H(x)=X+Y+Z.               \tag{1.2}
\]

Let \(B_t\) be the total number of zero-source births by time \(t\), and
let \(D_t\) be the total number of direct lower deaths \(Y\to0\) and
\(Z\to0\), with parallel labels counted separately.  Top reactions and
lower unary transfers preserve \(H\).  Therefore, pathwise at every finite
stopping time,

\[
                       H(X_t)-H(X_0)=B_t-D_t.          \tag{1.3}
\]

The theorem is the following.

> **Theorem 1.1 (common-catalyst all-clock macro).**  There are constants
> \(R<\infty\), \(a>0\), \(C<\infty\), and \(\eta>0\), depending only on
> the fixed labelled network, such that for every population \(x\) with
> \(H(x)\ge R\) one may choose an all-clock stopping time \(\tau_x\) which
> contains at least one ordinary physical jump, has its actual physical
> population as endpoint, and satisfies
> \[
>       \mathbb E_x\tau_x\le C,
>       \qquad
>       \mathbb E_x(D_{\tau_x}-B_{\tau_x})\ge a.       \tag{1.4}
> \]
> In particular \(\mathbb E_xH(X_{\tau_x})<\infty\), and after decreasing
> \(\eta\) if necessary,
> \[
>  \mathbb E_x[H(X_{\tau_x})-H(x)+\eta\tau_x]\le0.    \tag{1.5}
> \]

This is exactly the occupation macro required by the workload-only
physical-time Foster theorem.  No bound on the number of neutral top
reactions is asserted or used.

## 2. Exact labelled-particle top representation

Assume \(Y\ge1\), and write

\[
             z_{\mathsf X}=X,\qquad z_{\mathsf Z}=Z,
             \qquad z_{\mathsf Y}=Y-1.                \tag{2.1}
\]

The three top source propensities factor exactly as

\[
 (x)_{X+Y}=Yz_{\mathsf X},\qquad
 (x)_{Y+Z}=Yz_{\mathsf Z},\qquad
 (x)_{2Y}=Yz_{\mathsf Y}.                             \tag{2.2}
\]

Aggregate the labelled top rates between the corresponding states
\(\mathsf X,\mathsf Z,\mathsf Y\) into a three-state generator \(Q\).
Strong connectivity of the graph on \(T\) makes \(Q\) irreducible.  If

\[
                              A(t)=\int_0^tY(s)\,ds,   \tag{2.3}
\]

then, between lower reactions, the top chain in operational time \(A\) is
exactly \(H-1\) independently moving labelled particles with one-particle
generator \(Q\):

\[
                              \mathcal L_T=Y\mathcal L_Q. \tag{2.4}
\]

This is an algebraic factorization, not an averaging claim.

For every \(i\in\{\mathsf X,\mathsf Z,\mathsf Y\}\), choose one simple
directed \(Q\)-path from \(i\) to \(\mathsf Y\).  It has length at most
two.  Fix an operational horizon \(a_0>0\), split an initial part of it into
enough disjoint windows for these paths, and use independent graphical
Poisson clocks for every labelled particle and every labelled top arrow.
For a particle initially in state \(i\), let \(E_i\) be the event that:

1. its chosen path arrows occur in their prescribed windows;
2. no competing top arrow moves it off the chosen path; and
3. no top arrow leaves \(\mathsf Y\) anywhere in \([0,a_0]\).

Every required or forbidden clock family is finite, so

\[
                 p_*:=\min_i\mathbb P(E_i)>0.          \tag{2.5}
\]

The events for distinct particle labels are independent.  If a lower
\(Z\to Y\) transfer acts on a labelled \(\mathsf Z\)-particle during the
block, it moves that particle directly to the terminal state
\(\mathsf Y\).  Condition 3 then keeps it there.  Hence a \(Z\to Y\)
transfer can only help \(E_i\); it cannot invalidate the graphical lower
bound.  A direct \(Z\to0\) death deletes one particle, and no other
\(Z\)-sourced lower reaction is possible.

Let \(S\) be the number of the initial \(H-1\) labels whose events \(E_i\)
occur.  The Bernoulli variables need not have the same parameter, but all
have parameter at least \(p_*\).  A standard exponential Chernoff bound
gives constants \(c>0\) and \(n_0\) such that

\[
 \mathbb P\{S\ge p_*(H-1)/2\}\ge1-e^{-cH}
                 \qquad(H\ge n_0).                    \tag{2.6}
\]

This holds for every initial distribution of the free particles.  In
particular no assumption that most particles are initially \(\mathsf X\)
is hidden in the argument.

## 3. One operational block with every lower clock retained

Let

\[
 K_Y^R=\sum_{e:s(e)=Y}\kappa_e,\qquad
 \beta=\sum_{e:s(e)=0}\kappa_e>0.                     \tag{3.1}
\]

Starting from \(Y\ge1\), run the full chain until the first of:

* an increment \(a_0\) of the operational clock \(A\);
* a lower reaction sourced at \(Y\);
* a zero-source birth; or
* the fractional workload condition declared in Section 5.

Call the block **clean** if the operational-clock alternative occurs, and
call it **unspoiled** if neither a \(Y\)-sourced lower event nor a birth occurs
before the earlier of that operational endpoint and the fractional stop.
Before a \(Y\)-sourced lower event, top reactions and \(Z\)-sourced lower
reactions leave at least one catalyst, so \(Y\ge1\) and the physical time
needed for \(A\) to increase by \(a_0\) is at most \(a_0\).  In operational
time, the aggregate \(Y\)-sourced lower hazard is exactly \(K_Y^R\).
Conditional on every top and \(Z\)-sourced history, the probability of no
birth before that earlier endpoint is at least \(e^{-\beta a_0}\).
Consequently

\[
             \mathbb P\{\text{block is unspoiled}\mid\mathcal G\}
             \ge q_0:=e^{-(K_Y^R+\beta)a_0}>0,         \tag{3.2}
\]

where \(\mathcal G\) contains the complete graphical top and
\(Z\)-sourced history.  Thus an unspoiled block either reaches the
fractional-return branch, which is already a successful macro endpoint, or
is clean and reaches operational time \(a_0\).

All \(Z\to0\) deaths and all \(Z\to Y\) transfers remain active inside a
clean block.  Let \(M_Z\) be the number of direct \(Z\to0\) deaths during
it, and put

\[
                             \alpha=p_*/8,\qquad
                             \rho=p_*/4.                 \tag{3.3}
\]

On the graphical event in (2.6), at most \(M_Z\) successful labels have
been deleted.  Therefore one of the following observable endpoint
alternatives holds:

\[
 M_Z\ge\alpha H_{\rm start},
 \qquad\hbox{or}\qquad
 Y_{\rm end}\ge\rho H_{\rm start}\ge\rho H_{\rm end}.
                                                               \tag{3.4}
\]

Indeed, if the first alternative in (3.4) fails, (2.6) leaves at least
\(p_*(H_{\rm start}-1)/2-\alpha H_{\rm start}\) successful undeleted
labels.  For all sufficiently large \(H_{\rm start}\), this is at least
\(\rho H_{\rm start}\).  The first alternative is a death-rich block;
the second is a catalyst shell.  Since (3.2) holds conditional on the
graphical history, (2.6) and (3.2) imply that, for all sufficiently large
block-start workloads, a block either reaches the fractional stop or
terminates in one of (3.4), with conditional probability at least one
fixed \(p_0>0\).  A lower event sourced at \(Y\), including a direct death
or a catalyst-removing transfer \(Y\to Z\), merely ends the current block
at its actual endpoint.  It is counted and the next complete attempt starts
there.

## 4. Uniform seeding from the top-dead face

On \(Y=0\), every top source is disabled.  There is nevertheless a
uniform finite-mean physical seed of \(Y\), with a uniformly bounded
expected number of births.

Choose a simple directed lower path from \(0\) to \(Y\).  It has length
one or two.

* If a selected label \(0\to Y\) exists, wait for its constant-rate clock.
  Its mean waiting time is finite, and the expected number of all other
  births before it is finite.
* Otherwise the simple path is \(0\to Z\to Y\).  Wait for a selected
  \(0\to Z\) birth and label that new molecule.  Its first unary event has
  finite mean.  With one fixed positive probability it follows a selected
  \(Z\to Y\) label (any parallel \(Z\to Y\) label is also success); if it
  dies, repeat.  These trials are geometrically dominated.

Other lower reactions do not delay the selected constant birth clocks or
the labelled unary lifetime.  Direct deaths are favorable and retained.
Thus there are constants \(C_s,C_b<\infty\), uniform over the initial
number of \(Z\)-molecules, such that the seed time \(\sigma_s\) satisfies

\[
 \mathbb E\sigma_s\le C_s,\qquad
 \mathbb E B_{\sigma_s}\le C_b,\qquad
 Y(\sigma_s)\ge1.                                    \tag{4.1}
\]

Stopping earlier at the fractional workload condition of Section 5 only
improves these bounds.

## 5. Geometric complete attempts and finite birth debt

Fix a starting population \(x\), write \(H_0=H(x)\), and repeat the
following complete attempts:

1. if \(Y=0\), run the seed of Section 4;
2. from \(Y\ge1\), run one operational block of Section 3.

At every physical jump, stop the prelude on the fractional return

\[
                              H\le H_0/2.              \tag{5.1}
\]

If a clean block ends in one of (3.4), stop the prelude in the corresponding
death-rich or catalyst-shell branch.  Otherwise begin the next complete
attempt from the actual endpoint.

Until (5.1), every block starts with workload at least \(H_0/2\).  Choose
the eventual large-state threshold so that (2.6)--(3.4) give the same
conditional success probability \(p_0\) at every attempt.  Hence the number
of complete attempts is dominated by a geometric random variable.  Each
attempt has conditional expected duration at most \(C_s+a_0\), and contains
at most the uniformly integrable seed births plus one active-block birth.
There are constants independent of \(H_0\) such that

\[
        \mathbb E\tau_{\rm pre}\le C_{\rm pre},
        \qquad
        \mathbb E B_{\tau_{\rm pre}}\le C_{\rm pre}^B. \tag{5.2}
\]

Every failed-attempt death remains in \(D\) and is favorable.  Equation
(5.2), rather than a pathwise assertion about a successful block, is the
complete expected birth debt which will be charged below.

The three prelude endpoints are disjoint:

1. **fractional return:** \(H\le H_0/2\), so by (1.3)
   \[
                         D-B\ge H_0/2;                \tag{5.3}
   \]
2. **death rich:** before (5.1), a block has
   \[
                         M_Z\ge\alpha H_0/2;          \tag{5.4}
   \]
3. **catalyst shell:** at an endpoint with current workload \(n\),
   \[
                         Y\ge\rho n,\qquad n>H_0/2.   \tag{5.5}
   \]

If the lower graph has no direct \(Z\to0\) label, the second branch is
simply absent; the graphical alternative then produces (5.5).

## 6. Uniform all-clock service from the catalyst shell

Let

\[
 \delta_Y=\sum_{Y\to0}\kappa_{Y0},\qquad
 \delta_Z=\sum_{Z\to0}\kappa_{Z0}.                   \tag{6.1}
\]

Strong connectivity of \(R\) gives \(\delta_Y+\delta_Z>0\).  We first
prove a deterministic service fact without invoking a qualitative chart
argument.

On the unit simplex, write \(q=(q_{\mathsf X},q_{\mathsf Z},
q_{\mathsf Y})\) as a row vector.  The top mass-action ODE has the exact
time-changed linear form

\[
                           \frac{dq}{ds}=q_{\mathsf Y}qQ. \tag{6.2}
\]

In operational time \(\theta\), its solution is

\[
                              q(\theta)=q(0)e^{Q\theta}. \tag{6.3}
\]

The finite irreducible generator \(Q\) has a strictly positive invariant
row vector.  Hence, from every \(q(0)\) with
\(q_{\mathsf Y}(0)\ge\rho\), the solution enters the interior and both
\(q_{\mathsf Y}\) and \(q_{\mathsf Z}\) have infinite physical-time
integral.  This assertion is uniform over the compact initial shell.
Explicitly, for bounded operational \(\theta\),

\[
 q_{\mathsf Y}(\theta)
   \ge \rho e^{-K\theta}>0,                           \tag{6.4}
\]

and for large \(\theta\), \(q(0)e^{Q\theta}\) is uniformly close to the
positive invariant vector.  Since \(d\theta/ds=q_{\mathsf Y}\) and
\(q_{\mathsf Y}(\theta)\ge\rho e^{-K\theta}\), the physical time required
to reach any fixed \(\theta_0\) is at most
\((e^{K\theta_0}-1)/(K\rho)\) (with the evident \(K=0\) convention).
The convergence therefore gives a uniform positive lower bound on both
displayed service coordinates after a finite physical time.
Therefore, for every prescribed \(D_0<\infty\), there is a finite physical
fluid horizon \(T(D_0)\) such that

\[
 \inf_{q_{\mathsf Y}(0)\ge\rho}
 \int_0^{T(D_0)}
       [\delta_Yq_{\mathsf Y}(s)+\delta_Zq_{\mathsf Z}(s)]\,ds
                                                        \ge 2D_0. \tag{6.5}
\]

Now start the full stochastic chain at a shell endpoint of workload \(n\),
and run every clock for physical time \(T(D_0)/n\).  On the rescaled time
interval, the top density process converges uniformly to (6.2), uniformly
over the compact shell.  This follows directly from the graphical
martingale decomposition: the quadratic top clocks have density-martingale
quadratic variation \(O(n^{-1})\), the polynomial top drift is Lipschitz on
the simplex, and the lower unary and constant clocks produce only \(O(1)\)
reactions and hence \(o(1)\) density displacement.  Localization followed
by Gronwall gives uniform \(L^1\) convergence.

The direct-death compensator and (6.5) consequently give, after increasing
the large-state threshold,

\[
 \inf_{\text{shell endpoints}}
 \mathbb E D_{\rm serv}\ge D_0.                       \tag{6.6}
\]

The expected number of births in this window is exactly
\(\beta T(D_0)/n\).  All lower transfers and deaths remain active in the
density approximation and in (6.6).

After the service window, take one final ordinary physical jump.  This
guarantees that the complete macro contains a jump even if it started in a
catalyst shell and no clock fired during the fixed service window.  Since
the constant birth hazard is \(\beta>0\), the final holding time has mean at
most \(1/\beta\), and the final jump contributes at most one further birth.
Use the same final-jump convention on the death-rich branch.  A fractional
return already ends at an actual jump and needs no appended jump.

## 7. Expected ledger closure

First choose

\[
                              D_0=C_{\rm pre}^B+3.      \tag{7.1}
\]

Choose the service horizon from Section 6, and then choose the population
threshold \(R\) large enough that:

1. the graphical success probability is uniform for every block start with
   \(H\ge R/2\);
2. \(R/2\ge D_0\) and \(\alpha R/2\ge D_0\);
3. the expected service-window birth count is at most one; and
4. the uniform stochastic service estimate (6.6) holds.

The expected number of all births in a complete macro, restricted to the
union of the death-rich and catalyst-shell branches, is then at most

\[
                         C_{\rm pre}^B+2,              \tag{7.2}
\]

where the two extra units cover the service window and the final jump.
This is an unconditional restricted expectation, not a conditional moment
bound on a rare branch.
Let \(F,D,I\) denote respectively the fractional-return, death-rich, and
catalyst-shell endpoint events.  They form a partition.  Equations
(5.3)--(5.5), (6.6), and (7.2), with all failed-attempt deaths discarded as
favorable, give

\[
\begin{aligned}
 \mathbb E(D_\tau-B_\tau)
 &\ge D_0\mathbb P(F)+D_0\mathbb P(D)+D_0\mathbb P(I)
       -(C_{\rm pre}^B+2)\\
 &\ge1.
\end{aligned}                                             \tag{7.3}
\]

This is an **expected** complete ledger.  No line asserts that the local
deaths in the final successful block exceed the realized births in all
preceding failures.

The geometric prelude, fixed service window, and final holding time also
give one constant \(C<\infty\) with

\[
                              \mathbb E\tau\le C.       \tag{7.4}
\]

Pathwise, \(H(X_\tau)\le H(x)+B_\tau\), so (5.2), (7.2) give endpoint
integrability.  Taking \(a=1\) and, for example,

\[
                              \eta=\frac1{2C}           \tag{7.5}
\]

in (1.3), (7.3)--(7.4) proves (1.4)--(1.5).

## 8. Classwise consequence and exact scope

The binary chain is nonexplosive: population-increasing reactions have
constant or linear propensity, while quadratic top reactions preserve the
positive workload \(H\) and cannot accumulate on a finite population
sublevel.  The stopping rule above is a function of the current population,
the starting workload of the current macro, and fixed network data.  Every
competitor and failure ends at an actual physical endpoint, and every new
attempt begins there by the strong Markov property.

Theorem 1.1 supplies the occupation macro on the entire large-workload
region, hence in particular on the low-direct-death boundary required by
the workload-only physical-time Foster theorem

~~~text
research_notes/proof_first_levelset_h_alone_physical_time_foster_lemma.md
SHA-256 8cf2a8d41f0fab64bf34b6608fa7cf6b0f1b385a30f4a01afeb10c7732851b2a
~~~

That theorem has the independent exact-byte audit

~~~text
research_notes/proof_first_levelset_h_alone_physical_time_foster_lemma_exact_byte_audit.md
SHA-256 9d8fc8b5e15178e7a8305422ba7fd08e6875e851c37951207815d5d84babcc67
~~~

Consequently every closed irreducible class of (1.1) is positive recurrent.
The result is exactly the common-catalyst homogeneous kernel.  The other two
homogeneous kernels require their own carrier/source-balance macros and are
not claimed here.
