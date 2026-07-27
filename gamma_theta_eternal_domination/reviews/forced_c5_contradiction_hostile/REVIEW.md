# Hostile review: end-edge witness separation beyond the forced \(C_5\)

## Verdict

**PASS.**

I found no mathematical correction required in
`math/working/forced_c5_contradiction/NOTE.md` at SHA-256

`0c6a3de00f8e4daa53f4602c437ed51a22da911cfdff3f42445550b07e3430bb`.

The accepted claim boundary is exactly this:

> Let \(S=\{a,b,c\}\) be an independent state in an arbitrary specified
> one-guard eternal family \(\mathcal F\) of triples.  Suppose
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\), and an induced path
> \(x_0x_1x_2x_3\) in \(\overline G\) has exact family-response lists
> \[
> \{a\},\quad\{a,c\},\quad\{b,c\},\quad\{b\}.
> \]
> Then the end-edge common complement neighborhoods \(P_L,P_R\) are
> nonempty \(G\)-cliques, are disjoint from one another, and are disjoint
> from every co-state witness set \(Y_w\).  Together with the previously
> forced nonempty sets \(W,Z,Y_w\), this implies \(|V(G)|\ge 12\).

This is a conditional theorem about one exact mixed-\(P_4\) response pattern.
It does not exclude the pattern at order \(12\), prove the full \(k=3\)
slice, strengthen the general counterexample-order frontier, or resolve the
gamma--theta conjecture.  The note states these limitations correctly.

The arbitrary-family quantifier is sound.  No proof step replaces
\(\mathcal F\) by the greatest eternal family.  All family memberships used
below are obtained from an exact direct list, independent-state forcing,
one-guard closure, a previously proved arbitrary-family state, or exact
ridge covariance between independent states in this same \(\mathcal F\).

## Reviewed inputs

I re-read the target and the proof-bearing portions of:

- `math/working/k3_mixed_p4_attack.md`;
- `math/working/k3_mixed_witness_followup.md`;
- `math/working/cross_state_response_exchange.md`;
- `math/working/k3_projection_gluing.md`; and
- their hostile reviews.

The predecessor ledger used at target lines 58--157 agrees with the reviewed
predecessor results.  In particular, the states \(Q_L,Q_R,R_c,R_1,R_2\),
the nonempty witness systems \(W,Z,Y_w\), their stated externalities, and
the edges used by the new proofs all hold in the same arbitrary specified
family.

| artifact | SHA-256 |
|---|---|
| target note | `0c6a3de00f8e4daa53f4602c437ed51a22da911cfdff3f42445550b07e3430bb` |
| mixed-\(P_4\) predecessor | `3af645890638f07fa38b294def7967679e280a6447173aa320e8715da714d92c` |
| forced-\(C_5\) predecessor | `079c3ee0e880eb211f7e7460193e9c4c8212d70350965e668eb462f4f0a4db04` |
| ridge-covariance proof | `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7` |
| independent countermodel scan | `00ce6cfc78882c2f5e113786ecbc17fed5a9013ab89b2583f31823538c743b92` |
| bounded scan result | `b682d6ba2926afda6bafc9babadbecbe392395f7aaac3afa8e8e74778bd65409` |
| pinned `geng` | `588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1` |

## 1. Model, direct swaps, and restoration

Every attack in the new note is at a vertex outside the current triple.
Every displayed response replaces exactly one occupied vertex by the
attacked vertex, and the needed graph edge is either already in the ledger
or proved immediately before the move.

Negative direct-list entries are used correctly.  For an outside vertex
\(x\) and \(u\in S\),

\[
 S-u+x\in\mathcal F\quad\Longleftrightarrow\quad
 u\in L_S^{\mathcal F}(x).
\]

The reverse implication is the definition of the response list.  For the
forward implication, the family state \(S-u+x\) must dominate \(u\);
the two retained vertices of the independent state \(S\) miss \(u\), so
\(xu\in E(G)\).  Thus a negative list entry really does exclude the direct
successor state, not merely a preferred move.

The arbitrary-state restoration filter at target lines 147--157 is also
used with its exact quantifiers.  For any \(D\in\mathcal F\), choose each
missing reference vertex \(u\in S-D\) last in a restoration attack order.
Immediately before that last attack the state has form \(S-u+v\) for some
original outside position \(v\in D-S\), so
\(u\in L_S^{\mathcal F}(v)\).  This proves

\[
 S-D\subseteq\bigcup_{v\in D-S}L_S^{\mathcal F}(v).
\]

No successor is rejected merely because it is inconvenient; every
rejection in the target follows from exact family absence, restoration, or
failure of domination.

## 2. Audit of Lemmas 2.1 and 3.1

### Bridge alternatives

At target lines 174--199 the source

\[
D=\{a,b,x_1\}
\]

belongs to \(\mathcal F\), and \(x_3\notin D\).  There are exactly three
possible guard roles:

- \(x_1\to x_3\) has the forbidden successor
  \(S-c+x_3\);
- \(a\to x_3\), if retained, directly proves \(ax_3\in E(G)\);
- \(b\to x_3\), if retained, gives \(\{a,x_1,x_3\}\), which can dominate
  \(x_2\) only through \(a\), because both path guards miss \(x_2\).

Closure therefore proves \(ax_3\in E(G)\) or \(ax_2\in E(G)\).  Reversing
the path while exchanging \(a,b\) preserves the exact list table and gives
the second alternative.  This reflection is a relabeling of the same
argument and does not assume a graph automorphism.

### End-edge witnesses

Because \(\gamma(G)=3\), neither pair \(\{x_0,x_1\}\) nor
\(\{x_2,x_3\}\) dominates.  A missed vertex is respectively in \(P_L\) or
\(P_R\), proving both sets nonempty.  Every
\(\{p,x_0,x_1\}\) with \(p\in P_L\) is an independent triple.  Since
\(\alpha=3\), it is a maximum independent set and belongs to every eternal
triple family.  Two distinct vertices of \(P_L\) must be adjacent, or they
and \(x_0,x_1\) form an independent four-set.  The same argument handles
\(P_R\).

The externality list at target lines 284--294 is exhaustive:

- \(a,c\) see both left endpoints, while Lemma 2.1 makes \(b\) see at least
  one;
- \(x_2,x_3\) respectively see \(x_0,x_1\);
- every \(w\in W\) sees \(x_0\);
- every \(z\in Z\) sees \(x_1\); and
- the open neighborhoods exclude \(x_0,x_1\) themselves.

Reflection gives the right-end statement.  There is no circularity in the
restoration application: the proof explicitly establishes externality
independently and then obtains

\[
b\in L_S(p),\qquad a\in L_S(q).
\]

For distinct \(p,p'\in P_L\), the attack at \(p'\) from
\(\{p,x_0,x_1\}\) is unoccupied; both path guards miss \(p'\), while
\(pp'\in E(G)\).  Hence \(p\to p'\) is genuinely the unique response.

## 3. Audit of Theorem 3.2

Assume \(p\in P_L\cap P_R\).  Then \(p\) misses all four path vertices in
\(G\), and

\[
D_0=\{p,x_0,x_1\},\quad
D_1=\{p,x_1,x_2\},\quad
D_2=\{p,x_2,x_3\}
\]

are independent maximum triples in \(\mathcal F\).  The two covariance
steps and their domains are:

| ridge step | departing/entering vertices | transposition |
|---|---|---|
| \(D_0\to D_1\) | \(x_0,x_2\) | \((x_0\ x_2)\) |
| \(D_1\to D_2\) | \(x_1,x_3\) | \((x_1\ x_3)\) |

The transpositions are disjoint, so the composite is exactly

\[
\sigma=(x_0\ x_2)(x_1\ x_3).
\]

It maps \(D_0\) to \(D_2\), fixes \(p\) and the outside attack \(b\), and
keeps every intermediate attack in the outside domain required by the
ridge-covariance theorem.

Lemma 3.1 gives \(pb\in E(G)\), and the known state

\[
D_0-p+b=\{b,x_0,x_1\}=Q_L
\]

puts the role \(p\) in \(L_{D_0}^{\mathcal F}(b)\).  Exact covariance
therefore puts the same role in \(L_{D_2}^{\mathcal F}(b)\), forcing

\[
\{b,x_2,x_3\}\in\mathcal F.
\]

Restoration rejects this state because its missing reference positions are
\(\{a,c\}\), whereas

\[
L_S(x_2)\cup L_S(x_3)=\{b,c\}
\]

omits \(a\).  The contradiction is valid for an arbitrary \(\mathcal F\);
it does not require uniqueness of the response at either endpoint.

## 4. Audit of Theorem 4.1

Fix \(w\in W\) and suppose \(y\in Y_w\cap P_L\).

The state \(T_w=\{w,x_1,x_2\}\) dominates \(y\).  The guards \(w,x_1\)
miss \(y\), so \(yx_2\in E(G)\).  Likewise the state
\(R_c=\{c,x_0,x_3\}\) dominates \(y\); the guards \(c,x_0\) miss it, so
\(yx_3\in E(G)\).

Now consider

\[
E_0=\{y,x_0,x_1\},\quad
E_1=\{y,w,x_1\},\quad
E_2=\{w,x_1,x_2\}.
\]

All three are independent:

- \(E_0\) uses \(y\in P_L\);
- \(E_1\) uses \(y\in P_L\cap Y_w\) and \(w\in W\); and
- \(E_2=T_w\) is the accepted middle-ridge state.

They belong to \(\mathcal F\).  Membership of \(E_0,E_2\) follows from
independent-state forcing.  From \(E_0\), the unoccupied attack \(w\) has
the unique responder \(x_0\), because \(y,w\) and \(x_1,w\) are nonedges
and \(x_0w\) is an edge.  This forces \(E_1\).  From \(E_1\), the
unoccupied attack \(x_2\) has the unique responder \(y\), forcing \(E_2\).

The covariance ledger is:

| ridge step | departing/entering vertices | transposition |
|---|---|---|
| \(E_0\to E_1\) | \(x_0,w\) | \((x_0\ w)\) |
| \(E_1\to E_2\) | \(y,x_2\) | \((y\ x_2)\) |

Thus

\[
\tau=(x_0\ w)(y\ x_2)
\]

maps \(E_0\) to \(E_2\) and fixes the outside attack \(x_3\).  At \(E_0\),
the graph edge \(yx_3\) and the known successor

\[
E_0-y+x_3=R_1
\]

put \(y\) in the response list at \(x_3\).  Covariance transports it to the
role \(x_2\) at \((E_2,x_3)\), contradicting the path nonedge
\(x_2x_3\notin E(G)\).  All attacks are unoccupied and both covariance
steps are between independent family states.

The reflected proof is also valid.  Explicitly it assumes
\(y\in Y_w\cap P_R\), forces \(yx_1,yx_0\in E(G)\), and uses

\[
\{y,x_3,x_2\}\to\{y,w,x_2\}\to\{w,x_2,x_1\}
\]

with transpositions \((x_3\ w)\) and \((y\ x_1)\).  The attack \(x_0\)
and the successor \(R_2\) then transport the role \(y\) to the impossible
role \(x_1\), since \(x_1x_0\notin E(G)\).  This verifies that the brief
reflection at target lines 456--459 preserves every hypothesis.

## 5. Externality and the \(7+5\) count

Choose

\[
w\in W,\quad z\in Z,\quad p\in P_L,\quad q\in P_R,\quad y\in Y_w.
\]

The disjointness ledger is complete:

| chosen witness | already separated from |
|---|---|
| \(w\) | \(S\), the path |
| \(z\) | \(S\), the path, \(W\) |
| \(p,q\) | \(S\), the path, \(W\), \(Z\) |
| \(p\) versus \(q\) | Theorem 3.2 |
| \(y\) | \(S\), the path, \(W\), \(Z\), \(P_L\), \(P_R\) |

The predecessor proof of \(Y_w\cap Z=\varnothing\) is sound: every
\(y\in Y_w\) must see at least one of \(x_0,x_3\), whereas every
\(z\in Z\) misses both.  Hence the five witnesses are pairwise distinct
and external to the seven reference/path vertices.  The conclusion
\(7+5=12\) follows with no hidden assumption that any two witness sets are
singletons.

## 6. Countermodel attempts

I wrote a clean-room ordinary-set diagnostic,
`independent_countermodel_scan.py`, which imports no campaign evaluator or
transition helper.  It enumerates all unlabeled graphs, connected or not,
through order \(9\), filters exactly \(\gamma=\alpha=3\), and tests every
ordered reference triple and every ordered induced-complement \(P_4\).

The test covers proper eternal subfamilies, not only greatest families.  For
each graph and labeling it deletes precisely the six forbidden direct-swap
states from the set of all dominating triples and computes the greatest
one-guard-safe kernel.  Any eternal family realizing the exact lists is a
subset of this kernel by monotonicity; conversely, if the reference state
and six positive swaps survive, the kernel itself is such a family.  Thus
this is an exact existence test for a fixed tested graph and labeling.

The scan obtained:

| order | all unlabeled graphs | \(\gamma=\alpha=3\) | labelings reaching the kernel test | countermodels |
|---:|---:|---:|---:|---:|
| 7 | 1,044 | 53 | 0 | 0 |
| 8 | 12,346 | 317 | 0 | 0 |
| 9 | 274,668 | 3,349 | 112 | 0 |

As a nonvacuous positive control, the same code recovers the exact
21-state restricted kernel of `FDzro`, whose proper eternal family realizes
the mixed lists but has \(\gamma=2\).

This bounded scan found no counterexample, including no proper-family
countermodel, but it is supporting diagnostic evidence only.  It does not
cover orders \(10\) or \(11\), is not packaged as a proof-logged coverage
certificate, and is not used to establish the theorem.

Reproduction:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/forced_c5_contradiction_hostile/independent_countermodel_scan.py \
  --max-order 9
```

## 7. Exact nonclaims

This review does not accept any of the following:

1. the mixed response pattern is impossible at order \(12\) or above;
2. \(P_L\) has a prescribed adjacency relation with \(P_R\);
3. distinct \(Y_w\)-sets are disjoint;
4. the five witness systems force a thirteenth vertex;
5. every \(k=3\) equality graph avoids the mixed pattern; or
6. the universal gamma--theta conjecture follows.

Subject to this boundary, the target note passes adversarial review.
