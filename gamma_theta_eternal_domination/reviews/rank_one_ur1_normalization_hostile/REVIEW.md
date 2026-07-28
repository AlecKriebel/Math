# Hostile review: rank-one \(ur=1\) normalization

Date: 2026-07-28 (PDT)

Candidate commit:
`84bbe50d4c21a4956930ec84bfa637c6e99e5ec7`

## Verdict

\[
\boxed{\textbf{UNCONDITIONAL PASS}}
\]

I independently reconstructed the QQ1 and AQ1 hypotheses from accepted
C-150, replayed every symbolic attack and ridge transport in the candidate,
enumerated every optional incidence among the named vertices, and rebuilt
the fixed-graph control without importing the candidate checker or either
campaign verifier.

The candidate proves exactly the following.

> Under
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\), in the literal greatest
> eternal triple-family, every rank-one QQ1 or AQ1 collision of the
> accepted C-150 type has the displayed saturated normal form.  In AQ1,
> the private witness \(a=y_u\) produces the one-sided active edge
> \(u\triangleright a\), \(a\not\triangleright u\), and recreates a QQ1
> collision on \(S=\{a,p,q\}\) with the same rank-one reverse state and
> the same blocker.  In both rows, every common nonneighbor of \(a,r\)
> hits both \(p,q\), and the common-nonneighbor set is a nonempty
> \(G\)-clique.

This is a normalization theorem, not an exclusion of the final QQ1 core.
It does not address higher deletion rank, prove reciprocity, complete
\(k=3\), or resolve the gamma--theta conjecture.

I found no mathematical error, hidden freshness assumption, omitted
one-guard branch, reversed covariance map, occupied-vertex attack, or
inference from an absent family transition to a graph nonedge.

## Frozen candidate and dependencies

The reviewed bytes are frozen as follows.

| artifact | SHA-256 |
|---|---|
| candidate `NOTE.md` | `4983d87b0af8cec7ca06aa7a0a12b96bb480b8dbe4c886773770046b9b4090d6` |
| candidate `RESEARCH_LOG.md` | `2321e32049de10822e48b61a2416b7558d10061487f6291c224412cb4bd6653c` |
| candidate `MANIFEST.json` | `61552c2466bd52a1c0617cf70e2917be548cd533de8ace4c787e60f7edd5ab3b` |
| candidate `verify_implication.py` | `c7d89a82c16f6010719bcb604a4c21533613e85c3033c93d99c139f95affad7e` |
| candidate `expected_result.json` | `838dfd712a406c5c0a07bebe3ef48bc30833bf3b43011992a1da470cc08ca088` |
| candidate `verify_control.py` | `368f82ffb87ffabda215b3da210c187deab65025048d30a072a68469c5d184ab` |
| candidate `expected_control_result.json` | `453d04b7488634c09f1ab3cd1496150e7b1c11523c205a4b1dfaa2bf5ee32473` |
| candidate `verify_strict.sh` | `6d9ae279056c606b9c5a593375e2b1c85fcc8fa418f5c1c1af95e1fb9183e5b1` |
| accepted C-150 source | `acfbc262877c08f9e4b38aa38931c3b95699b50073aa9a67d8ac3f80ba9ba3fd` |
| accepted C-064 source | `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7` |
| accepted C-108 source | `d6a0ec8a7daff1cca0094e1929134507364cea3c2c8781fbe24956a3238048d8` |
| accepted C-010 source | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |

The candidate directory at the reviewed commit and the current working
tree were byte-identical during review.

## 1. Exact C-150 reconstruction and collision ledger

Write

\[
T=\{x,p,q\},\qquad B=\{u,p,q\}.
\]

Here \(T\) is maximum independent, \(B\) has deletion rank one, and the
deleting attack \(r\) has

\[
ur,pr,qr\in E(G).
\]

Rank one makes all three successors at \(r\) non-dominating.  Their
private witnesses \(a=y_u,b=y_p,c=y_q\) therefore have exactly the
required incidences

\[
\begin{array}{c|c|ccc}
 &\text{edge}&\multicolumn{3}{c}{\text{nonedges}}\\ \hline
a&au&ar&ap&aq\\
b&bp&bu&br&bq\\
c&cq&cu&cr&cp.
\end{array}
\]

The witness collisions are fully controlled.

- \(b,c\) are distinct from one another and from
  \(u,x,p,q,r\), using their private edges and the corresponding fixed
  nonedges.
- \(a\) is distinct from \(u,p,q,r,b,c\).
- In AQ1, \(xr\in E(G)\) and \(ar\notin E(G)\), so \(a\ne x\).
- In QQ1, \(xr,xp,xq\notin E(G)\) and \(xu\in E(G)\), so \(x\) itself is
  a valid private witness for the \(u\)-successor.  The canonical
  assignment \(a=x\) is therefore legitimate.

No loop \(aa\) or \(xx\) is introduced.  Every formula involving \(a\)
in QQ1 is read after the literal substitution \(a=x\).

The AQ1 root \(T\) dominates its fresh witness \(a\); since \(a\) misses
\(p,q\), this correctly forces \(ax\in E(G)\).

## 2. Transferred states and the complete \(U,R,S\) forcing

Accepted C-010 and \(i=\alpha=3\) extend each independent pair
\(\{u,b\}\), \(\{u,c\}\) to an independent triple.  C-108 transports the
active move \(u\to x\), after which the opposite root vertex is either
already present or is the unique responder to one unoccupied attack.
Thus

\[
M_p=\{x,b,q\},\qquad M_q=\{x,p,c\}
\]

are genuinely retained.  This uses only fixed graph nonedges; it does
not interpret any missing response as a graph nonedge.

I exhaustively checked every mover at the attack \(b\) from \(M_q\).

- \(c\to b\) gives \(\{x,p,b\}\), which misses \(q\).
- If \(p\to b\) is retained, the resulting \(W=\{x,b,c\}\) has a unique
  response \(x\to u\) at the unoccupied target \(u\), reaching
  \(U=\{u,b,c\}\).
- If \(x\to b\) is retained, \(\{b,p,c\}\) either misses \(u\), when
  \(up\) is absent, or has the unique response \(p\to u\), again
  reaching \(U\).

These are all guards in \(M_q\).  Closure therefore forces \(U\).  From
\(U\), \(b,c\) miss \(r\) and \(ur\) is present, so the sole response is

\[
U\xrightarrow{u\to r}R=\{r,b,c\}.
\]

In AQ1, \(r\) misses the unoccupied target \(a\).  Every possible
retained response is by \(b\) or \(c\):

\[
\begin{aligned}
\{r,b,c\}&\to\{r,a,c\}\to\{p,a,c\}\to\{p,a,q\},\\
\{r,b,c\}&\to\{r,a,b\}\to\{q,a,b\}\to\{q,a,p\}.
\end{aligned}
\]

The latter two moves in each line are unique by the private ledger,
\(pq\notin E(G)\), and \(pr,qr\in E(G)\).  Both lines end at
\(S=\{a,p,q\}\).  This proves retention of \(S\), independently of
which response closure selects at \(a\).  The state \(S\) is independent,
and its attack at \(x\) is unoccupied and has the unique response
\(a\to x\), returning to \(T\).

## 3. C-064 directionality and the saturation proof

I recomputed every C-064 permutation as the ordered product of ridge
transpositions.  The directions in the candidate are correct.

For the retained AQ1 \(b\to a\) branch under the counterassumption
\(ac\notin E(G)\), the path

\[
\{r,a,c\}\to\{p,a,c\}\to\{p,a,q\}\to T
\]

induces

\[
(r\ p)(c\ q)(a\ x).
\]

It fixes the outside target \(b\).  Since \(p\in L_T(b)\), exact
covariance pulls the marker back to \(r\in L_{\{r,a,c\}}(b)\), impossible
because \(rb\notin E(G)\).  The symmetric path correctly forces \(ab\)
when closure selects \(c\to a\).

For QQ1 with \(a=x\), the counterassumption \(xb\notin E(G)\) makes the
attack \(x\) from \(R\) force \(c\to x\).  The independent path

\[
\{r,b,x\}\to\{q,b,x\}\to T
\]

induces \((r\ q)(b\ p)\) and fixes the outside target \(c\).  The end
marker \(q\in L_T(c)\) pulls back to the impossible
\(r\in L_{\{r,b,x\}}(c)\), since \(rc\notin E(G)\).  The symmetric
calculation proves \(xc\).

The clean-room incidence audit enumerated all \(2^5=32\) QQ1 and
\(2^7=128\) AQ1 assignments of the optional named edges.  In each row,
exactly one assignment survives every proved implication.  It has

\[
ab,ac,bc,xb,xc,up,uq\in E(G)
\]

with \(a=x\) in QQ1.  The first-obstruction counts sum to the whole
incidence space, so no optional named edge or branch was skipped.

The remaining short attack trees are sound.

- \(W=\{x,b,c\}\) misses \(r\) in QQ1.
- In AQ1, its three responses at \(a\) miss \(r,p,q\), respectively.
- If \(bc\) were absent, \(U\) would be independent and C-108 would force
  the excluded \(W\).
- If \(up\) were absent, all three \(b\)-responses from \(M_q\) are
  excluded; the symmetric \(c\)-attack from \(M_p\) forces \(uq\).

Every exclusion ends in a named missed vertex or in a further complete
one-guard attack tree.

## 4. The new activity and AQ1-to-QQ1 reduction

After saturation, complete the independent pair \(\{u,b\}\) to
\(I=\{u,b,s\}\).  The completion vertex cannot collide with
\(a,x,p,q,r,c\): the already proved edges

\[
ua,ux,up,uq,ur,bc
\]

exclude each possibility.  Hence every target in the following argument
is unoccupied.

C-108 first retains \(J=\{x,b,s\}\).  At its attack \(a\):

- an \(s\to a\) successor misses \(q\);
- a \(b\to a\) successor either misses \(q\), or its unique response at
  \(q\) produces \(\{x,a,q\}\), which misses \(p\);
- the only surviving response is \(x\to a\), retaining
  \(I-u+a=\{a,b,s\}\).

The independent audit separately enumerated all four assignments of
\(sa,sq\), so neither optional edge is silently assumed.  The retained
successor proves \(u\triangleright a\).

At the independent state \(S=\{a,p,q\}\), the particular
\(a\to u\) successor is the omitted state \(B\).  C-108 makes the
ability of the fixed responder \(a\) at target \(u\) invariant across
all independent triples containing \(a\), and therefore proves
\(a\not\triangleright u\).  This does not assert that \(S\) has no
response at \(u\); it asserts only that \(a\) is not a responder.

Relative to the new root \(S\), the complementary reverse endpoint is
still \(B\), with the same rank one.  The same attack \(r\) has movers
\(u,p,q\), misses \(a\), hits \(p,q\), and has the same three
non-dominating successors with witnesses \(a,b,c\).  Hence it is
literally QQ1.  No blocker, rank, or private-witness datum is lost in the
AQ1-to-QQ1 reduction.

## 5. Universal full-hit completion quantifier

The pair \(\{a,r\}\) is independent.  Since \(i=\alpha=3\), it cannot be
a maximal independent pair and therefore has a completion
\(d\in C_{ar}\).  Two nonadjacent completions would form an independent
four-set with \(a,r\), so \(C_{ar}\) is a nonempty \(G\)-clique.

For an arbitrary \(d\in C_{ar}\), the retained state
\(S=\{a,p,q\}\) dominates \(d\), so \(d\) hits at least one of \(p,q\).
The quantifier is genuinely universal: the proof uses no further
property of \(d\).  Moreover, after saturation \(d\) cannot coincide
with any named core vertex.

If \(d\) hits only \(p\), the independent ridge path

\[
S\to\{a,d,q\}\to\{a,d,r\}
\]

induces \((p\ d)(q\ r)\) and fixes \(c\).  The marker
\(q\in L_S(c)\) maps to \(r\in L_{\{a,d,r\}}(c)\), contradicting
\(rc\notin E(G)\).  If \(d\) hits only \(q\), the symmetric path maps
the marker \(p\in L_S(b)\) to the impossible response \(r\) at \(b\).
The four possible \(dp,dq\) patterns were independently enumerated:
zero hits fails domination, each singleton hit contradicts C-064, and
only two hits survives.  Thus every \(d\in C_{ar}\) is complete to
\(\{p,q\}\).

## 6. Independent fixed-graph evaluation

The review checker independently decodes

\[
G_0=\texttt{Hslaghb}
\]

using a fresh small-Graph6 parser.  It uses bit masks to exhaust all
subsets for \(\gamma,\alpha,i\), a disjoint clique-partition dynamic
program for \(\theta\), and a literal greatest-fixed-point deletion for
one-guard eternal domination.  It obtains

\[
(n,m;\gamma,i,\alpha,\gamma^\infty,\theta)
=(9,17;3,3,3,4,4).
\]

There are 45 dominating triples.  The greatest triple kernel deletes
24 states in the first round and the remaining 21 in the second.  At
four guards, 101 of 110 initially dominating states survive after
deletion rounds of sizes 8 and 1.  The independently decoded seven-core
edge set agrees exactly with the candidate.

This confirms that `Hslaghb` is a sharp static boundary control with an
empty three-guard kernel.  It is not a counterexample and carries no
minimum-order claim.

## 7. Model and scope ledger

| audit item | result |
|---|---|
| attacks only at unoccupied vertices | **PASS** |
| exactly one guard moves along one graph edge | **PASS** |
| every retained successor dominates | **PASS** |
| QQ1 collision \(a=x\) handled literally | **PASS** |
| all \(M_q\to U\to R\to S\) response branches exhaustive | **PASS** |
| all C-064 products and pullback directions correct | **PASS** |
| \(W\) exclusion complete in both rows | **PASS** |
| \(xb,xc,bc,up,uq\) short attack trees complete | **PASS** |
| \(u\triangleright a\) and \(a\not\triangleright u\) distinction correct | **PASS** |
| AQ1 recreates the same rank-one QQ1 blocker | **PASS** |
| full-hit theorem quantified over every \(d\in C_{ar}\) | **PASS** |
| no family omission treated as a graph nonedge | **PASS** |
| independent `Hslaghb` parameters and empty \(K_3\) | **PASS** |
| exclusion of the final canonical QQ1 core | **OPEN / NOT CLAIMED** |
| higher ranks, reciprocity, complete \(k=3\), conjecture | **OPEN / NOT CLAIMED** |

## Strict replay

Run:

```sh
sh gamma_theta_eternal_domination/reviews/rank_one_ur1_normalization_hostile/verify_strict.sh
```

Expected final line:

```text
rank-one ur=1 hostile review: PASS
```

The strict script checks the frozen candidate hashes, replays the
candidate's own exact-byte verifier, runs the clean-room 160-incidence
and fixed-graph audit, and compares its JSON output byte for byte.
