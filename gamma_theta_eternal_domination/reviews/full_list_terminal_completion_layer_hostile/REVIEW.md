# Hostile review: the rank-zero terminal-completion layer

## Verdict

**UNCONDITIONAL PASS ON COMMIT
`e83ad600adcd1932ce9612239cf8a72b2f15a7a8`.**

The two formal completion theorems are correct at their stated scope.  From
the retained terminal \(\{v,t,r\}\), every common nonneighbor \(d\) of
\(x,r\) has a retained response state obtained by moving \(v\) or \(t\).
Retention of the state \(\{d,t,r\}\) forces
\(d\in N_G[w_v]\), including the collision \(d=w_v\), and its attack at
\(x\) uniquely returns to \(\{x,r,d\}\).  The symmetric statement gives
the two-closed-neighborhood cover when both secondary colors are present.

The proof uses only unoccupied attacks and one-edge, one-guard responses.  It
does not infer a graph nonedge from missing family membership or a missing
palette entry.  It does not compare deletion ranks.

The independent replay confirms all three exact controls.  It also exposes an
important terminology boundary: a named branch *state* can be retained even
when the corresponding move into it is not physical.  The candidate's formal
statements and the sets \(R_v,R_t\) are explicitly defined by state
membership, so this causes no mathematical defect.  Phrases such as “both
branches survive” must be read as “both named branch states are retained,”
not as a claim that both moves from the terminal are legal.

This result does **not** prove a safe color, a strict rank inequality, the
complete \(k=3\) case, or the gamma--theta conjecture.

## 1. Frozen candidate and dependencies

The reviewed candidate commit is
`e83ad600adcd1932ce9612239cf8a72b2f15a7a8`.  Its relevant frozen hashes are:

| Artifact | SHA-256 |
|---|---|
| Candidate `NOTE.md` | `be6aab16586fc661c425add810f5bfd160ca6545c548ab0b65bdce32f5ec8ccb` |
| Candidate `MANIFEST.json` | `1cbece40dfb7219eece0c8a11036bc6ea287f84e2c4998df502dc6ad369f88c9` |
| Candidate strict stdout | `cd0d99948fea753ebd6c8706d404ddc89ffacc9a47ed9420eddefef033152bb2` |

The manifest's declared source hashes and dependency hashes all match the
reviewed bytes.  The accepted dependencies used by the proof are:

| Dependency | SHA-256 |
|---|---|
| C-149 restricted-kernel note | `a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d` |
| C-157 rank-zero corridor note | `0497d07b8cf2bf1f5e3572f35d400d954745abae4490e6cac707f15cbcaeb22c` |
| C-157 control verifier | `3001b7f7b922cf91ad9ad4780b32d7f38acc4b673263ee7583869589709d6fc8` |
| C-168 corridor-transfer note | `3d0e38493159d69b6d790b9614253e02f92ab7acbf5acf7a54dc003f7f10bb87` |

C-157 supplies the nondominating alternate and its missed witness.  C-168
supplies
\[
uw_v,vw_v\in E(G),\qquad
tw_v,qw_v,rw_v\notin E(G),
\]
and the two retained witness states.  The new completion proof uses no
stronger consequence.

## 2. Occupancy and collision audit

Write
\[
S=\{u,v,t\},\quad T=\{v,t,q\},\quad E=\{v,t,r\}.
\]
The target \(x\) is full at \(S\), \(r\in N_{\overline G}(x)\), and the
nonroot corridor has \(q\notin S\cup N_{\overline G}(x)\cup\{x\}\).
Consequently \(xr\notin E(G)\), while \(x\) meets \(u,v,t,q\).

For
\[
C_{xr}=\{d\notin\{x,r\}:dx,dr\notin E(G)\},
\]
every \(d\) is distinct from \(u,v,t,q,x,r\):

- \(d\ne x,r\) by definition;
- \(d\ne u,v,t\) because \(x\) meets all root anchors;
- \(d\ne q\) because \(xq\in E(G)\).

Thus the attack at \(d\) from \(E\), and every later attack at \(x\), is
unoccupied.  All displayed configurations are genuine triples.

The witness exclusions from C-157 leave only one relevant unresolved
collision: \(d=w_v\), or symmetrically \(d=w_t\).  This is exactly why the
conclusion is \(d\in N_G[w_v]\), not the open edge \(dw_v\).  The four-row
logic table in the independent replay verifies that domination of \(w_v\)
by \(\{d,t,r\}\), when \(t,r\) miss \(w_v\), is equivalent to the required
closed-neighborhood conclusion in both collision and noncollision cases.

If both secondary colors exist, their witnesses are distinct.  A
\(v\)-witness meets \(v\) and misses \(t\), whereas a \(t\)-witness meets
\(t\) and misses \(v\); equality would simultaneously force an edge and a
nonedge.

## 3. Proof reconstruction

### 3.1 The completion set

Because \(\gamma(G)=3\), the pair \(\{x,r\}\) does not dominate.  A vertex
missed by its closed neighborhood lies in \(C_{xr}\), so this set is
nonempty.  Since \(xr\notin E(G)\), two nonadjacent vertices of \(C_{xr}\)
would join \(x,r\) to form an independent four-set, contradicting
\(\alpha(G)=3\).  Hence \(C_{xr}\) is a clique.

For every \(d\in C_{xr}\), the state
\[
I_d=\{x,r,d\}
\]
is an independent triple.  Its retention also follows dynamically below,
so the completion theorem does not need to conceal an additional use of the
maximum-independent-state theorem.

### 3.2 Nonempty response split

Attack \(d\) from the retained terminal \(E=\{v,t,r\}\).  The guard at
\(r\) cannot move because \(rd\notin E(G)\).  Eternal closure therefore
retains at least one physically reachable successor:
\[
D_v(d)=\{d,t,r\}\quad\text{via }v\to d,
\qquad
D_t(d)=\{v,d,r\}\quad\text{via }t\to d.
\]
Thus at least one of the two named states belongs to
\(\mathcal F^\star\).  This quantifier is existential over **retained
physical responses**, and it is stronger than the bare membership
conclusion needed later.

### 3.3 Closed-witness incidence

Suppose \(D_v(d)\in\mathcal F^\star\), whether or not this state was the
physical response selected in the preceding attack.  Every retained state
dominates.  Since \(t,r\) miss \(w_v\), domination of \(w_v\) by
\(\{d,t,r\}\) gives exactly
\[
d=w_v\quad\text{or}\quad dw_v\in E(G),
\]
that is, \(d\in N_G[w_v]\).  This argument does not require \(vd\) to be
an edge and is therefore valid for the membership-defined set \(R_v\).

Now attack \(x\) from \(D_v(d)\).  Both \(d\) and \(r\) miss \(x\), while
fullness gives \(tx\in E(G)\).  Hence \(t\to x\) is the unique physical
response, its endpoint is \(I_d\), and eternal closure retains \(I_d\).

The same proof after exchanging \(v,w_v\) with \(t,w_t\) yields
\[
D_t(d)\in\mathcal F^\star\Longrightarrow d\in N_G[w_t],
\]
and the unique response \(v\to x\) from \(D_t(d)\) to \(I_d\).

### 3.4 Two-witness cover and branch quantifiers

Define
\[
R_v=\{d\in C_{xr}:D_v(d)\in\mathcal F^\star\},\qquad
R_t=\{d\in C_{xr}:D_t(d)\in\mathcal F^\star\}.
\]
The retained-response split proves \(C_{xr}=R_v\cup R_t\); the preceding
domination arguments prove
\[
R_v\subseteq N_G[w_v],\qquad R_t\subseteq N_G[w_t].
\]
Therefore
\[
C_{xr}\subseteq N_G[w_v]\cup N_G[w_t].
\]

If \(d\notin N_G[w_v]\), then \(D_v(d)\) cannot be retained.  Closure at
the terminal attack consequently forces \(t\to d\) and the retained state
\(D_t(d)\).  It is the unique **retained** response, although \(v\to d\)
could still be a physical move to a nonretained state.  This is exactly the
candidate's formal claim.

The independent controls show why the distinction between membership and
reachability matters.  In the equality control:

- for \(u=0,d=13\), \(D_v(d)\) is retained but \(vd\notin E(G)\);
- for \(u=10,d=9\), the same phenomenon occurs.

It also occurs for \(u=2,d=6\) in the 11-vertex gamma-two control.  No proof
step assumes otherwise, and the candidate's sets \(R_v,R_t\) are correctly
defined by membership.

## 4. Palette and rank audit

The new proof uses positive palette membership only through the accepted
C-157/C-168 consequences.  It never argues that absence from a response
palette implies a graph nonedge, nor that absence of a successor from
\(\mathcal F^\star\) implies a missing move edge.

All completion transitions take place in the unrestricted greatest family.
A unique physical response at \(x\) proves retention of its endpoint, but it
does not say that \(x\) is a deletion-witness attack at any specified
restricted peeling round.  The candidate correctly makes no inequality
between the deletion ranks of the source and target, within one ban or
across different bans.

## 5. Independent exact replay

`independent_replay.py` imports no campaign code.  It uses adjacency
frozensets, frozenset guard configurations, direct exhaustive parameter
search, a separately written exact coloring backtracker, and literal
synchronous greatest-fixed-point deletion.  It decodes and re-encodes every
graph6 record and recomputes every edge-list hash.

### Equality rank-reversal control

For `OYifur}UO]}iTij]tpo]v`, the replay obtains:

| Quantity | Independent result |
|---|---:|
| order, size | \(16,71\) |
| \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | \((3,3,3,3,3)\) |
| unrestricted greatest family | \(304\) triples |
| unrestricted deletion rounds | \(3\) |
| restricted kernels for \(0,1,10\) | \(0,150,0\) |
| color-0 deletion rounds | \(28,81,132,62\) |
| color-1 finite deletion rounds | \(31,74,49\) |
| color-10 deletion rounds | \(32,81,128,62\) |
| dominating pairs | none |

The completion sets are \(C_{6,11}=\{13\}\) and
\(C_{6,5}=\{7,9\}\).  Every named first branch state is retained and has
source rank zero; each unique attack at \(x\) reaches an independent
completion of source rank three.  Every second branch state is also
retained.  As noted above, two of the first branch states are retained
without being physically reachable from their terminal.

### All-empty gamma-two control

For `JEhbtj{rvu?`, the replay obtains:

| Quantity | Independent result |
|---|---:|
| order, size | \(11,33\) |
| \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | \((2,2,3,3,4)\) |
| unrestricted greatest family | \(118\) triples |
| restricted kernels for \(0,1,2\) | \(0,0,0\) |
| dominating pairs | exactly \(\{1,10\},\{5,10\}\) |

The graph is exactly the stated one-vertex extension of MMV-001, with new
neighborhood \(\{0,1,2,3,4,6,7\}\).  The three completion sets are
\(\{10\},\{7\},\{6\}\).  Every named first and second branch state is
retained, all first states have source rank zero, and all independent
completions have source rank three.  This is a gamma-two boundary, not an
instance of the equality theorem.

### Full-terminal overlap control

For `HF~mdfj`, the replay obtains:

| Quantity | Independent result |
|---|---:|
| order, size | \(9,24\) |
| \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | \((2,2,3,3,3)\) |
| unrestricted greatest family | \(76\) triples |
| restricted kernels for \(0,1,2\) | \(68,65,65\) |
| terminal palette \(Q(5)\) | \(\{0,1,2\}\) |

The two witnesses are the distinct vertices \(6,7\), the completion set is
\(C_{3,5}=\{8\}\), and vertex \(8\) meets both witnesses.  Both named
branch states are retained for both secondary rows, and each attack at the
full target has the asserted unique return to \(\{3,5,8\}\).  The
independent completion survives the color-0 restricted kernel, so it has no
finite color-0 deletion rank.  This confirms both the overlap sharpness and
the absence of a forced rank comparison.

The independent stdout SHA-256 is
`6a4dd3fbf82835b049d71717266e88a24436e1bc9c17558ac4230fd249bc4526`.

## 6. Scope and reproduction

The discovery-only `UNSAT` observations through order 12 have no proof logs
or independent formula reconstruction.  The candidate labels them
`OBSERVED`, does not use them in either theorem, and does not promote a
finite exclusion.  This review preserves that status.

From the repository root, run:

```text
gamma_theta_eternal_domination/reviews/full_list_terminal_completion_layer_hostile/verify_strict.sh
```

The runner checks the frozen commit and all candidate/dependency bytes,
replays the candidate verifier, executes the independent implementation,
and compares its output byte for byte with the frozen result.

Best-guess completion of this hostile review: **100%**.  Best-guess
contribution of the accepted completion layer toward eliminating the
remaining full-list \(k=3\) branch: **about 5%**.  These are workload
estimates, not probabilities that the conjecture is true.
