# Hostile review: rank-zero full-list three-color coupling

## Verdict

**UNCONDITIONAL PASS ON COMMIT
`db9c046d029b7d074676e658a9728e5fa2846ca9`.**

The candidate theorem is correct at its stated rank-zero, nonroot-corridor
scope.  The palette transfer

\[
v\in Q(q)\cup Q(w)
\]

follows from two forced one-guard witness responses and one final closure
attack.  The delicate implication involving \(v\notin Q(q)\) is sound:
the proof first shows that retention of the relevant endpoint would force
both the edge \(qv\) and the required root-swap state, hence membership in
\(Q(q)\).  It then takes the contrapositive only at the level of family
membership.  It never infers a graph nonedge from a missing palette entry.

An independent set-based implementation confirms every exact assertion about
the equality and gamma-two controls.  The finite functional-digraph reduction
is exhaustive.  The exploratory solver table is correctly labeled
`OBSERVED`; it has no proof logs and is not promoted by this review.

This result does **not** prove that a safe color exists, compare ranks from
different color bans, eliminate all rank-zero corridor cycles, prove the
complete \(k=3\) case, or resolve the gamma--theta conjecture.

## 1. Frozen candidate and dependencies

The reviewed candidate note has SHA-256

`3d0e38493159d69b6d790b9614253e02f92ab7acbf5acf7a54dc003f7f10bb87`.

The declared accepted dependencies are present byte for byte:

| Dependency | SHA-256 |
|---|---|
| C-149 restricted-kernel note | `a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d` |
| C-154 terminal-gate note | `0d6eb44fa2807cd34e441c31364149577cccf39c28b426a5d81b7cc78c9d1253` |
| C-157 rank-zero corridor note | `0497d07b8cf2bf1f5e3572f35d400d954745abae4490e6cac707f15cbcaeb22c` |
| C-163 positive-rank note | `e25845bbf5e23886284f2046ac8c5c661b48176f4bef9fda5651f733d4a0edb0` |
| C-165 restoration note | `fc407cb436bfd48f1eb26123cbe02ad1318f4a8a3a8cdee02a48064362261b9d` |

C-149 supplies the retained corridor form, the ban convention, the nonroot
occupancies, and the diamond.  C-157 supplies exactly the legal unbanned
nondominating alternate, its missed witness, the edge from the secondary
anchor to that witness, and the witness collision exclusions.  The new proof
uses no stronger interpretation of either result.  C-154, C-163, and C-165
are used only to state the surrounding residual-case frontier.

## 2. Model and occupancy audit

Write

\[
S=\{u,v,t\},\quad
T=\{v,t,q\},\quad
E=\{v,t,r\},\quad
F_v=\{u,t,r\}.
\]

The hypotheses guarantee all displayed attacks are at unoccupied vertices:

- fullness gives \(B=N_{\overline G}(x)\) disjoint from \(S\);
- \(r\in B\), while the corridor mover
  \(q\notin S\cup B\cup\{x\}\);
- the corridor attack makes \(q\ne r\);
- C-157 gives \(w\notin S\cup\{x,q,r\}\).

Thus \(w\) is unoccupied in \(T\) and \(F_v\), and \(u\) is unoccupied in
\(\{w,t,q\}\).  Every displayed response replaces one guard by the attacked
vertex, and every move edge is explicitly justified.  No all-guards move,
occupied attack, distance move, or change of eternal family appears.

The phrase “exactly the two physical responders” in the final attack is also
literal: \(tu\notin E(G)\) because \(S\) is independent, while the proof
derives \(wu,qu\in E(G)\).

## 3. Theorem 2.1 line by line

### 3.1 Forced edges

Because \(v\in Q(r)\), the state

\[
F_v=S-v+r=\{u,t,r\}
\]

is retained.  The C-157 witness \(w\) is missed by
\(\{t,q,r\}\), so \(tw,qw,rw\notin E(G)\).  Since \(F_v\) dominates \(w\),
the only remaining guard \(u\) must meet \(w\).  C-157 separately gives
\(vw\in E(G)\).  This proves precisely (2.1).

### 3.2 The two witness ladders

At the unoccupied attack \(w\) from \(T\), the guards \(t,q\) miss \(w\)
and \(v\) meets it.  Therefore \(v\to w\) is the unique physical move and
closure retains \(\{w,t,q\}\).

At the same unoccupied attack from \(F_v\), the guards \(t,r\) miss \(w\)
and \(u\) meets it.  Therefore \(u\to w\) is unique and closure retains
\(\{w,t,r\}\).  Both deductions take place in the literal unrestricted
greatest family \(\mathcal F^\star\), as stated.

### 3.3 The palette transfer

The retained predecessor \(T\) dominates the omitted root anchor \(u\).
The other root anchors \(v,t\) miss \(u\), so \(qu\in E(G)\).  Together
with \(T=S-u+q\in\mathcal F^\star\), this gives \(u\in Q(q)\).

Now attack the unoccupied \(u\) from
\[
K=\{w,t,q\}\in\mathcal F^\star.
\]
The only physical endpoints are
\[
K-w+u=S-v+q,\qquad K-q+u=S-v+w.
\]

If the first endpoint is retained, it dominates the omitted root anchor
\(v\).  The two root guards \(u,t\) miss \(v\), hence \(qv\in E(G)\);
retention of that same endpoint then gives \(v\in Q(q)\).  Consequently
\[
v\notin Q(q)\Longrightarrow S-v+q\notin\mathcal F^\star.
\]
This is a valid contrapositive about a conjunction already proved.  It is
not the invalid implication \(v\notin Q(q)\Rightarrow qv\notin E(G)\).

Closure of \(K\) at \(u\) now forces the second endpoint.  The accepted
edge \(vw\) then yields \(v\in Q(w)\).  Hence
\(v\in Q(q)\cup Q(w)\) in all cases.  The independent checker exhausts the
four admissible truth-table rows for the endpoint/edge branch and finds no
failure.

## 4. Corollary and three-color reduction

When \(Q(r)=S\), C-157 proves that the missed-witness sets for the two
secondary anchors are disjoint: a witness for one secondary anchor misses
the other anchor, while a witness for that other anchor is adjacent to it.
Applying Theorem 2.1 separately therefore gives the stated two transfers
with distinct witnesses.  The primary color is already in \(Q(q)\), so the
three cases in Corollary 2.2 are exhaustive.

For three selected rank-zero nonsingleton nonroot corridor rows, choosing
one secondary color per row defines a fixed-point-free self-map on three
root colors.  There are exactly eight labeled maps:

- two directed 3-cycles;
- six 2-cycles with the third color feeding into one cycle vertex.

No cross-row vertex distinctness is used.  Terminal vertices, movers,
witnesses, and transfer endpoints from different rows may collide.  The
MMV-001 control realizes the extreme collision
\(w_u=q_{\sigma(u)}\) around a 3-cycle, confirming that the candidate has
not silently assumed otherwise.

## 5. Restricted-rank scope

The candidate keeps unrestricted family closure and restricted deletion
ranks separate.

- If a recipient endpoint is \(S-v+q_u\), then
  \(q_u\notin B\), so the endpoint is unbanned for color \(v\).
- If it is \(S-v+w_u\), it is unbanned exactly when \(w_u\notin B\).
- Under an empty recipient kernel, every retained unbanned dominating triple
  has a finite recipient rank.
- The two witness attacks are not deletion-witness attacks for the recipient
  peeling, so they imply no strict comparison with the source rank.

Ranks belonging to different bans are never compared.  The “open cross-ban
rank gate” is therefore an accurate description of what remains, rather than
an unproved step hidden inside the theorem.

## 6. Independent control replay

`independent_replay.py` imports no campaign code.  It uses neighbor sets,
sorted guard tuples, direct synchronous deletion, exhaustive subset
evaluation, and an independently written coloring backtracker.

### Equality control

For

`OYifur}UO]}iTij]tpo]v`

it obtains:

| Quantity | Independent result |
|---|---:|
| order, size | \(16,71\) |
| \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | \((3,3,3,3,3)\) |
| unrestricted greatest family | \(304\) triples |
| unrestricted deleted before stabilization | \(3\) triples |
| restricted kernels for colors \(0,1,10\) | \(0,150,0\) |
| color-0 deletion rounds | \(28,81,132,62\) |
| color-1 finite deletion rounds | \(31,74,49\) |
| color-10 deletion rounds | \(32,81,128,62\) |

It independently recovers
\[
Q(11)=\{0,1\},\quad Q(7)=\{1,10\},\quad Q(5)=\{0,10\}.
\]
Both named annihilated rows have rank-zero predecessors, the displayed
alternate misses exactly the named witness, both witness-ladder states are
retained, and the final transfer has exactly the responders \(w,q\).  In
each row \(v\notin Q(q)\), \(v\in Q(w)\), and the witness endpoint is
retained.  The color-1 predecessor and its dominating secondary alternate
\(\{0,3,7\}\) both lie in the 150-state kernel.

### Gamma-two control

For MMV-001

`IEhbtj{ro`

the replay obtains:

| Quantity | Independent result |
|---|---:|
| order, size | \(10,26\) |
| \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | \((2,2,3,3,4)\) |
| unrestricted greatest family | \(86\) triples |
| restricted kernels | \(0,0,0\) |
| dominating pairs | exactly \(\{8,9\}\) |

All three named predecessors have rank zero.  Every alternate misses exactly
the displayed witness; every ladder and transfer endpoint is retained; and
the exact collision cycle
\[
w_0=q_1,\qquad w_1=q_2,\qquad w_2=q_0
\]
is present.  This is a sharp gamma-two boundary, not a counterexample to the
theorem, because its \(\gamma=3\) hypothesis fails.

The independent stdout SHA-256 is
`93a2c9230925c99f8d02b47b2a4aa382d3b66a3d9d2d5143e6d6ac0f5c8a02fc`.

## 7. Discovery-CNF audit and status separation

The discovery generator has the claimed semantics.

- The root is an independent retained triple and the target is full.
- Four-set clauses impose \(\alpha\le3\).
- For every vertex pair, an auxiliary-variable block requires a third vertex
  missed by both closed neighborhoods, imposing \(\gamma\ge3\).
- Family clauses impose domination at every unoccupied attack and require at
  least one successor produced by moving one adjacent guard.
- The named nonedges make each secondary alternate nondominating, so each
  named corridor predecessor really is rank zero for its displayed ban.
- Root retention supplies \(\gamma\le3\), and a nonempty eternal triple
  family supplies \(\gamma^\infty\le3\); together with \(\gamma\ge3\), the
  encoded graph has exact equality at three.
- No clique-cover condition and no global restricted-kernel-emptiness
  condition are encoded.

An independent count gives
\[
\binom n2+\binom n3+\binom n2(n-2)+3\binom n3(n-3)
\]
variables and
\[
67+\binom n4+\binom n2(3(n-2)+1)+11\binom n3(n-3)
\]
clauses.  These reproduce all seven reported size rows exactly.

The statuses for \(n=10,\ldots,15\) have no DRAT/LRAT logs or independent
solver replay, and \(n=16\) is a timeout.  The candidate labels the entire
table `OBSERVED`, says it is not a finite exclusion, and uses none of it in
Theorem 2.1, Corollary 2.2, or Proposition 3.1.  This review preserves that
classification.

## 8. Reproduction

From the repository root:

```text
gamma_theta_eternal_domination/reviews/full_list_three_color_coupling_hostile/verify_strict.sh
```

The runner verifies the frozen candidate and dependency bytes, replays the
candidate checker, runs the independent implementation, checks its exact
stdout hash, reconstructs every CNF size row, and confirms that no discovery
status has been promoted beyond `OBSERVED`.

Estimated completion of this hostile review: **100%**.  Estimated contribution
of the accepted transfer lemma toward the remaining all-three-empty rank-zero
corridor subcase: **about 20%**.  This is a workload estimate, not a
probability of the conjecture.
