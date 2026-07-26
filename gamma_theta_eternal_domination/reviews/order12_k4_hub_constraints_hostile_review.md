# Hostile review: order-12, parameter-four hub constraints

**Verdict:** `ACCEPT_WITHOUT_SCOPE_INFLATION`

**Frozen author artifact:** `math/lemmas/order12_k4_hub_constraints.md`,
SHA-256
`aab7cc335fddc367375258b655cdf6a637e371adf1aeb731accf9186531ea00c`.

This verdict accepts the four stated lemmas as necessary conditions under the
note's hypotheses.  It does not promote them to a branch exclusion, an
order-12 finite result, or a theorem beyond the one-guard model.

## Proof audit

### Lemma 1

The characterization
\(\gamma^\infty(J)=1\) iff the nonempty graph \(J\) is complete is correct in
the stated unoccupied-attack, one-guard model.  Starting at any singleton in
an eternal family, attacking each other vertex both forces the corresponding
edge and puts the attacked singleton in the family.  Repeating from those
singletons forces every pair to be adjacent.  The nonempty hypothesis is
necessary and is present.

### Direction of induced-subgraph monotonicity

The direction used in Theorems 2 and 3 is correct:

\[
\gamma^\infty(G[S])\leq\gamma^\infty(G)
\qquad(S\ne\varnothing).
\]

For a direct check, take an eternal family of size \(k\) in \(G\), and among
its configurations minimize the number \(q\) of guards outside \(S\).  From a
configuration attaining this minimum, an attack in \(S\) cannot be answered
by moving an outside guard into \(S\), because the successor would be a family
member with fewer than \(q\) outside guards.  Hence a guard already in \(S\)
answers every such attack and the minimum-\(q\) configurations remain closed
under attacks in \(S\).  Their intersections with \(S\) all have size
\(k-q\).  They dominate \(G[S]\): otherwise an unoccupied vertex of \(S\)
with no inside guard neighbor could only be defended by an outside guard,
again contradicting minimality.  These intersections therefore contain an
eternal family for \(G[S]\).

This verifies that the displayed inequalities point from each induced
subgraph value upward to \(\gamma^\infty(G)\), as the note requires.

### Component additivity

The equality
\[
\gamma^\infty(J_1\mathbin{\dot\cup}J_2)
=\gamma^\infty(J_1)+\gamma^\infty(J_2)
\]
is used in the correct direction.  The upper bound combines eternal families.
For the lower bound, guards cannot cross components, so the guard count in
each component is invariant along every legal response sequence.  Projecting
responses to either component gives an eternal family of that component with
its allocated number of guards; summing the two lower bounds proves
additivity.

### Theorem 2

For a hub set \(X\), every \(G\)-edge between \(X\) and the odd-hole rim is
absent, so the induced graph really is
\(\overline C\mathbin{\dot\cup}G[X]\).  With the accepted one-guard identity
\(\gamma^\infty(\overline C)=3\), additivity and monotonicity yield
\[
3+\gamma^\infty(G[X])\leq4.
\]
When \(X\ne\varnothing\), Lemma 1 forces \(G[X]\) to be complete, equivalently
\(H[X]\) is independent.  The proof separately handles \(X=\varnothing\).

The result remains dependent on the previously accepted general odd-antihole
value; this note does not independently reprove that identity.  That is a
dependency, not a hidden extension of the claim.

### Theorem 3

If \(H[A]=\overline{C_7}\) and \(x\) is complete in \(H\) to \(A\), then
\(G[A\cup\{x\}]=C_7\mathbin{\dot\cup}K_1\).  The accepted
\(\gamma^\infty(C_7)=4\), additivity, and induced-subgraph monotonicity give
the impossible inequality \(5\leq4\).  Complement direction and the isolated
vertex contribution are both correct.

### Theorem 4 and edge cases

Property P3 is the exact complement formulation of “no three vertices
dominate \(G\).”  It follows from \(\gamma(G)=4\).

For a rim edge \(uv\) of an induced hole, no third rim vertex is adjacent in
\(H\) to both \(u\) and \(v\).  If all outside vertices are hubs, no other hub
can witness P3 for \(\{a,u,v\}\), because Theorem 2 makes hubs pairwise
nonadjacent.  If exactly one outside vertex \(y\) is not a hub, P3 forces that
same \(y\) to meet \(a\) and both ends of every rim edge, hence every rim
vertex, making \(y\) a hub after all.

The condition \(r\geq2\) is sufficient and used precisely where
\(t=r-1\) must leave a hub \(a\) to choose.  For \(r=2\) the conclusion is
the strong bound \(t=0\); for \(r=3\) it is \(t\leq1\).  No \(r=0\) or
\(r=1\) conclusion is silently imported.  Substitution of \(r=7\) for a
\(C_5\) and \(r=5\) for a \(C_7\) gives the stated order-12 bounds \(5\) and
\(3\).

## Independent finite probe

The clean-room probe
`reviews/order12_k4_hub_constraints_hostile_probe.py` implements the
one-guard greatest-fixed-point definition without importing a campaign
evaluator.  It checked:

- Lemma 1 and induced-subgraph monotonicity on all 1,099 labeled graphs
  through order five and all 32,767 nonempty induced-subgraph pairs;
- component additivity on 121 labeled component pairs of total order at most
  six;
- the P3 complement equivalence on 1,096 labeled graphs;
- the required values for \(C_7\) and the complements of \(C_5,C_7,C_9\);
- all \(2{,}048\) \(C_5\)-rim extensions with \(r=2\), and all \(262{,}144\)
  with \(r=3\), for the P3-plus-hub-independence conclusion.

All checks passed.  These finite checks are regression evidence only; the
proof audit above, not enumeration, supports the mathematical verdict.  The
exact run is recorded in
`reviews/order12_k4_hub_constraints_hostile_probe.log`.

## Claim boundary retained

The accepted consequences are redundant necessary filters:

- \(C_5\): at most five outside hubs, independent in \(H\);
- \(C_7\): at most three outside hubs, independent in \(H\);
- induced \(\overline{C_7}\): no outside vertex complete in \(H\) to the
  antihole.

They do not exclude any branch and do not license a fixed placement of the
hole, antihole, or anchored \(H\)-\(K_4\) without an orbit-complete argument.
