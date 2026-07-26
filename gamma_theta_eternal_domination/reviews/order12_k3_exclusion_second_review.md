# Second independent review of the order-12, parameter-three exclusion

## Verdict

**`ACCEPT_NO_BLOCKER`.**

The frozen theorem note
`math/lemmas/order12_k3_exclusion.md`, SHA-256
`b6010d6f365a62845e24666603f6417d87f14c37876e3406dc2a7c6b6ee91ae4`,
correctly establishes the certificate-backed finite result
\[
 \nexists G,\quad |V(G)|=12,\qquad
 \gamma(G)=\gamma^\infty(G)=3<\theta(G).
\]

The first coverage review
`reviews/order12_k3_exclusion_hostile_review.md`, SHA-256
`ed4df8f2f0ec52198fda5240c0ef98c39184e58a3b62e6b97caa093e2640b3bd`,
also states the correct conclusion and scope.  This second review found no
unresolved mathematical, coverage, certificate, model-variant, or
claim-boundary blocker.

Review date: 2026-07-25 PDT.

## Independent checks

The audit checked the dependency chain rather than treating the first review
as evidence for itself.

- Component additivity first gives a counterexample component.  At total
  domination parameter three, the accepted minimum-parameter theorem forces
  that component to consume the whole domination budget; every other
  nonempty component would contribute at least one.  Hence the original
  12-vertex graph is connected, rather than merely having a smaller
  connected counterexample component.
- Equality collapse gives
  \(\gamma=i=\alpha=\gamma^\infty=3\).  For \(H=\overline G\), the directions
  are \(\omega(H)=\alpha(G)=3\) and
  \(\chi(H)=\theta(G)>3\).
- By the Strong Perfect Graph Theorem, \(H\) has an odd hole or odd
  antihole.  At clique number three, the only odd-antihole lengths are five
  and seven.  The five-antihole is \(C_5\); an induced
  \(\overline{C_7}\) in \(H\) induces \(C_7\) in \(G\), contradicting
  induced-subgraph monotonicity and the self-contained
  \(\gamma^\infty(C_7)=4\) proof.
- The odd-wheel obstruction makes every resulting odd hole hub-free.
  Since \(\gamma(G)=3\), every vertex pair of \(H\) has a common
  \(H\)-neighbor.  A rim edge has no common neighbor on an induced hole.
  If only one vertex were outside the hole, it would be adjacent to both
  endpoints of every rim edge and hence be a forbidden hub.  Thus at least
  two vertices are outside.  At order 12, the exhaustive odd-hole lengths
  are exactly \(5,7,9\).
- The accepted C-028 and C-030 graph-to-CNF implications quantify the same
  connected order-12, parameter-three universes for the hub-free \(C_9\)
  and \(C_7\) branches.  C-033 realizes every graph in the remaining
  hub-free \(C_5\) branch as a model of \(F_5\); C-031 transports the full
  assignment, including auxiliary variables, to a model of
  \(F_5\land S\).
- Edge variables consistently encode \(H=\overline G\).  A legal guard move
  therefore uses a negative \(H\)-edge literal, meaning one \(G\)-edge.
  Attacks range only over \(r\notin D\), one guard \(u\in D\) is replaced
  by \(r\), every selected state dominates, every selected successor is in
  the nonempty family, and no all-guards-move convention is imported.
- Clique partitions of \(G\) are proper colorings of \(H\).  The complete
  bank clauses use the correct positive-\(H\)-edge sign to express
  \(\chi(H)>3\).

The decisive C5 post-run stack is bound by:

| Artifact | SHA-256 |
|---|---|
| exact \(F_5\land S\) CNF | `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104` |
| addition-only binary RUP proof | `c6c24853e30073e66fb396441edb176a0160d062a8558e25fa18a955f33927c3` |
| independent post-run probe | `e480f7a27b5e5424b6ba7507a85a57144949f974b37351ee0872cca1ba8a7937` |
| canonical post-run log | `bd7693fdad225f733c0d2e704c4de45186324cc62ffdec09a112836ceec014e5` |
| activating post-run review | `060c65bbc5b08f562289dcf43e36924d34a0ae90ae2cc72c895c59b7eaf916a3` |

As part of this second review, the independent post-run probe was run
afresh.  It exited zero, performed a new warning-fatal forward RUP-only
checker replay, and reproduced the retained 24,943-byte canonical log
byte-for-byte, including SHA-256
`bd7693fdad225f733c0d2e704c4de45186324cc62ffdec09a112836ceec014e5`.

The final documentation audit corrected two non-mathematical descriptions:
mode `0700` belongs to the run directory rather than all twelve artifacts,
and the short package-auditor command is run from the campaign directory.
No frozen run file, proof, checker transcript, canonical audit log, theorem
statement, or proof dependency changed.

## Recommended C-035 wording

> **`CERTIFIED-FINITE`.** No finite simple graph \(G\) on 12 vertices
> satisfies
> \(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\).  Equivalently, the complete
> \((n,k)=(12,3)\) counterexample slice is empty.  This includes disconnected
> graphs, but does not exclude order-12 counterexamples with common parameter
> \(k\ge4\), any larger-order counterexample, or resolve the universal
> \(\gamma\)–\(\theta\) conjecture.

## Scope exclusions

This review does not certify:

- any order-12 slice with common parameter \(k\ge4\);
- absence of counterexamples through order 12;
- any larger order;
- a universal graph-class or all-graphs theorem;
- a counterexample; or
- resolution of the \(\gamma\)–\(\theta\) conjecture.

The appropriate classification is `CERTIFIED-FINITE`, not `PROVED`, because
the three branch exclusions ultimately depend on exact finite proof
certificates.
