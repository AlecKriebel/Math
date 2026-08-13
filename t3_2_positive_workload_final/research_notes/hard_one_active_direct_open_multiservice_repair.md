# Multi-service repair for the 99 direct and six open one-active rows

**Proof-first candidate addendum, 2026-08-12 PDT.**  This note repairs the
specific defect found by the hostile audit of
`hard_one_active_1104_common_w_theorem.md`.  It does not alter that frozen
failed snapshot.  The repair is deliberately analytic: the finite table is
used only at the end to check 105 support predicates.  No orientation,
population box, history, or reaction word is enumerated.

The point of the repair is simple but essential.  One active service pays
only \(\log n\), whereas a deterministic inactive cloud of size
\(u=n^{o(1)}\) may change its factorial-linear entropy by order
\(u\log(2+u)\).  We therefore run

\[
                         K=1+u                                      \tag{1.1}
\]

physical services.  The active population remains \(n-n^{o(1)}\), the
inactive endpoint still has size \(n^{o(1)}\), and

\[
 K\log n-C K\log(2+K)\sim K\log n.                                \tag{1.2}
\]

This also resolves the arbitrary-correction seam: the linear correction is
charged at the final physical endpoint and telescopes.  It is not charged
once per fast internal reaction.

The conclusions below are submitted for a fresh hostile audit.  In
particular, an auditor is invited to produce a strong orientation for which
the tagged direct service clock, the open aggregate launch probability, or
one of the endpoint-weighted estimates below fails.  Until that replay is
complete, the repaired 105-row flag, the unified 1,104-row flag, every hard
pair flag, and the global T3-2 flag remain **false**.

## 1. Fixed-class setup and the required endpoint statement

Fix a hard support pair, arbitrary strongly connected directed graphs on
its two linkage supports, arbitrary positive rate constants, and a closed
irreducible physical class.  Relabel the unique old active coordinate as
\(C\), and start at

\[
                    X_0=(Z_0,C_0)=(z,n),\qquad |z|_1=u=n^{o(1)}.       \tag{1.3}
\]

Fix an arbitrary vector \(\ell\in\mathbb R^3\), choose \(K_\ell\) so that

\[
 G_\ell(x)=K_\ell+\sum_{i=1}^3\log(x_i!)+\ell\cdot x\ge1,
 \qquad W_\ell=G_\ell^4.                                           \tag{1.4}
\]

The stopped episode constructed below has three disjoint kinds of actual
post-jump endpoint.

* \(D_K\): the included reaction completing the \(K\)-th net service;
* \(E\): the included first lower-clock defect; and
* \({\cal B}\): the included first moving-cutoff crossing.

At a boundary crossing we retain the inherited path label: \(P\) means a
closed no-fast outer return, and \(B\) means that a carrier or fast
excursion is still open.  Since the estimates below first control their
union \({\cal B}=P\mathbin{\dot\cup}B\), they control both subsets with the
same actual-endpoint weight.

The episode may continue after its first old-debt service.  On the reflected
lift, that first service decreases the positive incoming mark.  Once the
mark reaches zero, later services are surplus services.  Reflection changes
only the auxiliary mark; it neither suppresses a physical reaction nor
changes the physical stopping time.  Thus no assumption that the incoming
debt is at least \(K\) is being made.

Put

\[
 R_\tau=1+|Z_\tau|_1+|C_\tau-n|+\tau .                            \tag{1.5}
\]

For either of the two mechanisms proved below, and every fixed \(r,M\),
there are constants and integers \(d_r\), independent of \(n,z\), such
that

\[
\begin{aligned}
 \mathbb P(D_K)&\ge1-n^{-1+o(1)},\\
 \mathbb E[R_\tau^r;D_K]&\le C_r(1+u+K)^{d_r},\\
 \mathbb E[R_\tau^r;E]&\le {C_r\over n}(1+u+K)^{d_r},\\
 \mathbb E[R_\tau^r;{\cal B}]&\le C_{r,M}n^{-M},\\
 C_\tau&=n-K\quad\hbox{on }D_K,\\
 \mathbb E\!\left[\sum_{i\ne C}\log(X_{\tau,i}!);D_K\right]
   &\le C(1+u+K)\log(2+u+K).
\end{aligned}                                                     \tag{1.6--1.11}
\]

Here and below \(n^{-1+o(1)}\) means \(n^{-1}\) times a fixed polynomial
in \(u+K\).  This distinction is useful: (1.8), rather than an unweighted
defect probability, retains every polynomial size bias needed by the exact
fourth-power expansion.

For the direct mechanism,

\[
                    \mathbb E\tau^r\le C_rK^r n^{-r};              \tag{1.12}
\]

for the open mechanism,

\[
                    \mathbb E\tau^r\le C_rK^r.                     \tag{1.13}
\]

These bounds are physical-time statements.

## 2. The multi-service entropy lemma

We first isolate the deterministic implication of (1.6)--(1.13).

> **Lemma 2.1 (subpower cloud amortization).**  Suppose a physical stopped
> episode from (1.3) satisfies (1.6)--(1.11), and has every fixed duration
> moment bounded by a fixed polynomial in \(1+u+K\).  If \(K=1+u\), then,
> for every fixed \(\ell\),
> \[
>  \mathbb E\{G_\ell(X_\tau)-G_\ell(X_0)\}
>       \le-cK\log n,                                               \tag{2.1}
> \]
> and
> \[
>  \mathbb E\{W_\ell(X_\tau)-W_\ell(X_0)+\tau\}
>       \le-cG_\ell(X_0)^3K\log n.                                 \tag{2.2}
> \]
> In particular the weaker local interface bound with right side
> \(-cG_\ell(X_0)^3\log n\) holds.  The endpoint has every prescribed
> fixed moment, including some order \(q>8\).

### Proof

On \(D_K\), the active factorial-linear increment is

\[
 \log{(n-K)!\over n!}-\ell_CK
 =-\sum_{j=0}^{K-1}\log(n-j)-\ell_CK
 \le-K\log(n-K)+|\ell_C|K.                        \tag{2.3}
\]

Because \(K=n^{o(1)}\), eventually \(K<n/2\).  For an inactive vector
\(y\),

\[
 \sum_{i\ne C}\log(y_i!)+\ell_{\ne C}\cdot y
 \le C_\ell(1+|y|_1)\log(2+|y|_1),                                \tag{2.4}
\]

whereas the same expression at \(z\) is bounded below by
\(-C_\ell(1+u)\).  Equations (1.6), (1.10), and (1.11) therefore give

\[
 \mathbb E[\Delta G_\ell;D_K]
 \le-K\log(n-K)+C_\ell K\log(2+K)+n^{-1+o(1)}K\log n.             \tag{2.5}
\]

The correction term in (2.4) is an endpoint difference.  Thus even if the
fast phase makes order \(n\tau\) internal conversions, its total
\(\ell\)-cost is only \(\ell\cdot(X_\tau-X_0)\).

A bounded reaction changes every coordinate by at most two.  From (1.8),
(1.9), and the elementary bound

\[
 |\log((m+j)!/m!)|\le C|j|\log(2+m+|j|),                            \tag{2.6}
\]

we obtain, for every fixed \(r\),

\[
 \mathbb E[|\Delta G_\ell|^r;E]=n^{-1+o(1)}(\log n)^r,
 \qquad
 \mathbb E[|\Delta G_\ell|^r;{\cal B}]=n^{-M}                    \tag{2.7}
\]

after increasing the moment order in (1.8)--(1.9).  Equations (2.5)--(2.7)
and \(\log K=o(\log n)\) prove (2.1).  They also give

\[
                 \mathbb E|\Delta G_\ell|^r
                    \le n^{o(1)}(\log n)^r.                        \tag{2.8}
\]

Stirling's bounds imply

\[
                         G_\ell(X_0)\asymp n\log n,                 \tag{2.9}
\]

uniformly along the subpower entrance sequence.  Use the exact identity

\[
 \Delta W_\ell
 =4G_0^3\Delta G_\ell+6G_0^2(\Delta G_\ell)^2
   +4G_0(\Delta G_\ell)^3+(\Delta G_\ell)^4,                       \tag{2.10}
\]

where \(G_0=G_\ell(X_0)\).  By (2.8)--(2.9), the last three expectations
are \(n^{-1+o(1)}\) relative to
\(G_0^3K\log n\).  The duration is polynomial in \(K=n^{o(1)}\), hence is
lower order as well.  Combining this with (2.1) proves (2.2).  Equations
(1.7)--(1.9) give every fixed endpoint moment. \(\square\)

## 3. Direct rows: the marked top-source process

Assume a linkage contains the physical source \(C\) and at least one
active-free complex.  Call a reaction **top sourced** if its source has
active degree one.  A top-sourced reaction whose target has active degree
zero is a service; a top-to-top reaction preserves \(C\).  Until the first
active-free-source reaction, retain every top-sourced reaction and use
active time

\[
                         s(t)=\int_0^t C_r\,dr.                      \tag{3.1}
\]

After stripping the common \(C\), every top complex is one of
\(0,A,B\).  Thus top-to-top reactions are immigration, death, or conversion
of labelled inactive particles; they never branch a particle.  A service
may land at a lower complex of inactive molecularity at most two.

### 3.1 A background-independent service clock

Strong connectivity of the linkage containing \(C\) supplies a simple
directed complex path from \(C\) to an active-free vertex.  Stop the path at
its first active-free vertex.  Every internal vertex is top, so after
stripping it is in \(\{0,A,B\}\).

Use the Harris labelled-particle construction for the unimolecular
top-to-top reactions.  Every background particle carries independent
exponential marks for each outgoing top edge of its type, and stripped-zero
births have independent Poisson marks.  This construction is exact because
no top source contains two inactive molecules.  If the first path edge is
not already a service, reserve one fresh birth mark in the first third of a
fixed interval and tag the particle it creates.  Reserve, in successive
subintervals, the desired outgoing mark of that tag at each later internal
vertex and require that none of the tag's other marks occur first.  The
product of these finitely many exponential probabilities is a number
\(\eta>0\) depending only on the fixed path and its rates.  It does not
depend on the number, positions, or clocks of the background particles.

We impose no restriction on background marks.  If a background particle
causes a service before the tag finishes, the desired event has already
occurred.  Otherwise background top-to-top marks neither consume nor move
the tag, because the graphical construction assigns the reacting particle
its own label.  It follows that there are constants \(T,\eta>0\), depending
on the chosen orientation and rates but not on the background population,
such that, in the defect-free top-only auxiliary process,

\[
 \mathbb P\{\hbox{some service in the next active-time interval }T
             \mid\mathcal F_s\}\ge\eta.                            \tag{3.2}
\]

Couple the physical chain to this auxiliary process up to the first
active-free-source clock; the paths are identical before that defect.
Applying (3.2) after successive services shows that
the active time \(S_K\) of the \(K\)-th service has negative-binomial
tails.  In particular, for every fixed \(r\),

\[
             \mathbb E S_K^r\le C_rK^r,
 \qquad
             \mathbb P\{S_K>CK+y\}\le C e^{-cy}.                   \tag{3.3}
\]

This is an aggregate service estimate.  The path was used only to construct
one background-independent clock; the physical process retains every top
reaction, and no probability is assigned to the event that the entire
system follows one selected word.

### 3.2 Population, defect, and boundary estimates

Let \(M_s=A_s+B_s\) in the top-only auxiliary process and let \(N_s\) count
services.  Top-to-top conversions do not increase \(M\); stripped-zero
births form a fixed-rate Poisson process \(\Pi\); and each service adds at
most two inactive molecules.  Hence, pathwise before the \(K\)-th service,

\[
                         M_s\le u+\Pi_s+2N_s.                       \tag{3.4}
\]

Equations (3.3)--(3.4) give, for every fixed \(r\),

\[
 \mathbb E(1+S_K+\sup_{s\le S_K}M_s)^r
       \le C_r(1+u+K)^r,                                           \tag{3.5}
\]

and an exponential tail above a fixed multiple of \(u+K\).

Every active-free source in the molecularity-two catalogue has total
physical propensity at most \(C(1+M)^2\).  Before \(K\) clean services the
active population is \(n-N_s\ge n-K\); therefore its hazard in active time
is at most

\[
                         {C(1+M_s)^2\over n-K}.                     \tag{3.6}
\]

Stop at the actual post-jump state of the first such firing.  The
compensator formula, (3.3)--(3.5), and polynomial size bias give, for every
fixed \(r\),

\[
 \mathbb E[(1+S+M+N)^r;E]
       \le {C_r\over n}(1+u+K)^{r+3}.                              \tag{3.7}
\]

The exponent \(r+3\) is inessential; what matters is that it is fixed.
The causing lower reaction is included, so (3.7) is an actual-endpoint
estimate, not a pre-jump estimate.

For localization take \(L_n=n^{1/16}\) and stop at the included first
crossing of inactive mass \(L_n\).  Since \(u+K=n^{o(1)}\), the compound
Poisson and negative-binomial tails in (3.3)--(3.4), with any polynomial
endpoint size bias, give

\[
                   \mathbb E[(1+S+M+N)^r;{\cal B}]
                         \le C_{r,M}n^{-M}.                         \tag{3.8}
\]

On the complement of \(E\cup{\cal B}\), exactly \(K\) top-to-lower
reactions have occurred and no active-free-source reaction has occurred.
Thus \(C_\tau=n-K\).  Moreover (3.4)--(3.5) and
\(\sum_i\log(z_i!)\le |z|_1\log(1+|z|_1)\) prove (1.7) and (1.11).
Finally, (3.1) and \(C_t\ge n-K\) give

\[
                         \tau\le {S_K\over n-K},                    \tag{3.9}
\]

which proves (1.12).  This establishes (1.6)--(1.12) for every direct row.

## 4. Open rows: an all-clock origin-launch ladder

The six open rows normalize to

\[
                   \{C,A+C\},\qquad\{0,B,2B,B+C\},                 \tag{4.1}
\]

and their one-active entrance has \(B_0=0\).  The possibly unbounded
subpower spectator is \(A_0=u\).

The two-vertex first linkage is necessarily bidirected under strong
connectivity.  After aggregation, its exact dynamics is

\[
 C\longrightarrow A+C\quad\hbox{at rate }\alpha C,
 \qquad
 A+C\longrightarrow C\quad\hbox{at rate }\beta CA,                \tag{4.2}
\]

with \(\alpha,\beta>0\).  It preserves \(C\).  Conditional on the clock

\[
                         s(t)=\int_0^t C_r\,dr,                     \tag{4.3}
\]

the exact independent-particle representation is

\[
 A_t\ \stackrel d=\
 \operatorname{Bin}\!\left(u,e^{-\beta s(t)}\right)
 +\operatorname{Pois}\!\left({\alpha\over\beta}
                    (1-e^{-\beta s(t)})\right).                    \tag{4.4}
\]

The clocks in the other linkage do not use \(A\).  We therefore first
construct an **unlocalized** stopping time \(\tau^\circ\) using only the
driving clocks and populations \((B,C)\): it is the first clean completion
of \(K\) services or the included first lower-source defect, with no
\(A\)-cutoff.  Conditional on the entire \((B,C)\)-path through
\(\tau^\circ\), its operational horizon
\(S^\circ=s(\tau^\circ)\) is deterministic and the independent-particle
construction gives the exact conditional law

\[
 A_{\tau^\circ}\mid\sigma\{(B_t,C_t):t\le\tau^\circ\}
 \ \stackrel d=\
 \operatorname{Bin}\!\left(u,e^{-\beta S^\circ}\right)
 +\operatorname{Pois}\!\left({\alpha\over\beta}
                    (1-e^{-\beta S^\circ})\right).                \tag{4.4a}
\]

The two summands use independent marks.  In particular, for every fixed
\(r\), uniformly in the realized \((B,C)\)-path,

\[
 \mathbb E(1+A_\tau)^r\le C_r(1+u)^r,
 \qquad
 \mathbb E\log(A_\tau!)\le C\{1+u\log(2+u)\}.                     \tag{4.5}
\]

This is the place where background-particle independence matters.  The
number of fast reactions in (4.2) may be of order \(n\tau\), but neither
their number nor their accumulated absolute linear displacement is charged;
only the endpoint in (4.4) is charged.

### 4.1 One clean net service

Write \(T=B+C\).  At a state with \(B=b>0\) and active population \(m\),
the aggregate \(T\)-exit rate is at least \(c m b\).  The sum of all
active-free-source propensities in the second linkage is at most
\(C(1+b^2)\).  Reactions in (4.2) may occur in between, but change neither
\(b\) nor \(m\).  Hence the first relevant-clock race gives

\[
 \mathbb P\{\hbox{a lower-source reaction precedes the next }T
                   \hbox{-exit}\}
       \le {C(1+b)\over m}.                                         \tag{4.6}
\]

On the complementary event the included \(T\)-exit is a clean service:
it lowers \(C\) by one and sends \(b\) to \(b-1+j\), where
\(j\in\{0,1,2\}\).  In particular the new value is at most \(b+1\).

It remains to start a service from \(b=0\).  Aggregate all outgoing
channels from the zero complex.  Their total rate \(\lambda_0\) is positive
and their target is in \(\{B,2B,T\}\).  If the target is \(B\) or \(2B\),
the next clean \(T\)-exit is already a net service.  If the target is
\(T\), that entry and its first clean \(T\)-exit have net active reward
zero.  When the exit target has positive \(B\), the following clean
\(T\)-exit is a net service; when it is zero, the system has returned to
the same \(b=0\) base and the attempt is repeated.

Let

\[
 p_*=\mathbb P_0\{0\to B\hbox{ or }2B\}
      +\mathbb P_0\{0\to T\}
         \mathbb P_T\{T\to B\hbox{ or }2B\}.                       \tag{4.7}
\]

All probabilities in (4.7) are aggregate outgoing-rate ratios.  Strong
connectivity implies \(p_*>0\): if the first term vanished and every
\(T\)-exit returned to zero, then \(\{0,T\}\) would be a closed proper
subset of the four-vertex linkage.  Thus the number of neutral attempts is
geometric with a parameter bounded below by the fixed number \(p_*\).
Every attempt waits an exponential time of rate \(\lambda_0\) and uses at
most two fast exits before either service or repetition.

During the intermediate states \(B\le2\), (4.6) is \(O(n^{-1})\).  Stop at
the actual post-jump endpoint if such a competing lower-source reaction
occurs.  We have proved an all-clock one-service kernel from \(b=0\) with

\[
\begin{aligned}
 \mathbb P(\hbox{defect})&\le C/n,\qquad
 \mathbb P(\hbox{clean net service})&\ge1-C/n,\\
 \mathbb E\tau_{\rm one}^r&\le C_r,\qquad
 B_{\rm service}&\le3\quad\hbox{on the clean path}.
\end{aligned}                                                     \tag{4.8--4.9}
\]

All polynomially size-biased versions of the first estimate hold.  Indeed,
the geometric attempt count has every moment, the intermediate \(B\) is
bounded, (4.4) supplies every \(A\)-moment, and the competing event is
integrated with its exact \(O(n^{-1})\) clock ratio.  This is the elementary
aggregate form of the Poisson regenerative block for the exact open
support (4.1); it neither truncates the immigration--death chain nor
chooses one orientation word.

### 4.2 Iteration

Restart the preceding kernel after every clean service.  If \(B>0\), use
the immediate race (4.6); if \(B=0\), use the geometric origin-launch
construction.  On a clean path the \(j\)-th service endpoint satisfies

\[
                         B_j\le j+3.                               \tag{4.10}
\]

Since the active population before completion is at least \(n-K\), summing
(4.6) and (4.8), with every polynomial endpoint size bias, gives

\[
 \mathbb E[(1+A+B+|C-n|+\tau)^r;E]
       \le {C_r\over n}(1+u+K)^{d_r}.                              \tag{4.11}
\]

Every clean macrocycle has net active reward exactly \(-1\): entries in a
neutral attempt are paired with their first exits, while the final exit is
unpaired.  Hence the clean \(K\)-service endpoint has \(C_\tau=n-K\).
The geometric waiting times and (4.6) give

\[
 \mathbb E\tau^r\le C_rK^r,
 \qquad
 \mathbb E(1+A_\tau+B_\tau)^r\le C_r(1+u+K)^r.                    \tag{4.12}
\]

Equations (4.5) and (4.10) give the sharper entropy estimate

\[
 \mathbb E\{\log(A_\tau!)+\log(B_\tau!);D_K\}
       \le C(1+u+K)\log(2+u+K).                                   \tag{4.13}
\]

For localization again use \(L_n=n^{1/16}\).  This cutoff is imposed only
**after** \(\tau^\circ\) has been constructed.  Let

\[
 \rho_A=\inf\{t:A_t\ge L_n\},\qquad
 \tau=\tau^\circ\wedge\rho_A.                                    \tag{4.13a}
\]

If \(\rho_A\le\tau^\circ\), include the reaction causing the crossing and
give the endpoint the inherited open-boundary label \(B\).  Thus the law
(4.4a) is never asserted after conditioning on an \(A\)-dependent stopping
time.

The clean \(B\)-path is bounded by (4.10).  Conditional on the unlocalized
\((B,C)\)-path, the operational time \(S^\circ\) is independent of the
marks driving \(A\).  Before a defect or the \(K\)-th service,
\(C\le n+1\), so (4.12) gives

\[
                  \mathbb E(1+S^\circ)^r\le C_rn^r(1+K)^r.        \tag{4.13b}
\]

At every deterministic operational time the initial-particle contribution
is at most \(u\), while the immigrant contribution is Poisson with mean at
most \(\alpha/\beta\).  Counting upcrossings of \(L_n\), conditionally on
\(S^\circ\), therefore gives

\[
 \mathbb P\{\sup_{t\le\tau^\circ}A_t\ge L_n\}
 \le C_Mn^{-M}.                                                     \tag{4.14}
\]

More explicitly, after the initial particles are labelled, an upcrossing
requires the immigrant subsystem to contain at least \(L_n-u-1\) particles
immediately before a birth.  Its stationary Poisson factorial tail supplies
the factor \(1/(L_n-u-1)!\); (4.13b) supplies only a polynomial operational-
time prefactor.  Since \(u+K=n^{o(1)}\), this is smaller than \(n^{-M}\)
for every fixed \(M\).  The same upcrossing calculation after multiplying
by any fixed polynomial of the endpoint and \(S^\circ\) proves the
endpoint-weighted form (1.9).  On its complement \(\tau=\tau^\circ\), so
(4.4a)--(4.5) give the one-sided inactive entropy bound on the actual
completion or defect endpoint.  This completes (1.6)--(1.11) and (1.13)
for the open rows.

## 5. Arbitrary \(\ell\), old debt, and actual endpoints

Three possible shortcuts are explicitly not used.

1. **No bounded-start substitution.**  All constants above are either
   independent of the initial cloud or multiplied by a fixed polynomial in
   \(1+u\).  The sole first-order inactive entropy term is bounded by
   \(C(1+u)\log(2+u)\), and is repaid by \(K\) services.
2. **No accumulated correction charge.**  For arbitrary fixed \(\ell\),
   the exact correction increment is
   \(\ell\cdot(X_\tau-X_0)\).  Fast redistribution cannot turn it into the
   sum of the absolute correction increments of the internal jumps.
3. **No post hoc endpoint replacement.**  The \(K\)-th service, first
   defect, and first cutoff crossing are all included.  Estimates
   (3.7)--(3.8) and (4.11)--(4.14) are post-jump and polynomially
   endpoint-weighted.

At a positive-debt entrance, the first included service is a genuine
old-particle service.  Continuing to \(K\) services does not require the
mark to remain positive, because surplus physical services at reflected
debt zero are allowed.  On the clean endpoint the active population is
\(n-K=n(1-o(1))\), so the episode never changes dimensional chart merely by
performing the intended services.

## 6. Predicate-level applicability to exactly 105 rows

The existing finite certificate is used only as follows.

* In each of its 99 `direct_C_killed_phase` incidences, a mixed linkage
  contains the physical source \(C\) and an active-free vertex.  This is the
  sole support premise of Section 3.  The molecularity-two catalogue itself
  gives the stripped menu \(\{0,A,B\}\), the degree-two lower-clock bound,
  and bounded service targets.
* In each of its six `open_poisson_regenerative_block` incidences, the
  normalized supports are exactly (4.1), and the normalized cap of \(B\) is
  zero.  These are precisely the premises of Section 4.

Strong connectivity and positive rates are quantified analytically after
these predicates are checked.  In particular, the finite certificate does
not inspect which directed edges occur, calculate \(p_*\), or test any
population path.

Combining Sections 2--4 proves the following candidate replacement for
Sections 4 and 6 of the failed frozen theorem.

> **Theorem 6.1 (direct/open multi-service repair).**  Fix any of the 99
> direct or six open hard one-active incidences, arbitrary strong
> orientations, arbitrary positive rate constants, a closed irreducible
> class, and an arbitrary fixed correction \(\ell\).  Every historically
> reachable positive-debt entrance (1.3), with \(u=n^{o(1)}\), has an
> all-reaction physical stopped episode with actual endpoints, path-labelled
> \(P/B\) boundaries, every fixed endpoint moment, and physical duration,
> satisfying
> \[
>  \mathbb E[W_\ell(X_\tau)-W_\ell(X_0)+\tau]
>       \le-cG_\ell(X_0)^3(1+u)\log n.                              \tag{6.1}
> \]
> The first service lowers incoming old debt; any later services after
> reflection reaches zero are surplus.  The theorem uses no bounded-start
> assumption.

This theorem is local.  Even after a strict PASS it would repair only the
105-row seam in the one-active theorem; it would not by itself certify a
hard pair or T3-2.
