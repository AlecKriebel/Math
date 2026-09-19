# Kourovka 16.63: local Lean repair and scope audit

Audit edition: 18 September 2026 (America/Los_Angeles; detailed logs use UTC).

## Verdict

**This is a partial formalization. The complete finite-group theorem is not
proved in Lean.** The supplied source explicitly recorded that limitation.
The local work runs and repairs its existing proof developments and audits
their scope; it does not fill the four missing mathematical developments.
This finding concerns the formalization's completeness and does not by itself
refute the paper.

The target is an actual nontrivial finite group of odd prime-power order with
the same order as its **full ordinary automorphism group**. The concrete paper
target is `|G| = |MulAut G| = 1009^52359`. The declarations
`Kourovka.Challenge.ExactOrders` and `NotebookAffirmative` define those intended
propositions. They are not proofs of them, and importing them does not prove
them.

## Compiler verification

**All 142 current production/root modules compile with Lean 4.19.0.** The
aggregate root also compiled successfully after its dependencies. Actual
transitive axiom and full-type queries passed for all **1,262 statically
inventoried public named declarations**. The only reported axioms are
`propext`, `Classical.choice`, and `Quot.sound`. No admission or custom problem
axiom was found; native decision procedures were not used.

Each module was compiled during the repair process. The final check matched
source/object hashes, rejected missing or stale objects, verified pinned
dependency cleanliness, and confirmed that the source/object/protected-input
snapshot stayed unchanged during the queries. The independent semantic
review's hashes match the same final 142 source files.

This was **per-module compilation followed by a final aggregate import and
object audit**, not a single fresh `check.py --milestones` run. Importing
objects alone does not recompile their source. Hashes and conservative
timestamp checks complement the recorded individual compiler acceptances;
they are not independently a proof of source-to-object correspondence. The
named-root inventory is not an exhaustive inventory of generated, anonymous,
or private declarations. Their dependencies are audited transitively when
used by queried roots, and all production source is included in compilation.

### What is checked

| Area | Checked result and scope |
| --- | --- |
| Original bracket | Equality with the raw integral formula, complete basis checks, and the ambient Lie-ring construction over arbitrary commutative rings. |
| Flags | Concrete finite-field generation and full/infinitesimal rigidity **under the stated flag-preservation hypotheses**. |
| Integral lattice | All 31 embedding slices, the scaled Lie ring, and p-adic generation. |
| Finite Lie ring | The coordinate carrier has cardinality `1009^52359`; its 846th lower-central term is zero, meaning class at most 846. All Lie-ring automorphisms are identified with all invertible bracket-preserving matrices; their number is not evaluated. |
| Derivations and rank | The actual derivation matrix and complete-kernel equivalence; 900 exact left-inverse identities; the rank upper bound 931 over every characteristic-zero field. |
| Counting infrastructure | Scalar/diagonal kernel counts and soundness of generic elementary circuits, conditional on their actual acceptance. No actual Smith replay is proved. |
| Analytic/BCH ingredients | Finite geometric inverses, conditional tensor-factorization results, Lie-word reconstruction and coefficient soundness. No BCH group or complete exp/log correspondence is constructed. |

### Evidence and semantic review

- `key_statements.log`: concise actual Lean output showing the two unproved
  target definitions, full automorphism types, explicit flag hypotheses,
  coordinate cardinality, nilpotency conclusion, and rank bound. Its
  `KeyStatements.lean` inspection command exited zero.
- `latest_accepted_object_audit.json` and
  `accepted_object_audits/20260919T045141.564977Z/manifest.json`: complete
  source/object manifest, actual per-declaration axiom lists, commands and
  before/after snapshots. Both actual query commands exited zero.
- `lean/logs/runs/20260919T045141.724341Z/029_accepted_object_axioms.log` and
  `030_accepted_object_statements.log`: actual compiler output. In the
  repository, these paths are under the sibling `../lean/` directory.
- `root_build_final.json`, `ambient_split_success/`, `embedding_rows/`,
  `inner_rows/`, and the module-family repair reports: compilation records.
- `frozen_semantic_review.md`, `final_semantic_source_snapshot.json`, and
  `final_statement_comparison.json`: independent comparison against the
  supplied ZIP. Of 821 original explicit theorem statements, 815 match
  textually after whitespace normalization; six changes clarify intended
  types/coercions. The final source contains 865 explicit theorem statements.
  No weakened original claim, changed target, altered mathematical data, or
  narrowed automorphism set was found. These counts are source-review
  metadata, not a separate proof-completeness metric.

The repairs include imports/API use, coercions and casts, explicit structure
construction, targeted rewrites, and bounded kernel reductions. Increased
resource limits enable computation of the actual modulus and do not add a
mathematical assumption. Earlier failed attempts remain separately recorded.

## Missing mathematical developments

1. **Concrete lifting.** Instantiate the general error, generation, weighted
   lattice, and flag arguments for representatives of every automorphism and
   every derivation of the actual finite quotient. Existing lemmas retain
   explicit integrality, preservation, and compatibility hypotheses.
2. **Integral exp/log.** Construct the maps, establish integrality and inverse
   identities at the required precision, and prove the full bijection. A
   conditional tensor-factorization lemma and a finite geometric inverse do
   not supply that construction.
3. **The actual Smith certificate.** Supply a concrete transformation for the
   14,415-by-961 derivation matrix, prove acceptance of the 931-pivot
   computation, and instantiate the complete kernel count. Generic elementary
   operations and diagonal-kernel formulas do not establish that acceptance.
4. **The BCH group and all its automorphisms.** Construct the multiplication,
   prove the group laws and both directions of the ordinary group/Lie
   automorphism correspondence, and conclude the exact orders and notebook
   theorem. A finite Lie-ring carrier and its cardinality do not supply this.

The independent analysis in `independent_scope_audit.md` identifies the actual
hypotheses and explains why the existing results do not imply these missing
steps. No custom final-result axiom, mock BCH group, assumed Smith acceptance,
or selected automorphism subgroup has been used to hide the gaps.

## Reproducibility and trust boundary

- Lean/Lake: `leanprover/lean4:v4.19.0`.
- Mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`.
- All dependency revisions are pinned in `lean/lake-manifest.json`.
- The audit used cached objects for the pinned upstream dependencies. Their
  revisions and source cleanliness were checked; the entire dependency stack
  and compiler were not rebuilt from source.
- Large concrete decisions use `decide +kernel`. They were split into finite
  cases to bound memory. No compiler-trusting native decision procedure is
  introduced.
- Static inventories and Python computations are supplementary evidence.
  They are not Lean elaboration or proof checks.
- A separate implementation of Lean's kernel has not been run. An AI audit
  does not establish external human peer review.

For a fresh sequential compilation of the complete local source, followed by
actual declaration-type and transitive axiom inspection, enter `lean/` and run:

```sh
python3 scripts/check.py --bootstrap --cache --milestones
```

This is the reproduction command, not a claim that the supplied project
contains the absent final theorem. The bounded runner deletes the selected
project's old objects before compiling; one failed prerequisite blocks its
dependents. It rejects missing outputs, changed sources, timeouts and
unexpected axiom dependencies. Its regression controls are recorded in
`runner_repair.md` and the accompanying JSON files.

The default command `python3 scripts/check.py` deliberately fails with
`INCOMPLETE_FINAL_GROUP_THEOREM_ABSENT`. That failure is a truthful final-result
gate, not a compiler failure to be suppressed.

## Provenance and publication

`intake.json` and `original_source_hashes.json` identify the untouched supplied
ZIP. `data_integrity.json` compares the original mathematical inputs with the
paper's inputs. The witness regeneration and literal checks were rerun after
moving the data declarations into smaller modules; see
`external_evidence_final.json`, `witness_regeneration_final.json`,
`literal_export_final.log`, and `direct_flag_final.json`. Deliberately corrupted
small witnesses are rejected. These external computations are explicitly
separate from Lean acceptance.

The download includes current source, pinned environment descriptions, repair
reports, logs, and a SHA-256 manifest. It excludes compiler objects and
dependency caches. Historical cloud reports and failed local attempts are
retained and identified as such; see this folder's `README.md`.

The version 1.1.0 paper, original source-and-certificates archive, and Zenodo
upload kit are unchanged. The supplied DOI is `10.5281/zenodo.22770864`.
This supplement creates no GitHub release and no new DOI.
