# Hostile review: rank-one QQ0/AQ0 exclusion

Review date: 2026-07-28 PDT

Frozen candidate commit:
`0ddef53f381fa7858e1c6db55f96126b30db5c5b`

Frozen candidate:
`math/working/rank_one_remaining_endgame/NOTE.md`

Candidate SHA-256:
`26d8e8bd08dc5e821596c8ba8c60a5f1b7704d3839f1cfe6671da6e7c88b28f6`

## Verdict

**UNCONDITIONAL PASS.**

Under
\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\]
the frozen note correctly proves that neither rank-one QQ0 nor rank-one
AQ0 can occur in the accepted C-150 multi-hit setup.  I found no missing
collision case, occupied attack, illegal move, unverified retained state,
or inference from an omitted family successor to a graph nonedge.

The proof is pleasantly narrower than the earlier C-150 normal form.  It
does not need the C-150 conclusion \(y_py_q\in E(G)\), C-064 ridge
covariance, or the value of \(xr\).  It uses one of the two retained mixed
witness states, attacks the other private witness, and rejects all three
possible guards separately.

The exact accepted scope is:

> If \(B=\{u,p,q\}\) has greatest-family deletion rank one, the deleting
> attack \(r\) satisfies \(ur\notin E(G)\) and \(pr,qr\in E(G)\), and
> \(T=\{x,p,q\}\) is the independent endpoint of a one-sided active
> orientation \(u\triangleright x\), then a contradiction follows,
> independently of whether \(xr\) is absent (QQ0) or present (AQ0).

This review does not promote the discovery-only SAT script, eliminate
QQ1/AQ1, address higher deletion rank, prove reciprocity, complete
\(k=3\), or resolve the gamma--theta conjecture.

## 1. Frozen-byte and dependency audit

The candidate manifest is internally correct: every listed artifact hash
matches the file at commit `0ddef53f`.  The tracked candidate files remain
byte-identical to that commit.  The tracked discovery-only
`probe_cases.py` and the untracked concurrent `minimize_pair_core.py` were
not used or reviewed as proof.

The mathematical dependencies used by the note are exactly these:

| dependency | reviewed source SHA-256 | use |
|---|---|---|
| equality chain | campaign reduction | \(\gamma=\alpha=3\) gives \(i=3\) |
| C-010 | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` | every independent triple belongs to the chosen eternal triple-family |
| C-108 | `d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8` | transports \(u\to x\) to every retained independent triple containing \(u\) and avoiding \(x\) |
| C-150 | `acfbc262877c08f9e4b38aa38931c3b95699b50073aa9a67d8ac3f80ba9ba3fd` | rank-one deleting successors are non-dominating and have the displayed private witnesses |

I reread the accepted hostile reviews for all three named dependencies.
C-010 is family-universal, not merely a greatest-family statement.
C-108 applies because the transported source is an independent triple
containing \(u\), avoids \(x\), and \(ux\in E(G)\).  C-150's rank-one
semantics are exact: a deleting attack on a rank-one dominating state has
every adjacency-eligible successor outside the initial dominating-state
universe, hence non-dominating.

No result about complement coloring, clique covers, C-064 covariance, or
the conjecture is imported.

## 2. Deleting attack and private witnesses

At \(B=\{u,p,q\}\), the attack \(r\) is unoccupied.  The hypotheses
\[
 ur\notin E(G),\qquad pr,qr\in E(G)
\]
make \(p\) and \(q\) the complete legal-mover list.  Thus its two
successors are
\[
 C_p=\{u,r,q\},\qquad C_q=\{u,p,r\}.
\]
Because the deletion rank is one, both are non-dominating.

Let \(y=y_p\) be missed by \(C_p\).  It misses \(u,r,q\).  Since the
dominating state \(B\) differs from \(C_p\) only by restoring \(p\), one
has \(py\in E(G)\).  Similarly, the missed vertex \(z=y_q\) satisfies
\[
 qz\in E(G),\qquad zu,zr,zp\notin E(G).
\]
This is precisely C-150's private-witness rule; no family omission is
being read as a nonedge.

## 3. Complete named-collision audit

All seven names \(u,x,p,q,r,y,z\) are forced distinct.

- \(x,p,q\) are distinct because \(T\) is a triple, and \(u,p,q\) are
  distinct because \(B\) is a triple.  The active edge \(ux\) gives
  \(u\ne x\).  The candidate's phrase “by the two states” is shorthand
  for these state facts together with the already assumed active edge;
  the conclusion is valid.
- The attacked vertex \(r\) is outside \(B\), and \(r\ne x\) because
  \(rp\) is an edge while \(xp\) is not.
- The missed vertex \(y\) is outside \(C_p=\{u,r,q\}\).  It is not \(p\)
  because \(yr\) is absent while \(pr\) is present, and it is not \(x\)
  because \(yp\) is present while \(xp\) is absent.
- Symmetrically, \(z\) is outside \(C_q=\{u,p,r\}\), is not \(q\)
  because \(zr\) is absent while \(qr\) is present, and is not \(x\)
  because \(zq\) is present while \(xq\) is absent.
- Finally \(y\ne z\), since \(yp\) is present and \(zp\) is absent.

This exhausts every pair among the seven names.  Consequently every later
named target is genuinely unoccupied, and every displayed three-set has
cardinality three.

## 4. Private-witness completion lemma

Fix \(g\in\{p,q\}\), let \(t\) be the other endpoint, and let \(y_g\)
miss both \(u\) and \(t\).  The pair \(\{u,y_g\}\) is independent.
Because \(i(G)=3\), it is not a maximal independent pair; because
\(\alpha(G)=3\), it extends to an independent triple
\[
 I=\{u,y_g,s\}.
\]
C-010 puts \(I\) in the greatest family.  The active edge \(ux\) ensures
\(x\notin I\), and C-108 transports \(u\to x\), retaining
\[
 J=\{x,y_g,s\}.
\]

The completion split in the candidate is exact.

- If \(s=t\), then \(J=\{x,y_g,t\}=M_g\) directly.
- The case \(s=g\) is impossible, because the private-witness edge
  \(gy_g\) would violate independence of \(I\).
- If \(s\ne t\), then \(t\) is unoccupied in \(J\).  Both \(x\) and
  \(y_g\) miss \(t\).  Since retained \(J\) dominates \(t\), necessarily
  \(st\in E(G)\), and \(s\) is the unique eligible responder.  Eternal
  closure therefore retains \(J-s+t=M_g\).

The inference \(st\in E(G)\) comes from domination of a retained state,
not from a missing transition.  Potential collisions of \(s\) with the
other named vertices are harmless: independence rules out \(x\) and
\(g\); if \(s\) is another allowed named vertex such as \(r\) or the
other witness, its forced edge to \(t\) gives exactly the same unique
one-guard response.  The clean-room checker explicitly exercised every
allowed named collision.

For \(g=q,t=p,y_g=z\), this proves the retained state
\[
 M_q=\{x,p,z\}.
\]

## 5. Exhaustive audit of the attack at \(y_p\)

The witness \(y=y_p\) is unoccupied in \(M_q\).  Its only possible
responders are the three guards \(x,p,z\), and the proof rejects all
three without assuming an absent move edge.

### Responder \(z\)

If \(zy\in E(G)\), its successor is
\[
 A=\{x,p,y\}.
\]
The unoccupied vertex \(q\) misses every guard:
\[
 qx,qp,qy\notin E(G).
\]
Thus \(A\) is non-dominating and cannot be retained.  If \(zy\) is
absent, \(z\) is simply ineligible.

### Responder \(p\)

The private edge \(py\) is present, so this successor always exists:
\[
 W=\{x,y,z\}.
\]
Attack the unoccupied vertex \(u\).  Both private witnesses miss \(u\),
while \(ux\) is present, so \(x\) is the unique eligible responder.  It
lands in
\[
 H=\{u,y,z\}.
\]
The distinct unoccupied vertex \(r\) misses all of \(u,y,z\), so \(H\)
is non-dominating.  Hence \(W\) has no retained answer at \(u\) and
cannot belong to the eternal family.

### Responder \(x\)

If \(xy\in E(G)\), its successor is
\[
 X=\{p,y,z\}.
\]
At the unoccupied target \(u\), the witnesses \(y,z\) are ineligible.
If \(pu\) is absent, there is no mover.  If \(pu\) is present, \(p\) is
the only mover and again lands in the non-dominating state \(H\).
Therefore \(X\) is not retained.  If \(xy\) is absent, \(x\) is
ineligible at the original attack.

These are all guards of \(M_q\).  The always-eligible \(p\)-move and
every optional \(x\)- or \(z\)-move lead outside the family.  This
contradicts closure of the retained state \(M_q\) at the unoccupied
attack \(y\).

Every transition above moves exactly one occupied guard along one
\(G\)-edge.  The proof never converts `not retained` into `nonadjacent`:
\(W\) and \(X\) are excluded by explicit later attacks, while \(A\) and
\(H\) are excluded by explicit missed vertices.

## 6. Clean-room finite bookkeeping

`independent_check.py` shares no code with the candidate.  Instead of
starting from a hand-selected optional-pair list, it scans all
\[
 2^{\binom72}=2{,}097{,}152
\]
simple graphs on the seven named vertices and filters the literal edge
and nonedge hypotheses.  It finds exactly 64 assignments:

| row | assignments |
|---|---:|
| QQ0 | 32 |
| AQ0 | 32 |

The four possible first-mover sets
\[
 \{p\},\quad\{p,x\},\quad\{p,z\},\quad\{p,x,z\}
\]
occur 16 times each.  Across the 64 assignments it checks 64 \(p\)
branches, 32 \(x\) branches, 32 \(z\) branches, 256 allowed named
completion collisions, and the exact \(s=t\) versus \(s\ne t\) split.
There were no failures.

The checker is evidence for finite incidence bookkeeping only.  The
family-forcing content of C-010, C-108, and C-150 was audited
mathematically above.

## 7. Reproduction

From `gamma_theta_eternal_domination/`:

```text
sh math/working/rank_one_remaining_endgame/verify_strict.sh
sh reviews/rank_one_qqaq0_hostile/verify_review.sh
```

Both commands return `PASS` with an exact byte comparison against their
frozen expected result.

## 8. Final accept/reject table

| item | decision |
|---|---|
| rank-one interpretation and two private witnesses | **ACCEPT** |
| all seven named vertices distinct | **ACCEPT** |
| completion lemma, with direct case \(s=t\) | **ACCEPT** |
| claim that \(s=g\) is impossible | **ACCEPT** |
| C-010 and C-108 use | **ACCEPT** |
| \(z\)-response at the attack on \(y_p\) | **ACCEPT** |
| \(p\)-response and terminal state \(H\) | **ACCEPT** |
| \(x\)-response, including both values of \(pu\) | **ACCEPT** |
| independence from the value of \(xr\) | **ACCEPT** |
| no omitted-family-to-nonedge inference | **ACCEPT** |
| rank-one QQ0 exclusion | **PROVED / ACCEPT** |
| rank-one AQ0 exclusion | **PROVED / ACCEPT** |
| discovery-only finite SAT claims | **NOT REVIEWED / NOT USED** |
| QQ1, AQ1, higher ranks, reciprocity, complete \(k=3\), conjecture | **OPEN / NOT CLAIMED** |
