# Full all-clock nested-carrier operator at the separated face

**Proof-first candidate, 2026-08-12 PDT.** This note replaces both the
failed frozen separated theorem and the failed stop-at-first-entry repair.
Its central rule is:

> a lower-to-\(A+C\) firing is never charged at its raw endpoint; it creates
> one pending entry, and its first later \(A+C\)-exit cancels it.

The stopping event is the first **surplus** \(A+C\)-exit, after all pending
entries have been consumed. Consequently the active factorial increment
telescopes exactly, regardless of the number of nested entries.

The result is arbitrary-orientation and arbitrary-positive-rate. No support,
orientation, or population enumeration is used. No flag is changed.

## 1. Support, gap, and statement

Let

\[
 q=A+C,\qquad
 \{q\}\subseteq{\cal C}
 \subseteq\{0,B,2B,C,2C,B+C,q\}                       \tag{1.1}
\]

be one strongly connected linkage. At the cofactor-free entrance write

\[
                              x=(a,b,0).                       \tag{1.2}
\]

Define the largest lower spectator monomial

\[
 m(b)=
 \begin{cases}
  1+b^2,&2B\in{\cal C},\\
  1+b,&2B\notin{\cal C},\
       {\cal C}\cap\{B,B+C\}\ne\varnothing,\\
  1,&B,2B,B+C\notin{\cal C},
 \end{cases}
 \qquad h(a,b)=\log{a\over m(b)}.                             \tag{1.3}
\]

The separated premise is \(h(a,b)\to\infty\).

For fixed \(\ell\), put

\[
 G_\ell(x)=K_\ell+\sum_{i=A,B,C}\log(x_i!)+\ell\cdot x\ge1,
 \qquad W_\ell=G_\ell^4.                                     \tag{1.4}
\]

> **Theorem 1.1 (nested-carrier stopped theorem).** Fix the support, strong
> graph, rates, closed irreducible class, and \(\ell\). Along every
> cofactor-free separated sequence (1.2)--(1.3), there is an included
> all-reaction stopping time \(\tau\) such that
> \[
>  \mathbb E_x[
>    W_\ell(X_\tau)-W_\ell(x)+\tau]
>       \le-cG_\ell(x)^3h(a,b).                               \tag{1.5}
> \]
> The terminal partition is:
>
> 1. the first surplus \(q\)-exit;
> 2. an included moving-localization endpoint whose weighted contribution
>    is \(o(G_\ell^3h)\); or
> 3. the exact invariant/frozen alternative.
>
> On service,
> \[
>             A_\tau=a-1,\qquad
>  \mathbb E[\log(B_\tau!)+\log(C_\tau!)-\log(b!)]
>       \le\log m(b)+C.                                      \tag{1.6}
> \]
> For every fixed \(p\), the positive part of the spectator entropy,
> centered endpoint, and physical duration have the moments needed for the
> fourth-power expansion.

The moving endpoint terminates this episode and is returned to the common
physical router. It is not continued secretly to a later promotion inside
the same stopping time.

## 2. The pending-entry ledger

During the episode define \(D\) reaction by reaction:

\[
 D^+=
 \begin{cases}
  D+1,&\hbox{a lower source fires to }q,\\
  D-1,&\hbox{\(q\) fires and }D>0,\\
  0,&\hbox{\(q\) fires and }D=0,\\
  D,&\hbox{otherwise}.
 \end{cases}                                                  \tag{2.1}
\]

Start with \(D=0\), and stop at the third line of (2.1), including that
reaction. Before the stop,

\[
                              A=a+D.                          \tag{2.2}
\]

Indeed the only reactions changing \(A\) are lower-to-\(q\) entries and
\(q\)-exits. Thus (2.2) is an exact pathwise identity, not an expectation.
At the stop,

\[
                              A_\tau=a-1.                     \tag{2.3}
\]

Every nested entry is therefore paired, and all active factorial increments
telescope:

\[
       \sum_{s\le\tau}\{\log(A_s!)-\log(A_{s-}! )\}
          =\log((a-1)!)-\log(a!)=-\log a.                     \tag{2.4}
\]

This identity is why the counter-race
\(B+C\to q\), whose raw endpoint costs \(+\log a\), causes no error.

## 3. The ideal Schur kernel

First suppress every non-\(q\) clock while \(C>0\), but retain all clocks
on \(C=0\). At a no-fast base \((u,d)\), the physical population is

\[
                         (A,B,C)=(a+d,u,0).                    \tag{3.1}
\]

A base-sourced reaction has one of three ideal outcomes.

1. A lower target with zero \(C\)-degree gives a bounded \(u\)-move and
   leaves \(d\) fixed.
2. Target \(q\) raises \(d\) by one. The first \(q\)-exit consumes that
   unit. A zero-\(C\) target returns to a base with the original \(d\); a
   positive-\(C\) target leaves a free carrier, and the subsequent
   \(q\)-exit lowers \(d\) if \(d>0\) or gives service if \(d=0\).
3. A positive-\(C\) lower target creates a free carrier directly; its next
   \(q\)-exit lowers \(d\) or gives service.

A clean branch begun with \(d=0\) has at most two \(q\)-firings before a
base return or service. From general \(d\), a clean burst has at most
\(d+2\) firings before a base return, debt decrease, or service; this count
is controlled by the debt weight below. Conditional \(q\)-targets have the
state-independent law

\[
               p_z={\kappa_{qz}\over\sum_{q\to w}\kappa_{qw}}. \tag{3.2}
\]

Delete exact population/mark self returns. Their diagonal inverse is
uniformly bounded: if a proposed exact block had no fixed-probability exit,
strong connectivity would give a directed cut edge sourced either at its
base complex, where the falling-factorial factor is identical, or at \(q\),
where (3.2) applies.

Let \(Q\) be the resulting substochastic continuation kernel on
\((u,d)\), killed at service.

## 4. Clean maximal-source Green theorem

Let \(e\in\{0,1,2\}\) be the maximal pure \(B\)-degree enabled at large
\(u\). A degree-\(e\) ideal macro either

* services,
* lowers \(d\),
* leaves \(d\) fixed and does not increase \(u\), or
* is an exact return already deleted.

Every positive \(u\)-move is sourced at degree at most \(e-1\), so its
normalized probability is \(O(u^{-1})\). The directed-cut argument makes
one of service, debt decrease, or strict \(u\)-decrease occur with fixed
probability outside a compact set.

Put

\[
 {\cal F}_{\theta,a}(u,d)
   =\exp\{\theta[u\log(u+e)+d\log a]\},
       \qquad 0<\theta<1/8.                                  \tag{4.1}
\]

### Lemma 4.1 (clean ordered Green)

For every \(0<\theta'<\theta<1/8\),

\[
       (I-Q)^{-1}{\cal F}_{\theta',a}(u,d)
          \le C_{\theta',\theta}{\cal F}_{\theta,a}(u,d),     \tag{4.2}
\]

uniformly along the separated sequence. Polynomial weights have the
sharper bound

\[
       (I-Q)^{-1}(1+u+d)^p\le C_p(1+u+d)^{p+1}.               \tag{4.3}
\]

The same estimates hold for moments of the clean macro count and physical
duration.

#### Proof

For a positive jump \(j\le2\),

\[
 {{\cal F}_{\theta,a}(u+j,d)\over
       {\cal F}_{\theta,a}(u,d)}
       \le C u^{2\theta}.                                    \tag{4.4}
\]

Its probability is \(O(u^{-1})\), hence its normalized contribution is
\(O(u^{-1+2\theta})=o(1)\). A dominant \(u\)-decrease has ratio
\(O(u^{-\theta})\). A debt-decreasing \(q\)-exit with a target containing
\(j\) spectator molecules has combined ratio
\[
                  a^{-\theta}u^{j\theta}
                    =(u^j/a)^\theta\le e^{-\theta h_u},       \tag{4.5}
\]
so it is also strict; service is killing. Compact service accessibility
follows by following a
simple strong-graph path from an enabled base complex to a positive-\(C\)
target; a state with no enabled base source is absorbing. This proves a
strict multiplicative drift outside a compact set and a finite compact
Green corrector, yielding (4.2).

For \(f_p=(1+u+d)^{p+1}\), a dominant decrease loses order
\((1+u+d)^p\), while a lower-degree positive move contributes at most that
order times \(O(u^{-1})\). The compact corrector gives (4.3). Holding times
at base are bounded by the inverse enabled base rate; clean open holding
times are \(O((a+d)^{-1})\). \(\square\)

## 5. Restoring all open-phase clocks

Let \(R\) be the operator which inserts one non-\(q\) reaction during a
clean open window and then resumes clean evolution from its actual target.
No inserted edge is killed. If its target is \(q\), (2.1) increments
\(D\); subsequent \(q\)-motion pairs it.

Below the moving localization, write

\[
 h_u=\log{a\over m(u)}.
\]

Choose the \(B\)-boundary \(L_a\) so that \(h_u\ge h/2\) for
\(u<L_a\):

\[
 L_a=
 \begin{cases}
 a^{1/4}\sqrt{b+1},&2B\in{\cal C},\\
 \sqrt{a(b+1)},&2B\notin{\cal C}.
 \end{cases}                                                  \tag{5.1}
\]

Also stop at \(C+D\ge a^{1/4}\). Both crossing reactions are included.

### Lemma 5.1 (all-insertion contraction)

In the weighted norm generated by (4.1),

\[
                         \|R\|\le e^{-c h}+o(1).               \tag{5.2}
\]

Consequently the full all-clock open resolvent is the convergent positive
series

\[
              (I-R)^{-1}=I+R+R^2+\cdots,                     \tag{5.3}
\]

with norm \(1+o(1)\). Its macro count, endpoint, and duration have the
Green bounds (4.2)--(4.3).

#### Proof

At an open state, the \(q\)-rate is at least \(c(a+d)C\). A lower source
with \(B\)-degree \(j\) has rate at most

\[
                        C(1+u)^j(1+C)^k,\qquad j+k\le2.       \tag{5.4}
\]

Under the \(C+D\) cutoff, its race ratio is its source monomial divided by
\(aC\).

If the inserted reaction is an entry to \(q\), it raises \(d\) by one but
consumes the source's \(j\) spectator molecules. Its race probability
times weighted ratio is
bounded by

\[
 {C u^j\over a}\ a^\theta u^{-\theta j}
   =C(u^j/a)^{1-\theta}
   \le C\exp\{-(1-\theta)h/2\}.                               \tag{5.5}
\]

Here \(u^j/a\le e^{-h_u}\le e^{-h/2}\). Sources involving \(C\) have an
additional bounded carrier moment and the same or smaller ratio. If the
inserted edge is not an entry, it does not raise \(d\); maximal source
degree either decreases the spectator weight or gives the standard
\(O(u^{-1+2\theta})\) positive-move factor. Exact self insertions have the
bounded directed-cut inverse.

Summing over the fixed edge set gives (5.2). Positivity and the Neumann
identity give (5.3). Polynomial bounds follow by differentiating the
counting parameter in the same series and applying (4.3). \(\square\)

Equation (5.3), rather than a first-insertion stop, is the load-bearing
repair. A raw entry costs \(\log a\), and the pending weight correctly
charges it by \(a^\theta\); consumption of its actual source molecules and
the race factor combine to the small monomial ratio in (5.5). Its eventual
exit is kept in the same operator block.

## 6. Service endpoint entropy

At service, (2.3)--(2.4) give the exact active contribution \(-\log a\).
The maximal-source Green estimate and all-insertion contraction give

\[
 \mathbb E[
   \log(B_\tau!)+\log(C_\tau!)-\log(b!)]
       \le\log m(b)+C,                                      \tag{6.1}
\]

and, for every fixed \(p\),

\[
 \mathbb E\left[
  \left(
   \log(B_\tau!)+\log(C_\tau!)-\log(b!)
  \right)^+\right]^p
     \le C_p(1+\log m(b))^p.                                 \tag{6.2}
\]

To see (6.1), expose the last clean killing macro. Its target has
spectator degree at most the degree defining \(m\), hence costs at most
\(\log m(b)+O(1)\). Every earlier dominant spectator decrease has favorable
factorial sign. Positive lower-degree moves are \(O(u^{-1})\) and are
summed by (4.2). The all-insertion resolvent changes the bound by \(1+o(1)\).
The \(C+D\) boundary has superpolynomially small weighted probability by
(4.2) and (5.3).

The fixed linear correction is handled in the same one-sided way: large
spectator decreases have factorial size \(u\log u\), absorbing
their \(O_\ell(u)\) linear cost, while positive endpoints have (6.2).
Therefore

\[
                    \mathbb E\Delta G_\ell
                         \le-h(a,b)+C.                         \tag{6.3}
\]

## 7. Fourth power, duration, and moving boundary

At the terminal service endpoint, the positive part of
\(\Delta G_\ell\) has the moments (6.2), while a large negative spectator
increment is retained with its favorable sign. The one-sided fourth-power
expansion gives

\[
 \begin{aligned}
 \mathbb E\Delta W_\ell
 &\le4G_\ell(x)^3\,\mathbb E\Delta G_\ell\\
 &\quad+C G_\ell(x)^2\mathbb E((\Delta G_\ell)^+)^2
       +C\mathbb E((\Delta G_\ell)^+)^4.                     \tag{7.1}
 \end{aligned}
\]

Since \(G_\ell(x)\asymp a\log a\), \(h\to\infty\), and
\(\log m(b)\le\log a\), the last two terms are
\(o(G_\ell(x)^3h)\). Equations (6.3) and (7.1) give the desired drift on
service.

The physical duration is bounded by the clean polynomial Green time times
the \(1+o(1)\) all-insertion factor. If \(2B\) is present,
\(b^2=o(a)\); otherwise \(b=o(a)\). Thus the duration is
\(o(G_\ell^3h)\).

The exponential Green bound makes the included crossings of (5.1) and
\(C+D=a^{1/4}\) smaller than every fixed inverse power of \(a\), with any
fixed polynomial endpoint reward. Their positive \(W_\ell\)-contribution
is \(o(G_\ell^3h)\). They terminate the episode and return to the common
router. This proves Theorem 1.1. \(\square\)

## 8. Invariant and frozen alternatives

If no positive-\(C\) lower complex is present, \(A-C\) is an exact
stoichiometric invariant. If no zero-\(C\) lower source is enabled at
\((a,b,0)\), the state is absorbing; in a closed irreducible class it is a
singleton. These are the only cases in which the compact service path used
in Lemma 4.1 is absent.

## 9. Audit obligations

The theorem is a new candidate and must not be cited as certified before a
hostile operator replay checks:

1. the exact clean Schur formulas on \((B,D)\);
2. the sourcewise weighted contraction (5.5), especially \(2C\)-source
   insertions and shifted carrier populations;
3. the sharp one-sided endpoint estimate (6.1);
4. the removal of both moving localizations; and
5. physical duration for every maximal molecular degree.

No part of this note relies on the rejected first-insertion estimate.
