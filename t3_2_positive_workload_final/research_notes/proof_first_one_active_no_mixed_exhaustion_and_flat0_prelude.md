# The one-active no-mixed exhaustion and the degree-zero-flat prelude

**Proof-first seam theorem, 2026-08-12 PDT.**  This note closes only the
one-active interface described below.  It gives a symbolic support
classification and an unconditioned physical-time prelude for the
Bellman/degree-zero-flat case.  It does not claim recurrence of the whole
network or certify any global composition.

Finite support inspection appears only in the seven-row truth table in
Section 3 and in the optional counts in Section 5.  No orientation, rate
vector, reaction history, population box, or stochastic path is enumerated
to prove a stochastic estimate.

## 1. Exact scope and statement

Use species (X,U,V).  Fix two disjoint nontrivial binary linkage supports
(L_1,L_2), each with an arbitrary strongly connected orientation and
arbitrary fixed positive labelled rates.  Fix a terminal one-active chart in
one closed irreducible population class such that

* (X\to\infty) along the alleged escape;
* ((U,V)) ranges in one fixed finite padded phase box;
* enabled support, source-order cell, active set, and lattice data are fixed;
  and
* a reaction changing any of those data is retained as a physical structural
  exit.

Assume the support pair has **no raw mixed two-active occurrence**: for every
choice of two active species and every chamber or wall of the binary
comparison arrangement, the exact ordered Q/U/C/S classifier gives the same
available/shielded status to (L_1) and (L_2).

For one linkage (L), define the following mutually exclusive categories.

* **Q:** (2X\in L).
* **F:** all complexes in (L) have one constant (X)-degree.
* **B:** Q and F fail, and there are (q,c\in L) with
  
  \[
        q_X=1,quad c_X=0,quad q_U\le c_U,quad q_V\le c_V. \tag{1.1}
  \]
* **D:** Q, F, and B all fail.

The theorem proved here is the following exact alternative.

> **Theorem 1.1 (one-active no-mixed seam).**  Under the hypotheses above,
> every one-active chart belongs to one of:
>
> 1. **quadratic:** at least one linkage is Q, and the ordinary factorial
>    generator is coercively negative;
> 2. **flat:** both linkages are F, and (X) is a class invariant;
> 3. **Bellman/Bellman:** both linkages are B, and actual-target all-clock
>    Bellman episodes have coercive negative marked-factorial reward or record
>    a physical structural exit;
> 4. **Bellman/flat:** one linkage is B and the other is F of (X)-degree
>    zero; the finite all-clock prelude of Theorem 6.1 gives coercive negative
>    reward, a physical structural exit, or a closed no-history phase; or
> 5. **signed invariant:** up to exchanging (U,V) and the linkages, the
>    supports are one of the five pairs in (4.4), and (X-U-V) is a common
>    physical invariant.
>
> In particular, no D/B or D/D support pair remains after the no-mixed
> hypothesis.  The conclusions use actual endpoints and make no conditional
> activation assertion.

Sections 2--5 prove the support alternative.  Sections 6--8 prove the
Bellman/flat stochastic prelude.

## 2. Symbolic shape of a dormant linkage

After Q fails, every complex has (X)-degree zero or one.  The degree-one
binary menu is

\[
                         X,qquad X+U,qquad X+V,       \tag{2.1}
\]

and the degree-zero menu is

\[
                         0,U,V,2U,U+V,2V.              \tag{2.2}
\]

If a nonflat linkage contains (X), then (1.1) holds with any degree-zero
complex.  Hence a D linkage does not contain (X).  If it contains (X+U),
then failure of (1.1) says that none of its degree-zero complexes contains
(U).  Its lower block is therefore a nonempty subset of
({0,V,2V}).  The (X+V) statement is symmetric.  If both (X+U) and
(X+V) occur, a lower complex must contain neither (U) nor (V), so it is
(0).

Thus D has exactly one of the symbolic forms

\[
\begin{array}{c|c|c}
\text{degree-one block}&\text{degree-zero block}&
          \text{within-linkage signed invariant}\\ \hline
\{X+U\}&\varnothing\ne S\subseteq\{0,V,2V\}&X-U\\
\{X+V\}&\varnothing\ne S\subseteq\{0,U,2U\}&X-V\\
\{X+U,X+V\}&\{0\}&X-U-V.
\end{array}                                             \tag{2.3}
\]

This classification uses only binaryity and the coordinatewise condition
(1.1).

## 3. The single-token dormant forms force a mixed two-active chart

It suffices by symmetry to treat

\[
                         L=\{X+U\}\cup S,qquad
 \varnothing\ne S\subseteq\{0,V,2V\}.                \tag{3.1}
\]

In the two-active chart ((X,U)), the unique top (X+U) is active
quadratic, so (L) is available in every chamber and wall.  The remaining
two-active tests needed to exclude a disjoint status-matching partner are
displayed below.  Write (A) and (S) for available and shielded.  A pair
(((R),(a,b))) means active coordinates (R) with positive integer weights
((a,b)).  The fourth column lists **all** disjoint nontrivial supports which
match (L) at the first displayed test.

\[
\begin{array}{c|c|c|l|c|c}
S&d_1&L(d_1)&\text{matching supports after }d_1&d_2&L(d_2)\\ \hline
\{0\}&(X,V;3,2)&S&\{U,2U\},\{V,U+V\}&(U,V;1,1)&S\\
\{V\}&(X,V;3,2)&S&
 \{0,U\},\{0,2U\},\{U,2U\},\{0,U,2U\},\{0,U+V\}
 &(X,V;2,3)&A\\
\{2V\}&(X,V;2,1)&S&
 \{0,U\},\{0,2U\},\{U,2U\},\{0,U,2U\},\{0,U+V\},\{V,U+V\}
 &(X,V;1,1)&A\\
\{0,V\}&(X,V;3,2)&S&\{U,2U\}&(X,V;1,1)&A\\
\{0,2V\}&(X,V;3,1)&S&\{U,2U\},\{V,U+V\}&(X,V;1,1)&A\\
\{V,2V\}&(X,V;3,1)&S&
 \{0,U\},\{0,2U\},\{U,2U\},\{0,U,2U\},\{0,U+V\}
 &(X,V;1,1)&A\\
\{0,V,2V\}&(X,V;3,1)&S&\{U,2U\}&(X,V;1,1)&A.
\end{array}                                             \tag{3.2}
\]

In the first row, both surviving supports are available at (d_2).  In each
other row, every surviving support is shielded at (d_2).  Thus every
candidate disagrees with (L) at the second test.

For completeness, (3.2) is a literal symbolic evaluation of the ordered
classifier.  At each test, first take the top block; then apply, in order,
flat, active-quadratic, one-active-particle-flat, unary, and shared-bounded-
cofactor.  The disjoint universe after fixing (3.1) contains only the
remaining named binary complexes.  The supports in column four are obtained
by these five tests directly; no orientation or stochastic data enter.

Consequently the first two rows of (2.3) are incompatible with the no-mixed
hypothesis.  A surviving D linkage must be

\[
                         L_D=\{0,X+U,X+V\}.            \tag{3.3}
\]

## 4. Exact five-partner theorem and the common invariant

In the ((X,U)) and ((X,V)) charts, (3.3) is always available because its
top contains the corresponding active-quadratic complex.  In the ((U,V))
chart it is shielded on the equality wall and available in either open
chamber: on the wall the top mixed complexes are not unary and share no
bounded cofactor with the lower (0); off the wall the top one and the lower
other one share bounded (X).

A disjoint partner having this same signature must be flat in total
(U+V)-degree on the equality wall and must have a changing top in both open
chambers.  The degree-zero shell cannot change top.  The degree-one shell,
after removing the already used (X+U,X+V), leaves only (U,V), and both
are required.  The degree-two shell is ({2U,U+V,2V}); a support must meet
both sides of its linear order.  Hence the exact partners are

\[
\begin{split}
 L_F\in\{&\{U,V\},\ \{2U,2V\},\ \{2U,U+V\},\\
          &\{2V,U+V\},\ \{2U,2V,U+V\}\}.
                                                               \tag{4.1}
\end{split}
\]

The same conclusion follows by applying the flat and active-quadratic tests
literally to the three total-degree shells; no larger binary shell exists.

Define

\[
                             H=X-U-V.                  \tag{4.2}
\]

Every complex of (L_D) has (H)-value zero.  The first support in (4.1)
has constant (H)-value (-1), and the other four have constant value
(-2).  Therefore every reaction of either linkage preserves (H): it is a
common physical invariant, for every strong orientation and every rate
vector.

The exact five unordered support pairs are therefore

\[
\begin{array}{c|c}
L_D&L_F\\ \hline
\{0,X+U,X+V\}&\{U,V\}\\
\{0,X+U,X+V\}&\{2U,2V\}\\
\{0,X+U,X+V\}&\{2U,U+V\}\\
\{0,X+U,X+V\}&\{2V,U+V\}\\
\{0,X+U,X+V\}&\{2U,2V,U+V\}.
\end{array}                                             \tag{4.3}
\]

On a one-active chart (U,V) are bounded.  Constancy of (4.2) on the fixed
class gives (X=H+U+V), so (X) is bounded as well.  The five pairs cannot
carry the alleged escape.

## 5. The remaining symbolic alternatives

If a linkage contains (2X), then (2X) is enabled for all large (X).
Every nonzero outgoing reaction from it lowers (X)-degree, because it is the
only binary complex of degree two.  For the ordinary factorial potential

\[
                         V(x)=\sum_i\log(x_i!),         \tag{5.1}
\]

that reaction has increment at most (-\log X+O(1)) and rate of order
(X^2).  Every other source has rate (O(X)) and positive increment
(O(\log X)), uniformly in the inactive box.  Thus

\[
                         {\cal L}V(x)\longrightarrow-\infty. \tag{5.2}
\]

Strong connectivity guarantees at least one nonzero outgoing label at
(2X); projected zero-displacement labels do not enter the CTMC.

If both linkages are F, every reaction preserves (X) exactly.  A nontrivial
binary flat linkage has degree zero or one.  The two linkages need not have
the same degree, but (X) is still a global class invariant.

If neither of these alternatives applies and there is no D linkage, the pair
is B/B or B/F.  The no-mixed hypothesis forces the flat member of a B/F pair
to have degree zero: a degree-one flat support paired with a nonflat B support
has opposite status in one of the ((X,U)), ((X,V)), or ((U,V)) cells.
This is the same top-block argument as Section 3.

As a non-load-bearing regression identity, exact support replay gives, for
each fixed choice of (X),

\[
\begin{array}{c|r}
\text{unordered category pair}&\text{no-mixed supports}\\ \hline
Q/B&6,050\\
Q/F_0&1,352\\
Q/F_1&54\\
B/B&1,224\\
B/F_0&731\\
F_0/F_0&19\\
F_0/F_1&54\\
D/F_0&5\\ \hline
\text{total}&9,489.
\end{array}                                             \tag{5.3}
\]

The proof of exhaustion is Sections 2--5, not the counts in (5.3).

## 6. The finite all-clock prelude for B/F0

Let (L_B) be the Bellman linkage and (L_0) the flat linkage.  Every source
and target in (L_0) has (X)-degree zero.  Fix (q,c\in L_B) satisfying
(1.1).  Carry the actual target (t) of the preceding physical reaction and
use the marked factorial potential

\[
                         F(x,t)=\sum_i\log((x_i-t_i)!). \tag{6.1}
\]

### 6.1 Finite pre-activation phase

Before the first (L_B) reaction, only (L_0) reactions occur.  They leave
(X) unchanged.  Record the inactive population ((U,V)), the actual flat
target mark, and the fixed chart labels.  This gives a finite phase set
({\cal P}).

Adjoin three absorbing sections:

* (A): the actual endpoint and target of the first (L_B) reaction;
* (E): the actual reaction causing a declared structural exit; and
* (H): a closed flat-only component from which no (L_B) source and no
  exit is reachable by an in-chart (L_0) path.

The firing which reaches (A,E), or (H) is included.  Let (sigma) be
this absorption time and (N_sigma) its physical reaction count.

All (L_0) propensities depend only on the finite inactive phase.  Hence
their positive values lie between constants (k_*>0) and (K_*<\infty).
An enabled (L_B) source has degree zero or one.  Its positive propensity is
at least (k_*); a degree-one source has propensity of order (X), which can
only accelerate absorption in (A).

No uniform activation probability is assumed.  It follows from the finite
graph.  From a transient phase from which (A) is reachable before (E\cup H),
choose a simple flat path to the first phase with positive (L_B) hazard.
At every earlier phase that hazard is zero, and the probability of taking the
chosen positive flat label is at least (k_*/K), where (K) bounds the total
flat and exit rate on the finite box.  At the last phase, the probability that
an (L_B) label fires before a flat label is at least

\[
                         {k_*\over k_*+K}.             \tag{6.2}
\]

A degree-one hazard only increases this probability.  Since a simple path
has length at most (|{\cal P}|-1), there is a derived constant
(ho>0), independent of (X), such that

\[
 \mathbb P_p(A\text{ before }E\cup H)\ge\rho          \tag{6.3}
\]

whenever (A) is graph-reachable from (p).  If it is not reachable, the
finite phase is absorbed in (E\cup H); activation probability is exactly
zero, not a missing small parameter.

The same simple-path argument, now aimed at (A\cup E\cup H), gives a
uniform positive absorption probability in each block of
(|{\cal P}|) jumps.  Thus for every fixed (r<\infty),

\[
                 \sup_{X,p}\mathbb E_p N_\sigma^r<\infty. \tag{6.4}
\]

At every pre-absorption state the current flat target is enabled and has an
outgoing flat label, so the total physical hazard is at least (k_*).  A
geometric number of conditionally exponential holding times therefore gives

\[
                         \sup_{X,p}\mathbb E_p\sigma^r<\infty. \tag{6.5}
\]

Equations (6.3)--(6.5) derive the needed activation/absorption estimates from
the literal finite physical phase.

### 6.2 Marked reward of the prelude

For a flat jump (y\to u), both the current mark (t) and source (y) have
(X)-degree zero.  The exact increment is

\[
 F(x-y+u,u)-F(x,t)=\log{(x)_t\over(x)_y},             \tag{6.6}
\]

which is uniformly bounded in absolute value on the padded inactive box.
For the first (L_B) reaction, the current mark still has degree zero.  If
its source has degree zero, (6.6) remains bounded.  If its source has degree
one, then

\[
                         \log{(x)_t\over(x)_y}
                              =-\log X+O(1).            \tag{6.7}
\]

Consequently the positive part of the complete prelude reward
(R_\sigma=F(X_\sigma,T_\sigma)-F(x,t)) satisfies, for every fixed (r),

\[
                         \sup_{X,p}\mathbb E_p(R_\sigma^+)^r<\infty. \tag{6.8}
\]

This follows from (6.4) and the bounded flat increments; the activation jump
cannot have an unbounded positive part.

## 7. Actual-target Bellman handoff

On absorption in (A), let (uin L_B) be the actual target of the included
activation reaction and let (x') be its actual population endpoint.  The
activation jump is not counted again.  Starting from the marked state
((x',u)), choose a simple same-linkage path

\[
                         u=y_0\to y_1\to\cdots\to y_m=c. \tag{7.1}
\]

Every designated source is physical because it is the preceding actual
target.  On path success the population telescopes to

\[
                         z=x'-u+c\ge c.                \tag{7.2}
\]

The active coordinate still diverges because (x'_X-X) is bounded.  At
(z), condition (1.1) enables (q), and (q_X=1>c_X=0).  Therefore

\[
                         p_c(z)\le{\lambda_c(z)\over\lambda_q(z)}
                                  \longrightarrow0.     \tag{7.3}
\]

Retain every physical clock, stop on the first deviation, and take one final
ordinary jump after reaching (c).  If (D_i) is the expected marked reward
of the ordinary all-clock jump at success-prefix stage (i), and (a_i) is
the probability of the next exact designated label, the unconditioned
recursion is

\[
                         J_m=D_m,qquad J_i=D_i+a_iJ_{i+1}. \tag{7.4}
\]

The exact source-entropy identity gives (D_i\le\log p_{y_i}+C).  At the
first source whose probability vanishes, (D_i\to-\infty); all earlier
label probabilities have positive limits, while the later positive tail is
multiplied by the vanishing label probability.  Hence, uniformly over the
finite set of activation endpoints and marks,

\[
                         J_0\le-A_X,qquad A_X\longrightarrow\infty, \tag{7.5}
\]

unless the designated prefix records a physical structural exit.  The same
one-jump source-weighted entropy bound gives every fixed positive reward
moment.  The Bellman continuation has at most ten jumps and uniformly bounded
physical-time moments.

The construction is pathwise nonoverlapping: the first (L_B) reaction is
the terminal jump of the prelude, its target initializes (7.1), and the first
jump counted by (7.4) is the **next** physical reaction.

## 8. The combined B/F0 alternative

Append the Bellman continuation of Section 7 only on (A).  Let (	au) be
the combined endpoint.  If activation is graph-reachable from the starting
finite phase, (6.3), (6.8), and (7.5) give

\[
 \mathbb E_{x,t}[F(X_\tau,T_\tau)-F(x,t)]
                         \le C-\rho A_X\longrightarrow-\infty, \tag{8.1}
\]

unless the prelude or Bellman prefix has positive physical structural-exit
probability.  This is not conditioning on activation: (8.1) averages the
activation, every waiting jump, deviations, and the actual endpoint under
the original all-clock law.  The lower bound (ho) was proved from the
finite graph rather than assumed.

If activation is not graph-reachable, the prelude ends in (E\cup H).  An
(E) endpoint is the retained physical structural exit.  In (H), every
enabled physical reaction belongs to (L_0), preserves (X), and stays in
the closed flat phase; no (L_B) source can become enabled.  If a closed
irreducible population class reaches (H), its reachable component has that
fixed value of (X).  It cannot support a one-active escape.  This is the
exact no-history alternative, not a stochastic drift claim.

Combining (6.4)--(6.5) with the bounded Bellman depth gives, for every fixed
(r<\infty),

\[
 \sup\mathbb E\tau^r<\infty,qquad
 \sup\mathbb E[(F(X_\tau,T_\tau)-F(x,t))^+]^r<\infty. \tag{8.2}
\]

The endpoint is always the actual physical endpoint and actual target of the
last included reaction.

> **Theorem 8.1 (degree-zero-flat prelude).**  Every B/F0 chart has the exact
> unconditioned alternative (8.1), physical structural exit, or closed
> no-history.  The stopping rule retains all clocks, includes the activation
> and exit-causing reactions once, uses the single marked potential (6.1),
> and satisfies (8.2).  It assumes no activation probability or mixing rate.

## 9. Scope of composition

On a supplied reaction-count terminal chart, a positive structural-exit flux
contradicts terminality, the Q and Bellman rewards contradict nonnegative
terminal workload/entropy balance, and the exact invariants or no-history
alternatives contradict one-active escape in the fixed class.  Within that
Green-occupation route, different alternatives need not share one global
Foster potential because the proof fixes one terminal chart and never follows
an exit into another chart.

This note does not itself prove the terminal-chart Green theorem, does not
prove a global state-selected Foster theorem with potential switching, and
does not assert positive recurrence.  Those are separate dependencies.  Its
durable conclusion is exactly Theorem 1.1 and the B/F0 physical seam in
Theorem 8.1.

