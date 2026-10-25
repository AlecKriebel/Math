# Independent analytic review — Zenodo 22168797

**Disposition: substantive certificate defect; defer this edition. Do not publish a research page on the strength of this review.** The mathematical verification task is complete for the requested stop-on-defect workflow. No repair was attempted. The principal structural theorem has not been disproved: its submitted finite certificate contains a false exclusion of two presentations of the same physical network, so that certificate does not establish the theorem as claimed.

## Exact source and reading coverage

The reviewed public record is DOI `10.5281/zenodo.22168797`, version **1.0.5-r1**, publication date **2026-08-30**. Main manuscript: *Generic Identifiability and Directed Containment for Strongly Tree-Child Level-2 Networks under the Kimura Two-Parameter Model*, 26 pages. Reader supplement: 24 pages. Both were read in full before receiving any current sibling mathematical conclusion for this paper.

Main PDF SHA-256: `e49e72c09183679f04362afe37917e410f0b8b6fe5dc98f423a0b642dce78cf4`.
Reader PDF SHA-256: `0448cfc078f91d0bb5f08097e3055d302e1ef5308664dc3a7443e728f38ffd9d`.
Released reproducibility ZIP SHA-256: `477c160057f7a729215dfd37960063d283ddbedcf95396a8239a9fd22e94ac62`.

`final_source_integrity.json` independently rechecks all seven published assets against the fresh receipt (size, MD5 and SHA-256), the API metadata hash, and all **483 extracted files** across the two ZIPs. All match. Sources were read-only throughout. The r1 archive edition is preserved; it is not silently relabelled as the earlier manuscript body version.

## Claim reconstructed before targeted exposure

The physical domain is `D+ = {(s,g): 0<s<1, 0<g<1, g>2s−1}`, with uniform-root K2P spectra `(1,s,g,s)` and independent interior reticulation weights. The CT corollary restricts further to `s²<g`. The network class consists of binary admissible semi-directed level-2 graphs that are tree-child under **every** admissible rooting. The graph operation is one-step root suppression preserving reticulation heads; leaf restrictions are distinct operations.

The relation in Definition 2.6 requires a full-dimensional regular **source** neighborhood and a physical analytic target section. The target need not be regular. Section 4, page 9, localizes this relation to complete ported factors: it explicitly includes retained arm parameters and then takes an analytic slice by the positive two-sector incidence torus. These are neither fixed-pendant normalized maps nor unrestricted complex varieties. The claimed conclusion is generic graph identifiability modulo ordinary triangle redirection, and equivalence of the corresponding directed physical relations. It does not assert pointwise uniqueness, global equality of all stochastic images for triangle redirections, numerical parameter identifiability, or noisy statistical recovery.

I reconstructed the proof route through positive quartet and full-map sunlet signs; bridge-fibre uniqueness and physical saturation; serial marginal submersions; finite source-open localization; primitive cycle/theta classification; restoration and one-/two-port coherence; ordinary-triangle common germs; semialgebraic exceptional sets; the strict-CT restriction; and the weak-versus-strong counterexamples and cherry extension. The critical finite classification is not replaced by its reported row counts.

## Substantive defect: an isomorphic pair is excluded by the wrong rank

The released file

`work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz`

has SHA-256 `7cf3f953fca695d612387143818843650498f84f55cf0a776f90c9afdd95eef6`.
Its line **137125**, `raw_id = 137124`, has:

- source index 2: `theta1`, repair `{2,3}`;
- target index 85: `theta0`, repair `{2,3}`;
- physical port permutation `[2,0,1,3]`;
- `corrected_category = exact_rank_exclusion`;
- reason `target_exact_generic_rank_below_source`, with source rank 14 and target rank 13.

The exact row and bound hashes are saved in `bound_false_exclusion_row.json`. `literal_witness_binding.json` checks that the independently written literal graphs below are exactly the released source and transported target rooted presentations, with no dummy leaves.

Use root `r`, reticulations `V,X`, and leaf labels `L0,...,L3`.

Source arcs:

```
r→S, r→L0, S→U, S→X, V→A, A→X,
A→L1, U→B, B→V, B→L2, U→V, X→L3.
```

Target arcs after the stated port permutation:

```
r→S, r→L2, S→U, S→V, U→A, A→X,
A→L0, V→B, B→X, B→L1, U→V, X→L3.
```

After suppressing `r` once, the following is a label- and arrowhead-preserving mixed-graph isomorphism from source to target:

```
S↦A, U↦U, V↦V, X↦X, A↦B, B↦S, Li↦Li.
```

It preserves every physical edge and every reticulation head. Independent exhaustive rooting enumeration finds **7 admissible rootings, all 7 tree-child**, on each graph. Thus this is inside the stated strong class, not a weak-class or inadmissible-rooting escape.

The fresh checker `fresh_false_exclusion.py` imports no submitted code. It checks the mixed-graph isomorphism, enumerates all admissible rootings, and constructs all switching terms directly from the literal arcs. After the physical edge and reticulation-weight transport, **all 64 conservation-supported Fourier polynomials have identical switching monomials**. The other 192 coordinates vanish under the uniform root. This is an exact identity in physical mixed-edge and inheritance parameters, not only a numerical collision.

Root placement does not create a loophole. Its two incident edge pairs enter only through their serial product. The paper's own serial-section lemma, also independently reconstructed here, gives physical local sections for every product in D+; the positive power section does so in strict CT. Hence these presentations have the same physical model and the same incidence-quotient model, and they certainly have the identity-induced directed relation required by the theorem. The checker additionally verifies exact equality at explicit transported rational strict-CT parameters.

Fresh exact Jacobians at rational points give:

| Presentation | Selected pendant parameters omitted | All physical parameters | Incidence torus | Full Jacobian modulo incidence torus |
|---|---:|---:|---:|---:|
| Source | 14 | 17 | 8 | 9 |
| Target | 13 | 17 | 8 | 9 |

These fresh Jacobian numbers are pointwise exact ranks, not a new independent generic upper-bound proof. The polynomial identity and graph isomorphism already prove the equal-model conclusion without that stronger claim.

The causal code path is visible in `k2p_atlas_core.py`: `selected_arm_edges` identifies all selected leaf arms; `descriptor_variant` and `model_descriptor_fast2` omit those edges before forming their polynomial maps. `generate_raw_ledger.py` compares those ranks directly at lines 239–243 before the mixed-graph terminal test. Such a fixed-arm rank depends on where the root/selected arm is placed. It is not the rank of the full map, nor the dimension of the quotient map defined on manuscript page 9. Thus the strict inequality is valid for a different pair of parameterizations and invalid as an exclusion of the paper's physical relation.

This contradicts the validity of terminal type (ii) in §6.2, pages 14–15, as applied to this row, and the claim that the complete finite census provides valid directed exclusions. Theorem 6.3 relies on this census; Theorem 7.3 and the generic/CT conclusions rely on that primitive theorem. A false negative between isomorphic graphs is **not itself a counterexample to their final structural statements**, which allow isomorphic graphs. It is nevertheless a substantive load-bearing proof/certificate defect. Publication is deferred for this edition. The pipeline was not patched and no replacement certificate was sought.

## Evidence completed before the defect

Fresh controls, completed before the published replay, used only literal printed definitions and generic symbolic/graph libraries:

- Exact sunlet `Ti` factorization and the ordinary-triangle rank-nine point.
- Both explicit weak-class three-leaf tensors, all 64 Fourier coordinates, strict CT membership, independent rooting counts `(5,2,3)` and `(7,2,5)`, and independent rank-nine minors.
- Cherry-extension observable Jacobian `4 us ug / (vs vg)`.
- Completion counts `831, 1983, 1983, 4155` from the stated combinatorial formula.
- Primitive cycle/theta occupancy and minimal strong-class repair patterns, derived independently by graph construction.
- Quartet polynomial identities, serial-product positivity checks, and simultaneous D+/CT gluing controls. Bounded rational controls support these constructions but are not presented as proofs of all real inequalities.

The larger analytic arguments were checked on paper: positivity prevents quartet-sign cancellation; full-map sunlet pullbacks avoid the invalid rooted-triple shortcut; rank-one bridge blocks and positive pair anchors give the stated two-sector gauges; source-open finite semialgebraic localization does not require target regularity; triangle rank nine survives arbitrary fixed exterior contraction after selecting a maximal-rank context; critical-image dimension and finite Nash stratification provide the intended genericity implication if the primitive classification were valid.

The published `--quick` replay completed **14 layers** before the concern was confirmed: manuscript guard, full-map reseal, corrected-universe replay, three-port/no-assert, domain/rooting, quartet signs, quartet bindings, raw displayed quartets, canonicalizer structure, parameter-transport structure, bridge gluing, analytic regressions, component-scale regressions, and the raw4 corrected overlay replay. It was deliberately interrupted during the following theta2 full-map replay. The log records `KeyboardInterrupt`; this is an investigator stop after a substantive defect, not an unexplained failed computation. No completed whole-package PASS is claimed. No expensive full regeneration was run after the defect.

## Primary interfaces and limitations

Primary-source reading covered Englander et al. v4, Propositions 2.9–2.10, Theorem 2.11 and Corollary 2.12, checking the K2P character relabelling and the pointwise positive-mixture quartet interface. It covered Huber et al. published Lemma 4.2 and its proof, with Figure 8 visually inspected: the semi-directed level-2 generators have the two stated reticulation-placement forms. The manuscript independently refines these into its rooted directed core cases. The generic semialgebraic reasoning was reconstructed directly; the full BCR 1998 chapter body was not obtained because the publisher access was restricted, and Coste's freely hosted notes could not be fetched. No claim of checking BCR's exact numbered text is made. Raw Britz/Holtgrefe sources were available but additional contextual reading was stopped when the substantive defect was established; they were not needed to establish this defect.

## Independence and exposure

All 50 manuscript/supplement pages and the first fresh-control families were completed without reading current sibling reports or dedicated historical verdicts. Public record metadata, the manuscript/supplement, and necessary authored mathematical support included historical pass counts and status claims. Those statements were encountered but not accepted as proof. The mathematical `canonicalizer_completeness/PROOF.md` was read; dedicated archived `AUDIT.md`/`PROOF_AUDIT.md` verdict bodies were not.

A coordination message to the scope agent prematurely included partial fresh-control pass results while requesting a primary source. That outgoing exposure was disclosed to the parent; the scope agent said it would exclude the results until its own scope conclusion. No current mathematical outcome was received from that agent. A message about the preceding, distinct paper 22136869 was received and is irrelevant to this result.

While independently tracing the atlas omission of selected arms, I identified the potential rank-versus-quotient mismatch and queued a diagnostic. Before that command dispatched, the parent supplied the adversarial target tuple and alleged isomorphism/ranks. The tuple and claim are therefore explicitly **targeted exposure**, not credited as independent discovery of that particular witness. The confirmation then used fresh literal graphs, independent Fourier-polynomial enumeration, exact Jacobians and rooting enumeration; no sibling code, report, or evidence artifact was read.

All results are retained under `reviews/analytic`. There were no source repairs, website edits, spreadsheet changes, Git operations, publication actions, or external communications.
