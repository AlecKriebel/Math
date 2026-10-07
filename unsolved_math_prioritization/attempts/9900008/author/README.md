# 9900008: diffuse allocation-only mass-stationarity

**Author verdict: claimed_solved, negative answer; independent review pending.**

The general background-free implication is refuted on R² by a deterministic diffuse measure supported on periodically spaced horizontal lines with alternating densities 1 and 2. Pointwise covariance and the stabilizers force each preserving allocation to preserve the root type, whereas the defining mass resampling changes root type with probability 2/3.

This is a source-scoped authored proof candidate, not a novelty claim, human-refereed result, or formal machine proof. The original unequal-weight atomic obstruction and the nearby authored atomic control are credited. The new item being submitted for audit is their explicit diffuse invariant-direction lift and its full source-scope analysis.

## Files

* `PROOF.md`: complete measurable model, allocation rigidity, noninjectivity and origin-exception checks, direct mass-stationarity violation, and optional Palm check
* `SOURCE_AUDIT.md`: exact source scope, existing special-case results, prior-work gate and retrieval limits
* `PUBLIC_METADATA.json`: corpus/source hashes, byte counts and public-history metadata
* `certificate.json` and `verify.py`: portable exact algebra and geometric controls
* `verification_results.json`: recorded execution and adversarial-control results
* `MANIFEST.json`: hashes of the payload files

## Reproduction

Run `python verify.py --self-test` and `python verify.py --integrity` from any working directory using the script's actual path. Python's standard library is sufficient. `python -O`, `python -I`, and `python -I -O` are supported and tested. The script uses explicit guards rather than assertions.

The checker exhausts the two-family quotient mass cases and tests exact rational shifted unit windows and line translations. These checks supplement the analytic proof; they do not replace its measurability or universal allocation argument.

## Scope

The example has an invariant horizontal direction and is singular with respect to planar Lebesgue measure. It does not address modified freeness or positive-density problems, the one-dimensional diffuse theorem, or the separately stronger Markovian-kernel premise. No source PDFs, source text, dataset records, or private coordination files are included.

One substantive proof-search approach was used (invariant-direction lift, simplified to a periodic two-family model). No GitHub or queue changes were made by this author package.
