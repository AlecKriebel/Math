# Exact-coloring finite rooted models: bounded certificates and crossing cores

## Status and scope

This packet does **not** solve the Erickson conjecture or the remaining finite residue. It provides fully proved finite-model bounds, a deterministic certificate checker, and elementary structural constraints that can support finite search. No remote files were changed.

The general reduction from infinite colorings to a finite graph with both vertex and edge colors is prior work: Stacey and Weidl explicitly state it on page 3 of their 1996 preprint, later published as *The existence of exactly m-coloured complete subgraphs*, JCTB 75 (1999), 1–18, DOI https://doi.org/10.1006/jctb.1998.1855. Their Example 1 is the two-core-vertex counterexample for (c,m)=(4,3). The elementary explicit bounds and structural counting arguments below are supplied with proofs; no originality claim has been checked or is being made.

Ranđelović, *Exactly Colored Complete Subgraphs of Infinite Graphs*, arXiv:2512.04233v1, https://arxiv.org/abs/2512.04233v1, gives the recent asymptotic theorem leaving a finite residue. It must not be described as a full resolution.

## 1. Rooted model and exact spectrum

A rooted model consists of a finite core V, a spoke label a(v) for every v in V, and a core-edge label b(uv) for every unordered pair. All labels lie in {0,...,c−1}, with every nonzero label used somewhere. Color 0 is the infinite tail color.

Replace the root by a countably infinite tail T: all edges within T get color 0; every edge vt with v in V and t in T gets a(v); core edges keep b. For S subset V define

P(S) = {0} union {a(v):v in S} union {b(uv):u,v in S, u != v}.

Every infinite clique in V union T meets T infinitely, and its palette is exactly P(S), where S is its intersection with V. Conversely every S is realized by S union T. Thus the exact infinite spectrum is {|P(S)|: S subset V}. The resulting coloring is surjective exactly when P(V) has size c.

## 2. Complete finite bound: at most 2(c−1) core vertices

There exists an exact c-coloring of countable K_omega with no infinite exactly m-colored clique if and only if such a rooted model exists with at most 2(c−1) core vertices and with |P(S)| != m for all S.

Proof of the nontrivial direction: apply infinite Ramsey to obtain an infinite monochromatic clique A, whose color we relabel 0. For each of the c−1 other colors choose a witness edge, and let V be the union of their endpoints. Then |V| <= 2(c−1). Delete V from A. For each v in the finite set V, refine the remaining infinite set to an infinite subset on which the color of vx is constant. The final infinite subset T remains monochromatic in color 0 and has a constant spoke color for every v. The restriction to V union T retains all c colors and remains m-avoiding. It is the required rooted model. The reverse direction follows from Section 1.

Consequently every fixed pair (c,m) has a finite exhaustive decision procedure. This is not a practical complexity bound and does not by itself settle a finite residue of unknown or enormous size. For an exhaustive negative search one must allow arbitrary spoke colors; restricting every spoke to 0 or to one common fresh color is not complete without an additional theorem.

## 3. Complete target verification: subsets of at most 2(m−1)

To verify that a supplied rooted model avoids m, it is enough to test |S| <= 2(m−1), even if its core is larger.

Proof: if P(S) has exactly m colors, select a witness for each of its m−1 nonzero colors. A spoke witness uses one vertex; an edge witness uses two. The union S' of those vertices has size at most 2(m−1). Its palette is contained in P(S) and includes every color of P(S), so P(S')=P(S).

The implemented checker validates symmetry, integer label ranges, and surjectivity before accepting any certificate. Its default target check uses this bound. A reported observed spectrum need not be the full spectrum unless full_spectrum_checked is true. --full-spectrum examines every subset.

## 4. Essential-color accounting

For a model on S, call a nonzero color essential at v if that color disappears when v is deleted. Any color is essential at at most two vertices: if it is essential at distinct u and v, every occurrence must be incident with both, so its only occurrence is the core edge uv. In particular a color essential at two vertices cannot occur on any spoke.

Let L(v) be the set of colors essential at v. Then

sum over v in S of |L(v)| <= 2(|P(S)|−1).

Also |L(v)| <= |S|, since the only slots removed with v are its spoke and its |S|−1 incident edges.

These statements are valid with repeated edge labels and arbitrary spoke labels.

## 5. Minimal crossing-core lemma

Suppose a rooted model avoids m>=3 and has at least m+1 colors. Choose S inclusion-minimal with p=|P(S)|>m, and put d=p−m+1.

Every vertex deletion leaves at most m−1 colors: minimality gives at most m and avoidance rules out m. Therefore every v in S is essential for at least d colors. If n=|S|, the accounting above gives

d <= n <= floor(2(p−1)/d).

Since d>=2 and p=m+d−1, this implies n<=m.

A sharper restriction on the upward palette jump is

binomial(d,2) <= m−2,

or equivalently

p <= m−1 + floor((1+sqrt(8m−15))/2).

Proof of the sharper inequality: if n>=d+1, then p−1 >= nd/2 >= d(d+1)/2. If n=d, each vertex must lose all n available slots as distinct essential colors. Every spoke is then nonzero and private to its vertex, and every edge has a unique nonzero color private to its two endpoints. Thus p−1=n(n+1)/2=d(d+1)/2 in this case also. Substituting p−1=m+d−2 proves the inequality.

The bound is attained for infinitely many m. Give every spoke and edge of a d-vertex core its own nonzero color. The full palette has p=1+binomial(d+1,2) colors and every proper subset has at most 1+binomial(d,2). Taking m=2+binomial(d,2) gives a minimal crossing core with p=m+d−1 and equality in binomial(d,2)<=m−2.

This is a local obstruction/cut condition, not a reduction of all prescribed palette counts to small c. A small crossing core may use p<c colors, and restoring the other c−p colors without creating m remains a genuine obstacle.

## 6. Tight maximum-size case and the diagonal

If a minimal crossing core has n=m, then p=m+1 and the core is exactly a disjoint union of rainbow cycles against background color 0:

- every spoke has color 0;
- every nonzero color appears on exactly one core edge;
- each core vertex is incident with exactly two such edges.

Proof: the inequality md <= 2(m+d−2) becomes (m−2)d<=2(m−2), so d=2 and p=m+1. Equality holds throughout the essential-color count. Every nonzero color must be essential at two vertices and every vertex essential for exactly two colors. Hence all positive colors are unique edges and form a 2-regular simple graph. All other slots are color 0. Conversely, deleting any nonempty set from such a graph deletes at least two distinct colored edges, so no induced core palette has size m.

For c=m+1, deleting redundant vertices from any rooted counterexample gives a core with at most m vertices. The rainbow m-cycle gives an explicit example attaining that bound for every m>=3. This construction is elementary known-style material, not a claim of a previously unresolved case.

## 7. Code and tests

- rooted_verify.py: dependency-free CLI certificate checker.
- check_examples.py: deterministic tests.
- known_rooted_4_3.json: the classic two-vertex example, with spectrum {1,2,4}.
- rooted_5_4.json: three-vertex example with spectrum {1,2,3,5}.
- rainbow_cycle_<c>_<m>.json: the diagonal examples for m=3,...,12.
- verified_examples.json: exhaustive subset results, witnesses, deletion-loss sets, and SHA-256 input identifiers.

Command:

python rooted_verify.py rooted_5_4.json --full-spectrum

At production time, all 12 supplied positive examples and three validation/negative checks passed. A fixed-seed comparison on 315 additional random surjective rooted models gave identical target verdicts for the bounded-subset check and the all-subsets check. These tests verify implementation behavior on those inputs; the completeness of the bound rests on the proof above.

## 8. Source-transcription caveat

The displayed final-case construction in Section 4 of Ranđelović v1 has apparent literal inconsistencies: the written Y_i pairs share edges for consecutive i, while the accompanying X_i has four vertices. The supplied text therefore should not be copied as a ready-to-run construction without checking an intended correction. This is a scoped transcription/construction warning, not a refutation of the paper's asymptotic theorem, and none of the proofs in this packet relies on that passage.
