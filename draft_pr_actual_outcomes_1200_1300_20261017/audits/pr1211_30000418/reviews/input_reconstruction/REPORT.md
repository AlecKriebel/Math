# Finite-input reconstruction

Current run: 2026-10-17 UTC. This report reconstructs a construction supplied in
the assignment. It does not claim discovery, priority, wholly blind review, or
knowledge of what was known at an earlier stage. No candidate proof or report
was read or compared. See `INFORMATION_BOUNDARY_RECEIPT.md`.

## Claims and exact outcomes

Let T have vertices a,b,c,d,e,a1,a2,b1,d1,e1,e2 and edges
ab,bc,cd,de,aa1,aa2,bb1,dd1,ee1,ee2. An L(2,1) labeling uses positive integers,
has adjacent differences at least two, and has unequal labels at distance two.
The ordinary palette number uses the common palette {1,...,k}; the arbitrary-list
number quantifies over every assignment of k-element positive-integer lists.

| Quantity | Verified outcome |
| --- | --- |
| Ordinary palette minimum of T | 5 |
| Number of labeled-vertex solutions for palette {1,...,5} | 8 |
| Solutions for the supplied A/B assignment | 0 |
| Arbitrary-list number of T | 6 |

Here A={1,2,3,4,5}; B={1,3,4,5,6}; the B vertices are a1,a2,e1,e2, and all
other vertices have A. Counts treat the named vertices as distinct; no quotient
by graph or label symmetries is taken.

These are finite mathematical conclusions, not empirical hypotheses. The success
criteria are a five-palette witness, an obstruction to palettes at most four, an
exhaustive obstruction to the stated lists, and a constructive universal
six-list upper bound. All are provided below. Computations corroborate the proofs.

## Ordinary palette: lower bound, witness, and exact count

For any degree-three vertex, its three neighbors must receive distinct labels.
Within {1,2,3,4}, at most two labels are at distance at least two from any
chosen center label. Therefore T cannot use four labels. Smaller palettes are
subsets of this palette and fail as well.

A five-palette witness, in the input vertex order, is:

| Vertex | a | b | c | d | e | a1 | a2 | b1 | d1 | e1 | e2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Label | 5 | 1 | 3 | 5 | 1 | 2 | 3 | 4 | 2 | 3 | 4 |

For the exact count, the degree-three vertices a,b,d,e must all have label 1
or 5: only those center labels leave three allowable neighbor labels in the
five-palette. Adjacent a,b are opposite; adjacent d,e are opposite; distance-two
b,d are opposite. Thus (a,b,d,e) has just the two orientations
(5,1,5,1) and (1,5,1,5). In either orientation c=3. The leaf labels at b and d
are forced. Each of the two outer pairs of leaves can be permuted in 2! ways.
The exact total is 2*(2!)*(2!)=8.

## Supplied five-element lists: complete short certificate

All three neighbors of b have A, as do all three neighbors of d. The possible
A labels at distance at least two from a center value are:

| Center value | Available A neighbor labels |
| --- | --- |
| 1 | 3,4,5 |
| 2 | 4,5 |
| 3 | 1,5 |
| 4 | 1,2 |
| 5 | 1,2,3 |

The three neighbors must be distinct, so b,d are each 1 or 5. They have distance
two, hence {b,d}={1,5}. Since c is adjacent to both, c=3.

Consider the outer endpoint x next to the center with label 1: x=a when b=1,
and x=e when d=1. Adjacency to that center and distance two from c force
x in {4,5}. Both leaves at x have B, are at distance two from the center labeled
1, and are at distance two from each other. Their individual available labels are:

| x | B labels at distance at least two from x, after excluding 1 |
| --- | --- |
| 4 | {6} |
| 5 | {3} |

The two leaves cannot take distinct labels from a singleton. Both possible
orientations of b,d are covered, proving infeasibility without relying on search.

## Source-free arbitrary-list upper bound

For any finite tree of maximum degree Delta>=1, lists of size Delta+3 suffice.
Root the tree and label in breadth-first order, processing each parent's children
in an arbitrary fixed order. For a nonroot vertex v with already labeled parent p,
exclude f(p)-1,f(p),f(p)+1. Also exclude the labels of already labeled neighbors
of p other than v. Those neighbors are exactly the earlier siblings of v and,
when p is not the root, the grandparent of v. They are the only other already
labeled vertices at distance two from v.

If p is the root, there are at most Delta-1 earlier siblings. Otherwise there is
one grandparent and at most Delta-2 earlier siblings. Thus at most Delta+2
integer values are excluded in either case. A list of Delta+3 distinct integers
contains an available value. The root has no restrictions when selected. Every
constraint is satisfied when its later endpoint is labeled. An isolated vertex
requires only one label.

T has maximum degree three, so every six-element positive-integer list assignment
is feasible. The supplied five-list obstruction gives the matching lower bound:
the arbitrary-list number is exactly six. No recalled or cited theorem is needed.

## Attaching paths at original leaves

The precise extension considered is: for each original leaf
a1,a2,b1,d1,e1,e2, append at most one outward simple path of any finite
nonnegative length. New paths are disjoint except for their specified original
attachment vertices. A zero length adds no vertex.

Each palette value t in {1,...,5} has at least two values s in the same palette
with |s-t|>=2. Starting from any valid last edge of a path, exclude its previous
label to enforce the distance-two condition. At least one choice remains for the
next label. Iterating extends the ordinary five-palette witness along every path;
different appended paths create no additional distance-one or distance-two
constraints with one another. Restriction to T proves the lower bound five.

The extended tree is still subcubic, so the universal six-list argument still
applies. Preserve the supplied A/B lists on T and assign any five-element lists
to new vertices. A solution would restrict to the impossible original instance.
Every tree in this precisely defined extension family therefore has ordinary
palette number five and arbitrary-list number six.

Attaching multiple paths at a single original leaf is a different operation and
is not silently included in this claim.

## Union-label rank compression: valid direction and limitation

Let the finite union of all lists be S={s1<...<sm}, and replace si by its rank i
in every list. For i<j, sj-si>=j-i because these are distinct integers. Therefore
a valid labeling of the rank-compressed instance lifts to a valid labeling of the
original instance. It preserves the inequalities at distance two and can only
increase adjacent differences when lifted.

The converse fails. On a single edge with singleton lists {1} and {3}, the
original labeling is valid, while the rank-compressed lists {1} and {2} are
infeasible. Consequently:

- Feasibility of a compressed instance proves feasibility of its original.
- Infeasibility of an original proves infeasibility of its compressed instance.
- Infeasibility of a compressed instance alone does not prove infeasibility of
  that original instance.

There is nevertheless a legitimate finite reduction for a universal n-vertex,
k-list claim. The union has m<=nk values. If every k-list assignment with full
union {1,...,m}, for all k<=m<=nk, is feasible, compressing and then lifting proves
the universal claim. Conversely any dense-union counterexample is already an
allowed positive-integer assignment. Equivalently, any original infeasible
instance compresses to another infeasible instance. These universal quantifiers
must not be confused with the invalid per-instance converse.

The supplied union A union B is already {1,...,6}; rank compression is the
identity here. Neither exact implementation compresses any labels.

## Reproducibility, falsification controls, and limits

Use Python 3 with the standard library only. Normal replay is:

```text
python3 -B replay.py
```

Replay checks the freeze hashes, regenerates the current mathematical output in
memory, and compares it with the frozen `results.json`. It does not rewrite a
research log or recreate historical chronology. To print a neutral current
output, run `python3 -B reconstruct.py`. To create a separate output file, use
`python3 -B reconstruct.py --output current-results.json`; existing output files
are deliberately not overwritten by that interface.

The primary exact method is deterministic minimum-domain branching with binary
constraint propagation. A separate tree dynamic program sums over child-star
label assignments; sibling labels are required to be distinct, and child labels
avoid their grandparent's label. Both return counts 0,0,0,0,8 for ordinary
palettes of sizes 1 through 5, and zero for the supplied assignment. A separate
BFS checker validates witnesses by graph distances rather than by the solver's
constraint construction.

Controls include adjacent equality and gap-one rejection, gap-two acceptance,
distance-two equality rejection, degree-three stars with palettes four and five,
80 seeded small-tree comparisons against complete Cartesian enumeration,
translation and vertex-order checks, the rank-compression counterexample, and
100 path-extension examples with random six-element lists. Restoring either
outer B leaf pair to A yields 16 solutions, so the supplied obstruction is not
an artifact of a solver that always rejects nearby inputs. All checks pass.

The algorithms are independently implemented approaches within this one
reconstruction; they are not separate human or agent verifications. No external
contact, other-agent consultation, candidate comparison, Git writes, push, or
release was performed. No novelty or historical priority determination was
attempted. There is no remaining mathematical gap for the finite claims and the
specified path-extension family. Candidate comparison and broader novelty
assessment remain outside the authorized scope.
