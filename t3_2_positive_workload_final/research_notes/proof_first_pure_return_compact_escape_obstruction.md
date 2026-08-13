# Compact escape resistance and the correct pure-return renewal

**Proof-only verdict (2026-08-11 PDT).**  Equation (5.11) in
*two_active_dormant_407_two_level_repair.md* is false, even at a
historically reachable positive-debt base.  The failure is not a matter of
the constant: in the example below the left side is of exact order (n),
whereas the asserted right side is (O(1)).  After the pure loops are
renewed, the upward exit has probability (1/3+O(n^{-1})), not
(n^{-1+o(1)}), and service has probability (1/3+O(n^{-1})), not
(1-o(1)).  The pure-loop duration is of order (n).

There is nevertheless a proof-first repair for this particular support.
The three order-one exits must be retained in one finite physical phase
kernel, rather than treating the nonexact interrupted exits as a small
perturbation.  Renewal of that phase kernel up to strict service gives
service probability (1-O(n^{-1})), endpoint decrement
(-log n+O(1)) for every fixed common (F_\ell), and a fourth-power
Foster episode.  Its duration moments are (O(n^q)).  This note proves that
support-local statement only.  It does not repair the other exact-pair
supports, certify the hard-317 kernel, or promote any incidence or pair.
No finite path enumeration is used.

## 1. An admissible historically consistent support

Use the normalized species ((U,V,I)) and take

\[
 {cal L}_+=\{0,V+I\},\qquad
 {cal L}_0=\{I,2U,2I,U+I\}.                         \tag{1.1}
\]

Orient the proper pair in both directions, put the complete directed graph
on the lower support, and give every reaction rate one.  Both linkages are
strong.  Start the reachable reflected lift at
(x^\circ=(0,0,0)), with every debt mark zero.  The physical word

\[
 0\longrightarrow V+I,quad
 0\longrightarrow V+I,quad
 2I\longrightarrow I,quad
 V+I\longrightarrow0                                      \tag{1.2}
\]

sends ((0,m,0)) to ((0,m+1,0)).  It is feasible for every (m\ge0).
Along (1.2), reflection is inactive in the (V)-coordinate and hence
(D_V=V).  Repeating (1.2) proves that

\[
                  x_n=(0,n,0),\qquad D_V=n,                 \tag{1.3}
\]

is historically reachable for every (n\ge1).  Thus neither compact
nontrapping nor the positive-debt hypothesis excludes these bases.

## 2. The pure inverse is (\Theta(n))

At (x_n), the only enabled reaction is (0\to V+I), so the first state
of every raw attempt is

\[
                         y_n=(0,n+1,1).                       \tag{2.1}
\]

At (y_n), the enabled clocks and their rates are

\[
\begin{array}{c|c}
\text{reaction}&\text{rate}\\ \hline
V+I\to0&n+1\\
0\to V+I&1\\
I\to2U, I\to2I, I\to U+I&1\text{ each}.
\end{array}                                                    \tag{2.2}
\]

If the first clock in (2.2) fires, the two-reaction attempt is a pure exact
return.  If (I\to2U) fires, the attempt ends immediately at the upward
no-fast state ((2,n+1,0)) and is not pure.  Consequently

\[
 {n+1\over n+5}\le Z^{\rm pure}(x_n)
       \le1-{1\over n+5},                                      \tag{2.3}
\]

and therefore

\[
 {n+5\over4}\le {1\over1-Z^{\rm pure}(x_n)}\le n+5.           \tag{2.4}
\]

In (1.1), the maximal (I)-free lower source is (2U), so the degree
used in (5.11) is (d=2).  At (u=0), its asserted upper bound is
(C(1+u)^{2-d}=C), in direct contradiction with (2.4).

The exact leading order is also elementary.  From height (I=1), the
probability of a nested zero-source opening is (O(n^{-1})).  Conditional
on such an opening, the probability of a lower firing before the fast
chain descends again is (O(n^{-1})).  At every larger pure height (i),
the downward rate is ((n+i)i), while the total zero-source plus lower
hazard is at most (C(1+i)^2).  Summing the resulting descending
birth--death race gives

\[
 1-Z^{\rm pure}(x_n)={3\over n}+O(n^{-2}),\qquad
 (1-Z^{\rm pure}(x_n))^{-1}={n\over3}+O(1).                    \tag{2.5}
\]

A pure path which reaches any cutoff (L_n\to\infty) has probability
smaller than every fixed power of (n^{-1}), and does not affect (2.5).

There is a second duration consequence.  Every pure attempt includes a
base wait of mean one for (0\to V+I), and a raw attempt is nonpure with
probability (\Theta(n^{-1})).  Hence, if (T_n) is the time to the first
nonpure raw attempt after pure renewal, then, for every fixed integer
(q\ge1),

\[
                     \mathbb E T_n^q=\Theta(n^q).                \tag{2.6}
\]

Thus a duration bound depending polynomially on (1+u) but not on (n)
is false at this same base.

## 3. What replaces the false spectator exponent

The compact-base exponent is an **escape resistance**, not the difference
between two spectator source degrees.  To state the elementary form needed
here, consider an exact pair ({aU,V+I}) at a fixed compact spectator
value.  Suppose no nonpure base clock is enabled.  Let (m) be the least
positive inactive population at which a nonpure slow source becomes
enabled along pure nested openings.  A pure attempt must win (m-1)
nested-opening races and then one slow-defect race, each against a fast
clock of order (n).  Conversely, any fixed directed defect edge at that
height supplies the matching lower bound.  Therefore

\[
             1-Z^{\rm pure}=\Theta(n^{-m}),\qquad
             (1-Z^{\rm pure})^{-1}=\Theta(n^m).                  \tag{3.1}
\]

For binary supports, (m\le2) whenever such an escape exists.  Historical
positive-debt transience says only that an escape exists for each fixed
(n); it does not replace (n^m) by a uniform compact constant.  In
(1.1), (m=1).  The other possible compact exponent really occurs: for

\[
 \{0,V+I\},\qquad \{U,2U,2I,U+I\},                              \tag{3.2}
\]

with complete unit-rate orientations, the first enabled defect requires a
nested opening to height two and then a (2I)-source firing, so the pure
inverse is (\Theta(n^2)).  Historical positive debt is still reachable,
because

\[
 (0\to V+I)^3,quad 2I\to U,quad U+I\to2I,quad
 (V+I\to0)^2                                             \tag{3.3}
\]

sends ((0,m,0)) to ((0,m+1,0)) and again keeps (D_V=V).

Away from the compact spectator set, an enabled degree-(d) base escape
can still give the factor (C(1+u)^{2-d}).  A correct uniform statement
must therefore retain a compact term of order (n^m).  More usefully, it
should avoid estimating the pure inverse in isolation.  If (K^{\rm np})
is the sum of all nonpure exit kernels, the normalized kernel

\[
             P_n=(1-Z^{\rm pure})^{-1}K^{\rm np}                 \tag{3.4}
\]

is the law of the first nonpure attempt.  Its order-one pieces must be
analyzed as physical transitions.  Only a ratio such as

\[
 {Z^{\rm int}\over1-Z^{\rm pure}}
   =\mathbb P\{\text{first nonpure attempt is an interrupted exact
                 return}\}                                      \tag{3.5}
\]

is a candidate small parameter.

## 4. The exact first-nonpure exit law

Return to (1.1).  Let (A_n,C_n,D_n) denote the raw kernels of the
following three disjoint paths after the forced opening:

\[
\begin{array}{c|c|c}
\text{first lower edge}&\text{fast completion}&\text{endpoint}\\ \hline
I\to2U&\text{none}&(2,n+1,0)\\
I\to U+I&V+I\to0&(1,n,0)\\
I\to2I&(V+I\to0)^2&(0,n-1,0).
\end{array}                                                       \tag{4.1}
\]

The last fast firing in the third row is strict service.  Equations
(2.2) and the fast hazards after the first lower edge give

\[
 A_n={1\over n}+O(n^{-2}),\qquad
 C_n={1\over n}+O(n^{-2}),\qquad
 D_n={1\over n}+O(n^{-2}).                                      \tag{4.2}
\]

Any other nonpure outcome requires either a nested opening followed by a
defect, or another slow firing before the indicated fast completion.  Its
total raw probability is (O(n^{-2})).  Dividing (4.2) by (2.5) proves

\[
\begin{aligned}
 (1-Z^{\rm pure})^{-1}A_n&={1\over3}+O(n^{-1}),\\
 (1-Z^{\rm pure})^{-1}C_n&={1\over3}+O(n^{-1}),\\
 (1-Z^{\rm pure})^{-1}D_n&={1\over3}+O(n^{-1}).                  \tag{4.3}
\end{aligned}
\]

An interrupted exact return needs at least two lower firings, since the
proper opening and matching cleanup cancel exactly and one edge between
distinct lower complexes cannot have zero reaction vector.  The second
lower firing must again beat a fast clock.  Thus

\[
       (1-Z^{\rm pure})^{-1}Z^{\rm int}=O(n^{-1}).                \tag{4.4}
\]

This proves the important distinction: the interrupted **exact** diagonal
is still small in this example, but the interrupted nonexact and terminal
pieces are order one.  They cannot be put into the perturbative kernel
claimed in the current repair.

## 5. A finite regenerative repair for this support

The order-one upward probability in (4.3) is not itself a recurrence
counterexample.  It deposits two spectator molecules together with one
unit of reserve.  Retaining that physical phase gives a finite killed
kernel.

Use (R=V-n), and consider the five nonterminal no-fast phases

\[
 {cal S}=\{(0,0),(1,0),(2,0),(2,1),(3,1)\},                    \tag{5.1}
\]

where each pair is ((U,R)).  Pure proper loops are renewed, but no
nonpure physical transition is erased.  At phases (U=0,1), wait through
the renewed proper loops until the first lower firing.  At phases (U\ge2),
renew harmless proper loops until a (2U)-source lower firing.  Then retain
the actual fast cleanup and stop if its firing at (R=0) is strict
service.

For unit rates, the limiting embedded transitions are read directly from
the enabled physical sources:

\[
\begin{array}{c|l}
(0,0)&I\to2U:(2,1),\quad I\to2I:D,\quad I\to U+I:(1,0),\\
(1,0)&I\to2U:(3,1),\quad I\to2I:D,\quad I\to U+I:(2,0),\\
     &U+I\to I:(0,0),\quad U+I\to2U:(2,1),\quad U+I\to2I:D,\\
(2,1)&2U\to I:(0,0),\quad2U\to2I:D,\quad2U\to U+I:(1,0),\\
(3,1)&2U\to I:(1,0),\quad2U\to2I:D,\quad2U\to U+I:(2,0),\\
(2,0)&2U\to I,2I,U+I:D.
\end{array}                                                       \tag{5.2}
\]

Here (D) is the first included strict-service firing.  Each of the three
arrows in a row with one enabled source has probability (1/3); the six
arrows from ((1,0)) have probability (1/6).  In particular, every
nonterminal phase has one-step killing probability at least (1/3).
The limiting Green matrix on ({\cal S}) is therefore finite, and its
absorption time has a geometric tail.

The finite-(n) physical kernel differs from (5.2) by (O(n^{-1})) in
each row.  Indeed, after a prescribed lower firing, every additional slow
clock is (O(1)) while the required cleanup clock is at least (cn).
At (U=0,1), nested proper openings which clean up again are part of the
pure renewal.  A nested opening can change the first-defect law only if a
further slow clock beats a fast cleanup, which has total renewed
probability (O(n^{-1})).  At (U\ge2), the number of harmless proper
loops before the enabled (2U)-source edge has bounded geometric moments,
and the same fast-race estimate applies.

Since the Green matrix of (5.2) is finite, the resolvent identity transfers
these row estimates through the whole phase episode.  If every anomalous
race is stopped and retained at its actual endpoint, then, starting from
((0,n,0)),

\[
 \mathbb P(D)=1-O(n^{-1}),\qquad
 \mathbb P(\text{anomalous endpoint})=O(n^{-1}).                 \tag{5.3}
\]

On (D), the actual old-active endpoint is (V=n-1); the other two
coordinates are bounded.  The number of phase transitions has uniformly
bounded moments.  The waiting time for a lower firing at (U=0,1) has
moments (O(n^q)), by the same geometric-sum calculation as (2.6), while
all other phase waits have bounded moments.  Hence the full regenerative
duration (	au_n) obeys

\[
                         \mathbb E\tau_n^q=O(n^q).                \tag{5.4}
\]

This proof uses only the displayed hazards and the finite Green matrix in
(5.2), not a bounded-depth reaction search.

## 6. Common-potential drift after regeneration

Fix any vector (\ell), choose (K_\ell) so that

\[
 F_\ell(x)=K_\ell+\sum_j\log(x_j!)+\ell\mathbin\cdot x\ge1,
 \qquad W_\ell=F_\ell^4.                                      \tag{6.1}
\]

At the start (x_n=(0,n,0)), (F_\ell(x_n)\asymp n\log n).  On the
good service event in (5.3), boundedness of (U,I) gives

\[
               F_\ell(X_{\tau_n})-F_\ell(x_n)
                    =-\log n+O_\ell(1).                          \tag{6.2}
\]

The stopped anomalous races have probability (O(n^{-1})); the fast-race
tail gives every fixed endpoint moment needed to charge their actual
coordinates.  Consequently, for fixed (q\le4),

\[
 \mathbb E\Delta F_\ell=-\log n+O_\ell(1),\qquad
 \mathbb E|\Delta F_\ell|^q=O_\ell(\log^q n).                   \tag{6.3}
\]

Expanding the fourth power and using (5.4) with (q=1) now yields

\[
 \mathbb E_{x_n}
   [W_\ell(X_{\tau_n})-W_\ell(x_n)+\tau_n]
 \le -cF_\ell(x_n)^3\log n                                  \tag{6.4}
\]

for all large (n).  Indeed, the leading term is
(-4F_\ell(x_n)^3\log n+O(F_\ell(x_n)^3)); every Taylor remainder is
(O(F_\ell(x_n)^2\log^2n+\log^4n)), and
(mathbb E\tau_n=O(n)) is smaller still.

Thus a regenerative/coboundary repair **can** recover the common-
(W_\ell) drift for the exact support (1.1), despite its constant upward
first-exit probability.  What cannot survive is the present proof's claim
that the upward exit is rare, that the nonexact interrupted kernel is a
small perturbation, or that the pure-renewed duration is polynomial only
in (1+u).

## 7. Strict claim boundary

The theorem-level conclusions of this note are:

1. the uniform estimate (5.11) of the current hard repair is false;
2. its asserted rare-upward/service-one first-exit partition is false on
   (1.1);
3. the compact pure-renewal duration asserted in Section 7 is false;
4. the correct compact inverse is governed by the escape resistance
   (m), and equals (\Theta(n)) in (1.1) and (\Theta(n^2)) in (3.2);
5. the normalized first-nonpure kernel (3.4), followed by a finite physical
   phase regeneration, repairs (1.1) and gives (6.4).

Items 1--4 are exact counterexamples to the current canonical proof.
Item 5 is a complete analytic repair only for (1.1).  A hard-317 theorem
requires an analogous structural phase argument for every compact
exact-pair alternative, plus independent composition and endpoint audits.

