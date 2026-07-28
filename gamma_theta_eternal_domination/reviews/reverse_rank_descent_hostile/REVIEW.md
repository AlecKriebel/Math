# Hostile review: finite-horizon star transport and reverse-rank descent

## Verdict

**PASS.**

The five candidate results are sound with their stated scope:

1. finite-horizon vertex-star transport;
2. the star-Lipschitz bound for extended synchronous deletion rank;
3. the reverse-endpoint Lipschitz potential under C-143;
4. exact one-round descent at a single-hit deleting attack; and
5. the conclusion that a rank-one or globally minimum-rank blocker must
   hit at least two guards of the independent endpoint.

The argument does not establish survivor reciprocity or eliminate the
remaining multi-hit collision branch.  It proves no complete parameter
case and does not resolve the gamma--theta conjecture.

## Frozen inputs and dependencies

The candidate manifest hashes agree byte for byte with the reviewed files:

| artifact | SHA-256 |
|---|---|
| candidate `NOTE.md` | `3481a7dcc650a83d3994ff4bfdfb7789a520bb6a29dc57b51c1a84d549fd5b77` |
| candidate `RESEARCH_LOG.md` | `8664d89caa287adaee0e92e615c3c5245dc0f2ae32171d282135b509d4f75f3c` |
| candidate `expected_result.json` | `4d9b0094e18d6af5f401391bb7a04fba7b09e7bc6067b99a741b0225d67ed868` |
| candidate `verify_controls.py` | `5a02183c178c772ad7cc9301c8b60c2ff9d8cbc72f4eb51bf2163f8ba1c9eb97` |
| accepted C-108 source | `d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8` |
| accepted C-143 source | `3255bcc3d75b8538d6c8e3288f8106b553194bbac1fc3ac590d18ba6d6f81de3` |

Both dependency uses are legitimate.  C-108 supplies response propagation
within a fixed responder/target star.  C-143 supplies domination, but not
survival, of every reverse endpoint.

## Symbolic audit

### Synchronous ranks and finite horizons

The convention

\[
\rho(D)=0\quad\Longleftrightarrow\quad D\notin\mathcal K_0,
\]

\[
\rho(D)=h\quad\Longleftrightarrow\quad
D\in\mathcal K_{h-1}\setminus\mathcal K_h\quad(h\geq1)
\]

has been used consistently.  For finite rank,

\[
D\in\mathcal K_j\quad\Longleftrightarrow\quad \rho(D)>j,
\]

while an infinite-rank state belongs to every horizon.  The proof never
confuses deletion round \(h\) with membership in \(\mathcal K_h\).

In Theorem 2.1, the state before attack \(b_\ell\) lies in
\(\mathcal K_{j+m-\ell+1}\); therefore the retained successor lies in
\(\mathcal K_{j+m-\ell}\).  This is the required one-layer loss, with no
off-by-one error at the final attack: when \(j=0,\ell=m\), the successor
must still dominate and lie in \(\mathcal K_0\).

### Forced-transport quantifiers

The overlap decomposition is valid for arbitrary overlap, including
\(m=0\).  At step \(\ell\), \(b_\ell\) is unoccupied: it is outside the
original source, outside the common part, and distinct from all earlier
targets.

No installed target-state guard can move to \(b_\ell\), because both
vertices lie in the independent set \(T'\).  If the guard at \(x\) moves,
the resulting state contains only vertices of
\((T\cup T')-\{v\}\).  Every one of those vertices is nonadjacent to the
now-unoccupied vertex \(v\), so the state is non-dominating.  Thus a
retained response is forced from the shrinking set \(O\), and exactly one
guard is consumed per attack.  This uses unoccupied attacks and exactly
one edge move throughout.

Applying the directed implication in both directions gives both survival
equivalence and

\[
|\rho(D)-\rho(D')|\leq |T-T'|
\]

when the ranks are finite, including cases where one finite rank is zero.

### Reverse-endpoint ranks

Under \(\gamma=\gamma^\infty=k\), the parameter chain supplies
\(i=\alpha=k\).  Activity \(u\triangleright x\) supplies the edge \(ux\);
therefore every independent endpoint containing \(x\) avoids \(u\), as
required by the star theorem with responder \(x\) and target \(u\).

C-143 makes every reverse endpoint dominating.  The assumed inactive
reverse orientation and C-108 keep every such endpoint outside the
greatest family.  Hence every reverse rank is positive and finite.  The
set of endpoint ranks is nonempty because a vertex extends to a maximal
independent set and well-coveredness gives size \(k\).

### Deleting attacks and exact descent

For a positive-rank state

\[
B\in\mathcal K_{h-1}\setminus\mathcal K_h,
\]

the definition of \(\mathcal K_h\) gives an unoccupied attack \(r\) for
which every adjacency-respecting one-guard successor has rank below
\(h\).  Non-dominating successors have rank zero, so no successor class
is silently omitted.

If \(r\) misses all of \(Q=T-\{x\}\), domination of \(B=\{u\}\cup Q\)
forces \(ur\in E(G)\).  The single move \(u\to r\) produces the
independent \(k\)-set \(Q\cup\{r\}\).  Since \(\alpha=k\), it is maximum
independent and is forced into every eternal \(k\)-family, including the
greatest family.  This contradicts deletion and proves
\(Q\cap N(r)\neq\varnothing\).

If the attack has exactly one neighbor \(q\) in the endpoint \(T\), that
neighbor lies in \(Q\).  The state \(J=T-q+r\) is independent of size
\(k\), contains \(x\), and the move \(q\to r\) produces exactly

\[
C=J-x+u.
\]

Deletion gives \(\rho(C)<h\); C-143 and C-108 give
\(1\leq\rho(C)<\infty\); the unit star-Lipschitz bound gives
\(|\rho(C)-h|\leq1\).  Therefore \(\rho(C)=h-1\).

For \(h=1\), this would contradict the positive-rank conclusion.  At a
globally minimum reverse endpoint, it would contradict minimality.
Together with \(Q\cap N(r)\neq\varnothing\), both cases force at least two
neighbors in \(T\).  The \(k=1\) case is vacuous because the asymmetric
premise itself would force a maximum-independent reverse response.

## Independent computation

`independent_checker.py` was written with integer masks and synchronous
snapshot deletion.  It imports no campaign evaluator and no candidate
code.  It independently:

- decoded all four graph6 controls and matched their edge-list hashes;
- recomputed \(\gamma,i,\alpha,\gamma^\infty\);
- recomputed every triple-kernel deletion rank;
- matched the two sharp Lipschitz controls;
- matched the rank-two to rank-one single-hit descent;
- matched the rank-one multi-hit boundary and all its rank-zero
  successors;
- exhausted all 33,867 labeled graphs through order six and every guard
  size, checking 1,918,272 star comparisons and 10,919,952 directed
  finite-horizon implications.

No equality graph through order six had an asymmetric active orientation,
so the small-order run gives no nonvacuous additional test of Section 4.
The two fixed boundary controls provide the nonvacuous rank-descent and
collision checks.  The candidate replay and the clean-room replay were
both byte-exact.

## Nonblocking editorial precision

Two phrases could be sharpened without changing any theorem:

- “Taking one rank to be infinite recovers C-108” means the
  **greatest-family instance** of C-108; accepted C-108 also applies to an
  arbitrary specified eternal subfamily.
- In Section 4, “legal one-guard successor” is best read as an
  adjacency-respecting edge-swap successor.  Some such successors can be
  non-dominating and have rank zero.  “Adjacency-eligible successor”
  would remove the possible ambiguity.

Neither wording issue affects the proof or its stated mathematical scope.

## Final scope table

| item | verdict |
|---|---|
| finite-horizon transport | **PROVED** |
| star-Lipschitz deletion rank | **PROVED** |
| positive finite reverse-rank landscape | **PROVED**, using accepted C-108 and C-143 |
| exact single-hit rank descent | **PROVED** |
| rank-one/minimum-rank blockers are multi-hit | **PROVED** |
| fixed controls and small-graph replay | **VERIFIED** |
| survivor reciprocity | **OPEN** |
| elimination of multi-hit collisions | **OPEN** |
| complete \(k=3\) case | **OPEN** |
| universal gamma--theta conjecture | **OPEN** |
