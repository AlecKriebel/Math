# Hostile review: coinductive greatest-family reciprocity normal form

## Verdict

**PASS**

The mathematical claims in the revised candidate
`math/working/coinductive_reciprocity/` are correct at their stated scope.
The candidate proves a conditional normal form and partial rank descent for
a hypothetical one-sided active exchange when

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3.
\]

It does **not** prove greatest-family reciprocity, the complete \(k=3\)
case, or the gamma--theta conjecture.  I found no hidden appeal to any of
those open statements.

The sole correction required by the first hostile pass has been made:

```diff
-That proper family contains all five states in (6.1) and omits \(O\).
+That proper family contains all five states in (6.4) and omits \(O\).
```

The revised candidate also incorporates the previously reviewed reciprocal
third-base consequence as Lemma 5.5.  Its exact formulas
(5.27)--(5.36) pass the final binding below.

## Revised source and accepted dependencies

The finally reviewed candidate bytes have these hashes:

| Artifact | SHA-256 |
|---|---|
| `NOTE.md` | `fd4989145e199b68642e862d78f1af00a965f23556c3bee04f9728f33ef86b87` |
| `RESEARCH_LOG.md` | `f21e4eced949dfd71bb21eef929e62504b0ba80168820abe9b096d6a23579480` |
| `MANIFEST.json` | `9f3c4c1a102ecc0a9af38b4e3be59423fa1e44b38ab21c4a2786bbe5404c4251` |

I read and reconstructed the relevant accepted dependencies rather than
accepting their names as black boxes:

| Dependency | Exact use | SHA-256 |
|---|---|---|
| C-010, forced maximum-independent states | every independent triple lies in every eternal triple-family | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |
| C-108, vertex-star propagation | activity of a fixed responder and target is uniform across retained independent triples containing that responder | `d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8` |
| C-134--C-138 boundary | greatestness alone is insufficient without \(\gamma=\alpha\); reciprocity and equal-rank induction remain open; no one-sided order-nine equality instance exists | principal C-134 note `4e195ff3ba8375a0319efd7a8362c5c09bc7fe9ec1970460d57721911ee1ef9f` |
| C-143, reverse endpoint domination | independently confirms and generalizes the candidate's rank-zero arguments, but supplies no survival or rank transport | `3255bcc3d75b8538d6c8e3288f8106b553194bbac1fc3ac590d18ba6d6f81de3` |

C-064 is listed as a candidate dependency, but none of the displayed
proofs in `NOTE.md` needs its full cross-state path theorem.  The candidate
uses C-108 directly for the only nontrivial response transport.

## Model audit

Every proof was checked in the standard one-guard-moves model:

- attacks are only at unoccupied vertices;
- one guard moves along one edge;
- a retained successor is a dominating triple;
- the greatest family is the literal greatest fixed point obtained from
  all dominating triples by synchronous deletion.

No proof uses all-guards movement, occupied-vertex attacks, complement
adjacency in place of graph adjacency, or a merely static secure-set
condition.

Under the candidate hypothesis, the parameter chain gives
\(i(G)=3\).  Since also \(\alpha(G)=3\), every maximal independent set has
size three.  This justifies every independent-pair completion used in the
note.

## Proof reconstruction

### Active relation

If \(p\triangleright q\), a retained independent triple containing \(p\)
has retained successor after replacing \(p\) by \(q\).  The edge \(pq\)
is forced: the other two guards are nonadjacent to \(p\), so the successor
could not dominate the vacated vertex \(p\) unless \(q\) met \(p\).
C-108 makes this relation independent of the selected maximum independent
triple containing \(p\).

This is a relation on **independent endpoint states**, not on arbitrary
states of the greatest kernel.  The candidate maintains that distinction.

### Lemmas 2.1 and 2.2

For a one-sided edge

\[
u\triangleright x,\qquad x\not\triangleright u,
\]

put \(W=N_{\overline G}(u)\cap N_{\overline G}(x)\).

- \(W\ne\varnothing\) because \(\gamma(G)=3\), so \(\{u,x\}\) does not
  dominate.
- If distinct \(w,w'\in W\) were nonadjacent in \(G\), the independent
  triple \(\{x,w,w'\}\) could answer the attack at \(u\) only by moving
  \(x\), reaching the retained independent triple \(\{u,w,w'\}\).  This
  contradicts \(x\not\triangleright u\).  Hence \(W\) is a \(G\)-clique.
- Extending \(\{x,w\}\) to \(\{x,w,z\}\), the attack at \(u\) cannot move
  \(w\), and moving \(x\) would contradict inactivity.  It therefore moves
  \(z\), retaining \(\{u,x,w\}\).
- From \(\{u,x,w\}\), an attack at another \(w'\in W\) has unique responder
  \(w\), because \(u\) and \(x\) both miss \(w'\).

All attacks here are unoccupied, and every asserted unique mover is
unique by graph adjacency before family membership is considered.

### Theorem 2.3 and Lemma 5.1

The general \(k=3\) reverse-domination proof is sound.  If
\(T=\{x,p,q\}\) is independent and \(T-x+u\) misses \(r\), extend
\(\{u,r\}\) to \(\{u,r,a\}\).  Activity and C-108 retain
\(\{x,r,a\}\).  The cases \(a=p\) or \(a=q\) would make that retained
state non-dominating.  Otherwise its domination of \(p,q\) forces
\(ap,aq\in E(G)\).  Attacking either endpoint uniquely moves \(a\) and
exposes the other, contradicting eternal closure.

Thus every complementary reverse endpoint dominates.  C-143 now proves
the same statement for every \(k\), but it adds only domination.  It does
not imply:

- that a reverse endpoint belongs to the greatest family;
- equality or monotonicity of complementary deletion ranks;
- that a minimum-rank reverse endpoint has a common-nonneighbor pivot;
- that an active replacement acts on arbitrary greatest-family states.

The candidate makes none of those invalid inferences.

Lemma 5.1 is a correct shorter proof for the shared-pivot corner.  It is
also now redundant with C-143, but not incorrect.

### Theorem 3.1 and Corollary 3.2

For independent completions

\[
S=\{u,w,a\},\qquad T=\{x,w,z\},
\]

the third vertices \(a,z\) must be distinct; otherwise both exchanged
independent endpoint states are retained and the original orientation is
reciprocal.

The asserted edges are forced in this order:

1. \(ux\) by activity;
2. \(xa\) and \(uz\) by the completion argument;
3. \(az\) because retained \(D=\{x,w,a\}\) must dominate \(z\).

Independence of \(S,T\) supplies the missing diagonals \(ua,xz\).
Therefore \(u,x,a,z\) induce the displayed \(G\)-cycle.  The attacks
at \(u\) from \(T\) and at \(z\) from \(S\) each have one omitted and one
retained candidate response, forcing \(R\) and \(P\), respectively.

Reading the four pairs of exchanged states gives exactly two opposite
one-sided active edges and two reciprocal edges.  Direct enumeration of
the three guards at each of the four named attacks gives exactly the four
response lists in Corollary 3.2.

### Theorem 4.1

Any failed complementary exchange gives \(u\triangleright x\) and
\(x\not\triangleright u\) by C-108.  The non-dominating pair
\(\{u,x\}\) supplies \(w\in W\), and well-coveredness supplies both
independent completions.  If their third vertices coincided, both
orientations would be retained.  Thus every failure has the claimed
shared-pivot repair square, including when the originally presented
endpoint triples were disjoint.

### Lemma 5.2

Because the omitted corner \(O\) dominates but is not in the greatest
fixed point, some unoccupied attack has no successor in the greatest
family.  Otherwise adjoining \(O\) to the greatest family would produce
a larger eternal family.  The attacks at the two displayed internal
vertices already have retained responses, so a blocker \(r\) lies outside
the five named vertices.

At \(r\), the \(a\)-response from \(S\) and the \(x\)-response from \(T\)
are exactly two forbidden successors of \(O\).  C-108 makes the shared
guard \(w\) active from \(S\) if and only if it is active from \(T\).
If it is inactive, eternal closure leaves only \(u\) on the \(S\)-side
and only \(z\) on the \(T\)-side.  This proves the stated exhaustive
dichotomy.

In the shared-pivot-active branch, there is one additional correct local
fact:

\[
\{u,a,r\},\{x,z,r\}\in\mathcal K,
\]

and attacking \(w\) from either state uniquely moves \(r\) back to \(w\),
returning \(S\) or \(T\).  This does **not** prove
\(r\triangleright w\) in the candidate's C-108 sense, because the two
intermediate states need not be independent.  It is retained-transition
reversibility, not active-edge reciprocity.

### Lemma 5.3

The minimum is correctly taken over the global class of all omitted
shared-pivot corners arising from all one-sided active orientations.
Every such corner has positive finite rank by Theorem 2.3/C-143.

If \(r\) deletes a minimum-rank corner \(O\) at round \(h\), every
one-edge successor at that attack has rank below \(h\).  The three
adjacency caps are justified by the following exact mappings:

| Assumed move | Extra nonedges | Independent endpoint | One-sided orientation | Lower-rank omitted corner |
|---|---|---|---|---|
| \(u\to r\) | \(wr,ar\notin E\) | \(\{a,w,r\}\) | \(z\triangleright a,\ a\not\triangleright z\) | \(\{r,w,z\}=O-u+r\) |
| \(w\to r\) | \(ur,xr,zr\notin E\) | \(\{x,z,r\}\) | \(u\triangleright x,\ x\not\triangleright u\) | \(\{u,z,r\}=O-w+r\) |
| \(z\to r\) | \(xr,wr\notin E\) | \(\{x,w,r\}\) | \(u\triangleright x,\ x\not\triangleright u\) | \(\{u,w,r\}=O-z+r\) |

Each displayed endpoint is independent under exactly the listed
nonedges plus the repair-square nonedges.  C-108 makes its reverse state
omitted, Theorem 4.1 puts it back in the globally minimized class, and
C-143 makes it dominating.  Hence its rank is positive and strictly
below \(h\), a contradiction.  No equality of paired finite ranks is
used.

The middle cap correctly retains the alternative \(ur\in E(G)\).
The order-nine inactive-only control shows that dropping such alternatives
by transporting an arbitrary rank minimum to a common pivot is unjustified.

### Lemma 5.4

In the paired-singleton branch with \(wr\notin E(G)\), the singleton
responses force \(ur,zr\in E(G)\), and Lemma 5.3 then forces
\(ar,xr\in E(G)\).  Any maximum-independent completion
\(U=\{r,w,c\}\) therefore avoids both \(x\) and \(a\).

At the attack \(x\), \(w\) cannot move.  If \(r\) moved, then
\(r\triangleright x\); Lemma 5.2 and C-108 give
\(x\not\triangleright r\), so \(\{r,w,z\}=O-u+r\) would be a lower-rank
omitted corner.  This contradicts minimality, forcing \(c\to x\).
The argument at \(a\) is symmetric and forces \(c\to a\).

This is propagation from the minimum-rank hypothesis.  It does not claim
that either new response survives after replacing the independent
endpoint by an arbitrary kernel state.

### Lemma 5.5: final binding of formulas (5.27)--(5.36)

The revised candidate now includes the previously reviewed third-base
consequence.  Every displayed formula is correctly bound to the hypotheses
of Lemma 5.4.

Retain the paired-singleton, \(wr\notin E(G)\) setup.  Write

\[
A_r=\{r,w,z\},\qquad C_r=\{u,w,r\}.
\]

These are exactly the identities in (5.27).  The edges \(ur,zr\) from
(5.32) make them the two legal successors of the deleting attack at \(r\)
from \(O\); the definition of that attack excludes both from
\(\mathcal K\), proving (5.28).  Equation (5.29) quantifies over every
maximum independent completion \(U=\{r,w,c\}\), exactly as Lemma 5.4
does.

Attack \(u\) from \(U\).  The guard \(w\) misses \(u\), while a move
\(c\to u\) would land in \(C_r\notin\mathcal K\).  Since \(ru\in E(G)\),
closure forces

\[
r\to u,\qquad \{u,w,c\}\in\mathcal K.
\]

This is (5.33).  Likewise, the attack at \(z\) forces

\[
r\to z,\qquad \{z,w,c\}\in\mathcal K,
\]

because \(wz\notin E(G)\) and the \(c\)-successor is
\(A_r\notin\mathcal K\).  This is (5.34), and the two retained successors
are exactly (5.30).  The paired-singleton list identities give the two
retained states in (5.35).

The eight active directions asserted in (5.31) have the following literal
maximum-independent witnesses:

| Active direction | Maximum independent base | Retained successor |
|---|---|---|
| \(r\triangleright u\) | \(U=\{r,w,c\}\) | \(U-r+u=\{u,w,c\}\), by (5.33) |
| \(u\triangleright r\) | \(S=\{u,w,a\}\) | \(S-u+r=\{r,w,a\}\), by (5.35) |
| \(r\triangleright z\) | \(U=\{r,w,c\}\) | \(U-r+z=\{z,w,c\}\), by (5.34) |
| \(z\triangleright r\) | \(T=\{x,w,z\}\) | \(T-z+r=\{r,w,x\}\), by (5.35) |
| \(c\triangleright a\) | \(U=\{r,w,c\}\) | \(U-c+a=\{r,w,a\}\), by Lemma 5.4 |
| \(a\triangleright c\) | \(S=\{u,w,a\}\) | \(S-a+c=\{u,w,c\}\), by (5.36) |
| \(c\triangleright x\) | \(U=\{r,w,c\}\) | \(U-c+x=\{r,w,x\}\), by Lemma 5.4 |
| \(x\triangleright c\) | \(T=\{x,w,z\}\) | \(T-x+c=\{z,w,c\}\), by (5.36) |

Thus the four genuinely reciprocal C-108 active pairs are

\[
r\leftrightarrow u,\qquad
r\leftrightarrow z,\qquad
c\leftrightarrow a,\qquad
c\leftrightarrow x.
\]

All attacked vertices are unoccupied in their displayed bases.  The edges
\(ru,rz\) are supplied by (5.20), while the edges \(ca,cx\) are supplied
by the retained Lemma 5.4 responses; undirectedness supplies each reverse
move along the same edge.  Unlike the
shared-pivot observation in the previous subsection, no direction is
witnessed only from a possibly non-independent kernel state.  No equality
of deletion ranks is used.  Formulas (5.27)--(5.36) therefore pass without
correction.

## Independent finite reconstruction

`independent_checker.py` shares no transition core with the candidate.
It uses integer masks, its own graph6 decoder, a fresh synchronous
greatest-kernel implementation, and a fresh DSATUR routine where a clique
cover value is checked.

It established:

- `FCXfO` decodes to the candidate's exact nine-edge graph and has
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)\);
- the displayed 16-state proper family has 64 attack obligations and 72
  retained moves, realizes the exact repair square and response lists, and
  omits `015`;
- the greatest family of `FCXfO` consists of all 18 dominating triples and
  contains both `015` and `135`;
- `GEjbug` has \((\gamma,i,\alpha,\gamma^\infty)=(2,2,3,3)\), a 41-state
  greatest triple-family, named reverse state `035` at deletion rank one,
  and all four named non-dominating whole-kernel translations;
- `HCOeuqr` independently realizes the named active edge \(3\to7\), state
  `057`, and non-dominating translation `035`;
- ``HCOe`Z{`` independently realizes reverse ranks \(1,1,2,0,0\) with
  sole shared-pivot rank \(2\);
- over the pinned stream of all 261,080 connected unlabeled order-nine
  graphs, the clean-room implementation reproduced all 2,949 static
  equality graphs, all 1,380 eternal equality graphs, 28,366 active
  directed edges, 220,086 whole-kernel transforms, 4,108 failures,
  16,366 inactive orientations, and exactly 422 inactive-only
  shared-minimum violations;
- the same full replay found zero actual one-sided active survivor
  instances, as required by C-138.

The connected graph stream hash was
`fe73f2b8aad1a653b6f3bee799efff369cc486688df5aeade62ce0b3b5889eb5`.
The final clean-room replay took 29.56 seconds and about 67.7 MB maximum
resident memory on this machine.  Its output hash remained
`6a98a93b1e691f6660feeaf938da143a4b95f4dec3d542e940d97da2d5bf086c`.

I also replayed the candidate's three programs.  All three outputs matched
their frozen JSON files byte for byte.  The two full order-nine dependent
replays each took about 16 seconds and 47 MB.

## Exact final scope

The following may be promoted:

- the common-nonneighbor clique and retained ridge;
- reverse-endpoint domination at \(k=3\) (now subsumed by C-143);
- the five-state repair-square normal form and response polarization;
- reduction of any reciprocity failure to a shared-pivot square;
- the exact blocker-list dichotomy;
- the three minimum-rank blocker adjacency caps;
- paired-singleton propagation when the blocker misses the pivot;
- Lemma 5.5's four reciprocal active pairs in the third-base system;
- the two finite refutations of stronger proof mechanisms.

The following remain open:

- greatest-family complementary-exchange reciprocity;
- elimination of the shared-pivot-active blocker branch;
- elimination of the remaining paired-singleton adjacency patterns;
- the complete \(k=3\) gamma--theta case;
- the universal gamma--theta conjecture.

The finite checks corroborate the controls and scope.  They are not a
proof of the conditional all-order lemmas; those are accepted on the
human-readable arguments audited above.
