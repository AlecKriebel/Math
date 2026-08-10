# Three-dimensional workload-cone gluing for two linkage classes

## Setup

The complete complex universe is

\[
\mathcal C_3=\{0,A,B,C,2A,2B,2C,A+B,A+C,B+C\}.
\]

Fix a terminal Green chart and let `I` be its active coordinate set.  A
complete source-rate flag is scalarized by a rational workload `h`, strictly
positive on every coordinate in `I` and zero on bounded coordinates.  For
each linkage, the certified top-complex alternative gives an actual available
terminal or a rational workload annihilating that linkage.

An available terminal is not started from a stale formal mark.  The
finite-shell construction in `finite_shell_activation.md` waits for an
actual channel of that linkage and uses its physically enabled target.

## Three active coordinates

If all three species are active, every binary top complex contains two active
particles and gives availability.  A nonflat linkage whose top complexes are
unary gives the unary availability branch.  Therefore a shielded linkage must
be flat under the global scalar workload `h`.  If both linkages are shielded,
`h` annihilates every reaction vector and is a global nonnegative invariant,
contradicting escape.

## Two active coordinates

By permutation take active set `{A,B}`.  Up to exchanging the active species,
all projected source orders are represented by

\[
(1,1,0),\quad(2,3,0),\quad(1,2,0),\quad(1,3,0).
\]

Each complex is assigned to linkage 1, linkage 2, or neither.  For every one
of the `3^10` assignments and every workload representative, the exact atlas:

1. applies the certified top split to each nontrivial linkage;
2. solves the rational common-workload equations
   \[
   q\cdot(y-z)=0,\qquad q_A,q_B>0;
   \]
3. computes deficiency.

The direct exhaustive result is:

- 187,488 nontrivial workload assignments checked;
- 446 shielded assignments;
- 382 common-invariant assignments;
- 60 deficiency-zero assignments;
- four ordered service assignments, comprising two types up to symmetry;
- no unclassified assignment.

The two service types are

\[
\{C,2C\}\ \&\ \{0,A,2A,B+C\},
\]

and

\[
\{0,C,2C\}\ \&\ \{A,2A,B+C\}.
\]

The reduced atlas has 29 classes: 27 deficiency zero and two service classes.

## Deficiency-zero branch

For a weakly reversible deficiency-zero network, directed spanning-tree
constants give a surjective logarithmic complex-balance system.  A positive
complex-balanced point exists for every positive rate vector, and the
product-Poisson measure is summable.  Restriction to each closed class gives a
stationary probability.

## Service branch

For both exceptional systems set `W=B-C`.  The linkage containing `B+C`
preserves `W`; the other linkage changes it by `-Delta C`.  The atlas chamber
has `h_B>2h_A`, so `W` is proper on the alleged escape chart.

In a finite shell, actual target-following paths raise `C` by one relative to
the trial start or leave the chart.  The stopping time is the first net
increase, so intervening downward `C` moves do not change the endpoint
identity.  Hence `W` falls by one, the bounded coordinate is promoted, or a
lower shell/rank is reached.  The killed shell is finite and has finite mean
absorption.

## One active coordinate

The finite-phase proof is stated in `one_active_phase_theorem.md`.  The key
source-ownership fact is that a competing linkage cannot consume the bounded
cofactor of a carrier `A+D` at linear-in-`A` order without using the same
source complex.  Thus the creator target remains physically enabled until
creator service, active-particle service, lower-order phase interruption, or
structural exit.  Exact finite Green elimination includes every interruption.
A zero effective class is an affine phase invariant, not a critical
nonzero-variance class.

## Cone alternative

Combining the active-set cases gives exactly one of:

1. a rational affine invariant positive on the escape cone;
2. a physically initiated rare-terminal episode or strict finite-phase
   transition;
3. finite-mean shell descent or lower-rank promotion;
4. a deficiency-zero product-form stationary probability.

The two-active cone intersection is verified by exact Farkas/nullspace
arithmetic.  No proportionality argument special to two dimensions is used.
