# Hostile review: multi-hit collision endgame

## Verdict

**PASS on the final revised bytes.**

The final confirmed candidate is:

- `NOTE.md` SHA-256
  `acfbc262877c08f9e4b38aa38931c3b95699b50073aa9a67d8ac3f80ba9ba3fd`;
- `MANIFEST.json` SHA-256
  `a7d29adbdcd44d8a2d157a731e84fc09f7d4d2c2175be3a02eb42179cc884636`.

The initial frozen candidate (`NOTE.md`
`ef0635065dcbffa900b3f991fd17cb3c1aa7b1a6ba84334de19a67da0e743a7e`,
manifest
`262364b4561c85df34c9e1bcda682c3ad549c5f777b26bb90ba9bd6bee6bb8e1`)
received `REVISE_LOCAL_ERRATA`.  The final bytes were checked
specifically for all three requested repairs:

1. Theorem 2.1 now explicitly assumes that the deleting attack is
   multi-hit:
   \[
     |N(r)\cap T|\ge 2.
   \]
   The preceding prose is now scoped to that hypothesis.  The note
   correctly records that C-146 supplies it at rank one and at a
   globally minimum-rank reverse endpoint.
2. Equation (4.2) now excludes the endpoints:
   \[
     C_{xr}
       =\{c\in V(G)-\{x,r\}:cx,cr\notin E(G)\}.
   \]
3. Lemma 3.1 now explicitly derives \(y_g\ne g\) from
   \(gr\in E(G)\) and \(y_gr\notin E(G)\) before using domination by
   \(B\).

I found no substantive defect in:

- the intended six-case multi-hit table;
- the all-rank XQ0 rank drop, reciprocity, and response square;
- the all-rank XQ1 reciprocity statement;
- the rank-one XQ0 contradiction;
- the QQ0/AQ0 paired-private-witness ridge;
- the XQ1 independent ladder; or
- the corrected QQ completion-clique alternative.

The candidate and clean-room control replays both pass unchanged.  The
strict scope is also correct: the note does not eliminate all multi-hit
collisions, prove reciprocity, complete \(k=3\), or resolve the
gamma--theta conjecture.

## 1. Dependency and rank audit

I reconstructed the exact portions of accepted C-143, C-145, and C-146
used by the candidate.

- C-143 makes every reverse endpoint \(B=T-x+u\) dominating.
- C-108 transports activity over every maximum-independent vertex star
  and makes the omitted reverse orientation uniform over all such
  endpoints.
- C-145 says that a one-sided active edge and any common nonneighbor
  retain their three-vertex repair ridge.
- C-146 uses the synchronous horizons
  \(\mathcal K_0,\mathcal K_1,\ldots\), with non-domination at rank zero,
  deletion from \(\mathcal K_{h-1}\) at rank \(h\), and survival at
  infinite rank.

If \(B\) has rank \(h\) and \(r\) deletes it at round \(h\), every
adjacency-eligible successor at \(r\) has rank below \(h\).  In XQ0 only
\(p\) can move.  When \(h=1\), its successor \(C_p\) is non-dominating.
When \(h\ge2\), membership \(B\in\mathcal K_{h-1}\) forces that unique
successor into \(\mathcal K_{h-2}\), while deletion excludes it from
\(\mathcal K_{h-1}\).  Hence
\[
  \rho(C_p)=h-1
\]
exactly.  There is no off-by-one error.

The six rows are exhaustive only after the missing multi-hit hypothesis
is supplied.  C-146 first guarantees that \(r\) hits at least one of
\(\{p,q\}\).  Relabeling makes \(pr\) an edge.  A second hit leaves,
up to \(p\leftrightarrow q\),
\[
  \{x,p\},\quad\{p,q\},\quad\{x,p,q\}.
\]
The independent binary choice \(ur\in E(G)\) gives exactly:

| row | \(N(r)\cap T\) | \(ur\) | \(B\)-movers |
|---|---|---:|---|
| XQ0 | \(\{x,p\}\) | no | \(p\) |
| XQ1 | \(\{x,p\}\) | yes | \(u,p\) |
| QQ0 | \(\{p,q\}\) | no | \(p,q\) |
| QQ1 | \(\{p,q\}\) | yes | \(u,p,q\) |
| AQ0 | \(\{x,p,q\}\) | no | \(p,q\) |
| AQ1 | \(\{x,p,q\}\) | yes | \(u,p,q\) |

There is no seventh row and no named-vertex collision hidden in this
table.  In the multi-hit setting \(r\ne x\): if \(r=x\), independence of
\(T\) makes \(r\) miss \(p,q\), so it cannot be multi-hit.

## 2. Active-relation audit

Every active-relation inference has either an explicit
maximum-independent witness or an accepted star/ridge transport.

### XQ0

- \(q\triangleright u\) is witnessed directly by \(T\), because
  \(L_T(u)=\{q\}\).
- If \(u\not\triangleright q\), \(r\) is a common nonneighbor of \(q,u\).
  C-145 would retain \(\{q,u,r\}=C_p\), contradicting the deleting
  attack.  Hence \(u\triangleright q\).
- A singleton \(L_T(r)=\{x\}\) directly witnesses
  \(x\triangleright r\); the common nonneighbor \(q\) and C-145 force
  \(r\triangleright x\), or else the alternate \(p\)-successor is
  retained.  The singleton \(\{p\}\) is symmetric.

The response square is literal.  For
\(D=T-g+r\), \(g\in\{x,p\}\), the non-\(q\) eligible move at target \(u\)
lands in omitted \(C_p\), while \(r\) misses \(u\); closure forces
\(q\to u\).  At the next unoccupied attack \(q\), only \(u\) is
adjacent, so \(u\to q\) returns to \(D\).

### XQ1

Deleting-attack exclusion removes the \(x\)-successor \(C_u\), so
\(L_T(r)=\{p\}\) directly witnesses \(p\triangleright r\).  If
\(r\not\triangleright p\), the common nonneighbor \(q\) and C-145 would
retain exactly \(C_u\).  Hence \(p\leftrightarrow r\).

### QQ

A singleton \(p\)- or \(q\)-response has the same sound C-145 reversal,
now using \(x\) as the common nonneighbor.  In the completion-clique
argument, \(p\leftrightarrow r\) is witnessed directly by the two
maximum-independent bases
\[
  \{x,p,c\},\qquad\{x,r,c\};
\]
the \(q\)-statement is symmetric.

### Private-witness paths

In Theorems 3.2 and 3.3, every use of the assumed
\(u\triangleright x\) begins at a maximum independent triple
\(\{u,r,y_g\}\), so accepted C-108 applies.  The remaining moves on the
displayed paths are forced one-edge responses, not unsupported activity
assertions.  The C-064 covariance invocation in (3.7) is in its valid
ridge scope: \(U_p,U_q\) are retained independent triples sharing
\(\{u,r\}\), and the targets \(p,q\) lie outside both states.

## 3. Rank-one XQ0 contradiction

This is the most important new exclusion and it is sound.

The unique XQ0 successor at rank one is non-dominating.  Its private
witness \(y=y_p\) satisfies
\[
  py\in E(G),\qquad
  yu,yr,yq\notin E(G).
\]
Together with \(ur\notin E(G)\), this makes
\(\{u,r,y\}\) an independent triple.  Equality makes it a retained
maximum independent state.  The assumed activity \(u\triangleright x\),
transported by C-108, retains \(\{x,r,y\}\).

The target \(q\) is unoccupied and misses all three guards:
\[
  qx,qr,qy\notin E(G).
\]
Thus there is no adjacent guard at all, let alone a retained successor.
This contradicts one-guard eternal closure.  The argument does not move
multiple guards, attack an occupied vertex, or assume that
\(\{x,r,y\}\) is independent.

## 4. Private-witness collisions and the two rank-one structures

For a legal mover \(g\), a missed vertex of
\(C_g=B-g+r\) misses \(r\) and \(B-\{g\}\).  Because \(gr\) is an edge,
it cannot equal \(g\); it also cannot equal an occupied member of
\(C_g\).  Domination by \(B\) therefore forces its unique \(B\)-neighbor
to be \(g\).

If \(g\ne g'\), then \(y_g\) is adjacent to \(g\), whereas
\(y_{g'}\) misses \(g\).  Hence \(y_g\ne y_{g'}\).  This also rules out
all collisions needed by the later attacks:

- a witness cannot equal \(u,p,q,r\);
- in XQ/AQ it cannot equal \(x\), because \(xr\) is an edge while it
  misses \(r\);
- in QQ it cannot equal \(x\), because it is adjacent to its named
  endpoint while \(x\) misses both \(p,q\).

For QQ0/AQ0, each
\[
 U_g=\{u,r,y_g\}
\]
is therefore genuinely independent and retained.  The attacks
\[
 u\to x,\qquad r\to t,\qquad y_g\to g
\]
are at distinct unoccupied vertices and are uniquely forced by the
stated adjacency pattern.  If \(y_p y_q\) were absent,
\(\{u,r,y_p,y_q\}\) would be independent, so \(\alpha=3\) forces the
edge.  C-064 then removes the local witnesses from their corresponding
endpoint-response lists exactly as claimed.

For XQ1, the two private witnesses \(y_p,y_u\) are distinct.  The initial
state \(T-p+r\) forces \(x\to y_p\).  Domination then forces the
\(y_p y_u\) edge, after which
\[
 \{y_p,r,q\}
 \to
 \{y_u,r,q\}
 \to
 \{y_u,p,q\}
 \to
 T
\]
uses respectively the one-edge moves
\[
 y_p\to y_u,\qquad r\to p,\qquad y_u\to x.
\]
All four displayed states are independent; each target is unoccupied.

## 5. Corrected QQ completion clique

With
\[
 C_{xr}
 =\{c\notin\{x,r\}:cx,cr\notin E(G)\},
\]
the proof is complete.

The independent pair \(\{x,r\}\) extends to an independent triple, so
the corrected set is nonempty.  Two nonadjacent external completions
would make an independent four-set, so it is a \(G\)-clique.  A
completion missing both \(p,q\) would make
\(\{x,p,q,c\}\) independent of size four.  Finally, a completion
missing \(p\) gives the two retained independent bases
\(\{x,p,c\}\) and \(\{x,r,c\}\), hence \(p\leftrightarrow r\); similarly
for \(q\).

Thus if neither reverse \(r\)-orientation is active, every external
completion hits both \(p,q\).  The initial frozen statement failed only
because its set notation omitted “\(c\notin\{x,r\}\)”; the final
confirmed bytes include that exclusion.

## 6. Independent fixed-control replay

`independent_checker.py` shares no transition core, graph representation,
or subset representation with the candidate evaluator.  It uses integer
adjacency masks, integer configuration masks, a separately written
graph6 decoder, and a literal synchronous greatest-fixed-point loop.

It independently obtains:

| graph | \((\gamma,i,\alpha,\gamma^\infty)\) | triple kernel | local result |
|---|---:|---:|---|
| `GEjbug` | \((2,2,3,3)\) | 41 | QQ1 reverse rank one; three rank-zero successors; \(p,q\) forward-active and reverse-inactive; \(\{x,r\}\) dominates and has no external completion |
| `GCOedo` | \((3,3,3,4)\) | 0 | XQ0 reverse rank one; unique successor misses vertex \(5\); independent source `567` would move to `057`, which misses \(q=1\) |

The clean-room JSON output has SHA-256
`81e97358596fd0f4228912e5970c27308afbf7a0eb87d414151efd7d0730ecb5`.
These controls establish only sharp boundary behavior, not the symbolic
lemmas.

## 7. Exact remaining collision cases

Even after the two edits, the candidate leaves all of the following
open:

1. XQ0 at rank \(h\ge2\): the successor has exact rank \(h-1\), but is
   not known to be a reverse endpoint.
2. Rank-one XQ1 after the forced four-facet ladder.
3. QQ with at least one reciprocal \(r\)-edge.
4. QQ with neither reciprocal edge but a nonempty completion clique all
   of whose vertices hit both \(p,q\).
5. AQ0 and AQ1 beyond the stated rank-one local structures.
6. Every higher-rank multi-hit successor, where non-domination witnesses
   need not exist.

Accordingly, neither greatest-family reciprocity, the complete \(k=3\)
case, nor the gamma--theta conjecture is proved.
