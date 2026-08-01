# Milestone 1: the inherited theta transfer is JC-specific

All character tuples below lie in `Z_2 x Z_2`, represented by
`{0,1,2,3}` with bitwise XOR.  Write

\[
q_{a b c d}=\widehat p(a,b,c,d),\qquad a\oplus b\oplus c\oplus d=0,
\]

and normalize `q_0000=1`.

## Theorem

**PROVED.** Let `N` and `N'` be the inherited four-leaf theta pair, with
leaves 1 and 4 attached at the `B,E` positions in `N` and at the `E,B`
positions in `N'`.

1. Under JC, `N` and `N'` have the inherited full-dimensional regular
   stochastic overlap.
2. Under K2P, `N` and `N'` do not have a full-dimensional stochastic model
   intersection.
3. Under K3P, `N` and `N'` do not have a full-dimensional stochastic model
   intersection.
4. In each of K2P and K3P, a generic parameter point of either topology lies
   outside the Zariski closure of the other topology's model.
5. Separation is not complete over the open stochastic parameter domains:
   every inherited JC common distribution is also a K2P and K3P common
   distribution after setting the richer edge multipliers equal.

Consequently the theta pendant-transfer move `Theta` belongs to the local JC
ambiguity system, but this instance of `Theta` does not belong to the K2P or
K3P ambiguity systems.

## Model conventions

**PROVED.** For K2P, character 1 is the singleton class and characters 2,3
form the doubleton class.  An edge has Fourier multipliers `(1,s,t,t)`.  Its
four increment probabilities are

\[
\frac{1+s+2t}{4},\quad
\frac{1+s-2t}{4},\quad
\frac{1-s}{4},\quad
\frac{1-s}{4}.
\]

The open stochastic domain is the locus where all four are positive.

**PROVED.** For K3P, an edge has multipliers `(1,x,y,z)`, with increment
probabilities

\[
\frac{1+x+y+z}{4},\quad
\frac{1+x-y-z}{4},\quad
\frac{1-x+y-z}{4},\quad
\frac{1-x-y+z}{4},
\]

again restricted to strict positivity.

## Separating quartics

Define the K3P quartic

\[
\begin{aligned}
I_{\mathrm{K3P}}={}&
 (q_{3232}-q_{0202}q_{3030})
 (q_{0213}q_{1001}-q_{0011}q_{1203})\\
&+(q_{0033}q_{3201}-q_{0231}q_{3003})
 (q_{1212}-q_{0202}q_{1010}).
\end{aligned}
\]

On the K2P submodel, global interchange of characters 2 and 3 identifies the
corresponding coordinates.  The specialization is

\[
\begin{aligned}
I_{\mathrm{K2P}}={}&
 (q_{2323}-q_{0202}q_{2020})
 (q_{0213}q_{1001}-q_{0011}q_{1203})\\
&+(q_{0022}q_{2301}-q_{0231}q_{2002})
 (q_{1212}-q_{0202}q_{1010}).
\end{aligned}
\]

Multiplying every cubic term by `q_0000` makes both expressions homogeneous
quartics.  Their eight expanded terms are recorded in
`certificates/model_robustness_invariants.json`.

**EXACTLY COMPUTED.** Direct substitution of the complete displayed-tree
Fourier parameterization of `N` gives

\[
I_{\mathrm{K2P}}\circ\phi_N^{\mathrm{K2P}}=0,
\qquad
I_{\mathrm{K3P}}\circ\phi_N^{\mathrm{K3P}}=0
\]

as polynomial identities over the integers.

**EXACTLY COMPUTED.** Neither identity holds on `N'`.  At the rational target
witness used by the verifier,

\[
I_{\mathrm{K2P}}
=-
\frac{530769561108218123463328187575021}
{8358844170240000000000000000000000000000000}
\neq0,
\]

and the least of all 48 edge-increment probabilities is `7/50`.

**EXACTLY COMPUTED.** At the rational K3P target witness,

\[
I_{\mathrm{K3P}}
=-
\frac{690050294443971144456773}
{419904000000000000000000000000000}
\neq0,
\]

and the least edge-increment probability is `29/300`.  Both inheritance
probabilities equal `1/2`, so both witnesses are strictly interior stochastic
points.

## Why this excludes full-dimensional overlap

**PROVED.** Each model closure is irreducible: it is the Zariski closure of the
polynomial image of an irreducible affine parameter space.  Moreover, `N'` is
obtained from `N` by the output-coordinate transposition of leaves 1 and 4.
Hence the two closures have equal dimension under each model.

If their stochastic images shared a relatively open subset of full local
dimension, its Zariski closure would force containment of one irreducible
model closure in the other.  Equal dimensions would then force equality.
The separating quartics show that equality is false.  Thus neither K2P nor
K3P admits full-dimensional overlap for this pair.

Applying the leaf transposition to each quartic gives an invariant vanishing
on `N'` but not identically on `N`.  Therefore the parameters whose
distribution lies in the other closure form a proper algebraic exceptional
set on both sides.  This is generic two-sided separation, not merely one
noncontainment witness.

## JC replay

**EXACTLY COMPUTED.** The rebuilt engine reproduces the inherited fourteen JC
orbit coordinates exactly and verifies all 64 zero-sum Fourier-coordinate
equalities modulo

\[
43337075\beta^2-36083110\beta+7336259.
\]

The interval

\[
\frac{441}{1250}<\beta<\frac{3529}{10000}
\]

contains exactly one root and certifies all inherited target multipliers in
`(0,1)`.

## Certificate boundary

**EXACTLY COMPUTED.** `src/verify_model_robustness.py` performs the SymPy replay
from the displayed trees.

**EXACTLY COMPUTED.** `src/verify_model_robustness_stdlib.py` independently
reconstructs and expands the K2P/K3P identities using only sparse-polynomial
arithmetic over `fractions.Fraction`; it imports none of the primary symbolic
engine.

**NUMERICALLY OBSERVED.** A finite-field multigraded search found no
source/target distinction among relations of coordinate degree at most three;
the first distinction in that search occurs in degree four.  Minimality of
degree four has not yet been converted into an exact Hilbert-function
certificate and is therefore not claimed.

## Remaining scope

**UNRESOLVED.** This theorem classifies only the inherited theta transfer.  It
does not yet determine the complete K2P/K3P move systems, the full level-2
generator atlas, triangle-redirection robustness under the richer models, or
the requested global local-to-global classification.

