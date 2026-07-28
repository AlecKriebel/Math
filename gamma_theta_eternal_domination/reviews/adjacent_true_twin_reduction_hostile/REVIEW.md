# Hostile review: adjacent true-twin reduction

## Verdict

**PASS — the stated lemmas, theorem, and corollary are proved as written.**

I found no missing hypothesis, one-guard model error, or exceptional graph.
The target reviewed had SHA-256
`b28262900ddb77d62caea61741e502f2da706900f51ce47165c2582b899c36ae`.

The sentence following the successor \(D'\) could optionally say explicitly
that the move edge remains in the induced graph \(Q\) and that \(D'\)
dominates \(Q\).  Both facts already follow immediately from
\(w,r\in V(Q)\), \(Q=G-v\), and \(D'\in\mathcal F\); this is an expository
addition, not a proof correction.

## Reconstruction of the static steps

Let \(N_G[u]=N_G[v]\), with \(u\ne v\), and let \(Q=G-v\).

1. The equality of closed neighborhoods itself implies \(uv\in E(G)\):
   \(u\in N_G[u]=N_G[v]\).
2. A dominating set of \(G\) can be made a set in \(Q\) without increasing
   its size.  Replace \(v\) by \(u\) if only \(v\) occurs; if both occur,
   delete \(v\).  In either case every vertex formerly covered by \(v\) is
   covered by \(u\).
3. A dominating set \(D\) of \(Q\) dominates \(v\).  If \(u\in D\), use the
   edge \(uv\).  Otherwise domination of \(u\) supplies
   \(d\in D\cap N_G(u)\), and closed-neighborhood equality gives
   \(d\in N_G(v)\).  This includes the possible one-vertex graph \(Q=K_1\).
4. An independent set contains at most one twin because the twins are
   adjacent.  Replacing \(v\) by \(u\) preserves every nonadjacency to a
   third vertex.  This proves equality of independence numbers in both
   directions.
5. Deleting \(v\) from a clique partition cannot increase its number of
   parts.  Conversely, the part of a partition of \(Q\) containing \(u\)
   remains a clique after adding \(v\): every third vertex adjacent to \(u\)
   is adjacent to \(v\), and \(u\) is adjacent to \(v\).

Thus all three static equalities in Lemma 1 are exact.  Adjacency is used
essentially in the independence and clique-cover arguments.

## Reconstruction of the eternal steps

### Forced independent states

For an eternal family \(\mathcal F\) of \(k\)-sets and an independent
\(k\)-set \(S\), choose any \(D\in\mathcal F\).  If \(s\in S-D\) is attacked,
the attack is legal because it is unoccupied.  A guard in \(D\cap S\)
cannot move to \(s\), since distinct vertices of \(S\) are nonadjacent.
Therefore the responding guard lies in \(D-S\), exactly one guard moves
along an edge to \(s\), and \(|D\cap S|\) increases by one.  After at most
\(k\) attacks the state is \(S\).  Every successor is in \(\mathcal F\), so
\(S\in\mathcal F\).  No occupied-vertex attack or all-guards move is used.

### The restricted family

Under \(\gamma(G)=\gamma^\infty(G)=k\), equality collapse and Lemma 1 give
\(\gamma(Q)=\alpha(Q)=k\).  Hence \(Q\) has an independent \(k\)-set \(S\).
It is also independent in \(G\), so the preceding argument puts it in every
eternal \(k\)-family \(\mathcal F\) of \(G\).  Because \(S\subseteq V(Q)\),
the restriction
\[
  \mathcal F_Q=\{D\in\mathcal F:v\notin D\}
\]
is nonempty.

Now take \(D\in\mathcal F_Q\) and attack
\(r\in V(Q)-D\).  The attack is the same unoccupied attack in \(G\).
Closure in \(G\) supplies a guard \(w\in D\cap N_G(r)\) and
\(D'=D-\{w\}+\{r\}\in\mathcal F\).  Since both \(w\) and \(r\) lie in
\(V(Q)\), their edge is present in the induced graph \(Q\).  Since neither
the old state nor the target contains \(v\), the successor avoids \(v\).
Finally \(D'\) dominates \(G\), hence it dominates \(Q\).  Therefore
\(D'\in\mathcal F_Q\) is a legal one-guard successor in \(Q\).

Configurations of \(\mathcal F\) containing both twins do not create a gap:
they are discarded, nonemptiness is separately guaranteed by \(S\), and a
transition from an avoiding state under an attack in \(Q\) cannot reintroduce
\(v\).  Thus \(\mathcal F_Q\) is eternal and
\(\gamma^\infty(Q)\le k=\gamma(Q)\); the reverse inequality is the universal
domination lower bound.

The clique-cover equality from Lemma 1 then makes \(Q\) a strictly
smaller counterexample whenever \(G\) is one, proving the corollary.
Connectedness is not required.  If desired, it is also preserved when one
of adjacent true twins is deleted.

## Explicit edge cases

- **\(K_2\):** \(k=1\), \(Q=K_1\), and the restricted family is the singleton
  state \(\{u\}\).  It is nonempty and has zero attack obligations, so the
  proof correctly handles vacuous closure.
- **A source state containing both twins:** it is not retained, but the proof
  never requires it.  The forced independent state witnesses a surviving
  configuration.
- **An attack at \(u\):** if \(u\) is unoccupied, it is an ordinary attack in
  both graphs.  The responding guard belongs to the current state and hence
  cannot be the deleted vertex.
- **\(k=1\):** Lemma 2 still works; its iteration has either zero or one
  attack.  No assumption \(k\ge2\) is needed.

## Clean-room exhaustive falsifier

`falsifier.py` uses integer adjacency masks, exhaustive subset algorithms
for \(\gamma\) and \(\alpha\), direct clique-partition recursion for
\(\theta\), and a literal greatest-fixed-point deletion algorithm for
\(\gamma^\infty\).  It imports no campaign evaluator or transition core.

The pinned `geng` stream covered all 12,113 connected unlabeled graphs
through order 8, with the standard per-order counts
\(1,1,2,6,21,112,853,11117\).  It checked:

- 4,087 graphs having an adjacent true-twin pair;
- 6,279 individual twin-pair incidences;
- all three static equalities at every incidence;
- 748 incidences satisfying \(\gamma=\gamma^\infty\);
- every parameter conclusion of Theorem 3 at those incidences;
- nonemptiness and every one-guard attack obligation of the restricted
  greatest family;
- inclusion of every independent \(k\)-state in the greatest family.

There were zero failures.  This finite check supports but is not needed for
the universal proof.

Hashes:

- `falsifier.py`:
  `a82dd4023a86d2daaeaf8171efbea155fff9711d328eff8d2fe41dccd4e47404`
- `result.json`:
  `24794b69fddb135b74bf588cca4591b380a5af625dd2a4849273314317fd0362`
- pinned `geng`:
  `588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1`

Run resource use was 1.50 seconds wall time, 46,153,728 bytes maximum
resident set size, and zero swaps.
