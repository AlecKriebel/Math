# The workload-only physical-time Foster lemma for level-set pairs

**Proof-first conditional composition lemma, 2026-08-12 PDT.**  This note
isolates the exact stochastic statement needed to promote a level-set pair
from local all-active drift to classwise positive recurrence.  It uses the
single linear workload preserved by the upper linkage.  There is no marked
factorial, chart potential, embedded-chain margin, or weighted seam.

The theorem below is conditional only on one explicit direct-death
occupation macro.  Finite computation is neither used nor needed.

## 1. Level-set network and exact workload identity

Fix a closed irreducible population class \(\Gamma\) of a reduced binary
stochastic mass-action network.  Constant coordinates have already been
deleted.  Suppose the two active linkage supports are \(T,R\), with

\[
 h\cdot y=2s\quad(y\in T),\qquad
 R=\{0\}\cup U,\qquad h\cdot u=s\quad(u\in U),          \tag{1.1}
\]

where \(h\in(0,\infty)^d\), \(s>0\), and \(U\) consists of distinct unary
complexes.  Give both linkages arbitrary fixed strongly connected labelled
graphs and arbitrary fixed positive rate constants.  Put

\[
                              H(x)=h\cdot x.             \tag{1.2}
\]

Parallel labelled channels are retained.  Projected zero-displacement labels
have already been discarded, so an ordinary jump below is an off-diagonal
physical transition.  The conditional Foster argument uses only (1.1); in
the exact 336 application \(d=3\) and
\(\operatorname{rank}\operatorname{span}(T-T)=2\).

This is proper on the reduced lattice.  For a lower unary vertex \(u\), set

\[
 \delta_u=\sum_{u\to0}\kappa_{u0},\qquad
 D=\{u\in U:\delta_u>0\},\qquad
 \beta=\sum_{0\to u}\kappa_{0u}.                       \tag{1.3}
\]

Strong connectivity of \(R\) gives \(D\ne\varnothing\): the last edge of a
directed path from a unary vertex to zero is sourced at an element of \(D\).
Every top reaction and every lower unary transfer preserves \(H\).  Thus the
physical generator has the exact global identity

\[
                 {\cal L}H(x)=s\beta
                    -s\sum_{u\in D}\delta_u x_u.        \tag{1.4}
\]

No upper clock is estimated or averaged in (1.4), regardless of its rate.

## 2. Direct-death boundary and macro hypothesis

Fix an integer \(k\ge1\), and define

\[
             {\cal D}_k=\{x\in\Gamma:x_u<k
                              \text{ for every }u\in D\}. \tag{2.1}
\]

Let \(C_R=\{x\in\Gamma:H(x)\le R\}\).  It is finite because \(H\) is
proper.  Choose \(R\) large enough that \(C_R\ne\varnothing\).

The load-bearing hypothesis is the following literal physical-time
statement.

> **Occupation macro \({\bf M}(k,R,\eta)\).**  There is \(\eta>0\) such
> that, for every \(x\in{\cal D}_k\) with \(x\notin C_R\), one may select an
> all-clock stopping time \(\tau_x\) satisfying:
>
> 1. \(\tau_x\) contains at least one ordinary off-diagonal physical jump;
> 2. \(\tau_x<\infty\) almost surely and
>    \({\mathbb E}_x\tau_x<\infty\);
> 3. its endpoint is the actual physical endpoint, with
>    \({\mathbb E}_xH(X_{\tau_x})<\infty\); and
> 4. the exact stopped workload inequality is
>    \[
>       {\mathbb E}_x\!\left[
>          H(X_{\tau_x})-H(x)+\eta\tau_x\right]\le0.  \tag{2.2}
>    \]
>
> The selection is a function of the current state and the fixed network
> data.  No condition is imposed on a future activation or reaction label.

A uniform negative constant on the right of (2.2) is stronger than needed.
The positive physical-time term is the coercive quantity.

Here is the stopped-integrability point in full.  For any almost surely
finite all-clock stopping time \(\tau\) with
\({\mathbb E}_x\tau<\infty\), let \(B_\tau\) be the aggregate number of
zero-source births and let \(N_{u,\tau}\) count the labels \(u\to0\).
Nonexplosion makes these counts finite pathwise, and the exact workload
balance is

\[
 H(X_\tau)-H(x)=s\left(B_\tau-
                    \sum_{u\in D}N_{u,\tau}\right).                 \tag{2.3}
\]

The aggregate birth clock has constant intensity \(\beta\).  The stopped
counting-process compensation formula, obtained first under bounded
time-and-count localization and then by monotone convergence, gives

\[
 {\mathbb E}_xB_\tau=\beta{\mathbb E}_x\tau.                         \tag{2.4}
\]

Since \(H(X_\tau)\ge0\), (2.3) gives the pathwise domination

\[
 \sum_{u\in D}N_{u,\tau}\le H(x)/s+B_\tau.                          \tag{2.5}
\]

Thus every direct-death count is integrable.  Applying the same localized
compensation formula to those counts now gives

\[
 {\mathbb E}_x\sum_{u\in D}N_{u,\tau}
 ={\mathbb E}_x\int_0^\tau
       \sum_{u\in D}\delta_uX_u(t)\,dt<\infty.                     \tag{2.6}
\]

Equations (2.3)--(2.6) also prove
\({\mathbb E}_xH(X_\tau)<\infty\); endpoint integrability is a
consequence of duration integrability, not an additional moment demand.
Taking expectations in (2.3) yields the exact stopped Dynkin identity

\[
 {\mathbb E}_x[H(X_\tau)-H(x)]
 =s\beta{\mathbb E}_x\tau
  -s{\mathbb E}_x\int_0^\tau
       \sum_{u\in D}\delta_uX_u(t)\,dt.                            \tag{2.7}
\]

Consequently the precise minimal occupation form of (2.2) is exactly

\[
 {\mathbb E}_x\int_0^{\tau_x}
       \sum_{u\in D}\delta_uX_u(t)\,dt
 \ge\left(\beta+{\eta\over s}\right){\mathbb E}_x\tau_x. \tag{2.8}
\]

Equivalently, with \(D_\tau=\sum_{u\in D}N_{u,\tau}\),

\[
                 s\,{\mathbb E}_x(D_\tau-B_\tau)
                         \ge\eta{\mathbb E}_x\tau_x.    \tag{2.9}
\]

Adding any fixed \(a>0\) to the right of (2.9), or \(-a\) to the right of
(2.2), is useful slack but is not part of the minimal theorem.

## 3. Pointwise complement needs no macro

Let

\[
        \delta_*=\min_{u\in D}\delta_u,\qquad
        c_k=s(\delta_*k-\beta).                         \tag{3.1}
\]

Increase \(k\), if necessary, so \(c_k>0\), and put

\[
                       \eta_0=\min\{\eta,c_k/2\}>0.    \tag{3.2}
\]

At \(x\notin{\cal D}_k\), (1.4) gives

\[
                         {\cal L}H(x)\le-c_k.          \tag{3.3}
\]

Let \(T_1\) be the next ordinary off-diagonal jump time.  In a nontrivial
irreducible class its rate \(q(x)\) is finite and positive.  The elementary
holding-time identity gives

\[
 {\mathbb E}_x\{H(X_{T_1})-H(x)+\eta_0T_1\}
 ={ {\cal L}H(x)+\eta_0\over q(x)}\le0.                \tag{3.4}
\]

The margin in (3.4) may vanish as \(q(x)\to\infty\).  This is harmless:
the proof below sums physical time, not embedded episode count.

## 4. Positive-duration episode tiling

For \(x\in C_R\), set \(N=0\) and \(S_N=0\).  Starting from
\(x\notin C_R\), define stopping times \(S_n\) recursively.
At \(S_n\):

* if \(X_{S_n}\in{\cal D}_k\), append the macro of Section 2;
* otherwise append the one-jump episode of Section 3.

Stop the recursion when an episode endpoint lies in \(C_R\).  Every
nonterminal episode contains at least one actual off-diagonal jump.  Chart
classification, active-set relabelling, or an algebraic declaration is not
an episode and consumes no index; all zero-time declarations are folded
into the rule which takes the next physical jump.

By the strong Markov property and (2.2), (3.4),

\[
 {\mathbb E}_x\!\left[
 H(X_{S_{(n+1)\wedge N}})-H(X_{S_{n\wedge N}})
 +\eta_0(S_{(n+1)\wedge N}-S_{n\wedge N})
 \middle|{\cal F}_{S_{n\wedge N}}\right]\le0,          \tag{4.1}
\]

where \(N\) is the first endpoint index in \(C_R\).  Summing gives

\[
             {\mathbb E}_xH(X_{S_{n\wedge N}})
                 +\eta_0{\mathbb E}_xS_{n\wedge N}
                         \le H(x).                     \tag{4.2}
\]

The induction behind (4.2) is integrable, not merely formal.  At every
nonterminal state, either (2.2) or (3.4) rearranges to

\[
 {\mathbb E}[H(\hbox{next endpoint})+\eta_0(\hbox{duration})
       \mid\hbox{current state}]\le H(\hbox{current state}).        \tag{4.3}
\]

Both terms on the left are nonnegative.  Starting from deterministic
finite \(H(x)\), (4.3) therefore supplies all first moments needed at the
next induction step.  The stopped count calculation (2.3)--(2.7) proves
the same fact directly from episode-duration integrability.  No polynomial
or exponential endpoint moment is used.

## 5. Conditional Foster theorem

> **Theorem 5.1 (workload-only physical-time Foster theorem).**  Assume the
> reduced level-set network (1.1) is nonexplosive and satisfies the
> occupation macro \({\bf M}(k,R,\eta)\) for some \(k,R,\eta\), with \(k\)
> large enough that the quantity in (3.1) is positive.  Then
> \[
>                    {\mathbb E}_x S_N
>                            \le {H(x)\over\eta_0}<\infty,             \tag{5.1}
> \]
> so every state has finite mean physical hitting time of the finite set
> \(C_R\).  The closed irreducible class \(\Gamma\) is positive recurrent.

### Proof

Let
\[
                         S_\infty=\lim_{n\to\infty}S_{n\wedge N}.
\]
Since \(H\ge0\), monotone convergence for the times in (4.2) gives

\[
                    \eta_0{\mathbb E}S_\infty\le H(x).                \tag{5.2}
\]

On \(\{N=\infty\}\), the episode endpoints contain an infinite subsequence
of ordinary physical jump times.  Nonexplosion forces their limit to be
infinite.  Hence (5.2) implies \({\mathbb P}(N=\infty)=0\), and (5.1)
follows.

For completeness, fix \(o\in C_R\).  The set \(C_R\) is finite.  For each
\(c\in C_R\), irreducibility supplies a finite actual labelled population
path from \(c\) to \(o\).  An attempt follows that path until either its
next prescribed label fires or a competing label fires, in which case the
attempt stops immediately.  Across the finitely many chosen path states,
the probability of completing the prescribed path has a positive uniform
lower bound \(p\), and the mean duration of one attempt has a finite uniform
upper bound \(a\).  The possible first competing endpoints form a finite
set \(E\).  By (5.1),

\[
 m=\begin{cases}
     \max_{e\in E}{\mathbb E}_eS_N,&E\ne\varnothing,\\
     0,&E=\varnothing
   \end{cases}
 <\infty.                                                          \tag{5.3}
\]

After a failed attempt, wait for this endpoint return to \(C_R\), then use
the path selected from the new state.  At every restart the conditional
success probability is at least \(p\), while the conditional mean cost of
the failed attempt and return is at most \(a+m\).  Thus the number of
attempts is dominated by a geometric variable and the mean hit of \(o\) is
finite.

If \(\Gamma\) is a singleton there is nothing more to prove.  Otherwise
the first ordinary jump from \(o\) has finite mean holding time and one of
finitely many endpoints.  Applying the preceding finite-mean hit bound
from each such endpoint gives a finite mean return time to \(o\).  Thus
\(\Gamma\) is positive recurrent. \(\square\)

## 6. Nonexplosion and fixed-class exceptions

For a binary network, nonexplosion is automatic here.  A degree-two source
cannot increase total molecule count because every target also has degree
at most two.  Every population-increasing channel therefore has source
degree zero or one.  The aggregate positive population drift is bounded by
\(C(1+|x|_1)\), and all jumps are bounded.  Localization followed by a Yule
comparison prevents population escape in finite time.  On a fixed
population sublevel there are finitely many states and bounded total rates,
so population-preserving upper reactions cannot accumulate infinitely many
jumps.

For the exact at-most-three-species \(h=(1,1,1)\) and permuted
\(h=(1,1,2)\) families, there are only two genuine reduction exceptions.

1. If the reduced class has no active reaction, irreducibility makes it a
   singleton.
2. On an exceptional common-catalyst face, every upper source contains a
   species \(Y\), the face has \(Y=0\), and \(Y\) is absent from the lower
   unary support.  Then \(Y\) is an exact full-network invariant.  It is
   fixed before the theorem is invoked, the upper linkage is inactive on
   that class, and the remaining network is an open unary linkage.

The latter reduction is positive recurrent directly.  Kill the unary
complex graph on first hitting zero.  Its subgenerator \(Q\) is transient
by strong connectivity, so \(v=(-Q)^{-1}{\bf1}>0\).  The linear function
\(v\cdot x\) has generator equal to a constant immigration term minus
\(\sum_i x_i\), up to the fixed labelled-rate convention.  It is a standard
linear Foster function.  Equivalently, the open unary linkage is weakly
reversible and deficiency zero.

No other closed no-service face is hidden in the theorem.  If an upper
source is active on a proper face, a strong upper path leaks from that face;
if the upper linkage is dead, strong connectivity of the open lower linkage
gives finite physical access to a direct-death unary unless the required
coordinate is the invariant just described.

## 7. Exact remaining macro for the two weights

For either weight, the hard analysis has exactly the same target.  Fix the
network, orientation, rates, class, \(k\), and a state
\(x\in{\cal D}_k\) with \(H(x)\) large.  Construct one all-clock stopping
time satisfying

\[
 {\mathbb E}_x\int_0^{\tau_x}
       \sum_{u\in D}\delta_uX_u(t)\,dt
 \ge\left(\beta+{\eta\over s}\right){\mathbb E}_x\tau_x,             \tag{7.1}
\]

with \(0<{\mathbb E}_x\tau_x<\infty\).  That is the precise minimal macro.
It need not bound the number of neutral upper reactions, reach a prescribed
complex by a fixed word, mix before the first lower event, or provide any
moment beyond first physical time.

For \(h=(1,1,1)\), a symbolic proof may use only the three exhaustive upper
activation geometries:

* a killed two-carrier Perron--Frobenius wedge;
* the dyadic two-minimum source-balance kernel; and
* the exact common-catalyst linear-chain kernel.

For completeness, fix a dormant pure-\(X\) ray and write the other species
as \(Y,Z\).  Dormancy excludes \(2X\).  Rank two forces at least one of
\(XY,XZ\).  Up to swapping \(Y,Z\): if both occur, one has the two-carrier
kernel; if only \(XY\) occurs and \(2Z\) occurs, one has the dyadic
two-minimum kernel; if only \(XY\) occurs and \(2Z\) is absent, rank two
forces the exact support \(\{XY,YZ,2Y\}\), the common-\(Y\)-catalyst
kernel.  This proves the symbolic exhaustion without listing orientations.

For \(h=(1,1,2)\), the exact upper supports are

\[
 \{C,2A,2B\},\quad \{C,2A,A+B\},\quad
 \{C,2B,A+B\},\quad \{C,2A,2B,A+B\}.                 \tag{7.2}
\]

Indeed the level-two shell is \(\{C,2A,A+B,2B\}\); its three quadratic
vertices are collinear, so rank two is equivalent to including \(C\) and
at least two of those vertices.

Supports containing the opposite pure double use the two-reservoir
source-balance kernel for propensities \(C\) and \(B(B-1)\).  The sole
no-opposite-double support \(\{C,A+B,2A\}\) uses the killed-complex linear
ascent to an \(A\)-occupied region, followed by an occupation/service
handoff.  A false uniform reaction-depth or \(O(H^{-1/2})\) entrance claim
is unnecessary: (7.1) charges all service accumulated during the complete
physical macro.

Once (7.1) is proved in these kernels, Theorem 5.1 performs the entire
global classwise composition under the single function \(H\).
