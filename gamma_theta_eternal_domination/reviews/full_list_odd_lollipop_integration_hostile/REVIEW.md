# Hostile review: full-list odd-lollipop integration

## Verdict

**PASS — all requested scope corrections are present, the control remains
exact, and no mathematical issue remains.**

Reviewed target SHA-256:
`31c72da963cedf7e90a095fa565c1d7690b4acacc2bb54d833be65311278e286`.

The exact nine-vertex example proves the advertised conclusion: a
single-full, augmentation-sensitive one-unit lollipop need not realize the
physical odd fan-path hypotheses.  It has \(\gamma=2\), so the note
correctly leaves every \(\gamma=3\)-sensitive assertion open.

## Revised-byte check

The revised minimality paragraph is now correct.  It explicitly restricts
the five-vertex lower bound to the subclass in which the outgoing terminal
port is the unit-support \(r\in R_x\), and separately records the
coincident-port obstruction \(q\notin R_x\).

Section 4 now propagates that distinction into an exhaustive three-way
boundary:

- separated terminal ports;
- one shared terminal port outside \(R_x\); or
- an implication walk with more than two binary clauses/components.

The revised opening now correctly calls terminal-port separation “one
explicit obstruction,” so it no longer suggests global uniqueness.

## Symbolic scope

The prerequisite odd fan-path theorem is frozen at SHA-256
`d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10`
and has a hostile `PASS` review at
`109d4d7fee3b941dea55e4b6188a5ad0b701a46167f8d03a2b4037aea917da55`.

The integration note otherwise uses it correctly.  Boolean equality of
ports as literals of one component variable does not identify their
physical vertices or manufacture complement edges.  Conversely, under the
stated physical-hub condition, the common port lies in \(R_x\), the
repeated connector is a vertex-distinct odd path inside \(W_a\), and the
fan theorem applies with \(p=x\).  The note correctly says that lollipops
with three or more binary clauses still require a separate reduction.

## Clean-room replay

`replay.py` uses integer bit masks, a fresh graph6 decoder, a literal
greatest-fixed-point computation, direct parameter and coloring searches,
and an independently constructed orientation truth table.  It does not
import or execute the target `verify.py`.

It confirms:

- labeled graph6 `HFzvvn{` and canonical graph6 `Hvzax|~`;
- exactly the nine listed complement edges;
- \((\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3)\);
- the five banned direct swaps
  \(014,015,016,127,128\);
- restricted-kernel deletion rounds \(8,1,4\);
- exactly 65 retained states and all 390 unoccupied-attack obligations;
- the exact response lists
  \[
  L(3)=012,\quad L(4)=L(5)=L(6)=01,\quad L(7)=L(8)=12;
  \]
- base assignments \((X,Y)=(0,0),(0,1)\);
- clauses
  \((\neg X\lor Y),(\neg X\lor\neg Y)\);
- augmentation unit \(X\), making the three-clause formula
  inclusion-minimally unsatisfiable;
- two semantic deletion list-colorings and zero extensions with
  \(x\) colored \(0\); and
- zero odd fan-path embeddings for every anchor color.

The sorted 65-state manifest has SHA-256
`0a699c89f61910d0e05875d3665f7c856d01bbd4a93e2f356b09a122ddf158b4`.

Artifact hashes:

- `replay.py`:
  `b944034103f98b3f57e1ffd404d00956bfdfcfeea1dfc2743dc41e5fd85a58e0`;
- `result.json`:
  `8cc75c25da867d718544feb1931d6e8726e6796a02b511e05b3a8471492e950d`.

The example refutes only the automatic local implication.  It is not an
equality graph, a counterexample to the gamma--theta conjecture, or evidence
against a future \(\gamma=3\)-specific port-identification theorem.
