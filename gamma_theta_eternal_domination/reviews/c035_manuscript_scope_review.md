# Independent mathematical and scope review of the C-035 manuscript

## Binding and verdict

**Verdict: `ACCEPT_NO_MATHEMATICAL_OR_SCOPE_BLOCKER`.**

This review binds the following exact manuscript bytes:

| Artifact | SHA-256 |
|---|---|
| `paper/c035_order12_k3/main.tex` | `dddf4a1b4aebed71a1f44a7f30b39b2c5855e72fd797bd4439283d358e122204` |
| `paper/c035_order12_k3/main.pdf` | `f84430ee4319a3c914cfe4f6182cf62d9fc840d26e8d0501b863bd2cc995864e` |

The mathematical theorem, its finite scope, and the graph-to-certificate
implication agree with accepted claim C-035.  I found no remaining error in
the one-guard model, disconnected reduction, SPGT template split, CNF
coverage argument, or reported certificate bindings.

This is acceptance of the mathematical and certificate scope of the exact
bytes above.  It is not a new replay of the large proof streams and does not
replace the accepted branch-specific independent checkers.

## Claim and model

The manuscript states exactly the certified finite claim:

> No finite simple graph \(G\) on 12 vertices satisfies
> \(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\).

It repeatedly and correctly excludes the stronger claims that all
order-12 parameters, higher orders, or the universal conjecture have been
settled.  Its definition of an eternal family permits attacks only at
unoccupied vertices and requires exactly one guard to traverse one edge.
The formula description uses response variables only for \(r\notin D\),
requires the moving guard to be adjacent in \(G\), selects the one-replacement
successor, and subjects every selected successor to the domination clauses.
There is no import of the all-guards-move model.

## Mathematical coverage audit

The parameter-chain proof correctly gives
\[
\gamma=i=\alpha=\gamma^\infty=3
\]
for any putative target.  The induced-subgraph monotonicity proof is valid:
maximizing the number of guards in an induced subgraph prevents a response
from entering it, so attacks within it have responses from projected guards;
those same responses also prove domination of every projected state.

The component argument fully covers disconnected graphs.  Additivity and
the total equality \(\sum\gamma(G_j)=\sum\gamma^\infty(G_j)=3\) force
componentwise equality.  A component carrying the strict clique-cover gap
is itself a counterexample and hence has common parameter at least three.
It exhausts the total domination budget, so no other nonempty component can
exist.  Connectedness is therefore a theorem, not an unreported generator
restriction.

For \(H=\overline G\), equality collapse gives
\(\omega(H)=3<\chi(H)\).  The Strong Perfect Graph Theorem supplies an odd
hole or antihole.  The manuscript correctly reduces an odd antihole to
length five or seven; the former is \(C_5\), and the latter would induce
\(C_7\) in \(G\), contradicting induced-subgraph monotonicity and
\(\gamma^\infty(C_7)=4\).  The odd-wheel obstruction makes the resulting odd
hole hub-free.  Failure of every pair to dominate \(G\) gives every pair a
common neighbor in \(H\).  Applying this to every rim edge shows that an
odd hole in a 12-vertex target has at least two external vertices and hence
length at most nine.  Thus the possibly overlapping \(C_5,C_7,C_9\)
branches are exhaustive.

The displayed proof of
\(\gamma^\infty(\overline{C_n})=3\) uses the complement adjacency correctly:
vertices at cyclic distance two are adjacent in \(\overline{C_n}\), although
the resulting pair is nondominating because the intervening cycle vertex is
undominated.  Consequently the iterative forced-successor argument and its
final contradiction are sound.

## Graph-to-formula implication

For each branch, a target graph maps to the formula in the required
direction:

1. \(H\)-edges assign the 66 graph variables.
2. \(\alpha(G)=3\) satisfies every no-\(K_4\) clause in \(H\).
3. \(\gamma(G)=3\) supplies an actual common \(H\)-neighbor for every pair.
4. Connectedness and the selected hub-free induced cycle satisfy the cut
   and template clauses.
5. An actual nonempty one-guard eternal three-family assigns the family and
   move variables.
6. Independent triples of \(G\), equivalently triangles of \(H\), belong to
   every eternal three-family by the proved forcing lemma.
7. Since \(\theta(G)=\chi(H)>3\), every recorded coloring clause is true.

The last point is especially important for \(C_9\).  That formula contains
only 170 valid coloring clauses, not a complete three-coloring bank.  The
coverage proof needs only that every target with \(\chi(H)>3\) satisfies
each recorded clause; it does not claim that an arbitrary model of the
\(C_9\) formula has \(\chi(H)>3\).  The revised abstract now says that the
formulas contain “valid coloring clauses implied by the obstruction to a
three-clique partition.”  This is accurate and no longer suggests that the
170-row \(C_9\) list is complete.  The later explicit remark also states
that completeness is neither claimed nor needed.

The \(C_5\) outer-signature ordering is presented as an equisatisfiable orbit
restriction under the full \(S_6\) action, rather than as a logical
consequence.  Relabeling graph, witness, family, and move variables together
preserves the source formula, so the coverage argument loses no target.

## Exact finite bindings

I independently parsed the three bound DIMACS files and confirmed the
manuscript's formula counts and hashes:

| Branch | Variables | Clauses | Literals | Bytes | CNF SHA-256 |
|---|---:|---:|---:|---:|---|
| \(C_5\) | 6,886 | 23,968 | 192,169 | 754,323 | `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104` |
| \(C_7\) | 6,886 | 21,718 | 148,551 | 621,864 | `6a011e685e58ef517f2ab8253ca40987bd7b742a470bedbacdc3a5e94fc995a7` |
| \(C_9\) | 6,886 | 20,200 | 117,841 | 530,053 | `2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d` |

I also checked the retained proof byte counts, hashes, and ASCII line counts
where applicable against the accepted records:

| Branch | Additions | Proof bytes | Proof SHA-256 |
|---|---:|---:|---|
| \(C_5\) | 247,981 | 6,337,621 | `c6c24853e30073e66fb396441edb176a0160d062a8558e25fa18a955f33927c3` |
| \(C_7\) | 284,317 | 18,093,724 | `e8052df40d3e0c39b945a8735889039daba55eacc351e1822828b3d94f7baae9` |
| \(C_9\) | 4,705 | 65,906 | `24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab` |

These values match
`results/order12_k3_exclusion_acceptance.json` and the branch certificate
packages.  The manuscript accurately distinguishes the binary \(C_5\)
proof from the ASCII \(C_7\) and \(C_9\) proofs and accurately reports that
the accepted decisive replays used RUP only.

## Blockers and boundary

There are **no remaining mathematical or scope blockers** in the bound
source and PDF.  During review, the original abstract wording could have
been read as saying that the partial \(C_9\) coloring list completely
encoded non-three-colorability.  That wording was corrected before the
hashes above were frozen.

Author metadata and a permanent public archive identifier remain explicit
pre-submission placeholders.  They do not affect the mathematical
acceptance recorded here, but they must be supplied before external
submission.
