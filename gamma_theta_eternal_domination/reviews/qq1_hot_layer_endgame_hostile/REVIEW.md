# Hostile review: retained QQ1 hot layer and outer bow-ties

Date: 2026-07-28 (PDT)

Candidate commit:
`b8ef2d4ddbfd5edd57c5e865c8a7ebf60f2f776c`

## Verdict

\[
\boxed{\textbf{UNCONDITIONAL PASS}}
\]

I independently reconstructed the canonical QQ1 incidence from accepted
C-158, checked every attack and every vertex collision in the candidate,
and wrote a clean-room bitset evaluator that imports neither candidate
code nor a campaign verifier.  I found no mathematical error, occupied
attack, extra guard move, missing eligible responder, hidden freshness
assumption, complement confusion, or inference from a missing family state
to a graph nonedge.

The candidate proves the following exact result.

> Assume
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\), let \(\mathcal K\)
> be the literal greatest family of dominating triples, and assume the
> accepted C-158 canonical rank-one QQ1 normal form.  For every
> \(x,r\)-completion \(d\), the state
> \(A=\{u,x,d\}\) is retained.  The common-nonneighbor set \(W_d\) of
> \(u,d\) is nonempty and is a \(G\)-clique.  Every member of \(W_d\)
> hits \(x,r\) and a side witness fixed by the retained response list at
> \(d\).  For each \(w\in W_d\), the five states
> \(I,A,K_w,E_w,F_w\) are retained and the sixth state
> \(O=\{u,r,d\}\) is omitted.  For every maximum-independent completion
> \(s\) of \(\{u,w\}\) and \(t\) of \(\{d,w\}\), the mixed state
> \(\{s,w,t\}\) is retained.  Consequently every nondegenerate outer
> pair \(s,d\) and \(t,u\) is active in both directions.

This does **not** eliminate either inner branch \(ud\notin E(G)\) or
\(ud\in E(G)\).  It does not eliminate canonical QQ1, prove
greatest-family reciprocity, complete \(k=3\), or resolve the
\(\gamma\)--\(\theta\) conjecture.

## 1. Frozen candidate and dependency boundary

The reviewed candidate bytes have these SHA-256 hashes:

| artifact | SHA-256 |
|---|---|
| `CANDIDATE_MANIFEST.json` | `9076ab509b24a9c9c8a36c7badc3d2a0f27906e5b967a1dbe825bf01924e80cd` |
| `NOTE.md` | `a7d9edb6e09354b8ce941377a0840ffa99c27315f9968ddee09395ed2c70a506` |
| `RESEARCH_LOG.md` | `94c846b8fdb61784719184cb54e8c651cbd4aa9195d3067dbbd54a43b54d7707` |
| `expected_result.json` | `eeaf6f78a778e2e85919f52bd4bda175b9bd7cb0d6ef4472503536f720d9a2c0` |
| `verify_implication.py` | `37a2e64807978ecd8c93641e449f7f66679e03a6f0582b81b0d3b3cc71c502e1` |
| `verify_strict.sh` | `4ebb0d778814edeea49ad4a6003bbe7a99a387bb8161b9119450f587524202e8` |

The mathematical dependencies and their exact uses are:

1. **C-010:** every independent triple is retained.
2. **C-108:** activity is uniform across independent triples containing
   the responder; this retains \(E_w\) directly when \(ud\) is a
   nonedge and transports \(u\to x\) in the edge-branch completion
   proof.  It also turns the original failure \(x\not\triangleright u\)
   into omission of \(O\).
3. **C-143:** the reverse state \(O=\{u,r,d\}\) dominates.  Its
   domination, not family retention, forces \(db,dc\).
4. **C-145:** only identifies the \(ud\)-nonedge inner geometry as the
   accepted repair square.  It is not needed for the new retained-corner
   or outer-bow-tie proofs.
5. **C-158:** supplies the exact canonical core, retained state
   \(U=\{u,b,c\}\), and the \(x,r\)-completion clique complete to
   \(p,q\).

The new proofs need no finite-order assertion and no unproved symmetry
principle.  C-161 is interpretive only after the nonedge-branch repair
square has been constructed.

## 2. Canonical incidence and distinctness

Write

\[
T=\{x,p,q\},\qquad B=\{u,p,q\}.
\]

The accepted core is

\[
\begin{aligned}
E_G\supseteq{}&
\{ux,ur,pr,qr,pb,qc,xb,xc,bc,up,uq\},\\
\overline E_G\supseteq{}&
\{xp,xq,pq,xr,bu,br,bq,cu,cr,cp\}.
\end{aligned}
\]

For \(d\in C_{xr}\), one has \(dx,dr\notin E(G)\) and
\(dp,dq\in E(G)\).  Accepted C-143 applies to the independent state

\[
I=\{x,r,d\}
\]

and the active edge \(u\triangleright x\), so

\[
O=\{u,r,d\}
\]

dominates.  Since \(u,r\) both miss each of \(b,c\), this forces

\[
db,dc\in E(G).
\]

These incidences exclude all collisions of \(d\) with the seven core
vertices:

- \(d\ne u\), since \(u\) hits \(x,r\);
- \(d\ne p,q\), since \(p,q\) hit \(r\);
- \(d\ne b,c\), since \(b,c\) hit \(x\).

Thus every later attack at \(d\) is genuinely unoccupied.

If \(w\in W_d\), then \(w\) misses \(u,d\).  The fixed edges above
exclude \(w=x,p,q,r,b,c\), so \(w\) is also external to the named core
and distinct from \(d\).

## 3. Retention of \(A=\{u,x,d\}\)

Attack the unoccupied vertex \(d\) from the accepted retained state

\[
U=\{u,b,c\}.
\]

The guards \(b,c\) are eligible because \(db,dc\) are edges.  If \(u\)
is eligible, its successor \(\{d,b,c\}\) misses \(r\).  Therefore at
least one side response survives:

\[
D_b=\{u,d,c\}\in\mathcal K
\quad\text{or}\quad
D_c=\{u,b,d\}\in\mathcal K.
\]

From \(D_b\), attack the unoccupied vertex \(x\).  The guard \(d\) is
ineligible.  The \(u\)-successor \(\{x,d,c\}\) misses \(r\), so closure
forces \(c\to x\) and reaches \(A\).  From \(D_c\), the symmetric attack
forces \(b\to x\) and reaches the same \(A\).

This proves \(A\in\mathcal K\) without assuming an edge \(ud\), and it
does not use a missing family transition as a graph nonedge.

The retained side list

\[
\Lambda_d=
\{b:D_b\in\mathcal K\}\cup
\{c:D_c\in\mathcal K\}
\]

is nonempty.  If \(D_b\) is retained, every vertex missing \(u,d\) must
hit \(c\); if \(D_c\) is retained, every such vertex must hit \(b\).
Thus one side is uniform over all of \(W_d\), and both sides are uniform
if both responses survive.  The clean-room symbolic audit checks all
three nonempty response lists and their five compatible single-witness
incidence patterns.

## 4. The hot set and the five retained corners

The equality \(\gamma(G)=3\) means the pair \(\{u,d\}\) cannot
dominate, so \(W_d\ne\varnothing\).

For \(w\in W_d\):

- retained \(A\) forces \(wx\in E(G)\);
- dominating \(O\) forces \(wr\in E(G)\);
- retained \(U\) and the side-list argument give the uniform side edge.

Define

\[
K_w=\{u,d,w\},\quad
E_w=\{x,d,w\},\quad
F_w=\{r,d,w\}.
\]

The attack at \(w\) from \(A\) has exactly one eligible guard, \(x\), so
it retains \(K_w\).  At the attack \(r\) from \(K_w\), the \(w\)-move
lands in the omitted state \(O\), \(d\) is ineligible, and closure
forces \(u\to r\), retaining \(F_w\).  At the attack \(x\) from \(F_w\),
only \(w\) is eligible and the response returns to \(I\).

The proof of \(E_w\) must split at \(ud\), and the candidate does so
correctly.

### 4.1 \(ud\) a nonedge

Then \(K_w\) is independent.  C-108 applies to the independent source
and the known activity \(u\triangleright x\), retaining

\[
K_w-u+x=E_w.
\]

### 4.2 \(ud\) an edge

Here \(K_w\) is not independent, so it cannot source a C-108 activity
claim.  Extend the independent pair \(\{u,w\}\) to

\[
S_s=\{u,w,s\}.
\]

Well-coveredness supplies a triple, and \(s\ne d\) because \(su\) is a
nonedge while \(du\) is an edge.  C-108 retains

\[
D_s=S_s-u+x=\{x,w,s\}.
\]

The retained state \(D_s\) must dominate \(d\).  Its guards \(x,w\)
miss \(d\), hence \(sd\) is an edge.  At the unoccupied attack \(d\)
from \(D_s\), only \(s\) is eligible, and the unique response is
\(E_w\).  This is a valid separate proof; no response direction is read
from the non-independent state \(K_w\).

The five retained states are therefore

\[
I,\ A,\ K_w,\ E_w,\ F_w,
\]

while \(O\) remains omitted by \(x\not\triangleright u\) at the
independent source \(I\).

All activity relations asserted before invoking C-145 have independent
sources:

\[
\begin{array}{c|c}
\text{direction}&\text{independent source}\\ \hline
x\triangleright w&I\\
r\triangleright w&I\\
r\triangleright u&I\\
w\triangleright x&K_w\quad(ud\notin E(G))\\
u\triangleright r&K_w\quad(ud\notin E(G)).
\end{array}
\]

In particular, the edge branch never infers reverse activity merely
from a transition out of \(K_w\).

Finally, if \(w,y\in W_d\) are distinct, retained \(K_w\) dominates
\(y\).  The guards \(u,d\) both miss \(y\), so \(wy\in E(G)\).
Therefore \(W_d\) is a \(G\)-clique.

## 5. Completion-set audit

For fixed \(w\), put

\[
\begin{aligned}
\mathcal S_w&=\{s:su,sw\notin E(G)\},\\
\mathcal T_w&=\{t:td,tw\notin E(G)\},
\end{aligned}
\]

with the two underlying pair vertices excluded as in the candidate.

Both sets are nonempty: each underlying independent pair extends to a
maximal independent set, and \(i=\alpha=3\) makes every such extension
a triple.  Each set is a \(G\)-clique, since two nonadjacent completions
would create an independent four-set.

They are disjoint.  A common member would miss all three guards of the
retained state \(K_w\), contradicting domination.

Domination by \(K_w\) also gives

\[
sd\in E(G)\quad(s\ne d),\qquad
tu\in E(G)\quad(t\ne u).
\]

The only possible collisions of \(s\) with the canonical core are
\(s=b,c\), and additionally \(s=d\) when \(ud\) is a nonedge.  The only
possible collision of \(t\) with the core is \(t=u\), again only when
\(ud\) is a nonedge.  All other named collisions are excluded by a
fixed edge to one member of the corresponding independent pair.

## 6. Complete omitted-bow-tie attack tree

Assume for contradiction that

\[
Q_{s,t}=\{s,w,t\}\notin\mathcal K.
\]

Start from \(U=\{u,b,c\}\) and attack \(r\).  Only \(u\) is eligible, so

\[
R=\{r,b,c\}\in\mathcal K.
\]

Attack \(w\) from \(R\).  The \(r\)-successor
\(\{w,b,c\}\) misses \(u\).  Hence a side guard moves and at least one
of

\[
\{r,b,w\},\qquad\{r,c,w\}
\]

is retained.

### 6.1 Side collisions \(s=b\) or \(s=c\)

If \(s=b\), then \(bw\) is a nonedge by definition of
\(\mathcal S_w\).  The \(b\to w\) branch is graph-ineligible, so closure
forces \(c\to w\), landing directly in

\[
Y=\{r,b,w\}=\{r,s,w\}.
\]

The attack at \(s\) must be skipped because \(s\) is already occupied.
The case \(s=c\) is symmetric.  The candidate handles both collisions
explicitly.

### 6.2 \(s\) outside the side witnesses

From either retained side state, attack the unoccupied vertex \(s\).
The guard \(w\) is ineligible.  An \(r\)-move, if the edge exists,
lands in a state whose three guards all miss \(u\).  Closure therefore
forces the remaining side guard to \(s\), producing the same retained
state

\[
Y=\{r,w,s\}.
\]

This also covers \(s=d\).  In that endpoint case \(r\) and \(w\) are
both graph-ineligible at \(d\), while the four-hit completion edges make
the side response eligible.

### 6.3 Final attack

Attack the unoccupied vertex \(t\) from \(Y\).  It is unoccupied because
\(\mathcal S_w\cap\mathcal T_w=\varnothing\), and \(t\ne r,w\).
The guard \(w\) is ineligible.  An \(r\)-move, if graph-eligible, lands
in the assumed omitted state \(Q_{s,t}\).  The only other possible
successor is

\[
\{r,w,t\},
\]

which misses \(d\).  Thus no retained response exists, contradicting
retention of \(Y\).

The clean-room checker exhausts all 16 abstract alias branches:

- both values of \(ud\);
- \(s=b,c,d\), or fresh when permitted;
- \(t=u\) or fresh when permitted;
- both possible retained side branches for a noncollision \(s\).

Six branches use the \(s=b,c\) occupied-target shortcut.  Eight contain
an endpoint degeneracy.  In the degeneracies the conclusion is even
more immediate:

\[
\begin{array}{c|c}
s=d&Q_{s,t}=J_t\in\mathcal K,\\
t=u&Q_{s,t}=S_s\in\mathcal K,\\
s=d,\ t=u&Q_{s,t}=K_w\in\mathcal K.
\end{array}
\]

No step of this attack tree uses the value of \(ud\), C-145, covariance,
or a graph nonedge inferred from family omission.

## 7. Outer reciprocity

For \(s\in\mathcal S_w\), \(s\ne d\), the edge \(sd\) was forced by
domination of \(K_w\).  Both directions have independent sources:

\[
S_s-s+d=K_w,\qquad
J_t-d+s=Q_{s,t}.
\]

Since \(\mathcal T_w\) is nonempty, the second witness always exists.
Thus \(s\leftrightarrow d\).

Similarly, for \(t\in\mathcal T_w\), \(t\ne u\),

\[
J_t-t+u=K_w,\qquad
S_s-u+t=Q_{s,t}
\]

prove \(t\leftrightarrow u\).  Nonemptiness of
\(\mathcal S_w\) supplies the second source.  All four source states are
independent.  The excluded endpoint cases are exactly those in which the
two vertices coincide with the opposite completion endpoint.

## 8. Independent fixed-control reconstruction

The clean-room verifier implements:

- a separate short-graph6 decoder;
- exhaustive exact \(\gamma,i,\alpha\);
- DSATUR coloring of the complement for \(\theta\);
- simultaneous greatest-fixed-point deletion for one-guard kernels and
  deletion ranks;
- an independent activity-star consistency check.

It reproduces:

| graph6 | \((n,m)\) | \((\gamma,i,\alpha,\gamma^\infty,\theta)\) | \(|\mathcal K_3|\) |
|---|---:|---:|---:|
| `Mslamztl~fnny~]~_` | \((14,67)\) | \((2,3,3,3,3)\) | 284 |
| `NslalntvXzn^{~n\|\|^w` | \((15,78)\) | \((2,3,3,3,3)\) | 285 |
| `Oslally^v{zn{~y~nn~j~` | \((16,91)\) | \((2,3,3,3,3)\) | 439 |

For each graph the two-guard greatest family is empty.  The first two
controls have unique \(x,r\)-completions \(d=9,7\), respectively,
\(W_d=\varnothing\), and rank vector

\[
(\rho(B),\rho(P_d),\rho(Q_d),\rho(O))=(1,2,2,3).
\]

The new edge control has

\[
d=7,\quad w=8,\quad
\mathcal S_w=\{5,9\},\quad
\mathcal T_w=\{10\},\quad ud\in E(G).
\]

It retains all 13 audited named states, including both mixed states
\(\{5,8,10\}\) and \(\{9,8,10\}\).  Exactly the side state
\(\{u,d,c\}\) survives among the two displayed side responses, agreeing
with \(wb=0,wc=1\).  It has

\[
(\rho(B),\rho(O))=(1,3)
\]

and 34 dominating pairs.

All three graphs have \(\gamma=2\).  They are sharp boundary controls
only.  They are not equality graphs for this theorem, are not
counterexamples, and cannot be used to prove any universal assertion.

## 9. Final scope decision

The candidate closes the proposed *outer omitted bow-tie* branch, but
both inner QQ1 branches survive:

1. when \(ud\) is a nonedge, the accepted C-145 square remains with its
   literal omitted corner and conserved rank;
2. when \(ud\) is an edge, the five-corner retained configuration remains
   and is realized locally by the gamma-two boundary control.

The correct next theorem must use global \(\gamma=3\) information to
couple a saturated outer layer back to the original rank-one omission.
No stronger conclusion is licensed by this review.
