# Hostile review: fixed-pivot repair iteration

## Verdict

**UNCONDITIONAL PASS**, relative only to the already accepted dependencies
frozen below.

Reviewed candidate commit:

```text
5b6ac280dc0e0b03d3a985a39f27af195b8571c6
```

Reviewed note SHA-256:

```text
82baf97f95ff3f62442187fbf5a3bd043e7d790ff052ae01424c0791fac173ae
```

The candidate proves exactly its stated fixed-pivot conclusions:

1. the endpoints of a one-sided active edge occupy different components of
   the complement link of every common nonneighbor;
2. the two selected components carry the asserted checkerboard orientation;
3. the omitted repair corner is one literal state for both asymmetric
   orientations; and
4. C-146 gives the stated two-sided rank bound.

No step proves reciprocity, complete \(k=3\), or the gamma--theta conjecture.
The fixed graph is correctly labeled a \(\gamma=2\) boundary control.

## Dependency audit

The standing hypothesis

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\]

also gives \(i(G)=3\) by the parameter chain.  The following accepted inputs
were checked at their frozen hashes:

| Input | SHA-256 |
|---|---|
| C-010 maximum-independent-state forcing | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |
| C-051 independent-antineighborhood projection | `543df545dea27669645979ce61451091140d4621f1e11cfdeeaa33437f4b5620` |
| reductions, including the \(\alpha=2\) theorem | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` |
| C-064 ridge-response covariance | `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7` |
| C-108 vertex-star activity | `d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8` |
| C-143 reverse-endpoint domination | `3255bcc3d75b8538d6c8e3288f8106b553194bbac1fc3ac590d18ba6d6f81de3` |
| C-145 repair-square normal form | `fd4989145e199b68642e862d78f1af00a965f23556c3bee04f9728f33ef86b87` |
| C-146 finite-horizon star Lipschitz theorem | `3481a7dcc650a83d3994ff4bfdfb7789a520bb6a29dc57b51c1a84d549fd5b77` |

### Link lemma

For a pivot \(w\), C-051 applied to the independent singleton gives

\[
Q=G-N_G[w]=G[N_{\overline G}(w)]
\quad\text{with}\quad
\gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=2.
\]

The accepted parameter-two theorem therefore gives \(\theta(Q)=2\), and
\(\overline Q=L_w\) is bipartite.  This does not use minimum-counterexample
minimality.

If \(v\in N_{\overline G}(w)\), then \(\{w,v\}\) is independent.  Extending
it to a maximal independent set and using \(i(G)=\alpha(G)=3\) supplies
\(\{w,v,t\}\).  Hence \(vt\) is a link edge.  This proves the claimed
isolate-free property, including when \(L_w\) is disconnected.

## Shortest-path repair audit

Let a simple link path be

\[
v_0=u,v_1,\ldots,v_d=x.
\]

The length-two case is exact.  From the retained independent state
\(\{x,w,v_1\}\), an attack at the unoccupied \(u\) has only the guard at
\(x\) available: \(w\) and \(v_1\) are both \(H\)-adjacent to \(u\).
Its successor is the retained independent state \(\{u,w,v_1\}\), forcing
\(x\triangleright u\).

For \(d\ge3\), every C-145 invocation has the following valid roles:

| role | vertex |
|---|---|
| pivot | the same \(w\) |
| asymmetric endpoints | the two current path endpoints |
| source completion | the next path vertex at the source end |
| target completion | the next path vertex at the target end |

All roles required to be distinct are distinct.  The path is simple; the
two completion vertices differ for \(d\ge3\); the pivot differs from every
link vertex; and the two current endpoints cannot coincide.  Each completion
triple is independent because its non-pivot pair is a link edge.  C-145
therefore replaces the orientation by the opposite orientation on
\((v_{d-1},v_1)\), reducing the remaining path length by exactly two while
keeping the same pivot.

The terminal cases are exhaustive:

- even original length reaches length two and the forced reverse response;
- odd original length reaches length one, where an active edge would have
  to be simultaneously a \(G\)-edge and an \(H\)-edge.

The hostile abstract replay separately exercised shortest distances
\(2,3,4,5\), with counts

```text
36920, 17604, 4800, 720.
```

No collision or scope failure survived.

## Synchronized walks and checkerboard quantifiers

At step \(j\), the two endpoints remain in the two original, distinct link
components.  Consequently they are distinct and have no link edge between
them; since both are in \(N_H(w)\), they are joined in \(G\).  Thus the
active relation and the next C-145 repair are always defined.  If the current
orientation is left-to-right, C-145 makes the next orientation
right-to-left, and conversely.  This proves the parity law by ordinary finite
induction.

Repeated vertices and immediate backtracks create no collision.  Each
individual walk step still traverses a link edge, and vertices drawn from the
two distinct components never coincide.  The clean-room audit explicitly
checked 87,888 endpoint pairs of synchronized walks of lengths zero through
six, including non-simple walks.

For \(c_i\in C_i\) and \(d_i\in D_i\), any paths from the selected roots have
parity \(i\).  Their length difference is even.  The shorter path can be
padded at any incident link edge by a two-step backtrack.  The isolate-free
lemma guarantees such an edge even for a length-zero path.  The independent
audit checked 15,084 such padding pairs.  The theorem correctly claims only
the same-side pairs \(C_0\times D_0\) and \(C_1\times D_1\); it makes no claim
about cross-side pairs or unrelated link components.

## C-064 and active-edge adjacency

No active edge is mistakenly treated as a link edge.  Link edges are
\(H\)-edges and hence \(G\)-nonedges.  Pairs from distinct link components
have no \(H\)-edge and hence are \(G\)-edges, exactly as required for an
active orientation.

The displayed repair states do not form a closed independent ridge path:
the mixed states contain one of the repair-square \(G\)-edges.  Within the
star of \(w\), independent ridge motion follows a component of \(L_w\), so
it cannot cross from the component of \(u\) to the component of \(x\).
The literal two-step backtrack composes the same two ridge transpositions in
reverse order.  C-064 requires response-incidence covariance, not trivial
holonomy.  The candidate is therefore correct to record a global path
leaving the star as open rather than infer a contradiction.

## Rank audit

With

\[
S=\{u,w,a\},\quad T=\{x,w,z\},\quad O=\{u,w,z\},
\]

the identities

\[
O=T-x+u=S-a+z
\]

are literal set identities.  There are not two corners whose ranks need a
comparison.  C-143 makes \(O\) dominating, and C-108 plus either inactive
reverse orientation excludes it from the greatest family, so
\(\rho(O)\) is positive and finite.

For every maximum independent \(J\ni x\), \(ux\in E(G)\) ensures
\(u\notin J\).  C-143 and C-108 likewise make \(B_J=J-x+u\) positive finite.
C-146 applies with the fixed responder \(x\), fixed target \(u\), and
independent endpoint triples \(J,T\), yielding

\[
|\rho(B_J)-\rho(O)|\le |J-T|\le2.
\]

The candidate proof states the finiteness of \(O\) explicitly and leaves the
identical one-line justification for \(B_J\) implicit when invoking C-146.
That is a presentational compression, not a missing premise or logical gap.

## Independent exact replay

`verify_cleanroom.py` imports no candidate or campaign evaluator.  It uses
integer-bitmask states and independently recomputes:

- \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3)\);
- empty one- and two-guard kernels and a 285-state greatest triple kernel;
- all 3,420 unoccupied-attack obligations with exactly one guard moving;
- deletion waves \(2,8,10,24,26,5\);
- uniform C-108 activity on every independent endpoint row;
- the five retained repair states and the single rank-three omitted corner;
- the rank-one canonical reverse endpoint and sharp difference two;
- the \(2K_2\) link at \(w=10\); and
- 23 global dominating pairs, with the selected pair \(\{0,1\}\)
  nondominating.

The same replay reconstructs
\(G=\overline{L(K_{3,3})}\) independently and obtains

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)
\]

with all nine complement links equal to \(2K_2\).  Thus the candidate's
warning that equality does not force link connectivity is exact.

The abstract clean-room closure audit covers all 3,672 labeled isolate-free
bipartite link graphs through order six.  Its totals match the candidate's
independently written audit:

```text
66,968 oriented nonedge roots
60,044 same-component roots, all contradictory
 6,924 separated roots, all consistent
27,468 forced checkerboard pairs
```

## Scope and reproducibility

The fixed order-15 graph is not an equality graph because
\(\gamma=2<3=\alpha=\gamma^\infty\).  Its selected asymmetric pair being
nondominating does not repair this global failure.  The example establishes
only that the selected-pair condition, literal greatest-family dynamics,
local C-064 covariance, and C-146 do not force rank descent without the
remaining global \(\gamma=3\) information.

Strict replay:

```text
sh reviews/repair_square_holonomy_hostile/verify_strict.sh
```

Expected terminal line:

```text
repair-square holonomy hostile review: PASS
```

Review-task completion: **100%**.  This theorem is a rigorous narrowing of
the reciprocity lane, but it does not by itself provide a meaningful
percentage resolution of the universal conjecture.
