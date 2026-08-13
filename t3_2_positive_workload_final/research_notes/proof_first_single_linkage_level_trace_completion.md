# Level-trace completion of the three-species single-linkage branch

**Proof-first theorem, 2026-08-12 PDT.** This note supplies the stopped
carrier lemma left open in
*proof_first_single_linkage_structural_reduction_and_mesoscopic_gap.md*.
It treats arbitrary strongly connected orientations and arbitrary fixed
positive rate constants. The proof does not enumerate supports,
orientations, or population boxes. Its only finite structural input is the
binary molecular-degree order \(0<1<2\).

The main device is the exact level

\[
                              H=A-C.                           \tag{0.1}
\]

Every zero-level carrier reaction has zero \(H\)-reward, including nested
openings. A cofactor-bearing **target** lowers \(H\), while a
cofactor-bearing **source** can raise it. The latter clocks are not erased:
they are included and paid sourcewise against the killed Green descent.
This source/target distinction is essential.

No global certification flag is changed in this note.

## 1. Scope and theorem

After relabelling the separated failed tier, the one-linkage support obeys

\[
 \{q\}\subseteq{\cal C}\subseteq{\cal Z}\cup{\cal P},\qquad
 q=A+C,                                                       \tag{1.1}
\]

where

\[
 {\cal Z}=\{0,B,2B,q\},\qquad
 {\cal P}=\{C,2C,B+C\}.                                      \tag{1.2}
\]

The cofactor-free entrance is

\[
                   x=(a,b,0),\qquad a\longrightarrow\infty.   \tag{1.3}
\]

Put

\[
 m(b)=
 \begin{cases}
  1+b^2,&2B\in{\cal C},\\
  1+b,&2B\notin{\cal C},\
          {\cal C}\cap\{B,B+C\}\ne\varnothing,\\
  1,&B,2B,B+C\notin{\cal C}.
 \end{cases}                                                  \tag{1.4}
\]

The separated tier assumption is exactly

\[
                              m(b)=o(a).                       \tag{1.5}
\]

For fixed \(\ell\in\mathbb R^3\), choose \(K_\ell\) so that

\[
 G_\ell(x)=K_\ell+\log(A!)+\log(B!)+\log(C!)+\ell\cdot x\ge1,
 \qquad W_\ell=G_\ell^4.                                     \tag{1.6}
\]

> **Theorem 1.1 (separated all-clock level trace).** Fix the support,
> orientation, rates, one closed irreducible class, and \(\ell\). There
> are \(c,C>0\), a finite set \(F\), and an included physical stopping time
> \(\tau\) such that every sufficiently large entrance (1.3) satisfying
> (1.5) has
> \[
>  \mathbb E_x\!\left[
>       W_\ell(X_\tau)-W_\ell(x)+\tau\right]
>       \le-c\,G_\ell(x)^3\log a.                              \tag{1.7}
> \]
> Every reaction clock is retained. In particular, a
> \({\cal P}\)-sourced firing during an open \(q\)-window is stopped and
> included, not suppressed.
>
> The only alternatives are:
>
> 1. an old-\(A\) service;
> 2. an included paid \({\cal P}\)-source endpoint;
> 3. an exact promotion to an enabled-top or balanced-two-top chart,
>    followed by that chart's physical episode using the same \(W_\ell\);
> 4. an included moving-localization endpoint of superpolynomially small
>    weighted probability;
> 5. an invariant or absorbing face.
>
> Before an appended outer episode,
> \[
>                         \mathbb E_x\tau\le C(1+a)^2.          \tag{1.8}
> \]

The proof is sequencewise in the usual tier-compactness sense. If no finite
exception set \(F\) existed, a violating sequence would have a proper tier
subsequence, and the estimates below would give (1.7) on that subsequence.

## 2. Exact level algebra and the only paid clocks

For a complex \(y\), let \(c(y)\) be its \(C\)-coefficient. The population
linear functional \(H=A-C\) has complex weights

\[
 H(0)=H(B)=H(2B)=H(A+C)=0,\qquad
 H(C)=-1,\quad H(2C)=-2,\quad H(B+C)=-1.                      \tag{2.1}
\]

Thus every reaction \(y\to z\) has

\[
                     \Delta H=c(y)-c(z).                      \tag{2.2}
\]

Consequently:

* a reaction with source and target in \({\cal Z}\) has exactly zero
  \(H\)-reward, at every shifted population;
* a \({\cal Z}\)-to-\({\cal P}\) reaction lowers \(H\) by one or two; and
* a \({\cal P}\)-to-\({\cal Z}\) reaction raises \(H\) by one or two.

This identifies the correct singular process. Retain every
\({\cal Z}\)-sourced reaction, even when \(C>0\), and kill the trace on its
first \({\cal P}\)-target. Temporarily suppress only
\({\cal P}\)-sourced reactions. In the physical process, stop at and include
the first such suppressed reaction. Call that endpoint \(E\). Before
killing or \(E\), all actual reactions are \({\cal Z}\)-sourced and
\({\cal Z}\)-targeted, so

\[
                              H(X_t)=a.                        \tag{2.3}
\]

At a clean killing target \(D\),

\[
                              H(X_D)\le a-1.                   \tag{2.4}
\]

The paid event \(E\) is the only way for the physical trace to violate
(2.3). This is stronger than declaring every lower firing in a carrier
window a defect: the potentially long zero-level trace is kept exactly.

If \({\cal C}\cap{\cal P}=\varnothing\), (2.2) makes \(A-C\) an exact
stoichiometric invariant. If no member of
\({\cal C}\cap\{0,B,2B\}\) is enabled at \(C=0\), no reaction is enabled.
In a closed irreducible class that state is a singleton. These are the
invariant and frozen alternatives in Theorem 1.1.

## 3. The clean killed trace

Until killing, write

\[
                         C=r,\qquad A=a+r,                     \tag{3.1}
\]

which follows from (2.3). A \(jB\)-source has rate

\[
                         \alpha_e(b)_{\underline j},
              \qquad j\in\{0,1,2\},                           \tag{3.2}
\]

and a \(q\)-source has rate

\[
                         \beta_e(a+r)r.                        \tag{3.3}
\]

### Lemma 3.1 (maximal-source killed Green)

Let \(Q_a\) be the embedded clean kernel obtained by deleting exact
population self returns and making every \({\cal P}\)-target absorbing.
Along every sequence with \(m(b)=o(a)\):

\[
 \begin{aligned}
 (I-Q_a)^{-1}(1+b)^p&\le C_p(1+b)^{p+1},\\
 \mathbb E_b N^p&\le C_p(1+b)^p,                              \tag{3.4}\\
 \mathbb P_b\{\max B\ge k\}
   &\le C\exp\{\theta b\log(b+e)-c k\log(k+e)\},
 \end{aligned}
\]

for every fixed \(p\), some \(\theta,c>0\), and all large \(a\). Here
\(N\) is the number of nonself clean macros before killing. Exact-return
counts, physical duration, carrier population, and the actual killing
endpoint have the corresponding polynomial moments. In particular,

\[
                          \mathbb E_b\tau_{\rm clean}
                               \le C(1+b)^2.                   \tag{3.5}
\]

#### Proof

Let \(d\in\{0,1,2\}\) be the largest pure \(B\)-degree present and enabled
outside a fixed compact set, and put

\[
                              J=B+dC.                          \tag{3.6}
\]

A \(q\to jB\) reaction changes \(J\) by \(j-d\le0\). A
\(dB\to q\) reaction leaves \(J\) unchanged, and a
\(dB\to jB\) reaction does not increase it. Every positive \(J\)-move is
sourced at degree at most \(d-1\), hence has normalized probability
\(O(B^{-1})\) relative to the degree-\(d\) clocks.

If the degree-\(d\) outcomes in a proposed zero-reward block were all exact
returns, strong connectivity would give an edge leaving the block. Its
source is either the same degree-\(d\) complex, where it has a fixed
conditional probability, or \(q\), where the common factor
\((a+r)r\) cancels and it again has a fixed conditional probability. The
leaving outcome is killing or a strict decrease of \(J\). Thus, after
deleting exact returns, outside a fixed compact set,

\[
 \begin{aligned}
  Q_a\{J'\le J-1\}+Q_a\{\dagger\}&\ge c,\\
  Q_a\{J'>J\}&\le C/J,\qquad |J'-J|\le2
       \quad\hbox{on one base macro}.                         \tag{3.7}
 \end{aligned}
\]

The only issue is more than one \(q\)-carrier. While \(r>0\), the aggregate
\(q\)-rate is at least \(c(a+r)r\), whereas all
\({\cal Z}\)-pure clocks have aggregate rate at most \(Cm(B)\).
Under (1.5), additional zero-level insertions during one cleanup form a
branching family of mean \(o(1)\). They are retained, and their total
progeny has every fixed moment. Hence they change only the constants in
(3.7).

For \(f_p(J)=(1+J)^{p+1}\), (3.7) gives

\[
                         (I-Q_a)f_p(J)\ge c_p(1+J)^p           \tag{3.8}
\]

outside a compact set. Strong connectivity supplies a finite killing path
from each enabled compact state; a compact state with no enabled source is
the frozen alternative. The finite Green corrector removes the compact
positive residual, proving the first two lines of (3.4). Applying the same
comparison to

\[
                  F_\theta(J)=\exp\{\theta J\log(J+e)\}
\]

proves the last line. Holding times and cleanup moments follow from
(3.2)--(3.3). The killing reaction is included, so these are post-jump
endpoint estimates. \(\square\)

### Lemma 3.2 (one-sided clean entropy)

Complete a clean killing by retaining the physical \(q\)-clocks until the
old \(A\)-population has fallen by one, or until a
\({\cal P}\)-sourced clock fires. With the latter clock still suppressed,
the clean endpoint \(D\) satisfies

\[
 \mathbb E\!\left[
   G_\ell(X_D)-G_\ell(a,b,0)\right]\le-\log a+C,               \tag{3.9}
\]

and, more strongly,

\[
 \mathbb E\!\left[
   W_\ell(X_D)-W_\ell(a,b,0)\right]
      \le-cG_\ell(a,b,0)^3\log a.                             \tag{3.10}
\]

#### Proof

At the first \({\cal P}\)-target there is a free \(C\)-unit not paired with
a new \(A\)-entry. Every \(q\)-firing lowers \(A\) by one. Zero-level
entries may have created paired carriers, but their matching \(q\)-exits
cancel first. The clean cleanup therefore reaches \(A\le a-1\); if a
\(q\)-target remains in \({\cal P}\), further \(q\)-firings only improve
the \(A\)-reward. The carrier count has the moments from Lemma 3.1.

For the spectator, (3.7) implies the one-sided terminal estimate

\[
               \mathbb E\,[\,\log(B_D!)-\log(b!)\,]\le C.     \tag{3.11}
\]

Indeed a dominant decrease loses \(\log(B+O(1))\), whereas a positive
move has probability \(O(B^{-1})\) and costs only \(O(\log(B+e))\).
The exponential Green bound controls the terminal overshoot. The same
estimate holds after adding the fixed spectator correction \(\ell_BB\):
a large decrease has favorable factorial part
\(-\Theta(B\log B)\), which absorbs its \(O_\ell(B)\) linear cost, while
positive moves have the Green tail above. The \(C\)-endpoint and the
remaining fixed linear increments have bounded positive expectation.
Combining these facts with
\(\log((a-1)!)-\log(a!)=-\log a\) proves (3.9).

For (3.10), use the exact fourth-power identity only on the positive
increment part. A large spectator decrease is retained with its favorable
sign, while the positive endpoint has moments controlled by the
exponential Green estimate. Since

\[
                \log(b!)=o(\log(a!))
\]

under (1.5), \(G_\ell\) remains comparable to \(a\log a\) throughout the
nonpromotion trace. The quadratic and higher positive remainders are
therefore lower order than \(G_\ell^3\log a\). \(\square\)

## 4. Sourcewise payment of cofactor-bearing clocks

The clean trace suppressed only \({\cal P}\)-sourced reactions. At a state
with \(C=r>0\), their aggregate rate is bounded by

\[
                  C\{r+r^2+Br\}.                              \tag{4.1}
\]

The \(q\)-rate is at least \(c(a+r)r\). After averaging the carrier
population from Lemma 3.1, the paid race at spectator level \(k\) is
therefore at most

\[
                            {C(1+k)\over a}.                   \tag{4.2}
\]

### Lemma 4.1 (ordered paid-Green estimate)

Let \(E\) be the included first \({\cal P}\)-sourced reaction during the
trace or its cleanup. Along every separated sequence (1.5),

\[
 \begin{aligned}
 &\mathbb E\!\left[
   \bigl(W_\ell(X_E)-W_\ell(x)\bigr)^+;E\right]                 \\
 &\qquad\le o(1)\,G_\ell(x)^3
   \left\{\log a+
     \mathbb E\sum_{\nu<N}
       \log(B_\nu+e)\,
       {\bf1}_{\{J_{\nu+1}<J_\nu\}}\right\}.                  \tag{4.3}
 \end{aligned}
\]

The same bracket, with a fixed negative coefficient, is supplied by the
clean killing/decrease part. Hence the actual killed kernel, with \(E\)
included, still obeys

\[
 \mathbb E_x\!\left[
   W_\ell(X_{\tau_0})-W_\ell(x)+\tau_0\right]
       \le-cG_\ell(x)^3\log a                                 \tag{4.4}
\]

unless the trace reaches a promotion boundary. Here \(\tau_0\) is the
first clean service, \(E\), or promotion endpoint.

#### Proof

Order the paid local time by the clean macro at which it occurs. The
sourcewise race bound (4.2), followed by the Green estimate (3.4), is the
exact analogue of an ordered Feynman--Kac first-insertion expansion. It
does not multiply a per-window estimate by an arbitrary deterministic
number of windows.

At a macro with spectator level \(k\), strong connectivity and (3.7)
supply, with fixed probability, either killing or a strict \(J\)-decrease.
Killing pays \(G_\ell^3\log a\). A strict spectator decrease pays
\(G_\ell^3\log(k+e)\). The paid positive cost at that macro is at most

\[
             {C(1+k)\over a}\,
                 G_\ell^3\{\log a+\log(k+e)\}.                 \tag{4.5}
\]

Localize first at \(B=L_a\), including the crossing reaction, where

\[
 L_a=
 \begin{cases}
  a^{1/4}\sqrt{b+1},&2B\in{\cal C},\\
  \sqrt{a(b+1)},&2B\notin{\cal C}.
 \end{cases}                                                  \tag{4.6}
\]

Under (1.5), \(b/L_a\to0\), while \(L_a^2/a\to0\) in the first case and
\(L_a/a\to0\) in the second. Lemma 3.1 makes this included boundary
smaller than every fixed inverse power of \(a\), even after any fixed
polynomial endpoint weight.

Below \(L_a\), if killing has fixed probability, (4.5) is
\(o(G_\ell^3\log a)\) because \(k/a\to0\). If decrease has fixed
probability, use

\[
 \sup_{1\le k\le L_a+O(1)}
 {\,k\log a\,\over a\log(k+e)}\longrightarrow0
                                                                  \tag{4.7}
\]

When \(2B\) is present, the sharper \(b^2/a\to0\) makes the ordered sum
smaller still. Exact self returns have a uniformly bounded diagonal inverse
by the same directed-cut argument used in Lemma 3.1. Summing (4.5) in
Green order proves (4.3). The moving-localization contribution is
negligible by the exponential Green estimate just noted.

The causing paid reaction changes each population by at most two. Its
positive fourth-power increment is therefore bounded by the right-hand
scale in (4.5); all preceding large spectator decreases keep their
favorable sign. The carrier and duration moments are lower order by
Lemmas 3.1--3.2. This proves (4.4). \(\square\)

This is the step which permits polynomially separated spectators. A crude
bound by the total lower propensity \(m(B)\) at every carrier window would
lose an extra power of \(B\). Sourcewise, the only paid complexes are
\(C,2C,B+C\), whose spectator degree is at most one.

## 5. Promotion is an exact outer chart

After the moving localization in (4.6), choose a fixed small
\(\varepsilon>0\) and stop at the first included crossing

\[
                         m(B)\ge\varepsilon A.                 \tag{5.1}
\]

Because the incoming sequence satisfies (1.5), Lemma 3.1's exponential
Green bound makes a clean crossing before service smaller than every fixed
inverse power of \(a\). Its post-jump endpoint is used.

There are only two structural promotion mechanisms.

1. A pure \(B\) or \(2B\) complex supplies \(m(B)\). It is enabled and is
   deterministic-top at (5.1), so \(D^1\cap E\ne\varnothing\).
2. No pure complex supplies the new scale. By (1.4), \(B+C\) is present and
   \(B\asymp A\); this is the balanced two-top chart
   \(\{A+C,B+C\}\).

The first endpoint enters the ordinary Anderson--Kim descending-source
episode. The second enters the balanced all-clock episode in Theorem 5.1
of *proof_first_single_linkage_structural_reduction_and_mesoscopic_gap.md*.
Both use the same \(W_\ell\). Appending the actual outer episode therefore
has zero switching toll. Equations (3.5), (4.4), and the outer physical
episode give (1.7)--(1.8), proving Theorem 1.1. \(\square\)

## 6. The balanced four-complex witness is deficiency zero

The support

\[
                          \{0,C,A+C,B+C\}                      \tag{6.1}
\]

used as the full-rank two-active tier witness in the structural note is
already deficiency zero. Relative to \(0\), the vectors

\[
 C=(0,0,1),\qquad A+C=(1,0,1),\qquad B+C=(0,1,1)              \tag{6.2}
\]

are independent. Hence \(s=3\), \(m=4\), one linkage, and

\[
                             \delta=m-1-s=0.                   \tag{6.3}
\]

For every strong orientation and positive rate vector, the stochastic
deficiency-zero theorem gives the product-form invariant measure and
positive recurrence on every closed irreducible class. Thus (6.1) is a
counterexample only to a one-active tier reduction, not a recurrence
obstruction.

Among balanced full-rank supports in

\[
             \{0,C,2C,A+C,B+C\},
\]

every four-complex support is likewise deficiency zero. The sole
non-deficiency-zero support is the full five-complex set, already covered
by the balanced all-clock theorem.

## 7. The remaining one-active shape

If both \(A+B\) and \(A+C\) are disabled top complexes, then \(B=C=0\).
Put

\[
                             H=A-B-C.                          \tag{7.1}
\]

The zero-level complex set is \(\{0,A+B,A+C\}\); every nonzero lower
target decreases \(H\). Before such a target, the inactive carrier
population is bounded. A \({\cal P}\)-sourced competitor has rate \(O(1)\),
whereas an enabled mixed source has rate \(\Theta(A)\). The directed-cut
argument gives a geometric exact-return inverse, the paid error is
\(O(A^{-1})\), and one old-\(A\) service gives
\(-\log A+O(1)\) entropy drift. If no nonzero lower target exists, (7.1)
is invariant; if \(0\) is absent, the face is frozen.

Thus the two-disabled-top one-active shape is the bounded-base special case
of Sections 2--4 and needs no orientation list or population search.

## 8. Completion of the one-linkage branch

Combine this note with the structural obstruction theorem.

* With at most two dynamic species, the only non-deficiency-zero exception
  is \(\{0,B,2B,A+B\}\), proved in
  *proof_first_single_linkage_2d_exception_service_theorem.md*.
* If a three-species tier has an enabled top-D source, the
  Anderson--Kim source/D-tier criterion applies.
* A single dominant disabled mixed top has the separated form (1.1);
  Theorem 1.1 covers every spectator scale, including \(B^2=o(A)\) and
  \(B=o(A)\).
* Two disabled tops with one divergent carrier are covered by Section 7.
* Two tied disabled tops with two divergent carriers are balanced and are
  covered by Section 6 or the balanced all-clock theorem.
* If all three populations diverge, every complex is enabled and the
  ordinary criterion applies.

These cases are forced by binary molecularity and the enabled-top identity;
they are not a support enumeration. The physical-time common-potential
composition in *proof_first_global_t3_2_classwise_composition.md* now gives
finite mean hitting time of a finite set in every closed irreducible class.
Therefore every classwise projected weakly reversible binary network with
at most three dynamic species and exactly one active linkage is positive
recurrent. Absorbing singleton classes are included.

## 9. Scope boundary

This theorem is classwise and concerns one projected active linkage. It
does not enlarge the literal hypothesis of the published pure-multiple
theorem. It does not promote any two-linkage atlas count or global T3-2
flag. Its new analytic content is the zero-level cancellation (2.3), the
arbitrary-scale maximal-source Green estimate, and the ordered sourcewise
payment (4.3).
