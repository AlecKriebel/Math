# Hostile review: full-list rank-rebound iteration

## Verdict: unconditional PASS

Date: 2026-07-28 (PDT)

Frozen candidate: commit `42629d71`, directory
`math/working/full_list_rank_rebound_iteration/`.

The candidate's theorem statements are correct at their stated scope.  I
independently reconstructed the restricted peeling argument, checked all
rank indices and Johnson distances, audited every named collision and
occupied-attack boundary in the completion fans, and recomputed the exact
13-vertex sharpness control without importing the candidate's transition
core.

This passes only the following local results:

1. the all-\(k\) tight-shell descent;
2. the rank-one second-fan anchor exit;
3. the two target-fan dominance/reciprocity splits; and
4. the exact gamma-two sharpness boundary.

It does **not** prove a safe color, the complete \(k=3\) case, a new finite
exclusion, or the gamma--theta conjecture.

## Frozen-byte audit

The candidate bytes agree with its manifest:

| File | SHA-256 |
|---|---|
| `NOTE.md` | `378633621b759c31d1b747b0f1a7bd657f17d8b60da9b8356488640e8fbb8f19` |
| `RESEARCH_LOG.md` | `d5dc301d3a086cc3a185fe63ba2075c6eeec912868fe66a876341c2fe3e87f6f` |
| `verify_boundary.py` | `49b3caa552e4562744fe8592fdaf8b604a9f811b107c645969b6917dc3d9682e` |
| `verify_strict.sh` | `1c45c5d9ed4bc03b92f87daebd5badeb4a95cb5ca36297990cdd17c58e31ffbc` |
| `expected_result.json` | `e74547cbbc38651f874f10124a1bb09b95db901a37cf8ff02e057f27b7722650` |

The candidate strict replay passes byte-for-byte.

## Proof reconstruction

### 1. Tight-shell descent

Let \(D\) have restricted rank \(s-1\) and ban distance \(s\ge2\).
By the definition
\[
\Omega_{j+1}=\Phi(\Omega_j),
\]
a deletion-witness attack for a rank-\((s-1)\) state has no physical
dominating unbanned response in \(\Omega_{s-1}\).  Every response retained
by the eternal family is nevertheless physical and dominating.  A
one-token move lowers Johnson distance to the ban by at most one, so such a
response has distance at least \(s-1\).  The accepted distance floor gives
rank at least \(s-2\), while deletion gives rank at most \(s-2\).  Hence
both are equalities.

The indexing is exact: a rank-\(j\) state lies in
\(\Omega_j\setminus\Omega_{j+1}\).  No off-by-one shift occurs.  The proof
quantifies only over responses retained in the same eternal family and
never treats a missing family endpoint as a graph nonedge.

### 2. Exact second-fan distance

For \(K_e=\{r,y,e\}\), neither fixed ban anchor \(v,t\) is present:
\(e\ne v\) because \(vr\in E(G)\), and \(e\ne t\) because
\(tr\in E(G)\) (also \(ty\in E(G)\)).  The state contains \(r\in B\).
Every banned triple has the form \(\{v,t,b\}\), \(b\in B\).  Thus a banned
triple shares at most one token with \(K_e\), while the choice \(b=r\)
shares one.  Therefore its distance is exactly two, including when
\(e\in B\).

The completion set \(C_{ry}\) is a clique by \(\alpha=3\).  For another
\(e'\in C_{ry}\), only \(e\) can answer the attack at \(e'\), and the
endpoint is \(K_{e'}\).  Minimum rank therefore prevents any such attack
from deleting \(K_e\).  This justifies the stated location of all deleting
attacks.

### 3. Why rank one forces the fixed anchors

At rank one, tight-shell descent makes every retained response have
distance one and rank zero.  The starting triple contains neither \(v\)
nor \(t\).  An endpoint at distance one must share two tokens with some
\(\{v,t,b\}\).  Since one guard moves, the new attacked vertex must be
\(v\) or \(t\); changing only the \(B\)-token cannot add either missing
anchor.  This remains true if \(K_e\) contains two vertices of \(B\).

Both attacks are unoccupied.  At \(v\), \(e\to v\) legally reaches the
already retained \(J=\{v,r,y\}\); at \(t\), eternal closure supplies a
physical retained response.  Tight-shell descent applies to every retained
response, not merely a selected one.

### 4. Target-fan split and reciprocal hinges

The pair \(q,w\) misses exactly \(C_{qw}\).  Because \(xq\) is an edge,
\(x\notin C_{qw}\).  Hence \(\{x,q,w\}\) dominates exactly when every
completion is adjacent to \(x\), equivalently
\(C_{qw}\cap N_{\overline G}(x)=\varnothing\).  The \(r,y\) statement is
identical, using \(xy\in E(G)\).

If \(d\in C_{qw}\cap B\), the states
\[
\{q,w,d\},\qquad \{x,w,d\}
\]
are maximum independent triples.  The attacks at \(x\) and \(q\)
uniquely exchange \(q\leftrightarrow x\).  If \(d=t\), the first state is
the already retained \(L_q\); membership \(t\in C_{qw}\) itself supplies
the otherwise potentially missing \(tq\) nonedge.  Thus the occupied
collision is handled without attacking \(t\).

If \(e\in C_{ry}\cap B\), the maximum independent states
\[
\{r,y,e\},\qquad \{x,r,e\}
\]
uniquely exchange \(y\leftrightarrow x\).  The possible collisions
\(e=v,t,x,r,y\) are excluded respectively by the named edges or by the
closed-neighborhood definition of \(C_{ry}\).  A collision \(e=w\) is
harmless.

The alternatives are correctly stated as inclusive: reciprocity may also
hold when the cross triple dominates.

## Independent finite audit

`verify_clean.py` uses integer adjacency and state masks and imports no
candidate or campaign implementation.  It performs four checks:

1. It exhausts every labeled graph through order four, every
   \(k\le3\), every eternal family, and every nonempty ban of \(k\)-sets
   for the tight-shell statement.
2. It audits anchored rank-one exits on every graph through order five
   and the deterministic order-six graph-code slice
   `code == 7 (mod 16)`.
3. It exhausts every labeled graph through order six for the static
   target-fan equivalence, fan clique consequence under \(\alpha\le3\),
   and both unique reciprocal moves.
4. It independently decodes `LEhbtnm~D]xln{`, recomputes all five exact
   parameters, its greatest eternal family, **all three** restricted
   kernels and rank tables, both completion fans and cross states, and
   the nonanchor rank-two deletion witness.

The candidate wrapper directly prints only the source-color restricted
data, although its prose says that the verifier recomputes all restricted
kernels.  This is a replay-coverage shortfall, not a mathematical defect:
the pinned predecessor verifier contains the other two computations, and
the clean-room checker here independently executes and checks all three.

## Gamma-two scope

The exact graph has
\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4).
\]
It is used only to refute two stronger local conclusions: extending the
anchor-exit claim beyond rank one, and deriving a surviving restricted
kernel from two retained dominating cross triples.  No theorem proof
imports \(\gamma=2\) behavior into the equality case, and the graph is not
presented as a gamma--theta counterexample.

## Reproduction

Run:

```sh
./gamma_theta_eternal_domination/reviews/full_list_rank_rebound_iteration_hostile/verify_strict.sh
```

The script replays the frozen candidate, the independent audit, and every
review-file hash.

Best-guess review completion: **100%**.  Best-guess contribution toward
eliminating the full-list rank-preserving escape branch: **25%**.  This is
a workload estimate, not a probability of correctness or conjecture
resolution.
