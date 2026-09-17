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
