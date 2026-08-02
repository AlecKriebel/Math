# All-threshold elimination for the 120-vector golden family

**Checkpoint:** 2026-08-01
**Scope:** exact first-principles exhaustion; no web or literature search.

## Result

No subset of the exact 120-vector golden family produces a non-five-colorable
diameter graph at any possible nonantipodal inner-product threshold.

More precisely, let \(V\) be the 120 vectors scaled by four, so every
\(v\in V\) has squared norm 16.  For a nonantipodal inner-product value \(t\),
call \(U\subseteq V\) admissible when

\[
 \langle x,y\rangle\ge t\qquad(x,y\in U).
\]

Join \(x,y\in U\) when \(\langle x,y\rangle=t\).  For each of the seven
possible values of \(t\), this graph is five-colorable.  At five thresholds a
single five-coloring of the full 120-vertex relation graph suffices.  At the
remaining thresholds \(0\) and \(8\), complete enumeration of all maximal
admissible subsets shows that every threshold graph is in fact at most
four-chromatic.

Because

\[
 \lVert x-y\rVert^2=32-2\langle x,y\rangle,
\]

this exhausts every possible diameter value of every subset of \(V\).

The self-contained exact checker is
borsuk_dimension4/search/h4_all_thresholds_search.py.

## 1. Exact spectrum of pair products

Coordinates lie in \(\mathbb Z[\sqrt5]\).  The vectors are

\[
 \{\pm4e_i\}_{i=1}^4,\qquad
 \{(\pm2,\pm2,\pm2,\pm2)\},
\]

together with the even coordinate permutations and independent signs on the
three nonzero entries of

\[
 (0,2,1+\sqrt5,-1+\sqrt5).
\]

The seven nonantipodal products, in exact increasing order in the positive
real embedding, are

\[
 -4-4\sqrt5,\quad -8,\quad 4-4\sqrt5,\quad 0,\quad
 -4+4\sqrt5,\quad 8,\quad 4+4\sqrt5.
\]

The full oriented relation graphs have:

| threshold \(t\) | relation edges | degree | elimination |
|---:|---:|---:|---|
| \(-4-4\sqrt5\) | 720 | 12 | full graph five-colored |
| \(-8\) | 1,200 | 20 | full graph five-colored |
| \(4-4\sqrt5\) | 720 | 12 | full graph five-colored |
| \(0\) | 1,800 | 30 | constrained exhaustion |
| \(-4+4\sqrt5\) | 720 | 12 | full graph five-colored |
| \(8\) | 1,200 | 20 | constrained exhaustion |
| \(4+4\sqrt5\) | 720 | 12 | full graph five-colored |

All comparisons and counts are reconstructed directly in
\(\mathbb Z[\sqrt5]\).

## 2. Five full-relation colorings

Three explicit certificates handle five thresholds.

### 2.1 The two \(4+4\sqrt5\)-magnitude relations

On the 60 antipodal lines, the projective relation

\[
 |\langle x,y\rangle|=4+4\sqrt5
\]

has an explicit five-coloring with five classes of 12 lines.  Giving both
orientations of a line its line color produces a five-coloring of both
120-vertex oriented relation graphs:

\[
 \langle x,y\rangle=-4-4\sqrt5
 \quad\text{and}\quad
 \langle x,y\rangle=4+4\sqrt5.
\]

### 2.2 The two \(4\sqrt5-4\)-magnitude relations

The same construction, with a second explicit line coloring, applies to

\[
 |\langle x,y\rangle|=4\sqrt5-4.
\]

It simultaneously colors the full oriented graphs at

\[
 t=4-4\sqrt5
 \quad\text{and}\quad
 t=-4+4\sqrt5.
\]

### 2.3 The negative-eight relation

The projective absolute-eight graph is six-chromatic, so a line coloring
cannot work.  Instead, the graph on all 120 oriented vectors with

\[
 \langle x,y\rangle=-8
\]

has an explicit five-coloring with five classes of 24.  This is the
antipodal-two-cover certificate from the signed-subset audit.

In all five cases, any admissible subset inherits the displayed full-graph
coloring.  Lower-product constraints therefore need not be solved.

## 3. Exact constrained exhaustion at \(t=0\) and \(t=8\)

For a threshold \(t\), form the compatibility graph \(C_t\) on the 120
oriented vectors:

\[
 xy\in E(C_t)
 \quad\Longleftrightarrow\quad
 \langle x,y\rangle\ge t.
\]

Admissible subsets are exactly the cliques of \(C_t\), and every such clique
is contained in a maximal clique.  It is therefore sufficient to color the
threshold graph induced by every maximal clique.

The checker enumerates all maximal cliques using exact bit-set
Bron--Kerbosch recursion with pivoting.  For every output it independently
checks pairwise compatibility and maximality.  It then determines the exact
chromatic number of the induced threshold graph by complete DSATUR
backtracking and directly verifies the returned coloring.

### 3.1 Threshold zero

There are exactly 30,000 maximal admissible subsets:

| size | count |
|---:|---:|
| 17 | 1,200 |
| 20 | 28,800 |

Their exact threshold-graph chromatic numbers are:

| chromatic number | count |
|---:|---:|
| 3 | 9,600 |
| 4 | 20,400 |

Thus every pairwise nonnegative subset has a four-colorable zero-product
graph.

The SHA-256 fingerprint of the lexicographically sorted maximal-clique list
is

~~~text
5ea861917eac9194187f318d6a8532176c5910f5a72dd375b1583d696a025e9a
~~~

### 3.2 Threshold eight

There are exactly 5,160 maximal admissible subsets:

| size | count |
|---:|---:|
| 7 | 4,560 |
| 8 | 600 |

Their exact threshold-graph chromatic numbers are:

| chromatic number | count |
|---:|---:|
| 3 | 3,120 |
| 4 | 2,040 |

The maximal-clique-list fingerprint is

~~~text
4df9a77b669f57950df62644be0272a3f4574d4ee3ab5c45ac2f052b6406b117
~~~

Again, every admissible subset inherits a coloring from a maximal one.

## 4. Why the exhaustion is complete

Let \(U\subseteq V\) be nonempty and have at least two points.  Its minimum
pairwise product is one of the seven tabulated values, say \(t\).  Then:

1. every pair in \(U\) has product at least \(t\), so \(U\) is admissible at
   threshold \(t\);
2. its diameter pairs are exactly its product-\(t\) pairs;
3. at the five directly colored thresholds, the full relation coloring
   restricts to \(U\);
4. at \(t=0\) or \(t=8\), \(U\) lies in an enumerated maximal admissible set,
   whose threshold graph is four-colorable.

Hence the diameter graph of every subset of this exact 120-vector family is
five-colorable.  No orientation choice, deletion pattern, or alternative
diameter level inside the family can yield a Borsuk counterexample.

## 5. Reproduction

From /Users/alec/Documents/Math-borsuk4 run

~~~text
python3 borsuk_dimension4/search/h4_all_thresholds_search.py --verify
~~~

The exact audit takes only a few seconds on the project machine and prints:

~~~text
H4 golden all-threshold exact audit passed
threshold=(0,0) maximal_admissible_sets=30000 sizes={20: 28800, 17: 1200} chi={3: 9600, 4: 20400}
threshold=(8,0) maximal_admissible_sets=5160 sizes={7: 4560, 8: 600} chi={4: 2040, 3: 3120}
non_5_colorable_admissible_threshold_graphs=0
~~~

The checker is independent of optional packages and floating-point
arithmetic.  It rebuilds the coordinates, exact product table, projective and
oriented coloring certificates, compatibility graphs, maximal-clique
enumerations, and all induced colorings.
