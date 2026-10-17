# Prior formalization: scope and dependency audit 01

Audit checkpoint: **2026-10-17 20:48:32 UTC**. Bounded source/scope audit: **100% complete**. Independent kernel reproduction: **0/50 OAI modules compiled**; the dependency probe failed before compiling the first module because matching Mathlib artifacts are absent. This is a completed scope audit with an explicit verification limit, not a claim that a build was reproduced.

## Strongest supported finding

The current primary Lean source states the full geometric universal-group claim: there exists one group of type F∞ containing an isomorphic copy of **every finitely presented group**, with no word-problem restriction. Its `HasTypeFInfinity` predicate is a genuine geometric definition, not merely an FP∞ or homology condition. The complete 50-module OAI import closure has no source-level `sorry`, `admit`, new `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `extern`, `run_tac`, `run_elab`, or `initialize` matches. This audit **does not certify that the 50 modules elaborate or that the compiled theorem has only the permitted axioms**: no successful build, comparator run, or actual `#print axioms` report was obtained.

No paper-geometry verdict, other reviewer verdict, or external correspondence was used to reach this conclusion. A separate child audit independently checked the definition semantics against pinned Mathlib source and found no weakening. No outreach, publication, commits, or pushes were performed.

## Revisions and primary artifacts

- Repository: [`openai/math` commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a`](https://github.com/openai/math/tree/1581d4cbdd69a0faf34b2089614fe2a814316a6a), the `main` head returned by GitHub at retrieval; commit timestamp `2026-10-12T21:55:24Z`.
- Solution: [`lean/OAI/GroupTheory/UniversalGroup/Main.lean`](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/OAI/GroupTheory/UniversalGroup/Main.lean), lines 20–50.
- Definition: [`Model.lean`](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/OAI/GroupTheory/UniversalGroup/Model.lean), lines 8–14.
- Challenge configuration: [`ComparatorChallenges/UniversalFInfinity.json`](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/ComparatorChallenges/UniversalFInfinity.json) and the adjacent challenge module. The configuration permits `propext`, `Quot.sound`, and `Classical.choice`; `enable_nanoda` is `false`. This is a configuration, **not a receipt of a successful check**.
- Toolchain: [`lean-toolchain`](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/lean-toolchain), `leanprover/lean4:v4.34.1`.
- Mathlib dependency: [`lakefile.lean:85–86`](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/lakefile.lean#L85), pinned to [`d13f23b723b8a846827a245b89c10fc7d3f11612`](https://github.com/leanprover-community/mathlib4/tree/d13f23b723b8a846827a245b89c10fc7d3f11612). The project has many unrelated Lake dependencies, but the solution's actual source import closure ends at `import Mathlib`; none of those other project packages appears in this closure.

The pinned [`formalization.yaml`](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/formalization.yaml) has repository-wide `status.scope: "Partial progress."` (lines 969–970) and global `review.status: unchecked` (line 1778). Its theorem-specific entry (lines 1749–1751) names this comparator configuration, declaration, and source file. Those global fields are **not evidence of a theorem-specific failure or success**; the actual statement and proof source above are the relevant theorem-specific facts. They also do not supply the missing successful checking receipt.

Pinned raw sources and API receipts are locally retained in the ignored `literature/formal_scope/raw/` directory. `literature/formal_scope/SOURCE_MANIFEST.json` records the 50 solution files, line and byte counts, SHA-256 hashes, and their Git blob identities; every fetched solution blob was checked against the pinned Git tree. The initial repository-wide recursive tree response was truncated, so the import inventory instead used the **untruncated UniversalGroup subtree**. The pinned Mathlib tree response was also untruncated.

## Exact theorem and predicate

The actual solution theorem statement is:

```lean
theorem universal_group_of_type_FInfinity :
    ∃ (H : Type u) (groupH : Group H),
      @HasTypeFInfinity H groupH ∧
      ∀ (G : Type u) [Group G] [Group.IsFinitelyPresented G],
        ∃ φ : G →* H, Function.Injective φ := by
  ...
```

It resides in `OAI.UniversalFInfinity`, and its actual target predicate is:

```lean
def HasTypeFInfinity (G : Type u) [Group G] : Prop :=
  ∃ (X : Type u) (_ : TopologicalSpace X) (_ : T2Space X)
    (_ : ConnectedSpace X) (cw : Topology.CWComplex (Set.univ : Set X)),
    (∀ n : ℕ, Finite (cw.cell n)) ∧
    (∃ x : X, Nonempty (FundamentalGroup X x ≃* G)) ∧
    ∃ (E : Type u) (_ : TopologicalSpace E) (_ : ContractibleSpace E)
      (p : E → X), Function.Surjective p ∧ IsCoveringMap p
```

The source text of this definition matches the comparator definition exactly, and the actual theorem statement matches the challenge statement exactly. The challenge module ends in `sorry`, as a challenge placeholder; **it is not imported by the solution**, and its placeholder is not part of the audited solution chain.

The full statement is parameterized by a fixed universe `u`; it provides an `H : Type u` universal for all finitely presented `G : Type u`. This is the usual set-theoretic meaning of the claimed group existence. It does not assert universality for all finitely generated or all countable groups. The construction first obtains an ordinary `Type` group and explicitly uses `ULift.{u}` to place it in the requested universe; this restriction does not omit any ordinary finitely presented isomorphism type.

## Why this really is geometric F∞

`Model.lean` imports Mathlib directly, then introduces only `HasTypeFInfinity`. Thus the geometric ingredients in this definition resolve to Mathlib rather than to previously introduced OAI surrogates. A search found no redeclarations of those ingredient names in the solution closure.

At the pinned Mathlib revision:

1. [`Topology/CWComplex/Classical/Basic.lean:135–162`](https://github.com/leanprover-community/mathlib4/blob/d13f23b723b8a846827a245b89c10fc7d3f11612/Mathlib/Topology/CWComplex/Classical/Basic.lean#L135) defines actual CW cells with characteristic maps, closure finiteness, weak topology, and coverage. The complex here is all of `X`, and `X` is Hausdorff and connected.
2. `∀ n, Finite (cw.cell n)` is exactly the finite-type condition in [`Classical/Finite.lean:48–52`](https://github.com/leanprover-community/mathlib4/blob/d13f23b723b8a846827a245b89c10fc7d3f11612/Mathlib/Topology/CWComplex/Classical/Finite.lean#L48). A fixed finite skeleton contains the finite union of cell sets in dimensions at most its dimension, so it is a finite CW complex. This does not assert finite total dimension, which F∞ does not require.
3. [`Topology/Homotopy/Contractible.lean:48–50`](https://github.com/leanprover-community/mathlib4/blob/d13f23b723b8a846827a245b89c10fc7d3f11612/Mathlib/Topology/Homotopy/Contractible.lean#L48) defines `ContractibleSpace E` through an actual homotopy equivalence with `Unit`, not through homological acyclicity.
4. [`Topology/Covering/Basic.lean:40–42,288–289`](https://github.com/leanprover-community/mathlib4/blob/d13f23b723b8a846827a245b89c10fc7d3f11612/Mathlib/Topology/Covering/Basic.lean#L288) defines a genuine covering map by evenly covered neighborhoods and homeomorphisms to a neighborhood times its discrete fiber. Mathlib allows empty fibers generally, but the explicit `Function.Surjective p` removes any empty-cover loophole.
5. A contractible cover is path connected and simply connected. Over a connected CW complex it is a universal cover, so `X` is a K(G,1) by the explicit fundamental-group isomorphism. This last interpretation uses ordinary covering-space mathematics; a separate Lean theorem packaging the English phrase “classifying space” was not compiled in this audit. The predicate already provides the substantive geometric witness directly, so no homology-to-homotopy bridge is being assumed.

[`GroupTheory/FinitelyPresentedGroup.lean:98–104`](https://github.com/leanprover-community/mathlib4/blob/d13f23b723b8a846827a245b89c10fc7d3f11612/Mathlib/GroupTheory/FinitelyPresentedGroup.lean#L98) uses the standard finite-generators and finitely normally generated kernel definition. No decidable equality, computable presentation, decidable word problem, torsion restriction, or homological finiteness instance appears among the theorem's hypotheses.

## Dependency mechanism and assumption audit

The entire OAI closure is a single import chain of **50 files, 19,991 lines, 884,044 bytes**, beginning with `Main.lean` and ending with `Model.lean → Mathlib`. No source admission or added-axiom token was found by the recorded scan. This is useful negative evidence but is not equivalent to elaborating proof terms and inspecting their axiom dependencies.

The final proof discharges its own construction inputs as follows:

- `Higman.NormalWords.embeds_presentation` (`HigmanEmbedding.lean:455`) embeds a recursively presented group into a finitely presented group. The computation assumption is applied to a specific enumerator, whose primitive recursiveness is proved in `UniversalPresentation.lean`; it is not imposed on the arbitrary target group `G`.
- `RecursiveUniversalThree.universal` (`UniversalPresentation.lean:535`) takes **only** a group and its finite-presentation instance and embeds it into the fixed recursively presented universal group. Its earlier `countable_universal` step ranges over all finite presentation codes.
- `ConcreteEnvelopes.self_maps` (`Idempotents.lean:236`) requires a finitely presented universal `U`; `Main.lean` constructs that witness and its universality. The returned diagram and injection supply the `Fact` instance required later.
- `AscendingTorus.of_injective` embeds that `U` in the ascending-torus group.
- `TorusGeometry.diagram_milnor_uniform_nullhomotopy` (`TorusSpheres.lean:485`) supplies actual stage nullhomotopies. `Brown.geometric_lifted_of_uniform` (`UniverseTransport.lean:160`) returns the geometric predicate by explicitly providing a CW base with finite cells, a fundamental-group isomorphism, and a contractible covering total space. The topology and discreteness instances it needs are set locally in `Main.lean`.
- The final arbitrary-group embedding is the composition of the universal recursive embedding, the Higman embedding, the ascending-torus embedding, and the universe-lift equivalence. There is no unfilled theorem parameter in the printed source statement.

If successfully compiled, the ordinary trust boundary would include Lean 4.34.1's kernel and its standard foundational axioms, the pinned Mathlib dependency, and the correspondence between the formal definitions and the mathematical claim. The comparator configuration restricts permitted axioms to `propext`, `Quot.sound`, and `Classical.choice`; **this audit did not observe a compiled report confirming that restriction**. Nor was an independent export checker run. The lack of a source `axiom`/`sorry` match cannot exclude every possible imported-library or elaboration issue.

## Local build probe and remaining verification

The installed matching runtime was available:

```text
Lean (version 4.34.1, arm64-apple-darwin24.6.0,
commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)
```

Invoking it on the pinned `Model.lean` stopped immediately with:

```text
Model.lean:1:0: error: unknown module prefix 'Mathlib'
```

The exact output is in ignored `raw/dependency_probe.txt`. Existing local Mathlib projects inspected use Lean 4.19.0 and Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`, so they cannot provide a matching compiled dependency. A complete checkout/cache installation and compilation was not undertaken: `Model` imports all of Mathlib, the repository recommends selective compilation, and the bounded task permits reporting why no full build was available. No repository-wide clone or build was started.

For stronger verification, prepare the exact pinned Mathlib/Lake environment, compile `OAI.GroupTheory.UniversalGroup.Main`, then run:

```lean
import OAI.GroupTheory.UniversalGroup.Main
#check OAI.UniversalFInfinity.universal_group_of_type_FInfinity
#print axioms OAI.UniversalFInfinity.universal_group_of_type_FInfinity
```

Finally run the pinned comparator configuration as described in the repository's [Comparator README](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/ComparatorChallenges/README.md). Until those steps succeed, the precise verified conclusion is **full claim scope and absence of source-level admission/axiom declarations in the 50 OAI files**, not independent machine verification of the proof.
