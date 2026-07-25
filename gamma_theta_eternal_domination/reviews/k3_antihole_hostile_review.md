# Hostile review: eliminating the \(k=3\) odd-antihole branch

## Verdict

**ACCEPT without correction.**

Lemma 1, Theorem 2, and the resulting order-12 three-template search split
are valid in the campaign's one-guard-moves model.  No critical-, high-,
medium-, or low-severity mathematical defect remains.  The previously
omitted lower bound is now stated explicitly as
\(\alpha(C_7)=3\leq\gamma^\infty(C_7)\).

This acceptance is relative to the Strong Perfect Graph Theorem and to the
already audited campaign lemmas named below.

Review date: 2026-07-25.

## Reviewed artifacts and dependencies

- `math/lemmas/k3_antihole_elimination.md`:
  `9e572203c09e082c3cbdfc0cdae8e4166007af3f909b73f7d8d2e196f04ddc4f`;
- `reviews/k3_antihole_hostile_probe.py`:
  `0eadbc484e2502ff73835baca153f4587216bf5b54d8833fb4c019c248d341a8`;
- `math/lemmas/maximum_independent_states.md`:
  `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e`;
- `math/reductions.md`:
  `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13`;
- `math/lemmas/k3_structural_day1.md`:
  `00d6fb851a3cb50ed907a593b0379376571251f8604974b5b67e05e2b0705d6e`;
- `math/lemmas/complement_k3_dictionary.md`:
  `54d7cafdc7047d75ed58739f6a773344a2f780aaecd0eafde8ed01a0692c6256`;
- local Goddard--Hedetniemi--Hedetniemi (2005) PDF:
  `46cf4f4516105514ddc362b77c3401f468b27505a7165aec0280e0983183ff7c`.

The probe is definition-level and imports neither campaign evaluator.

## 1. Model and citation audit

The cited primary source defines eternal 1-security by moving one guard from
a vertex equal or adjacent to the attacked vertex and requiring every
resulting guard set to dominate.  Its allowance of an occupied attack with
the guard at that vertex staying put is equivalent to the campaign convention
that attacks are restricted to unoccupied vertices: occupied attacks add no
constraint.

Theorem 3(a) of that paper, visibly checked in the archived source, states
that for odd \(n\),

\[
 \sigma_1(C_n)=\frac{n+1}{2},
\]

and attributes the result to Burger et al.  Thus the attribution and the
special value \(\gamma^\infty(C_7)=4\) are accurate.  The campaign note also
retains a self-contained proof, so its new structural consequence does not
depend solely on the citation.

## 2. Exact \(C_7\) proof

Three edges and a singleton form a clique partition of \(C_7\), and the
standard one-guard-per-clique strategy gives
\(\gamma^\infty(C_7)\leq4\).  The repaired sentence

\[
 \alpha(C_7)=3\leq\gamma^\infty(C_7)
\]

excludes one or two guards before the proof excludes three.

For a dominating triple, the cyclic gap lengths sum to four and each is at
most two.  The only multisets are therefore

\[
 \{2,1,1\}\quad\text{and}\quad\{2,2,0\}.
\]

Every triple of the second type is a dihedral image of
\(\{0,1,4\}\).  At the unoccupied attack \(3\), only guard \(4\) is adjacent
to the attacked vertex.  Its move produces \(\{0,1,3\}\), which leaves vertex
\(5\) undominated.  Hence no type-B triple can occur in an eternal
three-family.

The set \(S=\{0,2,4\}\) is an independent three-set and therefore maximum.
The accepted maximum-independent-state lemma forces \(S\) into any eternal
family of three-sets.  At attack \(1\), the only possible guards are \(0\)
and \(2\):

- moving \(0\) gives \(\{1,2,4\}\), leaving \(6\) undominated;
- moving \(2\) gives the forbidden type-B state \(\{0,1,4\}\).

Closure has no valid response, so no eternal three-family exists.

The independent probe found exactly 14 dominating triples, split into seven
of each gap type.  Literal greatest-fixed-point deletion returned no closed
three-family and a nonempty greatest four-family of size 28.  It also checked
the displayed clique partition and every failed successor directly.

## 3. Induced-subgraph and SPGT audit

Let \(H=\overline G\), with
\(\alpha(G)=\gamma^\infty(G)=3\), and suppose \(H\) is imperfect.  Then

\[
 \omega(H)=\alpha(G)=3.
\]

SPGT supplies an induced odd hole or odd antihole.  An odd antihole on
\(2q+1\) vertices has clique number

\[
 \omega(\overline{C_{2q+1}})
 =\alpha(C_{2q+1})=q.
\]

The ambient clique bound gives \(q\leq3\), while SPGT holes have length at
least five.  Only lengths five and seven remain.  The length-five antihole is
itself \(C_5\), already an odd hole.

If \(H\) contains an induced \(\overline{C_7}\), complementation on exactly
that vertex set makes \(G\) induce \(C_7\).  The accepted maximum-intersection
projection lemma gives induced-subgraph monotonicity in the correct direction:

\[
 \gamma^\infty(C_7)\leq\gamma^\infty(G).
\]

Lemma 1 would then force \(\gamma^\infty(G)\geq4\), contradicting the
hypothesis.  Thus the odd-antihole branch contributes no additional template,
and \(H\) must contain an induced odd hole.

There is no all-guards move, occupied-attack, complement, or inequality-
direction error in this chain.

## 4. Order-12 template conclusion

For a parameter-three counterexample, the accepted odd-wheel obstruction
makes every induced odd hole in \(H\) hub-free.  The complement dictionary
also says every vertex pair in \(H\) has a common neighbor.

The endpoints of a rim edge have no common neighbor on an induced hole of
length at least five, so they require an external common neighbor.  If the
hole had only one external vertex, that vertex would be adjacent to both
endpoints of every rim edge and hence to every rim vertex, making it a
forbidden hub.  At least two vertices therefore lie outside the hole.

At order 12 the hole has length at most 10.  The possible odd lengths at
least five are exactly

\[
 5,\ 7,\ 9.
\]

Consequently the synthesis search needs only the three overlapping branches

\[
 \text{induced hub-free }C_5,\qquad
 \text{induced hub-free }C_7,\qquad
 \text{induced hub-free }C_9.
\]

These branches are exhaustive but are not asserted to be disjoint.  The
conclusion is a structural reduction for the \(n=12,k=3\) target, not a
resolution of the universal conjecture.
