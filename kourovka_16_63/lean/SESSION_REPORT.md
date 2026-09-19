> **Historical delivery record — 17 September 2026.** The uncompiled status below describes the original cloud delivery. See the current root README, `progress.json`, and accompanying local verification report for the repaired source and actual compiler results.

# Expanded Lean source report
## Kourovka Notebook 16.63 · source revision 0.1.0 · 17 September 2026

**Delivered:** a standalone expanded Lean source package with substantive proof
bodies and exact small witnesses for offline compilation and repair.
**Not delivered:** a compiled or complete formalization of the finite-group theorem.

This continuation follows the user's explicit source-only instruction. No Lean
installation or execution was attempted. No remote repository, branch, CI job,
publication artifact, or DOI was changed; nobody was contacted and no money was
spent. The prior environment-failure records are historical, not new attempts.

## 1. Mathematical source written

### The explicit Lie ring, not an abstract substitute

The source fixes the raw unnormalized transvectants, original basis order,
149-term original bracket, the actual adapted basis change, weights
`(0,0,1,2,...,2)`, and the 199-term scaled bracket. It includes proof bodies for
coefficient identity, bilinearity, alternation, and Jacobi on arbitrary vectors.
The finite coefficient checks are paired with general basis-extensionality
arguments; checking a list of triples alone is not the proposed formal theorem.

`Ambient.lieRing`, `Lattice.lieRing`, and `Finite.lieRingAt` are explicit
structure values with proof fields, not axioms. The integral map
`embed = P ∘ diag(1009^(2+weight))` is used to connect the scaled bracket with
the original one and to prove its identities. No Lie-ring structure is falsely
assumed on the intermediate lattice A with the unscaled bracket.

`Finite.LAt i` is the actual coordinate type `Fin 31 → ZMod (1009^i)`.
The source includes reduction/lift identities, the exact reduction kernel,
cardinality, and the p-adic additive quotient equivalence. It contains a proof
draft that every bracket monomial of length at least 847 vanishes at depth
1689, and that mathlib's lower-central term of index 846 is zero. The
coordinate cardinality is not mislabeled as a theorem about a BCH group that
has not yet been constructed.

### Both flag-rigidity arguments

`Flag/Rigidity.lean` now contains full proof bodies for
`full_flag_rigidity` and `infinitesimal_flag_rigidity`, plus a wrapper for
ordinary mathlib Lie equivalences. The full argument takes an **arbitrary**
bracket-preserving linear bijection preserving the actual flag. It assumes
neither connectedness of an automorphism group nor membership in a selected
subgroup.

The concrete coordinate argument, the four h-weight projectors and the three
raw brackets that eliminate the remaining sign are all connected to the actual
bracket. The finish uses the 88-node generation chain for all 31 basis vectors.
The same chain is used to conclude that a derivation killing x and y is zero.

This direct route bypasses the finite-field automorphism classification and
cohomology calculations for the required stabilizer facts. It does not claim
that every proposition in the original paper has been formalized.

### Integral generation and representative-lifting ingredients

`Lattice/IntegralGeneration.lean` supplies cleared-denominator integer
expressions, exact target values, and their transport to the p-adic integers.
Every denominator is handled as a unit at 1009. The proof body for
`padic_generation` consequently concerns the actual p-adic coefficient ring,
not only the finite-field reduction.

`Lattice/Precision.lean` supplies the scaled-bracket error calculation and
`i-6` enlargement in a torsion-free common module, as well as word-induction
preservation by approximate automorphisms and derivations. `WeightedFlags`
connects lattice preservation with the flag. `NearIdentity` retains the actual
two-lattice loss in powers of a small endomorphism and supplies a finite
geometric inverse. The concrete arbitrary-quotient-representative lifting
assembly is still missing.

### Full Lie automorphisms and the actual derivation matrix

`Finite/LieAutomorphisms.lean` connects ordinary `LieEquiv Int` automorphisms,
residue-ring-linear Lie automorphisms, and **all** invertible bracket-preserving
matrices. This uses the separate automatic-linearity proof for arbitrary
additive endomorphisms. It does not identify a restricted family with the full
set by definition.

`Certificates/DerivationMatrix.lean` constructs K from the actual bilinear
bracket and proves the exact relation between its complete kernel and the
Leibniz equations for all linear maps. `Indexing` provides the lexicographic
row/column convention behind the 14415-by-961 matrix.

`InnerRank` contains a new small rational left-inverse certificate for 30 actual
inner-derivation directions. Its proof bodies put those directions in the
actual matrix kernel and prove injectivity. `InnerScalarExtension` transports
the witness itself to every characteristic-zero field, supplying a draft
`characteristic_zero_rank_upper` theorem. This is the independent rank bound
needed to rule out hidden higher-valuation invariants; a finite-precision zero
residual alone does not establish it.

### Kernel counting and analytic/BCH helpers

The scalar-kernel modules give explicit equivalences and counting proof bodies
for multiplication by c on `ZMod(c*q)`, including composite moduli, followed by
diagonal/padded kernels and transport under invertible coordinate changes.
`Elementary` includes genuine proof bodies for invertible shears, permutations
and verified unit rescalings, and for a generic operation-circuit checker.
**The actual 931-pivot Smith plan has not been translated into an accepted
Lean certificate.**

The tensor module defines the actual nonlinear action and its three commuting
differential operators. It includes the exact factorization-to-kernel argument
with its factorization and unit hypotheses explicit. It does not prove the
actual exponential/logarithm convergence, integrality or inverse identities.

The BCH-side modules give a Dynkin-Specht-Wever reconstruction proof draft for
Lie words and a collected-coefficient soundness theorem for homogeneous
integer Lie polynomials, with the necessary injective scalar hypothesis
visible. These are useful algebraic ingredients, not a finite Lazard theorem.
There is no BCH group multiplication or ordinary `MulAut G` count yet.

## 2. What was executed

All current tests below are external Python computations or static source
checks. None executed Lean or established a kernel-checked theorem.

| Executed check | Inspected result |
| --- | --- |
| Original frozen-input integrity | The original bracket, group JSON and Smith text retain their recorded SHA-256 and publication-tag Git blob identities |
| Raw coefficient and direct-flag checker | 4495 integer basis Jacobi triples, 12 special identities, 88 generation nodes and 31 targets passed; incorrect normalization rejected |
| Scaled bracket reconstruction | All 465 increasing-index basis pairs and all 199 scaled terms matched; 31 adapted inverse-vector controls passed |
| New inner-direction witness | All 900 rational left-inverse equations passed; 142 nonzero entries and their Lean literals matched; corrupted inverse rejected |
| Cleared-denominator generation witness | All 88 nodes, 31 targets and unit-denominator conditions passed; Lean vector literals matched; corrupted vector rejected |
| Scalar kernel controls | All 196 complete small cases for c,q from 1 through 14 passed |
| Dynkin controls | 420 exact Lie-word examples through degree 4 passed; this is not a general proof |
| Deterministic witness regeneration | Both new stored witness files reproduced exactly |
| Source and runner checks | All current local modules are in the root import closure; no forbidden direct admission/native-proof pattern was found; runner rejection controls passed |
| Default final gate | Expected exit 2: `INCOMPLETE_FINAL_GROUP_THEOREM_ABSENT` |

The final `source_evidence.py` run recorded approximately **0.27 seconds** wall
time under Python 3.13.5. That is an external small-witness check, not a measured
Lean checking time. No current Lean runtime or memory observation exists.

The original C++ Smith reproduction was executed in the **previous** session
and is retained only as historical evidence. It was not rerun or counted as a
new verification here.

## 3. Remaining substantive mathematics

Four major paths remain: the concrete arbitrary-representative lifting theorem;
the actual integral exponential/logarithm and same-precision full-set bijection;
a sound and accepted actual Smith certificate with the actual K kernel count;
and a validated finite BCH group with **both directions** of the full
group/Lie-ring automorphism correspondence. The final exact orders and notebook
corollary follow only after those paths are closed.

These gaps are in addition to compiler/API repairs in the present uncompiled
source. See `docs/REMAINING_OBLIGATIONS.md` for the exact written and unwritten
parts of each path. No completion percentage is inferred from source size.

## 4. Offline handoff

Start from the package directory, with Lean/Lake 4.19.0 available:

```sh
python3 scripts/check.py --bootstrap --cache --module Kourovka.Parameters
```

This is an **unexecuted** first compiler command. Then follow
`docs/OFFLINE_GUIDE.md`, especially `Kourovka.Flag.Rigidity` and the concrete Lie
modules. After deliberate source edits, use `--prepare-audit` to regenerate the
static inventory and actual-query requests. `--milestones` compiles all current
source; it never certifies the absent final group theorem.

The intended strict source check is

```sh
python3 scripts/check.py --bootstrap --fresh --recheck --milestones
```

It has not run. Actual axiom lists remain unknown, not empty. The optional
rechecker uses Lean's kernel rather than an independent implementation. Exact
elaborated statement fidelity still requires review.

## 5. Provenance and preservation

The paper target remains DOI `10.5281/zenodo.22770864`, tag
`kourovka-16-63-v1.1.0`, publication commit
`b575b59086c1f9756c4c65991f6aa8905a73304e`. The exact DOI archive identity is
still unverified; the historical locally attached report is labeled as such.
The earlier provenance record and source-only instruction are preserved.

The new package is version-pinned and self-contained as source/certificate
input; it does not bundle Lean or Mathlib binaries. The outer local Git metadata
identifies the source-preservation commit. The previous checkpoint's bundle is
separated into `history/`. Nothing was pushed to a public repository.
