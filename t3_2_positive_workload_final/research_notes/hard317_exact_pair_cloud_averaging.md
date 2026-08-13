# Exact proper-cloud averaging and the unified leading trace

**Proof-first scoped note, 2026-08-11 PDT.  Audit status: incomplete.**  This note replaces a pathwise
pure-renewal split by an exact regenerative averaging of the proper
birth--death cloud.  It applies to every exact proper pair

\[
                  L_+=\{aU,V+I\},\qquad a\in\{0,1,2\},             \tag{1.1}
\]

in the seventeen hard exact-pair supports.  The calculation is analytic:
no orientation or reaction-word enumeration is used.  The finite support
tables below verify only the structural fact that the equality set is
proper.  All orientations are arbitrary strong orientations and all rates
are arbitrary fixed positive rates.

This is a claim-neutral proof component.  It changes no certification flag
and does not certify the global theorem.

A hostile audit accepts the exact carrier product, coboundary, structural
equality sets, and large-spectator Foster mechanism, but rejects Lemma 2.1
as proved: the sourcewise opened-excursion two-insertion Green inequality and
the shifted post-lower cleanup estimate remain open.  In particular, the
base-local-time hazard must be decomposed as
\(A_e=k_e(0)+\lambda_0\,\mathbb E_1J_e\); it is not simply the
occupation of an excursion started at level one.  Sections 2, 7, and 8 are
therefore conditional until those two inequalities are supplied.

## 1. The exact carrier product

Start at a no-fast base

\[
                            x=(u,v,0).                              \tag{1.2}
\]

While only proper reactions fire, level \(i=I\) has

\[
                    (U,V,I)=(u-ai,v+i,i).                          \tag{1.3}
\]

Write \(\rho=\alpha/\beta\), where \(\alpha\) and \(\beta\) are the
forward and reverse proper rates.  The birth and death rates are

\[
 \lambda_i=\alpha(u-ai)_{\underline a},\qquad
 \mu_i=\beta(v+i)i.                                               \tag{1.4}
\]

For \(a=0\) this is a positive recurrent immigration--death chain; for
\(a=1,2\) it is finite.  Its reversible occupation weights, normalized at
level zero, are exactly

\[
 {\pi_i\over\pi_0}
   =\rho^i{(u)_{\underline{ai}}
            \over i!(v+1)^{\overline i}}.                         \tag{1.5}
\]

Indeed, multiplication of the detailed-balance ratios gives

\[
 \prod_{j=0}^{i-1}{\lambda_j\over\mu_{j+1}}
 =\rho^i{prod_{j=0}^{i-1}(u-aj)_{\underline a}
             \over i!\prod_{j=1}^i(v+j)}
 =\rho^i{(u)_{\underline{ai}}
             \over i!(v+1)^{\overline i}}.
\]

The identity includes \(a=0\), with the convention
\((u)_{\underline0}=1\).

Let a lower edge \(e:y\to z\) have source

\[
                  y=c_yU+b_yI,qquad c_y+b_y\le2,                 \tag{1.6}
\]

and rate \(\kappa_e\).  Its propensity at carrier level \(i\) is
\(\kappa_e(u-ai)_{\underline{c_y}}(i)_{\underline{b_y}}\).
Define its un-killed effective hazard per unit occupation time of level zero
by

\[
 A_e^{(n)}(u,v)
 =\sum_{i\ge0}{\pi_i\over\pi_0}\,
   \kappa_e(u-ai)_{\underline{c_y}}(i)_{\underline{b_y}}.          \tag{1.7}
\]

Put

\[
                         w_a(y)=c_y+ab_y.                          \tag{1.8}
\]

Substitution of \(i=b_y+j\) in (1.7) gives the exact series

\[
\boxed{
 A_e^{(n)}(u,v)
 ={\kappa_e\rho^{b_y}(u)_{\underline{w_a(y)}}
       \over(v+1)^{\overline{b_y}}}
 \sum_{j\ge0}{\rho^j
       (u-w_a(y))_{\underline{aj}}
       \over j!(v+b_y+1)^{\overline j}} .}                       \tag{1.9}
\]

The algebra uses

\[
 { (b_y+j)_{\underline{b_y}}\over(b_y+j)!}={1\over j!},\qquad
 (u)_{\underline{a(b_y+j)}}
 (u-a(b_y+j))_{\underline{c_y}}
 =(u)_{\underline{w_a(y)+aj}}.
\]

In particular, (1.9) vanishes exactly when \(w_a(y)>u\).  If
\(w_a(y)\le u\), every term is nonnegative, the \(j=0\) term is one, and

\[
 1\le \sum_{j\ge0}{\rho^j
       (u-w_a(y))_{\underline{aj}}
       \over j!(v+b_y+1)^{\overline j}}
 \le \exp\!\left\{{C(1+u)^a\over v}\right\}.                    \tag{1.10}
\]

Consequently, uniformly for \(v\ge n/2\) and \(u<L_n\),

\[
 A_e^{(n)}(u,v)
 =\kappa_e\rho^{b_y}v^{-b_y}
      (u)_{\underline{w_a(y)}}
 \left[1+O\!\left({(1+u)^a\over n}\right)\right].              \tag{1.11}
\]

This is the promised effective source law.  Each cofactor in the lower
source costs one power of the active population, while the proper carrier
turns its source degree into the workload degree \(c_y+ab_y\).

## 2. Killing at the first lower reaction

Formula (1.9) uses the un-killed proper carrier.  We now show that it also
gives the first-lower trace, with a uniform relative error.  Fix

\[
             L_n=\left\lfloor{n^{1/3}\over\log(n+e)}\right\rfloor,
 \qquad \varepsilon_n={CL_n^3\over n}=o(1),                      \tag{2.1}
\]

and stop the carrier at its included physical boundary.  During one open
proper excursion let

\[
             J=\int_0^{\tau_0}\lambda_{\rm low}(I_s)\,ds,         \tag{2.2}
\]

where \(\tau_0\) is its return to level zero and
\(\lambda_{\rm low}\) is the sum of all lower propensities.

### Lemma 2.1 (uniform excursion perturbation)

Uniformly over all carrier states below the boundary,

\[
       \sup_i\mathbb E_iJ^q\le C_q\varepsilon_n^q,
       \qquad q\ge1.                                             \tag{2.3}
\]

For every feasible lower edge, if \(\widehat A_e^{(n)}\) is its exact
contracted first-lower hazard per unit base local time, then

\[
       \widehat A_e^{(n)}(u,v)
          =A_e^{(n)}(u,v)[1+O(\varepsilon_n)].                    \tag{2.4}
\]

The occupation-weighted version is sharper:

\[
       \widehat A_e^{(n)}(u,v)
          =A_e^{(n)}(u,v)
             \left[1+O\!\left({(1+u)^3\over n}\right)\right].     \tag{2.5}
\]

Whenever at least one lower source is feasible, the proper-only boundary
hazard is superpolynomially smaller than the sum of the feasible lower
hazards.  If no lower source and no proper opening is feasible, the face is
static and there is no trace to contract.

#### Proof

Below the boundary the total lower clock is at most \(CL_n^2\), while at
level \(i\ge1\) the proper death clock is at least \(cni\).  The proper
birth clock is at most \(CL_n^a\le CL_n^2\).  Comparing successive
downcrossings with the death clock gives

\[
 \sup_{i<L_n}\mathbb E_i\int_0^{\tau_0}
       \lambda_{\rm low}(I_s)\,ds
 \le {CL_n^2\over n}\sum_{j=1}^{L_n}{1\over j}
 \le {CL_n^3\over n}.                                           \tag{2.6}
\]

The birth/death ratio is \(O(L_n^2/n)=o(1)\), so a geometric downcrossing
decomposition and the binomial recursion for an additive functional prove
all moments in (2.3).

For an opened excursion, the probability density that edge \(e\) is the
first lower reaction is

\[
 \mathbb E\int_0^{\tau_0}\lambda_e(I_t)
      \exp\!\left\{-\int_0^t\lambda_{\rm low}(I_s)ds\right\}dt.  \tag{2.7}
\]

Removing the exponential gives its un-killed occupation.  The error is a
two-time occupation integral.  Split it according to the temporal order of
the two hazard insertions.  For the future part, the conditional remaining
total hazard is bounded by (2.6).  For the past part, reverse the proper
excursion using detailed balance (1.5), and use the same bound.  Thus the
error in (2.7) is at most \(C\varepsilon_n\) times the un-killed
edge occupation.  Adding the exact level-zero hazard proves (2.4).
If the two-time occupation is evaluated with the product (1.5), rather
than bounded at the moving cutoff, size bias by any binary lower propensity
leaves a factorial carrier tail and costs at most three powers of \(1+u\).
The same argument then proves (2.5).

Finally, a proper-only boundary excursion requires order \(L_n\) nested
births.  The product (1.5) bounds its mass by

\[
           \sum_{i\ge L_n-C}{(CL_n^a/n)^i\over i!},               \tag{2.8}
\]

which is superpolynomial.  \(\square\)

There is an exact regenerative interpretation of (2.4).  At level zero,
lower clocks compete with the proper opening.  If the opening wins, run one
proper excursion until return, boundary, or its first lower firing.  Erase
every completed proper excursion.  If \(p_e\) is the probability that
edge \(e\) fires in one opened excursion, its contracted hazard is

\[
 \widehat A_e
   =\lambda_e(0)+\lambda_0p_e.                                  \tag{2.9}
\]

After all exact returns are summed, the next lower edge is selected with
probability \(\widehat A_e/\sum_f\widehat A_f\).  Thus no direct base
escape is misclassified as an \(O(n^{-1})\) interrupted branch.

## 3. Leading sources and clean macros

At a base \(u\), define

\[
 m_a(u)=\min\{b_y:y\in L_0,\ w_a(y)\le u\}.                      \tag{3.1}
\]

By (1.11)--(2.4), sources with \(b_y=m_a(u)\) are exactly the leading
sources in the contracted trace.  In the actual seventeen supports,
subleading selection before the moving boundary obeys

\[
 \mathbb P\{b_y>m_a(u)\mid\hbox{next lower edge}\}
 \le
 \begin{cases}
 C\{(1+u)^3/n+(1+u)^4/n^2\},&m_a(u)=0,\\
 C/n,&m_a(u)>0.
 \end{cases}                                                     \tag{3.2}
\]

The second line uses the structural fact proved in Section 5 that every
base with \(m_a(u)>0\) belongs to a fixed finite set.  In the first line,
a one-cofactor binary source has \(w_a\le a+1\le3\), and a two-cofactor
source has \(w_a=2a\le4\).  At \(u<L_n\), (3.2) is \(o(1)\).

After the first lower reaction, run the proper carrier to its next no-fast
state.  The probability of a second lower reaction during that cleanup is
\(O(\varepsilon_n)\) by Lemma 2.1.  From a base in the finite singular set
it is \(O(n^{-1})\), with every fixed endpoint moment, because the
size-biased carrier level is bounded with a factorial tail.

Call the macro **leading clean** when its lower source has order
\(m_a(u)\) and no second lower reaction occurs before cleanup.  If its edge
is \(y\to z\), every nested proper birth/death pair cancels and its exact
no-fast endpoint is

\[
 \begin{aligned}
 u'&=u-w_a(y)+w_a(z),\\
 v'&=v+b_y-b_z.                                                   \tag{3.3}
 \end{aligned}
\]

Define the bounded proof corrector

\[
                           H_a(u,v)=v+m_a(u).                      \tag{3.4}
\]

For every leading clean macro,

\[
 \Delta H_a=m_a(u')-b_z\le0.                                    \tag{3.5}
\]

Indeed, \(b_y=m_a(u)\), while \(u'\ge w_a(z)\), so
\(m_a(u')\le b_z\).  Equality holds exactly when \(z\) is leading at its
endpoint.  This single coboundary applies on both the formerly “ordinary”
and “priority” bases.

## 4. Equality phases

For an equality macro sourced at \(y\), put

\[
                         r=u-w_a(y)\ge0.                           \tag{4.1}
\]

If its target is \(z\), then \(u'=r+w_a(z)\).  Define

\[
 {cal M}_{a,r}
   =\{y\in L_0:b_y=m_a(r+w_a(y))\}.                              \tag{4.2}
\]

An edge \(y\to z\) with \(y,z\in{\cal M}_{a,r}\) is an equality macro
and preserves \(r\), provided the next selected source is the preceding
target.  This is a chosen positive-probability subpath of the physical
trace; no fictitious phase is inserted into its endpoint.

### Lemma 4.1 (proper equality set implies a strong cut)

If \({\cal M}_{a,r}\) is a nonempty proper subset of the lower support,
then from every \(y\in{\cal M}_{a,r}\) there is a finite sequence of
leading clean macros which either leaves the equality class with a strict
\(H_a\)-drop or reaches a base at which a lower order is enabled.

#### Proof

Strong connectivity supplies a directed path from \(y\) to the complement
of \({\cal M}_{a,r}\).  Stop it at its first exit.  At each internal vertex
choose that vertex as the next lower source.  Equations (1.9) and (2.4)
give every chosen edge positive contracted probability, and (4.2) makes
every pre-exit macro an equality.  The first exiting target is not leading
at its endpoint, so (3.5) is strict; if a lower-order source has become
feasible earlier, the trace has reached the nonsingular alternative.
\(\square\)

The chosen-source probabilities need not be bounded uniformly when \(r\)
diverges.  Uniform global control comes instead from the maximal-degree
Foster argument in Section 6.  On the finite singular set, however, Lemma
4.1 immediately gives one fixed positive cut probability.

## 5. Structural verification for the actual supports

The following tables are support bookkeeping, not orientation
enumeration.  Each entry follows directly by comparing the cofactor degrees
in (3.1).

For \(a=0\):

| lower support | \({\cal M}_{0,0}\) | \({\cal M}_{0,1}\) | \({\cal M}_{0,r},r\ge2\) |
|---|---|---|---|
| \(\{I,2U,2I,U+I\}\) | \(\{I,2U,U+I\}\) | \(\{I,2U\}\) | \(\{2U\}\) |
| \(\{U,2U,2I,U+I\}\) | \(\{U,2U,2I\}\) | \(\{U,2U\}\) | \(\{U,2U\}\) |
| \(\{U,I,2I,U+I\}\) | \(\{U,I\}\) | \(\{U\}\) | \(\{U\}\) |
| \(\{U,I,2U,2I\}\) | \(\{U,I,2U\}\) | \(\{U,2U\}\) | \(\{U,2U\}\) |
| \(\{U,I,2U,2I,U+I\}\) | \(\{U,I,2U\}\) | \(\{U,2U\}\) | \(\{U,2U\}\) |
| \(\{U,I,2U,U+I\}\) | \(\{U,I,2U\}\) | \(\{U,2U\}\) | \(\{U,2U\}\) |

For \(a=1\), the four supports containing \(0\) have equality set equal
to their \(I\)-free part:

\[
\begin{array}{c|c}
\{0,2U,2I,U+I\}&\{0,2U\}\\
\{0,I,2U,2I,U+I\}&\{0,2U\}\\
\{0,I,2U,2I\}&\{0,2U\}\\
\{0,I,2U,U+I\}&\{0,2U\}.
\end{array}                                                       \tag{5.1}
\]

For the remaining support,

\[
 L_0=\{I,2U,2I,U+I\},\qquad
 {cal M}_{1,0}=\{I,2U\},\quad
 {cal M}_{1,r}=\{2U\}\ (r\ge1).                               \tag{5.2}
\]

For \(a=2\), the five supports containing \(0\) again have equality set
equal to their \(I\)-free part:

\[
\begin{array}{c|c}
\{0,I,2I,U+I\}&\{0\}\\
\{0,U,2I,U+I\}&\{0,U\}\\
\{0,U,I,2I,U+I\}&\{0,U\}\\
\{0,U,I,2I\}&\{0,U\}\\
\{0,U,I,U+I\}&\{0,U\}.
\end{array}                                                       \tag{5.3}
\]

For the remaining support,

\[
 L_0=\{U,I,2I,U+I\},\qquad {cal M}_{2,r}=\{U\}\quad(r\ge0).    \tag{5.4}
\]

Every set in (5.1)--(5.4) and in the source-zero table is nonempty and
proper.  This proves the structural hypothesis of Lemma 4.1 for every
actual exact-pair support.

The singular bases, namely those with the proper opening enabled but no
cofactor-free lower source enabled, are consequently exactly:

- \(u=0,1\) in the first source-zero row;
- \(u=0\) in each of the other five source-zero rows; and
- \(u=1\) in the source-one support (5.2).

There is no source-two singular base.  Thus the singular set is finite and
orientation independent.

## 6. The killed leading equality trace

Let \(Q_n\) be the leading clean kernel restricted to \(\Delta H_a=0\),
and let \(S_n\) contain its strict drops.  Put

\[
                F_\theta(u)=\exp\{\theta u\log(u+e)\},
                \qquad0<\theta<\tfrac12.                         \tag{6.1}
\]

### Proposition 6.1 (unified killed Green bound)

For each actual exact-pair support and all sufficiently large \(n\),

\[
                 (I-Q_n)^{-1}F_\theta(u)\le C_\theta F_\theta(u) \tag{6.2}
\]

before the moving boundary.  The same statement holds for every fixed
polynomial weight and for fixed moments of the occupied macro count.

#### Proof

Outside a fixed compact set, \(m_a(u)=0\).  The leading sources and every
equality target are then \(I\)-free.  Let \(dU\) be the unique maximal
degree \(I\)-free lower complex.  By (1.11), the probability that the next
leading source is not \(dU\) is \(O(u^{-1})+o(1)\).  Every edge from
\(dU\) either has an \(I\)-bearing target and is killed by a strict drop,
or has an \(I\)-free target of degree below \(d\) and decreases \(U\).
There is no distinct \(I\)-free complex of the same degree.

An equality edge sourced below degree \(d\) can raise \(U\) by at most two.
Therefore

\[
 {Q_nF_\theta(u)\over F_\theta(u)}
 \le C u^{-\theta}+C u^{-1+2\theta}+o(1),                        \tag{6.3}
\]

which is strictly below one outside a larger fixed compact set because
\(\theta<1/2\).  If \(d=0\), every outgoing edge from \(0\) is killed and
the same conclusion is immediate.

On the remaining finite set, Lemma 4.1 and Section 5 exclude a closed
equality-only class.  For fixed positive rates its finite substochastic
matrix therefore has spectral radius below one.  A bounded finite-state
corrector joins this compact estimate to (6.3) and proves (6.2).  The
polynomial and macro-count versions follow from the same Foster recursion.
\(\square\)

This proof also resolves the source-selection subtlety in Lemma 4.1: the
strong path is used only for compact nontrapping.  The unbounded part is
controlled by the actual dominant physical source \(dU\), not by assuming
that the preceding target must become the next source.

## 7. Finite singular prelude and global clean service

The finite-singular implementation can stop at its first nonsingular base
and hand off to the same \(F_\theta\)-weighted kernel.  Lemma 4.1 and the
finiteness in Section 5 give a geometric leading-macro count, uniformly over
the singular bases.  Before this handoff, for every fixed \(p\),

\[
 \mathbb E[N_{\rm sing}^p]\le C_p,\qquad
 \mathbb P\{\hbox{subleading or dirty macro}\}\le {C\over n},
 \qquad
 \mathbb E T_{\rm sing}^p\le C_p n^{2p}.                         \tag{7.1}
\]

The \(n^2\) scale is sharp only when the first feasible lower source has two
cofactors.  Equation (7.1) follows from (1.11): an order-\(b\) leading macro
has geometric trial count of order \(n^b\), \(b\le2\), while every raw
base wait has bounded moments on the finite set.  The \(O(n^{-1})\) dirty
bound is (3.2) plus the bounded-base version of Lemma 2.1, summed against
the geometric equality Green function.

Alternatively, no handoff is needed.  Run the unified leading clean trace
globally and count strict drops.  If the initial active level is \(n\), then
after

\[
                      q=m_a(u_0)+1\le3                            \tag{7.2}
\]

strict drops,

\[
 H_a(U_q,V_q)\le n+m_a(u_0)-q\le n-1.                            \tag{7.3}
\]

Since \(m_a\ge0\), (7.3) implies \(V_q\le n-1\).  Hence the raw physical
path must already have crossed from \(V=n\) to \(V=n-1\) at a proper death;
that firing is strict old-active service.  Proposition 6.1 may be iterated
at most three times, so the ideal leading clean block has factorial endpoint
occupation and all fixed macro-count moments.

For a subpower start \(u_0=n^{o(1)}\), (3.2), Lemma 2.1, and the polynomial
version of Proposition 6.1 give

\[
 \mathbb P\{\hbox{any trace defect before service}\}=n^{-1+o(1)},
 \qquad
 \mathbb E T^p\le n^{2p+o(1)}.                                  \tag{7.4}
\]

The proper carrier tail (2.7) and (6.2) make the included moving-boundary
event superpolynomial.  Thus the averaged trace supplies either the finite
singular prelude with an identical-weight handoff or one unified clean
service mechanism.

## 8. Scope still requiring independent audit

The exact product, first-lower perturbation, coboundary, actual-support
strong cut, and killed leading Green bound are proved above.  Promotion still
requires an independent replay of:

- the endpoint-weighted version of the dirty cleanup estimate;
- the entropy increment at the actual first-service endpoint;
- the fourth-power Taylor uniform-integrability estimate with the common
  chart potential; and
- the marked strong-Markov gluing at a physical boundary.

No certification flag is changed here.
