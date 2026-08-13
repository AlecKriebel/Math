# Proof-first all-orders lemma for the two-level physical renewal

**Scoped status (2026-08-11 PDT).**  This note isolates one analytic
ingredient of the generalized Family-II repair.  It does not enumerate
supports or paths, does not change a certification flag, and does not promote
an incidence or pair.  Its conclusions are conditional only on the explicit
structural hypotheses below.  In particular, the finite atlas is used only
through the single implication (H5), not through a bounded-depth path check.

The main conclusions are these.

1. The target-degree/reserve identity gives
   \(r+j\le 2k+1\) at every nonpure service-free return.  It also gives
   \(r\le2k\) for every positive return and, by a separate source-degree
   argument, for every interrupted exact return.
2. The assertion \(r\le2k\) is false for a decreasing nonexact return.  An
   exact three-reaction counterexample is given in Section 4.  Thus the domain
   of that inequality must not be enlarged.
3. After the pure diagonal class is summed, the complete interrupted exact
   diagonal has norm

   \[
   O\!\left({L_n^3\over n}+{L_n^6\over n^2}\right)=o(1),
   \qquad L_n=\left\lfloor{n^{1/3}\over\log(n+e)}\right\rfloor .
   \]

   This proof sums all interruption orders by a geometric race argument.  It
   does not use the finite one-defect ledger.

## 1. Exact hypotheses

Let

\[
 \mathcal C=\{0,U,2U,I,2I,U+I,V+I\}.
\]

For a complex \(y\), write \(s_U(y)\) for its \(U\)-degree.  Consider a
finite mass-action network with fixed positive rate constants.  Put

\[
 \underline\kappa=\min_e\kappa_e>0,
 \qquad \overline\kappa=\max_e\kappa_e,
 \qquad M=\#\{\hbox{directed reactions}\}.
\]

All constants in this note may depend on
\((M,\underline\kappa,\overline\kappa)\), but not on \(u,n\), or on the
number of interruptions.

We use the following structural hypotheses.

- **(H1) Family-II form.**  The only complex containing \(V\) is \(V+I\).
  It lies in the proper linkage, and the lower linkage is \(V\)-free.  Both
  directed linkage graphs are strongly connected on their supports.
- **(H2) Physical chart.**  A base is \(x_u=(u,n,0)\) in coordinates
  \((U,V,I)\).  During an open excursion put \(R=V-n\), and stop, including
  the boundary-causing reaction, at strict service, the first included
  \(I=0\) return, or \(U\vee I\vee R\ge L_n\).  Before service,
  \(R\ge0\).
- **(H3) Fast and slow reactions.**  A reaction sourced at \(V+I\) is fast;
  every other reaction is slow.  At every open state \(I\ge1\), strong
  connectivity gives at least one outgoing fast reaction.  A slow reaction
  raises \(R\) by one exactly when its target is \(V+I\), and otherwise
  leaves \(R\) unchanged.  A nonterminal fast reaction lowers \(R\) by one.
- **(H4) Pure block.**  A pure word uses only one reaction
  \(aU\to V+I\) and its matching reaction \(V+I\to aU\), with arbitrary
  nesting before its first return to the base.  A completed pure word
  returns the complete physical state.  Repetition of completed words is
  performed by the outer diagonal inverse, not hidden inside one raw
  attempt.  Any exact first return not of this form is interrupted.
- **(H5) Post-contraction outer degree.**  There is a genuine base escape
  degree \(d\in\{0,1,2\}\).  For a two-vertex proper linkage
  \(\{aU,V+I\}\), a base escape clock has rate at least
  \(c_b(1+u)^d\), outside a fixed compact set, while the total base clock is
  at most \(C_b(1+u)^2\).  If the pure block is a proper subset of a larger
  proper linkage, strong connectivity supplies a fixed conditional escape
  probability \(\delta_b>0\) per pure traversal.  In a larger support,
  \(d\) is the maximal \(U\)-degree of an \(I\)-free complex over both
  linkages.  In an exact pair \(\{aU,V+I\}\), the diagonal source \(aU\)
  is deleted before \(d\) is chosen, and \(d\) is the maximal
  \(I\)-free degree in the lower linkage.  Finally,

  \[
  d=0\quad\Longrightarrow\quad
  L_+=\{2U,V+I\},\qquad
  L_0=\{0,I,2I,U+I\}.                                      \tag{1.1}
  \]

  The implication (1.1) is an atlas premise.  The analysis below proves
  everything after that implication, but does not prove the atlas premise.
- **(H6) Compact nontrapping.**  At the finitely many bases below the range
  where the falling-factorial comparison in (H5) applies, a raw attempt has
  probability bounded away from one of being a pure exact return.  This is
  automatic if the descriptor-local stopped class has no closed pure-only
  base, but it must be stated: otherwise \((I-Z^{\rm pure})^{-1}\) need not
  exist.

The constants \(c_b,C_b,\delta_b\) are allowed to depend on the fixed
orientation and fixed rate vector.  Uniformity over all positive rate
vectors is neither asserted nor needed; the theorem's quantifier is “for
each fixed positive rate vector.”

## 2. The exact source/target identity

Consider a service-free history from \(x_u\) to its first included no-fast
return.  Include the opening among the slow reactions, and write

\[
                  e_0,e_1,\ldots,e_k                         \tag{2.1}
\]

for the \(k+1\) slow reactions.  Thus \(k\) is the number of
**post-opening** slow reactions.  Write \(f_1,\ldots,f_h\) for the fast
reactions.  For a reaction \(e:y\to y'\), put

\[
 s(e)=s_U(y),\qquad t(e)=s_U(y').
\]

Every fast source has \(U\)-degree zero.  Define the relative source power
and the final spectator increment by

\[
 r=\sum_{i=0}^k s(e_i)-d,
 \qquad j=U_{\rm end}-u.                                      \tag{2.2}
\]

This definition of \(r\) is algebraic.  Turning it into a probability bound
also requires the race estimate in Section 5; an exponent ledger by itself
is not a kernel estimate.

Telescoping the \(U\)-increments gives the exact identity

\[
 r+j=\sum_{i=0}^k t(e_i)+\sum_{q=1}^h t(f_q)-d.                 \tag{2.3}
\]

Let \(p\) be the number of slow reactions in (2.1) whose target is
\(V+I\).  The reserve starts and ends at zero.  By (H3), those \(p\)
reactions are the only \(+1\) reserve steps and the fast reactions are the
only \(-1\) reserve steps.  Hence

\[
                         h=p.                                   \tag{2.4}
\]

Pair each slow target \(V+I\), whose \(U\)-degree is zero, with one of the
fast reactions in (2.4).  The fast target has \(U\)-degree at most two, so
each pair contributes at most two to the right side of (2.3).  Every
unpaired slow target is \(V\)-free and also has \(U\)-degree at most two.
There are \(k+1\) slow reactions.  Therefore

\[
                       r+j\le 2(k+1)-d.                          \tag{2.5}
\]

If \(d\ge1\), this proves

\[
                       r+j\le2k+1.                              \tag{2.6}
\]

If \(d=0\), (1.1) applies.  A nonpure return must use a lower-linkage
reaction.  Every lower target in (1.1) has \(U\)-degree at most one, so at
least one of the \(k+1\) contributions used in (2.5) saves one unit.  Thus
(2.6) also holds when \(d=0\).  This is the required strict improvement;
it follows from the target set in (1.1), not from a finite path list.

For a positive return, \(j\ge1\), and (2.6) immediately implies

\[
                   r\le2k,
                   \qquad r+\theta j\le2k+\theta
                   \quad(0<\theta<1).                            \tag{2.7}
\]

The second inequality follows from

\[
 r+\theta j=(r+j)-(1-\theta)j.
\]

In particular, the desired range \(0<\theta<1/2\) is covered.

## 3. The exact-return source bound

At an interrupted exact return \(j=0\), (2.6) alone gives only
\(r\le2k+1\).  The missing unit follows from source structure, as follows.

- If \(d\ge2\), every slow source has \(U\)-degree at most two, and hence

  \[
  r\le2(k+1)-d\le2k.                                             \tag{3.1}
  \]

- Suppose \(d=1\).  If every slow source had \(U\)-degree two, every slow
  source would be the unique complex \(2U\).  In a larger proper support,
  the presence of \(2U\) makes the post-contraction maximal base degree at
  least two, contrary to \(d=1\).  In a two-vertex proper support
  \(\{2U,V+I\}\), every \(2U\)-sourced slow reaction belongs to the pure
  block.  An interrupted return therefore has at least one slow source of
  degree at most one.  Consequently

  \[
  r\le 2(k+1)-1-d=2k.                                            \tag{3.2}
  \]

- Suppose \(d=0\).  By (1.1), every proper slow reaction is the pure
  opening \(2U\to V+I\), and every lower slow source has \(U\)-degree at
  most one.  Let \(m\) be the number of lower-linkage reactions in the
  word.  The word is interrupted, so \(m\ge1\).  If \(m=1\), the sum of
  all proper openings and matching fast cleanups is stoichiometrically zero
  at an exact return.  The sole lower reaction would then also have to have
  zero reaction vector, impossible because an edge joins distinct
  complexes.  Hence \(m\ge2\), and

  \[
  r\le 2(k+1-m)+m=2(k+1)-m\le2k.                                \tag{3.3}
  \]

Thus

\[
 \boxed{\ r\le2k\ \text{for every positive return and every interrupted
 exact return.}\ }                                               \tag{3.4}
\]

Together with (2.6), this is the correct coupled invariant.  No statement
about a bounded value of \(k\) was used.

## 4. Exact counterexample to the overstrong domain

The first inequality in (3.4) must not be asserted for every nonexact
return.  In the support (1.1), take the admissible word

```text
2U -> V+I,     U+I -> I,     V+I -> 2U.
```

For \(u\ge3\), its relative states are

\[
 (u,0,0)\longrightarrow(u-2,1,1)
 \longrightarrow(u-3,1,1)\longrightarrow(u-1,0,0).              \tag{4.1}
\]

It is a service-free decreasing continuing return.  Here

\[
 k=1,\qquad d=0,\qquad r=2+1=3,
 \qquad j=-1.                                                     \tag{4.2}
\]

Therefore \(r>2k\), while the correct target inequality remains true:

\[
                         r+j=2\le2k+1=3.                          \tag{4.3}
\]

This counterexample is harmless for the weighted continuation estimate:
its endpoint is smaller, so an increasing endpoint weight does not charge a
positive jump.  It is nevertheless fatal to an unqualified statement of
\(r\le2k\).

## 5. An all-orders race bound

We now prove the diagonal contraction without a one-defect path ledger.
At an open state below the boundary, \(I\ge1\), \(V=n+R\ge n\), and at
least one fast edge is enabled.  Hence

\[
 \lambda_f\ge\underline\kappa nI\ge\underline\kappa n.          \tag{5.1}
\]

Every slow source has molecularity at most two.  For \(L_n\ge2\), its
falling-factorial propensity is at most \(L_n^2\), and therefore

\[
 \lambda_s\le M\overline\kappa L_n^2,
 \qquad
 q_n:=\sup {\lambda_s\over\lambda_f+\lambda_s}
       \le C_s{L_n^2\over n},
 \qquad C_s={M\overline\kappa\over\underline\kappa}.            \tag{5.2}
\]

The displayed value of \(C_s\) can be enlarged to absorb the finitely many
small \(n\) and falling-factorial conventions.

Let \(N\) be the number of post-opening slow reactions before a
service-free included return.  If \(N=k\), reserve conservation implies
that the number of fast reactions is at most \(k+1\): the opening and the
\(k\) later slow reactions create at most \(k+1\) reserve units.  A binary
slow/fast word therefore has length at most \(2k+1\).  Summing detailed
edges first, each specified slow position costs at most \(q_n\), while a
fast position costs at most one.  The number of binary words is at most
\(2^{2k+2}=4^{k+1}\).  Thus, with

\[
                         \varepsilon_n=4q_n,                      \tag{5.3}
\]

and \(\varepsilon_n<1\),

\[
 \mathbb P\{N\ge m\mid\hbox{an excursion opened}\}
       \le {4\varepsilon_n^m\over1-\varepsilon_n}.               \tag{5.4}
\]

This estimate includes arbitrarily many interruptions.  A boundary-stopped
path is absent from an exact-return kernel, so discarding it only enlarges
the right side of (5.4).

## 6. Pure/interrupted diagonal renewal

Let \({\cal B}_n=\{x_u:0\le u<L_n\}\).  For one raw stopped attempt from
\(x_u\), let

\[
 Z^{\rm pure}(u),\qquad Z^{\rm int}(u)                            \tag{6.1}
\]

be the probabilities of, respectively, a pure and an interrupted exact
physical return to \(x_u\).  They are diagonal sub-Markov kernels on
\({\cal B}_n\).  Every continuing nonexact return, strict service, upward
return, or included boundary hit is assigned to a separate exit kernel.
In particular, an internal boundary hit is never put in either kernel in
(6.1).

The base escape comparison in (H5)--(H6) gives a constant \(A<\infty\)
such that

\[
 {1\over1-Z^{\rm pure}(u)}\le
 \begin{cases}
 A, &\text{the pure block is proper in a larger linkage},\\
 A(1+u)^{2-d},&\text{the proper linkage is the exact pair
                         \(\{aU,V+I\}\)}.
 \end{cases}                                                     \tag{6.2}
\]

Indeed, in the exact-pair case, selecting the genuine base escape clock
precludes a pure word, so

\[
 1-Z^{\rm pure}(u)\ge {c_b(1+u)^d\over C_b(1+u)^2}.
\]

In the larger-linkage case, an outgoing edge from the proper subset
\(\{aU,V+I\}\) has the same source propensity as the corresponding pure
edge.  Its conditional probability is a fixed positive ratio of rate
constants.  This proves the first line of (6.2).

Every interrupted exact return has at least one post-opening slow reaction:
with none, an exact opening/cleanup is pure.  In the unique \(d=0\) support,
it has at least two.  The latter assertion is the \(m=1\) argument in
Section 3, and is analytic.  Consequently, (5.4) and (6.2) give

\[
 \begin{aligned}
 R_n^{\rm int}(u)
  &:={Z^{\rm int}(u)\over1-Z^{\rm pure}(u)},\\
 \sup_{u<L_n}R_n^{\rm int}(u)
  &\le C_R\left\{
       \varepsilon_n+(1+L_n)\varepsilon_n
       +(1+L_n)^2\varepsilon_n^2\right\}\\
  &\le C_R'\left\{{(1+L_n)^3\over n}
                 +{(1+L_n)^6\over n^2}\right\}
       =:\delta_n.                                                \tag{6.3}
 \end{aligned}

Here the three terms correspond to a fixed-cut/larger linkage, an exact
pair with \(d\ge1\), and the unique exact pair with \(d=0\), respectively.
For all large \(n\), choose it so that \(\varepsilon_n\le1/2\).  One may
then take

\[
 C_R=8A,
 \qquad
 C_R'=8A\max\{8C_s,16C_s^2\},                                   \tag{6.4}
\]

after harmless enlargement for \(1+L_n\) in place of \(L_n\).

At the stated cutoff,

\[
 {L_n^3\over n}\le {1\over\log^3(n+e)},
 \qquad
 {L_n^6\over n^2}\le {1\over\log^6(n+e)},                       \tag{6.5}
\]

so \(\delta_n=o(1)\).  Notice that no claim about a maximal interruption
count occurs in (6.3).

## 7. The correct weighted operator statement

Let \(W:{\cal B}_n\to(0,\infty)\) be any base weight, including
\(W=H_\theta\).  For a positive base kernel \(K\), use the row norm

\[
 \|K\|_W=\sup_{x\in\mathcal B_n}{1\over W(x)}
                   \sum_{y\in\mathcal B_n}K(x,y)W(y).          \tag{7.1}
\]

Because \(R_n^{\rm int}\) is diagonal and returns the complete physical
state,

\[
 \left\|(I-Z^{\rm pure})^{-1}Z^{\rm int}\right\|_W
   =\sup_{u<L_n}R_n^{\rm int}(u)\le\delta_n=o(1)                \tag{7.2}
\]

for **every** positive weight \(W\).  This is the relevant weighted norm;
no auxiliary interruption mark appears at the endpoint.

Let \(K_\alpha\) be any raw exit kernel, where \(\alpha\) may denote a
continuing nonexact return, strict service, upward return, or included
boundary.  If \(F_\alpha\ge0\) is its actual endpoint reward, define

\[
 \|K_\alpha\|_{W,F_\alpha}
   =\sup_{u<L_n}{K_\alpha F_\alpha(u)\over W(u)}.                 \tag{7.3}
\]

First renew the pure class,

\[
 R_\alpha^{\rm pure}=(I-Z^{\rm pure})^{-1}K_\alpha,
\]

and then all interrupted exact returns.  Since \(\delta_n<1\) for all
large \(n\),

\[
 \begin{aligned}
 \widetilde K_\alpha F_\alpha
  &=\sum_{m=0}^\infty (R_n^{\rm int})^m
          R_\alpha^{\rm pure}F_\alpha,\\
 \|\widetilde K_\alpha\|_{W,F_\alpha}
  &\le {1\over1-\delta_n}
       \|R_\alpha^{\rm pure}\|_{W,F_\alpha}.                   \tag{7.4}
 \end{aligned}

Thus (7.4) keeps the actual terminal population and its actual reward and
sums an arbitrary number of interrupted exact returns.  It applies
unchanged to an entropy reward, a polynomial endpoint reward, or a boundary
indicator, provided the pure-renewed norm on the right is finite.  A path
that hits the boundary inside a would-be diagonal word is already in
\(K_{\rm boundary}\), not in \(Z^{\rm pure}\) or \(Z^{\rm int}\), so it
appears exactly once in (7.4).

Algebraically,

\[
 I-Z^{\rm pure}-Z^{\rm int}
  =(I-Z^{\rm pure})(I-R_n^{\rm int}),                            \tag{7.5}
\]

and therefore

\[
 (I-R_n^{\rm int})^{-1}(I-Z^{\rm pure})^{-1}K_\alpha
  =(I-Z^{\rm pure}-Z^{\rm int})^{-1}K_\alpha.                   \tag{7.6}
\]

This is the exact two-stage physical renewal.

For an additive nonnegative reward \(a\) accumulated during exact loops,
the same argument applies to the renewal-reward equation
\(h=a+(Z^{\rm pure}+Z^{\rm int})h\):

\[
 h=(I-R_n^{\rm int})^{-1}(I-Z^{\rm pure})^{-1}a.                 \tag{7.7}
\]

Equation (7.7) proves first-moment propagation once the pure-renewed reward
on its right is bounded.  Higher duration moments do **not** follow from
the probability contraction (7.2) alone.  They require a separate bound on
the pure-renewed loop-duration moments, followed by the usual binomial
induction (or differentiation of a time-marked kernel).  This is a distinct
hypothesis and should remain a distinct audit obligation.

## 8. What is proved, and what remains external

The proof in this note is fully all-orders after the following inputs are
granted:

1. the Family-II complex restriction (H1);
2. the post-contraction base escape estimate and the atlas implication
   \(d=0\Rightarrow\)(1.1);
3. compact nontrapping for the pure renewal; and
4. a separate pure-renewed bound for whichever terminal or duration reward
   is inserted on the right side of (7.4) or (7.7).

No finite path menu is needed for (2.6), (3.4), (5.4), or (6.3).  In
particular, a one-defect exact-return histogram is not a premise of the
diagonal contraction.

There are two precise cautions for the canonical repair.

- The phrase “\(r\le2k\) for every continuing return” is false by (4.1).
  The correct domain is “positive continuing or interrupted exact.”
- A Feynman--Kac probability estimate does not automatically retain an
  arbitrary terminal reward or a high duration moment.  Terminal rewards
  must be inserted as in (7.3)--(7.4), and duration moments need the
  additional pure-renewed moment input stated after (7.7).

Subject to those corrections, the interrupted diagonal is a genuine
\(o(1)\) perturbation of the pure physical renewal at the full
\(n^{1/3+o(1)}\) scale.
