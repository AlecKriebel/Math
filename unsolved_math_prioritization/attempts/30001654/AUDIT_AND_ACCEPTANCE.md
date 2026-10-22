# Independent audit and exact acceptance scope: C5 semisaturation

Problem 30001654 / OWR-4791-010. Audit date: 2026-10-10 UTC.

## Verdict

**Accepted as rigorous partial mathematics; not accepted as a solution of the assigned asymptotic conjecture.**

The two proof manuscripts were read completely and checked independently. No substantive mathematical error was found in either restricted lower bound, the equality classifications, the auxiliary structural lemma, or the infinite one-hub-leaf construction. The construction disproves the optional eventual exact-equality suggestion in the inspected arXiv version of Füredi–Kim, not the assigned assertion `ssat(n,C5)=11n/8+O(1)` and not the upper-bound inequality itself.

The audit does not establish novelty, global extremality of the construction, a defect in an uninspected journal version, or an exact finite semisaturation number.

## Distributed proofs and audit method

This proof-only edition preserves the audited mathematics in:

- `UNIVERSAL_CORE_THEOREM.md`: 7,576 bytes; SHA-256 `0eff5407ff1541344bb37841d16ce7d795d9e0280946767946dfbd1ed196e525`.
- `ROOTED_TWO_PATH_BOUND.md`: 5,801 bytes; SHA-256 `1b0fd52d5f6fa664c9d651f7b72801f5c8fd573d3d0c18fe40e9c9807b4dfbd2`.

The rooted equality and root-leaf corollary have the explicit order qualifications documented in [SCOPE_CLARIFICATION.md](SCOPE_CLARIFICATION.md). The underlying inequalities and proofs are unchanged; [PROVENANCE.md](PROVENANCE.md) records the editorial boundary.

The first was checked line by line for its deletion convention, local constraint, component inequality, counting identity, necessity and sufficiency of equality, and exhaustive construction verification. The second was checked for all implications of the rooted hypothesis, its component correction, outside-neighborhood edge accounting, equality, the leaf-at-root corollary, and its separate structural lemma.

## 1. Model and preliminary reductions

The model is finite simple graphs and ordinary, not induced, C5 copies. A graph is C5-semisaturated exactly when every missing edge `uv` has a simple four-edge `u`-to-`v` path in the original graph. Adding `uv` closes such a path into a new C5; conversely any newly created C5 must use the new edge and yields such a path when that edge is removed. Existing C5 copies are allowed throughout.

For the universal-core theorem, `n>=5` ensures the elementary leaf discussion has no exceptional two-vertex component:

1. A disconnected graph cannot satisfy the required path property across two components. Thus the graph is connected and has no isolated vertices.
2. Two different leaves cannot share a support: their only simple connecting path would have length two.
3. A leaf support cannot have degree two. If its neighbors were the leaf `x` and `w`, every path from `x` starts `x,v,w`, so the missing edge `xw` has no simple path of length four. Degree one would force the entire connected graph to have order two, already excluded.
4. Deleting the original leaves once therefore leaves a graph `H` with minimum degree at least two: an unsupported nonleaf loses no edge, and a supported vertex loses precisely one edge from degree at least three. No additional leaf deletion occurs. Thus the one-step operation really does give the nonempty usual 2-core here.

These points validate the deletion convention and ensure that the universal vertex `r` lies in the retained core. They do not assert that such a universal vertex always exists.

## 2. Universal-core theorem

Assume `r` is universal in `H`, let `F=H-r`, let `q=|V(F)|`, and mark the vertices of `F` supporting leaves. Write their number as `s`, and let `epsilon` record whether `r` supports one leaf. The previous reduction gives `epsilon` in `{0,1}`, `s<=q`, and `delta(F)>=1`. The counts are exactly

```
n = q+s+1+epsilon,
e(G) = q+e(F)+s+epsilon.
```

There is no double counting: the terms in the edge count are respectively the core edges incident with `r`, the edges wholly inside `F`, and all pendant edges.

### 2.1 Necessary marked-vertex condition

If `v` is marked and `x` is its leaf, the missing edge `xr` requires a simple path `x,v,a,b,r`. Neither `a` nor `b` can be a leaf, and neither can be `r` or repeat a previous vertex. Consequently `v,a,b` is a simple two-edge path wholly inside `F`. This is only a necessary condition on marked vertices, which is all the lower-bound proof needs.

### 2.2 Component estimate, including strict cases

For a component `C` of `F`, put `k=|V(C)|`, `a=|S intersect V(C)|`, and `f=e(C)`. The assertion is `8f>=3(k+a)`.

- `k=1` is impossible because `delta(F)>=1`.
- For `k=2`, neither endpoint of the single edge starts a two-edge path; hence `a=0`, and `8>6` is strict.
- For a three-vertex path, exactly the two endpoints can start two-edge paths, so `a<=2` and `16>15>=3(k+a)`.
- A three-vertex triangle has `8f=24>18>=3(k+a)`.
- For `k>=4`, connectedness and `a<=k` give `f>=k-1>=3k/4>=3(k+a)/8`. The middle comparison is equivalent to `k>=4`.

Equality in the last chain requires simultaneously `k=4`, `f=3`, and `a=4`. A four-vertex tree is either P4 or K1,3. The star center cannot start a two-edge path, so the fully marked star is excluded. A fully marked P4 attains equality. All smaller components were strict, so summation cannot hide any additional equality cases.

Summing and inserting the exact counts yields

```
8e(G)-11n
  = 8e(F)-3(q+s)-11-3epsilon
  >= -11-3epsilon.
```

The constants and signs are correct. Equality in this bound forces every component of `F` to be a fully marked P4. The nonempty core forces at least one such component, so `t>=1`.

### 2.3 Equality sufficiency and exact sizes

For `t` P4 blocks, the graph has `4t` path vertices, `4t` path leaves, one hub, and optionally its leaf. Its edges comprise `3t` path edges, `4t` hub edges, `4t` path-leaf edges, and optionally one more edge. Thus

```
n = 8t+1+epsilon,
e = 11t+epsilon.
```

For `epsilon=0` this gives equality in `8e>=11n-11`; for `epsilon=1` it gives equality in `8e>=11n-14`. Equality in the weaker uniform bound `8e>=11n-14` cannot occur when `epsilon=0`, since that case has the stronger bound with constant 11. No claim that these are the globally extremal graphs at their orders follows from the restricted theorem.

## 3. Every nonedge in the construction

Write a P4 block as `a-b-c-d`, use `u*` for the leaf supported by a path vertex `u`, and use `r*` for the optional hub leaf. All vertices in different P4 blocks are distinct, and the hub is outside every block. The following checks hold for every integer `t>=1`; they do not depend on sampling values of `t`.

1. **Path vertices in different blocks.** If `u'` and `v'` are path neighbors of `u` and `v`, the path `u,u',r,v',v` has the required four edges. Its five vertices are distinct because the two pairs lie in disjoint blocks.
2. **Nonadjacent path vertices in one block.** The only pairs are `(a,c)`, `(a,d)`, and `(b,d)`. The paths `a,b,r,d,c`, `a,b,r,c,d`, and `b,a,r,c,d` work, respectively. Their edges are path edges or hub edges and their vertices are distinct.
3. **A path leaf and the hub.** Every vertex `u` of P4 starts some simple path `u,v,w` of two edges. Then `u*,u,v,w,r` works. In particular this property holds for internal path vertices by heading toward the opposite endpoint through their other internal neighbor.
4. **A path leaf and another path vertex.** Its support is `u` and the other vertex is `v!=u`. If a path neighbor `w` of `u` can be chosen different from `v`, use `u*,u,w,r,v`. This includes all different-block pairs. If no such neighbor exists, `u` is a P4 endpoint and `v` its sole path neighbor. That `v` has a second path neighbor `z!=u`, giving `u*,u,r,z,v`. The latter path also has distinct vertices and four genuine edges.
5. **Two path leaves.** Their supports `u,v` are distinct, so `u*,u,r,v,v*` works independently of whether their supports are adjacent or in the same block.
6. **The hub leaf and a path vertex.** A simple two-edge path `v,w,z` in the block gives `r*,r,z,w,v`.
7. **The hub leaf and a path leaf.** A path neighbor `w` of `v` gives `r*,r,w,v,v*`.

These categories are exhaustive: all core pairs involving the hub are already edges; within a block, consecutive path vertices are edges; and each leaf-support pair is an edge. There is at most one hub leaf. Each listed witness has five distinct vertices, so no closed walk has been substituted for a simple path. This establishes semisaturation of both infinite families and completes the equality characterization.

## 4. Rooted two-edge-path theorem

Here the stronger local premise is that every vertex other than `r` is reachable from `r` by a simple path of exactly two edges. This is not the ordinary assertion that the graph has radius at most two: adjacent vertices must also be endpoints of such two-edge paths.

Let `N=N(r)`, let `W=V(G)-(N union {r})`, and let `a=|N|`. The premise forces `delta(G[N])>=1` because every vertex of `N` needs a common neighbor with `r`; every vertex of `W` has a neighbor in `N`; and no leaf can belong to `N`. The root itself cannot be a leaf in a nontrivial qualifying graph, since its only neighbor would not admit the required two-edge path. Thus all leaves are in `W`. Their distinct supports are in `N`.

Put `L` for the leaves, `l=|L|`, `W0=W-L`, and `w=|W0|`. Let `B` be the set of marked supports not starting a two-edge path in `G[N]`, with `b=|B|`.

### 4.1 Why every bad support has an outside witness

For `y` in `B`, the required four-edge path from its leaf to `r` leaves a simple three-edge path `y,z,t,r`. Its last internal vertex `t` is in `N`. The vertex `z` cannot be in `N`, or `y,z,t` would contradict the definition of `B`. It cannot be a leaf or `r`, either. Thus `z` lies in `W0` and has two distinct neighbors `y,t` in `N`. Witnesses for different `y` give distinct incidence edges `yz` even when they use the same vertex `z`. No unjustified injectivity among witness vertices is needed.

### 4.2 Corrected component estimate

The proposed inequality is

```
e(G[N]) >= 3(a+l)/8-b/4.
```

For a component with order `q`, `s` marked supports, and `beta` of them in `B`, its contribution on the right is `3(q+s)/8-beta/4`.

- At `q=2`, every marked vertex is bad, so `beta=s<=2`; the contribution is `3/4+s/8<=1`, the actual edge count.
- At `q=3`, the triangle easily exceeds the required value. A path with `s<=2` has right side at most `15/8<2`. If `s=3`, only its middle vertex is bad, so `beta=1` and the right side is exactly `18/8-1/4=2`.
- At `q>=4`, the uncorrected right side is at most `3q/4<=q-1<=e(C)`, and subtracting `beta/4` cannot hurt.

Thus every component satisfies the estimate, including the small components that require the correction.

### 4.3 Outside-neighborhood accounting

Partition `W0` into `U`, the vertices with exactly one neighbor in `N`, and `V`, those with at least two; write their sizes as `u,v`. Set `h=sum_{z in V}|N(z) intersect N|`. Then `w=u+v`, `h>=2v`, and the distinct witness incidences above imply `h>=b`.

A vertex of `U` must have a neighbor in `W0`: it is a nonleaf, has no edge to `r`, has exactly one edge into `N`, and cannot meet a leaf because all leaves have support in `N`. Counting incidences from `U` shows `e(G[W0])>=u/2`. Therefore

```
e(N,W0)+e(G[W0]) >= u+h+u/2 = 3u/2+h
                               >= 3(u+v)/2+b/4.
```

The final inequality is justified by `h-b/4>=3h/4>=3v/2`. This remains valid at `u=0`, `v=0`, or `b=0` and does not require the outside edges to form a matching.

All graph edges belong to exactly one of the counted categories: `a` root edges, `l` pendant edges, edges inside `N`, edges from `N` to `W0`, and edges inside `W0`. Combining the two estimates gives

```
e(G) >= a+l+3(a+l)/8-b/4+3w/2+b/4
      = 11(a+l)/8+3w/2
      = [11(n-1)+w]/8.
```

The cancellation and the coefficient of `w` are correct.

### 4.4 Equality and corollaries

Equality in the base inequality `8e>=11(n-1)` implies `w=0`. Then the outside-witness fact gives `b=0`. With this correction absent, the small components are strict and the component estimate forces fully marked P4s, exactly as in the universal-core proof. Conversely those graphs satisfy the rooted premise and attain equality. The manuscript correctly records the isolated one-vertex graph as a vacuous exception if no lower order restriction is imposed.

If there are no leaves, the direct estimates `e(G[N])>=a/2` and `e(N,W0)+e(G[W0])>=3w/2` give `e(G)>=3(n-1)/2`, as stated.

If one leaf `x` is attached to `r` and all other nonroot vertices have the rooted two-edge paths, remove `x`. A leaf cannot be internal in any path between retained vertices, so removal preserves both semisaturation and those two-edge paths. Exactly one edge and one vertex are removed, giving

```
8e(G) >= 8+11(n-2)+w = 11n-14+w.
```

The outside nonleaf count `w` is unchanged: only the degree of `r` changes, and `r` is excluded from that count. For `n>=5`, equality in the unstrengthened corollary `8e>=11n-14` is precisely the one-hub-leaf family. If this corollary is stated without an order restriction, K2 is the corresponding vacuous exception because its deletion is K1. This harmless edge case has no effect on the problem's `n>=5` domain; summaries of unrestricted equality should retain that qualification. The accepted equality statements concern the unstrengthened bounds; this audit does not claim a classification of equality in the bounds retaining the positive `w` term.

The universal-core subclass implies the applicable rooted hypothesis, with the possible single hub leaf excepted: every core neighbor of `r` has a neighbor inside `F`, and every other leaf is reached through its support. Thus the two accepted results are compatible; the rooted theorem applies beyond the universal-core setting.

## 5. Auxiliary intersecting-neighborhood lemma

Consider the supports `A` having degree two after the original leaves are removed. For distinct supports `y,z` in `A`, their two pendant leaves require a simple four-edge path. Its middle three vertices form `y,t,z`, with `t` in the retained core. Hence the two-element core neighborhoods of `y,z` intersect.

The set-family classification is valid even if some neighborhoods coincide. If all members have a common element, that is the first case. Otherwise take distinct intersecting members `{p,q}` and `{p,s}`. A member avoiding `p` must be `{q,s}`. Every other two-element member intersecting all three of these is one of those three sets. This establishes the second case.

In the common-element case, write the common vertex as `r`. If two supports `y,z` in `A` were adjacent, their core neighborhoods would be `{r,z}` and `{r,y}`. There could then be no simple three-edge path from `y` to `r`: starting with `r` ends prematurely, while starting with `z` forces the next nonleaf vertex to be `r`. That contradicts the four-edge path from `y`'s leaf to `r`. Therefore `A` is independent. Its second neighbor `f(y)` is consequently outside `A`, and the same required path has form `leaf,y,f(y),t,r`, furnishing the claimed two-edge path from `f(y)` to `r` avoiding `y`.

This structural lemma is accepted on its own terms. It does not establish that one root controls the whole graph or convert an arbitrary extremizer into the rooted class.

## 6. Infinite correction and its exact logical reach

For every `t>=1`, the now fully verified hub-leaf graph has

```
n=8t+2,
e=11t+1,
ceil(11(n-1)/8)=ceil(11t+11/8)=11t+2.
```

Consequently `ssat(8t+2,C5)<=11t+1<11t+2`. The sequence of orders is unbounded, so no eventual equality with that ceiling can hold. This is a rigorous infinite counterexample to the optional exact-equality suggestion; neither an exact determination of `ssat(8t+2,C5)` nor a matching lower bound at those orders is necessary for that conclusion.

It does not contradict the inequality `ssat(n,C5)<=ceil(11(n-1)/8)`: the new example lies below that proposed upper bound. It also cannot refute `ssat(n,C5)=11n/8+O(1)`, because its edge count is `11n/8-7/4`, differing by a constant only. No claim concerning a finite exception to the original inequality is accepted here.

## 7. Primary source and version verification

The retained Füredi–Kim PDF has 13 pages, 188,909 bytes, and SHA-256 `1f049570ebbe0fbc760c0b6eb964044869bf74184ede791c91f8db78482df4ea`. The source copy accompanying this attempt is byte-identical to the previously retained PDF. The auditor freshly rendered and visually inspected pages 1, 5, and 6 from those bytes.

- Page 1 identifies *Cycle-saturated graphs with minimum number of edges*, by Zoltán Füredi and Younjin Kim, as arXiv:1103.0067v1, dated 1 March 2011. Its later printing notation does not change the stated manuscript version.
- Page 5 gives the semisaturated definition, depicts the base P4-hub-and-leaves construction, and shows a ceiling in equation (6).
- Page 6 states the `11n/8+O(1)` conjecture and separately suggests eventual equality in (6). Those are distinct claims.
- The official [arXiv record](https://arxiv.org/abs/1103.0067), checked during this audit, lists v1 as its sole submission-history entry. The retained bytes came from the [public source PDF](https://arxiv.org/pdf/1103.0067) and identify themselves as v1. A fresh browser fetch of the version-specific PDF URL returned a cache-miss error; this audit therefore makes no claim of a fresh remote PDF byte comparison.

The recorded retrieval of the author-hosted journal-copy URL returned HTTP 404. No journal PDF bytes were obtained or visually inspected in this audit. Journal metadata and indexed snippets do not bridge that gap. The accepted attribution is therefore explicitly to the inspected arXiv version; no claim about what the journal version does or does not contain is accepted.

The source identification does not establish first-discovery priority for the construction or either restricted theorem. A bounded negative literature search is not a global novelty certificate.

## 8. Remaining gap and acceptance boundaries

The missing mathematical step is a lower bound `e(G)>=11|V(G)|/8-O(1)` for arbitrary C5-semisaturated graphs, or a justified reduction of extremal graphs into an accepted subclass with controlled additive loss. Neither manuscript proves such a reduction. The root assumptions are substantive: K3,3 is C5-semisaturated, since each same-side nonedge has a simple alternating four-edge path, but its bipartition prevents a two-edge path from any root to vertices on the opposite side. It also has no universal core vertex. Thus one cannot drop the hypotheses for all graphs.

Accepted items are exactly:

1. The universal-core inequality with its `epsilon`-dependent constant and exact equality characterization.
2. The rooted inequality `8e>=11(n-1)+w`, its base equality classification, its no-leaf strengthening, and its one-root-leaf corollary, with the stated trivial-order qualifications.
3. The separate pairwise-intersecting-neighborhood lemma and its common-root consequences.
4. The explicit infinite hub-leaf family and resulting refutation of the optional eventual exact ceiling equality in the verified arXiv statement.

Not accepted or established:

- A proof or disproof of the assigned asymptotic conjecture.
- Exact global semisaturation numbers or complete classifications of global extremizers.
- A journal-version defect claim, a novelty certificate, or a claim that no later literature resolves the general conjecture.

The appropriate mathematical status for this attempt is **partial**.
