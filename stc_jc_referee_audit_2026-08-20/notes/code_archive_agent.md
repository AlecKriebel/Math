# Independent archive/code audit

**Checkpoint:** 2026-08-20 21:11 PDT  
**Completion estimate for assigned code-archive audit:** 100%  
**Archive root used below:** `work/extracted/stc_jc_sharp_boundary_atlas_certificates_v1.1.5/`

## Scope and method

I read the complete 31-page manuscript and complete 7-page supplement before
inspecting the archive. I then read `PROOF_BOUNDARY.md`,
`THEOREM_CERTIFICATE_CROSSWALK.md`, `ATLAS_SUMMARY.md`, and
`REGENERATION_MAP.md`, traced the load-bearing data lineage from primitive
graphs through regenerated tensors and certificates, and performed focused
read-only recomputations. I did not edit any submitted file. I also did not run
`verify.sh quick`, `verify.sh full`, or `verify.sh regenerate-all`; those runs
were reserved for the lead audit.

Stored PASS logs and expected-output strings were not treated as evidence. The
findings below come from source inspection, exact frozen logical records tied
back to graph inputs, and small independently changed recomputations.

## Reconstructed mathematical obligation

Theorem 1.1 concerns fixed one-step `sd0` reductions of leaf-labelled binary,
simple, standard semi-directed level-2 networks. An admissible rooted origin
must be LSA-valid, and the strong class consists of networks with at least one
admissible origin for which **every** admissible origin is tree-child. All JC
edge multipliers and inheritance parameters lie in the strict open interval
`(0,1)`. The directed relation `N \preceq_JC N'` is source-relative local
containment at a source-regular common point; the target is not required to
have the same dimension. The claimed classification is equality of labelled
reduced bridge trees, with corresponding blobs labelled-isomorphic or related
by one ordinary triangle redirection. It therefore also excludes proper
one-sided containment.

The proof dependency I reconstructed is:

1. no-omnian/rooting structure and cycle/four-theta primitive exhaustiveness;
2. pointwise bridge-split recovery, including the one- and two-active-endpoint
   cases;
3. projective localization through the full incidence-scaling bridge fibre;
4. finite decorated-relation coverage of every bounded completion;
5. marginal submersion, fixed-full restoration, and coherent one-/two-port
   probes;
6. ordinary-triangle common germ and contextual gluing;
7. local-to-global assembly;
8. exact full-dimensional Omega and Theta counterfamilies outside the strong
   class.

The archive's stated proof boundary is consistent with that dependency:
`PROOF_BOUNDARY.md:3-18` assigns structural arguments to the manuscript and
the bounded directed-relation theorem to exact computation, while
`REGENERATION_MAP.md:9-21` identifies the replay chain. The code does not, and
cannot, replace the manuscript's continuous/open-map and finite-cover
arguments.

## Concrete defects

### R1 — the marginal-submersion auxiliary certificate uses the wrong edge equivalence and a tautological rank test

**Classification:** reproducibility defect; not a theorem-level counterexample
because the written proof of Lemma 6.2 gives the correct product-submersion
argument and the actual bounded tensor compilers use the correct
normalization.

Lemma 6.2 (manuscript pp. 15-16) requires grouping edge rows by their complete
**zero-sum JC indicator signature**. In particular, a selected split mask and
its complement are equivalent in every switching, and a row that is always
zero or the full selected mask is tensor-invisible and must be discarded.

The supposedly independent auxiliary verifier does something else:

- `reviews/root_probe/verify_parameter_submersion.py:157-165` forms classes
  from exact rooted descendant-mask tuples. It neither normalizes each mask by
  complement nor discards full-mask rows before defining the classes.
- `reviews/root_probe/verify_parameter_submersion.py:166-185` computes
  complement-normalized *columns* only as a redundancy statistic and counts
  tensor-invisible classes, but still includes those classes in the claimed
  target dimension.
- `reviews/root_probe/verify_parameter_submersion.py:180-181` assigns
  `jacobian_row_rank_at_open_point` and `parameter_target_dimension` the same
  expression, `len(classes) + len(retics)`. No Jacobian is formed or ranked.
- Consequently the asserted test at
  `reviews/root_probe/verify_parameter_submersion.py:246-247` is an identity,
  and `reviews/root_probe/verify_active_structural.py:126-130` promotes its zero
  failure count as a "path-product submersion rank" check.

I reran the completion enumeration in memory, replacing the class key in every
switching by

`0` for masks `0` and `full`, otherwise `min(mask, full ^ mask)`,

and then regrouping the complete rows. All **42,908** enumerated completions
changed relative to the verifier's raw class accounting (at minimum because
the full-mask/root class must disappear). A concrete bundled example is the
incoming-selected three-outgoing cycle completion with
`counts=[0,3]`, `sink_mask=0`. The auxiliary certificate reports the six raw
rows

`(1,1), (2,2), (4,4), (8,8), (12,12), (14,14)`.

Under the zero-sum equivalence, `(1,1)` and `(14,14)` are the same class, so
there are five visible classes, not six. The frozen certificate itself reports
37,416 completions with complement redundancy and 28,030 completions with an
invisible class, yet its rank check still cannot fail.

This defect should be repaired by constructing the correct normalized
indicator rows, deleting the tensor-invisible row, forming the actual
block-product descriptor Jacobian (or an exact rank-equivalent matrix), and
comparing that computed rank to the correctly normalized target dimension.
Until then this file must not be cited as an independent computational replay
of Lemma 6.2.

The theorem-level damage is limited: the manuscript explicitly proves the
correct positive product map on pp. 15-16, and the load-bearing hard-cover
compiler correctly performs zero/full deletion and mask/complement
normalization in `primary/hard_cover_compiler.py:141-164`.

### R2 — the graph-level probe-coherence collision check includes its answer in its key

**Classification:** reproducibility/interpretation defect; not a counterexample
to Lemma 6.4, and not load-bearing because the direct-anchor and compact-probe
semantic gates check the actual parent restrictions and transports.

The auxiliary deck constructs the support code, two one-port codes, and the
two-port/full code. At
`reviews/root_probe/verify_probe_coherence.py:308-310`, its grouping key is

`(support_code, codes[0], codes[1], codes[2])`,

while the value whose uniqueness is tested is exactly `codes[2]`. Therefore
the collision search at
`reviews/root_probe/verify_probe_coherence.py:329-335` is mathematically
incapable of returning two distinct values for a key. Nevertheless
`reviews/root_probe/verify_active_structural.py:98-105` treats zero collisions
as probe-coherence evidence.

As a falsification check I removed `codes[2]` from the key. Among 8,976
presentations this produced **372** collision groups (maximum multiplicity 2).
For the first cycle support/repair example, the segment words
`('Q1','P1','P0')` and `('Q1','P0','P1')` have the same support and the same two
one-port restrictions but different two-port/full codes. This is exactly why
Lemma 6.4 needs the `A ∪ {p,q}` probe: it is not a contradiction to the
theorem.

The abstract word test at
`reviews/root_probe/verify_probe_coherence.py:229-255` is non-tautological and
correctly checks that locations plus all pairwise orders reconstruct a word.
The real finite proof also independently checks the required two-port data:
`reviews/compact_probe_clean_clone_gate/semantic_gate.py:529-728` regenerates
the graph-derived descriptors, pullbacks, signs, transports and parent
restrictions, and `:731-805` checks the complete path union. Thus the remedy is
to relabel/remove the vacuous graph collision statistic or replace it with a
test of independently produced two-port transports against the full graph.

### E1 — `ATLAS_SUMMARY.md` calls n=4 presentation rows canonical-relation rows

**Classification:** exposition/schema documentation defect; no loss of
source-target information and no atlas-coverage failure found.

`ATLAS_SUMMARY.md:29-34` says the evidence map has "one authoritative record
per canonical relation." That is true for the 10,466 three-outgoing rows, but
not for the four-outgoing part. In
`verifiers/evidence_bindings.py:263-276`, the n=4 `relation_id` is the hash of
the **normalized raw presentation**, and the quotient-canonical digest is
stored separately as `canonical_relation_sha256`. Rows are emitted per raw
presentation at `verifiers/evidence_bindings.py:334-348`.

The archive's own quotient certificate shows the distinction:
`reviews/theta2_signature_gate/canonical_quotient_certificate.json:4` has only
3 direct canonical relations, `:140` has 57 nonretaining canonical relations,
and `:147` has 192 raw survivor presentations. The evidence map has all 192 n=4
presentation rows (18 direct, 42 selected-incoming duplicates, 132 restoration
roots), not 192 distinct quotient-canonical relations.

This wording should say "one authoritative record per three-outgoing canonical
relation and per four-outgoing survivor presentation," or the schema should
introduce a distinct `presentation_id`. The implementation retains the
canonical digest, source/target graph identifiers and exact transports, so
this is terminological rather than a mathematical omission.

## Load-bearing code audit

### Primitive graph to displayed switchings and exact Fourier tensors

I found the compilation correct. `primary/graph_model.py:405-437` identifies
the two incoming arcs at every reticulation, removes exactly one for every
switching, and computes descendant sets in the resulting displayed graph.
`primary/jc_tensor.py:75-112` constructs switching signatures and edge
exponents, while `primary/jc_tensor.py:175-204` attaches the appropriate
`lambda`/`1-lambda` switching weight and sums exact sparse monomials. The
clean-room implementation derives the same objects through its own effective
descriptor representation at
`reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py:312-350` and
`:1359-1388`.

### Relation identity and source-target provenance

`primary/atlas_compiler.py:721-778` includes the direction, both rooted graph
records, source and target colored codes, complete port matching, actual
incoming roles, and source/target position maps in each decorated relation.
The merge at `primary/atlas_compiler.py:907-925` only combines identical
canonical bodies and preserves the raw coverage/provenance. I found no target
hash-only collapse or loss of source embedding.

For n=4, the presentation-vs-canonical terminology noted in E1 does not erase
information: `verifiers/evidence_bindings.py:269-276,334-348` retains both
levels of identity and both graph IDs.

### Exact universe coverage and mutation sensitivity

The separately written n=3 generator takes primary streams only as comparison
inputs (`reviews/n3_universe_generator/generate_universe.py:429-458`), then
requires 10,826 raw presentations, 10,466 canonical relations, 10,106
singletons and 360 doubletons at `:472-500`. Its mutations at `:559-615`
exercise deletion, duplication, direction reversal, altered port matching,
deleted merged records, and split raw coverage.

I independently counted the evidence map: **10,658** total records, consisting
of 10,466 n=3 relations and 192 n=4 presentations, with unique presentation
identities. The n=3 dispositions are 5,284 strict, 5,120 pending/restoration,
and 62 isomorphism/T; the n=4 dispositions are 18 direct, 42 selected-rooting
duplicates, and 132 restoration roots. These agree with the regenerated
universe definitions, not merely with a log string.

`verifiers/evidence_bindings.py:352-395` reconstructs and byte-compares the
logical rows. `verifiers/verify_certificate_bundle.py:67-124` requires the
10,466/192 split, unique IDs, and an exact CSV projection. I found every
evidence row assigned once at its stated presentation level; E1 is the only
terminology mismatch.

The compact-probe mutation suite at
`reviews/compact_probe_clean_clone_gate/mutation_tests.py:155-243` rejects
deleted or duplicated paths, changed arcs/orders, a valid witness attached to
the wrong relation, changed valid transport, changed terminal class,
incoherent triangle choice, and altered provenance. Together with the n=3
mutations, this directly addresses omission, duplication, misassignment and
alteration.

### Certificates are graph-regenerated rather than identifier-selected

The primary atlas builds descriptor invariants from exact graph tensors.
`primary/atlas_compiler.py:260-286` uses a modular value only as an exact
nonzero witness and expands every modular zero over the integers. The bounded
clean-room replay reconstructs both graphs, their switchings and tensors,
checks exact pullbacks/signs, and verifies that attaching a valid polynomial
to the wrong graph fails (`reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py:1510-1589`).
Graph/provenance binding is checked at `:1609-1701` and complete relation hashes
at `:1704-1731`.

Strict-sign certificates use exact factorizations or rational Bernstein
coefficients. Equality terminals are reclassified from labelled mixed graphs,
not accepted from stored labels. The n=3 adversarial referee recomputes every
active/zero descriptor invariant and all polynomial bodies/factors. The n=4
clean-room gate dynamically derives separators and audits every surviving
state. I found no identifier allow-list serving as mathematical evidence.

### Restoration and probes

The n=3 hard cover contains 68,584 states (56,055 generic, 8,349 refined,
4,036 strict, 120 labelled-isomorphic, 24 T); the n=4 cover contains 2,106
states (1,860 generic, 114 refined, 132 isomorphic). State/root identifiers bind
the complete rooted source and target graphs, remaining dummy roles and exact
port maps. Child states are generated by all allowed insertions, and merged
state provenance requires identical child sets.

The direct-anchor compiler enumerates every admissible internal source-target
arc pair for all 62 anchors at
`reviews/direct_anchor_probe_closure/compile_direct_anchor_probes.py:482-643`,
producing 2,642 one-port and 18,224 two-port relations. The verifier separately
enumerates expected IDs and checks exact graph deletion/parent mapping at
`reviews/direct_anchor_probe_closure/verify_direct_anchor_probes.py:254-388`
and exact pullbacks/signs at `:402-462`.

The compact semantic replay does not trust the verbose frozen summaries. It
derives the hard-cover parent inventory, every one-/two-port child, exact
descriptors, polynomial pullbacks and signs, transports, and parent
restrictions (`reviews/compact_probe_clean_clone_gate/semantic_gate.py:529-728`).
It then checks the exact union of 276 paths and 269,730 relations at `:731-805`
(101,148 n=3 and 168,582 n=4, at most ten ports). This is the load-bearing
probe-coherence evidence; R2 concerns only a weaker auxiliary deck.

### Independence of implementations

The principal bounded clean-room code imports no primary graph/tensor module
and uses separate graph dataclasses, canonicalization, switching enumeration,
tensor algebra and polynomial algebra. The global bridge audit likewise reads
the published logical certificate and rebuilds the mathematics independently.

One residual assurance limitation is worth disclosing. Both the direct-anchor
compiler and its immediate verifier import the same mechanically vendored
engine:
`reviews/direct_anchor_probe_closure/compile_direct_anchor_probes.py:28-33`,
`reviews/direct_anchor_probe_closure/verify_direct_anchor_probes.py:22-26`, and
`reviews/direct_anchor_probe_closure/exact_engine.py:1-9`. Thus those two files
are not independent implementations of primitive graph/tensor semantics, even
though they independently enumerate expected records and mutations, and the
compact semantic gate supplies separate end-to-end coverage. I treat this as
an assurance limitation, not a demonstrated false certificate.

### Cut and bridge component checks

The cut verifier exhausts its endpoint and one-active local universes and
constructs graph witnesses at
`independent/bridge_cut/verify_cut.py:1066-1198`; the census contains 67
`F>0`, 9 `F=0,G>0`, one ordinary case, 204 strict wrong-split minors and 12
common displayed cases. The two-active identities/minors are checked exactly
at `:1201-1258`. The separately implemented global audit reconstructs these
from the logical JSON at
`reviews/global_bridge/exact_audit.py:702-816,833-894`.

The bridge verifier implements the universal log-linear incidence map and its
full gauge fibre at `independent/bridge_cut/verify_bridge.py:134-227`, with
exact finite tree regressions at `:340-364`. Its header correctly says those
regressions are not a substitute for the human proof (`:2-8`). An older
"arbitrary positive effective scale" concern in the global audit is already
resolved by Theorem 5.1 (manuscript p. 13): the statement is restricted to the
physical-locus intersection, and simultaneous gluing chooses sufficiently
small common scales. I found no present theorem contradiction there.

### Ordinary triangle, Omega and Theta

The triangle clean-room replay verifies an exact strict common point, exact
tensor equality, physical/effective rank four, and mutations
(`reviews/triangle_redirection_cleanroom/cleanroom_verify.py:516-534,692-796`).

For Omega, `omega_audit/independent/verify_omega_release.py:174-230` rebuilds
the two mixed graphs and checks rooting/class/triangle-free claims;
`:258-338` verifies positivity, exact equality and rank. The symbolic audit
checks all 64 coordinate identities under a rational nine-parameter
correspondence and exact generic-rank upper/lower bounds at
`omega_audit/independent/audit_omega_algebra.py:97-172`.

For Theta, the independent sharpness verifier forms the two exact Jacobians
and proves their determinant claims by two methods at
`s_tc_jc_sharp_boundary/reproducibility/independent/verify_sharpness.py:983-1111`.
It checks exact tensor equality, rank-eight minors, independent factorization
and localized dimension at `:1333-1485`, then the analytic identical-cherry
inverse and all-n induction at `:1492-1644`. I found no rank inflation,
boundary-only point, or missing all-n step.

### Regeneration lineage

`verifiers/regenerate_load_bearing.py:123-230` rebuilds cores, completions and
supports, deletes the derived descriptor cache, regenerates n=3 shards, hard
covers, compact probes and direct anchors. It compares exact logical outputs
at `:256-315`. `verifiers/run_gate.py:31-57` performs two isolated full
repetitions, and `verifiers/internal_math_gates.py:175-248` runs the component
and clean-room gates.

Although `regenerate_load_bearing.py` does not itself write the final evidence
map, the outer certificate verifier reconstructs that map from the regenerated
streams and requires exact equality
(`verifiers/verify_certificate_bundle.py:93-109`). The final manifest check
then binds every included proof-payload byte. I found no path where a stale
generated stream could be silently selected merely by an identifier.

## Overall code-audit assessment

I found **no theorem-level counterexample** in the graph/tensor/certificate
implementation and no evidence of an omitted, duplicated, misassigned or
altered load-bearing atlas record. The finite atlas, exact sign/equality gates,
restoration forests, probe closure, triangle germ, and Omega/Theta rank
certificates are materially regenerated from primitive inputs and have real
mutation sensitivity.

The archive nevertheless contains two concrete auxiliary-verifier defects
(R1 and R2) and one documentation/schema mismatch (E1). R1 is the most serious:
the file advertised as a marginal-submersion replay does not implement the
equivalence relation in Lemma 6.2 and its rank assertion is tautological. The
written proof and the actual hard-cover normalization prevent this from
invalidating Theorem 1.1, but the certificate must be corrected or its claimed
scope reduced. R2 should likewise be relabelled or made non-tautological.

**Code/archive-only recommended verdict: MINOR REVISION**, conditional on the
separate proof audit finding no mathematical gap. The appropriate revision is
to fix/reissue the two auxiliary certificates and correct the atlas-summary
wording; the evidence I inspected does not support MAJOR REVISION or INVALID on
code grounds alone.
