# Publication acceptance: weighted affine-line endpoint partials

Problem 30003235 / OWR-15169-009, rank 995. Acceptance date: 8 October 2026 UTC.

## Disposition and credited scope

Accept the five scoped partial approaches and the independent AI-assisted mathematical audit. The intended positive-weight, nonzero-slope endpoint remains **unsolved, 5/5 approaches used**. No mathematical correction was required. Publication adds no sixth proof-search approach. This is not conventional human peer review, formal theorem-prover certification, a novelty certificate or an exhaustive current-openness finding.

The target is the removal of positive epsilon from the affine-line coefficient condition in Hanna Husakova's overview, printed p. 2780 of [Oberwolfach Reports 48/2016](https://doi.org/10.4171/OWR/2016/48). The intended hypotheses are positive weights and nonzero slope, as in [An–Beresnevich–Velani, Theorem 1.2](https://doi.org/10.1016/j.aim.2017.11.009). The paper already covers nonzero rational slopes at the endpoint. The original overview's wider literal horizontal scope fails, as proved in the author packet; this is not a counterexample to the intended endpoint.

## Accepted results and precise gaps

1. Exact critical continued-fraction families separate the endpoint assumption from every strict-exponent assumption. The explicit horizontal counterexample corrects only the wider literal scope. The dual necessity argument is credited to the known theorem and does not prove sufficiency.
2. The endpoint condition implies a simultaneous winning/full-dimensional consequence at selected nearby noncritical weights by the credited ABV theorem. The constants need not persist at the limiting critical weight.
3. Rational translations and inversion through the heavier coordinate preserve weighted bad membership. Together with the credited coordinate-fiber theorem, this gives dimension one in every relatively open interval for nonzero-slope lines containing a rational point, for all positive weights summing to one. Coordinate exchange covers the other weight ordering. Unrestricted real-affine/projective invariance is not asserted.
4. Quantitative near-parallel resonance elimination identifies the endpoint's missing scale decay. It does not establish a general deletion count.
5. A weighted determinant bound forces height-window coefficient vectors to have rank at most two. A rational pencil does not by itself bound dangerous-interval unions or produce positive branching and a dimension-one Cantor set.

The unresolved case is general irrational a with b outside Q+Qa. The rational-point result uses weighted transference and the coordinate-fiber theorem as credited inputs. [An's original theorem](https://arxiv.org/abs/1203.2996) was checked at its statement during the audit, not re-proved in full. Later nondegenerate-curve results do not automatically cover affine lines. The [source audit](original/SOURCE_AUDIT.md), [source identities](original/SOURCE_IDENTITIES.json) and [full independent review](independent_audit/FULL_REPORT.md) retain exact inspection boundaries.

## Frozen provenance and optional qualifications

- Author original: 17 files; MANIFEST.json SHA-256 b499c40203ef2203d86d3dd6fd6e612944d7cbad92edb801170626965bc07b90.
- Independent audit: 11 files; AUDIT_MANIFEST.json SHA-256 ee06ce6399f65b6775d4f7e892dc91efd133e47e236197a00b84fba33f268eca.

Both slices, including historical stage wording, are immutable. The author README's awaiting-review wording describes its earlier freeze; the separate audit and this acceptance supply the subsequent review. No corrected slice is needed.

The audit's optional nonblocking notes are preserved separately: explicitly writing the rational-translation constant c/d^(1+1/sigma); expanding local bi-Lipschitz reasoning on intervals away from the inversion pole; and recognizing that the original optional external --probes interface permits repeated kinds rather than requiring exactly one of each kind. The publication replay includes a positive repeated-kind control to preserve that honest interface qualification. None is represented as a missing mathematical proof inference or a required correction.

## Verification and boundary

The original checker performs 9,485 finite checks and the separately written checker 9,638. Historical negative controls, exact output replay and actual write-rejected read-only relocation are exercised under ordinary, -O and -OO execution. The publication wrapper requires an externally pinned outer manifest, strict file/directory/type inventory, immutable inner pins, duplicate-key and nonfinite JSON rejection, and no symlink or special-file payloads. It rejects mutation fixtures, including rebound frozen checkers and separately bootstrapped verifier substitutions. A separately trusted verifier hash must be checked before executing that verifier.

The portable packet contains authored mathematical text, code, audits, acceptance and public source metadata only. PDFs, copied source text, extracted documents, dataset contents and private coordination material are excluded. Source-byte reverification is not run from this source-free packet. Finite controls do not establish universal theorems, and these checks are not a hostile-code execution sandbox or a filesystem-race defense.
