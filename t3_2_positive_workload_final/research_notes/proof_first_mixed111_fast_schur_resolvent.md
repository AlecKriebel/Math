# Fast Schur resolvent for the 111 mixed generalized templates

**Independent proof-first derivation and scoped audit, 2026-08-12 PDT.**
This note audits only the 111 mixed-template part of
`hard317_non_base_open_common_w_kernel.md` at frozen SHA-256

```text
3f3319c71f6dd3705aad81ff225fda35d0ac2cbcbc0a54c5237b280ff9ba0836
```

The six separated templates are not treated here.  Neither are the twelve
no-history templates or the seventeen exact base-open templates.  The
asymptotic input is the generalized one-active entrance

\[
                         (U,V,I)=(u,n,0),\qquad u=n^{o(1)}.       \tag{0.1}
\]

In particular, this is not a theorem for the eight additional templates in
the 154-template physical hard menu, where the second macroscopic population
need not satisfy (0.1).

The result of the audit is **PASS for the mixed 111-template stopped theorem
after one mandatory sign repair**, subject only to the frozen support
partition.  The equalities asserted in (7.5)--(7.6) of the frozen note are
stronger than its one-sided terminal majorant and are not needed: throughout
the Foster proof they must be replaced by the corresponding upper
inequalities.  A mixed trace can lose a macroscopic amount of spectator
entropy before service, so a matching lower estimate is not available under
the stated hypotheses.  The proof below makes the required one-sided
statement.  It is independent of an orientation list and uses the finite
support table only for the facts that the 111 templates are mixed and that
none is an exact base-open proper pair.  All probability estimates follow
from a single fast Schur complement and a maximal-source killed Green
argument.

The central point is simpler than a general carrier cloud.  Once a
base-sourced reaction fires, a clean mixed episode contains at most two
\(V+I\)-sourced reactions before either returning to \(I=V-n=0\) or crossing
\(V<n\).  Thus arbitrary strong orientations enter only through fixed
outgoing probabilities at \(V+I\).  The first additional nonfast firing is
controlled sourcewise at its actual shifted state and is retained as a paid
endpoint.

## 1. Abstract mixed class and physical labels

Put

\[
 {\cal B}=\{0,U,2U\},\qquad
 {\cal C}=\{I,2I,U+I\},\qquad q=V+I.             \tag{1.1}
\]

There are two disjoint linkage supports, each containing at least two
complexes.  The proper linkage contains \(q\), the lower linkage does not,
and both directed linkage graphs are strongly connected.  All complexes lie
in

\[
                    {\cal B}\cup {\cal C}\cup\{q\}.            \tag{1.2}
\]

Rate constants are arbitrary fixed positive numbers.  Constants below may
depend on the fixed support, orientation, and rate vector, but never on
\(n\), \(u\), or the incoming reflected mark.

Work throughout on the reachable marked lift of one fixed closed irreducible
physical class, initialized at its class reference with zero reflected
marks.  A **relevant base** is a state of that lift with \(I=R=0\) and
selected mark \(D_V>0\).  This historical qualification is essential; an
arbitrary physical point on an absorbing face need not admit service.

Call a linkage **mixed** if, after deleting \(q\), it contains a member of
both \({\cal B}\) and \({\cal C}\).  Assume:

1. at least one linkage is mixed;
2. the proper support is not an exact pair \(\{aU,q\}\) with
   \(a\in\{0,1,2\}\).

These are precisely the analytic hypotheses used for the 111-template
block.  Exact proper pairs \(\{I,q\},\{2I,q\},\{U+I,q\}\) are allowed:
they have no base opening and hence no pure base loop.

Write

\[
                              R=V-n.                             \tag{1.3}
\]

Before service, \(R\ge0\).  Fix

\[
 L_n=\left\lfloor {n^{1/3}\over\log(n+e)}\right\rfloor.        \tag{1.4}
\]

Starting from (0.1), stop at the first of the following physical events,
always including the event-causing reaction.

* \(D_n\): the first reaction crossing \(V<n\);
* \(E_n\): the first nonfast reaction during one of the fast cleanup
  windows defined in Section 3;
* \(P_n\): a cutoff-causing reaction landing on
  \(I=R=0,U\ge L_n\);
* \(B_n\): every other first cutoff hit
  \(U\vee I\vee R\ge L_n\).

If one reaction has several labels, use physical priority \(D_n\) first,
then \(P_n\) or \(B_n\), and only then \(E_n\).  The labels are therefore
disjoint, and a boundary-causing insertion is never replaced by its
preboundary state.

## 2. The exact ideal Schur complement

Write a non-\(V\) complex as

\[
                       x=c_xU+b_xI.                              \tag{2.1}
\]

At a no-fast base only reactions sourced at \(y=c_yU\in{\cal B}\)
are enabled.  Their rates are

\[
                       a_e(u)=\kappa_e(u)_{\underline{c_y}}.     \tag{2.2}
\]

All reactions sourced at \(q\) have the common mass-action factor \(VI\).
Consequently, conditional on a \(q\)-sourced reaction, its target has the
state-independent law

\[
 p_t={\kappa_{q,t}\over\kappa_q},\qquad
 \kappa_q=\sum_{q\to z}\kappa_{q,z}.                            \tag{2.3}
\]

For the moment suppress every nonfast firing after leaving the no-fast
face.  A base-sourced edge \(e:y\to z\) then has one of three exact ideal
outcomes.

1. If \(z\in{\cal B}\), it is the direct base move

   \[
                         u\longmapsto u-c_y+c_z.                 \tag{2.4}
   \]

2. If \(z\in{\cal C}\), then \(R=0,I=b_z\ge1\).  The next
   \(q\)-sourced firing crosses \(V<n\).  If its target is \(t\), the
   retained service endpoint is

   \[
   U_D=u-c_y+c_z+c_t,\quad I_D=b_z-1+b_t,\quad R_D=-1.           \tag{2.5}
   \]

3. If \(z=q\), the state first has \(R=I=1\).  Draw \(t\) with law
   (2.3).  For \(t\in{\cal B}\) this gives the base continuation

   \[
                         u\longmapsto u-c_y+c_t.                 \tag{2.6}
   \]

   For \(t\in{\cal C}\), the first fast firing leaves \(R=0,I=b_t\),
   and a second target \(s\), independently distributed by (2.3), gives
   the service endpoint

   \[
   U_D=u-c_y+c_t+c_s,\quad I_D=b_t-1+b_s,\quad R_D=-1.           \tag{2.7}
   \]

Thus a clean open branch has one fast firing before a no-fast return, or at
most two before service.  In particular,

\[
 |U_D-u|\le4,\qquad 0\le I_D\le3.                               \tag{2.8}
\]

Let \(k_Q(u,u')\) and \(k_S(u,d)\) be the sums of (2.2), multiplied by the
probabilities in (2.3), for the nonself continuation and service outcomes
above.  An outcome (2.6) with \(t=y\) is an exact return of the complete
physical population and is deleted.  Put

\[
 \Lambda(u)=\sum_{u'}k_Q(u,u')+\sum_dk_S(u,d),\qquad
 Q(u,u')={k_Q(u,u')\over\Lambda(u)},\quad
 S(u,d)={k_S(u,d)\over\Lambda(u)}.                              \tag{2.9}
\]

These formulas are used only when \(\Lambda(u)>0\).  They are the exact
Schur complement of all clean physical self returns.  Indeed, each visit
to the base selects a base-sourced clock by (2.2), and an opening selects
its fast target by (2.3).  Repeating a self outcome and summing the
geometric series gives exactly the normalization in (2.9).  Elapsed time
is not erased; it is restored in Section 7.

### Lemma 2.1 (the diagonal inverse is uniformly harmless)

For the abstract mixed class above, the clean exact-return probability
before the next nonself ideal macro is bounded away from one, uniformly in
the enabled base population.

#### Proof

An exact return can only use

\[
                         aU\longrightarrow q\longrightarrow aU. \tag{2.10}
\]

If either directed edge is absent, this return has probability zero.  If
both are present, the proper support contains a complex outside
\(\{aU,q\}\), by hypothesis.  Strong connectivity supplies a directed
edge leaving this proper subset.  Its source is either \(aU\) or \(q\).
In the first case it competes with the opening using the identical
falling-factorial source.  In the second it has a fixed conditional
probability in (2.3).  Hence every traversal of (2.10) has a fixed positive
chance to leave the two-node block.  Taking the minimum over the at most
three base complexes proves the assertion. \(\square\)

This is the only pure-renewal estimate needed for the mixed group.  The
false uniform estimate for an exact base-open proper pair is not being
reintroduced: those seventeen supports were removed before this lemma.

## 3. Sourcewise ordered insertion at the shifted cleanup

We now restore the true physical competition in an open state.  Before
service and below the cutoff, every fast window occurring in (2.5)--(2.7)
satisfies

\[
  V\ge n,\qquad 1\le I\le2,\qquad U\le u+4.                  \tag{3.1}
\]

The total fast and nonfast rates obey

\[
 \lambda_f=\kappa_qVI\ge c n I,\qquad
 \lambda_{\rm nf}\le C(1+U+I)^2.                               \tag{3.2}
\]

The second inequality is just binary molecularity, summed over the fixed
edge set.

### Lemma 3.1 (sourcewise two-window estimate)

Condition on the identity of the initiating base edge \(e\) at population
\(u\).  For every fixed \(p\),

\[
 \begin{aligned}
 \mathbb P_e\{\hbox{a nonfast insertion before clean completion}\}
     &\le {C(1+u)^2\over n},\\
 \mathbb E_e[(1+U_E+I_E+|R_E|)^p;
                 \hbox{that insertion}]
     &\le {C_p(1+u)^{p+2}\over n}.                              \tag{3.3}
 \end{aligned}
\]

The inserting reaction is included in the endpoint.  The same bounds hold
after the exact-return inverse of Lemma 2.1.

#### Proof

At a fixed open state, the exact first-clock probability that a nonfast
reaction precedes the next fast reaction is

\[
 {\lambda_{\rm nf}\over\lambda_f+\lambda_{\rm nf}}
       \le {C(1+u)^2\over n}                                    \tag{3.4}
\]

by (3.1)--(3.2).  A direct cofactor target has one such window.  An opening
to \(q\) has one window before its first downcrossing and, only when that
downcrossing targets \({\cal C}\), a second window at the shifted state

\[
 (U,I,R)=(u-c_y+c_t,b_t,0).                                    \tag{3.5}
\]

These are the two possible temporal orders of the additional insertion
relative to the distinguished first downcrossing.  Both states satisfy
(3.1), so their sum satisfies the first line of (3.3).

One binary reaction changes each coordinate by a bounded amount.  At the
included insertion endpoint,

\[
                  1+U_E+I_E+|R_E|\le C(1+u).                   \tag{3.6}
\]

Multiplying (3.4) by (3.6) proves the second line.  Finally, the number of
exact clean returns before a nonself macro has a geometric tail with fixed
parameter by Lemma 2.1.  Summing (3.3) over those attempts changes only its
constant. \(\square\)

Equivalently, if \(K_e^{\rm id}\) is the ideal source-
\(e\) macro and \(K_e^{\rm cl}\) its true no-insertion part, then, in every
degree-\(p\) actual-endpoint norm,

\[
 0\le K_e^{\rm id}-K_e^{\rm cl}
       \le {C_p(1+u)^{p+2}\over n}\,a_e(u).                    \tag{3.7}
\]

This is a relative, sourcewise statement.  It neither takes a supremum of
\(L_n^2/n\) over a long excursion nor conditions on a prescribed reaction
word.

## 4. Maximal-source killed spectator Green

Let

\[
 d=\max\{c:\ cU\hbox{ belongs to either linkage}\}.             \tag{4.1}
\]

For all sufficiently large \(u\), every base complex is enabled.  After
the self-return deletion in (2.9), a macro sourced at \(dU\) either

* services;
* continues to a strictly smaller base population.

If the only displayed outcome of one opening is the self return, the
strong-cut proof of Lemma 2.1 supplies a nonself outcome with the same
degree-\(d\) source factor.  Every positive continuation is sourced at
degree at most \(d-1\).  Hence

\[
 \Lambda(u)\asymp (1+u)^d,\qquad
 \mathbb P_u\{U_{1}>u\}=O((1+u)^{-1}),                          \tag{4.2}
\]

and a fixed fraction of the effective degree-\(d\) mass is decreasing or
killed.  This conclusion is orientation-independent.

### Lemma 4.1 (compact residual accessibility)

From every nonstatic no-fast base in the abstract mixed class, the ideal
trace has a positive-probability path to service.  On the reachable lift of
a closed irreducible physical class, a static no-fast base has zero
historical \(V\)-debt.

#### Proof

Choose a mixed linkage and a base complex \(eU\) in it.  If \(u\ge e\),
follow a directed linkage path from \(eU\) to its first ordinary cofactor
complex.  Along a base part of the path, the residual population

\[
                             r=u-e\ge0                            \tag{4.3}
\]

is preserved: after reaching a complex \(z\), the state contains
\(r+z\).  If the path passes through \(q\), choose its prescribed outgoing
edge with the positive probability (2.3).  A first ordinary cofactor
target at \(R=0\) is followed by service, exactly as in (2.5) or (2.7).
Thus service is accessible.

It remains only to reach such an \(eU\) when \(u<e\).  Choose \(e\) minimal
over the mixed linkages.  If a base complex is enabled, it lies in the
other, nonmixed linkage.  A nonmixed linkage containing a base complex is
base-only after deleting \(q\); the alternative, cofactor-only type has no
enabled source at \(I=0\).  If the base-only linkage is the proper linkage,
it has at least two base complexes; otherwise it would be the excluded
exact pair \(\{aU,q\}\).  Strong connectivity lets one follow a base path
to its maximal base degree \(m\).  This raises the population to at least
\(m\).  If \(m\ge e\), we are done.  The sole remaining degree pattern is
\(m=1,e=2\), in which case the base-only support contains both \(0\) and
\(U\).  Repeating a positive path from \(0\) to \(U\) raises the
population from zero or one to two.  Again the mixed base becomes enabled.
This argument uses the three possible molecular degrees, not an orientation
enumeration.

If no base source is enabled, no reaction is enabled at \(I=0\), so the
physical state is absorbing.  It need not have been globally unreachable:
a transient path with residual molecules can land there.  What is needed
here is the closed-class statement.  If this absorbing state belongs to the
closed irreducible physical class on which the reflected lift is built,
irreducibility forces that class to be the singleton state.  Its marked lift
is initialized there with zero mark, and therefore it cannot carry positive
historical debt.  In particular, a no-fast continuation from a relevant base
cannot land at a static base: before service it restores the same positive
incoming mark, while closedness keeps its physical endpoint in the fixed
class. \(\square\)

For a fixed compact set of base populations, Lemma 4.1 gives finitely many
positive service paths.  Enlarging the compact set to contain them yields
\(M<\infty\) and \(\eta>0\) such that, from every relevant compact state,
service or the outer drift region is reached within \(M\) ideal macros with
probability at least \(\eta\).  This is the compact minorization; no finite
state box is being used to infer the large-population estimate.

Put

\[
 F_\theta(u)=\exp\{\theta u\log(u+e)\},\qquad 0<\theta<\tfrac12. \tag{4.4}
\]

For a positive jump \(j\le2\),

\[
 {F_\theta(u+j)\over F_\theta(u)}\le C_j u^{\theta j}.          \tag{4.5}
\]

Its probability is \(O(u^{-1})\), so its normalized contribution is
\(O(u^{-1+2\theta})=o(1)\).  A degree-\(d\) decreasing move has ratio
\(O(u^{-\theta})\), and a service outcome contributes zero to \(QF\).
Equations (4.2), (4.5), and the compact minorization give, for
\(0<\theta'<\theta<1/2\),

\[
                  (I-Q)^{-1}F_{\theta'}(u)
                       \le C_{\theta',\theta}F_\theta(u).        \tag{4.6}
\]

Polynomial weights have a sharper start-polynomial version.  If
\(f_m(u)=(1+u)^m\), the same maximal-source comparison gives, outside a
compact set,

\[
                 (I-Q)f_{m+1}(u)\ge c_m f_m(u).                 \tag{4.7}
\]

Indeed, a dominant decrement loses order \((1+u)^m\), while a positive
lower-degree move has probability \(O(u^{-1})\) and changes
\(f_{m+1}\) by only \(O(u^m)\).  A dominant service gives an even larger
loss.  The positive residual in (4.7) is compactly supported and is removed
by the finite killed Green corrector supplied by Lemma 4.1.  Therefore, for
every fixed \(m\),

\[
             (I-Q)^{-1}f_m(u)\le C_m(1+u)^{m+C_m}.              \tag{4.8}
\]

The binomial recursion for the killed macro count gives all its fixed
moments with the same kind of polynomial start bound.

## 5. Paid event and boundary estimates

Let \(\widehat Q\) be the actual clean continuation kernel below the cutoff.
Every clean branch is an ideal branch multiplied by the probability of no
insertion in its one or two fast windows.  Hence, entrywise,

\[
                               0\le\widehat Q\le Q.              \tag{5.1}
\]

Summing the endpoint-weighted estimate (3.3) with (4.8), for every fixed
\(p\), gives

\[
 \mathbb E_{(u,n,0)}[(1+U_E+I_E+|R_E|)^p;E_n]
       \le {C_p(1+u)^{C_p}\over n}.                             \tag{5.2}
\]

This includes insertions occurring inside would-be exact self returns.

The exponential Green estimate also gives the maximal-population tail

\[
 \mathbb P_u\{\max U\ge k\}
       \le C F_\theta(u)\exp\{-c k\log(k+e)\}.                  \tag{5.3}
\]

Before the first insertion, \(I\le2,R\le1\); at the included first
insertion their values remain bounded by an absolute constant.  Thus, for
large \(n\), a mixed episode can reach the cutoff only through its
\(U\)-coordinate.  Since \(u=n^{o(1)}\) and
\(L_n=n^{1/3+o(1)}\), (5.3) yields, for every fixed \(p,M\),

\[
 \mathbb E[(1+U_\sigma+I_\sigma+|R_\sigma|)^p;
                  P_n\cup B_n]\le C_{p,M}n^{-M}.                \tag{5.4}
\]

The reaction causing the hit changes \(U\) by a bounded amount, so its
actual endpoint has \(U\le L_n+4\).  Equation (5.4) therefore also pays any
fixed factorial-polynomial reward, including the common fourth-power
potential below.

The ideal killed trace services almost surely by (4.6) and Lemma 4.1.
The only mass removed from it is (5.2) or (5.4).  Consequently

\[
                         \mathbb P(D_n)=1-n^{-1+o(1)}.           \tag{5.5}
\]

Moreover, (4.8), (5.2), and (5.4) give arbitrary fixed polynomial moments
of every actual terminal endpoint.

## 6. Actual service entropy

Fix the pair-wide vector \(\ell\), and write the spectator part of the
factorial entropy as

\[
                       B_\ell(u)=\log(u!)+\ell_Uu.               \tag{6.1}
\]

Since \(B_\ell\) is bounded below on the nonnegative integers, add a fixed
constant and write \(\overline B_\ell\ge1\).  This does not change any
increment.  Choose \(C_0>6\) and put

\[
 h(u)=\overline B_\ell(u)+C_0\log(u+e).                          \tag{6.2}
\]

### Lemma 6.1 (terminal, not cemetery, majorant)

There is a bounded nonnegative corrector \(\chi\) such that

\[
 Q(h+\chi)(u)+S\overline B_\ell(u)-(h+\chi)(u)\le0             \tag{6.3}
\]

at every relevant base.  Consequently the actual service endpoint obeys

\[
 \mathbb E[B_\ell(U_D)-B_\ell(u);D_n]
       \le C\log(u+e)+C+{C(1+u)^C\over n}.                      \tag{6.4}
\]

#### Proof

For a bounded positive jump \(j\),

\[
 B_\ell(u+j)-B_\ell(u)=j\log u+O(1),                           \tag{6.5}
\]

whereas a decrement by at least one costs \(-\log u+O(1)\).
Every degree-\(d\) nonself outcome is either a decreasing continuation or
a service.  In the service case (2.8) bounds its spectator gain by four,
while termination deletes the \(C_0\log(u+e)\) term from (6.2).  Thus every
dominant outcome contributes at most \(-c\log u\) for large \(u\).
Positive continuations have total probability \(O(u^{-1})\) by (4.2), and
their entire logarithmic cost is \(O((\log u)/u)\).  Therefore

\[
 Qh(u)+S\overline B_\ell(u)-h(u)<0                              \tag{6.6}
\]

outside a compact set.

Let \(g\) be the positive part of the left side of (6.6), and set
\(\chi=(I-Q)^{-1}g\).  The function \(g\) has finite support.  Compact
transience and the strong Markov property at its support show that \(\chi\)
is bounded.  Since \((I-Q)\chi=g\), (6.3) follows.

For the actual stopped trace, clean continuation and service kernels are
subkernels of \(Q\) and \(S\).  All functions in (6.3) are nonnegative, so
deleting defect and boundary mass can only improve the inequality.
Iteration gives

\[
 \mathbb E[\overline B_\ell(U_D);D_n]
       \le \overline B_\ell(u)+C_0\log(u+e)+\|\chi\|_\infty.    \tag{6.7}
\]

Subtracting \(\mathbb P(D_n)\overline B_\ell(u)\) produces one additional
term \((1-\mathbb P(D_n))\overline B_\ell(u)\), bounded by (5.2)--(5.5).
This proves (6.4). \(\square\)

### Remark 6.2 (why the equality in the frozen note is false)

The one-sided sign in (6.4) cannot in general be upgraded.  One of the 111
mixed supports is

\[
 L_+=\{0,2U,q\},\qquad L_0=\{U,I,2I\}.                          \tag{6.8a}
\]

Give both linkages the strong cyclic orientations

\[
 0\longrightarrow q\longrightarrow2U\longrightarrow0,
 \qquad U\longrightarrow I\longrightarrow2I\longrightarrow U, \tag{6.8b}
\]

and take unit rates.  Its ideal no-fast Schur trace has, at population
\(j\), the three clocks

\[
 j\to j-2\text{ at rate }j(j-1),\qquad
 j\to j+2\text{ at rate }1,\qquad
 \text{service at }U_D=j+1\text{ at rate }j.                    \tag{6.8c}
\]

The required bases are not artificial points outside the historical class.
For \(u,n\ge1\) of the same parity, repeat

\[
        0\to q,\qquad I\to2I,\qquad2I\to U                     \tag{6.8c'}
\]

\(n\) times from the origin, use \(2U\to0\) to reduce the spectator to
its parity representative, and use clean \(0\to q\to2U\) cycles to reach
\((u,n,0)\).  Conversely, from \((u,n,0)\), repeat
\(U\to I\), \(q\to2U\) exactly \(n\) times and then use
\(2U\to0\) to return to the origin.  Thus these bases lie in the origin's
closed communicating class, and the path which raises \(V\) gives a
historically positive selected mark.

Starting from large \(u\), the probability that the first
\(\lfloor u/8\rfloor\) effective events are all downward is bounded below
by a positive constant, because

\[
 \prod_{j=u,u-2,\ldots,\,3u/4}
 {j(j-1)\over j(j-1)+j+1}\ge c>0.                              \tag{6.8d}
\]

After this descent, the exponential maximal-source estimate makes the
chance of returning above \(7u/8\) before service
\(\exp\{-c'u\log u\}\).  The same estimate bounds the positive terminal
overshoot above the starting level by \(o(u\log u)\).  Therefore

\[
             \mathbb E[B_\ell(U_D)-B_\ell(u)]\le-c''u\log u    \tag{6.8e}
\]

for all large \(u\), after changing constants for \(\ell_U\).  Taking, for
example, \(u=\lfloor\exp\sqrt{\log n}\rfloor=n^{o(1)}\), the right side is
not \(o(\log n)\).  The true insertion error is
\(n^{-1+o(1)}\) by Section 3 and does not alter this conclusion.  Thus the
frozen assertions with equality are genuinely false, whereas their upper
inequality—and hence the fourth-power drift—remains valid.

Now put

\[
 G_\ell(x)=K_\ell+\sum_j\log(x_j!)+\ell\mathbin\cdot x,
 \qquad W_\ell(x)=G_\ell(x)^4,                                 \tag{6.8}
\]

with \(K_\ell\) fixed so that \(G_\ell\ge1\).  At service,
\(V_D=n-1\), so its active factorial increment is exactly \(-\log n\).
Equations (5.2), (5.4), and (6.4), with \(\log(u+e)=o(\log n)\), give the
one-sided estimate actually required by the Foster argument:

\[
 \mathbb E\Delta G_\ell\le-\log n+o(\log n).                  \tag{6.9}
\]

This retains the actual \(U_D,I_D\) in (2.5) or (2.7).  No service endpoint
is sent to a cemetery state.  Polynomial endpoint bounds also imply, for
each fixed \(r\),

\[
                              \mathbb E|\Delta G_\ell|^r=n^{o(1)}. \tag{6.10}
\]

For clarity, (6.10) is obtained by splitting the disjoint labels.  On
\(D_n\), use (2.8) and the polynomial spectator moments.  On \(E_n\), use
the endpoint-weighted estimate (5.2).  On \(P_n\cup B_n\), the included
endpoint is deterministically below \(L_n+4\) and (5.4) is available with
arbitrarily large \(M\).

## 7. Physical duration and common fourth-power drift

At every nonstatic no-fast base, an enabled falling factorial is at least
one.  Thus the holding time to the next base-sourced reaction has all fixed
moments bounded above by constants.  Lemma 2.1 gives a fixed geometric
moment bound for the number of exact self attempts.  Every open holding
time is dominated by an exponential clock of rate \(cn\).  Restoring all
of these times and applying the binomial additive-functional recursion to
the macro-count estimates after (4.8) yields, for each fixed \(p\),

\[
                 \mathbb E_{(u,n,0)}\sigma_n^p
                       \le C_p(1+u)^{C_p}.                       \tag{7.1}
\]

This is a physical-time statement: no elapsed exact-return time has been
discarded.

At the initial point, \(G_\ell(X_0)=\Theta(n\log n)\).  The identity

\[
 \Delta W_\ell
 =4G_\ell^3\Delta G_\ell+6G_\ell^2(\Delta G_\ell)^2
   +4G_\ell(\Delta G_\ell)^3+(\Delta G_\ell)^4                 \tag{7.2}
\]

together with (6.9)--(6.10) makes the last three terms
\(o(G_\ell^3\log n)\).  Since (7.1) is \(n^{o(1)}\) under (0.1), the
physical duration reward is smaller still.  Hence, for all sufficiently
large \(n\),

\[
 \mathbb E_{(u,n,0)}
   [W_\ell(X_{\sigma_n})-W_\ell(X_0)+\sigma_n]
      \le-cG_\ell(X_0)^3\log n.                                 \tag{7.3}
\]

Until \(D_n\), reflection is inactive in a positive incoming \(V\)-mark and

\[
                         D_V(t)=D_V(0)+V(t)-n.                   \tag{7.4}
\]

Thus \(D_n\) services one unit of actual historical debt.  Equation (7.3)
uses the same population potential \(W_\ell\) as adjacent charts; the
Schur and entropy correctors are proof devices only.

## 8. Scoped theorem and audit conclusion

> **Mixed generalized fast-Schur theorem.**  For every fixed strong
> orientation and fixed positive rate vector in any of the 111 mixed
> support templates of the generalized 146-template menu, every
> historically reachable positive-debt entrance (0.1) has the physical
> stopped block of Section 1.  It services one unit of old \(V\)-debt with
> probability \(1-n^{-1+o(1)}\), has arbitrary fixed endpoint and duration
> moments bounded by a polynomial in \(1+u\), pays both path-labelled
> included boundaries superpolynomially, retains the actual service
> entropy endpoint, and satisfies the common-\(W_\ell\) drift (7.3).

The proof is structural.  The support table is needed only to verify the
two hypotheses at the start of Section 1 and the count 111.  It is not used
to search state boxes, enumerate orientations, or cap reaction words.

Relative to the frozen note under audit, this derivation supplies the
mandatory inequality repair above and explicit proofs of its five hostile
replay points in the mixed scope:

1. (3.3)--(3.7) are the sourcewise ordered-insertion estimate at the actual
   shifted cleanup state;
2. Lemma 2.1 is the exact full pure-subgraph Schur contraction;
3. Lemma 4.1 proves compact residual accessibility, including transfer from
   a nonmixed base-only linkage;
4. (4.6)--(4.8) prove killed factorial and polynomial spectator Green
   bounds; and
5. Lemma 6.1 and Section 7 retain the terminal entropy and physical time.

No claim is made here for the six separated templates, where repeated full
proper regeneration genuinely occurs on an \(n\)-scale.  No incidence,
pair, global theorem, or publication flag is changed by this scoped PASS.
