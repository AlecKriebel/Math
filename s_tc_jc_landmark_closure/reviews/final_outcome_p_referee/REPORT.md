# Final adversarial referee report for Outcome P

Reviewed commit: `5377048de2362da513ea427c0aa8e698e5617767`

Review date: 2026-08-12

Final decision: **UNRESOLVED**

## Executive decision

**UNRESOLVED.** I found no exact counterexample to the proposed strongly
tree-child theorem, and most structural layers survived independent attack.
However, Outcome P cannot be promoted or submitted from this commit. The first
load-bearing failure is the claimed independent exhaustiveness of the
three-outgoing directed local atlas. The clean-room verifier independently
checks every relation that it is given, but it obtains the purported complete
universe by loading the primary relation stream. It does not independently
generate the target completion grammar or the relative source--target
presentation universe.

**UNRESOLVED.** A second local gap occurs in the arbitrary-word promotion. The
probe certificate starts from the 144 hard-cover terminal paths, whereas the
bounded theorem also has 62 direct residual isomorphism/ordinary-`T` relations.
No submitted theorem or certificate proves that every one- and two-port
extension of those direct anchors is represented among the 144 path-bound
families. This is not a counterexample, but it leaves exactly the implication
needed to recover arbitrary port words unproved.

**FALSE as a release claim.** The two probe-extension summaries and their
large binding streams used by the arbitrary-subdivision gate are present only
as untracked workspace files and are absent from commit `5377048d`. Moreover,
`reproducibility/verify_quick.sh` fails immediately because
`FINAL_OUTCOME.json` is intentionally absent. A fresh clone cannot reproduce
the claimed active release.

The maximal defensible status is therefore:

> **UNRESOLVED:** the positive standard-strong classification remains a
> well-supported candidate theorem, conditional on closure of the two local
> atlas/promotion gaps. The frozen weak-but-not-strong sharpness theorem is
> **VERIFIED** and remains publishable independently.

## Exact first failure

**UNRESOLVED.** The first missing implication in dependency order is node
`A3/R` (complete three-outgoing directed relation universe).

1. `reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py:2089--2112`
   resolves the primary relation path and executes
   `relations = list(iter_jsonl(relation_path))`.
2. The clean-room source contains no independent call implementing the target
   completion grammar, marginalized incoming completions, or all relative port
   permutations.
3. Its independent source-support partition audit proves only that every
   source support occurs in the loaded stream. Its relation fingerprints prove
   only that loaded records are distinct and internally bound.
4. Deleting a relation is rejected against a pinned primary count/hash; that
   mutation does not prove that the pinned set was mathematically exhaustive.
5. `reviews/proof_first_inventory_exhaustiveness/REVIEW.md` correctly records
   the upstream Fourier-signature collision selection as unresolved in that
   package.

The bounded scope audit in `n3_scope_certificate.json` reproduces the key
facts without importing project code: 10,466 relations are loaded; no target
grammar-generation call is present; and the classes are 5,284 strict, 5,120
pending, and 62 direct residual relations.

## Claim-by-claim verdict

| Load-bearing claim | Verdict | Referee conclusion |
|---|---|---|
| Locked `sd_0` topology class | **VERIFIED AFTER CORRECTION** | The exact class is the already-simple binary LSA-rootable reticulation-preserving `sd_0` class, not every preimage of a broader cleanup convention. |
| `S_TC` criterion | **VERIFIED AFTER CORRECTION** | The criterion in `docs/DEFINITIONS_LOCK.md` is sound: every tail of a retained reticulation edge must be incident with two undirected edges. The manuscript paraphrase at lines 226--230 is inaccurate and must be replaced. |
| At most one triangle per strong level-2 blob | **VERIFIED** | Cycle/theta reduction leaves only `(1,1,2)` and `(1,2,2)` as two-triangle possibilities; the former is nonsimple and the latter has no tree-child admissible rooting. |
| Root reduction | **VERIFIED AFTER CORRECTION** | A real leaf-bearing incoming boundary exists for each factor; source and target incoming boundaries are chosen independently. The proof does not require a common physical incoming port. |
| Pointwise cut theorem | **VERIFIED** | Cut iff flattening rank is at most four holds throughout the open JC cube. Both one-active and two-active crossings have exact strict certificates. |
| Both cut inclusions under one-sided containment | **VERIFIED** | Pointwise rank separation, rather than symmetric-overlap reasoning, gives equality of cut splits. |
| Ordinary median versus three-sunlet decoration | **VERIFIED** | `F=abc-t^2` is zero for the ordinary endpoint and strictly positive for the open sunlet endpoint. |
| Full bridge incidence kernel | **VERIFIED** | The exact fiber is the full incidence-scaling action. The reciprocal-only chart and physical bridge recovery remain correctly withdrawn. |
| Analytic projective slices and no bridge holonomy | **VERIFIED** | Positive rank-one factorization plus the degree-at-least-three anchor matrix gives local slices; the reduced bridge graph is a tree. |
| Finite-union localization/no cross-blob compensation | **VERIFIED, conditional on the local theorem** | Intrinsic projective extraction and semialgebraic finite-union dimension localize a source-open subgerm without choosing target parameters continuously. |
| Primitive cycle/four-theta universe | **VERIFIED** | The cyclomatic/degree proof is structural and the support repairs are independently checked. |
| Complete n3 directed relation universe | **UNRESOLVED** | Recordwise graph, Fourier, sign, and iso/`T` checks pass, but independent target/presentation exhaustiveness has not been implemented. |
| n3 strict and terminal algebra | **VERIFIED, conditional on the frozen relation universe** | All loaded strict pullbacks/signs, 5,344 root bindings, restoration paths, and 34-isomorphism/28-`T` direct residual classifications replay exactly. |
| Five-port `theta_2` signature gate | **VERIFIED** | Independent generation gives the exact `18+42+132` partition. The 42 selected-incoming cases are presentation duplicates with explicit mixed-graph transports; the 132 marginalized cases equal the fixed root multiset. |
| Fixed-full restoration direction | **VERIFIED** | Every restoration prefix is a marginal of one already fixed full relation; no containment is lifted from a smaller marginal. |
| Marginal submersion | **VERIFIED** | Disjoint positive path-product classes give full row rank and an onto semialgebraic map on the open cube. |
| Common anchor and coherent probes | **VERIFIED only for the 144 n3 and 132 n4 path-bound anchors** | The submitted streams prove fixed transport, segment location, pair order, and coherent `T` on those anchors. They do not certify the 62 direct n3 anchors. |
| Arbitrary-subdivision local theorem | **UNRESOLVED** | It depends on both the missing n3 universe generation and the missing direct-anchor probe crosswalk. |
| Ordinary three-sunlet germ | **VERIFIED** | All 64 Fourier coordinates agree at a strict rational point and each orientation has rank four, the normalized ambient dimension. |
| Embedded ordinary-`T` contraction | **VERIFIED AFTER CORRECTION** | The argument is valid once local analytic sections and the chain-rule rank step are stated explicitly; see the exact manuscript patch below. |
| Global necessity and converse gluing | **VERIFIED, conditional on the complete local theorem** | Correct bridge extraction localizes necessity; common local germs and effective bridge intervals glue with a local inverse and full rank. |
| Proper algebraic exceptional locus | **VERIFIED AFTER CORRECTION, conditional on the main theorem** | The finite-union argument is sound, but “critical-value closures” must mean images of loci where rank drops below generic model rank, and observable atlas factors must be specified. |
| Structural reconstruction | **VERIFIED as a terminating conditional algorithm** | Cut tests, finite bounded probes, and canonicalization terminate. The stated input-size caveat is appropriate; no physical bridge multiplier is recovered. |
| Frozen weak `W_TC\setminus S_TC` theorem | **VERIFIED** | The exact four-leaf equality, strict algebraic point, two rank-eight minors, topology census, and all-`n` leaf-substitution inverse replay. It is sharpness evidence only and is not an `S_TC` move. |

## The direct-anchor promotion gap

**UNRESOLVED.** The paper's bounded lemma has two equality exits:

- 144 terminal paths reached after fixed-full restoration; and
- 62 direct residual relations (34 isomorphisms and 28 ordinary `T`).

The active n3 probe summary has exactly 144 base terminal paths. Every probe
binding names `primary/certificates/hard_cover_schema3_n3_full_summary.json` as
its base, and no binding carries a direct bounded-relation id. Thus the
sentence “after fixing one anchor transport” has only been algebraically
certified for the restoration-terminal case.

Pointwise rigidity alone is insufficient. It proves uniqueness of a core map
*after* a one-port marginal is known to be isomorphic or `T`-related; it does
not prove that source-relative JC containment of that marginal forces such a
topological relation. The missing closure can be supplied in either of two
ways:

1. prove, with explicit normalized transports, that every direct-anchor
   `A+p` and `A+p+q` relation surviving the invariant filter is represented by
   one of the existing terminal probe relations; or
2. independently compile and certify the direct-anchor one- and two-port
   relation families.

Until one of these is done, the arbitrary-word theorem and therefore the
global classification remain unresolved.

## Consistency review of `source/paper/main.tex`

### Lemma 6.4 (embedded ordinary `T`)

**VERIFIED AFTER CORRECTION.** The intended contraction argument is correct,
including when the unchanged context is the complementary theta path. Tensor
equality is preserved by contraction. Rank four of each three-sunlet map gives
local analytic sections over one common open tensor neighborhood. If `d` is
the generic rank of the common analytic contraction `Phi(Q,C)`, a nonzero
`d`-minor cannot vanish on the nonempty open common product. At a point where
it is nonzero, composing with either local section gives physical rank `d` on
both sides. This yields one common full-dimensional regular blob germ.

The current lines 785--794 omit the local sections and chain-rule sentence and
say that the generic-rank locus meets an open product “on which the full model
has that generic rank,” which is too close to assuming the desired step.

**Exact patch request:** replace the second paragraph of the proof by:

> Let `f_i: Theta_i -> Q` be the normalized triangle-tensor map for
> orientation `i`. Since `df_i` has rank four, after shrinking about the
> certified point the constant-rank theorem gives a common open tensor
> neighborhood `U` and analytic local sections `s_i:U->Theta_i`. For the
> unchanged context let `Phi(Q,C)` be the common tensor contraction, and let
> `d` be its generic rank. A `d`-minor of `D Phi` is a nonzero analytic
> function on the connected ambient tensor--context chart, so it cannot
> vanish on the nonempty open set `U x C`. Choose `(Q,C)` in that set where
> the minor is nonzero. The chain rule applied to `(s_i(Q),C)` shows that both
> physical blob parameterizations have rank `d` there. Shrinking once more,
> `Phi(U x C)` is a common `d`-dimensional regular germ, equal to the full
> local model dimension on both sides.

### Exceptional locus

**VERIFIED AFTER CORRECTION.** Lines 830--850 have the right finite-topology
strategy, but the extra exceptional sets are not defined precisely enough.

**Exact patch request:** define `d_N=dim V_N`, replace “critical-value
closures” by “the Zariski closures of images of parameter loci on which the
Jacobian rank is `<d_N`,” and state that these are proper because an algebraic
map restricted to a rank-`<d_N` locus has image dimension at most `d_N-1` in
characteristic zero. State separately that every cut anchor and atlas witness
adjoined to `E_N` is an observable Fourier polynomial nonidentically zero on
the intended stratum. Do not adjoin an unspecified physical-parameter factor,
which need not define a proper distribution-side subset under parameter
nonidentifiability.

### Complete stochastic images

**VERIFIED.** The manuscript does not overclaim complete-image equality. It
explicitly disclaims it in the abstract, introduction, reconstruction
section, biological scope, and triangle certificate crosswalk. No patch is
needed on this point.

### Other exact manuscript patches

1. **FALSE wording:** lines 226--230 define the no-omnian criterion too
   narrowly. Replace it by the exact criterion in `docs/DEFINITIONS_LOCK.md`:
   every tail of a retained reticulation edge is incident with two undirected
   edges. This simultaneously excludes a tree vertex with two reticulation
   children and a reticulation with a reticulation child.
2. **UNRESOLVED overclaim:** lines 672--714 and Appendix lines 1098--1100 say
   the n3 relation universe was independently generated. Do not retain this
   wording until an independent completion/presentation generator produces
   the exact normalized relation multiset. Recordwise independent replay is
   not the same theorem.
3. **UNRESOLVED proof gap:** after line 731, add a separate direct-anchor case
   and its exact certificate/crosswalk before invoking Lemma 6.3.
4. **FALSE release statement:** abstract lines 89--90 and reproducibility
   lines 1031--1045 must not say every finite-atlas claim has independent
   replay while the n3 universe generation remains unclosed and the probe
   inputs remain untracked.
5. **VERIFIED AFTER CORRECTION:** in the all-`n` proof, specify that cherries
   are repeatedly substituted at a leaf other than leaf 1, so the stated
   leaf-1 adjacency witness literally remains unchanged.
6. **FALSE TeX text:** replace the literal `qquad` at lines 441 and 960 by
   `\qquad`.
7. **VERIFIED AFTER CORRECTION:** make the reconstruction operation bound
   explicit as at most all `2^{n-1}-1` nontrivial split tests plus
   `O(n^{10})` bounded local probes, excluding exact-number bit complexity.
   The present “polynomial relative to the explicit `4^n` table” claim is then
   transparent.

## Replay results

| Command/gate | Status | Result |
|---|---|---|
| `bash reproducibility/verify_quick.sh` | **FALSE** | Stops immediately: `FINAL_OUTCOME.json missing`. |
| Triangle clean-room verifier and mutations | **VERIFIED** | Complete 64-coordinate equality, strict point, rank four, graph quotient, and mutation suite pass. |
| Global bridge exact audit and mutations | **VERIFIED** | Exact incidence fiber, 67/9/1 endpoint partition, 204 one-active cases, two-active contradiction, and 15 mutations pass. |
| n3 bounded clean-room replay | **VERIFIED only recordwise** | All 10,466 loaded records, graph-derived pullbacks, signs, and residual topologies pass; universe generation remains unresolved. |
| n3 fixed-root hard cover | **VERIFIED, conditional on 5,344 roots** | All 68,584 states and exact terminal paths pass. |
| Five-port `theta_2` gate | **VERIFIED** | Exact three-pair survivor filter and `18+42+132` partition pass. |
| Arbitrary-subdivision promotion | **VERIFIED only on frozen path inputs** | 269,730 probe relations and all mutations pass; direct anchors are outside its declared base inventory. |
| Frozen weak theorem | **VERIFIED** | All 256 Fourier coordinates, strict field parameters, rank minors, topology census, and all-`n` inverse pass under the project virtual environment. |

The first frozen weak replay with the system Python failed only because
`networkx` was not installed there; the pinned project virtual environment
replay succeeded. This is an environment correction, not a mathematical
failure.

## Release-engineering findings

**FALSE.** Commit `5377048d` is not a clean-clone release:

- `FINAL_OUTCOME.json` and `RELEASE_METADATA.json` are absent by design;
- `primary/certificates/probe_extension_schema3_n3_final_summary.json` and
  `primary/certificates/probe_extension_theta2_schema3_final_summary.json`
  are not tracked;
- their n3/theta2 binding, graph, polynomial, and state streams are likewise
  untracked workspace artifacts;
- the active full verifier consumes these files through the promotion gate;
  and
- the manuscript crosswalk points to this referee directory before a verified
  verdict exists.

The fail-closed quick-script behavior is appropriate. It must remain failing
until the mathematical gaps are closed; do not create a positive
`FINAL_OUTCOME.json` merely to make the wrapper green.

## Minimal release recommendation

**UNRESOLVED / HOLD OUTCOME-P SUBMISSION.** Do not submit the unified positive
preprint in its current form. The shortest legitimate closure path is:

1. add one genuinely independent n3 completion/signature/presentation
   generator and require exact normalized multiset agreement with all 10,826
   raw and 10,466 canonical directed relations;
2. close the 62-direct-anchor `A+p/A+p+q` coverage by proof and exact
   crosswalk, or compile those probe families;
3. commit every load-bearing probe artifact or make the clean verifier
   regenerate it from tracked primitive data;
4. apply the manuscript patches above;
5. rerun all three clean-clone entry points; and
6. commission a new final whole-proof referee after those changes.

**VERIFIED.** The weak-class sharpness paper may remain available as a
separate proved result. **UNRESOLVED.** The unified sharp-boundary headline
must wait; this review neither proves it nor refutes it.
