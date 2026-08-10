# Adversarial referee report: arbitrary-subdivision promotion

## Verdict

**VERIFIED AFTER CORRECTION — scoped promotion theorem only.**

The arbitrary-subdivision step from the frozen n3/n4 fixed-full terminals to
complete port words is valid. No counterexample was found. Two formulations
were corrected:

1. every probe must remain bound to the exact terminal union
   `A = Q_s union Q_t` and its one transport; `Q_s` alone is unsafe when an
   ordinary triangle redirection changes a sink role;
2. the exact attained finite bound is **10 tensor ports**, not the historical
   crude bound 12. The old bound remains a valid overestimate, but it is not
   the exact certificate bound requested here.

This verdict uses the already independently verified local graph algebra as a
frozen input. It does not re-certify that algebra and does not, by itself,
prove the global level-2 identifiability theorem.

## Claim-by-claim result

| Claim | Status | Referee conclusion |
|---|---|---|
| Physical suppressed-path products | **VERIFIED** | Product classes are disjoint; the parameter restriction is an everywhere semialgebraic surjective submersion. The induced model marginal is submersive on a dense regular open source locus. |
| One-port common anchor | **VERIFIED AFTER CORRECTION** | True for the exact path-bound union `A=Q_s union Q_t`. Every one-port allowed transport extends its one fixed anchor transport. |
| Two-port total orders | **VERIFIED** | Conditional q transports extend their exact p parents. One-port locations plus all same-interval pair comparisons uniquely reconstruct every finite segment word, including empty and repeatedly subdivided segments. |
| Coherent ordinary `T` | **VERIFIED** | All 24 n3 `T` anchors have 5 allowed p and 30 allowed q descendants; all 840 remain `T` and restrict one anchor quotient map. Triangle-edge subdivisions are separated rather than mixed with probe-dependent redirections. |
| Finite tensor-port bound | **VERIFIED AFTER CORRECTION** | Anchors use at most 8 ports; p/q probes use at most 9/10. The ten-port stratum (one incoming plus nine outgoing) is attained by 38,016 n4 q relations. |
| Source-relative containment descent | **VERIFIED** | After shrinking inside the dense marginal-submersion locus, the marginal of a source-open germ is source-open and lies pointwise in the target restriction image. No continuous target preimage is chosen. |
| Nonstrong target restrictions | **VERIFIED AFTER CORRECTION** | The zero-character dummy grammar represents their tensors during restoration. Such a completion is not promoted as a standard-strong topology. Final anchored probes themselves retain the target support. |

## Exact inventory checked

- 144 n3 and 132 theta2-n4 path-bound anchors;
- 101,148 n3 and 168,582 n4 p/q relations;
- aggregate classes: 243,080 generic separators, 25,186 labelled
  isomorphisms, 840 ordinary `T`, and 624 strict separators;
- 10,516 n3 and 15,510 n4 parent-restricted allowed transports;
- all compact path ranges, packed p/q block partitions, clean-room
  compact/verbose bijections, and exact locked hashes;
- 68,584 n3 and 2,106 n4 final hard-cover role records against the
  incoming/sink/repair dummy grammar;
- all ordered words of three and four adversarial labels on 2, 5, and 6
  primitive segments: 5,394 presentations and no one-/two-probe collision.

The evidence package remains lightweight: no atlas generator, graph
canonicalizer, displayed-tree engine, or symbolic separator compiler was run.

## Adversarial attacks

All 16 theorem-logic mutations were rejected. They cover path deletion and
duplication, q truncation, nontrivial anchor automorphism, merged empty
segments, cross-anchor and child-transport corruption, cyclic pair orders,
probe-dependent `T`, triangle-sink transport change, overlapping path-product
classes, boundary parameters, omitted incoming/sink/repair roles, reversed
separator direction, and a false nine-port bound.

The attacks matter logically:

- without pointwise rigidity, one-port extensions need not share a map;
- isolated two-port decisions can form a cycle unless they restrict one
  actual target word;
- ordinary `T` cannot be chosen independently after a probe destroys the
  triangle;
- parameter-level openness fails if product classes overlap or leave the
  open JC cube;
- a zero/nonzero separator excludes only the directed containment for which
  its pullbacks were certified.

## Scope boundary

**Not decided here:** primitive-generator exhaustion, fixed-full local atlas
correctness beyond the frozen inputs, cut preservation, bridge peeling,
root reduction, no cross-blob compensation, or the final global theorem.

**Decided here:** once the verified fixed-full terminal hypotheses hold, no
new ambiguity or one-sided containment can appear solely from arbitrarily
long port subdivisions. A nonisomorphic/non-`T` full relation has a certified
separating marginal on at most ten tensor ports.

See `THEOREM_AND_PROOF.md` for the formal argument and
`certificates/promotion_audit_certificate.json` for the exact replay data.
