# First-mark resolvent lemma for the separated completed-return trace

**Proof-only operator component, 2026-08-12 PDT.**  This note proves the
first-mark/Neumann estimate needed in Section 5 of
*proof_first_separated_completed_return_ledger.md*.  It is conditional only
on that note's clean completed-return Green bound.  It does not prove the
clean bound, duration, localization removal, terminal entropy, or any
recurrence claim.  No certification flag is changed.

The important convention is that the clean kernel below is the
**substochastic physical kernel**: at an open state it retains the actual
probability of a (q=A+C)-sourced firing and loses the complementary mass
to a mark.  It is not the kernel obtained by suppressing the lower clocks
and then renormalizing the (q)-clock.  With the latter convention the
resolvent identity in Section 5 would not be exact.

## 1. Localized augmented chain

Work before service or either declared localization.  At every open state
(x=(A,B,C)), (C>0), assume

\[
 \delta=\sup_{x}\max_{y\ne q}{M_x(y)\over M_x(q)}<1,
 \qquad M_x(y)=\prod_i(x_i+1)^{y_i},                         \tag{1.1}
\]

where the supremum is over the localized episode and over lower complexes
which are enabled at (x).  In the separated chart, the moving (B,C,A)
cutoffs give \(\delta=\delta_a\to0\).

Augment an open state by a phase (s).  After a reaction with lower target
(z), put (s=z); after a lower-to-(q) reaction put (s=q).  At a
cofactor-free base use the artificial phase (dB), where (d) is the
largest zero-cofactor source degree.  A reaction which lands at (C=0)
resets the phase to (dB).  Zero-vector self reactions may be deleted,
since their generator contribution is zero.

For fixed (0<\theta<1/2), define

\[
 w(x,s)={e^{\theta G_\ell(x)}\over M_x(s)^\theta}             \tag{1.2}
\]

at an open state and use the same formula with (s=dB) at a base.  The
use of (x_i+1) makes all bounded-jump comparisons uniform at coordinate
boundaries.

Let (K) be the actual embedded kernel, killed at service or localization.
Split it exactly as

\[
                              K=Q+R,                           \tag{1.3}
\]

where (Q) retains every base-sourced transition and, at an open state,
only (q)-sourced transitions; (R) retains the non-(q)-sourced
transitions at open states.  Thus (R) is precisely the first-mark
operator after any clean prefix.

For a positive kernel (T), write

\[
             \|T\|_w=\sup_\xi{(Tw)(\xi)\over w(\xi)}.         \tag{1.4}
\]

## 2. One mark is small in the phase weight

### Lemma 2.1 (sourcewise first-mark bound)

There is a constant (C), depending only on the fixed graph, rates,
(\ell), and \(\theta\), such that

\[
                              \|R\|_w
                    \le C\delta^{1-\theta}.                  \tag{2.1}
\]

#### Proof

At an open state put (r_y=M_x(y)/M_x(q)).  The total (q)-rate is
uniformly comparable with (M_x(q)), while an enabled lower edge with
source (y) has rate at most (CM_x(y)).  The bounded-degree factorial
identity gives, for (x'=x+z-y),

\[
 e^{\theta(G_\ell(x')-G_\ell(x))}
       \le C\left({M_x(z)\over M_x(y)}\right)^\theta.         \tag{2.2}
\]

If (x') is open, the phase rule cancels the target monomial.  Consequently
the corrected contribution of this edge is

\[
 {\lambda_{yz}(x)\over\lambda_{\rm tot}(x)}
 {w(x',s')\over w(x,s)}
       \le C r_y^{1-\theta}r_s^\theta.                        \tag{2.3}
\]

This formula also holds when (z=q), since then (s'=q).  If (x') is a
base, (s'=dB).  Its target (z=jB) has (j\le d), so the uncancelled
factor (M_{x'}(z)^\theta/M_{x'}(dB)^\theta) is bounded; bounded jumps
also make (M_x(dB)/M_{x'}(dB)) bounded.  Thus (2.3) remains valid up to a
fixed constant.

Every open lower source has (r_y\le\delta).  Moreover (r_s\le\delta)
when (s\ne q), while (r_q=1).  Dropping the latter factor and summing
over the fixed finite edge set proves (2.1).  Notice in particular that a
mark with target (q) costs \(r_y^{1-\theta}\) before its apparently free
(q)-exit; the raw factor (a^\theta) never appears by itself. \(\square\)

## 3. The clean open bridge

Write the clean kernel in base/open blocks as

\[
 Q=\begin{pmatrix}Q_{BB}&Q_{BO}\\Q_{OB}&Q_{OO}\end{pmatrix}. \tag{3.1}
\]

### Lemma 3.1 (at most one free (q)-step)

For all sufficiently small \(\delta\),

\[
                   \|(I-Q_{OO})^{-1}\|_w\le C.               \tag{3.2}
\]

#### Proof

For a (q\to z\ne q) firing at an open state, the same substitution as in
(2.3) gives

\[
 {\lambda_{qz}(x)\over\lambda_{\rm tot}(x)}
 {w(x',s')\over w(x,s)}\le C r_s^\theta.                     \tag{3.3}
\]

The estimate remains true for a return to (C=0), by the same
target-to-(dB) comparison used above.  If (s\ne q), (3.3) is
(O(\delta^\theta)).  If (s=q), it is only (O(1)), but every
nonabsorbed successor has a lower phase (s'=z\ne q).  Therefore

\[
                  \|Q_{OO}\|_w\le C,
        \qquad \|Q_{OO}^{,2}\|_w\le C\delta^\theta.         \tag{3.4}
\]

A reaction (q\to q) is a zero-vector self reaction and has already been
deleted.  Grouping the Green series in pairs now gives

\[
 \sum_{n\ge0}Q_{OO}^n
 =(I+Q_{OO})\sum_{j\ge0}Q_{OO}^{2j},                          \tag{3.5}
\]

and proves (3.2) once (C\delta^\theta<1\).  This is the precise sense in
which the phase-(q) exit is free only once. \(\square\)

Let

\[
 H=(I-Q_{OO})^{-1},\qquad
 S=Q_{BB}+Q_{BO}H Q_{OB}.                                    \tag{3.6}
\]

Here (S) is exactly the clean completed base-return kernel, with service
and localization mass killed.  Base launch factors are bounded: a source
(cB) contributes

\[
              C(1+B)^{-(1-\theta)(d-c)},                     \tag{3.7}
\]

and a direct cofactor-free return has the additional bounded factor
(M(z)^\theta/M(dB)^\theta).  Hence (Q_{BO}) and (Q_{OB}) have bounded
weighted norm.

### Lemma 3.2 (lifting the clean base Green bound)

Assume the clean completed-return estimate

\[
                         \|(I-S)^{-1}\|_{w|_B}\le C_0.        \tag{3.8}
\]

Then

\[
                              \|(I-Q)^{-1}\|_w\le C_1,        \tag{3.9}
\]

where (C_1) is independent of the separated parameter.

#### Proof

The Schur complement formula gives the four blocks

\[
\begin{aligned}
 [(I-Q)^{-1}]_{BB}&=(I-S)^{-1},\\
 [(I-Q)^{-1}]_{BO}&=(I-S)^{-1}Q_{BO}H,\\
 [(I-Q)^{-1}]_{OB}&=HQ_{OB}(I-S)^{-1},\\
 [(I-Q)^{-1}]_{OO}&=H+HQ_{OB}(I-S)^{-1}Q_{BO}H.
\end{aligned}                                                 \tag{3.10}
\]

Equations (3.2), (3.7), and (3.8) bound every block. \(\square\)

The hypothesis (3.8) is exactly where the maximal-source completed-return
ledger and its strong-cut corrector enter.  In the case (d=0), a clean
(0\to q\to0) completion is a literal self-return.  Every clean nonexact
completion services; a fixed directed cut from \(\{0,q\}\) bounds the
diagonal inverse.  Thus no false factor such as (a^\theta B/a) is used in
this case.

## 4. First-mark decomposition and arbitrary later marks

### Theorem 4.1 (completed first-mark contraction)

Under (1.1) and (3.8), with

\[
                         \eta=\min\{\theta,1-\theta\},        \tag{4.1}
\]

one has

\[
 \boxed{\quad
       \|R(I-Q)^{-1}\|_w+\|(I-Q)^{-1}R\|_w
             \le C\delta^\eta.\quad}                         \tag{4.2}
\]

In particular, the conditional corrected payoff beginning with the first
open lower-source firing and continuing through all subsequent clean
(q)-motion and clean base returns is (O(\delta^\eta)) relative to the
clean continuation Green weight.

#### Proof

By Lemmas 2.1 and 3.2 and submultiplicativity,

\[
 \|R(I-Q)^{-1}\|_w
       \le C_1C\delta^{1-\theta}
       \le C_2\delta^\eta.                                   \tag{4.3}
\]

The reverse ordering is identical.  Probabilistically, (4.3) is the strong
Markov decomposition at the first mark (T): (2.3) pays the causing
reaction, Lemma 3.1 carries a target-(q) mark through its one free
(q)-exit, and (3.9) sums the remaining clean continuation. \(\square\)

For sufficiently large separated parameter, the right side of (4.2) is
less than one.  Since (K=Q+R) is the exact physical killed kernel,

\[
\begin{aligned}
 (I-K)^{-1}
  &=(I-Q)^{-1}
       [I-R(I-Q)^{-1}]^{-1}\\
  &=(I-Q)^{-1}
       \sum_{j\ge0}[R(I-Q)^{-1}]^j.                           \tag{4.4}
\end{aligned}

Every (j)-th term is a clean prefix followed by exactly (j) marks,
each with its following clean continuation.  Hence (4.4) retains arbitrary
nested lower-to-(q) entries and arbitrary later marks; no deterministic
word cutoff is present.  Moreover

\[
 \|(I-K)^{-1}\|_w\le {C_1\over1-C\delta^\eta},
 \qquad
 \|(I-K)^{-1}-(I-Q)^{-1}\|_w\le C'\delta^\eta.               \tag{4.5}
\]

Projecting (4.4) from base to the next completed base return gives the
desired completed-word estimate (5.5) of the ledger note.  The
factor (O(\delta^\eta)) is attached to the first physical mark, while all
later marks are generated recursively by the same Neumann factor.

## 5. Exact scope

Theorem 4.1 closes only the ordered-word summation conditional on the clean
completed-return Green estimate (3.8) and the stated localization.  It does
not establish (3.8), remove localization, estimate physical time, or
convert the corrected exponential weight to the terminal raw
(G_\ell)-moment.  Those remain separate proof obligations.  No support,
orientation, path, or population enumeration is used.
