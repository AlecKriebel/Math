# Nonexistence in the N=4, R=2 Knights-and-Rooks Problem

**13 September 2026. Self-contained proof and independently checkable certificate.**

There is no finite placement satisfying the requested conditions. The stronger
result below permits knight-knight attacks and only assumes at least four rook
targets per knight. Bounded-board searches are not the proof.

The exact target comes from Erich Friedman's February 2007 Math Magic page,
https://erich-friedman.github.io/mathmagic/0207.html . Its Knights and Rooks table
still displayed a question mark in column N=4, row R=2 when rechecked in this
session. Initial and final searches did not locate a prior exact-target
resolution; historical priority is not claimed established.

# Boundary obstruction: nonexistence for N=4, R=2

## Stronger statement
There is no finite nonempty set of knights and finite nonempty set of rooks on
integer squares such that every knight attacks at least four rooks and every
rook sees exactly two knights and no rooks. Knight-knight attacks are allowed
in this stronger statement. Thus it implies nonexistence for the requested
case with exactly four rook targets and no knight targets.

## Proof
Assume such a placement exists. Every rook has x-coordinate between the
minimum and maximum knight x-coordinates: a rook strictly to the right of
all knights could see a knight only in its west ray, and so at most one.
The left-hand statement follows likewise. Translate a rightmost knight to
A=(0,0). Every square with x>0 is empty.

A has only four possible rook targets, so all of
U=(-2,1), V=(-1,2), W=(-1,-2), Z=(-2,-1)
are rooks. U and Z must be separated by a knight, forcing C=(-2,0).
Likewise V and W require a knight at at least one of
B+=(-1,1), B0=(-1,0), B-=(-1,-1).

B0 cannot be a knight: two of its eight knight-move destinations have x>0,
and each of the other six is immediately horizontally adjacent to one of
U,V,W,Z and so cannot be a rook. A knight at B0 would attack zero rooks.
Reflect in y=0 if necessary so that B+ is a knight.

U already sees C immediately south and B+ immediately east. Because it
sees exactly two occupied rays, its north and west rays must be completely
empty. In particular (-2,2) and (-2,3) are empty. The square (-3,2) cannot
be a rook either, since V=(-1,2) would be visible to it across empty
(-2,2).

Of the eight knight-move destinations of B+, only the following four can
therefore be rooks:
(-3,0), (-2,-1), (0,-1), (0,3).
Two other destinations have x>0, and the remaining two were excluded
above. All four listed squares must be rooks. In particular X=(0,-1)
is a rook. Z and X force a knight at their only intervening square B-.

Z now sees C immediately north and B- immediately east, so its south ray
is empty; in particular (-2,-2) and (-2,-3) are empty. Hence (-3,-2)
cannot be a rook, since it would see W=(-1,-2) across empty (-2,-2).
Also X sees A immediately north and B- immediately west, so its south
ray is empty; in particular (0,-3) is empty.

Now inspect the eight knight-move destinations of B-:
(-3,-2), (-3,0), (-2,-3), (-2,1),
(0,-3), (0,1), (1,-2), (1,0).
The last two have x>0, and (-3,-2), (-2,-3), (0,-3) have just been
excluded. At most three rook targets remain, contradicting the assumed
lower bound of four. QED.

No condition on board dimensions, piece inventory, reachability, checkerboard
color, or knight-knight attacks entered this argument. The only symmetry
operation was reflection after a proved two-case alternative.

---

# Independently checkable finite obstruction

This is a necessary local relaxation of an alleged arbitrary finite
counterexample. It is NOT the assertion that searching a 4-by-7 board
suffices to find all finite placements.

## Why every hypothetical counterexample gives an assignment

Translate a rightmost knight to (0,0). A rook strictly to the right of all
knights could see a knight on at most one ray. Thus every square with x>0
is empty. Keep the square window

D = { -3,-2,-1,0 } x { -3,-2,-1,0,1,2,3 }.

Keep its actual piece types, and discard all information outside D.
All possible rook targets of the four distinguished positions
T = { (0,0),(-1,0),(-1,1),(-1,-1) }
are either in D or in the known-empty half-plane x>0. Therefore requiring
at least four rook targets for a knight at any of these positions remains
valid without assumptions about any other knight. A local rook can have
at most two locally occupied rays, since extra pieces outside cannot
remove an already occupied ray. Every pair of aligned rooks in D requires
an intervening knight; all intervening squares lie in D because D is a
rectangle. This is necessary for no rook to see another rook.

There are deliberately NO degree constraints on other knights, NO ban on
knight-knight attacks, NO lower bound of two on the local rook ray count,
and NO restrictions on pieces outside D other than the proved empty
half-plane. Thus the model is a relaxation, and its unsatisfiability rules
out all alleged finite counterexamples.

## Complete constraint specification

For p in D use Booleans K_p, R_p, O_p:

1. not(K_p and R_p), and O_p iff (K_p or R_p).
2. For each direction d with a nonempty intersection of the open ray
   p+t*d, t>=1, with D, use V_(p,d) iff the OR of O_q on that intersection.
   Directions having no square in D contribute the constant false.
3. If R_p, at most two of its V_(p,d) are true.
4. For every two distinct aligned p,q in D:
   not R_p or not R_q or OR(K_s : s strictly between p and q).
5. K_(0,0) is true. For each p in T:
   K_p implies sum(R_q : q in D and {|dx|,|dy|}={1,2}) >=4.

Clause encoding details: equivalences in (1)-(2) are expanded by the usual
forward and reverse implications. The at-most-two condition in (3) uses
one clause for each triple of direction flags, guarded by not R_p. For a
knight with t possible targets, the at-least-four condition in (5) uses
one guarded clause for each (t-3)-element subset of target variables.
Here t is 4 at the origin and 6 at the other three distinguished points.
This is equivalent to excluding t-3 simultaneously false targets.

The generator src/local_cnf.py writes 174 variables and 699 clauses:

| Group | Clauses |
|---|---:|
| Disjoint types and occupancy equivalences | 112 |
| Occupied-ray equivalences | 342 |
| Rook occupied-ray upper bounds | 54 |
| Intervening-knight conditions for aligned rooks | 126 |
| Conditional knight lower bounds | 64 |
| Origin is a knight | 1 |

There are 84 type/occupancy variables and 90 ray variables. Every variable
name and every original clause's reason are preserved in JSON files.

## Proof certificate and trust boundary

certificates/local_relaxation.cnf is DIMACS. The JSON UNSAT certificate
identifies this exact file by SHA-256. Each unit step records a literal and
the zero-based index of an original clause that forces it. A leaf records
an original clause falsified by the current assignment. An internal node
branches on an unassigned variable and includes both branches.

src/verify_unsat.py does not import the generator, DPLL prover, attack
checkers, or Z3. It checks the file digest, every unit inference, both
branches, and each contradiction. Its accepted certificate has:

- 3 nodes: one split, two contradictory leaves;
- split variable 19, K(-1,1);
- 151 unit inferences across the tree.

This is not an external peer review or a Lean formalization. It is a
separately implemented proof-certificate check of a necessary finite
obstruction, complementing the human-readable geometric proof.

## Run

python3 src/verify_unsat.py certificates/local_relaxation.cnf certificates/local_unsat_tree.json

Expected result:

VERIFIED UNSAT {"conflicts": 2, "nodes": 3, "splits": 1, "unit_steps": 151}

---

## Validation and reproduction

Two outgoing-attack algorithms were implemented separately: pairwise coordinate
and nearest-ray tests, versus explicit knight jumps and sorted row/column
neighbors. Both accepted visually transcribed source N1R1 and N4R1 examples;
the original source-image Git blob hashes were independently reproduced.
Source N4R1 has two knights and eight rooks and is NOT a target witness.

A separately reproduced N2R3 calibration has eight knights and six rooks,
with 16 knight-to-rook and 18 rook-to-knight outgoing attacks. Thus the
checkers do not assume a reciprocal incidence-count identity.

All 20 test methods passed, including 2,000 seeded random cross-checks,
eight transformed source examples, invalid-piece and blocker tests, rejection
of five corrupted proof certificates, and satisfiable checks after removing
each of three essential constraint families. The certificate was regenerated
identically and rechecked. These are separate algorithms, not external reviews.

Run from the extracted bundle root with Python 3.9 or newer:

```sh
python3 src/run_all.py
```

This needs only the standard library. Z3 is optional and was used only for
exploratory board searches. The environment used Python 3.13.5 and Z3 4.13.3.0.
Unrestricted 8x8 and 16x16 target models reported UNSAT. Optional dihedral
symmetry 12x12 and 16x16 models also reported UNSAT. The 32x32 attempt was
interrupted, with no reported solver outcome. None of these bounded outcomes
is used to prove the theorem.

See README.md, sources/REFERENCES.md, logs/full_verification.log,
MANIFEST.sha256, and progress.json for the artifact map, sources, inspected
outputs, file integrity, and exact verification/resume command. No external
review, publication, or contact with any person is asserted.
