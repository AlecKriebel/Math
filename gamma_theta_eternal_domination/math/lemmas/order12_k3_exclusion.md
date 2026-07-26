# Certified complete exclusion of the order-12, parameter-three slice

## Status and activation gate

This note proves the complete mathematical implication from the accepted
structural and finite branch results to the order-12, parameter-three
conclusion.  Its final certificate premise is:

> **C5 certificate premise \(P_5\).**  The exact DIMACS formula
> `results/synthesis_k3_hole5_signature_package/instance.cnf`, with
> SHA-256
> `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104`,
> is UNSAT by an independently accepted proof certificate.

The formula in \(P_5\) is the exact \(F_5\land S\) formula from C-031 and
C-033.  It has 6,886 variables, 23,968 clauses, 192,169 literals, and
754,323 bytes.

The two Git revisions have distinct provenance roles:

- `6f3ef0a0970b7214c34018fe32ea1ceeb5764d17` is the exact
  source/run-gate revision against which the production configuration
  reports `runtime_sources_match_head=true`;
- `dff45f4239e4acabc461533a0a213beec18ec56d` is the later immutable
  artifact-freeze revision that adds the 12 provisional run files without
  changing their payload bytes.

The artifact-freeze revision is not treated as a second execution revision,
and the runner is not used as proof evidence.  These revisions bind
provenance only; the independent proof replay required below is the
mathematical certificate gate.

For campaign claim promotion, \(P_5\) was defined to activate only when the
independent post-run review
`reviews/hole5_binary_production_postrun_hostile_review.md` existed and its
primary verdict was exactly

`ACCEPT_C5_UNSAT_CERTIFICATE_FOR_C033`.

That verdict must bind the exact CNF above, independently parse the exact
proof, independently rerun a warning-fatal forward RUP-only checker against
those same CNF and proof bytes, and accept the result as an UNSAT certificate
usable with C-033.  A solver result, runner-generated outcome, checker
transcript without clean-room replay, or audit of the runner itself does not
activate \(P_5\).

That gate is now satisfied.  The final clean-room artifacts are:

| Artifact | SHA-256 |
|---|---|
| independent post-run probe | `e480f7a27b5e5424b6ba7507a85a57144949f974b37351ee0872cca1ba8a7937` |
| deterministic canonical log | `bd7693fdad225f733c0d2e704c4de45186324cc62ffdec09a112836ceec014e5` |
| human-readable hostile review | `060c65bbc5b08f562289dcf43e36924d34a0ae90ae2cc72c895c59b7eaf916a3` |

The probe imports neither the production runner nor any synthesis module.
It independently reconstructs the exact formula, parses the raw and
addition-only binary proofs, confirms their byte-exact addition-subsequence
relation, reruns the separate accepted parser, and freshly replays the
addition-only proof with warning-fatal forward RUP-only checking.  Two final
full passes produced byte-identical canonical logs.  The checker exited zero,
used zero RAT lemmas, emitted empty stderr, and reported `s VERIFIED`.

Therefore \(P_5\) is accepted and the theorem below is an unconditional
`CERTIFIED-FINITE` result relative to the cited accepted mathematical
theorems and exact certificates.

All eternal-domination statements use the standard one-guard-moves model:
attacks are only at unoccupied vertices, and one guard moves along one edge
to the attacked vertex.

## The finite theorem

**Theorem 1 (order 12, parameter 3).**  No finite simple graph \(G\) on
12 vertices satisfies
\[
  \gamma(G)=\gamma^\infty(G)=3<\theta(G).
\tag{1}
\]
Equivalently, the complete
\((n,k)=(12,3)\) counterexample slice is empty.

The theorem includes disconnected graphs.  The proof below first shows that
any graph satisfying (1) would necessarily be connected; connectedness is
not silently imposed as an additional search restriction.

## 1. Equality collapse and the disconnected case

Suppose that \(G\) satisfies (1).  The accepted parameter chain
\[
 \gamma(G)\le i(G)\le\alpha(G)\le\gamma^\infty(G)\le\theta(G)
\]
gives
\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=3.
\tag{2}
\]

We now discharge disconnectedness without changing the order or losing the
parameter-three hypothesis.

Let \(G_1,\ldots,G_t\) be the nonempty components of \(G\), and write
\[
 a_j=\gamma(G_j),\qquad
 b_j=\gamma^\infty(G_j),\qquad
 c_j=\theta(G_j).
\]
The three parameters are additive over components, and the parameter chain
gives \(a_j\le b_j\le c_j\) for every \(j\).  Equality
\(\sum_j a_j=\sum_j b_j=3\) forces \(a_j=b_j\) componentwise.  The strict
inequality \(\sum_j b_j<\sum_jc_j\) then supplies a component \(G_q\) with
\[
 \gamma(G_q)=\gamma^\infty(G_q)<\theta(G_q).
\tag{3}
\]
Thus \(G_q\) is itself a counterexample.

The accepted minimum-parameter theorem says that every counterexample has
common parameter at least three.  Hence
\(\gamma(G_q)=\gamma^\infty(G_q)\ge3\).  But
\[
 3=\gamma(G)=\sum_j\gamma(G_j),
\]
and every nonempty component has domination number at least one.  Therefore
\(\gamma(G_q)=3\) and there is no other component.  Thus \(t=1\) and \(G\)
is connected.

This argument is stronger than merely extracting a smaller connected
counterexample: at total parameter three, the counterexample component
exhausts the entire domination budget, so no isolated vertex or other
component can remain.

## 2. The exhaustive complement split

Put \(H=\overline G\).  Equation (2) and
\(\theta(G)=\chi(H)\) give
\[
 \omega(H)=\alpha(G)=3<\chi(H).
\tag{4}
\]
Thus \(H\) is imperfect.

C-017, relative to the Strong Perfect Graph Theorem, eliminates the only
additional parameter-three odd-antihole branch.  More explicitly, an odd
antihole in \(H\) has length five or seven because
\(\omega(H)=3\); the five-antihole is \(C_5\), while an induced
\(\overline{C_7}\) in \(H\) would give an induced \(C_7\) in \(G\), contrary
to \(\gamma^\infty(G)=3\) because
\(\gamma^\infty(C_7)=4\) and eternal domination is monotone on induced
subgraphs.  Consequently \(H\) contains an induced odd hole.

C-014 says that \(\gamma^\infty(G)=3\) forbids an induced odd wheel in
\(H\).  Hence every induced odd hole in \(H\) is hub-free: no outside vertex
is adjacent in \(H\) to every rim vertex.

It remains to bound its length.  Since \(\gamma(G)=3\), no two vertices
dominate \(G\).  In the complement dictionary, this says that every pair of
vertices of \(H\) has a common \(H\)-neighbor.  The endpoints of a rim edge
of an induced cycle of length at least five have no common neighbor on the
rim.  They therefore have a common neighbor outside the hole.  There cannot
be only one vertex outside: that vertex would have to be a common neighbor
of the endpoints of every rim edge and hence would be a hub.  Thus at least
two vertices lie outside the hole.

Since \(|V(H)|=12\), the hole has length at most ten.  Its length is odd and
at least five, so the three exhaustive, possibly overlapping cases are
\[
  C_5,\qquad C_7,\qquad C_9,
\tag{5}
\]
each induced and hub-free in \(H\).

## 3. Exclusion of all three branches

The \(C_9\) branch is empty by C-028.  Its accepted graph-to-CNF theorem,
sealed formula, addition-only RUP proof, standalone replay, and hostile
review certify that no connected order-12 target satisfying (2) and
\(\theta(G)>3\) has a hub-free induced \(C_9\) in its complement.

The \(C_7\) branch is empty by C-030.  Its accepted exact full-bank CNF and
addition-only RUP proof received two strict warning-free RUP-only replays,
and its independent graph-to-CNF audit covers exactly the same connected
order-12 target with a hub-free induced \(C_7\).

Suppose finally that \(H\) contains a hub-free induced \(C_5\).  C-033
constructs, from the actual graph and an actual one-guard eternal
three-family, a satisfying assignment of the retained complete-bank formula
\(F_5\).  It assigns:

1. the edge variables from \(H\);
2. one actual common-neighbor witness for every vertex pair;
3. exactly the members of a nonempty eternal family to the family variables;
4. one legal, one-edge, one-guard response for every selected state and
   every unoccupied attack; and
5. every complete coloring-bank clause using
   \(\chi(H)=\theta(G)>3\).

C-031 proves that every satisfying assignment of \(F_5\) has a full-variable
\(S_6\)-orbit representative whose six outer adjacency signatures are
sorted.  Therefore C-033 gives a satisfying assignment of the exact
\(F_5\land S\) formula whose SHA-256 is the hash in \(P_5\).

The accepted premise \(P_5\) says that those exact bytes are unsatisfiable.
This is a contradiction.  Hence the \(C_5\) branch is empty as well.

The three cases in (5) are exhaustive, so all lead to contradictions.
Theorem 1 follows. \(\square\)

## 4. Exact dependency bindings

The proof above uses the following currently accepted bytes.

| Role | Artifact | SHA-256 |
|---|---|---|
| parameter chain, additivity, connected reduction, minimum parameter | `math/reductions.md` | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` |
| odd-wheel and order-12 template split, C-014 | `math/lemmas/k3_structural_day1.md` | `00d6fb851a3cb50ed907a593b0379376571251f8604974b5b67e05e2b0705d6e` |
| hostile acceptance of C-014 | `reviews/k3_structural_hostile_review.md` | `f2b0ce3d551576d5050bb03c7e8699bdffdb3ae35fbf5d3cf4b28c4e4ab270bc` |
| antihole elimination, C-017 | `math/lemmas/k3_antihole_elimination.md` | `9e572203c09e082c3cbdfc0cdae8e4166007af3f909b73f7d8d2e196f04ddc4f` |
| hostile acceptance of C-017 | `reviews/k3_antihole_hostile_review.md` | `7837fb360328533ea58a31d1a0eb60ef279a67d1e610144eb5206661ef38f5e3` |
| C-028 graph implication | `math/lemmas/hole9_template_exclusion.md` | `4305dcfc170f665d0c97b5d4601c3dd226099b61e11a2ad28a15fc66ee36c1f2` |
| C-028 acceptance record | `results/synthesis_k3_hole9_orphan_recovery_acceptance.json` | `ebede11b90e6e0b73d75f57c7706ba2e62e699281fcd8c15a208886dd53db291` |
| C-028 graph-theoretic hostile review | `reviews/hole9_template_exclusion_hostile_review.md` | `e17707945f3420c4ba2ecb6b3056b14789e2648e12e4c641772dfb7cee6452b7` |
| C-030 accepted hostile review | `reviews/hole7_addition_only_hostile_review.md` | `b904fcec9df16eff06640f36241a7589e1686777a57b7f32f9825832a8cecaa2` |
| C-030 exact CNF | `results/synthesis_k3_template_bank_packages/hole7/instance.cnf` | `6a011e685e58ef517f2ab8253ca40987bd7b742a470bedbacdc3a5e94fc995a7` |
| C-030 addition-only RUP proof | `certificates/synthesis_k3_hole7_full_bank_seed0_addition_only_v2/proof/addition-only.rup.drat` | `e8052df40d3e0c39b945a8735889039daba55eacc351e1822828b3d94f7baae9` |
| signature equisatisfiability, C-031 | `math/lemmas/hole5_signature_symmetry.md` | `8f8192774c3de65c2468115cc2d4aadd392fa7a1f73261c23fa49886d9c183e8` |
| hostile mathematical acceptance of C-031 | `reviews/hole5_signature_symmetry_hostile_review.md` | `169b99e083fe2079b3957de3095591142162aca76a10b42f9bb61266775ef223` |
| postcommit implementation binding for C-031 | `reviews/hole5_signature_symmetry_implementation_binding_addendum.md` | `0dd77b3d9012cbed92f402224f6f6f737f5464f16ca39856df74a97fc65d3cc0` |
| accepted exact \(F_5\land S\) package audit | `reviews/hole5_signature_package_hostile_review.md` | `b675ed1ba1e83a37069af4f3f526a98b3c627d1133300b1e5764fe933fa7b5ed` |
| C-033 conditional graph realization | `math/lemmas/hole5_template_exclusion_conditional.md` | `dee226088d17c2564da406f4e675a71f2d160cc678805e360e2ef51398b7e26b` |
| hostile acceptance of C-033 | `reviews/hole5_template_exclusion_conditional_hostile_review.md` | `c63613befffa7bd506691d6e8cdc48bd5dd72d3de947cec5834cdbf484b62405` |
| exact certified \(F_5\land S\) CNF | `results/synthesis_k3_hole5_signature_package/instance.cnf` | `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104` |
| C5 preserved raw binary proof | `results/synthesis_k3_hole5_signature_seed0_600s_binary/proof.raw.bdrat` | `c17ed1ee2782270ed861462ae7bdd94420a2079edf419a7d778d7096a67d1be4` |
| C5 certified addition-only binary proof | `results/synthesis_k3_hole5_signature_seed0_600s_binary/proof.additions.bdrat` | `c6c24853e30073e66fb396441edb176a0160d062a8558e25fa18a955f33927c3` |
| pinned strict proof checker | `tools/drat_trim_2023_05_22/drat-trim` | `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb` |
| C5 independent post-run probe | `reviews/hole5_binary_production_postrun_hostile_probe.py` | `e480f7a27b5e5424b6ba7507a85a57144949f974b37351ee0872cca1ba8a7937` |
| C5 deterministic post-run log | `reviews/hole5_binary_production_postrun_hostile_probe_log.json` | `bd7693fdad225f733c0d2e704c4de45186324cc62ffdec09a112836ceec014e5` |
| C5 activating hostile review | `reviews/hole5_binary_production_postrun_hostile_review.md` | `060c65bbc5b08f562289dcf43e36924d34a0ae90ae2cc72c895c59b7eaf916a3` |

The source/run-gate commit is
`6f3ef0a0970b7214c34018fe32ea1ceeb5764d17`; the provisional run-artifact
freeze is
`dff45f4239e4acabc461533a0a213beec18ec56d`.

The exact C-028 certified formula has SHA-256
`2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d`
and its addition-only RUP proof has SHA-256
`24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab`.
They are transitively bound by the C-028 acceptance and reviews above.

## 5. Promotion wording and scope

Since \(P_5\) is activated, the finite claim supported by this note is:

> **`CERTIFIED-FINITE`.**  No graph \(G\) on 12 vertices satisfies
> \(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\).  Equivalently, the complete
> order-12, parameter-three counterexample slice is empty.

By (2), the same statement may display
\(\gamma=i=\alpha=\gamma^\infty=3<\theta\).  The connected and unrestricted
order-12 formulations are equivalent here by Section 1.

This finite result does **not**:

- exclude order-12 counterexamples with common parameter \(k\ge4\);
- prove that no counterexample exists through order 12;
- address any higher order;
- prove a graph-class theorem; or
- resolve the universal \(\gamma\)--\(\theta\) conjecture.
