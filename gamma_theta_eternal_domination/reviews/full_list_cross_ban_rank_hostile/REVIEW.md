# Hostile review: trapped full-list witness escape

## Verdict

**UNCONDITIONAL PASS**

Review date: 2026-07-28 PDT

Candidate commit:

```text
2a49be9355261175f81f9c28f9be13f010ea2709
```

Candidate package:

```text
math/working/full_list_cross_ban_rank/
```

I independently reconstructed Theorem 2.1 and Corollary 2.2 from the
literal one-guard definition and the accepted C-149, C-157, and C-168
inputs.  Every attack is at an unoccupied vertex, every response moves
exactly one guard along an established edge, and every appeal to
retention is an appeal to closure of the same unrestricted greatest
family.  The restricted rank-zero semantics are correct.  The arbitrary
missed-witness quantifier and the full-terminal polarization are valid.
No missing palette entry or omitted family response is converted into a
graph nonedge.

The MMV-027 boundary control was then recomputed in a clean-room verifier
using integer masks and no campaign evaluator or candidate code.  It
matches every theorem-relevant parameter, family, palette, attack,
restricted kernel, and rank claimed in the candidate.

This verdict promotes only the stated trapped-witness escape and its
polarization corollary, together with the exact gamma-two sharpness
control.  It does **not** prove a surviving color-restricted kernel,
complete the parameter-three case, or resolve the gamma--theta
conjecture.

## 1. Exact dependency audit

The candidate names C-149, C-157, C-163, C-165, and C-168.  The proof of
Theorem 2.1 actually needs only the following accepted inputs:

1. **C-149:** the color-\(u\) restricted universe begins with every
   dominating triple outside
   \(\mathcal B_u(x)=\{S-u+b:b\in N_{\overline G}(x)\}\); the named
   nonroot corridor has \(q\notin S\cup B\cup\{x,r\}\) and the
   \(G\)-diamond on \(\{x,u,q,r\}\), with only \(xr\) missing.
2. **C-157:** for a secondary color \(v\in Q(r)-\{u\}\), the physical
   alternate \(A_v=\{t,q,r\}\) is unbanned and nondominating.  Every
   missed witness \(w\) satisfies
   \(vw\in E(G)\), \(wt,wq,wr\notin E(G)\), and
   \(w\notin S\cup\{x,q,r\}\).
3. **C-168:** the same witness also satisfies \(uw\in E(G)\), and the
   two unique attacks retain \(\{w,t,q\}\) and \(\{w,t,r\}\).

C-163 and C-165 are harmless background citations but are not logical
dependencies of the new theorem or corollary.

The accepted source hashes match the candidate manifest exactly:

```text
C-149  a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d
C-157  0497d07b8cf2bf1f5e3572f35d400d954745abae4490e6cac707f15cbcaeb22c
C-163  e25845bbf5e23886284f2046ac8c5c661b48176f4bef9fda5651f733d4a0edb0
C-165  fc407cb436bfd48f1eb26123cbe02ad1318f4a8a3a8cdee02a48064362261b9d
C-168  3d0e38493159d69b6d790b9614253e02f92ab7acbf5acf7a54dc003f7f10bb87
```

## 2. Independent proof reconstruction

Write

\[
S=\{u,v,t\},\quad
T=\{v,t,q\},\quad
E=\{v,t,r\},\quad
B=N_{\overline G}(x).
\]

The state \(T\) has restricted deletion rank zero for the color-\(u\)
ban, its deleting attack is \(r\in B\), and its selected unrestricted
response is \(q\to r\), ending at the retained but banned state \(E\).
Fix \(v\in Q(r)-\{u\}\).  Let \(w\) be an arbitrary missed witness for
the C-157 alternate \(\{t,q,r\}\), and assume \(w\in B\).

### 2.1 The first forced state and the edge \(tr\)

Fullness of \(x\) retains

\[
X_u=S-u+x=\{v,t,x\}.
\]

At the unoccupied attack \(w\), the guards \(t,x\) miss \(w\), while
\(v\) hits \(w\).  Thus \(v\to w\) is the unique response and

\[
M=\{w,t,x\}\in\mathcal F^\star.
\]

The retained state \(M\) dominates \(r\).  Both \(w\) and \(x\) miss
\(r\), respectively because \(w\) misses the C-157 alternate and
\(r\in B\).  Therefore \(tr\in E(G)\).

### 2.2 The rank-zero alternate is nondominating

At the original attack \(r\) from \(T\), the newly established edge
\(tr\) makes

\[
t\to r,\qquad H=\{v,q,r\}
\]

a physical response.  It is unbanned: every color-\(u\) banned state
contains the fixed pair \(\{v,t\}\), whereas \(H\) contains \(q\notin S\)
in place of \(t\).

The rank convention is crucial and is used correctly.  The initial
restricted universe is exactly

\[
\mathcal U_u^0=
\{D:|D|=3,\ D\text{ dominates }G,\ D\notin\mathcal B_u(x)\}.
\]

Rank zero means that the deleting attack \(r\) has no physical successor
in \(\mathcal U_u^0\).  If \(H\) dominated, its being unbanned would put
it in \(\mathcal U_u^0\), a contradiction.  Hence \(H\) is
nondominating.

This step uses neither the unrestricted deletion rank of \(H\) nor a
palette inference.  It is simply the definition of the first
synchronous restricted-deletion round.

### 2.3 Every missed vertex of \(H\)

Let \(y\) be **any** vertex missed by \(H\).  Then

\[
yv,yq,yr\notin E(G).
\]

The retained predecessor \(T=\{v,t,q\}\) dominates \(y\), so \(ty\) is
an edge.  The distinctness audit is complete:

- \(y\notin\{v,q,r\}\), because \(y\) is missed by that closed
  neighborhood;
- \(y\ne t\), because \(tr\) is an edge;
- \(y\ne u\), because the corridor diamond gives \(uq,ur\in E(G)\);
- \(y\ne x\), because the corridor diamond gives \(xq\in E(G)\);
- \(y\ne w\), because C-157 gives \(vw\in E(G)\).

Thus the proof applies separately to every member of the missed set; it
does not depend on selecting a special \(y\).

### 2.4 Every such \(y\) lies outside \(B\)

Suppose for contradiction that \(xy\notin E(G)\).  Attack the unoccupied
vertex \(r\) from \(X_u=\{v,t,x\}\).  Exactly \(v,t\) can respond:

\[
\begin{array}{c|c|c}
\text{move}&\text{endpoint}&\text{missed witness}\\ \hline
v\to r&\{t,x,r\}&w\\
t\to r&\{v,x,r\}&y.
\end{array}
\]

The first endpoint misses \(w\) because \(w\) misses \(t,x,r\).  The
second misses \(y\) because \(y\) misses \(v,r\) and, under the
counterfactual, \(x\).  The guard \(x\) cannot move because \(xr\) is a
nonedge.  Hence the retained state \(X_u\) has no dominating response,
contradicting one-guard closure.  Therefore \(xy\in E(G)\) and
\(y\notin B\).

### 2.5 The source edge \(uy\)

Suppose for contradiction that \(uy\notin E(G)\).  Attack the unoccupied
vertex \(y\) from \(M=\{w,t,x\}\).  The always-physical responses and the
optional third response are

\[
\begin{array}{c|c}
t\to y& D_t=\{w,x,y\},\\
x\to y& D_x=\{w,t,y\},\\
w\to y& D_w=\{x,t,y\}\quad\text{if }wy\in E(G).
\end{array}
\]

The state \(D_t\) misses \(r\), using the established nonedges
\(wr,xr,yr\).

The state \(D_x\) cannot belong to \(\mathcal F^\star\).  At its
unoccupied attack \(u\), the unique responder is \(w\): the edges and
nonedges are \(uw\in E(G)\), \(ut\notin E(G)\), and the counterfactual
\(uy\notin E(G)\).  Its unique endpoint \(\{u,t,y\}\) misses \(v\), since
\(uv,tv,yv\) are all nonedges.

If \(D_w\) is physical, it likewise cannot belong to
\(\mathcal F^\star\).  At its attack \(u\), the unique responder is
\(x\), using fullness for \(xu\), root independence for \(tu\), and the
counterfactual for \(yu\).  It reaches the same nondominating state
\(\{u,t,y\}\).

Thus \(M\) would have no retained response at \(y\), contradicting
closure.  Consequently \(uy\in E(G)\).

### 2.6 Retention of the unbanned escape

Attack \(y\) from \(M\) again, now without the false assumption
\(uy\notin E(G)\).  The endpoint \(D_t\) still misses \(r\), so closure
retains at least one of \(D_x,D_w\).

- If \(D_x=\{w,t,y\}\) is retained, attack the unoccupied \(v\).  Only
  \(w\) hits \(v\), and the unique endpoint is \(\{v,t,y\}\).
- If \(D_w=\{x,t,y\}\) is retained, only \(x\) hits \(v\), again with
  endpoint \(\{v,t,y\}\).

Therefore

\[
S-u+y=\{v,t,y\}\in\mathcal F^\star.
\]

Together with \(uy\in E(G)\), this gives \(u\in Q(y)\).  Since
\(y\notin B\), the state is unbanned for color \(u\).  If the
color-\(u\) restricted kernel is empty, every retained unbanned
dominating triple was deleted at a finite round, so this state has a
finite source-color rank.  No strict rank comparison is asserted.

### 2.7 Corollary 2.2

When \(Q(r)=S\), C-157 makes both secondary alternates nondominating, so
both missed sets \(W_v,W_t\) are nonempty.  If
\(w\in W_v\cap B\), Theorem 2.1 applies with this \(w\) and with **every**
\(y\in W_t\); hence all of \(W_t\) lies outside \(B\) and every such
\(y\) gives the retained source-color state above.  Exchanging \(v,t\)
gives the symmetric implication.  Therefore at most one of the two
missed sets meets \(B\).

## 3. Palette-to-adjacency audit

The proof uses only positive palette membership:

- \(v\in Q(r)\) supplies both \(vr\in E(G)\) and the retained state
  \(S-v+r\);
- the conclusion \(u\in Q(y)\) is established only after separately
  proving both \(uy\in E(G)\) and \(S-u+y\in\mathcal F^\star\).

The optional sentence about routing the C-168 transfer through \(w\)
uses \(v\notin Q(q)\) only through C-168's already-reviewed implication:
if the other candidate endpoint were retained, then it would itself
force \(v\in Q(q)\).  It does not infer \(vq\notin E(G)\).

Verdict on this audit item: **PASS**.

## 4. Independent exact replay of MMV-027

The review verifier decodes

```text
JEhbtnm~D]_
```

without a graph library and uses integer adjacency/configuration masks,
whereas the candidate verifier uses adjacency frozensets and sorted
tuples.  It independently obtains

\[
n=11,\quad m=34,\quad
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4).
\]

For \(\theta\), the clean search rejects one, two, and three colors on
\(\overline G\), then returns the explicit four-coloring

```text
[1,0,2,0,1,2,0,2,1,3,2].
```

For eternal domination, the literal kernels have sizes

```text
k=1: 0
k=2: 0
k=3: 122
```

and all 122 dominating triples at \(k=3\) already form the unrestricted
greatest family.

With

```text
S={0,5,6}, x=8, u=6, v=0, t=5, q=2, r=10, w=3, y=1,
```

the clean replay obtains

```text
B = {3,7,9,10}
Q(2)  = {5,6}
Q(10) = {0,5,6}
Q(3)  = {0,6}
Q(1)  = {5,6}.
```

It verifies all named retained states and attacks.  In particular, the
color-6 rank-zero predecessor \(\{0,2,5\}\), attacked at 10, has exactly
these three physical responses:

| mover | endpoint | source-banned? | dominates? |
|---|---|---:|---:|
| 0 | \(\{2,5,10\}\) | no | no |
| 2 | \(\{0,5,10\}\) | yes | yes |
| 5 | \(\{0,2,10\}\) | no | no |

This directly replays the rank-zero universe semantics used in the
proof.

All three restricted kernels are empty.  Their initial universe sizes,
deletion-round sizes, predecessor ranks, and escape ranks are:

| color | initial | round sizes | predecessor rank | escape rank |
|---:|---:|---|---:|---:|
| 0 | 118 | \(27,28,32,27,4\) | 1 | 2 |
| 5 | 119 | \(18,17,29,50,5\) | 3 | 2 |
| 6 | 119 | \(15,28,48,27,1\) | 0 | 0 |

Thus the proposed strict source-rank decrease is genuinely false:
both \(\{0,2,5\}\) and the escape \(\{0,1,5\}\) have color-6 rank zero.

The full-terminal polarization is also visible exactly:

```text
W_v = {3} intersects B,
W_t = {1} is disjoint from B.
```

Finally, the clean replay finds precisely six dominating pairs,

```text
{0,8}, {1,10}, {2,3}, {2,9}, {6,9}, {6,10}.
```

This confirms why the control is outside the equality hypothesis:
\(\gamma=2\).  It is not a gamma--theta counterexample.

## 5. Hash and scope audit

The following candidate bytes were checked:

```text
candidate commit
  2a49be9355261175f81f9c28f9be13f010ea2709
MANIFEST.json
  3c3680e754e5b2c4db6882a90406f2e19dd8b29f60730554875a3bcd4e6d20b8
NOTE.md
  5d79043d2072e4c84f7a6c5083a4da8bbde17fe52cc58e85b3e1cb9b7b4ce004
verify_control.py
  5a9f506c7171448c54df8124a447ed0ba6bcfddcdcc0a0b22266918fc20a5b32
verify_strict.sh
  63ca266b5b2311ed2486e654f6216469d324af446e7fcc60f65be1db9250bd61
expected_result.json
  6b6dcbd31d362653be23516378c170bd46b1e2ce6654a7fc4e5bb0f6c59590ff
```

The candidate strict replay passes with result hash

```text
6b6dcbd31d362653be23516378c170bd46b1e2ce6654a7fc4e5bb0f6c59590ff.
```

The exploratory solver statuses remain labeled **OBSERVED**, are not
used in the proof, and are not promoted by this review.

## 6. Final classification

- **PROVED, after review:** Theorem 2.1, including its arbitrary-\(y\)
  quantifier and finite-rank conclusion.
- **PROVED, after review:** Corollary 2.2, the full-terminal
  witness-set polarization.
- **EXACT FINITE CONTROL:** every stated MMV-027 parameter, family,
  palette, attack, restricted-kernel, and rank assertion.
- **REFUTED SHORTCUT:** the unbanned escape need not strictly lower the
  source restricted rank, even when all three restricted kernels are
  empty.
- **STILL OPEN:** a contradiction using \(\gamma=3\), existence of a
  safe color, complete \(k=3\), and the universal gamma--theta
  conjecture.
