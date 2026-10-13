# Independent Lean scope audit

Pinned source: `/Users/alec/Desktop/math`, commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
Audit date: 2026-10-07 UTC. No prior audits or reviews were read. All writes were confined to this audit folder. The source checkout remained clean.

## Conclusions

1. The actual source declares and supplies a proof of a strong **uniform unweighted** FPRAS, including a fixed finite-alphabet randomized machine and worst-case polynomial time on every random tape. This is stronger than a sampling-oracle statement. Its source-level theorem is not a weighted-hafnian FPRAS.
2. The actual source declares and supplies proofs of a global Poincaré inequality and mixing bound for the **constructed replica ladder**, under the explicit tree-bag and weight-comparability hypotheses below. This is not an unconditional gap theorem for an arbitrary single weighted matching chain.
3. The full actual local import closure consists of all 415 files in `OAI/Combinatorics/MatchingCount`. A lexical scan found no `sorry`, `admit`, `axiom`, `unsafe`, `opaque`, `implemented_by`, `native_decide`, or `cheat` in that closure. These are source-level scan results, not a kernel-generated axiom report.
4. Independent kernel verification was unavailable: the pinned checkout has no `.lake` directory, no compiled local modules, and no Mathlib dependency artifacts. A direct import probe failed because the required object file does not exist. Lean 4.34.1 is installed. No dependencies were installed or rebuilt.

## Exact main semantic scope

`lean/OAI/Combinatorics/MatchingCount/Model.lean:8–11` defines `GraphInput` by a natural vertex count and a finite set of ordered endpoint pairs satisfying increasing endpoints. Thus the input is a finite simple loopless undirected graph; no mathematical edge weights are input.

`Model.lean:14–23` defines perfect matchings and `Z` as their **integer cardinality**. `Model.lean:38–42` encodes the graph and the two rational approximation parameters, with no edge-weight field. `Model.lean:45–64` gives the finite-state, alphabet-8 randomized machine and one-write/one-move ticks. `Model.lean:81–82` defines

\[
t=C\bigl(|\operatorname{encodeInput}(G,\varepsilon,\delta)|+
\lceil\varepsilon^{-1}\rceil_++\operatorname{clog}_2\lceil\delta^{-1}\rceil_++1\bigr)^d.
\]

`Model.lean:94–100` places `∃ A C d` **before** `∀ G ε δ`, with `C>0`, `0<ε<1`, and `0<δ<1/2`. At time `t`, every length-`t` random tape produces a nonnegative encoded rational; a zero count produces encoded zero on every tape; and the fraction of fair tapes satisfying the relative-error inequalities is at least `1−δ`.

The actual proof is `OAI.MatchingFPRAS.thm_main` in `lean/OAI/Combinatorics/MatchingCount/Main.lean:21–30`. It uses the uniform physical time bound (`Complexity/PhysicalCost.lean:41–70`), output/zero semantics (`Probability/MainLaw.lean:30–41`), and fair-tape success theorem (`Probability/MainLaw.lean:53–68`). None of these theorem statements assumes the desired FPRAS conclusion.

The comparator file `lean/ComparatorChallenges/MatchingFPRAS.lean:105–106` contains a `sorry` template. It is **not imported by the actual theorem**: every external import in the audited actual closure is `Mathlib`, and no comparator module is imported. The comparator's template admission is therefore not evidence of an admission in the actual theorem.

There is no source-level uniform **weighted bounded-bit hafnian** FPRAS theorem in these 415 files. The presence of internal weighted Gibbs laws, rational activities, or a namespace named `WeightedOptions` does not change `GraphInput`, `Z`, or `MainStatement`.

## Exact ladder gap and assumptions

`OAI.MatchingFPRAS.Transport.concrete_ladder_poincare` is declared in `lean/OAI/Combinatorics/MatchingCount/Machines/TreePairProposal.lean:389–394`. Set

\[
N=|V|,\qquad q=32(10^4ND)^{100}.
\]

For every function on `Slot T q → PM BagEdge.Incident`, the declaration states

\[
\operatorname{Var}_{\operatorname{slotLaw}(w)}f\le
\frac{8(Tq^2+q)}3\operatorname{scanEnergy}f.
\]

The implicit section assumptions are `TreePairProposal.lean:369–387`, and the explicit arguments are lines 389–391:

- finite decidable vertex and label types;
- `bags : V → Finset J` and a simple label graph `G`;
- any two distinct labels in the same vertex bag are adjacent in `G` (`hbags`);
- `G.IsAcyclic` (`hG`);
- positive label heights, with `height a ≤ 2*height b` whenever `G.Adj a b`;
- a natural number `D≥1` and weights satisfying `height e.color / D ≤ w e ≤ 3*height e.color`;
- `N≥2`, an existing perfect matching `M₀`, and arbitrary natural tier count `T`.

The abstract `Replica.replica_gap` (`Probability/LocalVariance.lean:168–177`) assumes local `PairPoincare` inequalities. The concrete ladder proof **discharges** that assumption at `TreePairProposal.lean:406–415` using `adjacent_tree_pair_poincare`, then invokes the abstract assembly at lines 416–421. The earlier `tree_pair_poincare` (`TreePairProposal.lean:126–153`) reduces to the supplied proof of `CellDemands.pair_energy_inequality` (`Probability/Variance.lean:252–257`, proof following it). Thus the concrete declaration is not merely the abstract assembly with an unexplained local-gap hypothesis.

`OAI.MatchingFPRAS.Transport.concrete_ladder_mixing` (`Graphs/Evolve.lean:172–180`) carries the same structural assumptions (`Evolve.lean:158–170`) and states

\[
\left(\sum_s|P^n(z,s)-\nu(s)|\right)^2\le
\left(1-\frac3{8(Tq^2+q)}\right)^n(\nu(z)^{-1}-1).
\]

Its proof explicitly obtains the gap from `concrete_ladder_poincare` at `Evolve.lean:206–224`. This supplies a source-level global gap for that augmented ladder and its specified stationary product law, with the stated hypotheses. Source inspection alone does not certify the interpretation or kernel validity of every intervening mathematical definition.

## Verification bounds and receipts

All 415 local sources were hashed before/while scanning. The import parser found no multi-module import lines and no missing local imports. Their total source size is 3,091,883 bytes. The scan covers the entire actual MatchingCount directory, not only selected theorem files. The external `Mathlib` proof dependencies were not inspected, rebuilt, or axiom-audited. Classical/noncomputable definitions in source are not themselves proof admissions; the exact theorem axiom set remains unverified because the import probe could not load compiled modules.

The installed compiler reports Lean 4.34.1, commit `5045d0056413266e57c625dcd7c365b10e377c52`. The probe `axiom_probe.lean` requests `#print axioms OAI.MatchingFPRAS.thm_main`, but fails at its import with missing `Main.olean`; consequently it produces **no axiom list**. No successful build is claimed. Lake was not invoked: its configuration contains dependency bootstrap/patch actions (`lean/lakefile.lean:223–277`), incompatible with this read-only, no-dependency-rebuild audit.

All 423 unique upstream files actually read (including original documentation/configuration and an early out-of-scope SwitchChain inspection) were also compared against their exact pinned Git blobs; every SHA-256 matched. Those extra SwitchChain files did not enter the MatchingCount audit conclusions.

| Key actual source | SHA-256 |
| --- | --- |
| `MatchingCount/Model.lean` | `357b41c991087fcdba5ef7f7170cdc0705d986d3bedd3ca0b4ce115df8611b90` |
| `MatchingCount/Main.lean` | `5baa10d9bacd0be4ea26ae041a8600c9de9391abe8c0836c0ded10143054b100` |
| `MatchingCount/Machines/TreePairProposal.lean` | `dd4f9c5ac77f2ee5b0661149b8a1b287e2bb8e3fab41395d8d5c03f80cf74d28` |
| `MatchingCount/Graphs/Evolve.lean` | `bae4020faf50d034d1e53bef759cb18d11d76947b75bae9ebd0e44cfa3dd3a1a` |
| `MatchingCount/Probability/Variance.lean` | `787a09d90fe689fd0d79106a1d5f19a2d6c9fbbc14a4f6cdc4d307a33fe81ffb` |

Complete receipts: `read_receipts.jsonl`, `matching_main_import_closure.json`, `matching_main_declarations.json`, `matching_main_sorry_axiom_scan.json`, `whole_matching_count_source_scan.json`, `import_parser_check.json`, `pinned_blob_verification.json`, `build_inventory.json`, and `direct_lean_probe.json`. Numbered snapshots of the principal actual declarations are under `numbered_sources/`.
