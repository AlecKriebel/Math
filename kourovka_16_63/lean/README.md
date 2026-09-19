# Kourovka 16.63 — partial Lean development

**Local repair and audit edition · 18 September 2026.**

This is a partial formalization of ingredients of the construction in
[the paper](https://aleckriebel.github.io/Math/papers/kourovka-16-63/).
**It does not prove the final finite-group theorem.** The supplied draft was
explicitly incomplete; running a compiler cannot supply its missing mathematics.

The local audit repairs actual compiler errors and expensive finite reductions.
See the accompanying `audit/VERIFICATION_REPORT.md` in the downloadable package
(or `../lean_audit_2026_09_18/VERIFICATION_REPORT.md` in the repository) for the
final module-level build status, actual axiom dependencies, and remaining gaps.
Only the modules listed as accepted in that report are claimed checked.

## The missing mathematical developments

1. Instantiate the general lifting and lattice arguments for every finite Lie
   automorphism and every derivation solution.
2. Construct the integral exponential/logarithm bijection with the required
   finite precision and prove its hypotheses.
3. Prove acceptance of the actual Smith certificate and the resulting full
   derivation-kernel cardinality.
4. Construct the BCH group and prove the full correspondence with ordinary
   `MulAut`, then prove the unconditional notebook theorem.

`Kourovka.Challenge.ExactOrders` and `NotebookAffirmative` define the intended
propositions. Neither has a proof in this package. The generic certificate and
factorization theorems retain their explicit hypotheses.

## Reproduce the source checks

Install Lean/Lake **4.19.0**, Python 3.10 or later, and Git. Mathlib and every
transitive dependency are pinned in `lake-manifest.json`.

```sh
python3 scripts/check.py --bootstrap --cache --milestones
```

The runner compiles every local module in dependency order with one compiler
process at a time, then inspects actual declaration types and transitive axiom
dependencies. Large exact computations use `decide +kernel`, split into small
cases; they do not use `native_decide`. A successful current-source build still
is not the absent group theorem. Cached upstream Mathlib objects are used;
this is not a rebuild of the dependency stack from source.

For a selected module and its complete local import closure:

```sh
python3 scripts/check.py --module Kourovka.TableCertificate
```

The default final-result gate intentionally fails:

```sh
python3 scripts/check.py
# INCOMPLETE_FINAL_GROUP_THEOREM_ABSENT
```

See `docs/OFFLINE_GUIDE.md` for detailed options. Static/Python tests are
supplementary checks, not Lean proof checking.

## Provenance and review scope

The intake ZIP was `kourovka_16_63_lean_source_2026-09-17.zip`. The accompanying
audit records its hash, the original source hashes, compiler repairs, and local
check outputs. Original cloud-session reports and instructions under
`reference/`, `SESSION_REPORT.md`, and historical logs are retained as provenance;
their uncompiled status describes that earlier delivery. Some source-header
comments also retain that historical wording; the current report and
`progress.json` determine the checked status. They are not instructions
to the reader or evidence of local compiler acceptance.

The paper and original exact certificates remain version 1.1.0, DOI
`10.5281/zenodo.22770864`, Git tag `kourovka-16-63-v1.1.0`. This Lean supplement
does not change the paper or claim that the complete result is machine checked.
It does not establish external human peer review.
