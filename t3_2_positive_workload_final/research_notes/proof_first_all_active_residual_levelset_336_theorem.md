# The residual 336 all-active level-set theorem

**Proof-first physical-time theorem and exact finite support identity,
2026-08-12 PDT.**  This note closes the residual all-active branch left after
the mixed-atlas, strictly-positive-invariant, deficiency-zero, corrected
S-tier-cut, and affine-feasibility reductions.  The stochastic argument is a
direct generator calculation.  Finite computation is used only to prove that
the residual set is exactly the support family to which that calculation
applies.

The result is local to an all-active terminal chart.  It supplies the
physical-time Foster branch needed by a global chart composition; it does not
by itself claim recurrence of a network whose other terminal charts have not
been treated.

## 1. Correct analytic family

Let

\[
 {\mathcal C}_2=\{0,A,B,C,2A,2B,2C,A+B,A+C,B+C\}.
                                                               \tag{1.1}
\]

Consider a binary stochastic mass-action network with two disjoint linkage
supports \(T,R\subseteq{\mathcal C}_2\).  On each support fix an arbitrary
strongly connected directed reaction graph and arbitrary positive labelled
rate constants.  Suppose that there are \(h\in(0,\infty)^3\), \(s>0\), and
a set \(U\) of two or three distinct unary complexes such that

\[
 \begin{split}
  &\operatorname{rank}\operatorname{span}\{y-z:y,z\in T\}=2,\\
  &h\cdot y=2s \quad(y\in T),\\
  &R=\{0\}\mathbin\cup U,
       \qquad h\cdot u=s \quad(u\in U).
 \end{split}                                                   \tag{1.2}
\]

The rank condition makes the normal to the affine hull of \(T\)
one-dimensional.  Thus the positive normal \(h\) is unique up to multiplication
by a positive scalar.  Neither the cardinality nor the deficiency of \(T\)
is restricted beyond (1.2).

The initially proposed narrower formulation -- three quadratic complexes in
\(T\) and exactly two nonzero unary complexes in \(R\) -- is false as an
exhaustion statement.  The exact family contains \(T\)-supports of sizes
three through six, contains 78 incidences with all three unaries in \(R\),
and contains 24 incidences in which \(T\) itself has a unary complex.  For
example,

\[
 h=(1,1,2),\qquad
 T=\{C,2A,2B\},\qquad R=\{0,A,B\}                     \tag{1.3}
\]

satisfies (1.2) with \(s=1\), but \(T\) is not wholly quadratic.  The
level-set formulation (1.2) is the exact upward family and requires no case
split for this exception.

## 2. Direct physical-time generator calculation

Define the proper linear function

\[
                         H(x)=h\cdot x.                         \tag{2.1}
\]

It is proper on \({\mathbb Z}_{\ge0}^3\) because all three entries of \(h\)
are strictly positive.  For a reaction \(y\to z\), the generator contribution
to \(H\) is

\[
                 \kappa_{yz}(x)_y\,h\cdot(z-y),                \tag{2.2}
\]

where \((x)_y\) is the falling-factorial source monomial.

Every reaction internal to \(T\) preserves \(H\), by (1.2).  Hence

\[
                         {\mathcal L}_T H(x)=0                  \tag{2.3}
\]

for every orientation, every positive rate vector, and every population
state.  In particular arbitrarily fast quadratic clocks in \(T\) do not need
to be estimated or averaged.

For \(u\in U\), write \(i(u)\) for its species coordinate.  All targets of a
reaction sourced at \(u\) have \(H\)-level either \(s\) or zero.  Therefore

\[
 b_u:=\sum_{u\to z}\kappa_{uz}\,h\cdot(z-u)
     =-s\sum_{u\to0}\kappa_{u0}\le0.                          \tag{2.4}
\]

Similarly the zero-complex clock has constant propensity one and coefficient

\[
 b_0:=\sum_{0\to z}\kappa_{0z}\,h\cdot z
     =s\sum_{0\to u}\kappa_{0u}.                              \tag{2.5}
\]

This is a finite constant.  Strong connectivity of the graph on \(R\)
forces at least one edge entering zero: take the last edge of any directed
path from a unary vertex to zero.  Consequently there is \(u_*\in U\) with

\[
                     c_*:=-b_{u_*}
                         =s\sum_{u_*\to0}\kappa_{u_*0}>0.       \tag{2.6}
\]

Since the mass-action propensity of unary \(u\) is \(x_{i(u)}\), equations
(2.3)--(2.6) give the exact identity

\[
 \begin{split}
 {\mathcal L}H(x)
   &=b_0+\sum_{u\in U}b_u x_{i(u)}\\
   &\le b_0-c_*x_{i(u_*)}.
 \end{split}                                                   \tag{2.7}
\]

No transition probability, embedded-chain holding time, orientation list,
or path list appears in (2.7).

## 3. All-active terminal-chart exclusion

Let \(x_n\) be any all-active escaping sequence, so

\[
             (x_n)_A\longrightarrow\infty,\qquad
             (x_n)_B\longrightarrow\infty,\qquad
             (x_n)_C\longrightarrow\infty.                    \tag{3.1}
\]

The particular coordinate \(i(u_*)\) in (2.7) therefore diverges.  Thus

\[
                   {\mathcal L}H(x_n)\longrightarrow-\infty.  \tag{3.2}
\]

This proves the following statement.

> **Theorem 3.1 (all-active level-set Foster theorem).**  Every two-linkage
> binary network satisfying (1.2), with arbitrary strongly connected
> reaction graphs and arbitrary fixed positive rate constants, admits the
> proper linear function \(H=h\cdot x\) for which (2.7) holds.  Its
> physical-time generator tends to minus infinity along every all-active
> escaping sequence.  Hence no all-active terminal chart of this family can
> be a nondescending escape branch in a classwise Foster composition.

The conclusion is stronger than a negative constant drift: it is coercive
in one of the coordinates which the chart declares divergent.  Neutral
reactions in \(T\), including quadratic reactions with rates of order
\(|x|^2\), contribute exactly zero rather than an error term.

## 4. Exact finite universe

The finite certificate begins from all ordered pairs of disjoint supports in
\({\mathcal C}_2\), each having at least two complexes.  Inclusion-exclusion gives

\[
 \begin{split}
 N
  &=3^{10}-2\bigl(2^{10}+10\,2^9\bigr)
       +\bigl(1+10+10+90\bigr)\\
  &=46{,}872.
 \end{split}                                                   \tag{4.1}
\]

The precise inherited mixed-atlas prebranch is defined set-theoretically,
not by a new stochastic classifier.  Take the union of the two tables
returned by

    unique_pairs(POSITIVE_SHIELDED_MASKS)
    unique_pairs(SIGNED_SHIELDED_MASKS)

which has 5,169 ordered seed pairs, and close it under every species
permutation and linkage reversal.  The resulting orbit has 27,894 pairs.
Its complement in (4.1) has 18,978 pairs.  The proper strictly-positive-
invariant branch removes 146 of them.  The subsequent deficiency-zero branch
removes no additional pair, leaving 18,832 pairs.

There are 68 pairs among these 18,832 which would have been removed by the
weaker predicate requiring positivity only in two named active coordinates.
They are deliberately retained: that weaker invariant is not proper on an
all-active escape.  All 68 have zero corrected affine-feasible all-active
failure incidences, so retaining them changes neither the set in (4.2) nor its
fingerprint.  This check prevents an invalid composition shortcut through an
active-only invariant.

There are 169 exact tier-arrangement descriptors with all three coordinates
active.  On the Cartesian product of the 18,832 pairs and those descriptors,
retain precisely the incidences which

1. fail the corrected S-tier-superlevel universal strong-orientation cut; and
2. are feasible in an affine stoichiometric class.

This leaves exactly

\[
                   336\text{ incidences on }336\text{ pairs}. \tag{4.2}
\]

Independently, apply only the following support predicate to the same finite
universe: one linkage has internal rank two and lies entirely on \(h\)-level
\(2s\); the other is zero plus two or three unaries, all on \(h\)-level \(s\),
for the descriptor weight \(h>0\).  The output is the identical set of 336
incidences.  This proves that (1.2), rather than the narrower three-by-three
shape, is the exact analytic family.

## 5. Geometry of all 336 incidences

The exact histograms are

\[
\begin{array}{c|rrrr}
h & (1,1,1)&(1,1,2)&(1,2,1)&(2,1,1)\\ \hline
\text{incidences}&312&8&8&8
\end{array}                                                    \tag{5.1}
\]

and

\[
\begin{array}{c|rrrr}
|T|&3&4&5&6\\ \hline
\text{incidences}&154&126&48&8\\
\delta(T)&0&1&2&3
\end{array}.                                                   \tag{5.2}
\]

Every \(T\) has internal rank two.  The lower supports are

\[
\begin{array}{c|rrrr}
R&\{0,A,B\}&\{0,A,C\}&\{0,B,C\}&\{0,A,B,C\}\\ \hline
\text{incidences}&86&86&86&78.
\end{array}                                                    \tag{5.3}
\]

The full-network deficiency histogram is

\[
\begin{array}{c|rrrrr}
\delta&1&2&3&4&5\\ \hline
\text{incidences}&120&130&66&18&2.
\end{array}                                                    \tag{5.4}
\]

There are 312 incidences in which all complexes of \(T\) are quadratic and
24 in which \(T\) contains a unary complex.  Each linkage order occurs 168
times.  Every pair occurs with exactly one retained descriptor.

## 6. Frozen set fingerprints and scope

The rows are sorted by support payload, descriptor weight, and caps.  The
repository's established JSON encoding, with dictionary keys sorted, gives

```text
d0c31db81db2400e0ead6e4a1a86b237fbf3b8bbb597340856a2756e9f6c884d
```

An independent replay of the same sorted rows using insertion-ordered JSON
keys gives

```text
2bd4025f29d20ea4af467d46704c598652c9332ac4e32df18669cb7eb75c75a0
```

The two hashes encode the same 336 rows and differ only in JSON dictionary-key
order.  Both are asserted by the regression test.

The certificate proves the support/descriptor equality in Section 4 and the
histograms in Section 5.  It does not enumerate orientations and does not
prove a stochastic estimate.  The arbitrary-orientation and arbitrary-rate
statement is Theorem 3.1, proved by the exact generator identity (2.7).

The reproducible artifacts are

```text
src/all_active_residual_levelset_336_certificate.py
tests/test_all_active_residual_levelset_336_certificate.py
```
