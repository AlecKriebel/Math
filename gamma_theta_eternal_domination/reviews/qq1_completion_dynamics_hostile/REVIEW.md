# Hostile review: canonical QQ1 completion dynamics

Date: 2026-07-28 (PDT)

Candidate commit:
`02cab3f647e6449c5a8882d0d2d3c283f4254ae2`

## Verdict

\[
\boxed{\textbf{UNCONDITIONAL PASS}}
\]

I independently reconstructed the canonical QQ1 hypotheses from accepted
C-158, checked every use of C-010, C-064, C-108, C-143, C-146, and
C-161, replayed the complete cold-witness attack tree, audited all named
vertex collisions, and evaluated both fixed controls without importing
the candidate checker or either campaign verifier.

The candidate proves exactly the following.

> Assume
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\) and the accepted canonical
> rank-one QQ1 normal form.  Every common nonneighbor \(d\) of \(x,r\)
> hits \(p,q,b,c\), and \(\{u,x,d\}\) dominates \(G\).  Therefore every
> vertex missed by \(\{u,d\}\), whose existence is forced by
> \(\gamma(G)=3\), is an external hot witness: it hits \(x,r\) and at
> least one of \(b,c\).  The reverse completion state has rank at most
> three; if it has rank three, the two mixed states have rank exactly
> two.  When \(ud\) is a nonedge, the hot witness recreates the same
> repair-square asymmetry with the very same omitted corner and hence the
> same deletion rank.

This does **not** eliminate the hot-witness layer, the canonical QQ1
normal form, higher-rank asymmetry, or any counterexample.  It does not
prove complete \(k=3\) or the gamma--theta conjecture.

I found no mathematical error, hidden freshness assumption, omitted
one-guard response, occupied-vertex attack, misuse of complement
adjacency, or conversion of a missing family transition into a graph
nonedge.

## Frozen candidate and dependency ledger

| artifact | SHA-256 |
|---|---|
| candidate `NOTE.md` | `7deb990de3f1c4adf8540f1c922750197604ac0ea44131cd229a523716335328` |
| candidate `RESEARCH_LOG.md` | `4a4f7bb7e1d8fe02f25b7736dc0bc2a51692a838c3958d28beb277333a8a64af` |
| candidate `CANDIDATE_MANIFEST.json` | `d62d85bf10efe4857e804a30385adf698dd596efac8ddc73b09da5c5c7341a25` |
| candidate `expected_result.json` | `7ff18b948515d9c96f9ee46371b40c7436692dae269ba6112c452175e8be7be8` |
| candidate `verify_implication.py` | `9fd44d231d59b2d0f1d8db4fc434b8e6df5e2403985c7fdeaef2e89821192c1e` |
| candidate `verify_strict.sh` | `b8bd7b9cd1b75ea75639c9cb7e916ec8244086d6d24d8c10181d39f373f7dbb3` |
| accepted C-010 source | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |
| accepted C-064 source | `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7` |
| accepted C-108 source | `d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8` |
| accepted C-143 source | `3255bcc3d75b8538d6c8e3288f8106b553194bbac1fc3ac590d18ba6d6f81de3` |
| accepted C-146 source | `3481a7dcc650a83d3994ff4bfdfb7789a520bb6a29dc57b51c1a84d549fd5b77` |
| accepted C-158 source | `4983d87b0af8cec7ca06aa7a0a12b96bb480b8dbe4c886773770046b9b4090d6` |
| accepted C-161 source | `82baf97f95ff3f62442187fbf5a3bd043e7d790ff052ae01424c0791fac173ae` |

The candidate directory at the reviewed commit and at review time was
byte-identical.

## 1. Reconstruction of the canonical QQ1 core

Write

\[
T=\{x,p,q\},\qquad B=\{u,p,q\}.
\]

The accepted C-158 normal form gives

\[
ux,ur,pr,qr,pb,qc,xb,xc,bc,up,uq\in E(G)
\]

and

\[
xp,xq,pq,xr,bu,br,bq,cu,cr,cp\notin E(G).
\]

Here \(T\) is independent and retained, \(B\) is dominating of deletion
rank one, \(u\triangleright x\), and
\(x\not\triangleright u\).  For every

\[
d\in C_{xr},
\]

accepted C-158 gives

\[
dx,dr\notin E(G),\qquad dp,dq\in E(G).
\]

All named collisions involving \(d\) are excluded without a freshness
assumption:

- \(d\ne u\) because \(ux,ur\) are edges;
- \(d\ne p,q\) because \(pr,qr\) are edges;
- \(d\ne b,c\) because \(xb,xc\) are edges.

Thus every attack involving \(d\) in the candidate is genuinely at an
unoccupied vertex.

## 2. C-143 forces both additional completion edges

The triple

\[
I_d=\{x,r,d\}
\]

is independent and hence retained by C-010.  Applying accepted C-143 to
the active orientation \(u\triangleright x\) makes

\[
R_d=I_d-x+u=\{u,r,d\}
\]

dominating.

Both \(u\) and \(r\) miss \(b\).  Consequently domination of \(b\) by
\(R_d\) forces \(db\in E(G)\).  The identical argument at \(c\) forces
\(dc\in E(G)\).  This verifies that every \(d\in C_{xr}\), not merely
one selected completion, is adjacent to all of \(p,q,b,c\).

The candidate correctly warns that this conclusion needs C-143.
Independence of \(I_d\) alone does not imply domination of \(R_d\).

## 3. Complete cold-witness contradiction

Suppose a vertex \(w\) is missed by

\[
\{u,x,d\}.
\]

It is automatically outside that triple and distinct from every named
core vertex.  The triple

\[
J_d=\{x,w,d\}
\]

is independent, hence retained by C-010.

### First response list

Attack the unoccupied target \(u\) from \(J_d\).

- The guard \(w\) is graph-ineligible because \(wu\notin E(G)\).
- The guard \(x\) is graph-eligible, but its successor is absent from the
  greatest family because \(x\not\triangleright u\) and C-108 makes this
  status uniform over every independent triple containing \(x\).
- Eternal closure therefore forces \(d\to u\), proving \(du\in E(G)\)
  and
  \[
  L_{J_d}(u)=\{d\}.
  \]

There is no silent assumption that \(du\) was already an edge.  If it
were absent, the retained state \(J_d\) would have no response at \(u\),
which is already a contradiction.

The retained independent state \(J_d\) must also dominate \(r\).
Because \(x,d\) miss \(r\), this incidentally forces \(wr\in E(G)\).
The candidate does not use this extra edge in the cold attack tree.

### C-064 transport

The independent states

\[
I_d=\{x,r,d\},\qquad J_d=\{x,w,d\}
\]

share the ridge \(\{x,d\}\).  C-064 applies with the transposition
\((r\ w)\).  The attack target \(u\) and responder \(d\) are both fixed,
so exact covariance gives

\[
L_{I_d}(u)=\{d\}.
\]

The \(r\to u\) successor

\[
A=\{u,x,d\}
\]

is therefore absent from the family.  This is a family omission only.
The proof nowhere asserts \(ru\notin E(G)\); in fact \(ru\) is a fixed
canonical edge.

### Terminal attack from \(U\)

The accepted C-158 state

\[
U=\{u,b,c\}
\]

is retained.  Attack the unoccupied target \(d\).  The newly forced edge
\(du\) and the two C-143 consequences \(db,dc\) make all three guards
eligible.

1. \(u\to d\) gives \(\{d,b,c\}\), which misses \(r\).
2. \(b\to d\) gives \(D_b=\{u,d,c\}\).  At the unoccupied attack \(x\),
   \(d\) is ineligible.  The \(u\)-successor \(\{x,d,c\}\) misses \(r\),
   while the \(c\)-successor is the omitted state \(A\).
3. \(c\to d\) gives \(D_c=\{u,b,d\}\).  At \(x\), the
   \(u\)-successor \(\{x,b,d\}\) misses \(r\), while the
   \(b\)-successor is again \(A\).

These are all guards at both stages.  Each attack is unoccupied, each
allowed move uses one graph edge, and each rejected branch ends in either
a named missed vertex or the single previously proved family omission.
Thus \(U\) has no retained response at \(d\), a contradiction.

The clean-room audit exhausts all \(64\) assignments to the four unused
incidences \(wp,wq,wb,wc\), together with the initially unknown edges
\(du,rw\).  Thirty-two assignments make \(J_d\) miss \(r\), sixteen leave
no response at \(u\), and the remaining sixteen reach the complete
terminal attack on \(U\).  No incidence assignment survives.

## 4. Hot witnesses and collision audit

Since \(\gamma(G)=3\), the pair \(\{u,d\}\) does not dominate.  Choose
\(w\) missed by this pair.  The just-proved domination of
\(\{u,x,d\}\) forces \(wx\in E(G)\).  Domination by
\(R_d=\{u,r,d\}\) forces \(wr\in E(G)\), and domination by
\(U=\{u,b,c\}\) forces at least one of \(wb,wc\) to be an edge.

Every possible collision with the canonical core is excluded by a fixed
edge:

| proposed collision | edge preventing \(w\) from missing \(\{u,d\}\) |
|---|---|
| \(w=x\) | \(xu\) |
| \(w=p\) | \(pu\) and \(pd\) |
| \(w=q\) | \(qu\) and \(qd\) |
| \(w=r\) | \(ru\) |
| \(w=b\) | \(bd\) |
| \(w=c\) | \(cd\) |

Thus the witness is genuinely external.  The three possible side
patterns are \(wb\) only, \(wc\) only, or both; the candidate does not
silently choose one.

## 5. Conditional repair-square self-similarity

This part of the candidate is correctly conditional on

\[
ud\notin E(G).
\]

Only under that hypothesis is

\[
K=\{u,d,w\}
\]

independent.  C-108 transports \(u\triangleright x\) to \(K\), retaining

\[
K-u+x=\{x,d,w\}.
\]

The independent state \(I_d=\{x,d,r\}\), together with the forced edge
\(rw\), therefore witnesses \(r\triangleright w\).  Conversely, the
\(w\to r\) successor from \(K\) would be

\[
K-w+r=\{u,d,r\}=R_d,
\]

which is omitted because \(x\not\triangleright u\).  C-108 then gives
\(w\not\triangleright r\).

The omitted reverse corner for the original orientation and for the
repaired orientation is literally the same set \(R_d\), not merely an
isomorphic or rank-compared set.  C-161 therefore applies exactly, and
the tracked rank is conserved tautologically through the shared state.
No descent follows.

When \(ud\in E(G)\), \(K\) is not independent.  The candidate explicitly
does not assert the repaired orientation in that branch.

## 6. Deletion-rank diamond

C-143 makes \(R_d=\{u,r,d\}\) dominating.  C-108 and
\(x\not\triangleright u\) keep it outside the greatest family, so its
rank \(h\) is positive and finite.

The independent endpoint triples

\[
T=\{x,p,q\},\qquad I_d=\{x,r,d\}
\]

share \(x\) and differ in exactly two positions.  C-146 is invoked with
fixed responder \(x\) and fixed target \(u\), comparing the reverse
states \(B=T-x+u\) and \(R_d=I_d-x+u\).  Since \(\rho(B)=1\),

\[
1\le h\le3.
\]

The candidate's two local attacks are exhaustive.

- At \(p\) from \(R_d\), the \(u\)-successor \(\{p,r,d\}\) misses \(x\),
  the \(d\)-successor \(\{u,r,p\}\) misses \(c\), and only
  \(P_d=\{u,p,d\}\) can have positive rank.
- At \(q\), the symmetric two rank-zero successors leave only
  \(Q_d=\{u,q,d\}\).
- At \(q\) from \(P_d\), the only eligible movers are \(u,d\).
  The \(u\)-successor \(\{p,q,d\}\) misses \(x\); the
  \(d\)-successor is \(B\), of rank one.  Hence \(\rho(P_d)\le2\).
- The symmetric attack gives \(\rho(Q_d)\le2\).

If \(h\ge2\), membership \(R_d\in\mathcal K_{h-1}\) forces both mixed
states into \(\mathcal K_{h-2}\).  Therefore

\[
h\le1+\min\{\rho(P_d),\rho(Q_d)\}.
\]

In the top case \(h=3\), both ranks are forced to be exactly two.  The
clean-room rank enumeration has fourteen arithmetically admissible
\((h,\rho(P_d),\rho(Q_d))\) triples and a unique top triple
\((3,2,2)\).  The candidate does not claim exact lower-level ranks when
\(h=1\) or \(2\).

## 7. Complement-link caps

The four caps quoted from C-161 are in the correct direction.  If an
outside vertex \(z\) misses both asymmetric endpoints \(u,x\), then each
simultaneous pair of additional nonedges would create a path from \(u\)
to \(x\) in the complement link \(L_z\):

\[
u-b-q-x,\quad
u-b-r-x,\quad
u-c-p-x,\quad
u-c-r-x.
\]

C-161 forbids all four paths.  The completion-triple theorem adds that
such an outside \(z\) must hit each \(d\in C_{xr}\), so the completion
does not join the separated link components.  This is a compatibility
observation, not a new contradiction, and the candidate states it as
such.

## 8. Independent fixed-control evaluation

The clean-room checker uses a separate graph6 decoder, exhaustive subset
evaluation for \(\gamma,i,\alpha\), an exact clique-partition dynamic
program for \(\theta\), and literal synchronous greatest-kernel deletion
for two and three guards.

It obtains:

| graph6 | \(n,m\) | \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | \(|\mathcal K_3|\) | \((\rho(B),\rho(P_d),\rho(Q_d),\rho(R_d))\) |
|---|---:|---:|---:|---:|
| `Mslamztl~fnny~]~_` | \(14,67\) | \((2,3,3,3,3)\) | 284 | \((1,2,2,3)\) |
| `NslalntvXzn^{~n||^w` | \(15,78\) | \((2,3,3,3,3)\) | 285 | \((1,2,2,3)\) |

For both graphs it independently verifies:

- \(u\triangleright x\) and \(x\not\triangleright u\);
- the canonical private witnesses for all three rank-zero successors of
  \(B\) at \(r\);
- the unique \(x,r\)-completion, at vertices \(9\) and \(7\),
  respectively;
- adjacency of that completion to \(p,q,b,c\);
- domination by \(\{u,x,d\}\) and by the pair \(\{u,d\}\); and
- the exact rank vector \((1,2,2,3)\).

The first control has 21 dominating pairs and \(\{u,x\}\) dominates.
The second has 23 dominating pairs while \(\{u,x\}\) does not dominate.
Both stop before the equality-only hot layer because \(\{u,d\}\)
dominates.  They are sharp \(\gamma=2\) controls, not counterexamples and
not evidence that the hot layer is realizable under \(\gamma=3\).

## 9. Model and scope ledger

| audit item | result |
|---|---|
| every independent triple retained only via accepted C-010 | **PASS** |
| C-143 applied to the correct reverse endpoint | **PASS** |
| C-064 uses one retained independent ridge and the correct transposition | **PASS** |
| exact list \(L_{J_d}(u)=\{d\}\) justified | **PASS** |
| all attacks are at unoccupied vertices | **PASS** |
| exactly one guard moves along one graph edge | **PASS** |
| every cold-tree response branch is exhausted | **PASS** |
| all hot-witness core collisions excluded | **PASS** |
| conditional \(ud\)-nonedge hypothesis retained | **PASS** |
| same repair corner, not an assumed rank inequality | **PASS** |
| C-146 uses fixed responder/target and distance two | **PASS** |
| rank-zero, finite-rank, and retained states distinguished | **PASS** |
| absent family transition never treated as a graph nonedge | **PASS** |
| controls independently decoded and evaluated | **PASS** |
| canonical QQ1 or hot layer excluded | **OPEN / NOT CLAIMED** |
| complete \(k=3\) or universal conjecture | **OPEN / NOT CLAIMED** |

## Strict replay

From the repository root, run:

```sh
sh gamma_theta_eternal_domination/reviews/qq1_completion_dynamics_hostile/verify_strict.sh
```

Expected final line:

```text
QQ1 completion-dynamics hostile review: PASS
```

The strict script checks the frozen candidate hashes, replays the
candidate's byte-exact checker, runs the clean-room symbolic and
fixed-control audit, and compares its JSON output byte for byte.
