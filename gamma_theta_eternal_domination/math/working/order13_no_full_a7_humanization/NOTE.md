# Three-way anchored closure in the order-13 residual core

## Status

Date: 2026-07-28 (PDT)

This lane did **not** produce a universal proof of the gamma--theta
conjecture or a counterexample.

It produced two concrete outcomes:

1. a proof-log-backed **certified finite strengthening** of the structured
   order-13 residual exclusion: full eternal closure is unnecessary; closure
   through states retaining at least one original anchor already gives
   UNSAT; and
2. three directly checked SAT controls showing that any two of the three
   single-anchor depth-two slices are insufficient.

The second outcome sharply refutes the tempting proof strategy that two
frozen-anchor lanes, considered without the third, should already force a
clique partition.  The surviving obstruction is genuinely three-way at this
finite frontier.

An independent generator and hostile coverage audit have reconstructed the
radius reduction and accepted the UNSAT proof.  The SAT controls are explicit
finite countermodels to the stated partial-closure generalization, not
counterexamples to the gamma--theta conjecture.

## 1. Anchored closure radius

Let \(S=\{0,1,2\}\) be the distinguished independent family state.  For a
triple \(D\), its Johnson distance from \(S\) is

\[
  d_S(D)=3-|D\cap S|.
\]

Define radius-\(r\) anchored closure to mean that the ordinary literal
one-guard response condition is imposed on each selected state \(D\) with
\(d_S(D)\le r\), for every unoccupied attack.  No closure is imposed outside
that ball.

For triples, radius two is exactly closure on selected states retaining at
least one member of \(S\).  A response from such a state may enter a
completely disjoint state, but no later response from that disjoint state is
required.

The tested formulas retain every other hypothesis of the structured residual
instance:

- the static equality conditions at parameter three;
- \(\theta(G)>3\);
- the exact no-full response condition at \(S\);
- two physical pure-signature response ports and their mates;
- the residual signature ordering; and
- at most three neutral outside vertices.

## 2. Certified finite strengthening

The radius-two formula is UNSAT:

\[
 \boxed{\text{closure on }D\cap S\ne\varnothing\text{ already excludes the
 structured order-13 residual branch}.}
\]

Its exact census and hashes are:

```text
variables:  9,802
clauses:   76,214
CNF SHA-256:
8bd4ae50e2ac06deb6560c4ff482eb19d7b64a4769029284da4660ccbefd1b55

addition-only DRAT lines: 168,880
addition-only DRAT bytes: 9,367,094
addition-only DRAT SHA-256:
f5fcbe26885ab229636d511d2b1ee47203478002fb22ce34407f1182d1c1eeea
```

Pinned DRAT-trim replay with ASCII parsing, forward checking,
warning-fatal mode, and RUP-only additions returned

```text
s VERIFIED
0 RAT lemmas
```

The first backward core has 12,251 input clauses.  It retains 1,488 closure
reply obligations on 158 of the 166 triples meeting \(S\), and no obligation
from a triple disjoint from \(S\).  This is substantially smaller than the
full-closure core, but it is still distributed across essentially the whole
anchored radius-two layer.  It did not collapse to a short human attack tree.

This finite strengthening is useful conceptually: any proof extracted from
this branch can stop once the third original guard has moved.  Eternal play
after all three original guards have been replaced is irrelevant to this
order-13 contradiction.

## 3. Radius one is insufficient

Radius one retains closure only at \(S\) and its direct one-swap states.  The
formula is SAT.  The retained model has graph6

```text
LBZ]VZuZtyvasr
```

and exact graph parameters

\[
  (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4).
\]

Its selected family has 165 dominating triples and satisfies every imposed
radius-one response.  It fails full closure first on radius-two states.  Thus
the second replacement layer is genuinely necessary; a proof using only the
reference state and direct responses cannot establish the residual
contradiction.

## 4. Any two depth-two anchor slices are insufficient

For \(R\subset S\), impose radius-two closure only on selected states
\(D\) with \(D\cap R\ne\varnothing\).  When \(|R|=2\), this retains:

- closure at \(S\);
- closure at every direct one-swap state; and
- two of the three single-anchor depth-two slices.

All three choices of \(R\) are SAT.  A standalone checker ignores every SAT
move variable, reconstructs \(G\) and the selected family, computes the exact
graph parameters, and directly replays each required one-guard response.

```text
retained R={0,1}: graph6 LBZ]ditl\jtoq}
retained R={0,2}: graph6 LBZMbqjntjJp`}
retained R={1,2}: graph6 LBZ]b|j\rpufme
```

Each graph satisfies

\[
  (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4).
\]

The selected partial families and direct replay counts are:

| retained slices | family states | required attacks checked | full-closure failures | failures in omitted single-anchor slice |
|---|---:|---:|---:|---:|
| \(0,1\) | 142 | 640 | 47 | 13 |
| \(0,2\) | 160 | 600 | 22 | 5 |
| \(1,2\) | 153 | 570 | 30 | 6 |

Every full-closure failure lies outside the retained slices, and each model
has at least one failure in the omitted single-anchor slice rather than only
after all anchors disappear.

Therefore the following proposed strengthening is **REFUTED**:

> In the structured order-13 residual branch, closure through any two
> original-anchor slices suffices to force a 3-coloring of the complement.

It does not.  All three single-anchor depth-two slices must interact.

The direct checker and result hashes are:

```text
verify_two_slice_controls.py
d36afdd6ed1698aa3043c1d441877b9caf78feccf8659d5512ad9fdabed666b9

two-slice-controls-result.json
7b1f8a567b9bb17d6084abdec1a1255555dd17db9152aacba172b742fd57c74b
```

## 5. Semantically redundant blocks

A separate exact reduction removes 3,589 clauses from the full structured
formula without changing its mathematical content:

- 715 explicit \(H\)-\(K_4\) clauses;
- 2,860 selected-state domination clauses;
- the family-nonempty clause;
- four port-to-anchor \(G\)-edge units already forced by positive responses;
- two negative port-list units already forced by their nonzero signatures;
  and
- seven no-full clauses for vertices already known to be nonneutral.

The reasons are human and parameter-independent:

1. literal closure at a selected state forces that state to dominate;
2. an independent eternal triple-state and the standard
   \(\alpha\le\gamma^\infty\) inequality force \(\alpha=3\);
3. a positive direct response forces the corresponding move edge in \(G\);
4. if \(\sigma(x)\ne\varnothing\), then
   \(L(x)\subseteq S-\sigma(x)\), so \(x\) cannot have a full list; and
5. after sorting the residual signatures and requiring label 10 to be
   nonzero, only labels 7, 8, and 9 can be neutral.

The resulting 81,025-clause formula remains UNSAT.  This cleans the
mathematical dependency graph, but it is not itself a new graph theorem.

## 6. Sharp hypothesis controls

Three additional SAT controls separate the main ingredients:

| removed ingredient | graph6 | exact parameters |
|---|---|---|
| \(\theta>3\) | `LBZMbpzZR\|ukis` | \((3,3,3,3,3)\) |
| \(\gamma\ge3\) | `LBZ]VuzjLmy}ve` | \((2,2,3,3,4)\) |
| eternal closure | ``LBZE`crKxfe^K~`` | \((3,3,3,4,4)\) |

Thus the contradiction is not static, not a consequence of closure without
the domination lower bound, and not a consequence of equality without the
clique-cover gap.

## 7. Proof-research conclusion

No short human lemma was extracted from the DRAT core.  The useful conclusion
is narrower and more directional:

- closure after all three original guards have left is unnecessary;
- closure at the first replacement layer is insufficient;
- the second replacement layer is necessary; and
- all three original-anchor slices at that layer are jointly necessary.

This supports a three-way gluing or holonomy proof target.  It also warns
against spending further effort on arguments confined to one or two frozen
projections: explicit controls satisfy all such tested partial obligations
while retaining \(\theta=4\).
