# Hostile review: global-holonomy static gate

## Verdict

**UNCONDITIONAL PASS.**

Commits reviewed:

- `1b6353a0` — `Refute the static holonomy strengthening`
- `6e3f9436` — `Clarify the static-gate coverage scope`

The candidate correctly refutes the newly proposed static implication, and
does not inflate that refutation into a result about the universal
\(\gamma\)–\(\theta\) conjecture.  No critical, high, or medium defect was
found.

The exact accepted conclusion is:

> The conditions that \(H\) is \(K_4\)-free, every pair of vertices of
> \(H\) has a common neighbor, and every vertex link is bipartite and
> isolate-free do **not** imply \(\chi(H)\leq3\), even when every link is a
> connected \(P_4\).  The graph \(H=\overline{C_7}\) is an order-minimal
> countermodel to this exact static implication.

This is a negative result about one proposed proof route.  It is not a
counterexample to the campaign conjecture: for \(G=C_7\),

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4),
\]

so the required equality \(\gamma=\gamma^\infty\) fails.

## 1. Independence of this review

`verify_independent.py` is a clean-room standard-library checker.  It imports
neither candidate code nor either campaign eternal-domination evaluator.  It
reconstructs the graph from the cyclic definition, parses and emits graph6
records independently, enumerates all relevant vertex subsets, builds the
one-guard configuration game directly, reconstructs the clique complex, and
enumerates the finite universes used for minimality.

The only external programs used are pinned nauty 2.9.3 binaries:

- `labelg`, solely to check the advertised tool-relative canonical graph6
  strings; and
- `geng`, for an ancillary unlabeled cross-check through order nine.

The decisive order-at-most-six coverage does not rely on `geng`: it iterates
all \(2^{\binom n2}\) labeled adjacency masks.

## 2. Graph convention and graph6 audit

The witness JSON reconstructs exactly the cyclic graph

\[
E(G)=\{\{i,i+1\}:i\in\mathbb Z/7\mathbb Z\}
\]

and its simple complement.  The two edge sets are disjoint and partition all
21 unordered vertex pairs.

The clean-room graph6 encoder and decoder give:

| graph | labeled graph6 | pinned-`labelg` canonical graph6 |
|---|---|---|
| \(G=C_7\) | `FhCKG` | `FoDPO` |
| \(H=\overline{C_7}\) | `FUzro` | `F}hXw` |

After decoding each canonical record, a brute-force search over all \(7!\)
vertex permutations verifies isomorphism to the declared graph.  This also
resolves the harmless fact that other labeled graph6 records, such as the
campaign's previously used labeling of \(C_7\), encode the same isomorphism
type.

## 3. Static countermodel

All advertised static properties replay exactly.

- A clique of \(H\) is an independent set of \(C_7\), so
  \(\omega(H)=3\) and \(H\) is \(K_4\)-free.
- All 21 unordered pairs have a nonempty common-neighbor intersection in
  \(H\).
- At every root \(w\), the induced link on \(N_H(w)\) has four vertices,
  degree sequence \(1,1,2,2\), is connected, and is bipartite.  Thus it is a
  \(P_4\), in particular isolate-free.
- A color class of \(H\) is a clique of \(C_7\) and has size at most two, so
  three colors cover at most six vertices.  The four parts
  \(\{0,1\},\{2,3\},\{4,5\},\{6\}\) give a four-coloring.  Hence
  \(\chi(H)=4\).

Therefore the proposed static implication is genuinely false, including its
connected-link strengthening.

## 4. One-guard model and exact parameters

The independent game kernel uses precisely the model in the campaign:

1. attacks range only over vertices absent from the current configuration;
2. one occupied guard is removed;
3. that guard must be adjacent in \(G\) to the attacked vertex;
4. the attacked vertex is inserted; and
5. the successor must remain in the active family of dominating
   configurations.

Direct subset enumeration gives

\[
\gamma(G)=i(G)=\alpha(G)=3,\qquad \theta(G)=4.
\]

The synchronous greatest-fixed-point calculation finds 14 dominating
triples, seven deleted in round one and seven in round two, leaving an empty
three-guard kernel.  The four-guard kernel has 28 states.  Independently, the
eight states obtained by placing one guard in each member of

\[
\{0,1\},\quad\{2,3\},\quad\{4,5\},\quad\{6\}
\]

are checked obligation by obligation and form an eternal four-family.  Thus
\(\gamma^\infty(G)=4\).

The C-020 attack tree is also complete:

- from \(S=\{0,2,4\}\), attack \(1\);
- the only adjacent guards are \(0,2\);
- \(0\to1\) leaves \(6\) undominated;
- \(2\to1\) gives the dominating state \(\{0,1,4\}\);
- attack \(3\), for which the only adjacent guard is \(4\);
- \(4\to3\) leaves \(5\) undominated.

The standard forced-independent-state argument is sound: successively attack
unoccupied members of \(S\).  Because \(S\) is independent, a guard already
on \(S\) cannot move to another member of \(S\), so the number of occupied
members strictly increases until the state is \(S\).  Consequently the
two-ply tree excludes every eternal three-family, not merely one selected
family.

## 5. Clique-complex topology

The maximal cliques of \(H\) are exactly

\[
F_i=\{i,i+2,i+4\}\qquad(i\in\mathbb Z/7\mathbb Z).
\]

Every maximal clique has size three, so the flag clique complex is pure
two-dimensional.  Independent reconstruction gives

\[
f=(7,14,7),\qquad \chi=7-14+7=0.
\]

Exactly seven edges have one incident triangle and seven have two.  The
boundary edges form the connected cycle

\[
0-4-1-5-2-6-3-0.
\]

Every vertex link is a path, so this is a connected compact triangulated
surface with one boundary component.  A separate triangle-orientation
constraint calculation is inconsistent, confirming nonorientability.  By
the classification of compact connected surfaces, one boundary component,
Euler characteristic zero, and nonorientability identify the surface as a
Möbius band.  The candidate's flagness, purity, boundary, and Möbius-band
claims are therefore all correct.

The candidate also correctly says that this is not a closed
pseudomanifold: the links are paths, not cycles.

## 6. Exact order-minimality

The clean-room verifier iterates every labeled graph on orders \(1\) through
\(6\):

\[
1+2+8+64+1024+32768=33867.
\]

For each graph it directly checks \(K_4\)-freeness, the common-neighbor
condition, link bipartiteness and isolate-freeness, and exact
three-colorability.  No non-three-colorable static graph occurs.

The candidate's triangle-normalized static-base counts reproduce exactly:

\[
0,\ 0,\ 1,\ 6,\ 100,\ 2055.
\]

For clarity, without triangle normalization the order-one count is \(1\),
because the empty link is vacuously isolate-free; the corresponding direct
counts are

\[
1,\ 0,\ 1,\ 6,\ 100,\ 2055.
\]

This is only a convention at order one.  It has no effect on the
countermodel search, since an order-one graph is three-colorable and every
graph satisfying the pair condition at order at least three contains a
triangle.  Commit `6e3f9436` correctly labels the displayed candidate counts
as triangle-normalized.

Together with \(\overline{C_7}\), this proves that order seven is minimal for
the **exact stated static implication**.  It does not prove a new lower bound
for a counterexample to the \(\gamma\)–\(\theta\) conjecture.

As an ancillary check, pinned `geng` supplies exactly

\[
1,2,4,11,34,156,1044,12346,274668
\]

unlabeled graphs at orders one through nine.  At order seven there are
exactly three static countermodel types, with 12, 13, and 14 edges.  The
14-edge type is \(\overline{C_7}\).  Exactly its seven boundary-edge
deletions survive the static gate, and they are all isomorphic to the same
13-edge type.  The review also independently confirms the candidate's
explicitly non-theorem-grade observation that no closed-link countermodel
appears through order nine.

## 7. SAT/CEGAR scope audit

The discovery encoding is semantically sound.

- Fixing a triangle is safe.  The every-pair common-neighbor condition first
  produces an edge and then extends the endpoints of an edge to a triangle.
- The six-negative-literal clause on each four-set is exactly \(K_4\)
  exclusion.
- For each pair, at least one witness variable is selected, and a selected
  witness implies both required incident edges.  Existentially this is
  exactly the common-neighbor condition.
- The guarded link-color clauses activate precisely on a triangle
  \(wuv\), which is an edge \(uv\) in the link of \(w\), and force the two
  link colors to differ.
- Separate isolate-free clauses are unnecessary: if \(u\in N_H(w)\), a
  common neighbor of the pair \(u,w\) is adjacent to \(u\) inside the link
  of \(w\).
- For a proper three-coloring \(c\), the cut requiring some same-colored
  pair to become an edge excludes exactly graphs for which \(c\) remains
  proper.  It cannot exclude a graph that genuinely needs four colors.

The candidate's 64-graph order-four truth-table audit replays successfully.
It imports the candidate formula builder, so it is a polarity/conditional
audit rather than a clean-room large-order coverage proof; the candidate
states this limitation accurately.

The order-six CaDiCaL `UNSAT` run has no proof log and remains
**OBSERVED as a solver run**.  The mathematical absence at order six is
independently proved by the labeled enumeration.  The order-seven through
order-ten discovery witnesses each pass the clean-room direct predicate and
coloring check, but no large-order absence claim relies on those exploratory
runs.

## 8. Prior-art and scope audit

The no-novelty framing is accurate.

- Accepted C-020 already records the same \(C_7\) two-attack failure.
- Accepted C-064 already records the seven-facet loop and nontrivial
  ridge-transport holonomy.

The candidate adds the audit relevant to the newly proposed strengthening:
the same accepted control also has the every-pair common-neighbor property,
connected \(P_4\) links, and the flag Möbius-band realization.  It does not
claim that the basic \(C_7\) control is new.

Finally, the candidate explicitly rejects the invalid hereditary inference.
An induced copy of this static complex inside a larger graph need not retain
the same attack tree: outside vertices can dominate failed successors or
provide new legal responses.  Any later use must preserve the full dynamic
quantifiers.

## 9. Final assessment

The proposed purely static holonomy route is exhausted.  The useful research
conclusion is the one stated by the candidate: a successful gluing theorem
must use actual eternal-family survival, not only physical complement links
or their local topology.

Campaign completion estimate for this review subtask: **100%**.  This is a
review-completion estimate, not a probability that the universal conjecture
is true.
