# Hostile review: rank-one XQ1 endgame

Review date: 2026-07-28 PDT

Frozen candidate commit:
`fab045f4a90cfabf19f953b09d0e874735e6f5a9`

## Verdict

**UNCONDITIONAL PASS on the frozen candidate.**

The theorem in
`math/working/rank_one_xq1_endgame/NOTE.md` is correct at its stated
scope:

> Under
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\), for the literal greatest
> eternal triple-family, a one-sided active edge cannot have a rank-one
> XQ1 reverse-endpoint collision of the accepted C-150 type.

I found no named-vertex collision, missing adjacency, use of C-064 at an
exchanged or occupied target, use of C-108 outside an independent
vertex-star, illegal attack, multi-guard response, wrong successor, or
hidden complement reversal.  No correction to the candidate is required.

This eliminates only the rank-one XQ1 row.  It does not eliminate the
other rank-one rows, any higher-rank collision, prove active-edge
reciprocity, complete parameter three, or resolve the gamma--theta
conjecture.

## Frozen objects and accepted dependencies

| Object | SHA-256 |
|---|---|
| candidate `NOTE.md` | `ddb77704f2edad1cec7ff95629b34b56ed4182d211fc26089f69bc2a9b7bbf06` |
| candidate `MANIFEST.json` | `856470d7742221146ac845ff102644a732d10ae4115a1c7441e3829507edb34b` |
| candidate `verify_implication.py` | `dd4b26a9fbc717901b9211a53ffe57275a59b865d3621ad3d6055f893158e6be` |
| candidate `expected_result.json` | `8eb1195eeb68749c244b5a000c32dc1d8ec3491bfc6cbe5f7abee478b3dc6cb3` |
| C-064 source | `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7` |
| C-064 hostile review | `bc5011d85d333fb66fce3ea563e4cc80cf016090cc3427e44187b2e40fb5f9f8` |
| C-108 source | `d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8` |
| C-108 hostile review | `5044df431a67fce050bb602c6f0510c9acbdeec2b90de0d1aaeb1c1ffed62a2e` |
| C-150 source | `acfbc262877c08f9e4b38aa38931c3b95699b50073aa9a67d8ac3f80ba9ba3fd` |
| C-150 hostile review manifest | `146ea579ee944d94d635063ee820975eab1a69849ca1e139fe1a7beb57609bb4` |

I read the complete source and hostile review for every accepted dependency
actually invoked.

- C-064 transports the complete family-response list across two retained
  independent \(k\)-states sharing a ridge.  At an outside target fixed by
  the exchanged transposition, the list is transported by that
  transposition.
- C-108 makes the ability of a fixed shared guard \(u\) to answer a fixed
  target \(x\) uniform across all retained independent \(k\)-states
  containing \(u\) and avoiding \(x\).
- C-150 supplies the rank-one XQ1 private witnesses, all named incidences
  used here, and the four retained independent facets.  Its final hostile
  review passed after the earlier scope errata were incorporated into the
  accepted source bytes.

No stronger version of any dependency is used.

## 1. Complete incidence and collision audit

Write

\[
T=\{x,p,q\},\qquad B=\{u,p,q\}.
\]

For the XQ1 deleting attack \(r\), the accepted data are

\[
N(r)\cap T=\{x,p\},\qquad ur\in E(G).
\]

The rank-one successors obtained by moving \(p\) and \(u\) are
non-dominating.  Their C-150 private witnesses \(y=y_p\) and \(z=y_u\)
satisfy

\[
\begin{aligned}
&py\in E(G), && yu,yr,yq\notin E(G),\\
&uz\in E(G), && zr,zp,zq\notin E(G),
\end{aligned}
\]

and C-150 further supplies

\[
xy,xz,yz\in E(G).
\]

Together with the active edge, the XQ1 row, and independence of \(T\),
these facts classify every pair among

\[
u,x,p,q,r,y,z.
\]

There are exactly nine forced edges, ten forced nonedges, and two
undetermined pairs:

\[
\begin{array}{c|ccccccc}
 &u&x&p&q&r&y&z\\ \hline
u&-&1&?&?&1&0&1\\
x&1&-&0&0&1&1&1\\
p&?&0&-&0&1&1&0\\
q&?&0&0&-&0&0&0\\
r&1&1&1&0&-&0&0\\
y&0&1&1&0&0&-&1\\
z&1&1&0&0&0&1&-
\end{array}
\]

The only optional pairs are \(up\) and \(uq\).

All seven names are genuinely distinct.  The state and attack definitions
separate \(u,x,p,q,r\); in particular the displayed edge \(xr\) also
separates \(r\) from \(x\).  The witness \(y\) lies outside
\(\{u,r,q\}\), cannot equal \(p\) because \(yr\) is absent while \(pr\)
is present, and cannot equal \(x\) because \(yp\) is present while \(xp\)
is absent.  Similarly \(z\) lies outside \(\{r,p,q\}\), cannot equal
\(u\) because \(zr\) is absent while \(ur\) is present, and cannot equal
\(x\) because \(zr\) is absent while \(xr\) is present.  Finally
\(y\ne z\) because \(yp\) is present and \(zp\) is absent.

## 2. Both C-064 applications are in exact scope

The relevant retained ladder is

\[
\begin{aligned}
J_y&=\{y,r,q\},\\
J_z&=\{z,r,q\},\\
K_z&=\{z,p,q\},\\
T&=\{x,p,q\}.
\end{aligned}
\]

Every displayed state is independent.  At the unoccupied target \(y\)
from \(J_z\), the adjacency pattern is

\[
yz\in E(G),\qquad yr,yq\notin E(G).
\]

Thus \(z\) is the only adjacency-eligible guard, and its successor is the
retained state \(J_y\).  This proves the physical exact list

\[
L_{J_z}(y)=\{z\}
\]

without using covariance.

The first C-064 application compares \(J_z\) and \(K_z\).  They share
\(\{z,q\}\), exchange \(r\leftrightarrow p\), and \(y\) lies outside both
states and is fixed by that transposition.  It gives

\[
L_{K_z}(y)=\{z\}.
\]

The second application compares \(K_z\) and \(T\).  They share
\(\{p,q\}\), exchange \(z\leftrightarrow x\), and again \(y\) lies outside
both and is fixed.  Therefore

\[
\boxed{L_T(y)=\{x\}}.
\]

There is no invocation at the exchanged target and no undefined
response-list evaluation.  The \(x\)-successor is

\[
T-x+y=\{y,p,q\}\in\mathcal K,
\]

whereas the exact omitted \(p\)-successor is

\[
\boxed{M=T-p+y=\{x,y,q\}\notin\mathcal K}.
\]

The guard \(q\) is not another possible responder because \(qy\) is a
nonedge.

## 3. Maximal-independent completion and C-108 scope

The equality hypotheses and the parameter chain give

\[
3=\gamma(G)\le i(G)\le\alpha(G)=3,
\]

so \(i(G)=3\).  Since \(uy\) is a nonedge, extend \(\{u,y\}\) to a
maximal independent set.  It can have neither two vertices, by \(i=3\),
nor more than three, by \(\alpha=3\).  Hence it is exactly

\[
I=\{u,y,s\}.
\]

It is a maximum independent set, so it belongs to the greatest eternal
family.  The active edge \(ux\) ensures \(x\notin I\).  Thus the C-108
vertex-star hypotheses are exact: \(I\) is retained and independent,
contains the responder \(u\), and avoids the target \(x\).  The assumed
orientation \(u\triangleright x\) therefore retains

\[
P=I-u+x=\{x,y,s\}.
\]

No claim that \(P\) is independent is made or needed.

The named collision audit for \(s\) is exhaustive.  It cannot equal
\(x,p,r,z\), since those vertices are adjacent to \(u\) or \(y\), and it
cannot equal \(u\) or \(y\) because it is the third set member.  The only
possible named collision is \(s=q\).

- If \(s=q\), then \(P=M\), contradicting the exact omission above.
- If \(s\ne q\), then \(q\) is unoccupied in \(P\).  Since \(P\) is a
  retained dominating state while \(qx,qy\) are nonedges, domination of
  \(q\) forces \(qs\in E(G)\).  At the attack on \(q\), neither \(x\) nor
  \(y\) has a move edge.  The guard \(s\) is the unique eligible responder,
  so one-guard closure forces exactly
  \[
  P-s+q=\{x,y,q\}=M\in\mathcal K,
  \]
  again a contradiction.

The last move attacks an unoccupied vertex, moves exactly one occupied
guard, follows the forced edge \(sq\), and produces exactly the state
previously proved absent.  This closes every completion case.

## 4. Clean-room finite bookkeeping audit

The independent checker in this review directory imports no candidate
module, campaign evaluator, graph library, or solver.  It reconstructs
the nine/two/ten pair partition from separately grouped primitive
incidences, verifies all four independent ladder states, and applies fresh
ordinary-set transpositions.

It checks explicitly that \(y\) is outside both states in each C-064
application.  It then exhausts:

- all four choices of the optional named edges \(up,uq\);
- every possible named completion of \(\{u,y\}\); and
- all 128 local edge patterns for an external completion \(s\), including
  all four optional named-edge patterns.

Exactly 64 external patterns allow the retained state
\(\{x,y,s\}\) to dominate \(q\); all 64 force \(sq\), make \(s\) the
unique response to the unoccupied attack at \(q\), and produce \(M\).
The checker result is byte-for-byte reproducible.

The candidate strict checker also passes unchanged.  Its stdout is
identical to `expected_result.json`, SHA-256
`8eb1195eeb68749c244b5a000c32dc1d8ec3491bfc6cbe5f7abee478b3dc6cb3`.

The candidate's CaDiCaL runs are correctly labeled `OBSERVED` and are not
used in this verdict.

## 5. Reproduction commands

From the campaign repository root:

```text
gamma_theta_eternal_domination/math/working/rank_one_xq1_endgame/verify_strict.sh

python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/rank_one_xq1_endgame_hostile/independent_check.py \
  | cmp -s - \
  gamma_theta_eternal_domination/reviews/rank_one_xq1_endgame_hostile/independent_result.json
```

Both commands exit with status zero.

## Exact status boundary

| Status | Content |
|---|---|
| `PROVED` | the rank-one XQ1 collision is impossible under the stated equality, greatest-family, and one-sided-active-edge hypotheses |
| `CHECKED` | complete named pair/collision table; both C-064 domains and transpositions; exact omitted successor; all named and external completion cases |
| `OBSERVED` | the candidate's uncertified finite SAT UNSAT runs; not used in the proof |
| `OPEN` | the other rank-one rows, all higher-rank collisions, reciprocity, complete \(k=3\), and the universal conjecture |
