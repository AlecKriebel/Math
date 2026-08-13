# Full all-clock joint-return theorem for the separated carrier

**Proof-first theorem, 2026-08-12 PDT.**  This note assembles the
orientation-free separated-scale theorem from frozen proof components and
their hostile audits.  It uses no enumeration of supports, orientations,
reaction words, or population boxes.  Every reaction clock is physical,
every terminal crossing reaction is included, and the stopping rule is
independent of the factorial-linear correction.

## 1. Statement

Put

\[
 q=A+C,\qquad
 \{q\}\subseteq{\cal C}
 \subseteq\{0,B,2B,C,2C,B+C,q\}.                         \tag{1.1}
\]

Let the directed reaction graph on \({\cal C}\) be strongly connected,
let all rate constants be fixed and positive, and fix one closed
irreducible population class \(\Gamma\).  Delete zero-displacement
reactions, which do not change the state process.  Define

\[
 {\cal F}={\cal C}\cap\{0,B,2B\},\qquad
 {\cal P}={\cal C}\cap\{C,2C,B+C\},                        \tag{1.2}
\]

and

\[
 m(b)=
 \begin{cases}
  1+b^2,&2B\in{\cal C},\\
  1+b,&2B\notin{\cal C},\
       {\cal C}\cap\{B,B+C\}\ne\varnothing,\\
  1,&B,2B,B+C\notin{\cal C}.
 \end{cases}                                               \tag{1.3}
\]

For fixed \(\ell\in\mathbb R^3\), choose \(K_\ell\) so that

\[
 G_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\cdot x\ge1,
 \qquad W_\ell(x)=G_\ell(x)^4.                             \tag{1.4}
\]

> **Theorem 1.1 (separated all-clock joint return).**  Let
> \(x_n=(a_n,b_n,0)\in\Gamma\) satisfy
> \[
>        h_n=\log{a_n\over m(b_n)}\longrightarrow\infty.    \tag{1.5}
> \]
> Then the following ordered alternatives are exhaustive.
>
> 1. If no member of \({\cal F}\) is enabled at \(b_n\), then \(x_n\)
>    is an absorbing singleton.
> 2. If an \({\cal F}\)-source is enabled but
>    \({\cal P}=\varnothing\), then \(A-C\) is an exact
>    stoichiometric invariant.  A divergent sequence (1.5) therefore
>    cannot occur in the one fixed class \(\Gamma\).
> 3. If an \({\cal F}\)-source is enabled and
>    \({\cal P}\ne\varnothing\), there is one statewise, all-clock
>    physical stopping rule \(x\mapsto\tau_x\), independent of \(\ell\),
>    such that \(\tau_x<\infty\) almost surely, every terminal reaction
>    is included, and, for all sufficiently large separated entrances,
>    \[
>    \boxed{\quad
>    \mathbb E_x[
>      W_\ell(X_{\tau_x})-W_\ell(x)+\tau_x]
>       \le-c_\ell G_\ell(x)^3
>                    \log{a\over m(b)}.\quad}               \tag{1.6}
>    \]
>
> For every fixed integer \(r\ge1\), the rule in Alternative 3 satisfies
> \[
>       \mathbb E_x\tau_x^r\le C_r(1+b)^r,                  \tag{1.7}
> \]
> and there is a finite \(q_r\), depending only on the fixed network and
> \(r\), such that
> \[
>       \mathbb E_x(1+|X_{\tau_x}-x|_1+\tau_x)^r
>              \le C_r(1+a+b)^{q_r}.                       \tag{1.8}
> \]

Constants may depend on the fixed graph, rates, class, \(r\), and
\(\ell\), but not on the entrance scale.

## 2. Exact physical stopping rule

At \(x=(a,b,0)\), put

\[
 \epsilon={m(b)\over a}=e^{-h},\qquad
 \bar\delta=\sqrt\epsilon=e^{-h/2}.                         \tag{2.1}
\]

Let \(p\in\{0,1,2\}\) be the spectator degree selected by (1.3), and fix
a sufficiently small constant \(c_0>0\).  Give first priority to the
included reaction fired from an open state whose endpoint crosses

\[
 A\notin[a/2,2a],\qquad
 C\ge c_0\bar\delta a,\qquad
 1+B^p\ge c_0\bar\delta a\quad(p\ge1).                     \tag{2.2}
\]

Call this label \(B_O\).  For \(p=0\), the spectator condition is absent.

At \(C=0\), a **clean macro** begins with one reaction sourced at an
enabled member of \({\cal F}\), thereafter retains only reactions sourced
at \(q\), and ends at the first actual return to \(C=0\).  Write

\[
                    k=A_{\rm start}-A_{\rm return}.         \tag{2.3}
\]

Repeat unmarked clean completed macros with \(k=0\).  Subject to the
priority of \(B_O\), an unmarked clean return with \(k\ge1\) is terminal
service \(S\).

If a reaction sourced below \(q\) fires while open, mark its first
occurrence, retain every later physical clock, and stop at the next actual
\(C=0\) return as \(E\), unless \(B_O\) occurs first.  The first marked
reaction may itself be the terminal \(C=0\) return.

Only after an unmarked clean \(k=0\) return, apply the completed-base guard

\[
                 1+B^p\ge {c_0\over2}\bar\delta a
                 \quad(p\ge1),                             \tag{2.4}
\]

and label such an endpoint \(B_0\).  Thus the exact priority is

\[
                    B_O\quad>\quad S\text{ or }E
                         \quad>\quad B_0,                   \tag{2.5}
\]

and

\[
                       \Omega=S\mathbin{\dot\cup}E
                                  \mathbin{\dot\cup}B,
 \qquad B=B_O\mathbin{\dot\cup}B_0.                        \tag{2.6}
\]

In particular, a long service or marked genealogy is never relabelled by
the narrower base guard, and a marked path never begins another base
macro.

## 3. Frozen, invariant, and physical-loss branches

If no member of \({\cal F}\) is enabled, every possible source requires
positive \(C\), so the base is frozen.  If \({\cal P}=\varnothing\), all
complexes lie in \({\cal F}\cup\{q\}\), and the functional \(A-C\) has
the same value on every complex.  It is therefore preserved by every
reaction.  At a cofactor-free state in one fixed class, \(A\) is fixed,
which excludes (1.5).

A cofactor-free endpoint with no enabled member of \({\cal F}\) is
absorbing, because every remaining source contains \(C\); since \(\Gamma\)
is closed, every reachable endpoint lies in \(\Gamma\), and irreducibility
then forces \(\Gamma\) to be that absorbing singleton.  Hence on the
nonfrozen active-loss branch no distinct no-\({\cal F}\) base endpoint is
reachable.

Suppose now that an \({\cal F}\)-source is enabled and
\({\cal P}\ne\varnothing\).  Choose an enabled \(f\in{\cal F}\) and a
simple directed path from \(f\) to its first \({\cal P}\)-vertex.  The
path is physically executable because every target creates the next
source.  At its last vertex \(q\) is enabled, and one nonself \(q\)-edge
lowers \(A\) by one.

On any fixed spectator compact, every chosen base edge has a fixed positive
conditional probability, while every chosen \(q\)-edge shares the common
factor \(AC\) with its competitors.  The bounded path therefore gives a
uniform compact killing/active-loss cut.  At large \(B\), the maximal
cofactor-free source gives the exterior cut in Section 4.  This is the
exact physical active-loss branch; failure of either cut is contained in
the frozen or invariant alternatives above.

This trichotomy, including its fixed-class exclusion, has an independent
strict PASS in
proof_first_separated_invariant_no_history_routing_audit.md,
SHA-256
cef9030583f0856a9243b93abece2a3f3eb3bb28912e438774d75946c24af1b1.

## 4. Clean completed-return Green theorem

Let

\[
 d=\max\{c:cB\in{\cal F}\}.                                \tag{4.1}
\]

For a clean completed macro sourced at \(cB\), let \(T\) be its number
of \(q\)-firings and let \(e=1\) when its base target is \(q\).  Exact
active balance and carrier balance give

\[
                k=T-e\ge0,\qquad
                B_\tau-b\le pk+(d-c).                      \tag{4.2}
\]

The exceptional case \(p=1,d=0\) is included: only \(B+C\) can create a
spectator molecule, and a completed carrier genealogy contains at most
\(k\) such targets.

If \(k=0\), every clean completion is exactly

\[
                 cB\longrightarrow jB,
 \qquad\hbox{or}\qquad
                 cB\longrightarrow q\longrightarrow jB,
 \qquad c,j\le d.                                          \tag{4.3}
\]

After literal population returns are contracted, a maximal-source
nonself return strictly lowers \(B\).  A positive return must be sourced
at degree \(c<d\).  Its source probability and raw factorial tilt obey,
for fixed \(0<\theta<1/2\),

\[
 (1+B)^{c-d}
 {e^{\theta G_\ell(A,B',0)}
       \over e^{\theta G_\ell(A,B,0)}}
 \le C(1+B)^{-(1-\theta)(d-c)}.                            \tag{4.4}
\]

Literal returns have a uniformly bounded diagonal inverse by the directed
cut out of \(\{dB,q\}\).  The physical active-loss history of Section 3
gives a fixed-block spectral gap on the remaining spectator compact.
Consequently the clean kernel, killed at service or localization, has a
same-exponent Green bound.  Its polynomial additive-functional hierarchy
also controls every fixed moment of the number of continuing \(k=0\)
macros.

On a clean service path, (4.2) pairs every positive spectator molecule
with either the lower source-degree factor or an active loss.  Before the
moving boundary,

\[
 (a)_{\underline k}^{-\theta}(1+B_\tau)^{\theta pk}
                       \le C\bar\delta^{\theta k},          \tag{4.5}
\]

so \(k\ge1\) carries the separated service factor.

The ledger, same-exponent Green theorem, literal-return cut, polynomial
hierarchy, and the warning that a critical genealogy need not have an
unweighted spectator moment all have an independent PASS in
proof_first_separated_clean_base_green_audit.md, SHA-256
96c72e11a6105013b8d7b6e2309da7c2dbebccfa0b72640bfb3cfe6cf1608b36.

## 5. Full open phase and raw terminal transforms

For a complex \(y\), put

\[
 M_x(y)=\prod_i(x_i+1)^{y_i},\qquad
 {\cal M}(x)=M_x(dB)=(1+B)^d.                              \tag{5.1}
\]

At an open state attach the last-target phase \(s\), with \(s=q\) after
a lower-to-\(q\) firing.  Define

\[
 V_\theta(x,s)=e^{\theta G_\ell(x)}
       \left({{\cal M}(x)\over M_x(s)}\right)^\theta
       \quad(C>0),
 \qquad
 V_\theta(x)=e^{\theta G_\ell(x)}\quad(C=0).               \tag{5.2}
\]

Inside (2.2), every lower monomial ratio
\(r_y=M_x(y)/M_x(q)\) is \(O(\bar\delta)\).  Bounded-degree factorial
comparison gives the sourcewise table

\[
 {\lambda_{yz}(x)\over\lambda_{\rm tot}(x)}
 {V_\theta(x+z-y,s')\over V_\theta(x,s)}
 \le
 \begin{cases}
  C r_y^{1-\theta}r_s^\theta,&y\ne q,\\
  C r_s^\theta,&y=q.
 \end{cases}                                                \tag{5.3}
\]

A phase-\(q\) exit can be free only once, because it sets a lower phase.
With \(\eta=\min\{\theta,1-\theta\}\), the full post-mark open kernel
\(K_{OO}\), killed at its next base return or \(B_O\), therefore satisfies

\[
 \|K_{OO}^2\|_{V_\theta}\le C\bar\delta^\eta,
 \qquad
 \|(I-K_{OO})^{-1}\|_{V_\theta}\le C.                      \tag{5.4}
\]

This Green operator retains arbitrary later lower-source reactions and
arbitrary carrier branching.

Let \(Q\) be the physical clean prefix kernel, killed at
\(S,E,B_O,B_0\).  Restrict first marks to causing reactions which do not
cross \(B_O\), and split them as

\[
                         R=R_B+R_O,                         \tag{5.5}
\]

where \(R_B\) itself lands at \(C=0\), while \(R_O\) remains open.  Let
\(T_{OE}\) be the exit from the open post-mark kernel to its next base
without an earlier boundary hit.  The exact \(E\)-terminal operator is

\[
       (I-Q)^{-1}
       \{R_B+R_O(I-K_{OO})^{-1}T_{OE}\}.                    \tag{5.6}
\]

Crossing marks and the complementary open exit belong to \(B_O\).
Formula (5.6) therefore includes a direct marked reaction such as
\(C\to0\), retains all later physical clocks, and never continues past
the completed marked return.

The first mark costs \(C\bar\delta^{1-\theta}\).  Since (5.2) is exactly
the raw exponential at both base endpoints, (5.4)--(5.6) yield

\[
 \mathbb E_x[e^{\theta\Delta G_\ell};E]
        \le C\bar\delta^{1-\theta}
        \le C e^{-\eta h/2}.                               \tag{5.7}
\]

For clean service, the completed ledger (4.2)--(4.5), rather than a
terminal divisor moment, gives

\[
 \mathbb E_x[e^{\theta\Delta G_\ell};S]
        \le C\bar\delta^\theta
        \le C e^{-\eta h/2}.                               \tag{5.8}
\]

The phase table has an independent PASS in
proof_first_separated_phase_corrector_open_green_audit.md, SHA-256
5286d3fbd5d57e92047f8db1339130c228498215bdd23d4d3ebcb1946db26114.
The exact physical first-mark resolvent is frozen in
proof_first_separated_first_mark_resolvent_lemma.md, SHA-256
d4c4baff29ffda942798f28fc69d4b30ab25ee2c8e13d1960a4ee20b6d772506.

The normalized raw-terminal theorem is frozen in
proof_first_separated_normalized_phase_marked_terminal_repair.md,
SHA-256
149c2edd9a8427a442a66e4f99c026be96313bfc4e5072f96d0aa380502ffa77.
Its independent hostile audit is frozen in
proof_first_separated_normalized_phase_marked_terminal_repair_independent_audit.md,
SHA-256
5dd855cbb52bd84b83886209b9a0dd96cb91229275037f759be7cdac85d6a0b1,
with verdict **STRICT PASS**.

## 6. Included boundary estimate

Put

\[
 L=\min\{a,\bar\delta a,
              (\bar\delta a)^{1/p}:p\ge1\}.                 \tag{6.1}
\]

Since \(\epsilon\ge a^{-1}\), one has \(L\ge ca^{1/4}\).  The entrance is
an \(o(1)\) fraction of the completed-base guard.  Every continuing clean
\(k=0\) return changes \(B\) by at most two, while the same-exponent clean
kernel has a strict contraction \(\rho<1\).  Hence a \(B_0\)-path contains
\(\Omega(L)\) contracted continuing returns and has raw endpoint-weighted
mass at most

\[
                              C\rho^{cL}.                   \tag{6.2}
\]

An excursion opens below half the spectator threshold.  Reaching any
component of (2.2) requires \(\Omega(L)\) bounded open reactions.  Pairing
steps in (5.4) gives corrected mass

\[
                    C(C\bar\delta^\eta)^{cL/2}.             \tag{6.3}
\]

At the included open endpoint every dynamic coordinate is \(O(a)\), and
conversion from \(V_\theta\) to the raw exponential costs at most
\(Ca^{2\theta}\).  When \(p=0\), species \(B\) occurs in no complex and
is constant on the fixed class.  Thus every fixed polynomial endpoint
mark costs only a fixed power of \(a\).  Equations (6.2)--(6.3) imply,
for every fixed \(N\) and every fixed nonnegative polynomial \(P\),

\[
 \mathbb E_x[e^{\theta\Delta G_\ell}P(X_\tau);B]
                         \le C_{N,P}a^{-N}.                 \tag{6.4}
\]

This includes an open crossing whose causing reaction lands directly at
\(C=0\), because the required pre-jump path is already counted in (6.3)
and the base reset is raw.

## 7. Almost-sure termination and physical time

At every preterminal open state, the aggregate \(q\)-source probability is
\(1-O(\bar\delta)\).  Every nontrivial \(q\)-firing lowers \(A\) by one,
whereas a lower-sourced firing raises \(A\) by at most one.  For a small
fixed \(t>0\), the embedded active increment therefore satisfies

\[
        \mathbb E[e^{t(A_{j+1}-A_j)}\mid{\cal F}_j]
                      \le e^{-\gamma}                       \tag{7.1}
\]

at every preterminal open state, with fixed \(\gamma>0\).  If \(\nu\) is
the number of state-changing reactions in one open excursion, the included
lower active boundary gives

\[
                    \mathbb P\{\nu>n\}
                       \le \exp(Ca-\gamma n),               \tag{7.2}
\]

and consequently

\[
                         \mathbb E\nu^r\le C_ra^r.          \tag{7.3}
\]

Thus every open excursion terminates almost surely, even for critical or
supercritical carrier offspring laws.  At every preterminal open state the
total physical rate is at least \(cAC\ge ca\).  Conditional exponential
holding-time bounds and (7.3) imply that the unique terminal long open
excursion has uniformly bounded physical-time moments.

Before that excursion, every continuing clean \(k=0\) macro has the
bounded form (4.3).  After literal returns are contracted, a maximal-source
trial is killed or lowers \(B\) with fixed probability, while a positive
move has probability \(O((1+B)^{-1})\).  The compact active-loss cut of
Section 3 and the exterior contraction imply

\[
 \mathbb P\{N_B>n\}\le C e^{tb-\gamma'n},\qquad
 \mathbb E N_B^r\le C_r(1+b)^r                            \tag{7.4}
\]

for the number \(N_B\) of contracted continuing trials.  Literal returns
expand into uniformly geometric blocks.  At every nonfrozen base, the
total rate is bounded below by a fixed positive constant.  Restoring all
base and open holding times proves

\[
                       \boxed{\mathbb E_x\tau^r
                                      \le C_r(1+b)^r.}      \tag{7.5}
\]

The endpoint estimate (1.8) comes directly from the included caps, not from
an unweighted moment of a critical genealogy.  An \(S\)- or \(E\)-endpoint
occurs below \(B_O\) and, by its terminal priority, is not continued beyond
its completed return; hence \(A,C\), and the dynamic spectator \(B\) are
\(O(a)\).  A \(B_O\)- or \(B_0\)-endpoint is the first crossing of the
same caps by a bounded reaction, and has the same polynomial size bound.
When \(p=0\), \(B\) is fixed on \(\Gamma\).  Combining this deterministic
endpoint bound with (7.5) proves (1.8).

More importantly, (7.2) proves almost-sure termination of every open
macro under the exact boundary priority (2.5), and (7.4) proves that only
finitely many continuing unmarked \(k=0\) base macros occur almost surely.
The first later mark, service, or included guard is therefore reached in
finite physical time.  Thus \(\tau_x<\infty\) almost surely for the exact
rule of Section 2.

The physical-duration theorem is frozen in
proof_first_separated_physical_duration_joint_return.md, SHA-256
504b87e600c382e9c82b88cf0ea88f87a6a4b6c7783202cc9cc2faa79fefc640.
Its hostile audit is frozen in
proof_first_separated_physical_duration_joint_return_audit.md, SHA-256
c9be124327288bbb45f42cbb005c9b96d854cfb629f94dd4c7cc61cc456ccb56,
with verdict **STRICT PASS ON THE PHYSICAL ACTIVE-LOSS BRANCH**.  Section 3
is exactly the routing required by that scope qualification.

## 8. Common fourth-power drift

The terminal labels \(S,E,B\) are disjoint and exhaustive.  Equations
(5.7)--(5.8) and (6.4) imply, for fixed \(c,\theta>0\),

\[
 \mathbb E_x[e^{\theta\Delta G_\ell};S]
 +\mathbb E_x[e^{\theta\Delta G_\ell};E]
       \le Ce^{-ch},\qquad
 \mathbb E_x[e^{\theta\Delta G_\ell};B]\le C_Na^{-N}.      \tag{8.1}
\]

Here \(h\le\log a\), \(h\to\infty\), and
\(G_\ell(a,b,0)\ge c_\ell a\log a\) for all sufficiently large separated
entrances.  In particular \(h=o(G_\ell(x))\).  Exponential Markov applied
to (8.1) shows that

\[
                     \Delta G_\ell\le-c'h                 \tag{8.2}
\]

with probability \(1-o(1)\).  Since \(G_\ell\ge1\), monotonicity of
\(t\mapsto t^4\) on the attainable range gives on (8.2)

\[
       W_\ell(X_\tau)-W_\ell(x)
                  \le-c''G_\ell(x)^3h.                    \tag{8.3}
\]

For the exceptional positive part,

\[
 ((G_\ell+u)^4-G_\ell^4)^+
        \le C_\theta(1+G_\ell^3)e^{\theta u/2},
 \qquad u\ge0.                                             \tag{8.4}
\]

Cauchy--Schwarz and (8.1) make its expectation
\(o(G_\ell(x)^3h)\).  No moment of a large negative entropy increment is
needed; such an endpoint only improves (8.3).

Finally, (1.3), (1.5), and (7.5) give

\[
                  \mathbb E_x\tau
                       =o(G_\ell(x)^3h).                    \tag{8.5}
\]

Combining (8.3)--(8.5) proves (1.6) with the same
\(W_\ell=G_\ell^4\) for every chart and every terminal label.

The raw-exponential fourth-power lift is frozen in
proof_first_separated_raw_exponential_w4_lift.md, SHA-256
3badb799468f6912659916ab2bc4ee556f5c113f00fbea01d106c88449cc0134.
Its independent hostile audit is frozen in
proof_first_separated_raw_exponential_w4_lift_audit.md, SHA-256
3cf72b58a328bb493aa48f9b1fd11ec164f49c4504f7a40c0dcc3a1d6062326e,
with verdict **STRICT PASS**.

## 9. Scope, rejected predecessors, and publication interface

The theorem is:

* fixed-class and exact on the frozen/invariant alternatives;
* valid for every strong orientation and every fixed positive rate vector;
* all-clock after the first mark, with arbitrary later marks and arbitrary
  carrier branching;
* exact at the direct-base first mark and every included boundary;
* almost surely finite and physical-time aware; and
* stated with the common fourth-power workload used by the global
  classwise composition.

It does **not** assert an unweighted scale-relative terminal spectator
moment.  Such a moment is false for critical carrier genealogies and is
unnecessary: the normalized phase weight is raw at completed returns, the
included boundary is paid edgewise, and physical time is controlled by the
active-coordinate reaction clock.

Two predecessor constructions are explicitly retired and must not be
cited as proofs:

1. proof_first_single_linkage_level_trace_completion.md, frozen at SHA-256
   08c216dcf5926484e39edcab22df9ab119cd45f63f3f605154d6193a01c9f558,
   stopped at the wrong logarithmic scale and failed hostile audit.
2. proof_first_single_linkage_full_all_clock_nested_carrier.md, frozen at
   SHA-256
   490f42487ec5045e17a7fa0dc1e69f61f836d17d0ee5ae3ce6af304fc7c230ac,
   stopped after an unmatched positive active entry and is false.

The present theorem replaces both with completed physical joint returns,
the exact \(B_O>S/E>B_0\) terminal priority, and the normalized raw
phase weight.  It is the publication-safe separated input to the
single-linkage theorem in at most three dynamic species.
