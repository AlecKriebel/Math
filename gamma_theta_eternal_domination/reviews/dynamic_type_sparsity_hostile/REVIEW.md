# Hostile review: dynamic-type sparsity

Review date: 2026-07-28 PDT

Candidate:
`math/working/dynamic_type_sparsity/NOTE.md`

Frozen candidate SHA-256:
`f3309daa2497a10c978fac28286959d6ec2fb52e8438c727cdf2eafce89aa1a7`

Manifest SHA-256:
`8d2515d6ee7078ba5ddadba02e159ab1dd00d74c7dc7811ea715c39298777727`

## Verdict

**UNCONDITIONAL PASS.**

Lemma 2.1, Theorem 3.1, and Corollary 4.1 are correct under their stated
hypotheses.  The two applications of the no-dominating-pair condition in
the single-sealed-positive argument exhaust both outside and anchor
witnesses.  The applications of C-094, C-082, and C-079 are within their
accepted scopes and preserve the exact one-guard model.

No missing response is treated as a graph nonedge.  The proof uses only
the valid direction

\[
 i\in L(t)\Longrightarrow it\in E(G)
\]

and its contrapositive when a literal complement edge is already known.
The final equality

\[
 L(t)=N_G(t)\cap S
\]

is obtained only after Theorem 3.1 proves the unique omitted-anchor
incidence is physical.

The exact scope is:

- an arbitrary eternal family of triples;
- a retained independent reference triple \(S\);
- \(\gamma(G)=3\); and
- every outside response list at \(S\) has exact size two.

The result proves universal physicality only within this exact-two-list
branch.  It does not cover singleton or full lists, prove satisfiability
of the response 2-CNF, transport clause edges, prove the complete
\(k=3\) case, or resolve the gamma--theta conjecture.

## 1. Exact model and list direction

The family-relative list is

\[
 L(t)=\{i\in S:S-i+t\in\mathcal F\}.
\]

If \(i\in L(t)\), the retained direct-swap state must dominate the omitted
anchor \(i\).  The other two members of the independent reference state
are nonadjacent to \(i\), so \(it\in E(G)\).  This proves the only
response-to-adjacency direction used in the note.

Closure from \(S\) makes every outside list nonempty: attack the
unoccupied outside vertex and record the responding anchor.  In the
unit-free no-full branch, the only possible list size is therefore two.
No all-guards move, occupied attack, or list/greatest-family conflation
appears.

The independent state and eternal triple-family also give

\[
 3\le\alpha(G)\le\gamma^\infty(G)\le3.
\]

Thus the equality prerequisites used by C-094 and C-082 are automatic;
they are not additional unproved assumptions.

## 2. Single sealed-positive exclusion

Let \(L(z)=\{i,j\}\) and \(S=\{i,j,k\}\), with

\[
 N_H(z)\cap P_i^+=\varnothing.
\]

Because \(\gamma(G)=3\), the pair \(\{j,z\}\) does not dominate.  A vertex
not dominated by a pair cannot be one of its occupied endpoints, so there
is \(w\notin\{j,z\}\) with

\[
 jw,zw\in E(H).
\]

The proof's first case split is complete.

### Outside first witness

If \(w\notin S\), the literal edge \(jw\in E(H)\) and the valid
contrapositive of list membership imply \(j\notin L(w)\).  The literal
edge \(zw\in E(H)\), together with sealing, implies
\(i\notin L(w)\): otherwise \(w\in P_i^+\) would be a complement neighbor
of \(z\).  Hence \(L(w)\subseteq\{k\}\), contradicting exact size two.

### Anchor first witness

If \(w\in S\), then \(w\ne j\) because \(j\) is a pair endpoint.
Moreover \(w\ne i\), since \(i\in L(z)\) forces \(iz\in E(G)\), while
the common-neighbor condition requires \(wz\in E(H)\).  Therefore
\(w=k\), and the proof obtains the literal edge

\[
 kz\in E(H).
\]

Now apply \(\gamma(G)=3\) to the distinct pair \(\{k,z\}\).  Its common
complement neighbor \(w'\notin\{k,z\}\) again has two exhaustive
locations.

- If \(w'\notin S\), then \(kw'\in E(H)\) gives
  \(k\notin L(w')\), while \(zw'\in E(H)\) and sealing give
  \(i\notin L(w')\).  Exact size two is impossible.
- If \(w'\in S\), it is not \(k\), the pair endpoint; it is not \(i\),
  because \(iz\in E(G)\); and it is not \(j\), because
  \(j\in L(z)\) forces \(jz\in E(G)\).  No anchor remains.

This proves Lemma 2.1.  It does not assume the two gamma witnesses are
distinct from one another, and it needs no three-cap collision argument.

## 3. From one dynamic port to a sealed positive

Let \(t\) be type \(i\) with a dynamic omitted incidence:

\[
 L(t)=S-\{i\},\qquad it\in E(G).
\]

Accepted C-094 applies in exactly this dynamic case.  It supplies distinct
outside vertices \(y,r\) with

\[
 ty,yr,iy,ir\in E(H),
\]

and with \(t-y-r\) a length-two path in the omitted-color projection
\(H[W_i]\).  The current proof uses only the first edge:

\[
 t,y\in W_i,\qquad ty\in E(H).
\]

This is the required mixed edge: \(t\) is dynamically adjacent to \(i\)
in \(G\), while \(iy\in E(H)\) is physical.  No complement edge is
transported from a merely equivalent Boolean representative.

Accepted C-082 now applies to the literal connector edge \(ty\).  Both
endpoints omit \(i\), and at least one endpoint—\(t\)—is adjacent to
\(i\) in \(G\).  Therefore C-082 supplies an **outside** common
complement neighbor \(z\) satisfying

\[
 tz,yz\in E(H),\qquad i\in L(z).
\]

The “outside” conclusion is essential and is justified by the dynamic
endpoint; the anchor \(i\) cannot be the cap.

To prove sealing, suppose \(p\in P_i^+\) and \(pz\in E(H)\).  Accepted
C-079 applies with

\[
 \text{positive tail }p,\quad
 \text{common port }z,\quad
 (v_0,v_1)=(t,y).
\]

The four literal complement edges are

\[
 pz,\ zt,\ zy,\ ty.
\]

The vertices are distinct:

- \(t\ne y\) comes from C-094;
- open-neighborhood edges make \(z\ne t,y\) and \(p\ne z\);
- \(i\in L(p)\), while \(i\notin L(t)\cup L(y)\), separates \(p\) from
  the path endpoints.

Thus this is precisely the forbidden length-one odd fan of C-079.  Hence

\[
 N_H(z)\cap P_i^+=\varnothing.
\]

The resulting \(i\)-positive sealed cap contradicts Lemma 2.1.  Therefore
no dynamic exact-two-list port exists.

## 4. No reversed response/nonedge inference

Every graph/list inference in the proof has one of these forms:

1. \(i\in L(t)\) forces \(it\in E(G)\), because a retained state must
   dominate the omitted anchor;
2. a previously established literal edge \(it\in E(H)\) implies
   \(i\notin L(t)\), by the contrapositive of item 1;
3. sealing plus a literal edge \(zt\in E(H)\) excludes
   \(i\in L(t)\); or
4. C-094, C-082, or C-079 supplies or consumes explicitly stated
   complement edges under its accepted hypotheses.

At no point does the proof start from \(i\notin L(t)\) and infer
\(it\in E(H)\).  In particular, the first physical edge \(iy\), the cap
edges \(zt,zy\), and the fan edges are all literal dependency outputs,
not reconstructions from missing responses.

## 5. Final anchor-incidence identity

For every outside vertex \(t\), exact size two gives a unique omitted
anchor \(i\).

- The two anchors in \(L(t)\) are \(G\)-neighbors of \(t\) by direct-swap
  domination.
- Theorem 3.1 makes the omitted incidence \(it\) an \(H\)-edge.

Those are all three anchors.  Therefore

\[
 L(t)=N_G(t)\cap S.
\]

This identity concerns only anchor incidences.  It neither determines nor
transports complement edges between outside vertices, exactly as the note
states.

## 6. Clean-room reconstruction of the `EFnG` control

The checker
`reviews/dynamic_type_sparsity_hostile/independent_check.py` imports no
candidate verifier, search code, graph library, or campaign evaluator.  It
independently decodes `EFnG` and confirms that the complement edge set is

```text
01 02 12 14 25 35
```

so the graph has order 6 and size 9.

It exhausts all vertex subsets for the static parameters, brute-force
colors the complement, and independently computes the greatest
one-guard fixed point for every \(k=1,\ldots,6\).  The result is

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\]

The greatest-kernel sizes for \(k=1,\ldots,6\) are

```text
0, 0, 18, 15, 6, 1
```

so the claimed greatest triple kernel has exactly 18 states and the
one- and two-guard kernels are empty.

The selected family has 12 distinct triples and the frozen serialization
hash

```text
36d6c1856e11d65da3bcd0fc453a4dea5c418bd520292638dd10169aec76885c
```

Every selected state dominates.  The checker replayed all 36 unoccupied
attack obligations and found 44 retained legal responses.

At \(S=\{0,1,2\}\), direct family membership gives

\[
\begin{array}{c|c|c}
v&L(v)&\text{omitted incidence}\\ \hline
3&\{1,2\}&03\in E(G),\\
4&\{0,2\}&14\in E(H),\\
5&\{0,1\}&25\in E(H).
\end{array}
\]

Thus vertex 3 is exactly one dynamic type-0 port, while vertices 4 and 5
are physical ports of the other two types.  This confirms the stated
\(\gamma=2\) sharpness boundary and not a counterexample to the
gamma--theta conjecture.

The six vertices are also the minimum possible number for a reference
triple plus three distinct displayed ports, one of each type.

## 7. Reproduction and hashes

Run:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/dynamic_type_sparsity_hostile/independent_check.py
```

The strict run is deterministic and warning-free under Python 3.14.6.
Exact candidate, manifest, dependency, control, and checker hashes are
recorded in `evidence.json`.
